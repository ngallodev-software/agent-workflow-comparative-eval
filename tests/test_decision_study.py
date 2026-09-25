from agent_workflow_comparative_eval import (
    build_decision_study_report,
    load_study_spec,
    make_exclusion,
    make_outcome,
    make_precomputed_decision_observation,
    make_provider_request,
)


def _obs(feature, decision_id, semantic_type, case_id, control, candidate, *, probability=None, probabilities=None):
    return make_precomputed_decision_observation(
        feature_id=feature,
        decision_id=decision_id,
        semantic_type=semantic_type,
        identity={"dataset_version": "routing-study-v1.0.0", "question_set": "routing/v2"},
        source_input={"task": case_id},
        projected_input={"metadata": {}},
        control_decision=control,
        candidate_decision=candidate,
        semantic_status="success",
        request_id=f"req-{case_id}",
        probability=probability,
        confidence=0.9 if semantic_type != "noul" else None,
        probabilities=probabilities,
        policy_candidate=candidate,
        applied_result=control,
        fallback={"used": False, "reason": None},
        case_id=case_id,
        observation_id=f"{feature}-{case_id}",
    )


def test_preregistered_study_spec_is_packaged_and_valid():
    spec = load_study_spec("routing-semantic-v1")
    assert spec["study_id"] == "routing-semantic-v1"
    assert spec["sample_policy"]["minimum_oracle_eligible_per_seam"] == 100
    assert spec["oracle_policy"]["hidden_from_inference"] is True


def test_decision_study_report_separates_seams_and_deduplicates_requests():
    choice = _obs(
        "routing.task-class/v1", "routing.task_class", "choice", "c1",
        "implementation", "review",
        probabilities={"implementation": 0.1, "diagnosis": 0.1, "review": 0.7, "documentation": 0.05, "other": 0.05},
    )
    noul = _obs(
        "routing.interaction-required/v1", "routing.interaction_required", "noul", "c1",
        False, True, probability=0.8,
    )
    score = _obs(
        "routing.semantic-risk/v1", "routing.semantic_risk", "score", "c1",
        1, 1.6, probabilities={"0": 0.1, "1": 0.2, "2": 0.7},
    )
    outcomes = [
        make_outcome(choice["observation_id"], "static-oracle", {"oracle": "review"}),
        make_outcome(noul["observation_id"], "static-oracle", {"oracle": True}),
        make_outcome(score["observation_id"], "static-oracle", {"oracle": 2}),
    ]
    request = make_provider_request(
        request_id="req-c1",
        identity={"provider": "typesafe", "model": "jev-test"},
        decisions=["routing.task_class", "routing.interaction_required", "routing.semantic_risk"],
        status="success",
        duration_seconds=0.2,
        usage={
            "input_tokens": 100,
            "output_tokens": 3,
            "provider_total_tokens": 103,
            "token_evidence_complete": True,
            "cost_evidence_complete": False,
        },
        request_sha256="a" * 64,
    )
    report = build_decision_study_report(
        [choice, noul, score],
        outcomes,
        study_id="routing-semantic-v1",
        study_version="1.0.0",
        requests=[request, request],
        ece_minimum_n=1,
    )
    assert report["request_efficiency"]["unique_requests"] == 1
    assert report["request_efficiency"]["usage"]["input_tokens"] == 100
    assert report["seams"]["routing.task-class/v1"]["correctness"]["candidate_accuracy"]["rate"] == 1.0
    assert report["seams"]["routing.interaction-required/v1"]["calibration"]["ece_eligible"] is True
    assert report["seams"]["routing.semantic-risk/v1"]["correctness"]["candidate_ordinal"]["mean_absolute_error"] == 0.4


def test_exclusions_are_explicit_and_counted():
    obs = _obs(
        "routing.task-class/v1", "routing.task_class", "choice", "c2",
        "review", "review",
        probabilities={"implementation": 0.02, "diagnosis": 0.02, "review": 0.9, "documentation": 0.03, "other": 0.03},
    )
    exclusion = make_exclusion(
        study_id="routing-semantic-v1",
        case_id="c-missing",
        decision_id="routing.task_class",
        reason_code="oracle_missing",
        stage="oracle-join",
    )
    report = build_decision_study_report(
        [obs],
        [],
        study_id="routing-semantic-v1",
        study_version="1.0.0",
        exclusions=[exclusion],
    )
    assert report["counts"]["exclusions"] == 1
    assert report["exclusions"]["reason_counts"] == {"oracle_missing": 1}
    assert report["seams"]["routing.task-class/v1"]["correctness"]["eligible"] is False
