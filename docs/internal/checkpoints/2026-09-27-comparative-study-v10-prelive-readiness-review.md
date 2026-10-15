# Comparative Evaluation — v2 Pre-Live Readiness Review Complete

**Date:** 2026-09-27  
**Checkpoint:** `comparative-study-v10`  
**Relationship to v8/v9:** additive readiness review; earlier checkpoints remain historical records of the implementation and first runtime-identity hardening boundaries.

## Review conclusion

The repository-level v2 / agentic-Jev change surface has now been reviewed end-to-end through:

- comparative-eval merge `b9bedd0d3664e1d47628bfa2b0c3afea2c009399`;
- benchmark merge `ef9f2b5836369b08a9641492ebb6fa4f18b5cee4`.

The codebase is ready for the **next bounded live qualification step**.

It is not yet ready for:

- real routing-semantic-v2 A/B/C adjudication;
- automatic v1 re-score/replication;
- the full 24 × 3 agentic-Jev exploratory pilot;
- public v2/pilot result publication.

## What was verified

### routing-semantic-v2 contract

- new study identity remains separate from v1;
- the v2 corpus has 120 cases;
- case semantic content is unchanged from v1 apart from new study/dataset identity;
- the v2 pass requires structured justification for every eligible seam;
- A/B labels and justifications remain excluded from the C dispute view;
- human three-way review can receive independent A/B/C labels and structured justifications after C completes;
- final-output and aggregate-session usage are separate;
- reasoning summaries are supplementary/private and not required authoritative rationale;
- the IA-9/10/11 synthetic preflight deliberately cannot qualify the real cohort by itself.

### agentic-jev-pilot-v1 contract

- three arms remain baseline / skill-only / skill+Jev;
- authoring opportunity tags remain hidden from the coding agent;
- TypeSafe credentials remain host-only;
- the pilot remains exploratory with no overall-winner or coding-quality claim;
- runtime/tool qualification remains a prerequisite for the 24 × 3 run.

## Additional review corrections

### Benchmark PR #56 — complete runtime/environment freeze checks

Merge:

`d6ad29b16572358376d73bafdf7097e40cbd4954`

The earlier lock recorded some runtime identities without rechecking all of them before qualification/run.

The strengthened lock now binds and rechecks:

- Inspect AI / Inspect SWE pinned versions;
- Codex platform;
- Docker/Compose identity;
- resolved local sandbox image identity for `python:3.12-bookworm`;
- benchmark Inspect-harness implementation SHA-256;
- host-side Jev implementation SHA-256;
- `typesafe-sdk==0.6.0`;
- frozen TypeSafe skill SHA;
- frozen 24-task manifest SHA.

The live bridge qualification was also tightened to require exactly one Jev invocation, exactly one receipt, and exactly one successful receipt.

All benchmark `test`, `agentic-jev-import`, and `inspect-import` jobs passed before merge.

### Benchmark PR #57 — preserve the v1 execution boundary

Merge:

`ef9f2b5836369b08a9641492ebb6fa4f18b5cee4`

The v2 provenance upgrade had been applied in a shared Inspect runner, which meant a hypothetical new v1 execution would have emitted the v2 scoped provenance shape.

The frozen/published v1 result was never changed or rerun.

PR #57 makes provenance output version-aware:

- v1 retains the historical `model_usage` artifact shape;
- v2 receives `final_output_usage`, `aggregate_session_usage`, request/model-call counts, and reasoning-summary observation.

A regression test now asserts the v1/v2 separation.

## Repository ownership check

No routing-semantic-v2 or agentic-jev-pilot implementation is required in Agent-Workflow core at this stage.

No v2/pilot evidence belongs in benchmark-results yet.

That preserves the current boundary:

~~~text
comparative-eval
  study semantics / contracts / claim boundary

benchmark
  execution / qualification / evidence collection

Agent-Workflow
  existing deterministic workflow authority

benchmark-results
  sanitized published evidence only after a publication gate
~~~

## Immediate next step

### Track A — routing-semantic-v2

Run the live synthetic IA-9/10/11 evidence preflight using the initially matched v1 adjudicator model identity.

Required result:

~~~text
IA-9 pass
IA-10 pass
IA-11 pass
real_cohort_ready: false
~~~

The `false` value remains required and expected.

After a passing preflight:

1. freeze the canonical real-v2 blinded authoring view;
2. create/freeze the real v2 module/runtime lock;
3. implement/run the complete IA-1..IA-11 real-cohort qualification path;
4. only then authorize real A/B/C adjudication.

### Track B — agentic-jev-pilot-v1

Before the runtime freeze, ensure `python:3.12-bookworm` is materialized locally so its exact image identity can be recorded.

Then:

1. create the strengthened runtime lock;
2. run the exactly-once live Jev bridge qualification;
3. inspect both artifacts.

Do not start the 24 × 3 pilot immediately after qualification.

Before spending the 72 executions, freeze a task-level analysis/annotation contract for:

- opportunity-conditioned invocation;
- primitive choice;
- immediate follow-through / action change.

The raw Inspect logs and private receipts preserve the underlying evidence, but the analysis projection should be defined before pilot outcomes are observed.

## Later decision still requiring preregistration

The v2 study says that sufficiently different v2 oracle labels may motivate a re-score or replication of the v1 candidate/control result.

The operational threshold for "materially different" is not yet frozen.

That threshold is not required for the synthetic preflight, but it must be fixed before observed v2-vs-v1 oracle differences are used to decide whether inference is rerun.

## Phase map

~~~text
routing-semantic-v1             CLOSED / PUBLISHED

routing-semantic-v2
  study/protocol draft          COMPLETE
  pass-v2 implementation        COMPLETE
  replication corpus            COMPLETE (draft identity)
  repository readiness review   COMPLETE
  live IA-9/10/11 preflight     NEXT
  authoring-view/module freeze  BLOCKED ON PREFLIGHT
  full IA-1..IA-11              BLOCKED
  real A/B/C                    BLOCKED

agentic-jev-pilot-v1
  three-arm design              COMPLETE
  skill/tool/task implementation COMPLETE
  runtime identity hardening    COMPLETE
  repository readiness review   COMPLETE
  runtime freeze                NEXT
  live tool qualification       NEXT
  analysis-contract freeze      BLOCKED ON QUALIFICATION
  24 × 3 pilot                  BLOCKED
~~~

## Claim boundary

The correct statement at this checkpoint is:

> Repository review is complete enough to begin live qualification.

It is not:

> v2 is qualified, or the agentic-Jev pilot is ready to run in full.

No new treatment outcome has been observed during these corrections.
