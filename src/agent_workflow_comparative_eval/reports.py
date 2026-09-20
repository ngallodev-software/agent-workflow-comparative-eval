from __future__ import annotations
from collections.abc import Mapping,Sequence
from typing import Any
from .constants import REPORT_SCHEMA
from .legacy import upgrade_legacy_record
from .observations import validate_observation
from .outcomes import validate_outcome
from .pairing import assert_same_cohort
from .timing import timing_summary
from .metrics.correctness import correctness_counts,binary_classification
from .metrics.reliability import arm_reliability
from .metrics.efficiency import paired_efficiency
from .metrics.calibration import brier_score, expected_calibration_error, multiclass_brier_score, multiclass_log_loss
from .contracts import validate_record


def _oracle_map(outcomes:Sequence[Mapping[str,Any]])->dict[str,Any]:
    result={}
    for raw in outcomes:
        record=upgrade_legacy_record(raw) if str(raw.get("schema","")).startswith("agent-workflow-typesafe/") else dict(raw)
        validate_outcome(record)
        if record.get("outcome_kind")=="static-oracle":
            outcome=record.get("outcome",{}); oracle=outcome.get("oracle") if isinstance(outcome,Mapping) else None
            if oracle is not None: result[str(record["observation_id"])]=oracle
        elif record.get("outcome_kind")=="human-adjudication":
            outcome=record.get("outcome",{}); truth=outcome.get("ground_truth") if isinstance(outcome,Mapping) else None
            if truth is not None: result.setdefault(str(record["observation_id"]),truth)
    return result

def comparison_report(observations:Sequence[Mapping[str,Any]],outcomes:Sequence[Mapping[str,Any]]=())->dict[str,Any]:
    if not observations: raise ValueError("at least one observation is required")
    canonical=[]
    for raw in observations:
        record=upgrade_legacy_record(raw) if str(raw.get("schema","")).startswith("agent-workflow-typesafe/") else dict(raw); validate_observation(record); canonical.append(record)
    feature,mode,identity=assert_same_cohort(canonical); oracle_by_id=_oracle_map(outcomes)
    controls=[]; candidates=[]; truths=[]
    for obs in canonical:
        oid=str(obs["observation_id"])
        if oid in oracle_by_id:
            controls.append(obs["control"].get("result")); candidates.append(obs["candidate"].get("result")); truths.append(oracle_by_id[oid])
    correct=correctness_counts(controls,candidates,truths)
    # Backward-compatible keys expected by Agent-Workflow's current gate.
    correctness={k:correct[k] for k in ("control_only","candidate_only","both_correct","both_wrong")}
    correctness.update({k:correct[k] for k in ("control_correct","candidate_correct","control_rate","candidate_rate")})
    # Add binary detail only when all eligible results are single boolean values or one-field boolean mappings.
    def bool_value(v:Any):
        if isinstance(v,bool):return v
        if isinstance(v,Mapping) and len(v)==1:
            x=next(iter(v.values())); return x if isinstance(x,bool) else None
        return None
    cb=[bool_value(x) for x in controls]; nb=[bool_value(x) for x in candidates]; tb=[bool_value(x) for x in truths]
    if truths and all(x is not None for x in cb+nb+tb):
        correctness["control_binary"]=binary_classification([bool(x) for x in cb],[bool(x) for x in tb]); correctness["candidate_binary"]=binary_classification([bool(x) for x in nb],[bool(x) for x in tb])
    control_d=[float(x["control"]["duration_seconds"]) for x in canonical if isinstance(x.get("control",{}).get("duration_seconds"),(int,float))]; candidate_d=[float(x["candidate"]["duration_seconds"]) for x in canonical if isinstance(x.get("candidate",{}).get("duration_seconds"),(int,float))]
    efficiency={"control":timing_summary(control_d),"candidate":timing_summary(candidate_d),"paired":{}}
    for metric in ("duration_seconds","provider_elapsed_seconds","first_output_latency_seconds","provider_total_tokens","retry_count","provider_billed_cost","local_estimated_cost"):
        efficiency["paired"][metric]=paired_efficiency(canonical,metric)
    reliability={"candidate_timeouts":sum(x.get("candidate",{}).get("status")=="timeout" for x in canonical),"candidate_errors":sum(x.get("candidate",{}).get("status")=="error" for x in canonical),"control":arm_reliability([x.get("control",{}) for x in canonical]),"candidate":arm_reliability([x.get("candidate",{}) for x in canonical])}
    # Calibration is reported only when the normalized candidate result actually preserves probability evidence.
    binary_probs=[]; binary_truths=[]; multi_probs=[]; multi_truths=[]
    for obs in canonical:
        oid=str(obs["observation_id"])
        if oid not in oracle_by_id: continue
        truth=oracle_by_id[oid]; result=obs.get("candidate",{}).get("result")
        if isinstance(truth,bool) and isinstance(result,Mapping) and isinstance(result.get("probability"),(int,float)):
            binary_probs.append(float(result["probability"])); binary_truths.append(truth)
        elif isinstance(truth,str) and isinstance(result,Mapping) and isinstance(result.get("probabilities"),Mapping):
            vector={str(k):float(v) for k,v in result["probabilities"].items() if isinstance(v,(int,float))}
            multi_probs.append(vector); multi_truths.append(truth)
    if binary_probs and len(binary_probs)==len(truths):
        calibration={"eligible":True,"kind":"binary","n":len(binary_probs),"brier":brier_score(binary_probs,binary_truths),"ece":expected_calibration_error(binary_probs,binary_truths)}
    elif multi_probs and len(multi_probs)==len(truths):
        calibration={"eligible":True,"kind":"multiclass","n":len(multi_probs),"brier":multiclass_brier_score(multi_probs,multi_truths),"log_loss":multiclass_log_loss(multi_probs,multi_truths)}
    else:
        calibration={"eligible":False,"reason":"probability evidence unavailable in normalized candidate results"}
    selected_ids={str(x["observation_id"]) for x in canonical}; downstream_records=[]
    for raw in outcomes:
        if str(raw.get("observation_id")) in selected_ids: downstream_records.append(str(raw.get("observation_id")))
    record={"schema":REPORT_SCHEMA,"feature_id":feature,"cohort":dict(identity),"counts":{"observations":len(canonical),"oracle_eligible":len(truths),"control_success":sum(x.get("control",{}).get("status")=="success" for x in canonical),"candidate_success":sum(x.get("candidate",{}).get("status")=="success" for x in canonical)},"correctness":correctness,"efficiency":efficiency,"reliability":reliability,"calibration":calibration,"downstream":{"outcome_ids":downstream_records},"limitations":["shadow evidence is descriptive and does not establish causality","quality counts require an independent oracle"]}
    validate_record(record,REPORT_SCHEMA); return record

build_report=comparison_report
