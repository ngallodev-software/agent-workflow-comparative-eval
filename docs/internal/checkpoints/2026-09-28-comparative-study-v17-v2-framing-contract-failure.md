# Comparative Evaluation — v2 Framing-Contract Failure and Structured-Output Requirement

**Date:** 2026-09-28  
**Checkpoint:** `comparative-study-v17`  
**Relationship to v16:** additive live-qualification evidence. v16 records the study-identity plumbing defect and benchmark 0.6.1 correction. This checkpoint records the next corrected run reaching IA-9 and failing the final-output framing contract.

## Observed live failure

After updating to benchmark `0.6.1`, the full `routing-semantic-v2` qualification reused the existing frozen runtime lock and progressed into the v2 IA-9/10/11 evidence preflight.

Adjudicator A then failed before pass wrapping with:

~~~text
routing-semantic-v2 preflight adjudication contract invalid;
adjudicator=preflight-a;
error=Inspect adjudicator did not return a JSON object:
Expecting value: line 1 column 1 (char 0)
~~~

The diagnostic identified:

- adjudicator: `preflight-a`;
- completion source: `model_output.completion`;
- parsed completion: absent;
- raw completion: durably preserved under the private qualification evidence root.

No real A/B/C cohort adjudication began.

## What the preserved completion showed

The raw completion was not empty and was not the wrong terminal message.

It contained:

1. one prose sentence announcing that the files had been read and adjudications were being emitted;
2. immediately afterward, a complete JSON object with a `records` array.

The JSON body contained both synthetic v2 cases and, for each case:

- all three required routing seams;
- labels in the expected domains;
- a structured justification for every assigned seam;
- `decisive_case_evidence` as arrays rather than scalar strings;
- bounded `rubric_rule` strings;
- allowed `ambiguity` values.

The observed failure is therefore specifically a **transport/framing contract failure**:

> the authoritative completion did not consist exclusively of the required JSON object.

This distinction matters. The adjudicator appears to have satisfied the semantic decision-evidence shape while violating the machine framing requirement.

## Why the benchmark remains correct to fail closed

The v2 prompt already requires:

~~~text
Return JSON only. Do not include markdown fences or additional fields.
~~~

The benchmark parser intentionally attempts to parse the entire authoritative completion as JSON.

It must remain strict.

Do **not** fix this class of failure by:

- stripping leading prose;
- locating the first `{` and parsing a substring;
- accepting fenced JSON plus commentary;
- repairing or normalizing model output after generation;
- retrying repeatedly until the model happens to emit a compliant frame and then ignoring the failed attempts.

Those approaches would move contract enforcement from generation into permissive post-processing and would erase exactly the interface failure qualification is intended to expose.

## Stronger architecture discovered

The preferred correction is to enforce the final result schema **at the generation boundary** and retain the current parser/semantic validators afterward as an independent second line of defense.

The desired chain becomes:

~~~text
frozen v2 authoring/dispute view
  -> exact model-output JSON Schema
  -> Codex final-output structured generation
  -> exact whole-completion JSON parse
  -> case/seam/label validation
  -> structured-justification validation
  -> provenance / IA evidence
~~~

This is strictly stronger than prompt-only JSON instructions.

## Capability investigation

The pinned runtime is:

- Inspect AI `0.3.268`;
- Inspect-SWE `0.2.70`;
- Codex CLI `0.158.0`.

Codex CLI natively supports:

~~~text
codex exec --output-schema <FILE>
~~~

for a JSON Schema describing the model's final response shape.

Inspect AI also has structured-output machinery through `GenerateConfig.response_schema`.

However, the actual v2 execution uses Inspect-SWE's `codex_cli()` agent wrapper. In Inspect-SWE `0.2.70`:

- `codex_cli()` constructs the Codex command internally;
- it exposes configuration overrides but no final-output-schema argument;
- it invokes an absolute resolved Codex binary path;
- therefore a PATH/binary shim cannot cleanly inject `--output-schema`;
- simply passing Inspect-level `response_schema` does not cause Codex CLI to request structured final output.

Inspection of current Inspect-SWE `main` shows that this final-output-schema seam is still not exposed.

The clean implementation boundary is therefore an Inspect-SWE Codex-wrapper capability such as:

~~~python
codex_cli(..., output_schema=<json schema or path>)
~~~

which deterministically writes/locates the schema in the sandbox and appends the native Codex `--output-schema` argument.

## Durable implementation tracker

The stronger requirement is now tracked in:

**agent-workflow-benchmark issue #69 — “Enforce v2 adjudicator final output with Codex --output-schema”**

Acceptance criteria include:

- exact A/B schema generation from the assigned authoring view;
- dispute-specific C schema generation;
- native Codex `--output-schema` enforcement;
- runtime-lock evidence that structured-output enforcement is enabled;
- schema hash recorded in qualification evidence;
- existing strict whole-completion parser retained unchanged;
- regression proving prose-prefixed JSON is still rejected;
- no permissive JSON extraction fallback;
- no real v2 cohort until the strengthened runtime is frozen and qualified.

## Current qualification disposition

The current full qualification attempt is a real failed attempt and should remain preserved.

Do not overwrite it in place.

The correct next methodological sequence is:

1. retain the current failure evidence unchanged;
2. implement or obtain the Inspect-SWE/Codex final-output-schema seam;
3. integrate exact v2 schema generation in benchmark;
4. update the runtime/module identity as required;
5. freeze a new runtime lock if the executable runtime changes;
6. rerun complete IA-1 through IA-11 qualification;
7. inspect the resulting qualification artifact;
8. only then authorize real A/B/C.

A simple prompt-only retry is not equivalent to this stronger correction.

## Phase map

~~~text
routing-semantic-v2 2.0.0
  frozen study/dataset/protocol      COMPLETE
  frozen blinded authoring view      COMPLETE
  v2 module pair                     COMPLETE
  runtime lock                       FROZEN
  study-ID plumbing defect           FOUND / FIXED
  final-output framing failure       FOUND
  provider/Codex schema enforcement  REQUIRED / TRACKED AS BENCHMARK #69
  full IA-1..IA-11 qualification     NOT PASSED
  real A/B/C                         BLOCKED
~~~

## Claim boundary

Safe claim:

> The corrected full v2 qualification reached the structured-evidence stage and exposed a final-output framing failure: the adjudicator returned a semantically complete JSON body preceded by prose. The benchmark correctly failed closed. The stronger correction is generation-time schema enforcement through Codex final-output structured output, not permissive parsing.

Not safe:

> IA-9 passed after ignoring the preamble.

Not safe:

> The real v2 cohort is qualified.

Both remain false at this checkpoint.
