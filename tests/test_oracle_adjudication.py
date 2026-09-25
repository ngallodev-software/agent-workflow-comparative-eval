from __future__ import annotations

import copy

import pytest

from agent_workflow_comparative_eval import (
    compare_oracle_adjudications,
    freeze_oracle_bundle,
    oracle_bundle_sha256,
    oracle_tiebreak_view,
    validate_oracle_adjudication,
)


def _corpus():
    return {
        "schema": "agent-workflow-comparative-eval/decision-study-corpus/v1",
        "study_id": "routing-semantic-v1",
        "dataset_version": "oracle-tooling-test-v1",
        "cases": [
            {
                "schema": "agent-workflow-comparative-eval/decision-study-case/v1",
                "case_id": "case-1",
                "dataset_version": "oracle-tooling-test-v1",
                "task": "Review the parser, fix any demonstrated defect, and document the change.",
                "metadata": {"task_type": "review", "risk": "normal"},
                "tags": ["construction-only", "mixed-intent"],
                "oracle_eligible": {
                    "routing.task_class": True,
                    "routing.interaction_required": True,
                    "routing.semantic_risk": True,
                },
            },
            {
                "schema": "agent-workflow-comparative-eval/decision-study-case/v1",
                "case_id": "case-2",
                "dataset_version": "oracle-tooling-test-v1",
                "task": "Prepare the approved production migration script without executing it.",
                "metadata": {
                    "task_type": "implementation",
                    "risk": "high",
                    "authorization_state": "approved",
                },
                "tags": ["construction-only", "authorization"],
                "oracle_eligible": {
                    "routing.task_class": True,
                    "routing.interaction_required": True,
                    "routing.semantic_risk": True,
                },
            },
        ],
    }


def _submission(adjudicator_id, records):
    return {
        "schema": "agent-workflow-comparative-eval/oracle-adjudication/v1",
        "study_id": "routing-semantic-v1",
        "dataset_version": "oracle-tooling-test-v1",
        "protocol_version": "routing-semantic-oracle-v1.0.0",
        "adjudicator_id": adjudicator_id,
        "blinded": True,
        "completed_at": f"2026-09-25T00:00:0{len(adjudicator_id)}Z",
        "records": records,
    }


def _record(case_id, task_class, interaction, risk):
    return {
        "case_id": case_id,
        "labels": {
            "routing.task_class": task_class,
            "routing.interaction_required": interaction,
            "routing.semantic_risk": risk,
        },
        "rationales": {},
    }


def _ab():
    a = _submission(
        "A",
        [
            _record("case-1", "implementation", False, 0),
            _record("case-2", "implementation", False, 2),
        ],
    )
    b = _submission(
        "B",
        [
            _record("case-1", "review", True, 2),
            _record("case-2", "implementation", False, 2),
        ],
    )
    return a, b


def test_complete_adjudication_is_bound_to_corpus_and_protocol():
    a, _ = _ab()
    validated = validate_oracle_adjudication(a, _corpus())
    assert validated["adjudicator_id"] == "A"

    incomplete = copy.deepcopy(a)
    incomplete["records"][0]["labels"].pop("routing.semantic_risk")
    with pytest.raises(ValueError, match="incomplete"):
        validate_oracle_adjudication(incomplete, _corpus())

    wrong = copy.deepcopy(a)
    wrong["protocol_version"] = "wrong"
    with pytest.raises(ValueError, match="protocol_version"):
        validate_oracle_adjudication(wrong, _corpus())


def test_ab_comparison_exposes_disputed_pairs_but_not_votes():
    a, b = _ab()
    comparison = compare_oracle_adjudications(_corpus(), a, b)
    assert comparison["pair_count"] == 6
    assert comparison["agreement_count"] == 3
    assert comparison["disagreement_count"] == 3
    assert comparison["disagreements"] == [
        {"case_id": "case-1", "decision_id": "routing.task_class"},
        {"case_id": "case-1", "decision_id": "routing.interaction_required"},
        {"case_id": "case-1", "decision_id": "routing.semantic_risk"},
    ]
    encoded = repr(comparison)
    assert "implementation" not in encoded
    assert "review" not in encoded

    same = copy.deepcopy(b)
    same["adjudicator_id"] = "A"
    with pytest.raises(ValueError, match="different adjudicators"):
        compare_oracle_adjudications(_corpus(), a, same)


def test_tiebreak_view_is_blind_to_ab_votes_and_construction_tags():
    a, b = _ab()
    comparison = compare_oracle_adjudications(_corpus(), a, b)
    view = oracle_tiebreak_view(_corpus(), comparison)
    assert len(view["cases"]) == 1
    assert view["cases"][0]["case_id"] == "case-1"
    assert view["cases"][0]["required_decisions"] == [
        "routing.task_class",
        "routing.interaction_required",
        "routing.semantic_risk",
    ]
    encoded = repr(view)
    assert "construction-only" not in encoded
    assert "independent_votes" not in encoded
    assert view["blinding"]["prior_adjudicator_labels_included"] is False


def test_freeze_requires_c_then_explicit_consensus_for_three_way_conflicts():
    a, b = _ab()
    with pytest.raises(ValueError, match="C adjudication"):
        freeze_oracle_bundle(
            _corpus(), a, b, oracle_version="oracle-test-v1"
        )

    c = _submission(
        "C",
        [
            {
                "case_id": "case-1",
                "labels": {
                    "routing.task_class": "diagnosis",
                    "routing.interaction_required": False,
                    "routing.semantic_risk": 1,
                },
                "rationales": {},
            }
        ],
    )
    with pytest.raises(ValueError, match="consensus resolution"):
        freeze_oracle_bundle(
            _corpus(),
            a,
            b,
            adjudication_c=c,
            oracle_version="oracle-test-v1",
        )

    consensus = {
        "schema": "agent-workflow-comparative-eval/oracle-consensus-resolution/v1",
        "study_id": "routing-semantic-v1",
        "dataset_version": "oracle-tooling-test-v1",
        "protocol_version": "routing-semantic-oracle-v1.0.0",
        "resolved_by": ["panel-1"],
        "blinded_to_treatment_outputs": True,
        "completed_at": "2026-09-25T00:10:00Z",
        "resolutions": [
            {
                "case_id": "case-1",
                "decision_id": "routing.task_class",
                "label": "implementation",
                "rationale": "The required final deliverable changes executable behavior.",
            },
            {
                "case_id": "case-1",
                "decision_id": "routing.semantic_risk",
                "label": 1,
                "rationale": "The change is meaningful but locally recoverable.",
            },
        ],
    }
    oracle = freeze_oracle_bundle(
        _corpus(),
        a,
        b,
        adjudication_c=c,
        consensus_resolution=consensus,
        oracle_version="oracle-test-v1",
    )
    assert oracle["frozen"] is True
    assert oracle["records"][0]["labels"] == {
        "routing.task_class": "implementation",
        "routing.interaction_required": False,
        "routing.semantic_risk": 1,
    }
    assert oracle["records"][1]["labels"] == {
        "routing.task_class": "implementation",
        "routing.interaction_required": False,
        "routing.semantic_risk": 2,
    }
    methods = oracle["records"][0]["adjudication"]["decisions"]
    assert methods["routing.task_class"]["method"] == "consensus"
    assert methods["routing.interaction_required"]["method"] == "majority"
    assert methods["routing.semantic_risk"]["method"] == "consensus"
    assert oracle["records"][1]["adjudication"]["decisions"]["routing.task_class"]["method"] == "agreement"

    assert oracle_bundle_sha256(oracle) == oracle_bundle_sha256(copy.deepcopy(oracle))


def test_c_must_be_distinct_and_exactly_cover_disputes():
    a, b = _ab()
    c = _submission(
        "A",
        [
            {
                "case_id": "case-1",
                "labels": {
                    "routing.task_class": "implementation",
                    "routing.interaction_required": False,
                    "routing.semantic_risk": 2,
                },
                "rationales": {},
            }
        ],
    )
    with pytest.raises(ValueError, match="independent from A/B"):
        freeze_oracle_bundle(
            _corpus(),
            a,
            b,
            adjudication_c=c,
            oracle_version="oracle-test-v1",
        )

    partial = _submission(
        "C",
        [
            {
                "case_id": "case-1",
                "labels": {"routing.task_class": "implementation"},
                "rationales": {},
            }
        ],
    )
    with pytest.raises(ValueError, match="required dispute set"):
        freeze_oracle_bundle(
            _corpus(),
            a,
            b,
            adjudication_c=partial,
            oracle_version="oracle-test-v1",
        )
