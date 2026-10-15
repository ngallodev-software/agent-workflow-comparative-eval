# Comparative Evaluation — v2 Inspect Schema-Bridge Qualification Failure

**Date:** 2026-09-29  
**Checkpoint:** `comparative-study-v19`  
**Relationship to v18:** additive integration-evidence checkpoint. v18 remains the historical record of implementing native Codex final-output schema enforcement; this checkpoint records the first live failure exposed by that strengthened path.

## Boundary at this checkpoint

The `routing-semantic-v2` qualification reached the live synthetic A/B Inspect/Codex-LB/DeepSeek path under native Codex structured-output enforcement, but it did **not** produce a qualification manifest.

No oracle sample completed. The failed attempt therefore produced integration evidence only; it did not produce adjudication evidence that could contaminate the experimental cohort.

Real A/B/C remains blocked.

## Authoritative repository baselines inspected before the correction

Before changing the implementation, current remote HEADs were inspected:

- `ngallodev-software/agent-workflow-comparative-eval@54d4281b99aca1c883b8453a568b651b317f2b4a`;
- `ngallodev-software/agent-workflow-benchmark@4b48eaf23b35f2cb7eb6b6458f1cadbf2e99044c`;
- `meridianlabs-ai/inspect_swe@d5bb1abdf59cd5cfdb7217667e500df3e83ece92`.

The upstream Inspect-SWE Codex source at that HEAD still has Git blob:

`a5c5f21207d2fee496b8ef775c07757e2c524725`.

That is the exact source identity targeted by the existing downstream compatibility layer.

## Observed live failure

The live qualification run emitted an Inspect bridge warning before the provider failure:

```text
The bridged request's text.format.schema uses JSON Schema keywords Inspect
does not model (const, maxItems, minItems); they have been dropped, so the
model is constrained more weakly than the request asked.
```

The v2 model-facing schema contained a per-case discriminator equivalent to:

```json
{
  "case_id": {
    "const": "<case id>"
  }
}
```

Inspect AI `0.3.268` does not model `const`. Once the bridge dropped that keyword, the nested `case_id` schema became an empty schema object.

The downstream provider rejected the request with HTTP 400:

```text
Invalid schema for response_format 'codex_output_schema':
In context=('properties', 'records', 'items', 'anyOf', '0',
'properties', 'case_id'), schema must have a 'type' key.
```

The same warning identified `minItems` and `maxItems` as unsupported bridge constraints.

The task then stopped with zero completed samples.

## Evidence retention

The failed qualification attempt is preserved as methodological/integration evidence.

The raw runtime/provider log remains private under the project evidence policy. Its retained SHA-256 identity is:

`e17e3d6fef347a590f768f470f0991a116081a397220cdac079f39b952082435`

No raw provider request/response material is added to the public repository.

The absence of a `qualification.json` is itself part of the failure state; the qualifier did not advance far enough to seal a passing qualification artifact.

## Root cause

The original structured-output correction addressed the missing Inspect-SWE -> Codex CLI seam:

```text
codex_cli(output_schema=...)
  -> sandbox-local schema
  -> codex exec --output-schema <FILE>
```

That transport was necessary but not sufficient.

The active Inspect AI Responses bridge parses the Codex request through `inspect_ai.util._json.JSONSchema`. In the pinned `0.3.268` runtime, that model represents:

- `type`;
- `format`;
- `description`;
- `default`;
- `enum`;
- `items`;
- `properties`;
- `additionalProperties`;
- `anyOf`;
- `required`;
- `pattern`;
- `minLength`;
- `maxLength`;
- `minimum`;
- `maximum`;
- `examples`.

It does not represent `const`, `minItems`, or `maxItems`.

Inspect AI's bridge deliberately diagnoses unmodelled schema constraints but currently drops them rather than rejecting the client request. That behavior is compatible with Inspect AI's general bridge policy, but it is not sufficient for an Inspect-SWE API that claims to honor a caller-supplied final-output schema.

## Methodological interpretation

This is a qualification success in the methodological sense that the live pre-cohort gate exposed a false-enforcement boundary before experimental data collection.

It is **not** a successful qualification result.

The important invariant is unchanged:

> A runtime may not claim that a result-affecting structured-output contract was enforced when an intermediate bridge silently weakened that contract.

The correct response is therefore fail-closed validation before execution, not permissive output repair and not a weaker study gate.

## Revised Inspect-SWE PR requirement

The proposed Inspect-SWE feature contract has been revised before opening an upstream PR.

The new requirement is:

1. `codex_cli(output_schema=...)` validates bridge representability synchronously at construction;
2. every non-annotative JSON Schema constraint the active Inspect `JSONSchema` model cannot preserve is rejected;
3. nested failures report RFC 6901-style JSON Pointer paths;
4. `const`, `minItems`, and `maxItems` are explicit regression cases;
5. an unsupported schema fails before sandbox creation, Codex launch, bridge traffic, or model calls;
6. a bridge-representable `type + enum` schema is a positive case;
7. Inspect-SWE validates and preserves caller semantics but does **not** rewrite them.

In particular, Inspect-SWE must not automatically transform:

```json
{"const":"case-1"}
```

into:

```json
{"type":"string","enum":["case-1"]}
```

That adaptation belongs to the caller that owns the schema contract.

The revised proposal is staged in Agent-Workflow Benchmark at:

`docs/upstream/inspect-swe-176-output-schema-openspec.md`.

## Local executable implementation

Because the connected GitHub identity has read-only access to `meridianlabs-ai/inspect_swe`, the equivalent upstream behavior is implemented locally through the existing exact-byte compatibility seam rather than pushed to upstream yet.

Draft benchmark PR:

**#71 — `fix: fail closed on lossy Inspect output schemas`**

Branch:

`fix/v2-inspect-schema-representability`

The compatibility capability identity is advanced from:

`agent-workflow-benchmark/inspect-swe-codex-output-schema/v1`

to:

`agent-workflow-benchmark/inspect-swe-codex-output-schema/v2`.

The v2 capability:

- validates against the pinned Inspect AI `JSONSchema.model_fields`;
- walks the same modeled nested schema positions used by the bridge;
- reports all unsupported constraint paths deterministically;
- rejects them during `codex_cli()` construction;
- deterministically serializes only a validated schema;
- stages the already-validated bytes inside `CODEX_HOME`;
- passes the schema to native Codex with `--output-schema`;
- never rewrites unsupported schema semantics.

The benchmark package identity is advanced to `0.6.3` on the feature branch so this stronger runtime cannot be confused with the released `0.6.2` transport-only capability.

## Benchmark-owned schema adaptation

The v2 generation-time schema is changed only where required to remain representable across the pinned bridge.

### Exact case ID

Before:

```json
{"const":"<case id>"}
```

After:

```json
{"type":"string","enum":["<case id>"]}
```

### Array cardinality

Generation-time `minItems` / `maxItems` constraints are removed from:

- top-level `records`;
- `decisive_case_evidence`.

This does **not** remove those result requirements.

Deterministic post-generation validation still rejects:

- missing cases;
- extra cases;
- duplicate case IDs;
- unknown case IDs;
- wrong decision-seam sets;
- evidence arrays containing fewer than one or more than three items;
- over-length evidence strings;
- invalid rubric-rule strings;
- invalid ambiguity values.

The generation schema is therefore narrowed to the bridge-representable subset while the benchmark's acceptance contract remains fail closed.

## CI evidence and first new failure

The first draft-PR CI run proved the new Inspect-specific lane:

- compatibility patch application: passed;
- positive `type + enum` construction: passed;
- nested unsupported-keyword construction failures: passed;
- runtime capability introspection: passed;
- sandbox specification check: passed;
- guardrail probe: passed;
- agentic-Jev import lane: passed.

The general test job initially failed one test because the adjudication runtime-lock schema still required capability `.../v1`.

That failure is valid integration evidence: advancing the executable capability without advancing its frozen runtime-lock contract was correctly rejected.

The runtime-lock schema was corrected on the branch to require capability `.../v2`.

The subsequent CI run at benchmark commit `a8b209ad584d648bbc2f3d7b616c40e7d5599719` passed completely. The repository test lane, Inspect import/construction lane, and agentic-Jev import lane are therefore green for this branch state.

## Qualification rule remains unchanged

The live v2 qualifier is not weakened.

The branch is not sufficient merely because:

- unit tests pass;
- the compatibility patch installs;
- `codex_cli()` rejects unsupported schemas;
- a synthetic local schema is bridge-representable.

The complete live IA-1 through IA-11 qualification must run under the new `0.6.3` / capability-v2 runtime identity.

Any newly surfaced failure is to be retained and treated as additional integration evidence.

## Next execution boundary

Before opening the upstream Inspect-SWE pull request:

1. install benchmark branch `fix/v2-inspect-schema-representability` at or after `a8b209ad584d648bbc2f3d7b616c40e7d5599719` into the private Agent-Workflow runtime;
2. apply/verify the capability-v2 Inspect-SWE compatibility patch;
3. deliberately archive the prior failed qualification attempt;
4. freeze a new v2 runtime lock bound to benchmark `0.6.3`, capability v2, and its patched source hash;
5. rerun full live IA-1 through IA-11 qualification through Codex-LB / DeepSeek Flash;
6. inspect the generated A/B and C schema artifacts/hashes and every qualification gate;
7. preserve any new failure as another additive integration checkpoint;
8. open the upstream Inspect-SWE PR only after the local behavior has survived live qualification;
9. keep real A/B/C blocked until that qualification genuinely passes.

## Current phase map

```text
routing-semantic-v2 2.0.0
  frozen study/dataset/protocol          COMPLETE / UNCHANGED
  frozen blinded authoring view          COMPLETE / UNCHANGED
  framing-contract failure               PRESERVED
  native output-schema transport         IMPLEMENTED
  schema-bridge loss                     FOUND / PRESERVED
  Inspect-SWE PR spec revision            COMPLETE
  local fail-closed compatibility v2     IMPLEMENTED ON DRAFT PR
  bridge-representable benchmark schema  IMPLEMENTED ON DRAFT PR
  benchmark package                      0.6.3 ON DRAFT PR
  repository CI                          PASS
  new live runtime lock                  BLOCKED ON PRIVATE BRANCH INSTALL
  live IA-1..IA-11 qualification         BLOCKED ON PRIVATE RUNTIME
  upstream Inspect-SWE PR                BLOCKED ON LIVE QUALIFICATION
  real A/B/C                             BLOCKED
```

## Claim boundary

Safe:

> Live v2 qualification exposed that Inspect AI 0.3.268 weakens unsupported JSON Schema constraints at the bridge. No oracle sample completed. The proposed Inspect-SWE feature has therefore been strengthened to reject bridge-unrepresentable schemas at construction, and the benchmark's model-facing schema has been narrowed to the representable subset without relaxing deterministic result validation.

Not yet safe:

> The capability-v2 runtime has passed live IA-1 through IA-11 qualification.

That claim requires the next private live run.
