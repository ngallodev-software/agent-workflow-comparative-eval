from __future__ import annotations
import math
from collections.abc import Sequence

def brier_score(probabilities:Sequence[float],truths:Sequence[bool])->float|None:
    if len(probabilities)!=len(truths): raise ValueError("probability/truth lengths differ")
    if not probabilities: return None
    vals=[]
    for p,t in zip(probabilities,truths,strict=True):
        p=float(p)
        if not 0<=p<=1: raise ValueError("probability outside [0,1]")
        vals.append((p-(1.0 if t else 0.0))**2)
    return sum(vals)/len(vals)
def expected_calibration_error(probabilities:Sequence[float],truths:Sequence[bool],*,bins:int=10)->float|None:
    if len(probabilities)!=len(truths): raise ValueError("probability/truth lengths differ")
    if not probabilities:return None
    if bins<1: raise ValueError("bins must be positive")
    buckets=[[] for _ in range(bins)]
    for p,t in zip(probabilities,truths,strict=True):
        p=float(p)
        if not 0<=p<=1: raise ValueError("probability outside [0,1]")
        buckets[min(bins-1,int(p*bins))].append((p,bool(t)))
    total=len(probabilities); ece=0.0
    for bucket in buckets:
        if not bucket:continue
        conf=sum(p for p,_ in bucket)/len(bucket); acc=sum(1.0 if t else 0.0 for _,t in bucket)/len(bucket); ece += len(bucket)/total*abs(acc-conf)
    return ece

def multiclass_brier_score(probabilities: Sequence[dict[str, float]], truths: Sequence[str]) -> float | None:
    if len(probabilities) != len(truths):
        raise ValueError("probability/truth lengths differ")
    if not probabilities:
        return None
    labels = sorted({label for vector in probabilities for label in vector} | set(truths))
    total = 0.0
    for vector, truth in zip(probabilities, truths, strict=True):
        if any(not 0 <= float(value) <= 1 for value in vector.values()):
            raise ValueError("probability outside [0,1]")
        mass = sum(float(vector.get(label, 0.0)) for label in labels)
        if abs(mass - 1.0) > 1e-6:
            raise ValueError("multiclass probabilities must sum to 1")
        total += sum((float(vector.get(label, 0.0)) - (1.0 if label == truth else 0.0)) ** 2 for label in labels)
    return total / len(probabilities)


def multiclass_log_loss(probabilities: Sequence[dict[str, float]], truths: Sequence[str], *, epsilon: float = 1e-15) -> float | None:
    if len(probabilities) != len(truths):
        raise ValueError("probability/truth lengths differ")
    if not probabilities:
        return None
    losses = []
    for vector, truth in zip(probabilities, truths, strict=True):
        value = float(vector.get(truth, 0.0))
        if not 0 <= value <= 1:
            raise ValueError("probability outside [0,1]")
        losses.append(-math.log(min(1.0 - epsilon, max(epsilon, value))))
    return sum(losses) / len(losses)
