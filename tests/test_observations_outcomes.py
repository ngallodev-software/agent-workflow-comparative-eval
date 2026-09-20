import pytest
from agent_workflow_comparative_eval import *

def test_observation_is_control_authoritative_and_secret_free():
    obs=observation(feature_id="f/v1",mode="static",identity={"dataset_version":"v1","repetition":0},source_input={"secret":"not-persisted"},projected_input={"x":1},control=lambda:{"v":1},candidate=lambda:{"v":2},observation_id="o1")
    assert obs["schema"]==OBSERVATION_SCHEMA
    assert obs["comparison"]["candidate_applied"] is False
    assert obs["comparison"]["authoritative_arm"]=="control"
    assert "not-persisted" not in str(obs)
    validate_observation(obs)

def test_timeout_classification_and_no_exception_text():
    def slow(): raise RuntimeError("sensitive detail")
    obs=observation(feature_id="f",mode="static",identity={},source_input={},projected_input={},control=lambda:{},candidate=slow)
    assert obs["candidate"]["status"]=="error" and obs["candidate"]["error_class"]=="RuntimeError"
    assert "sensitive detail" not in str(obs)

def test_outcome_joiner_is_idempotent_and_immutable():
    j=OutcomeJoiner(); first=j.join("o","static-oracle",{"oracle":{"x":1}}); second=j.join("o","static-oracle",{"oracle":{"x":1}})
    assert first["outcome"]==second["outcome"]
    with pytest.raises(ImmutableOutcomeConflict): j.join("o","static-oracle",{"oracle":{"x":2}})
