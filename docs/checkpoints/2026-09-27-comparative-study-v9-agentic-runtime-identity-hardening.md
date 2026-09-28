# Comparative Evaluation — Agentic Jev Runtime Identity Hardened Before Live Freeze

**Date:** 2026-09-27  
**Checkpoint:** `comparative-study-v9`  
**Relationship to v8:** additive pre-live correction; v8 remains the historical record of the first live-preflight boundary.

## Discovery

A static review performed after the v8 implementation checkpoint but **before any live agentic-Jev runtime lock, tool qualification, or 24 × 3 pilot run** found a reproducibility gap in the pilot runtime identity.

The runtime lock already bound:

- Codex CLI identity;
- Inspect AI / Inspect SWE versions;
- coding model and model arguments;
- optional requested Jev model;
- frozen TypeSafe skill snapshot;
- exact 24-task development manifest;
- Docker identity;
- host-tool receipt contract.

It did **not** bind two result-affecting host-runtime components:

1. the exact implementation of the host-side Jev bridge itself;
2. the installed `typesafe-sdk` version used by that bridge.

A later edit to the bridge implementation or an SDK change could therefore have occurred after the runtime lock was created while the lock still appeared valid.

## Correction

Agent-Workflow Benchmark PR **#55**, merged as:

`c0c2a7affa1375af985c2af3fa9283134befe239`

hardens `agentic-jev-pilot-v1` before its first live freeze.

The runtime lock now records and later re-verifies:

- SHA-256 of `agent_workflow_benchmark.benchmarking.agentic_jev`;
- exact `typesafe-sdk==0.6.0` runtime identity.

Runtime-lock creation fails if the pinned SDK is unavailable or has a different version. Qualification and pilot execution reject a lock if either the host-tool implementation hash or SDK version has changed.

The runtime-lock schema, tests, and pilot documentation were updated with the same invariant.

## Verification

The corrected benchmark PR passed all repository CI jobs on its final head:

- `test` — passed;
- `agentic-jev-import` — passed;
- `inspect-import` — passed.

The dedicated agentic-Jev import job also verifies that the installed SDK version is `0.6.0`.

## Why this is a pre-freeze correction, not a study revision

No agentic-Jev live runtime lock had been frozen and no provider result had been observed when this gap was found.

Therefore:

- no experimental outcome was discarded or reinterpreted;
- no frozen cohort was mutated;
- no pilot semantics were changed after observing results;
- the correction belongs to the pre-execution qualification boundary.

This is exactly the kind of defect the freeze/qualification process is intended to expose.

## Current boundary

The v8 phase map remains valid except that the runtime-freeze step now carries a stronger identity contract.

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
  host-tool/SDK identity lock   COMPLETE
  runtime freeze                NEXT
  live tool qualification       NEXT
  24 × 3 pilot                  BLOCKED ON QUALIFICATION
~~~

## Immediate execution sequence

After updating the benchmark checkout to the merged PR #55 state:

1. run the routing-semantic-v2 synthetic IA-9/10/11 evidence preflight;
2. inspect its artifact and require IA-9/10/11 to pass while `real_cohort_ready` remains `false`;
3. freeze the agentic-Jev runtime using the strengthened lock;
4. run the one-call agentic-Jev tool qualification;
5. inspect the runtime lock and qualification artifact;
6. do **not** run the 24 × 3 pilot unless qualification passes.

The frozen v1 study remains unchanged.
