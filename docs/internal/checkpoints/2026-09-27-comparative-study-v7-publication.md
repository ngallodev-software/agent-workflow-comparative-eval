# Comparative Evaluation — P3 Verified Publication

**Date:** 2026-09-27  
**Checkpoint:** `comparative-study-v7`  
**Supersedes current execution state in:** `docs/checkpoints/2026-09-27-comparative-study-v6-checkpoint.md`

## Final v1 phase state

~~~text
P0A  authenticated adjudicator qualification      COMPLETE
P0B  independent oracle freeze + validation       COMPLETE
P1   live instrumentation smoke                   PASS
P2   full 120-case comparative study              COMPLETE
P3   sanitized public evidence                    VERIFIED + PUBLISHED
~~~

The frozen v1 study is complete.

## P3 verification

The publication verifier passed with:

- 120 cases;
- 120 public oracle records;
- 120 provider requests;
- 360 observations;
- 360 oracle outcomes;
- 0 exclusions;
- study eligibility: true;
- exact file allowlist: pass;
- manifest integrity: pass;
- public oracle projection: pass;
- evidence privacy contract: pass;
- no private A/B/C adjudicator votes;
- no human-resolution rationale;
- no human participant identity;
- no private reasoning summaries.

Reviewed source P3 archive SHA-256:

`b07c3899dfa6c504a919e6eb425f2e561267bc994ee86ce880972ae8b84abad2`

## Public evidence

Published in Agent-Workflow Benchmark Results:

`comparative-eval/routing-semantic-v1/results/`

Benchmark-results merge:

`8b3f07d5d52c8405631cca95395aaa7a7d2d7abd`

The public evidence includes:

- result narrative;
- machine-readable aggregate summary;
- P3 verification record;
- human-readable study report;
- publication-integrity note;
- reviewed source-bundle checksum.

Private P0B Inspect logs, private frozen-oracle provenance, individual A/B/C votes, human-resolution rationale/participant identity, raw provider traffic, and private reasoning summaries remain unpublished.

## Published seam-level result

### Interaction required

- candidate: 110/120 = **91.67% accuracy**;
- deterministic control: 86/120 = **71.67%**;
- paired difference: **+20.0 pp**;
- 95% interval: **+10.83 to +29.17 pp**.

### Task class

- candidate: 98/120 = **81.67% accuracy**;
- deterministic control: 63/120 = **52.50%**;
- paired difference: **+29.17 pp**;
- 95% interval: **+20.0 to +38.33 pp**.

### Semantic risk

- candidate MAE: **0.28975**;
- deterministic control MAE: **0.29167**;
- paired error difference: **-0.001917**;
- 95% interval: **-0.101917 to +0.092917**.

The semantic-risk interval spans zero; do not characterize that seam as a demonstrated improvement.

## Request evidence

- 120/120 provider requests succeeded;
- input tokens: 91,445;
- output tokens: 10,598;
- provider total tokens: 102,043;
- p50 latency: 0.1468 s;
- p90: 0.1865 s;
- p95: 0.2206 s.

Provider cost evidence is incomplete. No treatment-cost conclusion is supported.

## Calibration/reporting note

One probability vector out of 120 in each multiclass seam had total probability mass 0.99.

The reporting correction:

- preserved raw evidence;
- normalized only the derived calibration copy;
- recorded 1/120 normalized vectors per multiclass seam;
- recorded maximum mass deviation 0.01.

## Final public claim boundary

Supported:

- higher semantic-candidate accuracy for task class and interaction-required decisions in this frozen cohort;
- no comparable semantic-risk error separation;
- zero exclusions;
- 120/120 provider success;
- request-level token/latency evidence;
- independent frozen-before-inference oracle;
- verified public/privacy boundary.

Not supported:

- universal superiority of TypeSafe/Jev;
- downstream software-quality causality;
- cost advantage;
- material semantic-risk improvement;
- generalization beyond the frozen study without replication.

## Methodological history remains part of the result

Do not erase the failures that produced the final design:

1. disagreement was initially being treated as useful evidence without independent correctness;
2. semantic probability evidence had previously been lost in persistence projection;
3. the authoritative oracle pass omitted structured decision justifications;
4. later audit found reasoning summaries existed upstream in private Inspect logs;
5. oracle provenance usage had final-output rather than aggregate-session scope;
6. full P2 reporting exposed a 0.99 probability-mass assumption;
7. P3 review caught that the original publisher would have copied private oracle provenance.

The completed study is therefore also a case study in evidence engineering.

## Future work

The frozen v1 study is closed.

Future adjudication changes belong to a new versioned study/protocol and are tracked in:

`docs/plans/routing-semantic-v2-adjudication-evidence-contract.md`

The v2 design requires structured provider-neutral rationales and explicit aggregate-session usage provenance before another real cohort begins.
