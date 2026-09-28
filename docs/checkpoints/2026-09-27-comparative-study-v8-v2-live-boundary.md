# Comparative Evaluation — v2 Implementation Ready for Live Preflight

**Date:** 2026-09-27  
**Checkpoint:** `comparative-study-v8`  
**Relationship to v1:** v1 remains complete, immutable, and publicly published.

## Current state

The next evaluation cycle is now split into two deliberately separate tracks:

~~~text
Track A — routing-semantic-v2
repair adjudication/evidence mechanics
        ↓
reuse exact v1 case meanings under a new dataset identity
        ↓
measure oracle stability before deciding whether candidate/control must be rerun

Track B — agentic-jev-pilot-v1
keep the existing Inspect / Inspect-SWE Codex harness
        ↓
compare baseline vs TypeSafe-skill-only vs skill+live-Jev
        ↓
observe where Codex elects to invoke Jev
        ↓
use pilot evidence to decide what a later full task-outcome study should freeze
~~~

These tracks answer different questions and must not be collapsed into one experiment.

## Routing semantic v2 implementation

Comparative-eval now defines:

- study: `routing-semantic-v2`;
- study version: `2.0.0-draft.1`;
- protocol: `routing-semantic-oracle-v2-draft.1`;
- new pass contract: `agent-workflow-benchmark/decision-study-adjudication-pass/v2`;
- required structured justification for every eligible decision;
- explicit final-output and aggregate-session usage scopes;
- optional/private provider reasoning summaries that are not authoritative rationale.

The new v2 replication corpus is registered as:

`routing-semantic-corpus-v2.0.0-draft.1`

It contains the exact same 120 case meanings as the v1 corpus. The only intended corpus-level semantic difference is the new study/dataset identity. A regression test asserts this identity-only replication property.

Comparative-eval merge containing the v2 corpus:

`d6553f9442e3aa20a1c7c78dbcb7115d12b54b29`

## Benchmark implementation

Agent-Workflow Benchmark now contains the v2 pass/provenance mechanics and the agent-directed Jev pilot lane.

Primary benchmark merges:

- `87dec01d81e43cddc763378a9d08cf3bfd4654da` — v2 adjudication evidence + agent-directed Jev pilot;
- `cdbd3233511d1f3ffcc9922b275ce9f13d2321da` — codex-lb defaults carried into the new lanes.

CI passed for both PR heads.

### v2 evidence preflight

The synthetic v2 preflight exercises:

- **IA-9** — structured rationale round-trip;
- **IA-10** — final-output vs aggregate-session usage scope;
- **IA-11** — optional reasoning-summary observation.

It intentionally reports `real_cohort_ready: false` even when those gates pass.

That is correct. A passing IA-9/10/11 preflight proves the new evidence path works; it does not freeze the real v2 cohort.

### Agent-directed Jev pilot

The pilot uses three independent arms:

| Arm | Codex | Frozen TypeSafe skill | Live Jev tool |
| --- | --- | --- | --- |
| A-baseline | yes | no | no |
| B-skill-only | yes | yes | no |
| C-skill-plus-jev | yes | yes | yes |

The TypeSafe skill is frozen from:

- repository: `typesafe-ai/skills`;
- commit: `65a39f393687675ce170e6094757de20370365b9`;
- release: `v0.5.7`.

The live Jev tool is host-side and exposed to Codex through Inspect bridged tools/MCP. `TYPESAFE_API_KEY` remains on the host and is not injected into the sandbox.

The pilot task set contains **24 public-safe development tasks**. Private authoring tags identify plausible semantic-decision opportunities but are stripped before Codex sees each task.

The pilot is exploratory only. It cannot establish a coding-quality winner.

## Why the skill-only arm is required

A simple baseline vs skill+Jev comparison would confound two interventions:

1. TypeSafe decision-making instructions;
2. actual live Jev judgments.

The skill-only arm isolates those effects.

This is necessary before deciding whether Jev belongs:

- in the prompt/skill layer;
- as an optional callable tool;
- at runtime-enforced deterministic seams;
- or in a specialized future harness.

## Immediate live boundary

Repository implementation is ready for the next two live checks.

### 1. routing-semantic-v2 evidence preflight

Use the same adjudicator model as v1 initially to minimize a model-identity confound:

~~~bash
cd /lump/apps/agent-workflow-benchmark
git pull --ff-only

export V2_ADJUDICATION_MODEL='openai-api/codex-lb/deepseek-flash'
export V2_ADJUDICATION_MODEL_ARGS_JSON='{"responses_api":true}'

bash scripts/adjudication/v2-evidence-preflight.sh
~~~

Expected terminal state:

~~~text
IA-9 pass
IA-10 pass
IA-11 pass
real_cohort_ready: false
~~~

The `false` value is expected at this boundary.

### 2. agent-directed Jev runtime/tool qualification

For the development pilot, use one exact coding-model identity across all three arms. Using the already available DeepSeek path is acceptable for the first exploratory cohort:

~~~bash
export AGENTIC_JEV_MODEL='openai-api/codex-lb/deepseek-flash'
export AGENTIC_JEV_MODEL_ARGS_JSON='{"responses_api":true}'

bash scripts/agentic-jev/p0-freeze-runtime.sh
bash scripts/agentic-jev/p0-qualify-tool.sh
~~~

Do **not** run the 24 × 3 pilot until the tool qualification passes and its artifact is reviewed.

## What happens after the live checks

If the v2 evidence preflight passes:

1. generate the canonical v2 blinded authoring view from the registered v2 corpus;
2. freeze its SHA-256;
3. create the real v2 Inspect/direct module pair;
4. freeze a new runtime lock;
5. run complete IA-1 through IA-11 qualification;
6. only then run real A/B/C adjudication.

If the agent-directed Jev tool qualification passes:

1. inspect the frozen runtime lock and qualification;
2. run the 24 × 3 exploratory pilot;
3. analyze invocation frequency, primitive selection, failure/reliability, and where Jev changes subsequent agent behavior;
4. use those observations to define a later preregistered task-outcome study.

## Explicit non-goals

At this stage do not:

- modify the frozen v1 oracle;
- call the new v2 corpus an independent effectiveness replication;
- automatically rerun v1 candidate/control inference;
- claim the 24-task pilot measures coding quality;
- build a Jev-specialized coding harness before pilot evidence justifies one.

## Current phase map

~~~text
routing-semantic-v1             CLOSED / PUBLISHED

routing-semantic-v2
  study/protocol draft          COMPLETE
  pass-v2 implementation        COMPLETE
  IA-9/10/11 preflight code     COMPLETE
  v2 replication corpus         COMPLETE (draft identity)
  live IA-9/10/11 preflight     NEXT
  authoring-view freeze         BLOCKED ON PREFLIGHT
  full IA-1..IA-11              BLOCKED
  real A/B/C                    BLOCKED

agentic-jev-pilot-v1
  three-arm design              COMPLETE
  frozen skill snapshot         COMPLETE
  thin host-side Jev tool       COMPLETE
  24-task exploratory set       COMPLETE
  runtime freeze                NEXT
  live tool qualification       NEXT
  24 × 3 pilot                  BLOCKED ON QUALIFICATION
~~~
