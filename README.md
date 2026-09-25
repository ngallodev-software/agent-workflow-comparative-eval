# Agent-Workflow Comparative Eval

## Summary

- **What it is:** a provider-neutral library defining comparison records, frozen datasets, pairing rules, metrics, and deterministic statistics.
- **Why it exists:** comparison semantics should not belong to Agent-Workflow core or to any one semantic provider such as TypeSafe/Jev.
- **Key boundary:** it compares evidence; it does not schedule runs, select models, apply decisions, or own lifecycle state.
- **Who uses it:** Agent-Workflow providers and benchmark/reporting consumers can share the same versioned comparison meaning.

`agent-workflow-comparative-eval` is a dependency-neutral Python library for
paired feature-level evaluation. It defines the evidence contracts, frozen
datasets, pairing semantics, metrics, and deterministic statistics used to
compare bounded decision implementations without making the evaluator itself
part of workflow authority.

The library owns **comparison meaning**, not workflow authority. It does not
schedule Agent Runs, select models or executors, apply candidate decisions,
persist host lifecycle state, or call TypeSafe/Jev.

## Why this is a separate library

Agent-Workflow can compare deterministic control decisions with candidate
semantic decisions, but the meaning of that comparison should not belong to a
specific provider. Keeping the evaluation layer separate gives deterministic,
TypeSafe-backed, and future candidate implementations the same versioned
observation/outcome contracts and the same frozen corpora.

That separation also prevents benchmark and provider code from silently changing
labels, cohort rules, or result semantics when their runtime behavior changes.

```text
candidate/control evidence
        |
        v
agent-workflow-comparative-eval
  - versioned observations
  - frozen datasets
  - pairing/cohorts
  - normalized usage/timing
  - metrics/statistics
        |
        v
consumer-owned reporting / policy
```

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

Historical TypeSafe-v1 records remain readable through
`upgrade_legacy_record()` and the validators. Historical bytes are never
rewritten in place.

## Decision-study surface

Version `0.2.0` adds a preregistered, provider-neutral study layer without moving workflow authority into this package:

- a frozen `routing-semantic-v1` study specification;
- separate inference-case and frozen-oracle contracts so labels cannot leak into model inputs;
- three per-decision observations for task class, interaction requirement, and semantic risk;
- one provider-request record per batched semantic call, preventing latency/token/cost triple-counting;
- explicit exclusions and denominators;
- Choice/Noul/Score-specific correctness, calibration, and paired uncertainty reporting.

The study specification is in [`docs/studies/routing-semantic-v1.md`](docs/studies/routing-semantic-v1.md). Portfolio-safe implementation status and a Mermaid data-flow diagram are in [`docs/portfolio/COMPARATIVE_STUDY_PROGRESS.md`](docs/portfolio/COMPARATIVE_STUDY_PROGRESS.md).

## Frozen datasets

`load_corpus("routing-v1")` and `load_corpus("skill-behavior-v1")` return
the same case IDs, labels, and dataset versions shipped by the TypeSafe plugin
baseline. The shared library is their canonical owner going forward;
result-affecting edits require a new dataset version.

## Consumer boundary

- **Agent-Workflow** owns deterministic control execution, bounded built-in
  TypeSafe projection/question sets/SDK calls, shadow scheduling, semantic
  receipts, provider telemetry, persistence, lifecycle outcome joins, review,
  and acceptance.
- **Historical `agent-workflow-typesafe` records** remain compatibility inputs
  only; the standalone plugin is no longer the current ownership boundary.
- **This library** owns neutral records, datasets, pairing/cohorts, usage/timing
  normalization, metrics, deterministic statistics, and report construction.
- **Benchmark/reporting consumers** decide how observations are grouped,
  displayed, or used in a study; this package does not declare a treatment
  winner.

The library imports no Agent-Workflow runtime code and remains
dependency-neutral. Version `0.2.0` adds study-grade decision evidence while keeping the existing v1 generic records readable. The current integration candidate is qualified against Agent-Workflow `0.11.10` and agent-workflow-benchmark `0.4.0`; [`COMPATIBILITY.json`](COMPATIBILITY.json) records the exact tested revisions and CI runs.

## Study-readiness audit

The dated Phase 0 audit is preserved as a frozen engineering artifact rather than folded into README marketing copy:

- [2026-09-24 Phase 0 current-state audit and implementation plan](docs/audits/2026-09-24-phase-0-current-state-audit-and-implementation-plan.md)
- [Audit index and publication context](docs/audits/README.md)
- [Portfolio case study](https://ngallodev-software.uk/projects/agent-workflow-comparative-eval)

The audit's central finding is that the evaluation engine is substantially implemented, while the first defensible comparative-decision study still requires a frozen independent oracle corpus, lossless per-seam evidence persistence, explicit batch/request accounting, and a dedicated benchmark execution/publication lane. Current BM3–BM5 TypeSafe qualification evidence remains integration evidence rather than an effectiveness dataset.

## Related repositories

- [Agent-Workflow](https://github.com/ngallodev-software/agent-workflow) —
  workflow/lifecycle authority and the built-in bounded semantic provider.
- [Agent-Workflow TypeSafe AI](https://github.com/ngallodev-software/agent-workflow-typesafe-ai) —
  standalone provider adapter and historical source of the first evaluation
  contracts.
- [Agent-Workflow Benchmark](https://github.com/ngallodev-software/agent-workflow-benchmark) —
  benchmark execution, scoring, sealing, and reporting integration.
- [Benchmark Results](https://github.com/ngallodev-software/agent-workflow-benchmark-results) —
  public paired measurements and limitations.

## Development

```bash
python -m pip install -e '.[test]'
python -m pytest
python -m build
```

See `docs/`, `VALIDATION_REPORT.md`, and `SOURCE_PROVENANCE.json` for the
current validation and provenance record.
