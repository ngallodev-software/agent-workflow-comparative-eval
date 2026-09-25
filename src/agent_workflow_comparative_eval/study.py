from __future__ import annotations

import json
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from importlib.resources import files
from typing import Any
from uuid import uuid4

from .constants import (
    DECISION_STUDY_EXCLUSION_SCHEMA,
    DECISION_STUDY_REPORT_SCHEMA,
    DECISION_STUDY_SPEC_SCHEMA,
    DECISION_STUDY_CASE_SCHEMA,
    DECISION_STUDY_ORACLE_SCHEMA,
    DECISION_STUDY_CORPUS_SCHEMA,
    DECISION_STUDY_ORACLE_BUNDLE_SCHEMA,
    OBSERVATION_SCHEMA,
    PROVIDER_REQUEST_SCHEMA,
)
from .contracts import validate_record
from .identity import sha256
from .metrics.calibration import (
    brier_score,
    expected_calibration_error,
    multiclass_brier_score,
    multiclass_log_loss,
)
from .metrics.correctness import (
    binary_classification,
    classification_metrics,
    correctness_counts,
    ordinal_metrics,
)
from .metrics.reliability import arm_reliability
from .observations import validate_observation
from .outcomes import validate_outcome
from .statistics import paired_bootstrap_interval, wilson_interval
from .timing import timing_summary
from .usage import aggregate_usage

_STUDIES = {"routing-semantic-v1": "routing-semantic-v1.study.json"}


def list_studies() -> tuple[str, ...]:
    return tuple(sorted(_STUDIES))


def load_study_spec(name: str) -> dict[str, Any]:
    try:
        filename = _STUDIES[name]
    except KeyError as exc:
        raise ValueError(f"unknown decision study: {name}") from exc
    resource = files("agent_workflow_comparative_eval").joinpath("resources", "studies", filename)
    value = json.loads(resource.read_text(encoding="utf-8"))
    validate_record(value, DECISION_STUDY_SPEC_SCHEMA)
    return value


def validate_decision_study_corpus(value: Mapping[str, Any]) -> dict[str, Any]:
    validate_record(value, DECISION_STUDY_CORPUS_SCHEMA)
    dataset_version = str(value["dataset_version"])
    seen: set[str] = set()
    cases: list[dict[str, Any]] = []
    for raw in value["cases"]:
        if not isinstance(raw, Mapping):
            raise ValueError("decision-study corpus case must be an object")
        validate_record(raw, DECISION_STUDY_CASE_SCHEMA)
        case_id = str(raw["case_id"])
        if case_id in seen:
            raise ValueError(f"duplicate decision-study case ID: {case_id}")
        if raw["dataset_version"] != dataset_version:
            raise ValueError(
                f"case {case_id} dataset_version differs from corpus dataset_version"
            )
        seen.add(case_id)
        cases.append(dict(raw))
    return {**dict(value), "cases": cases}


def validate_decision_study_oracle_bundle(
    value: Mapping[str, Any],
    *,
    expected_study_id: str | None = None,
    expected_dataset_version: str | None = None,
) -> dict[str, Any]:
    validate_record(value, DECISION_STUDY_ORACLE_BUNDLE_SCHEMA)
    study_id = str(value["study_id"])
    dataset_version = str(value["dataset_version"])
    if expected_study_id is not None and study_id != expected_study_id:
        raise ValueError("oracle bundle belongs to a different study")
    if (
        expected_dataset_version is not None
        and dataset_version != expected_dataset_version
    ):
        raise ValueError("oracle bundle dataset_version does not match inference corpus")
    seen: set[str] = set()
    records: list[dict[str, Any]] = []
    for raw in value["records"]:
        if not isinstance(raw, Mapping):
            raise ValueError("decision-study oracle record must be an object")
        validate_record(raw, DECISION_STUDY_ORACLE_SCHEMA)
        case_id = str(raw["case_id"])
        if case_id in seen:
            raise ValueError(f"duplicate decision-study oracle case ID: {case_id}")
        if raw["dataset_version"] != dataset_version:
            raise ValueError(
                f"oracle record {case_id} has a different dataset version"
            )
        seen.add(case_id)
        records.append(dict(raw))
    return {**dict(value), "records": records}


def make_provider_request(
    *,
    request_id: str,
    identity: Mapping[str, Any],
    decisions: Sequence[str],
    status: str,
    duration_seconds: float | None,
    usage: Mapping[str, Any] | None = None,
    request_sha256: str | None = None,
    error_class: str | None = None,
    recorded_at: str | None = None,
) -> dict[str, Any]:
    record = {
        "schema": PROVIDER_REQUEST_SCHEMA,
        "request_id": request_id,
        "recorded_at": recorded_at or datetime.now(timezone.utc).isoformat(),
        "identity": dict(identity),
        "decisions": list(dict.fromkeys(str(item) for item in decisions)),
        "request_sha256": request_sha256,
        "status": status,
        "duration_seconds": duration_seconds,
        "usage": dict(usage or {}),
        "error_class": error_class,
        "privacy": {"raw_content_stored": False, "secret_values_stored": False},
    }
    validate_record(record, PROVIDER_REQUEST_SCHEMA)
    return record


def make_exclusion(
    *,
    study_id: str,
    case_id: str,
    reason_code: str,
    stage: str,
    decision_id: str | None = None,
    detail: str | None = None,
) -> dict[str, Any]:
    record = {
        "schema": DECISION_STUDY_EXCLUSION_SCHEMA,
        "study_id": study_id,
        "case_id": case_id,
        "decision_id": decision_id,
        "reason_code": reason_code,
        "stage": stage,
        "detail": detail,
    }
    validate_record(record, DECISION_STUDY_EXCLUSION_SCHEMA)
    return record


def make_precomputed_decision_observation(
    *,
    feature_id: str,
    decision_id: str,
    semantic_type: str,
    identity: Mapping[str, Any],
    source_input: Mapping[str, Any],
    projected_input: Mapping[str, Any],
    control_decision: Any,
    candidate_decision: Any,
    semantic_status: str,
    request_id: str,
    probability: float | None = None,
    confidence: float | None = None,
    probabilities: Mapping[str, float] | None = None,
    policy_candidate: Any = None,
    applied_result: Any = None,
    fallback: Mapping[str, Any] | None = None,
    candidate_arm_status: str = "success",
    control_duration_seconds: float | None = None,
    candidate_policy_seconds: float | None = None,
    case_id: str | None = None,
    observation_id: str | None = None,
    data_class: str = "production-metadata",
    mode: str = "shadow-normal-usage",
) -> dict[str, Any]:
    if semantic_type not in {"choice", "noul", "score"}:
        raise ValueError("semantic_type must be choice, noul, or score")
    if candidate_arm_status not in {"success", "error", "timeout", "skipped", "not_applicable"}:
        raise ValueError("invalid candidate arm status")
    control_result = {"decision_id": decision_id, "decision": control_decision}
    candidate_result = {
        "decision_id": decision_id,
        "semantic_type": semantic_type,
        "decision": candidate_decision,
        "semantic_status": semantic_status,
        "probability": probability,
        "confidence": confidence,
        "probabilities": {str(k): float(v) for k, v in (probabilities or {}).items()},
        "policy_candidate": policy_candidate,
        "applied_result": applied_result,
        "fallback": dict(fallback or {}),
        "request_id": request_id,
    }
    record = {
        "schema": OBSERVATION_SCHEMA,
        "observation_id": observation_id or str(uuid4()),
        "feature_id": feature_id,
        "mode": mode,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "identity": dict(identity),
        "input": {
            "case_id": case_id,
            "input_sha256": sha256(source_input),
            "projection_sha256": sha256(projected_input),
            "raw_input_persisted": False,
        },
        "control": {
            "status": "success",
            "duration_seconds": control_duration_seconds,
            "result": control_result,
            "usage": {},
        },
        "candidate": {
            "status": candidate_arm_status,
            "duration_seconds": candidate_policy_seconds,
            "result": candidate_result,
            "usage": {},
        },
        "comparison": {
            "candidate_applied": False,
            "authoritative_arm": "control",
            "agreement": control_decision == candidate_decision if candidate_arm_status == "success" else None,
            "normalized_control": control_decision,
            "normalized_candidate": candidate_decision if candidate_arm_status == "success" else None,
        },
        "privacy": {
            "data_class": data_class,
            "raw_content_stored": False,
            "secret_values_stored": False,
        },
    }
    validate_observation(record)
    return record


def _oracle_map(outcomes: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for raw in outcomes:
        validate_outcome(raw)
        if raw.get("outcome_kind") not in {"static-oracle", "human-adjudication"}:
            continue
        outcome = raw.get("outcome")
        if not isinstance(outcome, Mapping):
            continue
        oracle = outcome.get("oracle", outcome.get("ground_truth"))
        if oracle is not None:
            result[str(raw["observation_id"])] = oracle
    return result


def _decision(result: Any) -> Any:
    if isinstance(result, Mapping):
        if "decision" in result:
            return result.get("decision")
        if "value" in result:
            return result.get("value")
        if len(result) == 1:
            return next(iter(result.values()))
    return result


def _semantic_type(observations: Sequence[Mapping[str, Any]]) -> str | None:
    observed: set[str] = set()
    for obs in observations:
        result = obs.get("candidate", {}).get("result")
        if isinstance(result, Mapping) and isinstance(result.get("semantic_type"), str):
            observed.add(str(result["semantic_type"]))
    if len(observed) > 1:
        raise ValueError("one feature cohort cannot mix semantic types")
    return next(iter(observed)) if observed else None


def _paired_change(control_ok: Sequence[bool], candidate_ok: Sequence[bool], *, label: str) -> dict[str, Any]:
    if len(control_ok) != len(candidate_ok):
        raise ValueError("paired correctness lengths differ")
    deltas = [float(int(candidate) - int(control)) for control, candidate in zip(control_ok, candidate_ok, strict=True)]
    return paired_bootstrap_interval(deltas, label=label)


def _change_analysis(
    controls: Sequence[Any],
    candidates: Sequence[Any],
    truths: Sequence[Any],
    candidate_success: Sequence[bool],
) -> dict[str, int]:
    counts = {
        "agreements_correct": 0,
        "agreements_wrong": 0,
        "beneficial_changes": 0,
        "harmful_changes": 0,
        "changed_both_wrong": 0,
        "candidate_no_decision": 0,
    }
    for control, candidate, truth, success in zip(
        controls, candidates, truths, candidate_success, strict=True
    ):
        if not success:
            counts["candidate_no_decision"] += 1
            continue
        if control == candidate:
            counts["agreements_correct" if control == truth else "agreements_wrong"] += 1
        elif candidate == truth and control != truth:
            counts["beneficial_changes"] += 1
        elif control == truth and candidate != truth:
            counts["harmful_changes"] += 1
        else:
            counts["changed_both_wrong"] += 1
    return counts

def _rate_interval(successes: int, total: int) -> dict[str, Any]:
    return {"successes": successes, "n": total, "rate": successes / total if total else None, "wilson_95": wilson_interval(successes, total)}


def _feature_report(
    feature_id: str,
    observations: Sequence[Mapping[str, Any]],
    oracle: Mapping[str, Any],
    *,
    ece_minimum_n: int,
) -> dict[str, Any]:
    semantic_type = _semantic_type(observations)
    candidate_arms = [obs.get("candidate", {}) for obs in observations]
    semantic_statuses: Counter[str] = Counter()
    fallback_reasons: Counter[str] = Counter()
    for obs in observations:
        result = obs.get("candidate", {}).get("result")
        if isinstance(result, Mapping):
            status = result.get("semantic_status")
            if isinstance(status, str):
                semantic_statuses[status] += 1
            fallback = result.get("fallback")
            if isinstance(fallback, Mapping) and fallback.get("used") is True:
                fallback_reasons[str(fallback.get("reason") or "unknown")] += 1

    controls: list[Any] = []
    candidates: list[Any] = []
    truths: list[Any] = []
    candidate_success: list[bool] = []
    answered_controls: list[Any] = []
    answered_candidates: list[Any] = []
    answered_truths: list[Any] = []
    answered_obs: list[Mapping[str, Any]] = []

    for obs in observations:
        oid = str(obs["observation_id"])
        if oid not in oracle:
            continue
        control = _decision(obs.get("control", {}).get("result"))
        if control is None:
            continue
        candidate_arm = obs.get("candidate", {})
        candidate = _decision(candidate_arm.get("result"))
        success = candidate_arm.get("status") == "success" and candidate is not None
        controls.append(control)
        candidates.append(candidate)
        truths.append(oracle[oid])
        candidate_success.append(success)
        if success:
            answered_controls.append(control)
            answered_candidates.append(candidate)
            answered_truths.append(oracle[oid])
            answered_obs.append(obs)

    base: dict[str, Any] = {
        "semantic_type": semantic_type,
        "counts": {
            "observations": len(observations),
            "oracle_eligible": len(truths),
            "candidate_answered": len(answered_truths),
            "candidate_no_decision": len(truths) - len(answered_truths),
        },
        "reliability": {
            "candidate": arm_reliability(candidate_arms),
            "semantic_statuses": dict(sorted(semantic_statuses.items())),
            "fallback_reasons": dict(sorted(fallback_reasons.items())),
            "answer_coverage": (
                len(answered_truths) / len(truths) if truths else None
            ),
        },
    }
    if not truths:
        base["correctness"] = {
            "eligible": False,
            "reason": "no oracle-eligible observations",
        }
        base["calibration"] = {
            "eligible": False,
            "reason": "no oracle-eligible observations",
        }
        return base

    if semantic_type in {"choice", "noul"}:
        counts = correctness_counts(controls, candidates, truths)
        control_ok = [
            control == truth
            for control, truth in zip(controls, truths, strict=True)
        ]
        candidate_ok = [
            success and candidate == truth
            for candidate, truth, success in zip(
                candidates, truths, candidate_success, strict=True
            )
        ]
        answered_ok = [
            candidate == truth
            for candidate, truth in zip(
                answered_candidates, answered_truths, strict=True
            )
        ]
        correctness: dict[str, Any] = {
            "paired_counts": counts,
            "control_accuracy": _rate_interval(sum(control_ok), len(control_ok)),
            # Candidate attempt accuracy treats timeout/error/no-decision as incorrect.
            "candidate_accuracy": _rate_interval(
                sum(candidate_ok), len(candidate_ok)
            ),
            "candidate_answered_accuracy": (
                _rate_interval(sum(answered_ok), len(answered_ok))
                if answered_ok
                else {"successes": 0, "n": 0, "rate": None, "wilson_95": None}
            ),
            "candidate_answer_coverage": (
                len(answered_truths) / len(truths) if truths else None
            ),
            "candidate_minus_control_accuracy": _paired_change(
                control_ok, candidate_ok, label=f"{feature_id}:attempt-accuracy"
            ),
            "change_analysis": _change_analysis(
                controls, candidates, truths, candidate_success
            ),
        }
        if semantic_type == "choice":
            candidate_labels = [
                candidate if success else "__no_decision__"
                for candidate, success in zip(
                    candidates, candidate_success, strict=True
                )
            ]
            correctness["control_classification"] = classification_metrics(
                controls, truths
            )
            correctness["candidate_classification"] = classification_metrics(
                candidate_labels, truths
            )
            correctness["candidate_answered_classification"] = (
                classification_metrics(answered_candidates, answered_truths)
                if answered_truths
                else {"n": 0, "accuracy": None, "labels": [], "confusion_matrix": {}}
            )
        else:
            correctness["control_binary"] = binary_classification(
                [bool(x) for x in controls], [bool(x) for x in truths]
            )
            correctness["candidate_binary_answered"] = (
                binary_classification(
                    [bool(x) for x in answered_candidates],
                    [bool(x) for x in answered_truths],
                )
                if answered_truths
                else {
                    "n": 0,
                    "tp": 0,
                    "tn": 0,
                    "fp": 0,
                    "fn": 0,
                    "accuracy": None,
                    "precision": None,
                    "recall": None,
                    "f1": None,
                }
            )
        base["correctness"] = correctness
    elif semantic_type == "score":
        control_numbers = [float(x) for x in controls]
        truth_numbers = [float(x) for x in truths]
        correctness = {
            "control_ordinal": ordinal_metrics(control_numbers, truth_numbers),
            "candidate_answer_coverage": (
                len(answered_truths) / len(truths) if truths else None
            ),
        }
        if answered_truths:
            candidate_numbers = [float(x) for x in answered_candidates]
            answered_truth_numbers = [float(x) for x in answered_truths]
            answered_control_numbers = [float(x) for x in answered_controls]
            abs_effect = [
                abs(candidate - truth) - abs(control - truth)
                for control, candidate, truth in zip(
                    answered_control_numbers,
                    candidate_numbers,
                    answered_truth_numbers,
                    strict=True,
                )
            ]
            correctness["candidate_ordinal"] = ordinal_metrics(
                candidate_numbers, answered_truth_numbers
            )
            correctness["candidate_minus_control_absolute_error"] = (
                paired_bootstrap_interval(
                    abs_effect, label=f"{feature_id}:absolute-error"
                )
            )
        else:
            correctness["candidate_ordinal"] = {
                "n": 0,
                "mean_absolute_error": None,
                "signed_bias": None,
                "within_one_level_accuracy": None,
            }
            correctness["candidate_minus_control_absolute_error"] = {
                "n": 0,
                "mean": None,
                "lower": None,
                "upper": None,
                "confidence": 0.95,
            }
        base["correctness"] = correctness
    else:
        base["correctness"] = {
            "eligible": False,
            "reason": "semantic type unavailable",
        }

    candidate_results = [
        obs.get("candidate", {}).get("result") for obs in answered_obs
    ]
    if semantic_type == "noul":
        probabilities = [
            result.get("probability") if isinstance(result, Mapping) else None
            for result in candidate_results
        ]
        if (
            answered_truths
            and all(
                isinstance(p, (int, float)) and not isinstance(p, bool)
                for p in probabilities
            )
        ):
            probs = [float(p) for p in probabilities]
            calibration: dict[str, Any] = {
                "eligible": True,
                "n": len(probs),
                "brier": brier_score(
                    probs, [bool(x) for x in answered_truths]
                ),
            }
            if len(probs) >= ece_minimum_n:
                calibration["ece"] = expected_calibration_error(
                    probs, [bool(x) for x in answered_truths]
                )
                calibration["ece_eligible"] = True
            else:
                calibration["ece"] = None
                calibration["ece_eligible"] = False
                calibration["ece_reason"] = f"requires n >= {ece_minimum_n}"
            base["calibration"] = calibration
        else:
            base["calibration"] = {
                "eligible": False,
                "reason": "complete answered Noul probability evidence unavailable",
            }
    elif semantic_type in {"choice", "score"}:
        vectors: list[dict[str, float]] = []
        for result in candidate_results:
            raw = (
                result.get("probabilities")
                if isinstance(result, Mapping)
                else None
            )
            if not isinstance(raw, Mapping):
                vectors = []
                break
            vectors.append(
                {
                    str(k): float(v)
                    for k, v in raw.items()
                    if isinstance(v, (int, float)) and not isinstance(v, bool)
                }
            )
        labels = [str(x) for x in answered_truths]
        if len(vectors) == len(answered_truths) and vectors:
            base["calibration"] = {
                "eligible": True,
                "n": len(vectors),
                "multiclass_brier": multiclass_brier_score(vectors, labels),
                "log_loss": multiclass_log_loss(vectors, labels),
            }
        else:
            base["calibration"] = {
                "eligible": False,
                "reason": "complete answered probability distribution evidence unavailable",
            }
    else:
        base["calibration"] = {
            "eligible": False,
            "reason": "semantic type unavailable",
        }
    return base

def _request_report(requests: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    unique: dict[str, Mapping[str, Any]] = {}
    for request in requests:
        validate_record(request, PROVIDER_REQUEST_SCHEMA)
        request_id = str(request["request_id"])
        existing = unique.get(request_id)
        if existing is not None and dict(existing) != dict(request):
            raise ValueError(f"provider request ID {request_id!r} has conflicting evidence")
        unique[request_id] = request
    values = list(unique.values())
    durations = [float(x["duration_seconds"]) for x in values if isinstance(x.get("duration_seconds"), (int, float)) and not isinstance(x.get("duration_seconds"), bool)]
    statuses = Counter(str(x.get("status")) for x in values)
    usages = [x.get("usage", {}) for x in values if isinstance(x.get("usage"), Mapping)]
    return {
        "unique_requests": len(values),
        "status_counts": dict(sorted(statuses.items())),
        "duration_seconds": timing_summary(durations),
        "usage": aggregate_usage(usages) if usages else {},
        "decisions_observed": sum(len(x.get("decisions", [])) for x in values),
        "accounting_rule": "provider request evidence is deduplicated by request_id before aggregation",
    }


def build_decision_study_report(
    observations: Sequence[Mapping[str, Any]],
    outcomes: Sequence[Mapping[str, Any]],
    *,
    study_id: str,
    study_version: str,
    requests: Sequence[Mapping[str, Any]] = (),
    exclusions: Sequence[Mapping[str, Any]] = (),
    cohort: Mapping[str, Any] | None = None,
    ece_minimum_n: int = 100,
    minimum_oracle_n: int = 100,
) -> dict[str, Any]:
    if not observations:
        raise ValueError("decision study requires observations")
    for obs in observations:
        validate_observation(obs)
    oracle = _oracle_map(outcomes)
    groups: dict[str, list[Mapping[str, Any]]] = {}
    for obs in observations:
        groups.setdefault(str(obs["feature_id"]), []).append(obs)
    for exclusion in exclusions:
        validate_record(exclusion, DECISION_STUDY_EXCLUSION_SCHEMA)
        if exclusion.get("study_id") != study_id:
            raise ValueError("exclusion belongs to another study")
    reasons = Counter(str(item["reason_code"]) for item in exclusions)
    seams = {feature_id: _feature_report(feature_id, items, oracle, ece_minimum_n=ece_minimum_n) for feature_id, items in sorted(groups.items())}
    seam_eligibility = {
        feature_id: {
            "oracle_eligible_n": int(report["counts"]["oracle_eligible"]),
            "minimum_required": minimum_oracle_n,
            "eligible": int(report["counts"]["oracle_eligible"]) >= minimum_oracle_n,
        }
        for feature_id, report in seams.items()
    }
    record = {
        "schema": DECISION_STUDY_REPORT_SCHEMA,
        "study_id": study_id,
        "study_version": study_version,
        "cohort": dict(cohort or {}),
        "counts": {
            "observations": len(observations),
            "oracle_outcomes": len(oracle),
            "features": len(groups),
            "exclusions": len(exclusions),
        },
        "seams": seams,
        "request_efficiency": _request_report(requests),
        "exclusions": {"count": len(exclusions), "reason_counts": dict(sorted(reasons.items()))},
        "eligibility": {
            "minimum_oracle_n_per_seam": minimum_oracle_n,
            "seams": seam_eligibility,
            "all_observed_seams_eligible": bool(seam_eligibility) and all(
                item["eligible"] for item in seam_eligibility.values()
            ),
        },
        "limitations": [
            "agreement between control and candidate is not correctness without an independent oracle",
            "shadow observations do not establish downstream causal effects",
            "provider request efficiency is request-level and must not be multiplied by the number of decision seams",
        ],
    }
    validate_record(record, DECISION_STUDY_REPORT_SCHEMA)
    return record
