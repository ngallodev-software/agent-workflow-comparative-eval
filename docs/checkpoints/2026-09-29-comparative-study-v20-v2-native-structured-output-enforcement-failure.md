# Comparative Study v20 — Native structured-output enforcement failure

**Date:** 2026-09-29  
**Study:** `routing-semantic-v2`  
**Status:** qualification blocked; real oracle A/B/C remains prohibited

## Context

The preceding v19 checkpoint recorded the first live structured-output qualification failure: Inspect AI 0.3.268 could not preserve `const`, `minItems`, or `maxItems` through its bridge schema model. The benchmark-side capability-v2 work therefore changed the model-facing schema to the bridge-representable subset, added construction-time fail-closed validation, and retained unsupported cardinality requirements in deterministic post-generation validation.

This checkpoint records the next live failure observed after that change. It is additive evidence and does not rewrite v19.

## Observed behavior

A preserved synthetic qualification Inspect log reached a successful task/sample boundary:

- Inspect task status: `success`
- sample role: `C`
- sample error: none
- model identity reported by the sample: `deepseek-flash`
- terminal completion length: 1,373 characters
- terminal assistant message length: 1,373 characters
- the final model event exposed the same terminal completion

The terminal completion was **not empty**. It began with ordinary explanatory prose and then emitted a JSON object matching the intended adjudication shape.

The benchmark's strict whole-completion decoder rejected the result at the first character:

```text
Inspect adjudicator did not return a JSON object:
Expecting value: line 1 column 1 (char 0)
```

The raw private completion and Inspect log remain on the qualification host and are not committed here.

## Current-path refinement

A subsequent read-only diagnostic of the active failed qualification attempt
narrowed the failure to the tiebreaker path:

- primary A completed successfully with a JSON-object-only terminal completion;
- primary B completed successfully with a JSON-object-only terminal completion;
- C completed successfully at the Inspect sample level but returned explanatory
  prose followed by the JSON object;
- no qualification manifest was produced.

The same benchmark helper constructs both primary and C through
`_inspect_eval(..., output_schema=...)`. The benchmark source therefore does
not show a separate C path that simply omits `output_schema`. The remaining
structured-output difference is the schema generated from the assigned view:
primary uses the two-case synthetic qualification view, while C uses the
dispute-only view.

The active Inspect logs did not expose a persisted raw provider request through
the current `ModelEvent.call.request` surface, so this refinement still does
not prove whether the final C request reached the provider with the intended
`text.format` control. That attribution remains open.

## Interpretation

This is a distinct integration failure from v19.

The earlier failure occurred before a sample completed because an unsupported schema keyword was silently dropped and the provider rejected the malformed transported schema.

This attempt progressed farther:

1. the model-facing schema passed the new representability boundary;
2. Inspect/Codex execution completed a synthetic sample;
3. a terminal answer was captured;
4. the terminal answer violated the required JSON-only structured-output boundary by prefixing free-form prose before the JSON object.

The presence of an apparently usable JSON suffix does **not** make the qualification valid.

## Why the benchmark must not extract the embedded object

A permissive recovery such as locating the first `{` and decoding the trailing object would weaken the study contract.

The v2 qualification is testing whether the native Codex/Inspect structured-output path enforces the requested final-output schema. Accepting prose-plus-JSON would turn an enforcement failure into an apparent success and would make the qualification unable to distinguish:

- native structured output that is actually enforced; from
- ordinary unconstrained text that merely happens to contain parseable JSON.

Therefore the existing strict whole-completion parser remains the correct gate for this qualification.

## Current fault boundary

The preserved evidence establishes the symptom but does not yet identify which layer failed to preserve or enforce the output-format request.

Candidate boundaries include:

- Codex CLI construction/forwarding of `--output-schema`;
- Inspect-SWE / Inspect agent-bridge translation;
- the OpenAI-compatible provider request emitted by Inspect;
- `codex-lb` request forwarding/model-source adaptation;
- DeepSeek Responses structured-output enforcement.

The next diagnostic must inspect the actual model API request, not infer from the final text.

## Required next diagnostic

Perform one archived qualification retry with Inspect model-API logging enabled while preserving the current failed attempt.

For the final model call, verify whether the outbound request actually contains the expected structured-output control and schema. In particular, capture enough private evidence to answer:

1. Was a `json_schema` output format sent on the final request?
2. Did the expected schema arrive intact?
3. Was any strict/enforcement flag present at the provider-facing boundary?
4. Did `codex-lb` forward or transform that control?
5. Did the provider return unconstrained prose despite receiving the schema?

Do not change the parser or weaken any qualification gate before that evidence is inspected.

## Study boundary

No real `routing-semantic-v2` oracle A/B/C cohort may start from this attempt. A passing IA-1 through IA-11 qualification remains mandatory.

If the next retry exposes another integration failure, preserve it as another additive checkpoint. If it passes, retain this failed attempt as evidence that the integration required hardening before the real study began.
