# Website Editor Handoff — Oracle Decision-Provenance Gap

**Date:** 2026-09-26  
**Audience:** portfolio / website editor  
**Source postmortem:** `docs/audits/2026-09-26-oracle-decision-justification-evidence-gap.md`

## Purpose

Add a dated methodology/timeline update explaining a failure discovered after the first independent oracle cohort: the study retained A/B/C labels but did not retain the adjudicators' original decision justifications.

This should be presented as an evidence-engineering lesson and a limitation of the completed v1 adjudication, not as evidence that the oracle labels are wrong.

## Recommended timeline entry

**2026-09-26 — Oracle evidence-retention gap identified**

After freezing the first independent oracle, review found that the execution contract had persisted adjudicator labels but not the concise reasoning/decision justification anticipated by the frozen protocol for difficult three-way conflicts. The frozen oracle remains intact, but the missing provenance limits retrospective analysis of *why* adjudicators disagreed. The next study version will make structured decision justification and round-trip persistence a preflight invariant.

## Recommended case-study treatment

Place this after the oracle-freeze milestone and before any later full comparative-results milestone.

Suggested narrative:

> Freezing independent ground truth exposed a second-order problem: a label is enough to score a decision, but not enough to explain the failure mode behind a disagreement. The first adjudication cohort preserved the votes while its labels-only output contract discarded the adjudicators' original decision justifications. Rather than reconstruct explanations after the fact, the study records the limitation and changes the next evaluation contract: every independent decision must carry a compact structured justification whose persistence is verified before the cohort runs.

Emphasize that this was discovered through review of the evidence chain itself.

## Public metrics that may accompany the entry

Use only with scope labels:

- **120** frozen public-safe cases;
- **3** evaluated routing seams;
- **36** DeepSeek-4.1-Flash API requests through oracle freeze;
- **726,263** tokens through oracle freeze;
- **$0.07 USD** provider/API cost through oracle freeze;
- later P1 smoke: **8 cases / 24 observations / 8 requests / 0 exclusions**.

The 36 / 726,263 / $0.07 figures are oracle-construction accounting through P0B freeze via:

`OpenAI Codex harness -> codex-lb -> DeepSeek-4.1-Flash API`

They exclude P1/P2/P3 and are not Jev treatment cost.

The P1 figures validate the live evidence path only. They are not comparative-effectiveness results.

Do **not** publish counts of A/B disagreement, C adjudications, or three-way conflicts unless a later sanitized evidence artifact establishes those counts reproducibly.

## Visual suggestion

A small evidence-chain diagram is appropriate:

```text
Frozen case
   |
   +--> A: label + intended justification
   +--> B: label + intended justification
                    |
                    v
              persisted record
              labels: YES
              justifications: NO   <-- discovered gap
                    |
                    v
        corrective contract for next cohort
        structured justification + persistence check
```

Avoid depicting private chain-of-thought. Use terms such as **decision justification**, **decision provenance**, **decisive evidence**, and **rubric rule applied**.

## Claim boundaries

Safe:

- the labels were retained;
- the original independent decision justifications were not;
- the frozen protocol anticipated rationales for genuine three-way resolution;
- the human resolution therefore had a reduced evidence set;
- the gap limits retrospective disagreement diagnosis and reasoning-provenance audit;
- the frozen v1 oracle is not being rewritten;
- future cohorts should require structured justifications and verify persistence before adjudication.

Do not say:

- the oracle is invalid;
- the labels are known to be wrong;
- missing rationales can be regenerated faithfully;
- the study captured model chain-of-thought;
- the API accounting measures Jev efficiency;
- either comparative arm won.

## Link target

The website should link the methodology/timeline entry to:

`docs/audits/2026-09-26-oracle-decision-justification-evidence-gap.md`

The detailed postmortem contains the failure definition, impact analysis, corrective schema direction, future diagnostic metrics, and public claim boundary.

## Relationship to existing website handoff

This handoff supplements `docs/portfolio/WEBSITE_AGENT_HANDOFF_2026-09-26.md`.

The earlier handoff already notes the missing-rationale limitation. This new document gives the website editor a focused narrative and direct link target so the limitation can be treated as a first-class dated study milestone rather than a footnote.
