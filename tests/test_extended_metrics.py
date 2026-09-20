from agent_workflow_comparative_eval import (
    classification_metrics, ordinal_metrics, brier_score,
    multiclass_brier_score, multiclass_log_loss, compare_trials, ComparisonPolicy,
)

def test_classification_and_ordinal_metrics():
    c=classification_metrics(["a","b","b"],["a","a","b"])
    assert c["accuracy"] == 2/3 and c["confusion_matrix"]["a"]["b"] == 1
    o=ordinal_metrics([1,3,4],[1,2,2])
    assert o["mean_absolute_error"] == 1.0 and o["within_one_level_accuracy"] == 2/3

def test_calibration_metrics():
    assert brier_score([0.8,0.2],[True,False]) == 0.039999999999999994
    assert multiclass_brier_score([{"a":.8,"b":.2}], ["a"]) > 0
    assert multiclass_log_loss([{"a":.8,"b":.2}], ["a"]) > 0

def test_generic_trial_compare():
    base=[{"task_id":"t","repetition":i,"verdict":"pass" if i<5 else "fail"} for i in range(10)]
    cand=[{"task_id":"t","repetition":i,"verdict":"pass" if i<8 else "fail"} for i in range(10)]
    report=compare_trials(base,cand,policy=ComparisonPolicy(minimum_n=10))
    assert report["paired_n"]==10 and report["pass_rate_difference"]==0.3
