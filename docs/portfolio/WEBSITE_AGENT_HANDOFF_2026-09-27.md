# Website Agent Handoff — Comparative Evaluation Published Result

**Date:** 2026-09-27  
**Audience:** portfolio / website synthesis agent  
**Status:** P0A–P3 complete; sanitized public result published

## Current authoritative state

The first `routing-semantic-v1` study is complete.

~~~text
P0A  adjudicator/runtime qualification           COMPLETE
P0B  blinded independent oracle                   COMPLETE
P1   bounded live instrumentation smoke           PASS
P2   full 120-case comparative inference/report  COMPLETE
P3   sanitized publication + verification         COMPLETE / PUBLISHED
~~~

Public evidence is now available in:

`ngallodev-software/agent-workflow-benchmark-results/comparative-eval/routing-semantic-v1/results/`

Published benchmark-results merge:

`8b3f07d5d52c8405631cca95395aaa7a7d2d7abd`

The P3 verification independently passed the privacy/integrity boundary before publication.

## Study shape

- frozen study: `routing-semantic-v1` / `1.1.0`;
- dataset: `routing-semantic-corpus-v1.0.0`;
- frozen cases: **120**;
- observations: **360**;
- provider requests: **120**;
- oracle outcomes: **360**;
- exclusions: **0**;
- oracle: `routing-semantic-oracle-v1.0.0`;
- question set: `routing/v2`;
- projector: `routing-state/v2`;
- oracle absent during inference;
- all three seams study-eligible at `n=120`.

## Public result

### Interaction required

- semantic candidate: **91.67% accuracy** (110/120);
- deterministic control: **71.67%** (86/120);
- paired candidate-minus-control difference: **+20.0 percentage points**;
- 95% interval: **+10.83 to +29.17 points**;
- beneficial changes: **30**;
- harmful changes: **6**.

### Task class

- semantic candidate: **81.67% accuracy** (98/120);
- deterministic control: **52.50%** (63/120);
- paired difference: **+29.17 percentage points**;
- 95% interval: **+20.0 to +38.33 points**;
- beneficial changes: **38**;
- harmful changes: **3**;
- changed but both wrong: **10**.

### Semantic risk

- semantic candidate MAE: **0.28975**;
- deterministic control MAE: **0.29167**;
- paired candidate-minus-control absolute-error mean: **-0.001917**;
- 95% interval: **-0.101917 to +0.092917**.

The semantic-risk result does **not** show the separation seen in the two classification seams.

## Calibration

- interaction-required Brier: **0.07741**;
- interaction-required ECE: **0.14942**;
- task-class multiclass Brier: **0.27346**;
- task-class log loss: **1.80242**;
- semantic-risk multiclass Brier: **0.32484**;
- semantic-risk log loss: **0.53531**.

One probability vector out of 120 in each multiclass seam had total probability mass 0.99. Raw evidence was preserved; only the derived calibration copy was normalized. The public report discloses this.

## Request-level evidence

- provider requests: **120**;
- successful requests: **120**;
- input tokens: **91,445**;
- output tokens: **10,598**;
- provider total tokens: **102,043**;
- p50 request duration: **0.1468 s**;
- p90: **0.1865 s**;
- p95: **0.2206 s**.

Provider cost evidence is incomplete. **Do not publish a treatment-cost conclusion.**

## What the website can now say

Safe, source-backed wording includes:

- in this frozen 120-case routing cohort, the semantic candidate was more accurate than the deterministic control on **task classification** and **interaction-required classification**;
- the paired intervals for those two accuracy differences remained above zero;
- semantic-risk ordinal error was approximately unchanged at this study's resolution;
- all 120 semantic provider requests completed successfully;
- the full study had zero exclusions;
- the independent oracle was frozen before inference and was joined only afterward;
- the P3 public bundle passed explicit privacy/integrity checks before publication.

Prefer **seam-specific language** over a single overall-winner statement.

## What the website should not say

Do not generalize this study into claims that:

- TypeSafe/Jev is universally better than deterministic routing;
- Jev improves downstream software quality;
- Jev is cheaper;
- Jev is faster overall;
- semantic risk improved materially;
- the result proves a causal benefit outside the frozen corpus/runtime;
- the study captured or published hidden chain-of-thought.

Do not publish private A/B/C votes, private reasoning-summary text, human-resolution rationale/participant identity, credentials, or raw provider traffic.

## Methodological story worth preserving

The portfolio narrative should not begin with the final percentages.

The engineering progression is the stronger story:

~~~text
"semantic and deterministic routing disagree"
        |
        v
disagreement is not correctness
        |
        v
freeze an independent blinded oracle
        |
        v
discover the oracle contract dropped structured rationale
        |
        v
audit retained logs: reasoning summaries existed upstream
        |
        v
learn that evidence must survive projection boundaries
        |
        v
run bounded P1 instrumentation smoke
        |
        v
run full P2 cohort
        |
        v
report crashes on a 0.99 probability mass
        |
        v
preserve raw evidence; normalize derived calibration only
        |
        v
P3 review catches private-oracle disclosure risk
        |
        v
publish an explicit redacted public projection
~~~

The recurring theme is **evidence engineering**: what is generated, what is retained, what is transformed, what is allowed into a claim, and what must remain private.

## Oracle-provenance correction

The v1 authoritative A/B/C pass retained labels but no structured per-decision rationales.

A later audit found contemporaneous provider reasoning summaries in private Inspect logs. This corrected the diagnosis:

- explanatory evidence existed upstream;
- the labels-only pass did not promote it into the authoritative resolution record;
- the original human resolver did not receive it;
- the frozen v1 oracle was not rewritten.

Future v2 design requires provider-neutral structured justifications and explicit aggregate-session usage provenance.

Do not describe the private reasoning summaries as hidden chain-of-thought.

## P3 publication boundary

A pre-publication review found that the original publisher would have copied the private frozen oracle verbatim.

That was corrected before public release.

The published oracle is now an explicit public projection:

**Retained:**

- final frozen labels;
- resolution status;
- resolution method.

**Removed:**

- adjudicator identities;
- individual A/B/C votes;
- pass hashes/timestamps;
- human-resolution rationale;
- participant identities;
- private reasoning summaries.

This is a useful engineering milestone in its own right:

> A valid private artifact is not automatically a valid public artifact.

## Recommended website structure

### Above the fold

A concise framing:

> **A 120-case blinded comparative routing study, with ground truth frozen before inference.**  
> The semantic candidate improved task-class and interaction-required accuracy in the frozen cohort; semantic-risk error was effectively unchanged. The more important engineering story is how the evaluation was rebuilt around independent ground truth, lossless evidence, and a fail-closed publication boundary.

### Result visual

Use three separate seam cards or rows rather than one aggregate score:

~~~text
Task class
81.7% semantic vs 52.5% control
+29.2 pp [95%: +20.0, +38.3]

Interaction required
91.7% semantic vs 71.7% control
+20.0 pp [95%: +10.8, +29.2]

Semantic risk
MAE 0.290 vs 0.292
paired interval spans zero
~~~

The visual should make the heterogeneous result obvious.

### Methodology/evolution visual

Show the pipeline:

~~~mermaid
flowchart LR
    A[Frozen cases] --> B[Deterministic control]
    A --> C[Semantic candidate]
    D[Blinded A/B/C oracle] --> E[Frozen ground truth]
    B --> F[Inference evidence]
    C --> F
    F --> G[Post-inference oracle join]
    E --> G
    G --> H[Correctness / calibration / reliability]
    H --> I[P3 public projection]
    I --> J[Verified public evidence]
~~~

Below that, use the dated failure/correction timeline.

## Ordered source pack

Read in this order:

1. `docs/checkpoints/2026-09-27-comparative-study-v7-publication.md`
2. `docs/portfolio/COMPARATIVE_STUDY_PROGRESS.md`
3. public result: `agent-workflow-benchmark-results/comparative-eval/routing-semantic-v1/results/README.md`
4. public machine summary: `.../results/summary.json`
5. public P3 verification: `.../results/verification.json`
6. public integrity note: `.../results/PUBLICATION-INTEGRITY.md`
7. `docs/studies/routing-semantic-v1.md`
8. `docs/studies/routing-semantic-v1-oracle-review-guide.md`
9. `docs/studies/routing-semantic-v1-oracle-protocol.md`
10. `docs/audits/2026-09-26-oracle-decision-justification-evidence-gap.md`
11. `docs/audits/2026-09-27-oracle-reasoning-summary-retention-audit.md`
12. `docs/plans/routing-semantic-v2-adjudication-evidence-contract.md`
13. Agent-Workflow Benchmark `docs/COMPARATIVE_DECISION_STUDY.md`
14. Agent-Workflow Benchmark `scripts/decision-study/README.md`

## Website-agent synthesis instruction

> Update the comparative-evaluation case study from the P3-verified public evidence, not from private P2 files. Present the three routing seams separately. State that task-class and interaction-required accuracy were higher for the semantic candidate in the frozen 120-case cohort, with their paired 95% intervals, while semantic-risk MAE was approximately unchanged and its interval spans zero. Preserve the evolution-of-method story: disagreement was not correctness; an independent oracle was frozen before inference; structured adjudicator rationale was accidentally omitted from the authoritative pass even though private reasoning summaries later proved explanatory evidence existed upstream; the full run exposed a calibration-mass edge case; and P3 review caught a private-oracle publication risk before release. Do not collapse the results into a universal winner claim, do not claim downstream software-quality causality or cost advantage, and do not publish private oracle provenance or reasoning-summary text.
