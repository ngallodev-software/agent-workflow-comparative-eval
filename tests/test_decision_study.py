import hashlib
import json
from pathlib import Path

import pytest
from agent_workflow_comparative_eval import (
    build_decision_study_report,
    load_study_spec,
    make_exclusion,
    make_outcome,
    make_precomputed_decision_observation,
    make_provider_request,
    validate_decision_study_corpus,
    validate_decision_study_oracle_bundle,
    load_study_corpus,
    study_corpus_manifest,
    oracle_authoring_view,
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
    assert report["seams"]["routing.semantic-risk/v1"]["correctness"]["candidate_ordinal"]["mean_absolute_error"] == pytest.approx(0.4)


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


def test_neutral_study_bundle_validators_own_dataset_integrity():
    corpus = {
        "schema": "agent-workflow-comparative-eval/decision-study-corpus/v1",
        "study_id": "routing-semantic-v1",
        "dataset_version": "routing-semantic-corpus-v1.0.0",
        "cases": [
            {
                "schema": "agent-workflow-comparative-eval/decision-study-case/v1",
                "case_id": "case-001",
                "dataset_version": "routing-semantic-corpus-v1.0.0",
                "task": "Review the parser change.",
                "metadata": {},
                "tags": ["smoke"],
                "oracle_eligible": {
                    "routing.task_class": True,
                    "routing.interaction_required": True,
                    "routing.semantic_risk": True,
                },
            }
        ],
    }
    assert validate_decision_study_corpus(corpus)["cases"][0]["case_id"] == "case-001"

    oracle = {
        "schema": "agent-workflow-comparative-eval/decision-study-oracle-bundle/v1",
        "study_id": "routing-semantic-v1",
        "dataset_version": "routing-semantic-corpus-v1.0.0",
        "oracle_version": "oracle-v1",
        "frozen": True,
        "records": [
            {
                "schema": "agent-workflow-comparative-eval/decision-study-oracle/v1",
                "case_id": "case-001",
                "dataset_version": "routing-semantic-corpus-v1.0.0",
                "labels": {
                    "routing.task_class": "review",
                    "routing.interaction_required": False,
                    "routing.semantic_risk": 1,
                },
                "provenance": {"kind": "test"},
                "adjudication": {"status": "frozen"},
                "frozen": True,
            }
        ],
    }
    validated = validate_decision_study_oracle_bundle(
        oracle,
        expected_study_id="routing-semantic-v1",
        expected_dataset_version="routing-semantic-corpus-v1.0.0",
    )
    assert validated["frozen"] is True


def test_neutral_corpus_rejects_duplicate_case_ids():
    case = {
        "schema": "agent-workflow-comparative-eval/decision-study-case/v1",
        "case_id": "dup",
        "dataset_version": "v1",
        "task": "Inspect the change.",
        "metadata": {},
        "tags": [],
        "oracle_eligible": {
            "routing.task_class": True,
            "routing.interaction_required": True,
            "routing.semantic_risk": True,
        },
    }
    with pytest.raises(ValueError, match="duplicate"):
        validate_decision_study_corpus({
            "schema": "agent-workflow-comparative-eval/decision-study-corpus/v1",
            "study_id": "routing-semantic-v1",
            "dataset_version": "v1",
            "cases": [case, dict(case)],
        })


def test_packaged_routing_semantic_corpus_has_target_size_and_blinded_oracle_view():
    corpus = load_study_corpus("routing-semantic-v1")
    assert corpus["dataset_version"] == "routing-semantic-corpus-v1.0.0"
    assert len(corpus["cases"]) == 120
    assert len({case["case_id"] for case in corpus["cases"]}) == 120
    assert all(all(case["oracle_eligible"].values()) for case in corpus["cases"])

    manifest = study_corpus_manifest("routing-semantic-v1")
    assert manifest["case_count"] == 120
    assert len(manifest["sha256"]) == 64

    view = oracle_authoring_view(corpus)
    assert len(view["cases"]) == 120
    assert view["blinding"]["construction_tags_included"] is False
    assert all("tags" not in case for case in view["cases"])
    assert all("task" in case and "metadata" in case for case in view["cases"])


def test_frozen_oracle_authoring_artifact_matches_generated_view_and_hashes():
    root = Path(__file__).resolve().parents[1]
    artifact_path = (
        root
        / "docs"
        / "studies"
        / "artifacts"
        / "routing-semantic-v1"
        / "oracle-authoring-view.json"
    )
    manifest_path = artifact_path.with_name("oracle-authoring-view.manifest.json")
    corpus_path = (
        root
        / "src"
        / "agent_workflow_comparative_eval"
        / "resources"
        / "studies"
        / "routing-semantic-v1.corpus.json"
    )

    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    generated = oracle_authoring_view(load_study_corpus("routing-semantic-v1"))

    assert artifact == generated
    assert len(artifact["cases"]) == 120
    assert all("tags" not in case for case in artifact["cases"])
    assert manifest["corpus"]["sha256"] == hashlib.sha256(corpus_path.read_bytes()).hexdigest()
    assert manifest["oracle_authoring_view"]["sha256"] == hashlib.sha256(
        artifact_path.read_bytes()
    ).hexdigest()
    assert manifest["frozen_for_independent_adjudication"] is True


def test_multiclass_calibration_normalizes_provider_mass_without_mutating_evidence():
    choice = _obs(
        "routing.task-class/v1",
        "routing.task_class",
        "choice",
        "normalized-choice",
        "implementation",
        "review",
        probabilities={
            "implementation": 0.10,
            "diagnosis": 0.10,
            "review": 0.59,
            "documentation": 0.10,
            "other": 0.10,
        },
    )
    original = dict(choice["candidate"]["result"]["probabilities"])
    outcome = make_outcome(
        choice["observation_id"],
        "static-oracle",
        {"oracle": "review"},
    )

    report = build_decision_study_report(
        [choice],
        [outcome],
        study_id="routing-semantic-v1",
        study_version="1.1.0",
        minimum_oracle_n=1,
    )

    calibration = report["seams"]["routing.task-class/v1"]["calibration"]
    assert calibration["eligible"] is True
    assert calibration["probability_normalization"]["applied"] is True
    assert calibration["probability_normalization"]["normalized_vectors"] == 1
    assert calibration["probability_normalization"]["total_vectors"] == 1
    assert calibration["probability_normalization"][
        "max_absolute_mass_deviation"
    ] == pytest.approx(0.01)
    assert choice["candidate"]["result"]["probabilities"] == original


def test_invalid_multiclass_probability_vector_disables_calibration_not_report():
    score = _obs(
        "routing.semantic-risk/v1",
        "routing.semantic_risk",
        "score",
        "invalid-score",
        1,
        1.4,
        probabilities={"0": 0.5, "1": -0.1, "2": 0.6},
    )
    outcome = make_outcome(
        score["observation_id"],
        "static-oracle",
        {"oracle": 1},
    )

    report = build_decision_study_report(
        [score],
        [outcome],
        study_id="routing-semantic-v1",
        study_version="1.1.0",
        minimum_oracle_n=1,
    )

    seam = report["seams"]["routing.semantic-risk/v1"]
    assert seam["correctness"]["candidate_ordinal"]["n"] == 1
    assert seam["calibration"]["eligible"] is False
    assert seam["calibration"]["invalid_vector_count"] == 1
    assert (
        seam["calibration"]["reason"]
        == "complete valid answered probability distribution evidence unavailable"
    )


def test_routing_semantic_v2_draft_requires_structured_justification_and_usage_scope():
    spec = load_study_spec("routing-semantic-v2")
    assert spec["study_id"] == "routing-semantic-v2"
    assert spec["status"] == "design-implementation"
    assert spec["replication_of"]["study_id"] == "routing-semantic-v1"
    assert spec["oracle_policy"]["structured_justification_required"] is True
    assert (
        spec["oracle_policy"]["adjudication_pass_schema"]
        == "agent-workflow-benchmark/decision-study-adjudication-pass/v2"
    )
    assert spec["oracle_policy"]["supplementary_reasoning_summary"] == {
        "authoritative": False,
        "private_only": True,
        "required": False,
    }
    assert spec["oracle_policy"]["usage_scope_required"] == [
        "final_output_usage",
        "aggregate_session_usage",
        "provider_request_count",
        "model_call_count",
    ]


def test_agentic_jev_pilot_has_three_arms_and_no_effectiveness_claim():
    spec = load_study_spec("agentic-jev-pilot-v1")
    assert spec["study_id"] == "agentic-jev-pilot-v1"
    assert spec["sample_policy"]["target_tasks"] == 24
    assert spec["sample_policy"]["exploratory_only"] is True
    assert spec["oracle_policy"]["required"] is False
    assert [arm["id"] for arm in spec["arms"]] == [
        "A-baseline",
        "B-skill-only",
        "C-skill-plus-jev",
    ]
    assert spec["arms"][0]["typesafe_skill"] is False
    assert spec["arms"][1]["typesafe_skill"] is True
    assert spec["arms"][1]["jev_tool"] is False
    assert spec["arms"][2]["jev_tool"] is True
    assert (
        spec["frozen_runtime_identity"]["skill_commit"]
        == "65a39f393687675ce170e6094757de20370365b9"
    )
    assert spec["claim_policy"]["no_downstream_quality_claim_until_followup_study"] is True


def test_routing_semantic_v2_replication_corpus_preserves_v1_case_content():
    v1 = load_study_corpus("routing-semantic-v1")
    v2 = load_study_corpus("routing-semantic-v2")
    assert v2["study_id"] == "routing-semantic-v2"
    assert v2["dataset_version"] == "routing-semantic-corpus-v2.0.0-draft.1"
    assert len(v1["cases"]) == len(v2["cases"]) == 120

    def semantic_projection(case):
        value = dict(case)
        value.pop("dataset_version", None)
        return value

    assert [semantic_projection(case) for case in v2["cases"]] == [
        semantic_projection(case) for case in v1["cases"]
    ]
    manifest = study_corpus_manifest("routing-semantic-v2")
    assert manifest["study_id"] == "routing-semantic-v2"
    assert manifest["case_count"] == 120
    assert len(manifest["sha256"]) == 64
