# Comparative Study v21 — Full v2 qualification passes with sanitized ingress proof

**Date:** 2026-09-29  
**Study:** `routing-semantic-v2`  
**Status:** full live qualification passed; real oracle A/B/C may proceed under the frozen v2 contract

## Context

v19 preserved the lossy Inspect schema-bridge failure. v20 preserved the later C-path
failure where a successful synthetic tiebreaker returned explanatory prose before
its JSON object and the strict whole-completion parser rejected it.

Neither prior checkpoint is superseded or rewritten by this result.

This checkpoint records the first full live `routing-semantic-v2` qualification
that passed the strengthened structured-output path end to end.

## Passing qualification

Private-host attempt identity:

- attempt id: `20260929T171720Z`
- adjudicator: `openai-api/codex-lb/deepseek-flash`
- Inspect model-API raw logging: disabled
- sanitized Codex-LB ingress capture: enabled
- qualification manifest: present
- `qualified: true`
- IA-1 through IA-11: all `pass`

The frozen runtime lock was reused. No parser relaxation, embedded-object
extraction, schema rewriting, or qualification-gate bypass was introduced.

The successful current qualification produced JSON-object-only terminal
completions for:

- primary A;
- primary B;
- qualification C;
- evidence-preflight A;
- evidence-preflight B;
- evidence-preflight C.

## Structured-output transport proof

A loopback-only diagnostic proxy sat between the Inspect/OpenAI-compatible client
and the already-running local Codex-LB. It forwarded request bodies unchanged and
persisted only bounded transport metadata:

- request method and path;
- model id;
- `text.format` type/name/description/strict flag;
- canonical SHA-256 of the supplied JSON Schema.

It did not retain prompts, input/messages, tool arguments, header values, model
responses, or full schemas.

The capture observed **15 POST requests to `/v1/responses`**. Every captured
structured-output request carried:

- `text.format.type = json_schema`;
- `text.format.strict = true`;
- the expected `codex_output_schema` name/description;
- a schema hash matching one of the persisted model-facing schema artifacts.

Observed schema identities:

- primary schema:
  `edba8028555970ce4157f2b57cf91abf4bd605fcef405273c85007ff49f5725f`;
- qualification C schema:
  `0dad21672253a7e1db64022249930bce62b4e72c013b39663e43fbcdffeb2f71`;
- evidence-preflight C schema:
  `a101279e200c1b809fbc56b47ee8f5cb7dca4ceec133326fa9114e9e0879164e`.

The persisted primary and C schemas contained zero empty schema nodes and zero
unsupported `const`, `minItems`, or `maxItems` constraints. Exact case
identity remained represented as `type: string` plus a one-value `enum`.

This establishes that the passing run carried the intended strict JSON-schema
controls through the benchmark/Inspect/Codex CLI boundary to Codex-LB ingress.

## What this does and does not establish about v20

The v20 prose-plus-JSON C failure remains genuine evidence. It is not deleted,
reclassified as operator error, or retroactively made passing.

The new capture proves that the current code/runtime can transport the strict
schema correctly and complete all qualification gates. It does **not** prove the
exact provider-facing request shape of the earlier failed attempt because that
attempt predates the sanitized ingress capture.

Given:

1. the earlier C sample completed but violated the JSON-only boundary;
2. the later retry used the strengthened same study contract and frozen runtime;
3. the passing retry delivered the exact C schema with `strict=true` to
   Codex-LB ingress; and
4. C then returned JSON-only,

the earlier failure is consistent with an intermittent structured-output
enforcement failure somewhere downstream of benchmark schema construction.
The historical evidence is insufficient to assign that earlier failure to a
specific downstream component.

The benchmark therefore keeps the strict whole-completion parser as the
fail-closed detector. A recurrence during real A/B/C must fail rather than
salvage an embedded object.

## Benchmark integration disposition

Agent-Workflow Benchmark PR #71 was held in draft until this private live
qualification succeeded.

After this pass:

- PR #71 CI was green;
- the PR was marked ready;
- PR #71 merged as
  `9ef7f055b3475929ea95d3b2c7509b457c6299df`;
- the durable diagnostic tooling remains opt-in and private-evidence oriented.

## Study boundary after v21

The full frozen IA-1 through IA-11 qualification requirement is now satisfied.

The real `routing-semantic-v2` A/B/C cohort is no longer blocked by
qualification. It may proceed under the frozen v2 study/module/runtime identities.

The following requirements remain unchanged during the real cohort:

- keep A and B independent;
- reveal A/B only after both primary passes complete;
- create C only from the blinded dispute view;
- preserve structured justifications and scoped provenance;
- keep strict JSON-only parsing;
- fail closed on any structured-output or contract-validation violation;
- preserve failed attempts rather than rewriting them into successful evidence.
