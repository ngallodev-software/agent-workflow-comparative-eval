from __future__ import annotations
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any
from .constants import OUTCOME_SCHEMA, LEGACY_OUTCOME_SCHEMA
from .contracts import validate_record
from .errors import ImmutableOutcomeConflict
from .legacy import upgrade_legacy_record

_ALLOWED={"static-oracle","human-adjudication","agent-run-outcome","none"}

def make_outcome(observation_id: str, outcome_kind: str, outcome: Mapping[str,Any]) -> dict[str,Any]:
    if not observation_id: raise ValueError("observation_id is required")
    if outcome_kind not in _ALLOWED: raise ValueError("invalid outcome kind")
    record={"schema":OUTCOME_SCHEMA,"observation_id":observation_id,"joined_at":datetime.now(timezone.utc).isoformat(),"outcome_kind":outcome_kind,"outcome":dict(outcome)}
    validate_outcome(record); return record
outcome=make_outcome

def validate_outcome(value: Mapping[str,Any]) -> None:
    record=upgrade_legacy_record(value) if value.get("schema")==LEGACY_OUTCOME_SCHEMA else dict(value)
    validate_record(record,OUTCOME_SCHEMA)
    if record.get("outcome_kind") not in _ALLOWED: raise ValueError("invalid outcome kind")

class OutcomeJoiner:
    def __init__(self)->None: self._outcomes:dict[tuple[str,str],dict[str,Any]]={}
    def join(self, observation_id: str, outcome_kind: str, outcome: Mapping[str,Any])->dict[str,Any]:
        key=(observation_id,outcome_kind); existing=self._outcomes.get(key)
        if existing is not None:
            if existing["outcome"] != dict(outcome): raise ImmutableOutcomeConflict("outcome join conflicts with immutable prior outcome")
            return dict(existing)
        record=make_outcome(observation_id,outcome_kind,outcome); self._outcomes[key]=record; return dict(record)
    def records(self)->tuple[dict[str,Any],...]: return tuple(dict(self._outcomes[k]) for k in sorted(self._outcomes))
