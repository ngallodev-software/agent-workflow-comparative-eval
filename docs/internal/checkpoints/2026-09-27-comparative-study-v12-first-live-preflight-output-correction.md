# Comparative Evaluation — First Live v2 Preflight Exposes Agent Terminal-Output Contract Gap

**Date:** 2026-09-27  
**Checkpoint:** `comparative-study-v12`  
**Relationship to v11:** additive live-qualification correction; v11 remains the pre-live model-identity freeze.

## What happened

The first live `routing-semantic-v2` IA-9/10/11 evidence-preflight attempt reached the C tiebreaker stage and failed while decoding the adjudicator result.

Observed execution state:

- the A and B samples completed and were decoded into v2 adjudication contracts;
- the synthetic A/B disagreement and blinded C dispute view were created;
- the C Inspect sample completed without an Inspect sample error;
- the harness read `c_result.output.completion`;
- that field was empty/non-JSON for this agent-backed run;
- `_json_completion` therefore raised before C could be wrapped and before an IA-9/10/11 preflight artifact could be completed.

The failure was an execution-contract defect in the benchmark harness, not an oracle-label result.

## Root cause

The shared adjudication runner assumed the adjudication answer must always be available in:

`EvalSample.output.completion`

That assumption is valid for the historical v1 path and had worked for earlier samples, but it is too narrow for an Inspect agent-backed execution.

An agent run can expose its terminal generated assistant text in the sample message transcript while `ModelOutput.completion` is empty.

The v2 runner therefore needed an explicit terminal-agent-output extraction contract.

## Correction

Benchmark PR #60 merged as:

`37b1e9670bef79f648f0939e4f55fca2b3b6294b`

The corrected extraction rule is version-aware.

### routing-semantic-v1

No behavior change.

V1 continues to read only:

`ModelOutput.completion`

and its historical provenance shape remains unchanged.

### routing-semantic-v2 and newer studies

The runner now:

1. prefers a non-empty `ModelOutput.completion`;
2. if that field is empty, inspects the terminal generated assistant message;
3. accepts only the last generated assistant message;
4. refuses to reuse an earlier assistant message when the terminal assistant is still making a tool call or has no terminal text.

The source is now recorded as one of:

- `model_output.completion`;
- `messages.terminal_assistant`.

The v2 preflight artifact requires an A/B/C `completion_sources` map.

V2 Inspect provenance likewise records the adjudication completion source.

## Retry-evidence correction

The first failed attempt left a partially populated generated preflight directory.

Previously, `FORCE_V2_PREFLIGHT=1` permitted reuse of that populated directory. That could mix old Inspect logs with retry artifacts.

PR #60 also changes the forced-retry path so the generated v2 preflight subdirectory is deleted and recreated before execution.

This preserves a clean evidence boundary between the failed first attempt and the retry.

## Regression coverage

The benchmark regression suite now verifies:

- v2 fallback to the terminal generated assistant message when `output.completion` is empty;
- non-empty `output.completion` remains authoritative;
- a pre-tool assistant message is never reused as a terminal answer;
- v1 keeps its historical output-only extraction behavior;
- forced v2 retry recreates a clean generated preflight root.

All benchmark `test`, `agentic-jev-import`, and `inspect-import` jobs passed on both CI trigger paths before merge.

## Interpretation boundary

No IA-9/10/11 result should be inferred from the failed attempt.

It established only that:

- the real DeepSeek/codex-lb/Inspect path progressed through A/B and into C;
- the v2 terminal-output extraction assumption was incomplete;
- the preflight must be rerun after the correction.

It did **not** produce a valid completed preflight artifact and therefore did not authorize the real v2 cohort.

No case content, rubric, adjudication label, treatment inference, provider model identity, or frozen v1 evidence was changed.

## Aha

> In an agent harness, the model response object and the agent's terminal answer are related evidence surfaces, not necessarily the same storage field.

A reproducible evaluation must specify which terminal surface is authoritative and record which one was used.

## Updated phase map

~~~text
routing-semantic-v2 2.0.0-draft.2
  model identity                    FROZEN: DeepSeek Flash
  evidence-contract implementation COMPLETE
  first live IA-9/10/11 attempt     FAILED: terminal-output extraction contract
  extraction correction             MERGED: benchmark 37b1e967...
  clean retry                        NEXT
  real authoring/module/runtime      BLOCKED ON PREFLIGHT
  full IA-1..IA-11                  BLOCKED
  real A/B/C                         BLOCKED

agentic-jev-pilot-v1 0.1.0-draft.2
  unchanged by this correction
  Luna/high runtime freeze           NEXT
  one-call Jev qualification         NEXT
  24 x 3 pilot                       BLOCKED
~~~

## Immediate next action

Update the benchmark host to merge `37b1e9670bef79f648f0939e4f55fca2b3b6294b` or later, then rerun the v2 preflight with the force flag so the failed generated evidence directory is cleaned first.

Expected success boundary remains:

~~~text
IA-9 pass
IA-10 pass
IA-11 pass
real_cohort_ready: false
~~~

A passing synthetic preflight still does not authorize real v2 adjudication.
