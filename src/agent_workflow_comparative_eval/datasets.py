from __future__ import annotations
import hashlib
import json
from importlib.resources import files
from typing import Any

_DATASETS = {"routing-v1": "routing-v1.json", "skill-behavior-v1": "skill-behavior-v1.json"}


def _resource(name: str):
    try:
        filename = _DATASETS[name]
    except KeyError as exc:
        raise ValueError(f"unknown evaluation corpus: {name}") from exc
    return files("agent_workflow_comparative_eval").joinpath("resources", "datasets", filename)


def dataset_document(name: str) -> dict[str, Any]:
    value = json.loads(_resource(name).read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("cases"), list):
        raise ValueError("evaluation corpus is invalid")
    return value


def load_corpus(name: str) -> list[dict[str, Any]]:
    value = dataset_document(name)
    cases = value["cases"]
    if not all(isinstance(case, dict) for case in cases):
        raise ValueError("evaluation corpus is invalid")
    return [dict(case, dataset_version=value["dataset_version"]) for case in cases]


load_dataset = load_corpus


def list_datasets() -> tuple[str, ...]:
    return tuple(sorted(_DATASETS))


def dataset_manifest(name: str) -> dict[str, Any]:
    resource = _resource(name)
    raw = resource.read_bytes()
    value = json.loads(raw)
    return {
        "name": name,
        "filename": _DATASETS[name],
        "dataset_version": value.get("dataset_version"),
        "feature_id": value.get("feature_id"),
        "case_count": len(value.get("cases", [])),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }
