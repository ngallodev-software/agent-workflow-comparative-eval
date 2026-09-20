from agent_workflow_comparative_eval import normalize_usage, aggregate_usage

def test_api_usage_aliases_and_ms_match_host_semantics():
    got=normalize_usage({"prompt_tokens":10,"completion_tokens":5,"duration_api_ms":250,"cost_usd":0.12,"currency":"USD"},currency=None,price_catalog_id=None,source="test",billing={"mode":"api"})
    assert got["input_tokens"]==10 and got["output_tokens"]==5 and got["provider_total_tokens"]==15
    assert got["provider_elapsed_seconds"]==0.25 and got["provider_billed_cost"]==0.12
    assert got["local_estimated_cost"] is None and got["token_evidence_complete"] is True

def test_subscription_cost_is_not_provider_billed():
    got=normalize_usage({"input_tokens":1,"output_tokens":2,"cost_usd":0.5},currency="USD",price_catalog_id=None,source="test",billing={"mode":"subscription","provider_billed_cost_semantics":"not-attributable"})
    assert got["provider_billed_cost"] is None
    assert got["local_estimated_cost"]==0.5
    assert got["local_estimated_cost_source"]=="provider-emitted-equivalent"

def test_aggregate_missingness_does_not_become_zero():
    a=normalize_usage({"input_tokens":1,"output_tokens":2},currency="USD",price_catalog_id=None,source="x")
    b=normalize_usage({},currency="USD",price_catalog_id=None,source="x")
    got=aggregate_usage([a,b])
    assert got["input_tokens"] is None and got["provider_total_tokens"] is None
