from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from .constants import LEGACY_TO_CANONICAL, CANONICAL_TO_LEGACY
from .contracts import validate_record
from .errors import ContractError


def upgrade_legacy_record(value: Mapping[str, Any], *, validate: bool = True) -> dict[str, Any]:
    result = dict(value)
    schema = result.get("schema")
    if validate and isinstance(schema, str):
        validate_record(result, schema)
    if schema in LEGACY_TO_CANONICAL:
        result["schema"] = LEGACY_TO_CANONICAL[schema]
    elif schema not in CANONICAL_TO_LEGACY:
        raise ContractError(f"record is not a known comparative-eval v1 record: {schema!r}")
    if validate:
        validate_record(result)
    return result


def downgrade_typesafe_v1_record(value: Mapping[str, Any], *, validate: bool = True) -> dict[str, Any]:
    result = dict(value)
    schema = result.get("schema")
    if validate and isinstance(schema, str):
        validate_record(result, schema)
    if schema in CANONICAL_TO_LEGACY:
        result["schema"] = CANONICAL_TO_LEGACY[schema]
    elif schema not in LEGACY_TO_CANONICAL:
        raise ContractError(f"record is not a known comparative-eval v1 record: {schema!r}")
    if validate:
        validate_record(result)
    return result
