from __future__ import annotations
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any
from .identity import sha256
from .statistics import paired_bootstrap_interval, wilson_interval

DEFAULT_COHORT_KEYS = (
    "fixture_revision", "task_id", "base_revision", "prompt_sha256",
    "oracle_sha256", "acceptance_commands_sha256", "scope_policy_sha256",
    "scorer_versions_sha256", "sandbox", "budget_sha256", "repetition",
)

@dataclass(frozen=True)
class ComparisonPolicy:
    confidence: float = 0.95
    minimum_n: int = 10
    effect_threshold: float = 0.0
    allow_unpaired: bool = False
    primary_metric: str = "pass_rate"
    stop_rule: str = "fixed_n"


def compare_trials(
    baseline: Sequence[Mapping[str, Any]],
    candidate: Sequence[Mapping[str, Any]],
    *,
    policy: ComparisonPolicy = ComparisonPolicy(),
    cohort_keys: Sequence[str] = DEFAULT_COHORT_KEYS,
) -> dict[str, Any]:
    def key(item: Mapping[str, Any]) -> tuple[Any, ...]:
        return tuple(item.get(name) for name in cohort_keys)
    left = {key(item): item for item in baseline}
    right = {key(item): item for item in candidate}
    if len(left) != len(baseline) or len(right) != len(candidate):
        raise ValueError("duplicate trial cohort key")
    unmatched = sorted(str(item) for item in set(left) ^ set(right))
    paired = sorted(set(left) & set(right), key=str)
    if unmatched and not policy.allow_unpaired:
        raise ValueError(f"trial cohorts do not match: {unmatched[:10]}")
    differences = [float(right[k].get("verdict") == "pass") - float(left[k].get("verdict") == "pass") for k in paired]
    baseline_passes = sum(left[k].get("verdict") == "pass" for k in paired)
    candidate_passes = sum(right[k].get("verdict") == "pass" for k in paired)
    effect = sum(differences) / len(differences) if differences else 0.0
    cohort_sha = sha256(paired)
    interval = paired_bootstrap_interval(differences, label=f"compare:{cohort_sha}", confidence=policy.confidence) if len(paired) >= policy.minimum_n else None
    winner = None
    if interval is not None and not unmatched and policy.primary_metric == "pass_rate":
        if interval["lower"] is not None and float(interval["lower"]) > policy.effect_threshold:
            winner = "candidate"
        elif interval["upper"] is not None and float(interval["upper"]) < -policy.effect_threshold:
            winner = "baseline"
    return {
        "schema": "agent-workflow-comparative-eval/trial-comparison/v1",
        "paired": not unmatched,
        "descriptive_only": bool(unmatched),
        "cohort_sha256": cohort_sha,
        "paired_n": len(paired),
        "unmatched": unmatched,
        "baseline": {"passes": baseline_passes, "rate": baseline_passes / len(paired) if paired else None, "wilson": wilson_interval(baseline_passes, len(paired), policy.confidence)},
        "candidate": {"passes": candidate_passes, "rate": candidate_passes / len(paired) if paired else None, "wilson": wilson_interval(candidate_passes, len(paired), policy.confidence)},
        "pass_rate_difference": effect,
        "paired_bootstrap": interval,
        "winner": winner,
        "confidence": policy.confidence,
        "primary_metric": policy.primary_metric,
        "effect_threshold": policy.effect_threshold,
        "stop_rule": policy.stop_rule,
        "tail_metrics_eligible": {"p90": len(paired) >= 20, "p95": len(paired) >= 40},
    }
