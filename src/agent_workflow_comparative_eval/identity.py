from __future__ import annotations
import hashlib
import json
from collections.abc import Mapping
from typing import Any


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


canonical_hash = sha256


def cohort_key(*, feature_id: str, mode: str, identity: Mapping[str, Any]) -> str:
    return sha256({"feature_id": feature_id, "mode": mode, "identity": dict(identity)})


def identity_equal(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    return canonical_json(dict(left)) == canonical_json(dict(right))
