# Agent-Workflow Comparative Eval

`agent-workflow-comparative-eval` is a dependency-neutral Python library for paired feature-level evaluation. It defines the evidence contracts and measurement semantics shared by Agent-Workflow's built-in bounded semantic provider path and other candidate implementations.

The library owns **comparison meaning**, not workflow authority. It does not schedule Agent Runs, select models/executors, apply candidate decisions, persist host lifecycle state, or call TypeSafe/Jev.

## Core surface

```python
from agent_workflow_comparative_eval import (
    load_corpus,
    observation,
    validate_observation,
    run_static_cases,
    outcome,
    comparison_report,
)
```

Canonical v1 records use the neutral namespace:

- `agent-workflow-comparative-eval/eval-feature/v1`
- `agent-workflow-comparative-eval/comparison-observation/v1`
- `agent-workflow-comparative-eval/comparison-outcome/v1`
- `agent-workflow-comparative-eval/comparison-report/v1`

Historical TypeSafe-v1 records remain readable through `upgrade_legacy_record()` and the validators. Historical bytes are never rewritten in place.

## Frozen datasets

`load_corpus("routing-v1")` and `load_corpus("skill-behavior-v1")` return the same case IDs, labels, and dataset versions shipped by the TypeSafe plugin baseline. The shared library is their canonical owner going forward; result-affecting edits require a new dataset version.

## Consumer boundary

- **Agent-Workflow** owns deterministic control execution, bounded built-in TypeSafe projection/question sets/SDK calls, shadow scheduling, semantic receipts, provider telemetry, persistence, lifecycle outcome joins, review, and acceptance.
- **Historical `agent-workflow-typesafe` records** remain compatibility inputs only; the standalone plugin is no longer the current ownership boundary.
- **This library** owns neutral records, datasets, pairing/cohorts, usage/timing normalization, metrics, deterministic statistics, and report construction.

The library imports no Agent-Workflow runtime code and remains dependency-neutral. Library version `0.1.0` is recorded as verified with Agent-Workflow `0.10.1` through `0.11.4` in `COMPATIBILITY.json`.
