from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Any

from .constants import (
    DECISION_STUDY_ORACLE_BUNDLE_SCHEMA,
    DECISION_STUDY_ORACLE_SCHEMA,
    ORACLE_ADJUDICATION_SCHEMA,
    ORACLE_CONSENSUS_RESOLUTION_SCHEMA,
    ORACLE_DISAGREEMENT_SET_SCHEMA,
    ORACLE_TIEBREAK_VIEW_SCHEMA,
)
from .contracts import validate_record
from .identity import sha256
from .study import (
    load_study_spec,
    oracle_authoring_view,
    validate_decision_study_corpus,
    validate_decision_study_oracle_bundle,
)


def _study_identity(corpus: Mapping[str, Any]) -> tuple[dict[str, Any], str]:
    value = validate_decision_study_corpus(corpus)
    spec = load_study_spec(str(value["study_id"]))
    protocol = spec.get("oracle_policy", {}).get("protocol_version")
    if not isinstance(protocol, str) or not protocol:
        raise ValueError("study spec has no oracle protocol_version")
    return spec, protocol


def _decision_order(spec: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(str(item["decision_id"]) for item in spec["decision_seams"])


def _case_index(corpus: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(case["case_id"]): case for case in corpus["cases"]}


def _eligible_pairs(
    corpus: Mapping[str, Any], spec: Mapping[str, Any]
) -> tuple[tuple[str, str], ...]:
    order = _decision_order(spec)
    result: list[tuple[str, str]] = []
    for case in corpus["cases"]:
        eligible = case["oracle_eligible"]
        for decision_id in order:
            if eligible.get(decision_id) is True:
                result.append((str(case["case_id"]), decision_id))
    return tuple(result)


def _valid_label(decision_id: str, label: Any) -> bool:
    if decision_id == "routing.task_class":
        return isinstance(label, str) and label in {
            "implementation",
            "diagnosis",
            "review",
            "documentation",
            "other",
        }
    if decision_id == "routing.interaction_required":
        return isinstance(label, bool)
    if decision_id == "routing.semantic_risk":
        return (
            isinstance(label, int)
            and not isinstance(label, bool)
            and 0 <= label <= 2
        )
    return False


def _validate_label(decision_id: str, label: Any) -> None:
    if not _valid_label(decision_id, label):
        raise ValueError(
            f"invalid oracle label for {decision_id}: {label!r}"
        )


def _labels_map(
    adjudication: Mapping[str, Any],
) -> dict[tuple[str, str], Any]:
    result: dict[tuple[str, str], Any] = {}
    for record in adjudication["records"]:
        case_id = str(record["case_id"])
        for decision_id, label in record["labels"].items():
            key = (case_id, str(decision_id))
            if key in result:
                raise ValueError(
                    f"duplicate adjudication label for {case_id}:{decision_id}"
                )
            result[key] = label
    return result


def validate_oracle_adjudication(
    value: Mapping[str, Any],
    corpus: Mapping[str, Any],
    *,
    require_complete: bool = True,
    required_pairs: Sequence[tuple[str, str]] | None = None,
) -> dict[str, Any]:
    validate_record(value, ORACLE_ADJUDICATION_SCHEMA)
    corpus_value = validate_decision_study_corpus(corpus)
    spec, protocol = _study_identity(corpus_value)

    if value["study_id"] != corpus_value["study_id"]:
        raise ValueError("oracle adjudication belongs to a different study")
    if value["dataset_version"] != corpus_value["dataset_version"]:
        raise ValueError("oracle adjudication dataset_version does not match corpus")
    if value["protocol_version"] != protocol:
        raise ValueError("oracle adjudication protocol_version does not match study")

    cases = _case_index(corpus_value)
    eligible = set(_eligible_pairs(corpus_value, spec))
    seen_cases: set[str] = set()
    labeled_pairs: set[tuple[str, str]] = set()
    records: list[dict[str, Any]] = []

    for raw in value["records"]:
        case_id = str(raw["case_id"])
        if case_id in seen_cases:
            raise ValueError(f"duplicate adjudication case ID: {case_id}")
        case = cases.get(case_id)
        if case is None:
            raise ValueError(f"adjudication contains unknown case ID: {case_id}")
        seen_cases.add(case_id)

        labels = dict(raw["labels"])
        rationales = dict(raw.get("rationales") or {})
        for decision_id, label in labels.items():
            decision_id = str(decision_id)
            pair = (case_id, decision_id)
            if pair not in eligible:
                raise ValueError(
                    f"adjudication labels an ineligible seam: {case_id}:{decision_id}"
                )
            _validate_label(decision_id, label)
            labeled_pairs.add(pair)
        unknown_rationales = set(rationales) - set(labels)
        if unknown_rationales:
            raise ValueError(
                f"rationales without labels for {case_id}: "
                + ", ".join(sorted(unknown_rationales))
            )
        records.append(
            {
                "case_id": case_id,
                "labels": labels,
                "rationales": rationales,
            }
        )

    expected = set(required_pairs) if required_pairs is not None else eligible
    if required_pairs is not None:
        unknown = expected - eligible
        if unknown:
            raise ValueError("required adjudication pairs include ineligible seams")
        if labeled_pairs != expected:
            missing = sorted(expected - labeled_pairs)
            extra = sorted(labeled_pairs - expected)
            raise ValueError(
                f"adjudication does not match required dispute set; "
                f"missing={missing!r} extra={extra!r}"
            )
    elif require_complete and labeled_pairs != eligible:
        missing = sorted(eligible - labeled_pairs)
        extra = sorted(labeled_pairs - eligible)
        raise ValueError(
            f"adjudication is incomplete; missing={missing!r} extra={extra!r}"
        )

    return {**dict(value), "records": records}


def compare_oracle_adjudications(
    corpus: Mapping[str, Any],
    left: Mapping[str, Any],
    right: Mapping[str, Any],
) -> dict[str, Any]:
    corpus_value = validate_decision_study_corpus(corpus)
    spec, protocol = _study_identity(corpus_value)
    left_value = validate_oracle_adjudication(left, corpus_value)
    right_value = validate_oracle_adjudication(right, corpus_value)

    if left_value["adjudicator_id"] == right_value["adjudicator_id"]:
        raise ValueError("A/B oracle adjudications must use different adjudicators")

    left_labels = _labels_map(left_value)
    right_labels = _labels_map(right_value)
    pairs = _eligible_pairs(corpus_value, spec)
    disagreements: list[dict[str, str]] = []
    agreement_count = 0

    for case_id, decision_id in pairs:
        if left_labels[(case_id, decision_id)] == right_labels[(case_id, decision_id)]:
            agreement_count += 1
        else:
            disagreements.append(
                {"case_id": case_id, "decision_id": decision_id}
            )

    result = {
        "schema": ORACLE_DISAGREEMENT_SET_SCHEMA,
        "study_id": corpus_value["study_id"],
        "dataset_version": corpus_value["dataset_version"],
        "protocol_version": protocol,
        "adjudicators": [
            str(left_value["adjudicator_id"]),
            str(right_value["adjudicator_id"]),
        ],
        "pair_count": len(pairs),
        "agreement_count": agreement_count,
        "disagreement_count": len(disagreements),
        "disagreements": disagreements,
    }
    validate_record(result, ORACLE_DISAGREEMENT_SET_SCHEMA)
    return result


def validate_oracle_disagreement_set(
    value: Mapping[str, Any], corpus: Mapping[str, Any]
) -> dict[str, Any]:
    validate_record(value, ORACLE_DISAGREEMENT_SET_SCHEMA)
    corpus_value = validate_decision_study_corpus(corpus)
    spec, protocol = _study_identity(corpus_value)
    if value["study_id"] != corpus_value["study_id"]:
        raise ValueError("disagreement set belongs to a different study")
    if value["dataset_version"] != corpus_value["dataset_version"]:
        raise ValueError("disagreement set dataset_version does not match corpus")
    if value["protocol_version"] != protocol:
        raise ValueError("disagreement set protocol_version does not match study")

    eligible = set(_eligible_pairs(corpus_value, spec))
    seen: set[tuple[str, str]] = set()
    for item in value["disagreements"]:
        pair = (str(item["case_id"]), str(item["decision_id"]))
        if pair in seen:
            raise ValueError(f"duplicate disagreement pair: {pair!r}")
        if pair not in eligible:
            raise ValueError(f"disagreement references ineligible pair: {pair!r}")
        seen.add(pair)

    if int(value["pair_count"]) != len(eligible):
        raise ValueError("disagreement pair_count does not match corpus")
    if int(value["disagreement_count"]) != len(seen):
        raise ValueError("disagreement_count does not match disagreements")
    if int(value["agreement_count"]) + len(seen) != len(eligible):
        raise ValueError("agreement/disagreement counts do not cover eligible pairs")
    return dict(value)


def oracle_tiebreak_view(
    corpus: Mapping[str, Any], disagreement_set: Mapping[str, Any]
) -> dict[str, Any]:
    corpus_value = validate_decision_study_corpus(corpus)
    spec, protocol = _study_identity(corpus_value)
    disputes = validate_oracle_disagreement_set(disagreement_set, corpus_value)
    if not disputes["disagreements"]:
        raise ValueError("A/B adjudications have no disagreements; C tie-break is not required")
    authoring = oracle_authoring_view(corpus_value)
    authoring_cases = {
        str(case["case_id"]): case for case in authoring["cases"]
    }

    by_case: dict[str, list[str]] = {}
    for item in disputes["disagreements"]:
        by_case.setdefault(str(item["case_id"]), []).append(
            str(item["decision_id"])
        )

    decision_order = _decision_order(spec)
    cases: list[dict[str, Any]] = []
    for source_case in corpus_value["cases"]:
        case_id = str(source_case["case_id"])
        if case_id not in by_case:
            continue
        source = authoring_cases[case_id]
        needed = set(by_case[case_id])
        cases.append(
            {
                "case_id": case_id,
                "task": source["task"],
                "metadata": dict(source["metadata"]),
                "required_decisions": [
                    decision_id
                    for decision_id in decision_order
                    if decision_id in needed
                ],
            }
        )

    relevant = {
        str(item["decision_id"])
        for item in disputes["disagreements"]
    }
    view = {
        "schema": ORACLE_TIEBREAK_VIEW_SCHEMA,
        "study_id": corpus_value["study_id"],
        "dataset_version": corpus_value["dataset_version"],
        "protocol_version": protocol,
        "decision_seams": [
            dict(item)
            for item in spec["decision_seams"]
            if str(item["decision_id"]) in relevant
        ],
        "oracle_policy": dict(spec["oracle_policy"]),
        "cases": cases,
        "blinding": {
            "construction_tags_included": False,
            "control_outputs_included": False,
            "candidate_outputs_included": False,
            "prior_adjudicator_labels_included": False,
        },
    }
    validate_record(view, ORACLE_TIEBREAK_VIEW_SCHEMA)
    return view


def validate_oracle_consensus_resolution(
    value: Mapping[str, Any],
    corpus: Mapping[str, Any],
    *,
    required_pairs: Sequence[tuple[str, str]] | None = None,
) -> dict[str, Any]:
    validate_record(value, ORACLE_CONSENSUS_RESOLUTION_SCHEMA)
    corpus_value = validate_decision_study_corpus(corpus)
    spec, protocol = _study_identity(corpus_value)
    if value["study_id"] != corpus_value["study_id"]:
        raise ValueError("consensus resolution belongs to a different study")
    if value["dataset_version"] != corpus_value["dataset_version"]:
        raise ValueError("consensus resolution dataset_version does not match corpus")
    if value["protocol_version"] != protocol:
        raise ValueError("consensus resolution protocol_version does not match study")

    eligible = set(_eligible_pairs(corpus_value, spec))
    seen: set[tuple[str, str]] = set()
    resolutions: list[dict[str, Any]] = []
    for raw in value["resolutions"]:
        pair = (str(raw["case_id"]), str(raw["decision_id"]))
        if pair in seen:
            raise ValueError(f"duplicate consensus resolution pair: {pair!r}")
        if pair not in eligible:
            raise ValueError(f"consensus resolution references ineligible pair: {pair!r}")
        _validate_label(pair[1], raw["label"])
        seen.add(pair)
        resolutions.append(dict(raw))

    if required_pairs is not None and seen != set(required_pairs):
        missing = sorted(set(required_pairs) - seen)
        extra = sorted(seen - set(required_pairs))
        raise ValueError(
            f"consensus resolutions do not match unresolved pairs; "
            f"missing={missing!r} extra={extra!r}"
        )
    return {**dict(value), "resolutions": resolutions}


def _resolution_map(
    consensus: Mapping[str, Any],
) -> dict[tuple[str, str], Mapping[str, Any]]:
    return {
        (str(item["case_id"]), str(item["decision_id"])): item
        for item in consensus["resolutions"]
    }


def freeze_oracle_bundle(
    corpus: Mapping[str, Any],
    adjudication_a: Mapping[str, Any],
    adjudication_b: Mapping[str, Any],
    *,
    adjudication_c: Mapping[str, Any] | None = None,
    consensus_resolution: Mapping[str, Any] | None = None,
    oracle_version: str,
) -> dict[str, Any]:
    if not oracle_version:
        raise ValueError("oracle_version must be non-empty")

    corpus_value = validate_decision_study_corpus(corpus)
    spec, protocol = _study_identity(corpus_value)
    a = validate_oracle_adjudication(adjudication_a, corpus_value)
    b = validate_oracle_adjudication(adjudication_b, corpus_value)
    if a["adjudicator_id"] == b["adjudicator_id"]:
        raise ValueError("A/B oracle adjudications must use different adjudicators")

    disagreement = compare_oracle_adjudications(corpus_value, a, b)
    dispute_pairs = tuple(
        (str(item["case_id"]), str(item["decision_id"]))
        for item in disagreement["disagreements"]
    )

    c: dict[str, Any] | None = None
    if dispute_pairs:
        if adjudication_c is None:
            raise ValueError("C adjudication is required for A/B disagreements")
        c = validate_oracle_adjudication(
            adjudication_c,
            corpus_value,
            require_complete=False,
            required_pairs=dispute_pairs,
        )
        if c["adjudicator_id"] in {
            a["adjudicator_id"],
            b["adjudicator_id"],
        }:
            raise ValueError("C adjudicator must be independent from A/B")
    elif adjudication_c is not None:
        raise ValueError("C adjudication supplied but A/B have no disagreements")

    a_labels = _labels_map(a)
    b_labels = _labels_map(b)
    c_labels = _labels_map(c) if c is not None else {}

    three_way: list[tuple[str, str]] = []
    for pair in dispute_pairs:
        av = a_labels[pair]
        bv = b_labels[pair]
        cv = c_labels[pair]
        if cv != av and cv != bv:
            three_way.append(pair)

    consensus: dict[str, Any] | None = None
    if three_way:
        if consensus_resolution is None:
            raise ValueError(
                "explicit consensus resolution is required for three-way conflicts: "
                + ", ".join(f"{case_id}:{decision_id}" for case_id, decision_id in three_way)
            )
        consensus = validate_oracle_consensus_resolution(
            consensus_resolution,
            corpus_value,
            required_pairs=three_way,
        )
    elif consensus_resolution is not None:
        raise ValueError(
            "consensus resolution supplied but there are no three-way conflicts"
        )
    consensus_map = _resolution_map(consensus) if consensus is not None else {}

    case_records: list[dict[str, Any]] = []
    decision_order = _decision_order(spec)
    pair_set = set(_eligible_pairs(corpus_value, spec))
    c_id = str(c["adjudicator_id"]) if c is not None else None

    for case in corpus_value["cases"]:
        case_id = str(case["case_id"])
        labels: dict[str, Any] = {}
        methods: dict[str, Any] = {}
        for decision_id in decision_order:
            pair = (case_id, decision_id)
            if pair not in pair_set:
                continue
            av = a_labels[pair]
            bv = b_labels[pair]
            votes = [
                {"adjudicator_id": str(a["adjudicator_id"]), "label": av},
                {"adjudicator_id": str(b["adjudicator_id"]), "label": bv},
            ]
            if av == bv:
                final = av
                method = "agreement"
                detail: dict[str, Any] = {
                    "method": method,
                    "independent_votes": votes,
                }
            else:
                assert c is not None and c_id is not None
                cv = c_labels[pair]
                votes.append({"adjudicator_id": c_id, "label": cv})
                counts = Counter(
                    json_key(label)
                    for label in (av, bv, cv)
                )
                majority_key, majority_count = counts.most_common(1)[0]
                if majority_count >= 2:
                    final = next(
                        label
                        for label in (av, bv, cv)
                        if json_key(label) == majority_key
                    )
                    method = "majority"
                    detail = {
                        "method": method,
                        "independent_votes": votes,
                    }
                else:
                    resolution = consensus_map[pair]
                    final = resolution["label"]
                    method = "consensus"
                    detail = {
                        "method": method,
                        "independent_votes": votes,
                        "resolved_by": list(consensus["resolved_by"]),
                        "rationale": str(resolution["rationale"]),
                    }
            _validate_label(decision_id, final)
            labels[decision_id] = final
            methods[decision_id] = detail

        record = {
            "schema": DECISION_STUDY_ORACLE_SCHEMA,
            "case_id": case_id,
            "dataset_version": corpus_value["dataset_version"],
            "labels": labels,
            "provenance": {
                "protocol_version": protocol,
                "adjudicator_ids": [
                    str(a["adjudicator_id"]),
                    str(b["adjudicator_id"]),
                    *([c_id] if c_id is not None else []),
                ],
                "submission_completed_at": {
                    str(a["adjudicator_id"]): str(a["completed_at"]),
                    str(b["adjudicator_id"]): str(b["completed_at"]),
                    **(
                        {c_id: str(c["completed_at"])}
                        if c is not None and c_id is not None
                        else {}
                    ),
                },
                "treatment_outputs_seen": False,
            },
            "adjudication": {
                "method": "independent-ab-with-blind-c-tiebreak",
                "decisions": methods,
                **(
                    {
                        "consensus_completed_at": str(consensus["completed_at"]),
                        "consensus_resolved_by": list(consensus["resolved_by"]),
                    }
                    if consensus is not None
                    else {}
                ),
            },
            "frozen": True,
        }
        validate_record(record, DECISION_STUDY_ORACLE_SCHEMA)
        case_records.append(record)

    bundle = {
        "schema": DECISION_STUDY_ORACLE_BUNDLE_SCHEMA,
        "study_id": corpus_value["study_id"],
        "dataset_version": corpus_value["dataset_version"],
        "oracle_version": oracle_version,
        "frozen": True,
        "records": case_records,
    }
    return validate_decision_study_oracle_bundle(
        bundle,
        expected_study_id=str(corpus_value["study_id"]),
        expected_dataset_version=str(corpus_value["dataset_version"]),
    )


def json_key(value: Any) -> str:
    """Stable type-sensitive key for tiny independent-vote multisets."""
    if isinstance(value, bool):
        return f"bool:{str(value).lower()}"
    if isinstance(value, int):
        return f"int:{value}"
    return f"str:{value}"


def oracle_bundle_sha256(bundle: Mapping[str, Any]) -> str:
    validate_decision_study_oracle_bundle(bundle)
    return sha256(bundle)
