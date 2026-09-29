# Comparative Study v22 — Real-cohort structured-output schema scale boundary

**Date:** 2026-09-29  
**Study:** `routing-semantic-v2`  
**Status:** implementation hardening in progress; real oracle A/B/C re-blocked pending fresh 0.6.4 qualification

## Context

v21 records a genuine full live qualification pass for the strengthened
`routing-semantic-v2` structured-output path. That result remains valid historical
evidence for benchmark 0.6.3 and is not rewritten by this checkpoint.

Before starting the first real 120-case A/B cohort, a separate readiness review
examined the model-facing schema at real-cohort scale. No real v2 oracle label had
been produced when this boundary was discovered.

## Scale finding

The frozen v2 authoring view contains 120 cases.

Every one of those 120 cases has the same three eligible decision seams:

- `routing.task_class`;
- `routing.interaction_required`;
- `routing.semantic_risk`.

The 0.6.3 schema generator nevertheless emitted one complete record-schema
variant per case. Each variant repeated the same label and justification shape and
differed only in its one-value `case_id` enum.

A deterministic reconstruction of the real model-facing schema measured:

- per-case `anyOf` representation: **225,971 serialized characters**;
- eligibility-grouped representation: **3,310 serialized characters**;
- reduction: **222,661 characters / 98.54%**;
- case identities preserved: **120 of 120**.

The schema content is ASCII at this boundary, so the serialized character count
also approximates the request-body byte contribution.

## Why v21 did not exercise this boundary

The full qualification correctly tested A/B/C structured-output enforcement,
justification round trips, provenance, and transport using a small synthetic
qualification view.

That synthetic view contained two cases. It therefore proved the contract and
transport behavior but did not stress the schema generator at the 120-case real
cohort size.

The v21 qualification should not be stretched into evidence about a scale it did
not exercise.

## Representation-only hardening

Benchmark 0.6.4 changes the v2 model-facing schema representation without changing
the oracle semantics.

Cases are grouped by identical eligible-decision sets. Each group receives one
record schema whose `case_id` field is a string enum containing all case IDs in
that group.

For the frozen real v2 authoring view, all 120 cases share one eligibility shape,
so the real primary schema becomes one record variant with a 120-value case-id
enum rather than 120 repeated record variants.

The following deterministic invariants remain unchanged after generation:

- exact expected case set;
- no missing cases;
- no unexpected cases;
- no duplicate cases;
- exact required decision seams per case;
- valid labels;
- required structured justifications;
- justification evidence cardinality and bounded fields.

The compaction therefore changes transport representation, not ground-truth
semantics or acceptance criteria.

Strategy identity:

`eligibility-grouped-case-enum/v1`

## Qualification invalidation boundary

The 0.6.3 v21 qualification is preserved but is not sufficient to authorize real
runs under the 0.6.4 schema generator.

The new implementation records in IA-1:

- `agent_workflow_benchmark_version = 0.6.4`;
- `v2_output_schema_strategy = eligibility-grouped-case-enum/v1`.

Both the core real-run qualification gate and the repository-owned v2 oracle
driver reject a qualification whose benchmark version or schema-strategy identity
does not match the installed implementation.

This prevents the earlier passing manifest from being silently reused after the
model-facing schema changed.

## Real-cohort operator hardening

The same pre-live review found that the historical `p0b-*` shell workflow is
versioned around v1 defaults. A dedicated `v2-oracle.sh` driver is being added
instead of relying on manual environment overrides.

The v2 driver is designed to:

- require IA-1 through IA-11;
- require exact module/runtime/qualification hashes;
- require clean benchmark/comparative checkouts and installed-source parity;
- verify the module-pinned authoring view, protocol, and corpus;
- write immutable private run identity before the first provider call;
- pass `--study routing-semantic-v2` explicitly to generic decision-study
  commands;
- freeze only as `routing-semantic-oracle-v2.0.0`;
- keep full model output in private stage logs;
- retain sanitized Codex-LB ingress evidence by default;
- fail if observed model requests do not carry `json_schema`, `strict=true`,
  and the exact persisted stage-schema hash;
- refuse in-place retries of real model stages;
- stop at the human-resolution boundary when three-way conflicts require review.

## Current execution boundary

Real `routing-semantic-v2` A/B/C is blocked again.

Before any real label:

1. benchmark 0.6.4 grouped-schema implementation and v2 driver must pass CI;
2. the private host must install that exact benchmark checkout;
3. the prior v21 qualification must be archived, not overwritten;
4. a fresh full live qualification must pass IA-1 through IA-11;
5. the new manifest must record benchmark 0.6.4 and
   `eligibility-grouped-case-enum/v1` in IA-1;
6. sanitized ingress evidence must again confirm the intended strict schema
   transport.

Only after those gates pass may the real A/B cohort start.

## Historical boundary

This checkpoint does not weaken or reinterpret v19, v20, or v21.

- v19 remains the schema-representability failure.
- v20 remains the prose-plus-JSON C enforcement failure.
- v21 remains the first full successful qualification and ingress proof for
  benchmark 0.6.3.
- v22 records a newly discovered real-cohort scale boundary before real evidence
  was produced.

The sequence is itself part of the engineering evidence.
