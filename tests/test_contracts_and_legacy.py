from agent_workflow_comparative_eval import *

def test_legacy_observation_upgrades_without_mutating():
    legacy={"schema":LEGACY_OBSERVATION_SCHEMA,"observation_id":"x","feature_id":"f","mode":"static","recorded_at":"now","identity":{},"input":{"case_id":None,"input_sha256":"a"*64,"projection_sha256":"b"*64,"raw_input_persisted":False},"control":{"status":"success","duration_seconds":0.1,"result":{},"usage":{}},"candidate":{"status":"success","duration_seconds":0.2,"result":{},"usage":{}},"comparison":{"candidate_applied":False,"authoritative_arm":"control","agreement":True,"normalized_control":{},"normalized_candidate":{}},"privacy":{"data_class":"synthetic","raw_content_stored":False,"secret_values_stored":False}}
    old=dict(legacy); canonical=upgrade_legacy_record(legacy)
    assert legacy==old
    assert canonical["schema"]==OBSERVATION_SCHEMA
    validate_observation(canonical)
    assert downgrade_typesafe_v1_record(canonical)["schema"]==LEGACY_OBSERVATION_SCHEMA

def test_all_packaged_schemas_are_valid_jsonschema():
    from jsonschema import Draft202012Validator
    for sid in known_schema_ids(): Draft202012Validator.check_schema(schema_for(sid))
