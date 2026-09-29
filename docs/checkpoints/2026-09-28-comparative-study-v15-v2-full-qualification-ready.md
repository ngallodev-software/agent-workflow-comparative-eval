# Comparative Evaluation — v2 Full Qualification Tooling Frozen and Released

**Date:** 2026-09-28  
**Checkpoint:** `comparative-study-v15`  
**Relationship to v14:** additive pre-adjudication implementation milestone. v14 remains the record of the first complete live IA-9/10/11 synthetic evidence pass and the decision to freeze real-cohort identities.

## Current boundary

The `routing-semantic-v2` real-cohort identities and full qualification tooling are now frozen and released across the coordinated stack.

No real 120-case v2 oracle labels have been generated.

The next live action is the complete IA-1 through IA-11 qualification against the frozen v2 module and a newly frozen runtime lock. Real A/B/C adjudication remains blocked until that qualification completes and its artifacts are inspected.

## Frozen comparative-eval identities

The pre-adjudication freeze promoted the v2 draft identities to:

- study: `routing-semantic-v2` / `2.0.0`;
- dataset: `routing-semantic-corpus-v2.0.0`;
- oracle protocol: `routing-semantic-oracle-v2.0.0`.

The canonical blinded authoring view is:

`docs/studies/artifacts/routing-semantic-v2/oracle-authoring-view.json`

Frozen SHA-256 identities:

- authoring view: `88a18b5e1a1132a25da41bee5fabbeeaa8a687be395fc28bd39c0b4d6a9a2617`;
- oracle protocol: `ff165c964fd032e95160ff760a0f46e661e88d41fd22a376f9b0767e24ba793e`;
- corpus: `99f113ce05c2921a45534e3e7cf17f410379589208cf95415a57c47caff61236`.

The 120 case meanings remain the methodological replication of v1. Construction tags, control/candidate outputs, and oracle labels are excluded from the authoring view.

## Coordinated releases

### comparative-eval 0.3.1

Merge:

`32ae2a9ad2e63a15c662b9f7bbab581583ab2b32`

The patch release gives the frozen v2 study/corpus resources a distinct package identity from the earlier 0.3.0 draft-resource build.

### benchmark 0.6.0

Merge:

`49c2f974eb51caf54d4169396e16d60f682cab6c`

The benchmark now contains the complete post-preflight v2 qualification path:

- frozen direct-Docker and Inspect v2 module definitions;
- IA-1 through IA-8 executed against the v2 pass-v2 contract;
- IA-9 through IA-11 rerun under the same final frozen runtime identity rather than inherited from the earlier draft preflight;
- `inspect-adjudication-qualification/v2` output;
- `scripts/adjudication/v2-qualify.sh` as the bounded operator entry point;
- archived retry handling that preserves prior evidence;
- direct-Docker v2 preparation/execution support so IA-5 parity is against an executable reference path rather than declarative metadata only.

Benchmark CI passed the test/build, Inspect import/guardrail, and agentic-Jev import lanes before merge.

### SpecGen 0.2.12

Merge:

`d330d41d7adab89e81fb0b0fb48ee8d4f352a8fd`

This is a compatibility-only release targeting Agent-Workflow 0.11.12. It adds an explicit 0.11.12 public-contract compatibility fixture/snapshot and does not introduce new SpecGen authoring semantics.

Its CI installed SpecGen and the exact Agent-Workflow 0.11.12 candidate together, verified release metadata, ran critical seams and pytest, and built the wheel successfully.

### Agent-Workflow 0.11.12

Merge:

`52d6bdf5f28443421582f21782b302cf347d3b75`

The full-stack installer now freezes:

- spec-contracts `0.2.1`;
- Agent-Workflow `0.11.12`;
- comparative-eval `0.3.1`;
- SpecGen `0.2.12`;
- benchmark `0.6.0`;
- TypeSafe SDK `0.6.0`.

The final Agent-Workflow CI matrix passed Linux Python 3.11/3.12/3.13, macOS, and Windows before merge.

## Why the full qualifier reruns IA-9 through IA-11

The successful preflight in v14 authorized the freeze step, but it was a synthetic evidence-contract preflight and deliberately reported:

~~~text
real_cohort_ready: False
~~~

The full qualifier does not convert that prior artifact into final qualification evidence.

Instead, after creating/reusing the frozen v2 runtime lock, it reruns the synthetic v2 evidence checks under the same final module/runtime/model identity used by the IA-1 through IA-8 qualification path. This ensures one qualification artifact binds all eleven gates to the final cohort configuration.

## Next live command

After updating/installing the coordinated stack, run:

~~~bash
cd /lump/apps/agent-workflow-benchmark

export CODEX_LB_BASE_URL='http://127.0.0.1:2455/v1'
export CODEX_LB_API_KEY='inspect-placeholder'
export V2_ADJUDICATION_MODEL='openai-api/codex-lb/deepseek-flash'

bash scripts/adjudication/v2-qualify.sh
~~~

Expected success boundary:

~~~text
routing-semantic-v2 full qualification: PASS
IA-1 pass
IA-2 pass
IA-3 pass
IA-4 pass
IA-5 pass
IA-6 pass
IA-7 pass
IA-8 pass
IA-9 pass
IA-10 pass
IA-11 pass
qualified: True
runtime_lock: ...
qualification: ...
~~~

A passing result is still a review boundary, not an instruction to immediately run real A/B/C. Inspect the runtime lock and qualification artifact first.

## Phase map

~~~text
routing-semantic-v2 2.0.0
  IA-9/10/11 evidence preflight    PASS
  study/dataset/protocol freeze    COMPLETE
  canonical blinded authoring view COMPLETE
  comparative-eval package         0.3.1 / RELEASED
  v2 direct + Inspect modules       COMPLETE
  benchmark qualifier               0.6.0 / RELEASED
  coordinated Agent-Workflow stack 0.11.12 / RELEASED
  full IA-1..IA-11 live run         NEXT
  qualification artifact review     BLOCKED ON LIVE RUN
  real A/B/C                         BLOCKED

routing-semantic-v1
  CLOSED / PUBLISHED / IMMUTABLE
~~~

## Claim boundary

The safe statement at this checkpoint is:

> The frozen routing-semantic-v2 cohort configuration and complete IA-1 through IA-11 qualification tooling are released and ready for the bounded live qualification run.

It is not yet:

> The real v2 cohort is fully qualified, or real v2 oracle adjudication has begun.
