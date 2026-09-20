from __future__ import annotations
import time, uuid
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from typing import Any
from .constants import OBSERVATION_SCHEMA, LEGACY_OBSERVATION_SCHEMA
from .contracts import validate_record
from .identity import sha256
from .legacy import upgrade_legacy_record

_ALLOWED_MODES={"static","shadow-normal-usage","guarded-experiment"}

def _arm(call: Callable[[], Mapping[str,Any]] | None, timeout: float | None=None) -> dict[str,Any]:
    if call is None: return {"status":"not_applicable","duration_seconds":None,"result":None,"usage":{}}
    started=time.perf_counter()
    try: value=dict(call())
    except TimeoutError: return {"status":"timeout","duration_seconds":time.perf_counter()-started,"result":None,"usage":{}}
    except Exception as exc: return {"status":"error","duration_seconds":time.perf_counter()-started,"result":None,"usage":{},"error_class":type(exc).__name__}
    duration=time.perf_counter()-started
    if timeout is not None and duration > timeout: return {"status":"timeout","duration_seconds":duration,"result":None,"usage":{}}
    usage=value.get("usage",{})
    safe_usage={str(k):v for k,v in usage.items() if v is None or (isinstance(v,(int,float)) and not isinstance(v,bool))} if isinstance(usage,Mapping) else {}
    result={"status":"success","duration_seconds":duration,"result":value,"usage":safe_usage}
    for key in ("provider_elapsed_seconds","first_output_latency_seconds"):
        v=value.get(key)
        if isinstance(v,(int,float)) and not isinstance(v,bool) and v>=0: result[key]=float(v)
    return result


def make_observation(*, feature_id: str, mode: str, identity: Mapping[str,Any], source_input: Mapping[str,Any], projected_input: Mapping[str,Any], control: Callable[[],Mapping[str,Any]], candidate: Callable[[],Mapping[str,Any]]|None, case_id: str|None=None, data_class: str="synthetic", candidate_timeout: float|None=None, observation_id: str|None=None, candidate_applied: bool=False, authoritative_arm: str="control") -> dict[str,Any]:
    if mode not in _ALLOWED_MODES: raise ValueError("invalid comparison mode")
    if candidate_timeout is not None and candidate_timeout <= 0: raise ValueError("candidate_timeout must be positive")
    control_arm=_arm(control)
    candidate_arm=_arm(candidate,candidate_timeout)
    left,right=control_arm.get("result"),candidate_arm.get("result")
    record={"schema":OBSERVATION_SCHEMA,"observation_id":observation_id or str(uuid.uuid4()),"feature_id":feature_id,"mode":mode,"recorded_at":datetime.now(timezone.utc).isoformat(),"identity":dict(identity),"input":{"case_id":case_id,"input_sha256":sha256(source_input),"projection_sha256":sha256(projected_input),"raw_input_persisted":False},"control":control_arm,"candidate":candidate_arm,"comparison":{"candidate_applied":bool(candidate_applied),"authoritative_arm":authoritative_arm,"agreement":None if left is None or right is None else left==right,"normalized_control":left,"normalized_candidate":right},"privacy":{"data_class":data_class,"raw_content_stored":False,"secret_values_stored":False}}
    validate_observation(record)
    return record

observation=make_observation


def validate_observation(value: Mapping[str,Any]) -> None:
    original_schema=value.get("schema")
    if original_schema == LEGACY_OBSERVATION_SCHEMA:
        # Preserve the actual 0.1.0 compatibility invariant.
        if value.get("comparison",{}).get("candidate_applied") is not False or value.get("comparison",{}).get("authoritative_arm") != "control": raise ValueError("legacy observation must remain control-authoritative")
        record=upgrade_legacy_record(value)
    else: record=dict(value)
    validate_record(record, OBSERVATION_SCHEMA)
    inp=record.get("input",{}); privacy=record.get("privacy",{}); comparison=record.get("comparison",{})
    for key in ("input_sha256","projection_sha256"):
        digest=inp.get(key)
        if not isinstance(digest,str) or len(digest)!=64 or any(c not in "0123456789abcdef" for c in digest): raise ValueError("invalid observation digest")
    if inp.get("raw_input_persisted",False) is not False or privacy.get("raw_content_stored") is not False or privacy.get("secret_values_stored") is not False: raise ValueError("observation violates privacy boundary")
    if record.get("mode") in {"static","shadow-normal-usage"} and (comparison.get("candidate_applied") is not False or comparison.get("authoritative_arm")!="control"): raise ValueError("static/shadow observation must remain control-authoritative")


def run_static_cases(cases: Sequence[Mapping[str,Any]], *, feature_id: str, control: Callable[[Mapping[str,Any]],Mapping[str,Any]], candidate: Callable[[Mapping[str,Any]],Mapping[str,Any]], repetitions: int=1) -> list[dict[str,Any]]:
    if repetitions < 1: raise ValueError("repetitions must be positive")
    observations=[]
    for case in cases:
        case_id=case.get("case_id")
        for repetition in range(repetitions):
            identity={"dataset_version":case.get("dataset_version","unknown"),"repetition":repetition}
            observations.append(make_observation(feature_id=feature_id,mode="static",identity=identity,source_input=case,projected_input=case,case_id=case_id if isinstance(case_id,str) else None,control=lambda case=case:control(case),candidate=lambda case=case:candidate(case)))
    return observations
