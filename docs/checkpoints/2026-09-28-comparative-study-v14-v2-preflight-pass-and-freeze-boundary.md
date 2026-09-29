# Comparative Evaluation — v2 Synthetic Evidence Pass and Real-Cohort Freeze Boundary

**Date:** 2026-09-28  
**Checkpoint:** `comparative-study-v14`  
**Relationship to v13:** additive live-qualification milestone. Earlier failed attempts remain historical evidence and are not rewritten by this pass.

## Successful live evidence preflight

A clean DeepSeek-backed `routing-semantic-v2` synthetic evidence preflight completed with:

~~~text
routing-semantic-v2 evidence preflight: PASS
IA-9 pass
IA-10 pass
IA-11 pass
real_cohort_ready: False
~~~

The passing private artifact was written at:

~~~text
$XDG_DATA_HOME/agent-workflow/routing-semantic-v2-preflight/preflight.json
~~~

The explicit `real_cohort_ready: False` result is expected and required. The synthetic pass proves the v2-only evidence path; it does not itself authorize the 120-case oracle cohort.

## What the pass establishes

The live path now demonstrates, synthetically and against the frozen DeepSeek adjudicator identity:

- required structured justifications survive model output, wrapping, schema validation, dispute construction, C execution, and human-resolution rendering;
- A/B labels and justifications remain absent from C's blinded dispute input;
- final-output usage and aggregate-session usage remain distinct;
- logical model-call and provider-request counts are recoverable from typed Inspect model events;
- optional reasoning-summary capture remains observational rather than authoritative;
- the v2 adjudication model and model arguments remain fixed at `openai-api/codex-lb/deepseek-flash` with Responses API enabled.

## Live failures discovered before the pass

The passing run does not erase the preceding failures.

After v13, workstation qualification exposed three additional execution-boundary defects before the successful pass.

### Installed-package path assumptions

Two benchmark paths worked from a source checkout but failed from the installed wheel:

1. the v2 prompt template was resolved by walking upward from `__file__`;
2. the human-resolution renderer was likewise resolved as a repository shell-script path.

These were packaging defects rather than adjudication outcomes.

Benchmark releases corrected them by packaging the prompt and moving resolution rendering into the Python package while retaining the operator shell wrapper.

### Structured-rationale contract failure

A later live run reached the v2 evidence contract and failed IA-9 because one adjudicator emitted an invalid `decisive_case_evidence` value for:

~~~text
rsv2-preflight-002:routing.task_class
~~~

The validator rejected the result because the preregistered contract requires 1-3 strings, each at most 320 characters.

This was a genuine qualification observation, not a harness-path failure.

The contract was not weakened and the malformed model output was not repaired after the fact. Benchmark `0.5.4` instead:

- made the JSON-array requirement explicit in the shared v2 prompt;
- preserved the same 1-3 item and 320-character bounds;
- persisted raw and parsed completion diagnostics before failing;
- retained fail-closed IA-9 validation.

The subsequent clean run passed IA-9/10/11.

## Real-cohort freeze initiated only after the pass

Because no real v2 labels existed yet, this checkpoint is the correct result-affecting freeze boundary.

The registered draft identities are promoted to their real-cohort identities without changing case semantics:

- study: `routing-semantic-v2`, version `2.0.0`;
- dataset: `routing-semantic-corpus-v2.0.0`;
- oracle protocol: `routing-semantic-oracle-v2.0.0`.

The exact 120-case content remains the methodological replication of v1.

A canonical blinded authoring view is now generated from the registered v2 corpus and frozen under:

~~~text
docs/studies/artifacts/routing-semantic-v2/oracle-authoring-view.json
~~~

Its manifest records the corpus, study, protocol, and authoring-view hashes. Construction tags, treatment/control outputs, and oracle labels remain absent.

## Remaining gate

The real cohort is still blocked.

The existing benchmark live qualifier is historically v1-specific: its execution path currently builds the v1 synthetic view, validates the v1 pass schema, compares against the v1 direct module, and records IA-1 through IA-8.

The next implementation step is therefore:

1. create the frozen v2 direct and Inspect adjudication module pair against the new authoring-view/corpus/protocol hashes;
2. freeze a v2 runtime lock;
3. extend the live qualification path so the v2 qualification artifact contains IA-1 through IA-11;
4. bind IA-9/10/11 to the passing v2 evidence preflight;
5. run and inspect that complete qualification;
6. only then authorize real A/B/C.

No real v2 oracle label has been produced at this checkpoint.

## Updated phase map

~~~text
routing-semantic-v2 2.0.0
  synthetic IA-9/10/11          PASS
  dataset/protocol/study freeze IN PROGRESS
  canonical authoring view      FROZEN ON PRE-ADJUDICATION BRANCH
  v2 module pair                NEXT
  v2 runtime lock               BLOCKED ON MODULE
  full IA-1..IA-11              BLOCKED ON MODULE/QUALIFIER
  real A/B/C                    BLOCKED

routing-semantic-v1
  CLOSED / PUBLISHED / IMMUTABLE
~~~

## Interpretation boundary

The safe statement is:

> The v2 evidence contract has passed live synthetic qualification, and the real-cohort identity freeze can now proceed.

It is not yet:

> The real v2 oracle cohort is qualified or running.
