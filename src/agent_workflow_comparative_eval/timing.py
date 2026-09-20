from __future__ import annotations
import math
from collections.abc import Sequence

def quantile(values:Sequence[float],q:float)->float|None:
    if not values: return None
    if not 0<=q<=1: raise ValueError("q must be between 0 and 1")
    ordered=sorted(float(v) for v in values); pos=(len(ordered)-1)*q; low,high=math.floor(pos),math.ceil(pos)
    return ordered[low] if low==high else ordered[low]+(ordered[high]-ordered[low])*(pos-low)
def timing_summary(values:Sequence[float])->dict[str,float|int|None]:
    vals=[float(v) for v in values]
    return {"n":len(vals),"p50":quantile(vals,.5),"p90":quantile(vals,.9) if len(vals)>=20 else None,"p95":quantile(vals,.95) if len(vals)>=40 else None}
