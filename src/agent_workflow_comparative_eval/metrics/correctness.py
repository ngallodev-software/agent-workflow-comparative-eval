from __future__ import annotations
from collections.abc import Sequence
from typing import Any

def correctness_counts(control:Sequence[Any],candidate:Sequence[Any],oracle:Sequence[Any])->dict[str,int|float|None]:
    if not (len(control)==len(candidate)==len(oracle)): raise ValueError("control/candidate/oracle lengths differ")
    result={"control_only":0,"candidate_only":0,"both_correct":0,"both_wrong":0}
    for left,right,truth in zip(control,candidate,oracle,strict=True):
        l=left==truth; r=right==truth
        result["both_correct" if l and r else "both_wrong" if not l and not r else "control_only" if l else "candidate_only"] += 1
    n=len(oracle); control_correct=result["control_only"]+result["both_correct"]; candidate_correct=result["candidate_only"]+result["both_correct"]
    return {**result,"eligible":n,"control_correct":control_correct,"candidate_correct":candidate_correct,"control_rate":control_correct/n if n else None,"candidate_rate":candidate_correct/n if n else None}

def binary_classification(predictions:Sequence[bool],truths:Sequence[bool])->dict[str,int|float|None]:
    if len(predictions)!=len(truths): raise ValueError("prediction/truth lengths differ")
    tp=tn=fp=fn=0
    for p,t in zip(predictions,truths,strict=True):
        if p and t: tp+=1
        elif not p and not t: tn+=1
        elif p: fp+=1
        else: fn+=1
    n=len(truths); precision=tp/(tp+fp) if tp+fp else None; recall=tp/(tp+fn) if tp+fn else None; f1=2*precision*recall/(precision+recall) if precision is not None and recall is not None and precision+recall else None
    return {"n":n,"tp":tp,"tn":tn,"fp":fp,"fn":fn,"accuracy":(tp+tn)/n if n else None,"precision":precision,"recall":recall,"f1":f1}

def classification_metrics(predictions: Sequence[Any], truths: Sequence[Any]) -> dict[str, Any]:
    if len(predictions) != len(truths):
        raise ValueError("prediction/truth lengths differ")
    labels = sorted({str(x) for x in predictions} | {str(x) for x in truths})
    matrix = {truth: {pred: 0 for pred in labels} for truth in labels}
    correct = 0
    for prediction, truth in zip(predictions, truths, strict=True):
        t, p = str(truth), str(prediction)
        matrix[t][p] += 1
        correct += int(prediction == truth)
    return {
        "n": len(truths),
        "accuracy": correct / len(truths) if truths else None,
        "labels": labels,
        "confusion_matrix": matrix,
    }


def ordinal_metrics(predictions: Sequence[int | float], truths: Sequence[int | float]) -> dict[str, float | int | None]:
    if len(predictions) != len(truths):
        raise ValueError("prediction/truth lengths differ")
    if not truths:
        return {"n": 0, "mean_absolute_error": None, "signed_bias": None, "within_one_level_accuracy": None}
    errors = [float(p) - float(t) for p, t in zip(predictions, truths, strict=True)]
    return {
        "n": len(errors),
        "mean_absolute_error": sum(abs(e) for e in errors) / len(errors),
        "signed_bias": sum(errors) / len(errors),
        "within_one_level_accuracy": sum(abs(e) <= 1 for e in errors) / len(errors),
    }
