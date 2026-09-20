from __future__ import annotations
from collections.abc import Mapping,Sequence
from typing import Any
from .errors import CohortError

def assert_same_cohort(observations:Sequence[Mapping[str,Any]])->tuple[str,str,dict[str,Any]]:
    if not observations: raise ValueError("at least one observation is required")
    feature=str(observations[0].get("feature_id")); mode=str(observations[0].get("mode")); identity=dict(observations[0].get("identity",{}))
    if any(o.get("feature_id")!=feature or o.get("mode")!=mode or o.get("identity")!=identity for o in observations): raise CohortError("comparison report cannot mix feature, mode, or cohort identities")
    return feature,mode,identity
