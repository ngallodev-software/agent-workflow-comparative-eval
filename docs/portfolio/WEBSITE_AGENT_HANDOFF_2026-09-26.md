# Website Agent Handoff — Comparative Evaluation After Oracle Freeze

**Date:** 2026-09-26  
**Audience:** portfolio / website synthesis agent  
**Purpose:** update the public-facing case-study narrative after completion of P0A/P0B/P1 and the full P2 run, while keeping private P2 outcome metrics behind the P3 publication-review boundary.

## Current authoritative state

The routing-semantic comparative study has advanced materially since the earlier portfolio notes.

Completed:

- P0A authenticated adjudicator qualification;
- IA-1 through IA-8 qualification gates;
- independent blinded A/B oracle adjudication;
- disagreement-only C adjudication;
- recorded human resolution of genuine three-way conflicts;
- oracle freeze;
- final oracle validation against the frozen 120-case corpus;
- P1 bounded live TypeSafe/Jev instrumentation smoke;
- P1 persisted-evidence verification.

The qualified adjudicator path for the completed cohort was:

`openai-api/codex-lb/deepseek-flash`

Execution provenance for these oracle-construction runs is:

`OpenAI Codex harness -> codex-lb load balancer -> DeepSeek-4.1-Flash API`

The routed runtime alias remained `openai-api/codex-lb/deepseek-flash`; `DeepSeek-4.1-Flash` is the provider/model identity used for the API accounting record.

Cumulative provider/API accounting for the initial qualification/adjudication runs through and including P0B oracle freeze:

- cost: **$0.07 USD**;
- API requests: **36**;
- tokens: **726,263**.

This accounting is scoped to oracle-baseline construction through freeze. It excludes P1 TypeSafe/Jev smoke traffic, P2 comparative inference, and P3 publication work. The figures are operator-recorded provider/API metrics and are not reconstructed from committed raw billing traffic. See `docs/evidence/oracle-baseline-api-usage-2026-09-26.md` and its JSON companion.

The independent oracle is now frozen and available privately for later post-inference joining.

P1 verification evidence:

- 8 deterministic smoke cases;
- 8 observed cases;
- 8 provider requests;
- 24 per-seam observations;
- 0 exclusions;
- one provider request per observed case;
- three observations per observed case;
- unique request IDs;
- semantic probability evidence persisted;
- oracle absent during inference;
- privacy boundary preserved;
- request-level usage not triple-counted;
- question set `routing/v2`;
- projector `routing-state/v2`;
- verification status: `pass`.

P2 completion evidence now available privately:

- 120 frozen cases;
- 360 per-seam observations;
- 120 provider requests;
- 0 exclusions;
- post-inference join to the already frozen oracle;
- study eligibility: pass;
- correctness/calibration/reliability/efficiency report generated.

Not yet completed:

- P3 sanitized public evidence publication/review.

Therefore **do not move private P2 outcome metrics or winner language onto the website until the P3 publication boundary is reviewed and approved**.

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
- cumulative oracle-baseline API accounting through freeze was $0.07 USD across 36 DeepSeek-4.1-Flash API requests and 726,263 tokens, routed via the OpenAI Codex harness and `codex-lb`;
- the bounded live instrumentation smoke passed before the preregistered full run;
- P1 verified the intended request/observation/accounting/privacy evidence chain on 8 development-only cases with 0 exclusions;
- P2 full inference and reporting are complete on the private evidence path;
- a favorable semantic result is not required for publication.

Do not expose private A/B/C adjudication artifacts, credentials, raw provider traffic, or private host paths.

## Claims that remain prohibited until P3 publication review

Do not say or imply:

- TypeSafe/Jev improves routing correctness;
- TypeSafe/Jev reduces errors;
- semantic routing is more accurate than deterministic routing;
- one arm "won";
- latency/cost overhead is acceptable or superior;
- calibration is good;
- the confidence policy is validated;
- the private P2 report may be copied verbatim to the public site.

The full study has now run, but outcome claims still require sanitized P3 evidence review before public rendering.

## Current execution phase map

~~~text
P0A  authenticated adjudicator qualification      COMPLETE
P0B  independent oracle freeze + validation       COMPLETE
P1   bounded live instrumentation smoke           PASS — 8 cases / 24 observations / 8 requests / 0 exclusions
P2   full 120-case comparative study              COMPLETE — 120 cases / 360 observations / 120 requests / 0 exclusions
P3   sanitized publication                        NEXT
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

The normal P1 operator entry point was:

~~~bash
bash scripts/decision-study/p1-all.sh
~~~

P1 deterministically derived a small development-only subset from the exact frozen corpus and recorded the source corpus hash + selected case IDs. The completed smoke verified the live evidence chain and unblocked P2.

P1 is **development evidence only**. It verifies instrumentation and evidence integrity; it does not establish comparative effectiveness.

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

## Known limitation discovered during P0B — corrected after private-log audit

The frozen protocol envisioned using independent adjudicator rationales during genuine three-way discussion.

The authoritative Inspect pass persisted labels but no structured rationales because the output contract requested labels-only JSON. The original human-resolution workflow therefore used only the frozen case prompt, supplied metadata, frozen rubric, and A/B/C labels.

A later audit of the retained private Inspect `.eval` logs found contemporaneous provider reasoning summaries for A/B/C. Those summaries were supplementary execution evidence, not part of `adjudication.json`, and were not available to the resolver at the time.

Do not retrofit those summaries into the frozen oracle. Future cohorts should require provider-neutral structured justifications and verify their complete round-trip before real adjudication.

See `docs/audits/2026-09-27-oracle-reasoning-summary-retention-audit.md`.

## Recommended public presentation

### Above the fold

Use a concise status framing:

> **Independent ground truth was frozen before treatment inference, and the full 120-case comparative run has now completed.**  
> The study progressed through oracle construction, bounded evidence-path validation, and full P2 inference/reporting without exposing the oracle during inference.

It is safe to show the methodological milestones and P2 execution counts. Keep correctness/calibration/latency/cost outcome claims behind the P3 sanitized-publication review until approved.

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
P1 evidence-path verification [PASSED]
     ->
P2 full comparative inference [COMPLETE]
     ->
P3 sanitized evidence [NEXT]
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

5. `docs/checkpoints/2026-09-27-comparative-study-v6-checkpoint.md`  
   Current phase state: P2 complete, P3 publication review next, plus reasoning-summary audit correction.

6. `docs/checkpoints/2026-09-26-comparative-study-v5-checkpoint.md`  
   Historical P1-to-P2 handoff retained for chronology.

7. `docs/checkpoints/2026-09-26-comparative-study-v4-checkpoint.md`  
   Historical P0B-to-P1 handoff retained for chronology.

8. `docs/portfolio/COMPARATIVE_STUDY_PROGRESS.md`  
   Portfolio-facing architecture/status summary.

9. `docs/evidence/oracle-baseline-api-usage-2026-09-26.md`  
   Durable P0A/P0B execution provenance and cumulative DeepSeek-4.1-Flash provider/API accounting through oracle freeze. The adjacent JSON file is the machine-readable companion.

Supporting implementation evidence:

10. `docs/audits/2026-09-27-oracle-reasoning-summary-retention-audit.md`

11. Agent-Workflow Benchmark `docs/COMPARATIVE_DECISION_STUDY.md`

12. Agent-Workflow Benchmark `docs/INSPECT_ORACLE_ADJUDICATION.md`

13. Agent-Workflow Benchmark `scripts/adjudication/README.md`

14. Agent-Workflow Benchmark `scripts/decision-study/README.md`

Use implementation documents to verify claims and reproducibility. Do not turn the public page into an operator runbook.

## Suggested synthesis instruction for the website agent

> Update the comparative-evaluation case study using the ordered source pack in this handoff. P0A/P0B/P1/P2 are complete; P3 sanitized-publication review is next. Lead with the evolution from measuring disagreement to establishing independent correctness, then show that the live evidence path was smoke-tested before the full 120-case run. Explain blinded A/B/C adjudication, frozen-before-inference ground truth, recorded human resolution, evidence/privacy boundaries, and the staged execution path. Correctly describe the provenance limitation: structured rationales were absent from the authoritative adjudication pass, while a later audit found provider reasoning summaries retained in private Inspect logs outside the original human-resolution workflow. Do not publish private reasoning-summary text or private P2 outcome metrics until the P3 public-evidence boundary is reviewed. Keep implementation commands below the fold or linked to GitHub rather than in the main narrative.

## Next website update trigger

P2 is complete privately. Do not populate public outcome areas directly from the private report.

After P3 publication review:

- link sanitized evidence and reproducibility artifacts.
