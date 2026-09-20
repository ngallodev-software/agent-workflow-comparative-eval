from __future__ import annotations
import hashlib, math, random
from statistics import mean, NormalDist
from collections.abc import Iterable, Sequence

def wilson_interval(successes:int,count:int,confidence:float=.95)->list[float]|None:
    if not count: return None
    if not 0.5 < confidence < 1.0: raise ValueError("confidence must be between 0.5 and 1")
    z=1.959963984540054 if confidence == .95 else NormalDist().inv_cdf(0.5 + confidence / 2); proportion=successes/count; denominator=1+z*z/count; center=(proportion+z*z/(2*count))/denominator; margin=z*math.sqrt(proportion*(1-proportion)/count+z*z/(4*count*count))/denominator
    return [round(max(0.0,center-margin),6),round(min(1.0,center+margin),6)]

def _seed(label:str)->int: return int(hashlib.sha256(label.encode("utf-8")).hexdigest()[:16],16)
def paired_bootstrap_interval(values:Iterable[float],*,label:str,confidence:float=.95,samples:int=10000)->dict[str,float|int|None]:
    observed=[float(x) for x in values]
    if not observed: return {"n":0,"mean":None,"lower":None,"upper":None,"confidence":confidence}
    if len(observed)==1:
        x=observed[0]; return {"n":1,"mean":x,"lower":x,"upper":x,"confidence":confidence}
    if samples<2: raise ValueError("samples must be >= 2")
    generator=random.Random(_seed(label)); estimates=sorted(mean(generator.choice(observed) for _ in observed) for _ in range(samples)); alpha=(1-confidence)/2; li=max(0,min(samples-1,int(alpha*samples))); ui=max(0,min(samples-1,int((1-alpha)*samples)-1))
    return {"n":len(observed),"mean":round(mean(observed),6),"lower":round(estimates[li],6),"upper":round(estimates[ui],6),"confidence":confidence}
def paired_binary_deltas(control:Iterable[bool],candidate:Iterable[bool])->list[float]: return [float(int(r)-int(l)) for l,r in zip(control,candidate,strict=True)]
