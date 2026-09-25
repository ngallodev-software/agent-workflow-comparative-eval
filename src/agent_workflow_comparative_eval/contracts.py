from __future__ import annotations
import json
from collections.abc import Mapping
from importlib.resources import files
from typing import Any
from jsonschema import Draft202012Validator

from .constants import (
    FEATURE_SCHEMA, OBSERVATION_SCHEMA, OUTCOME_SCHEMA, REPORT_SCHEMA,
    PROVIDER_REQUEST_SCHEMA, DECISION_STUDY_EXCLUSION_SCHEMA,
    DECISION_STUDY_REPORT_SCHEMA, DECISION_STUDY_SPEC_SCHEMA,
    DECISION_STUDY_CASE_SCHEMA, DECISION_STUDY_ORACLE_SCHEMA,
    DECISION_STUDY_CORPUS_SCHEMA, DECISION_STUDY_ORACLE_BUNDLE_SCHEMA,
    LEGACY_FEATURE_SCHEMA, LEGACY_OBSERVATION_SCHEMA, LEGACY_OUTCOME_SCHEMA, LEGACY_REPORT_SCHEMA,
    LEGACY_TO_CANONICAL,
)
from .errors import ContractError

_SCHEMA_FILES = {
    FEATURE_SCHEMA: "eval-feature.schema.json",
    OBSERVATION_SCHEMA: "comparison-observation.schema.json",
    OUTCOME_SCHEMA: "comparison-outcome.schema.json",
    REPORT_SCHEMA: "comparison-report.schema.json",
    PROVIDER_REQUEST_SCHEMA: "provider-request.schema.json",
    DECISION_STUDY_EXCLUSION_SCHEMA: "decision-study-exclusion.schema.json",
    DECISION_STUDY_REPORT_SCHEMA: "decision-study-report.schema.json",
    DECISION_STUDY_SPEC_SCHEMA: "decision-study-spec.schema.json",
    DECISION_STUDY_CASE_SCHEMA: "decision-study-case.schema.json",
    DECISION_STUDY_ORACLE_SCHEMA: "decision-study-oracle.schema.json",
    DECISION_STUDY_CORPUS_SCHEMA: "decision-study-corpus.schema.json",
    DECISION_STUDY_ORACLE_BUNDLE_SCHEMA: "decision-study-oracle-bundle.schema.json",
    LEGACY_FEATURE_SCHEMA: "eval-feature.schema.json",
    LEGACY_OBSERVATION_SCHEMA: "comparison-observation.schema.json",
    LEGACY_OUTCOME_SCHEMA: "comparison-outcome.schema.json",
    LEGACY_REPORT_SCHEMA: "comparison-report.schema.json",
    "agent-workflow-comparative-eval/library-release-handoff/v1": "library-release-handoff.schema.json",
    "agent-workflow-comparative-eval/consumer-adoption-handoff/v1": "consumer-adoption-handoff.schema.json",
}


def schema_for(schema_id: str) -> dict[str, Any]:
    try:
        filename = _SCHEMA_FILES[schema_id]
    except KeyError as exc:
        raise ContractError(f"unknown comparative-eval schema: {schema_id}") from exc
    root = files("agent_workflow_comparative_eval").joinpath("schemas")
    if schema_id in LEGACY_TO_CANONICAL:
        root = root.joinpath("legacy")
    return json.loads(root.joinpath(filename).read_text(encoding="utf-8"))


def validate_record(value: Mapping[str, Any], schema_id: str | None = None) -> None:
    declared = schema_id or value.get("schema")
    if not isinstance(declared, str):
        raise ContractError("comparative-eval record has no schema")
    schema = schema_for(declared)
    errors = sorted(Draft202012Validator(schema).iter_errors(dict(value)), key=lambda e: list(e.path))
    if errors:
        first = errors[0]
        where = ".".join(str(x) for x in first.path) or "<root>"
        raise ContractError(f"{declared} validation failed at {where}: {first.message}")


def known_schema_ids() -> tuple[str, ...]:
    return tuple(sorted(_SCHEMA_FILES))
