# Comparative Evaluation — Second Live v2 Preflight Isolates Provenance-Count Instrumentation Gap

**Date:** 2026-09-28  
**Checkpoint:** `comparative-study-v13`  
**Relationship to v12:** additive live-qualification correction; v12 remains the record of the first terminal-output extraction failure.

## What happened

After benchmark PR #60 corrected terminal-agent-output extraction and forced-retry cleanup, the DeepSeek-backed `routing-semantic-v2` IA-9/10/11 evidence preflight was rerun from a clean generated evidence root.

The second attempt completed far enough to emit the preflight artifact and evaluate all three new evidence gates.

Observed gate state:

- **IA-9 — pass**
- **IA-10 — fail**
- **IA-11 — pass**

The preflight therefore remained non-passing overall and did not authorize the real v2 cohort.

The generated evidence showed that A/B/C usage retained token totals, but both of the request-scope counters required by IA-10 were null:

- `model_call_count: null`
- `provider_request_count: null`

The failure was isolated to provenance-count instrumentation rather than adjudication structure, C blinding, or optional reasoning-summary capability.

## Evidence boundary

The second attempt established several useful facts without becoming a valid readiness pass.

IA-9 demonstrated that the v2 adjudication records round-tripped with the expected study/dataset/protocol/schema identities, distinct A/B/C adjudicators, and a blinded C input view that did not include A/B labels or justifications.

IA-11 demonstrated that the optional reasoning-summary capability gate was satisfied on the live path.

IA-10 failed because the benchmark was still attempting to obtain request counts from aggregate `ModelUsage` evidence. The pinned Inspect usage object carries token/cost aggregates but does not provide the request counters the v2 provenance contract needs.

The stronger per-call evidence surface is the typed Inspect `ModelEvent` stream attached to `sample.events`.

## Diagnostic correction

Benchmark PR #61 merged before the instrumentation fix:

`247ef783e466c6817028cdb2161ef495ef8f7ebb`

It preserved the fail-closed behavior but made the raised preflight failure identify every non-passing IA gate and the generated artifact path.

No study semantics or evidence schema changed in that PR.

## IA-10 correction

Benchmark PR #62 merged as:

`a898b39d6ef476e99dc1d33080c7b6e01c2494f9`

The v2/newer provenance path now derives counts from Inspect model events:

- `model_call_count` = number of typed `ModelEvent` records;
- `provider_request_count` = non-cache model events plus recorded retries;
- cache reads remain logical model calls but do not count as provider requests;
- invalid retry evidence fails closed instead of being silently zero-filled.

`ModelUsage` remains authoritative for aggregate token/cost usage. It is no longer treated as a request-count source.

The historical `routing-semantic-v1` provenance shape remains unchanged.

## Package/version alignment

The correction also closes the cross-repository version mismatch that was visible during the second preflight investigation.

### comparative-eval

PR #23 had already merged the study-contract release:

- package: `0.3.0`
- merge: `fd596aa67cccb940338617cbe04317a1715884b7`

### benchmark

PR #62 advances the benchmark package:

- `0.4.1` -> `0.5.0`
- `agent-workflow>=0.11.11,<0.12`
- `agent-workflow-comparative-eval==0.3.0`

The package, import/plugin, README, dependency, and CI version surfaces are aligned.

The PR CI completed successfully before merge.

## Interpretation boundary

The second preflight is a valid failure artifact, not a passing readiness result.

It supports the narrow statements that:

- the repaired terminal-output path completed A/B/C strongly enough to evaluate IA-9/10/11;
- IA-9 and IA-11 passed;
- IA-10 exposed a request-count instrumentation defect;
- the defect was corrected after the failed attempt;
- no real v2 cohort has been authorized or run.

It does **not** support any new treatment-effectiveness claim, v2 oracle outcome, or pilot outcome.

No v1 result, v2 case content, rubric, model identity, or observed adjudication label was modified.

## Aha

> Aggregate usage and per-call provenance are different evidence layers.

A token/cost aggregate can be complete for accounting while still being insufficient to answer how many logical model calls or provider requests occurred. Those counts must come from the event stream that actually represents calls and retries.

## Updated phase map

~~~text
routing-semantic-v2 2.0.0-draft.2
  model identity                    FROZEN: DeepSeek Flash
  evidence-contract implementation COMPLETE
  first live preflight              FAILED: terminal-output extraction
  extraction correction             MERGED: benchmark 37b1e967...
  second live preflight             IA-9 PASS / IA-10 FAIL / IA-11 PASS
  count instrumentation correction  MERGED: benchmark a898b39d...
  benchmark package                 0.5.0
  comparative-eval package          0.3.0
  clean post-fix preflight          NEXT
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

Update the benchmark host to merge `a898b39d6ef476e99dc1d33080c7b6e01c2494f9` or later, then rerun the DeepSeek v2 preflight from the clean forced-retry path.

Expected success boundary remains:

~~~text
IA-9 pass
IA-10 pass
IA-11 pass
real_cohort_ready: false
~~~

A passing synthetic preflight still does not authorize real v2 adjudication. The real authoring/module/runtime freeze and remaining IA qualification stay separate gates.
