# Comparative Evaluation — P2 Completion / Reasoning-Summary Audit / P3 Handoff

**Date:** 2026-09-27  
**Checkpoint:** `comparative-study-v6`  
**Supersedes execution sequencing in:** `docs/checkpoints/2026-09-26-comparative-study-v5-checkpoint.md`

## Phase state

- P0A authenticated adjudicator qualification: **complete**;
- P0B independent oracle construction/freeze/validation: **complete**;
- P1 bounded live instrumentation smoke: **pass**;
- P2 full 120-case comparative inference/reporting: **complete**;
- P3 sanitized publication preparation/review: **next**.

## P2 execution evidence

The completed P2 run reports:

- frozen cases: **120**;
- per-seam observations: **360**;
- provider requests: **120**;
- exclusions: **0**;
- oracle outcomes after post-inference join: **360**;
- all three observed seams eligible at `n=120`;
- oracle was not visible during inference.

The detailed outcome report remains on the private evidence path pending P3 publication review. This checkpoint intentionally does not copy private case-level artifacts or unreviewed outcome claims into the public repository.

## Oracle provenance finding corrected after private-log audit

The 2026-09-26 postmortem correctly identified that the authoritative A/B/C pass and human-resolution workflow lacked structured per-decision justifications.

A subsequent audit of the retained private Inspect `.eval` logs established that provider/model reasoning summaries had survived as supplementary execution evidence.

Therefore:

~~~text
model/harness explanation capability            available in actual cohort
private Inspect reasoning-summary events        retained
authoritative adjudication-pass rationale       absent
available to original human resolution          no
raw hidden chain-of-thought                     not claimed / not required
safe to retrofit into frozen oracle             no
~~~

The methodological failure is **decision-provenance promotion**: useful explanatory evidence existed in the runtime transcript, but the labels-only output contract and pass wrapper did not promote a bounded rationale into `adjudication.json` or the resolution worksheet.

Authoritative correction:

`docs/audits/2026-09-27-oracle-reasoning-summary-retention-audit.md`

The original postmortem remains linked as the record of the failure as first understood.

## Additional provenance-accounting issue

The same audit found that per-role `inspect-provenance.json` usage reflected final sample-output usage rather than aggregate model/session usage for the multi-call adjudication session.

Those fields must not be used as complete oracle-session token totals.

The already recorded provider/API aggregate through oracle freeze remains the public accounting source:

- **36** API requests;
- **726,263** tokens;
- **$0.07 USD** provider/API cost.

Future provenance contracts should distinguish final-output usage from aggregate session/model usage explicitly.

## P3 boundary

P3 should:

1. prepare the benchmark-owned sanitized publication tree;
2. review aggregate P2 correctness/calibration/reliability/efficiency metrics;
3. verify every denominator and exclusion;
4. confirm that private oracle reasoning summaries and private case-level evidence are absent;
5. publish only approved aggregate/sanitized evidence;
6. update the website handoff from methodology/status claims to outcome claims only after that review.

## Future adjudication contract

A future versioned oracle cohort should require a provider-neutral structured justification for each eligible label.

Reasoning summaries may be retained privately as supplementary execution evidence when available, but must not substitute for the authoritative justification contract.

P0A should fail unless the label + structured-justification evidence survives:

~~~text
model output
  -> pass wrapping
  -> schema validation
  -> dispute construction
  -> human-resolution rendering
  -> final evidence bundle
~~~

## Immediate continuation summary

> P2 inference/reporting is complete on the full frozen 120-case cohort with 360 observations, 120 provider requests, and 0 exclusions. A post-freeze private-log audit corrected the oracle-provenance diagnosis: reasoning summaries were retained in Inspect logs, but the authoritative labels-only pass omitted structured justifications and the original human-resolution workflow never saw the summaries. The frozen oracle remains unchanged. P3 sanitized-publication review is next.
