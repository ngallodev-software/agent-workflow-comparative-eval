from __future__ import annotations
from collections.abc import Mapping,Sequence
from typing import Any

def arm_reliability(arms:Sequence[Mapping[str,Any]])->dict[str,int|float|None]:
    total=len(arms); counts={s:sum(a.get("status")==s for a in arms) for s in ("success","error","timeout","skipped","not_applicable")}
    error_classes={}
    for arm in arms:
        name=arm.get("error_class")
        if isinstance(name,str) and name: error_classes[name]=error_classes.get(name,0)+1
    return {"n":total,**counts,"success_rate":counts["success"]/total if total else None,"timeout_rate":counts["timeout"]/total if total else None,"error_rate":counts["error"]/total if total else None,"missing_usage":sum(not bool(a.get("usage")) for a in arms),"error_classes":error_classes}
