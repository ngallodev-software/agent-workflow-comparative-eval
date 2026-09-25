# Comparative Evaluation Implementation Checkpoint

**Date:** 2026-09-24  
**Checkpoint:** comparative-study-v1  
**Purpose:** durable continuation point before compatibility-record finalization and merges.

## Current status

All four integration branches are green.

| Repository | Branch | PR | Current HEAD | CI |
| --- | --- | ---: | --- | --- |
| agent-workflow-comparative-eval | comparative-study-v1 | #2 | bc8261f24c0bf51e955e9292598b3a0343d79f7d | success |
| agent-workflow | comparative-study-v1 | #33 | 1388dbf31672c55dd35c0fcc3a3293fbaf4cc69d | success |
| agent-workflow-benchmark | comparative-study-v1 | #31 | 1205b83d2621be3e6bcb566feaf6650d6fc88885 | success |
| agent-workflow-benchmark-results | comparative-study-v1 | #5 | a328eb942bc0dc2eeedae4e02176dd0b608fae36 | success |

## Implemented

### agent-workflow-comparative-eval 0.2.0

- Frozen preregistered study specification: routing-semantic-v1.
- Separate inference-case and frozen-oracle contracts.
- Provider-request evidence contract for one batched semantic call.
- Explicit study exclusion records and reason codes.
- Lossless per-decision observation support for:
  - routing.task_class / Choice;
  - routing.interaction_required / Noul;
  - routing.semantic_risk / Score.
- Decision-study reporting:
  - correctness;
  - classification and ordinal metrics;
  - calibration;
  - reliability;
  - Wilson intervals;
  - deterministic paired bootstrap effects;
  - request-level efficiency;
  - explicit sample eligibility.
- Candidate timeout/error/no-decision cases remain in attempt-level correctness denominators.
- Calibration remains conditional on usable probability evidence.
- Minimum oracle-eligible sample threshold is machine-readable.
- Portfolio-ready study progress/architecture documentation.
- New CI matrix on Python 3.11 and 3.13.

### Agent-Workflow 0.11.10

- Comparative-eval dependency moved to 0.2.0.
- TypeSafe/Jev DecisionEvidence now retains:
  - request ID;
  - projector version;
  - probability/confidence/distribution;
  - usage/token evidence;
  - request hash;
  - model/question-set identity.
- Decision receipts preserve the same evidence.
- Comparative persistence now emits three decision observations instead of one lossy composed-route observation.
- One shared provider-request record is persisted for the batched Jev call.
- Receipt-to-neutral-evidence projection is centralized in routing_comparison_records().
- Normal runtime and benchmark study paths reuse the same projection code.
- Deterministic control remains authoritative in comparative mode.
- Privacy invariant verifies raw task text is absent from neutral SQLite evidence.
- CI exercises the real comparative-eval 0.2.0 integration.
- TypeSafe adapter invariant verifies SDK request identity and usage survive into DecisionEvidence.

### agent-workflow-benchmark 0.4.0

Dedicated comparative decision-study lane added:

- decision-study-validate
- decision-study-run
- decision-study-report
- decision-study-publish-prepare

Important safeguards:

- run accepts only the inference corpus; it has no oracle argument;
- run-manifest records oracle_seen_during_inference: false;
- report is the first stage allowed to load the frozen oracle;
- oracle-like keys in inference metadata are rejected;
- production Agent-Workflow decision boundary is reused;
- one Jev request becomes three decision observations but one request-level usage/latency record;
- publication preparation excludes raw TypeSafe HTTP audit logs;
- publication manifest and Markdown report are generated automatically;
- development samples below threshold are marked study_eligible: false.

Non-network integration tests cover oracle separation and request deduplication.

### agent-workflow-benchmark-results

Public evidence scaffold added without fabricated metrics:

- comparative-eval/README.md
- comparative-eval/routing-semantic-v1/IMPLEMENTATION_STATUS.md
- methodology/README.md
- limitations/README.md

The scaffold explicitly says:

- full corpus not yet frozen;
- independent oracle not yet frozen;
- full study not run;
- no current Jev effectiveness claim is supported.

It includes a portfolio-ready Mermaid architecture diagram and status boundary.

## Important design decisions now locked

1. Agreement is not correctness.
2. Oracle labels are separate from inference input and blinded until post-inference reporting.
3. One production-style batched Jev request is evaluated as three decision seams but counted once for provider latency/tokens/cost.
4. Raw semantic evidence, host policy candidate, and applied result are separate layers.
5. Provider failures/no-decision remain effectiveness/reliability evidence rather than being silently removed.
6. Candidate accuracy at the attempt level counts failure/no-decision as incorrect; answered-only accuracy is reported separately.
7. Calibration is conditional on answered cases with usable probability evidence.
8. Minimum publishable sample target is 100 oracle-eligible cases per seam, target 120 shared cases.
9. A favorable Jev result is not required for publication.
10. Portfolio claims must distinguish implementation progress from empirical study results.

## Portfolio-safe material already surfaced

- comparative-eval: docs/portfolio/COMPARATIVE_STUDY_PROGRESS.md
- comparative-eval: docs/studies/routing-semantic-v1.md
- benchmark: docs/COMPARATIVE_DECISION_STUDY.md
- benchmark-results: comparative-eval/routing-semantic-v1/IMPLEMENTATION_STATUS.md

These contain Mermaid diagrams and implementation-status language suitable for partial or full rendering.

## Remaining work from this checkpoint

### Immediate

1. Update comparative-eval compatibility/validation records to reflect completed qualification against:
   - Agent-Workflow 0.11.10;
   - benchmark 0.4.0.
2. Verify PR metadata/mergeability.
3. Merge in dependency order:
   1. agent-workflow-comparative-eval PR #2;
   2. Agent-Workflow PR #33;
   3. agent-workflow-benchmark PR #31;
   4. agent-workflow-benchmark-results PR #5.
4. After each upstream merge, update downstream dependency references from integration branches to released/default-branch versions if needed and rerun CI.
5. Tag/release versions only after the merged default branches are revalidated.

### Study work after implementation merge

1. Build/freeze the 120-case public-safe routing corpus.
2. Establish independent blinded oracle workflow/adjudication.
3. Freeze oracle and hashes.
4. Run a small development study to validate instrumentation only.
5. If instrumentation is clean, run the full preregistered study.
6. Publish sanitized results regardless of whether Jev improves, matches, or underperforms deterministic control.

## Do not do yet

- Do not claim Jev improves routing correctness, quality, latency, tokens, cost, or downstream software quality.
- Do not pool BM3-BM5 TypeSafe qualification calls into the new study.
- Do not change study-defining labels, rubrics, exclusions, or primary metrics after inspecting the full-study outcomes without creating a new version.
