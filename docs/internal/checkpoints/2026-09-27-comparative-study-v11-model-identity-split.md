# Comparative Evaluation — Model Identity Split Frozen Before Live Qualification

**Date:** 2026-09-27  
**Checkpoint:** `comparative-study-v11`  
**Relationship to v10:** additive pre-live experimental-design decision; v10 remains the record of repository readiness before the coding-agent model was selected.

## Decision

The two active studies now deliberately use different model identities because they answer different questions.

### routing-semantic-v2

Keep the v1-matched adjudicator path:

- model: `deepseek-flash`;
- provider path: `openai-api/codex-lb/deepseek-flash`;
- request mode: Responses API via `{"responses_api": true}`;
- no new reasoning-effort override.

Reason: this study is a methodological replication. The intended change is the rationale/provenance evidence contract, not the adjudicator model.

### agentic-jev-pilot-v1

Freeze the new coding-agent pilot on:

- model: `gpt-6-luna`;
- provider path: `openai-api/codex-lb/gpt-6-luna`;
- reasoning effort: `high`;
- request mode: Responses API;
- Codex internal model configuration: `gpt-6-luna`;
- minimum Codex CLI version: `0.155.0`.

Every A/B/C arm uses that exact coding-agent identity.

The only arm differences remain:

~~~text
A: Luna
B: Luna + frozen TypeSafe skill
C: Luna + frozen TypeSafe skill + live Jev
~~~

## Why the studies split here

Using Luna for routing-semantic-v2 would confound the v2 methodological repair with an adjudicator-model change.

Using DeepSeek merely for symmetry in the agent-directed pilot would impose a historical constraint on a new exploratory question whose instrument must:

- understand the TypeSafe skill;
- decide whether a semantic tool is useful;
- construct a bounded typed Jev request;
- interpret the result;
- integrate the result into subsequent coding-agent behavior.

The pilot is therefore allowed to choose its coding agent before the first live runtime lock/outcome, provided the choice is then frozen identically across all arms.

## Interface verification

The model selection was checked through the actual stack rather than guessed from environment-variable names.

### Inspect AI

Inspect separates:

- `model_args` — provider/model construction arguments;
- `reasoning_effort` — generation configuration.

Therefore `high` reasoning is supplied to `inspect_ai.eval(..., reasoning_effort="high")`, not placed inside `model_args`.

### Inspect SWE / Codex

The pinned Inspect SWE `0.2.70` supports an explicit `model_config` for Codex prompt/tool alignment.

Its bundled fallback catalog predates GPT-6 Luna, so relying on implicit catalog derivation could alias Luna to an older/latest-known model profile.

The pilot therefore explicitly passes:

`model_config="gpt-6-luna"`

and refuses a resolved Codex CLI below `0.155.0`, the current Codex model catalog's minimum client version for GPT-6 Luna.

### codex-lb

The Responses path carries reasoning effort using the Responses `reasoning.effort` contract.

The benchmark keeps `{"responses_api": true}` as the provider-construction argument and leaves reasoning effort in Inspect generation configuration, avoiding two competing representations.

## Benchmark implementation

### PR #58 — Luna/high pilot identity

Merge:

`b1eb04494ec08db83b41652577777658bcf8f3e1`

The agentic-Jev runtime lock now fails closed unless:

- model is exactly `openai-api/codex-lb/gpt-6-luna`;
- reasoning effort is exactly `high`;
- `responses_api` is exactly true;
- no reasoning override appears in `model_args`;
- Codex model config is `gpt-6-luna`;
- resolved Codex CLI is at least `0.155.0`.

Qualification and all three pilot arms receive the frozen `reasoning_effort` through Inspect.

All benchmark test/import checks passed before merge.

### PR #59 — DeepSeek v2 replication identity

Merge:

`00c2406b2c9bed9ef8fd2464bdcaa975630a0d7e`

The routing-semantic-v2 evidence preflight now fails closed unless:

- model is exactly `openai-api/codex-lb/deepseek-flash`;
- model args are exactly `{"responses_api": true}`.

The preflight artifact records both fields and its schema requires them.

All benchmark test/import checks passed before merge.

## Version changes

Because the coding-agent model is result-affecting even though no live pilot outcome exists yet:

- `agentic-jev-pilot-v1`: `0.1.0-draft.1` -> `0.1.0-draft.2`.

Because v2 now makes the previously intended adjudicator continuity explicit:

- `routing-semantic-v2`: `2.0.0-draft.1` -> `2.0.0-draft.2`.

The v2 corpus identity remains `routing-semantic-corpus-v2.0.0-draft.1` because no case content changed.

## Historical boundary

No live IA-9/10/11 preflight had run when this decision was made.

No agentic-Jev runtime lock, live tool qualification, or 24 × 3 outcome existed.

Therefore:

- no observed result was discarded;
- no frozen cohort was rewritten;
- no model was selected after seeing pilot outcomes;
- v1 remains immutable;
- v10 remains a valid historical checkpoint.

## Updated phase map

~~~text
routing-semantic-v1
  CLOSED / PUBLISHED

routing-semantic-v2 2.0.0-draft.2
  evidence-contract implementation   COMPLETE
  replication corpus                 COMPLETE (draft identity unchanged)
  adjudicator identity: DeepSeek     FROZEN IN CODE/STUDY
  live IA-9/10/11 preflight          NEXT
  real authoring/module/runtime       BLOCKED ON PREFLIGHT
  full IA-1..IA-11                    BLOCKED
  real A/B/C                          BLOCKED

agentic-jev-pilot-v1 0.1.0-draft.2
  three-arm design                    COMPLETE
  coding-agent: GPT-6 Luna / high     FROZEN IN CODE/STUDY
  skill/tool/tasks                     COMPLETE
  runtime identity hardening           COMPLETE
  runtime freeze                       NEXT
  live exactly-once Jev qualification  NEXT
  task-level analysis contract         BLOCKED ON QUALIFICATION
  24 × 3 pilot                         BLOCKED
~~~

## Immediate next step

The next work remains empirical qualification, not further model selection.

Track A:

~~~bash
export V2_ADJUDICATION_MODEL='openai-api/codex-lb/deepseek-flash'
export V2_ADJUDICATION_MODEL_ARGS_JSON='{"responses_api":true}'
bash scripts/adjudication/v2-evidence-preflight.sh
~~~

Expected:

~~~text
IA-9 pass
IA-10 pass
IA-11 pass
real_cohort_ready: false
~~~

Track B:

~~~bash
export AGENTIC_JEV_MODEL='openai-api/codex-lb/gpt-6-luna'
export AGENTIC_JEV_REASONING_EFFORT='high'
export AGENTIC_JEV_MODEL_ARGS_JSON='{"responses_api":true}'

bash scripts/agentic-jev/p0-freeze-runtime.sh
bash scripts/agentic-jev/p0-qualify-tool.sh
~~~

Do not run the 24 × 3 pilot until the generated runtime-lock/qualification artifacts are reviewed and the task-level analysis contract is frozen.
