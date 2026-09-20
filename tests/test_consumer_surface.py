import agent_workflow_comparative_eval as lib

def test_expected_consumer_top_level_surface():
    for name in ["sha256","canonical_hash","load_corpus","load_dataset","observation","make_observation","validate_observation","run_static_cases","outcome","make_outcome","OutcomeJoiner","comparison_report","build_report"]:
        assert callable(getattr(lib,name))
    assert lib.__version__=="0.1.0"
