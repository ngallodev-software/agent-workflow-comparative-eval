from __future__ import annotations
import json
from collections.abc import Mapping
from dataclasses import dataclass
from importlib.resources import files
from typing import Any
from .constants import FEATURE_SCHEMA, LEGACY_FEATURE_SCHEMA
from .errors import ComparativeEvalError
from .legacy import upgrade_legacy_record

@dataclass(frozen=True)
class EvalFeature:
    feature_id: str
    control: Mapping[str, Any]
    candidate: Mapping[str, Any]
    normalization: Mapping[str, Any]
    oracle: Mapping[str, Any]
    metrics: tuple[str, ...]
    capture: Mapping[str, Any]

    def as_record(self) -> dict[str, Any]:
        return {"schema":FEATURE_SCHEMA,"feature_id":self.feature_id,"control":dict(self.control),"candidate":dict(self.candidate),"normalization":dict(self.normalization),"oracle":dict(self.oracle),"metrics":list(self.metrics),"capture":dict(self.capture)}

class FeatureRegistry:
    def __init__(self) -> None: self._features: dict[str,EvalFeature] = {}
    def register(self, feature: EvalFeature | Mapping[str,Any]) -> EvalFeature:
        if not isinstance(feature, EvalFeature):
            record=dict(feature)
            if record.get("schema") == LEGACY_FEATURE_SCHEMA: record=upgrade_legacy_record(record)
            if record.get("schema") != FEATURE_SCHEMA: raise ValueError("invalid evaluation feature schema")
            metrics=record.get("metrics")
            if not isinstance(metrics,list) or not all(isinstance(x,str) for x in metrics): raise ValueError("feature metrics must be a string list")
            feature=EvalFeature(str(record["feature_id"]),record["control"],record["candidate"],record["normalization"],record["oracle"],tuple(metrics),record["capture"])
        if not feature.feature_id.strip() or feature.feature_id in self._features: raise ValueError(f"invalid or duplicate feature: {feature.feature_id!r}")
        self._features[feature.feature_id]=feature; return feature
    def get(self, feature_id: str) -> EvalFeature:
        try: return self._features[feature_id]
        except KeyError as exc: raise ComparativeEvalError(f"unknown evaluation feature: {feature_id}") from exc
    def records(self) -> tuple[dict[str,Any],...]: return tuple(self._features[n].as_record() for n in sorted(self._features))


def default_feature_registry() -> FeatureRegistry:
    value=json.loads(files("agent_workflow_comparative_eval").joinpath("resources","feature-registry.json").read_text(encoding="utf-8"))
    registry=FeatureRegistry()
    for feature in value.get("features",[]): registry.register(feature)
    return registry
