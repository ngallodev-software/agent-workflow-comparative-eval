# Changelog

## 0.3.3

Pre-run evidence hardening for the preregistered Agentic-Jev SWE-Lancer study.

- Binds paired reports to one frozen source/runtime identity and preserves the actual frozen cohort artifact SHA separately from the paired-key digest.
- Adds paired latency and token-overhead summaries so the preregistered overhead question is reportable from captured trial evidence.
- Preserves exact Jev context-completeness call counts and resolved Jev model identities while retaining the existing trial-level process summary.
- Adds score-availability reliability counts and rejects mixed-runtime or mixed-source reports before aggregation.
- Does not change the frozen study cohort policy, arms, prompt, official correctness oracle, primary estimand, missing-score rule, or inferential methods.

## 0.3.2

Preregistered paired task-outcome semantics for the first Jev effectiveness study.

- Adds `agentic-jev-swe-manager-v1`, a fixed 30-task fresh SWE-Lancer manager study using GPT-6 Luna in paired skill-only control and same-skill + live-Jev treatment arms.
- Treats the upstream Inspect Evals SWE-Lancer scorer as canonical correctness rather than reimplementing gold/scoring locally.
- Adds versioned paired-decision trial/report records with intent-to-treat attempt accuracy, four-cell paired correctness classification, deterministic paired bootstrap intervals, and two-sided exact McNemar inference.
- Preserves Jev activation/context and visible justification/reconciliation evidence without requiring or exporting hidden chain-of-thought.
- Keeps previously observed manager tasks out of the new cohort and forbids outcome-dependent stopping or called-only causal claims.

## 0.3.0

Versioned follow-up study contracts and pre-live methodological controls.

- Adds `routing-semantic-v2` as a separate methodological replication with required structured justifications, explicit usage scope, and frozen DeepSeek adjudicator continuity.
- Adds the `agentic-jev-pilot-v1` exploratory three-arm coding-agent study with frozen GPT-6 Luna/high runtime identity.
- Adds the v2 replication corpus identity while preserving v1 case semantics and frozen/public v1 evidence.
- Records pre-live model-identity boundaries and live-qualification corrections without rewriting earlier checkpoints.
- Keeps legacy datasets, v1 study semantics, generic comparison contracts, and historical readers intact.

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
