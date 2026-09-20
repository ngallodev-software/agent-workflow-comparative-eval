from agent_workflow_comparative_eval import *

def test_frozen_datasets_and_versions():
    r=load_corpus("routing-v1"); s=load_corpus("skill-behavior-v1")
    assert [x["case_id"] for x in r]==["route-implementation","route-review","route-interaction","route-other"]
    assert all(x["dataset_version"]=="routing-v1.0.0" for x in r)
    assert all(x["dataset_version"]=="skill-behavior-v1.0.0" for x in s)
    assert dataset_manifest("routing-v1")["case_count"]==4

def test_default_registry_has_initial_features():
    reg=default_feature_registry(); ids={r["feature_id"] for r in reg.records()}
    assert ids=={"routing-advice/v1","skill-behavior-eval/v1"}
