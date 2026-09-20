from __future__ import annotations
from collections.abc import Mapping,Sequence
from typing import Any
from ..statistics import paired_bootstrap_interval

def _num(v:object)->float|None: return float(v) if isinstance(v,(int,float)) and not isinstance(v,bool) else None
def _arm_metric(arm:Mapping[str,Any],metric:str)->float|None:
    if metric=="duration_seconds": return _num(arm.get(metric))
    if metric in {"provider_elapsed_seconds","first_output_latency_seconds"}: return _num(arm.get(metric))
    usage=arm.get("usage")
    return _num(usage.get(metric)) if isinstance(usage,Mapping) else None

def paired_efficiency(observations:Sequence[Mapping[str,Any]],metric:str)->dict[str,Any]:
    deltas=[]; percentages=[]; excluded=0
    for obs in observations:
        left=_arm_metric(obs.get("control",{}),metric); right=_arm_metric(obs.get("candidate",{}),metric)
        if left is None or right is None: excluded+=1; continue
        if metric in {"provider_billed_cost","local_estimated_cost"}:
            lu=obs.get("control",{}).get("usage",{}); ru=obs.get("candidate",{}).get("usage",{})
            if isinstance(lu,Mapping) and isinstance(ru,Mapping):
                if metric=="provider_billed_cost" and lu.get("currency")!=ru.get("currency"): excluded+=1; continue
                if metric=="local_estimated_cost" and (lu.get("currency"),lu.get("price_catalog_id"))!=(ru.get("currency"),ru.get("price_catalog_id")): excluded+=1; continue
        deltas.append(right-left)
        if left != 0: percentages.append((right-left)/abs(left)*100.0)
    return {"n":len(deltas),"excluded":excluded,"mean_difference":sum(deltas)/len(deltas) if deltas else None,"mean_percentage_difference":sum(percentages)/len(percentages) if percentages else None,"paired_bootstrap":paired_bootstrap_interval(deltas,label=f"efficiency:{metric}") if deltas else None}
