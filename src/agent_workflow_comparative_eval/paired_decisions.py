from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Any

from .constants import PAIRED_DECISION_REPORT_SCHEMA, PAIRED_DECISION_TRIAL_SCHEMA
from .contracts import validate_record
from .identity import sha256
from .statistics import mcnemar_exact_p_value, paired_bootstrap_interval, wilson_interval

_ARM_STATUSES = {"success", "error", "timeout", "cancelled"}
_PAIR_CLASSES = {
    "both_correct",
    "both_incorrect",
    "control_only_correct",
    "treatment_only_correct",
}


def _normalized_arm(value: Mapping[str, Any], *, treatment: bool) -> dict[str, Any]:
    status = str(value.get("status", ""))
    if status not in _ARM_STATUSES:
        raise ValueError(f"invalid paired-decision arm status: {status!r}")
    raw_score = value.get("official_score")
    score_available = (
        isinstance(raw_score, (int, float))
        and not isinstance(raw_score, bool)
        and float(raw_score) in {0.0, 1.0}
    )
    official_score = float(raw_score) if score_available else None
    decision_record = value.get("decision_record")
    if decision_record is not None and not isinstance(decision_record, Mapping):
        raise ValueError("decision_record must be an object or null")
    selected = value.get("selected_proposal_id")
    if selected is not None and (not isinstance(selected, str) or not selected.strip()):
        raise ValueError("selected_proposal_id must be a non-empty string or null")
    arm = {
        "status": status,
        "score_available": score_available,
        "official_score": official_score,
        "correct": bool(score_available and official_score == 1.0),
        "selected_proposal_id": selected,
        "decision_record": dict(decision_record) if isinstance(decision_record, Mapping) else None,
        "usage": dict(value.get("usage", {})) if isinstance(value.get("usage"), Mapping) else {},
        "duration_seconds": value.get("duration_seconds"),
        "error_class": value.get("error_class"),
    }
    if treatment:
        jev = value.get("jev")
        if not isinstance(jev, Mapping):
            raise ValueError("treatment arm requires a jev evidence object")
        tool_calls = int(jev.get("tool_calls", 0))
        successful_calls = int(jev.get("successful_calls", 0))
        if tool_calls < 0 or successful_calls < 0 or successful_calls > tool_calls:
            raise ValueError("invalid Jev tool call counts")
        request_hashes = jev.get("request_hashes", [])
        if not isinstance(request_hashes, Sequence) or isinstance(request_hashes, (str, bytes)):
            raise ValueError("Jev request_hashes must be an array")
        hashes = [str(item) for item in request_hashes]
        context_complete = jev.get("context_complete")
        context_known_calls = jev.get("context_known_calls")
        context_complete_calls = jev.get("context_complete_calls")
        if context_known_calls is None:
            context_known_calls = 1 if successful_calls > 0 and context_complete is not None else 0
        if context_complete_calls is None:
            context_complete_calls = 1 if context_complete is True and context_known_calls else 0
        context_known_calls = int(context_known_calls)
        context_complete_calls = int(context_complete_calls)
        if not 0 <= context_complete_calls <= context_known_calls <= successful_calls:
            raise ValueError("invalid Jev context completeness counts")
        resolved_models = jev.get("resolved_models", [])
        if not isinstance(resolved_models, Sequence) or isinstance(resolved_models, (str, bytes)):
            raise ValueError("Jev resolved_models must be an array")
        models = sorted({str(item).strip() for item in resolved_models if str(item).strip()})
        arm["jev"] = {
            "tool_calls": tool_calls,
            "successful_calls": successful_calls,
            "context_complete": context_complete,
            "context_known_calls": context_known_calls,
            "context_complete_calls": context_complete_calls,
            "resolved_models": models,
            "request_hashes": hashes,
        }
    return arm


def _pair_class(control_correct: bool, treatment_correct: bool) -> str:
    if control_correct and treatment_correct:
        return "both_correct"
    if control_correct:
        return "control_only_correct"
    if treatment_correct:
        return "treatment_only_correct"
    return "both_incorrect"


def make_paired_decision_trial(
    *,
    study_id: str,
    sample_id: str,
    repetition: int,
    source: Mapping[str, Any],
    runtime: Mapping[str, Any],
    control: Mapping[str, Any],
    treatment: Mapping[str, Any],
    privacy: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if repetition < 0:
        raise ValueError("repetition must be nonnegative")
    control_arm = _normalized_arm(control, treatment=False)
    treatment_arm = _normalized_arm(treatment, treatment=True)
    control_selected = control_arm["selected_proposal_id"]
    treatment_selected = treatment_arm["selected_proposal_id"]
    changed = (
        control_selected != treatment_selected
        if control_selected is not None and treatment_selected is not None
        else None
    )
    pair_class = _pair_class(control_arm["correct"], treatment_arm["correct"])
    record = {
        "schema": PAIRED_DECISION_TRIAL_SCHEMA,
        "study_id": study_id,
        "sample_id": sample_id,
        "repetition": repetition,
        "source": dict(source),
        "runtime": dict(runtime),
        "control": control_arm,
        "treatment": treatment_arm,
        "pair": {
            "classification": pair_class,
            "decision_changed": changed,
            "treatment_minus_control_correctness": int(treatment_arm["correct"]) - int(control_arm["correct"]),
        },
        "privacy": dict(
            privacy
            or {
                "raw_provider_content_stored": False,
                "secret_values_stored": False,
            }
        ),
    }
    validate_paired_decision_trial(record)
    return record


def validate_paired_decision_trial(value: Mapping[str, Any]) -> None:
    validate_record(value, PAIRED_DECISION_TRIAL_SCHEMA)
    expected = _pair_class(bool(value["control"]["correct"]), bool(value["treatment"]["correct"]))
    if value["pair"]["classification"] != expected:
        raise ValueError("paired-decision classification does not match arm correctness")
    expected_delta = int(bool(value["treatment"]["correct"])) - int(bool(value["control"]["correct"]))
    if value["pair"]["treatment_minus_control_correctness"] != expected_delta:
        raise ValueError("paired-decision correctness delta is inconsistent")
    if value["privacy"]["raw_provider_content_stored"] is not False:
        raise ValueError("paired-decision trial cannot persist raw provider content")
    if value["privacy"]["secret_values_stored"] is not False:
        raise ValueError("paired-decision trial cannot persist secret values")


def _decision_field_present(arm: Mapping[str, Any], field: str) -> bool:
    record = arm.get("decision_record")
    return isinstance(record, Mapping) and isinstance(record.get(field), str) and bool(str(record[field]).strip())


def _numeric(value: Any) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return None


def _usage_value(value: Any, aliases: Sequence[str]) -> float | None:
    if not isinstance(value, Mapping):
        return None
    for key in aliases:
        numeric = _numeric(value.get(key))
        if numeric is not None:
            return numeric
    children = [_usage_value(child, aliases) for child in value.values() if isinstance(child, Mapping)]
    known = [item for item in children if item is not None]
    return sum(known) if known else None


def _paired_overhead(
    normalized: Sequence[Mapping[str, Any]],
    *,
    getter: Any,
    label: str,
    confidence: float,
    minimum_interval_n: int,
) -> dict[str, Any]:
    control_values: list[float] = []
    treatment_values: list[float] = []
    deltas: list[float] = []
    for item in normalized:
        control = getter(item["control"])
        treatment = getter(item["treatment"])
        if control is None or treatment is None:
            continue
        control_values.append(float(control))
        treatment_values.append(float(treatment))
        deltas.append(float(treatment) - float(control))
    n = len(deltas)
    return {
        "known_paired_n": n,
        "control_mean": sum(control_values) / n if n else None,
        "treatment_mean": sum(treatment_values) / n if n else None,
        "treatment_minus_control_mean": sum(deltas) / n if n else None,
        "paired_bootstrap": (
            paired_bootstrap_interval(deltas, label=label, confidence=confidence)
            if n >= minimum_interval_n
            else None
        ),
    }


def build_paired_decision_report(
    trials: Sequence[Mapping[str, Any]],
    *,
    study_id: str,
    study_version: str,
    confidence: float = 0.95,
    minimum_interval_n: int = 10,
) -> dict[str, Any]:
    if not trials:
        raise ValueError("paired-decision report requires at least one trial")
    if minimum_interval_n < 2:
        raise ValueError("minimum_interval_n must be at least 2")
    seen: set[tuple[str, int]] = set()
    normalized: list[Mapping[str, Any]] = []
    for trial in trials:
        validate_paired_decision_trial(trial)
        if trial["study_id"] != study_id:
            raise ValueError("paired-decision trial belongs to another study")
        key = (str(trial["sample_id"]), int(trial["repetition"]))
        if key in seen:
            raise ValueError(f"duplicate paired-decision trial key: {key}")
        seen.add(key)
        normalized.append(trial)

    n = len(normalized)
    source_hashes = {sha256(item["source"]) for item in normalized}
    runtime_hashes = {sha256(item["runtime"]) for item in normalized}
    if len(source_hashes) != 1:
        raise ValueError("paired-decision report cannot mix source identities")
    if len(runtime_hashes) != 1:
        raise ValueError("paired-decision report cannot mix runtime identities")
    cohort_hashes = {str(item["source"].get("cohort_sha256", "")) for item in normalized}
    if len(cohort_hashes) != 1 or not next(iter(cohort_hashes)):
        raise ValueError("paired-decision report requires one frozen cohort_sha256")
    source_sha256 = next(iter(source_hashes))
    runtime_sha256 = next(iter(runtime_hashes))
    cohort_sha256 = next(iter(cohort_hashes))
    pair_keys_sha256 = sha256(sorted(seen))
    control_correct = [bool(item["control"]["correct"]) for item in normalized]
    treatment_correct = [bool(item["treatment"]["correct"]) for item in normalized]
    deltas = [
        float(int(treatment) - int(control))
        for control, treatment in zip(control_correct, treatment_correct, strict=True)
    ]
    counts = Counter(str(item["pair"]["classification"]) for item in normalized)
    control_only = counts["control_only_correct"]
    treatment_only = counts["treatment_only_correct"]
    interval = (
        paired_bootstrap_interval(
            deltas,
            label=f"{study_id}:{cohort_sha256}:{pair_keys_sha256}:accuracy",
            confidence=confidence,
        )
        if n >= minimum_interval_n
        else None
    )
    treatment_calls = [int(item["treatment"]["jev"]["tool_calls"]) for item in normalized]
    treatment_successes = [int(item["treatment"]["jev"]["successful_calls"]) for item in normalized]
    context_values = [
        item["treatment"]["jev"].get("context_complete")
        for item in normalized
        if int(item["treatment"]["jev"]["successful_calls"]) > 0
    ]
    context_known_calls = sum(int(item["treatment"]["jev"].get("context_known_calls", 0)) for item in normalized)
    context_complete_calls = sum(int(item["treatment"]["jev"].get("context_complete_calls", 0)) for item in normalized)
    resolved_models = sorted({
        model
        for item in normalized
        for model in item["treatment"]["jev"].get("resolved_models", [])
    })
    known_changes = [item["pair"]["decision_changed"] for item in normalized if item["pair"]["decision_changed"] is not None]
    changed = sum(value is True for value in known_changes)

    record = {
        "schema": PAIRED_DECISION_REPORT_SCHEMA,
        "study_id": study_id,
        "study_version": study_version,
        "cohort_sha256": cohort_sha256,
        "paired_n": n,
        "identity": {
            "source_sha256": source_sha256,
            "runtime_sha256": runtime_sha256,
            "pair_keys_sha256": pair_keys_sha256,
        },
        "primary": {
            "metric": "official_swe_lancer_attempt_accuracy_difference",
            "control": {
                "correct": sum(control_correct),
                "n": n,
                "accuracy": sum(control_correct) / n,
                "wilson": wilson_interval(sum(control_correct), n, confidence),
            },
            "treatment": {
                "correct": sum(treatment_correct),
                "n": n,
                "accuracy": sum(treatment_correct) / n,
                "wilson": wilson_interval(sum(treatment_correct), n, confidence),
            },
            "treatment_minus_control_accuracy": sum(deltas) / n,
            "paired_bootstrap": interval,
            "minimum_interval_n": minimum_interval_n,
        },
        "discordant_pairs": {
            "control_only_correct": control_only,
            "treatment_only_correct": treatment_only,
            "total": control_only + treatment_only,
            "mcnemar_exact_p_value": mcnemar_exact_p_value(control_only, treatment_only),
        },
        "pair_classification_counts": {name: counts.get(name, 0) for name in sorted(_PAIR_CLASSES)},
        "decision_change": {
            "known_n": len(known_changes),
            "changed": changed,
            "rate": changed / len(known_changes) if known_changes else None,
        },
        "jev_exposure": {
            "treatment_trials": n,
            "trials_with_any_call": sum(value > 0 for value in treatment_calls),
            "trials_with_successful_call": sum(value > 0 for value in treatment_successes),
            "tool_calls": sum(treatment_calls),
            "successful_calls": sum(treatment_successes),
            "successful_call_context_complete_trials": sum(value is True for value in context_values),
            "successful_call_context_known_trials": sum(value is not None for value in context_values),
            "successful_call_context_complete_calls": context_complete_calls,
            "successful_call_context_known_calls": context_known_calls,
            "resolved_models": resolved_models,
        },
        "observable_decision_evidence": {
            "control_justification_present": sum(_decision_field_present(item["control"], "justification") for item in normalized),
            "treatment_justification_present": sum(_decision_field_present(item["treatment"], "justification") for item in normalized),
            "treatment_reconciliation_present": sum(_decision_field_present(item["treatment"], "semantic_evidence_reconciliation") for item in normalized),
        },
        "execution_reliability": {
            "control_statuses": dict(sorted(Counter(str(item["control"]["status"]) for item in normalized).items())),
            "treatment_statuses": dict(sorted(Counter(str(item["treatment"]["status"]) for item in normalized).items())),
            "control_scores_available": sum(bool(item["control"]["score_available"]) for item in normalized),
            "treatment_scores_available": sum(bool(item["treatment"]["score_available"]) for item in normalized),
            "paired_scores_available": sum(bool(item["control"]["score_available"]) and bool(item["treatment"]["score_available"]) for item in normalized),
            "attempt_scoring_rule": "missing or non-binary official score is counted incorrect in the preregistered primary attempt-level analysis",
        },
        "overhead": {
            "duration_seconds": _paired_overhead(
                normalized,
                getter=lambda arm: _numeric(arm.get("duration_seconds")),
                label=f"{study_id}:{cohort_sha256}:{pair_keys_sha256}:duration",
                confidence=confidence,
                minimum_interval_n=minimum_interval_n,
            ),
            "input_tokens": _paired_overhead(
                normalized,
                getter=lambda arm: _usage_value(arm.get("usage", {}), ("input_tokens", "prompt_tokens")),
                label=f"{study_id}:{cohort_sha256}:{pair_keys_sha256}:input_tokens",
                confidence=confidence,
                minimum_interval_n=minimum_interval_n,
            ),
            "output_tokens": _paired_overhead(
                normalized,
                getter=lambda arm: _usage_value(arm.get("usage", {}), ("output_tokens", "completion_tokens")),
                label=f"{study_id}:{cohort_sha256}:{pair_keys_sha256}:output_tokens",
                confidence=confidence,
                minimum_interval_n=minimum_interval_n,
            ),
            "total_tokens": _paired_overhead(
                normalized,
                getter=lambda arm: _usage_value(arm.get("usage", {}), ("provider_total_tokens", "total_tokens")),
                label=f"{study_id}:{cohort_sha256}:{pair_keys_sha256}:total_tokens",
                confidence=confidence,
                minimum_interval_n=minimum_interval_n,
            ),
        },
        "limitations": [
            "Correctness is imported from the official Inspect Evals SWE-Lancer scorer; this library does not redefine the gold proposal.",
            "The primary estimate is intent-to-treat for Jev availability: treatment tasks with no Jev call remain in the treatment denominator.",
            "Any called-only or successful-call-only subset is self-selected and is descriptive rather than a causal treatment estimate.",
            "A fixed cohort of this size is not well powered for small effects; report the paired interval and discordant counts alongside the point estimate.",
        ],
    }
    validate_record(record, PAIRED_DECISION_REPORT_SCHEMA)
    return record
