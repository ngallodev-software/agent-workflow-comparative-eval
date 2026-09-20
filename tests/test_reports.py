from agent_workflow_comparative_eval import *

def test_report_preserves_legacy_gate_keys_and_cohort_safety():
    cases=[{"case_id":"a","dataset_version":"v1","oracle":{"x":1}},{"case_id":"b","dataset_version":"v1","oracle":{"x":2}}]
    obs=run_static_cases(cases,feature_id="f",control=lambda c:{"x":c["oracle"]["x"]},candidate=lambda c:{"x":1},repetitions=1)
    outs=[outcome(o["observation_id"],"static-oracle",{"oracle":next(c["oracle"] for c in cases if c["case_id"]==o["input"]["case_id"])}) for o in obs]
    report=comparison_report(obs,outs)
    assert report["correctness"]["both_correct"]==1
    assert report["correctness"]["control_only"]==1
    assert report["correctness"]["candidate_only"]==0
    assert report["counts"]["oracle_eligible"]==2
    assert "duration_seconds" in report["efficiency"]["paired"]

def test_report_rejects_mixed_repetition_identity():
    cases=[{"case_id":"a","dataset_version":"v1"}]
    obs=run_static_cases(cases,feature_id="f",control=lambda c:{},candidate=lambda c:{},repetitions=2)
    import pytest
    with pytest.raises(CohortError): comparison_report(obs)
