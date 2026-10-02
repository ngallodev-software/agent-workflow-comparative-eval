from agent_workflow_comparative_eval import (
    build_paired_decision_report,
    list_studies,
    load_study_spec,
    make_paired_decision_trial,
    mcnemar_exact_p_value,
)


SOURCE = {
    "task": "inspect_evals/swe_lancer",
    "task_variant": "swe_manager",
    "inspect_evals_commit": "1" * 40,
    "eval_version": "1-B",
    "scorer": "inspect_evals.swe_lancer.scorers.swe_lancer_scorer",
    "scorer_source_sha256": "a" * 64,
    "cohort_sha256": "b" * 64,
}
RUNTIME = {
    "model": "openai-api/codex-lb/gpt-6-luna",
    "reasoning_effort": "high",
    "skill_commit": "d0ac1ef45d1b79b18b2905872c62cb9e68d961c7",
    "skill_sha256": "c" * 64,
}


def arm(score, selected, *, calls=0, successful=0):
    value = {
        "status": "success",
        "official_score": score,
        "selected_proposal_id": selected,
        "decision_record": {
            "justification": "Visible bounded justification with decisive evidence.",
            "semantic_evidence_reconciliation": "Semantic evidence was advisory to primary evidence.",
        },
        "usage": {},
        "duration_seconds": 1.0,
        "error_class": None,
    }
    if calls is not None:
        value["jev"] = {
            "tool_calls": calls,
            "successful_calls": successful,
            "context_complete": True if successful else None,
            "request_hashes": ["d" * 64] if successful else [],
        }
    return value


def trial(sample_id, control_score, treatment_score, control_selected, treatment_selected):
    control = arm(control_score, control_selected, calls=None)
    treatment = arm(
        treatment_score,
        treatment_selected,
        calls=1,
        successful=1,
    )
    return make_paired_decision_trial(
        study_id="agentic-jev-swe-manager-v1",
        sample_id=sample_id,
        repetition=0,
        source=SOURCE,
        runtime=RUNTIME,
        control=control,
        treatment=treatment,
    )


def test_exact_mcnemar():
    assert mcnemar_exact_p_value(0, 5) == 0.0625
    assert mcnemar_exact_p_value(0, 0) == 1.0


def test_paired_report_classifies_all_four_cells():
    values = [
        trial("a", 1, 1, "p1", "p1"),
        trial("b", 0, 0, "p1", "p2"),
        trial("c", 1, 0, "p1", "p2"),
        trial("d", 0, 1, "p1", "p2"),
    ]
    report = build_paired_decision_report(
        values,
        study_id="agentic-jev-swe-manager-v1",
        study_version="1.0.0-preregistered",
        minimum_interval_n=2,
    )
    assert report["paired_n"] == 4
    assert report["primary"]["control"]["correct"] == 2
    assert report["primary"]["treatment"]["correct"] == 2
    assert report["primary"]["treatment_minus_control_accuracy"] == 0.0
    assert report["discordant_pairs"]["control_only_correct"] == 1
    assert report["discordant_pairs"]["treatment_only_correct"] == 1
    assert report["decision_change"]["changed"] == 3
    assert report["jev_exposure"]["trials_with_successful_call"] == 4


def test_missing_score_is_attempt_level_incorrect():
    value = trial("missing", None, 1, None, "p2")
    assert value["control"]["score_available"] is False
    assert value["control"]["correct"] is False
    assert value["pair"]["classification"] == "treatment_only_correct"


def test_swe_manager_study_is_registered():
    assert "agentic-jev-swe-manager-v1" in list_studies()
    spec = load_study_spec("agentic-jev-swe-manager-v1")
    assert spec["sample_policy"]["target_tasks"] == 30
    assert spec["oracle_policy"]["gold_redefinition_forbidden"] is True
