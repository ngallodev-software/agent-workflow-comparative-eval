# Changelog

## 0.2.0

Study-grade comparative-decision evidence and reporting.

- Freezes the `routing-semantic-v1` preregistered study specification before the full-study oracle or outcomes exist.
- Adds neutral provider-request evidence so one batched semantic call is accounted once rather than copied into three decision totals.
- Adds per-decision precomputed observation support preserving raw semantic decision, probability/confidence/distribution, policy candidate, applied result, fallback, and request identity.
- Adds explicit study exclusion records.
- Adds a decision-study report that evaluates Choice, Noul, and Score with different correctness/calibration semantics, Wilson intervals, deterministic paired bootstrap effects, and request-level efficiency.
- Adds separate inference-case and frozen-oracle schemas so oracle labels can be withheld from inference.
- Keeps the existing v1 generic observation/report contracts readable and unchanged.

## 0.1.0

Initial shared comparative-evaluation release candidate.

- Extracts candidate-neutral observation, outcome, pairing, cohort, metrics, statistics, and report semantics.
- Preserves explicit readers/upgraders for the historical `agent-workflow-typesafe/.../v1` evidence namespace.
- Ships the frozen `routing-v1.0.0` and `skill-behavior-v1.0.0` oracle datasets unchanged from the TypeSafe plugin baseline.
- Reproduces the selected Agent-Workflow 0.10.1 usage/cost/missingness, Wilson interval, and deterministic paired-bootstrap semantics.
- Imports neither Agent-Workflow nor TypeSafe SDK/provider code.
