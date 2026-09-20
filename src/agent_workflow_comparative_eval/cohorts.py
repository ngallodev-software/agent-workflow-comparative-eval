from __future__ import annotations
from collections.abc import Mapping,Sequence
from typing import Any
from .identity import canonical_json

def group_by_cohort(observations:Sequence[Mapping[str,Any]])->dict[str,list[dict[str,Any]]]:
    groups:dict[str,list[dict[str,Any]]]={}
    for obs in observations:
        key=canonical_json([obs.get("feature_id"),obs.get("mode"),obs.get("identity",{})]); groups.setdefault(key,[]).append(dict(obs))
    return groups
