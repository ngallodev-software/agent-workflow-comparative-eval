# Website Agent Handoff — Comparative Evaluation After Oracle Freeze

**Date:** 2026-09-26  
**Audience:** portfolio / website synthesis agent  
**Purpose:** update the public-facing case-study narrative after completion of P0A/P0B without overstating P1/P2 results.

## Current authoritative state

The routing-semantic comparative study has advanced materially since the earlier portfolio notes.

Completed:

- P0A authenticated adjudicator qualification;
- IA-1 through IA-8 qualification gates;
- independent blinded A/B oracle adjudication;
- disagreement-only C adjudication;
- recorded human resolution of genuine three-way conflicts;
- oracle freeze;
- final oracle validation against the frozen 120-case corpus.

The qualified adjudicator path for the completed cohort was:

`openai-api/codex-lb/deepseek-flash`

The independent oracle is now frozen and available privately for later post-inference joining.

Not yet completed:

- P1 bounded live TypeSafe/Jev instrumentation smoke;
- P2 full 120-case comparative inference;
- P2 correctness/calibration/efficiency report;
- P3 sanitized public evidence publication.

Therefore **do not claim that TypeSafe/Jev is more accurate, faster, cheaper, better calibrated, or more reliable than deterministic control yet**.

## What changed in the story

Earlier work could answer:

> Does semantic routing disagree with deterministic routing?

That is not enough to establish improvement.

The study architecture now answers the more important question:

> When semantic routing disagrees with deterministic routing, which decision is actually more correct against an independently frozen oracle?

That required moving from implementation/benchmark instrumentation into explicit experimental design:

~~~text
routing case
   |
   +--> deterministic control
   |
   +--> semantic candidate
   |
   +--> independent oracle
             |
             +--> blinded A
             +--> blinded B
             +--> disagreement-only C
             +--> recorded human resolution when A/B/C have no majority
~~~

The oracle is frozen before live comparative inference, so candidate/control results cannot influence the ground truth used to score them.

## Why this is portfolio-relevant

The strongest portfolio story is not "I added another benchmark."

The stronger story is the evolution from:

1. observing model-assisted routing behavior;
2. discovering that disagreement is not correctness;
3. identifying missing evidence needed for calibration and comparison;
4. separating deterministic workflow authority from semantic evidence;
5. preregistering measurable research questions;
6. creating a public-safe 120-case corpus;
7. designing a blinded independent oracle;
8. qualifying an isolated A/B/C adjudication runtime;
9. freezing the ground truth before treatment inference;
10. building a staged P1/P2/P3 execution lane so instrumentation is verified before committing to the full study.

This demonstrates engineering work around evidence quality, experimental controls, reproducibility, privacy boundaries, failure accounting, and claim discipline.

## Newly safe claims for the website

The site may now state that:

- the study has a frozen, independently adjudicated oracle;
- A and B labeled the blinded authoring view independently;
- C received only disputed cases/seams and did not see A/B labels;
- true three-way conflicts were resolved through a recorded human-review step under the frozen rubric;
- the oracle was frozen and validated before live comparative inference;
- the adjudication runtime was qualified through IA-1 through IA-8 before real labels were produced;
- the oracle and inference paths remain structurally separate;
- the next phase is a bounded live instrumentation smoke before the preregistered full run;
- a favorable semantic result is not required for publication.

Do not expose private A/B/C adjudication artifacts, credentials, raw provider traffic, or private host paths.

## Claims that remain prohibited until P2

Do not say or imply:

- TypeSafe/Jev improves routing correctness;
- TypeSafe/Jev reduces errors;
- semantic routing is more accurate than deterministic routing;
- one arm "won";
- latency/cost overhead is acceptable or superior;
- calibration is good;
- the confidence policy is validated;
- the 120-case study has been run.

Those statements require P2 evidence.

## Current execution phase map

~~~text
P0A  authenticated adjudicator qualification      COMPLETE
P0B  independent oracle freeze + validation       COMPLETE
P1   bounded live instrumentation smoke           TOOLING READY / NOT YET RUN
P2   full 120-case comparative study              PENDING P1
P3   sanitized publication                        PENDING P2
~~~

Agent-Workflow Benchmark commit `68b9d7763369cadeeb0ed87c6c33864263a8d9b2` adds the reproducible post-oracle execution lane:

~~~text
scripts/decision-study/
  env.sh
  lib.sh
  p1-prepare-smoke.sh
  p1-run-smoke.sh
  p1-verify-smoke.sh
  p1-all.sh
  p2-run-full.sh
  p2-report.sh
  p2-all.sh
  p3-publish-prepare.sh
  README.md
~~~

The normal P1 operator entry point is:

~~~bash
bash scripts/decision-study/p1-all.sh
~~~

P1 deterministically derives a small development-only subset from the exact frozen corpus and records the source corpus hash + selected case IDs. Its verification checks the live evidence chain before P2.

## Important methodological detail to preserve

The study separates three concepts that should not be collapsed in the website explanation:

~~~text
semantic model evidence
        |
        v
Agent-Workflow candidate policy
        |
        v
applied deterministic decision
~~~

Agent-Workflow remains workflow/lifecycle authority. TypeSafe/Jev supplies semantic evidence.

The study separately evaluates:

- raw semantic evidence quality;
- policy/candidate behavior;
- the applied control decision.

This is important because a useful semantic signal can exist even when deterministic policy intentionally remains authoritative.

## Oracle reviewer semantics

If explaining the human-resolution step, use the reviewer guide rather than raw JSON terminology.

Key concepts:

- `task` = the verbatim case prompt;
- `metadata` = supporting evidence, not an answer key;
- `oracle_eligible` = which seams require labels, not the labels themselves;
- `routing.task_class` asks for the primary requested deliverable;
- `routing.interaction_required` asks whether a material external decision/authorization is missing;
- `routing.semantic_risk` asks the consequence of acting on a materially wrong interpretation.

Do not imply that declared metadata such as `risk: low` is itself ground truth.

## Known limitation discovered during P0B

The frozen protocol envisioned using independent adjudicator rationales during genuine three-way discussion.

The completed Inspect cohort persisted independent labels but not the adjudicators' original rationales because the output contract requested labels-only JSON.

Human resolution therefore used:

- the frozen case prompt;
- supplied metadata;
- the frozen rubric;
- A/B/C independent labels.

Do not reconstruct missing model rationales.

This should be presented as a documented methodological limitation, not hidden.

## Recommended public presentation

### Above the fold

Use a concise status framing:

> **Independent ground truth is now frozen.**  
> The study moved beyond measuring disagreement and established a blinded A/B/C oracle before running the comparative treatment.

Do not present outcome metrics yet.

### Main visual

Recommended diagram:

~~~mermaid
flowchart LR
    A[Frozen public-safe cases] --> B[Blinded adjudicator A]
    A --> C[Blinded adjudicator B]
    B --> D{Agreement?}
    C --> D
    D -->|yes| E[Provisional oracle]
    D -->|no| F[Dispute-only blinded C]
    F --> G{Two-of-three?}
    G -->|yes| E
    G -->|no| H[Recorded human resolution]
    H --> E
    E --> I[Frozen oracle]
    I --> J[Later post-inference scoring]
~~~

### Secondary visual

Show the study progression:

~~~text
instrumentation
     ->
disagreement measurement
     ->
independent correctness oracle
     ->
P1 evidence-path verification
     ->
P2 full comparative inference
     ->
P3 sanitized evidence
~~~

### Example case

A public-safe example may illustrate the oracle semantics, but do not expose private adjudication results.

A suitable example from the frozen authoring view is:

> "Identify which repository artifacts are suitable for a public case study and which should remain private."

Use it to explain that:

- the case prompt is the thing being labeled;
- metadata is evidence;
- semantic risk is the consequence of a materially wrong interpretation;
- `oracle_eligible` means the question is applicable, not that its answer is `true`.

Do not publish the private A/B/C votes or human final resolution unless a later publication decision explicitly sanitizes and approves them.

## Ordered source pack for website synthesis

Read in this order:

1. `docs/studies/routing-semantic-v1.md`  
   High-level study purpose, research questions, blinding, sample/statistical policy, publication policy.

2. `docs/studies/routing-semantic-v1-oracle-review-guide.md`  
   Human explanation of case fields, oracle questions, semantic-risk reasoning, and review boundaries.

3. `docs/studies/routing-semantic-v1-oracle-protocol.md`  
   Authoritative labeling/adjudication protocol.

4. `src/agent_workflow_comparative_eval/resources/studies/routing-semantic-v1.study.json`  
   Machine-readable study contract, metrics, evidence policy, exclusions, and frozen runtime identities.

5. `docs/checkpoints/2026-09-26-comparative-study-v4-checkpoint.md`  
   Current phase state and P0B-to-P1 handoff.

6. `docs/portfolio/COMPARATIVE_STUDY_PROGRESS.md`  
   Portfolio-facing architecture/status summary.

Supporting implementation evidence:

7. Agent-Workflow Benchmark `docs/COMPARATIVE_DECISION_STUDY.md`

8. Agent-Workflow Benchmark `docs/INSPECT_ORACLE_ADJUDICATION.md`

9. Agent-Workflow Benchmark `scripts/adjudication/README.md`

10. Agent-Workflow Benchmark `scripts/decision-study/README.md`

Use implementation documents to verify claims and reproducibility. Do not turn the public page into an operator runbook.

## Suggested synthesis instruction for the website agent

> Update the comparative-evaluation case study using the ordered source pack in this handoff. Preserve the distinction between completed oracle methodology and not-yet-run comparative outcome measurement. Lead with the evolution from measuring disagreement to establishing independent correctness. Explain blinded A/B/C adjudication, frozen-before-inference ground truth, recorded human resolution, evidence/privacy boundaries, and the staged P1/P2/P3 execution path. Use the methodological limitation about missing persisted adjudicator rationales as evidence of transparent study practice. Do not make any comparative performance claim until P2 data exists. Keep implementation commands below the fold or linked to GitHub rather than in the main narrative.

## Next website update trigger

After P1:

- update status to instrumentation smoke passed/failed;
- show evidence-path checks, but still no comparative-effectiveness claims.

After P2:

- replace placeholder outcome areas with actual correctness, calibration, disagreement, reliability, latency/token/cost, uncertainty, denominators, and exclusions;
- state conclusions only to the extent supported by the completed report.

After P3:

- link sanitized evidence and reproducibility artifacts.
