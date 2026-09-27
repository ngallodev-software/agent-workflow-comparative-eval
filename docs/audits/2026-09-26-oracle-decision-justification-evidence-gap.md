# Comparative Evaluation Methodological Postmortem — Missing Adjudicator Decision Justifications

**Date:** 2026-09-26  
**Study:** `routing-semantic-v1`  
**Classification:** experimental-design limitation / evidence-retention failure  
**Status:** documented after oracle freeze; frozen v1 oracle is not retroactively altered

## Executive summary

The first `routing-semantic-v1` oracle cohort successfully preserved independent adjudicator **labels**, but it did not preserve the adjudicators' original **decision justifications**. The frozen oracle protocol anticipated that genuine three-way conflicts could be resolved using the case, frozen rubric, and independent rationales. The implemented Inspect output contract instead requested labels-only JSON.

This is not a loss of the oracle labels themselves. A/B labels were retained, C labels were retained where required, and the final frozen oracle was produced and validated before comparative inference. The failure is that the evidence chain cannot now answer an important second-order question:

> **Why did an adjudicator choose that label, and why did adjudicators disagree?**

That distinction matters. A comparative study can still score candidate/control decisions against the frozen labels, but it cannot retrospectively decompose oracle disagreement into rubric ambiguity, differing interpretation of supplied evidence, boundary-case judgment, or adjudicator reasoning error with the fidelity originally intended.

The correct response is not to reconstruct missing rationales after the fact. Doing so would create post-hoc evidence and contaminate the historical record. The v1 limitation must remain explicit, while a future adjudication contract should require concise, structured decision justifications at the time each independent label is produced.

## What the frozen protocol intended

The frozen oracle protocol defines three independent decision seams across a 120-case public-safe corpus:

- `routing.task_class` — five-class categorical decision;
- `routing.interaction_required` — binary decision;
- `routing.semantic_risk` — ordinal 0–2 consequence decision.

A and B independently label eligible seams without seeing treatment outputs or each other's labels. Disagreements are sent to C. Two-of-three agreement resolves a disputed seam. When all three categorical labels differ, or risk produces the 0/1/2 pattern, the protocol requires recorded adjudication using the case, frozen rubric, and independent rationales.

The protocol also says the adjudication record should preserve independent labels, resolution method, and a concise rationale for resolved disagreements.

## What the implementation actually retained

The completed Inspect cohort persisted the independent labels but not the original adjudicator rationales because the adjudicator output contract requested labels-only JSON.

Consequently, human resolution of genuine three-way conflicts had access to:

1. the verbatim frozen case prompt;
2. supplied frozen metadata;
3. the frozen decision-seam rubric;
4. the independent A/B/C labels.

It did **not** have the original explanation each model used to arrive at its label.

This means the study retained the **decision outcome** but discarded a material part of the intended **decision provenance**.

## Why this is a methodological failure

### 1. Disagreement became observable but not fully diagnosable

A/B/C label differences tell us **that** adjudicators disagreed. They do not tell us **why**.

Without contemporaneous justifications, a disagreement cannot reliably be classified after the fact as:

- a genuinely ambiguous task;
- a rubric-definition ambiguity;
- different weighting of supplied metadata versus task text;
- a mixed-intent precedence interpretation;
- a semantic-risk boundary disagreement;
- a missed authorization/publication/security cue;
- a simple labeling/reasoning error.

Those are materially different failure modes. They imply different corrective actions.

### 2. Human adjudication lost information the protocol expected it to use

The frozen protocol explicitly envisioned independent rationales as evidence during genuine three-way conflict resolution. Because those rationales were not retained, the human resolver operated with a reduced evidence set.

This does not justify changing the frozen oracle now. It does mean the actual implementation was weaker than the intended protocol at this point and the limitation belongs in the study record.

### 3. The study cannot audit adjudicator reasoning fidelity after freeze

After the oracle is frozen, we can inspect the labels and final resolution records, but we cannot test whether an adjudicator:

- applied the primary-deliverable rule correctly;
- copied or over-weighted stale metadata;
- confused convenience with required interaction;
- treated generic complexity as semantic consequence;
- imported facts outside the blinded authoring view.

The reviewer guide warns against all of these behaviors. Without contemporaneous justification evidence, compliance can only be inferred from labels, not audited directly.

### 4. The evidence is insufficient for a useful error taxonomy

One of the most valuable outputs of a comparative evaluation is not merely a winner/loser count. It is a map of **where decisions fail and why**.

The missing justifications prevent a defensible retrospective taxonomy of oracle disagreement mechanisms. Any such taxonomy built now would require new interpretation by the researcher and would no longer represent the independent adjudicators' original reasoning.

### 5. It reduces reproducibility of the adjudication process

Another qualified adjudicator can reproduce the rubric and produce new labels, but cannot reproduce the historical path from the original evidence to the original labels because part of that path was never persisted.

Reproducibility therefore exists at the artifact/protocol/label level, but not at the original decision-justification level.

## What this failure does **not** mean

The limitation should not be overstated.

It does **not** mean:

- the 120-case corpus was lost;
- A/B/C labels were discarded;
- the oracle was exposed to candidate/control outputs;
- the oracle was frozen after treatment inference;
- the P1 instrumentation smoke is invalid;
- the final oracle must be rewritten;
- missing rationales should be regenerated.

The independent oracle remains the frozen v1 scoring authority under the procedure actually executed. The limitation constrains interpretation of adjudicator disagreement and the strength of provenance available for the most difficult oracle cases.

## Public-surfaceable quantitative context

The following figures are already durable and safe to surface with their scope intact.

| Metric | Public value | Correct interpretation |
| --- | ---: | --- |
| Frozen corpus | **120 cases** | Public-safe study corpus used for oracle construction and planned P2 inference |
| Decision seams | **3** | task class, interaction required, semantic risk |
| Oracle-construction API cost through freeze | **$0.07 USD** | P0A/P0B qualification + adjudication accounting only |
| Oracle-construction API requests through freeze | **36** | DeepSeek-4.1-Flash API requests via Codex harness -> `codex-lb` |
| Oracle-construction tokens through freeze | **726,263** | Aggregate provider/API accounting; no input/output split supplied |
| P1 development smoke cases | **8** | Instrumentation validation only; not comparative-effectiveness evidence |
| P1 per-seam observations | **24** | Three observations per observed smoke case |
| P1 provider requests | **8** | One request per observed smoke case |
| P1 exclusions | **0** | Bounded smoke evidence only |

The API accounting above must not be presented as Jev treatment cost or as comparative efficiency. P1 counts must not be presented as evidence that either decision arm is more correct.

No public count of A/B disagreements, C adjudications, or genuine three-way conflicts is asserted here because the currently public repository artifacts inspected for this postmortem do not provide a defensible sanitized aggregate for those quantities. They should be added later only from an approved, reproducible evidence artifact.

## Root cause

The immediate root cause was a mismatch between **protocol semantics** and **output-schema semantics**.

The protocol treated rationales as part of the evidence available for difficult adjudication. The execution contract optimized the model response down to labels-only JSON. Because the run pipeline preserved what the output contract emitted, the missing field became an irreversible evidence gap once the independent passes completed.

The broader process failure was that preflight qualification validated whether the adjudicator could produce valid labels, but did not fail closed on whether **all evidence required by downstream adjudication and analysis** was persisted.

In other words:

```text
protocol requirement
      |
      v
independent label + justification
      |
      X   output contract retained label only
      |
      v
frozen historical record
```

The system validated answer shape more strongly than evidence completeness.

## Corrective design for the next study version

A future oracle/adjudication contract should require a compact structured justification for every independently produced label. This should be an auditable decision explanation, **not unrestricted hidden chain-of-thought**.

A suitable record can include:

```json
{
  "label": "review",
  "justification": {
    "decisive_case_evidence": [
      "requested final deliverable is an assessment of an existing artifact"
    ],
    "rubric_rule": "review takes precedence when the final deliverable is an assessment and no implementation change is required",
    "ambiguity": "none",
    "confidence": "high"
  }
}
```

For semantic risk, the justification should identify the consequence boundary relied upon. For interaction-required, it should identify the missing material decision/authorization if true, or why supplied state is sufficient if false.

The schema should bound justification length and prohibit treatment/control information.

### Required safeguards

The next version should fail qualification unless all of the following hold:

1. every eligible label has a non-empty structured justification;
2. the justification is produced in the same independent pass as the label;
3. A cannot see B; B cannot see A; C cannot see A/B labels or rationales before producing its own decision;
4. treatment/control outputs remain absent;
5. justification fields survive persistence and export;
6. three-way adjudication tooling renders the independent justifications without silently merging them;
7. the final record identifies whether majority or discussion resolved the seam;
8. unresolved conflicts remain unresolved rather than being forced to preserve sample size;
9. sanitized publication rules explicitly define whether justifications are public, summarized, or private;
10. a preflight fixture proves round-trip persistence before real adjudication begins.

## New metrics enabled by preserving decision justifications

These should be considered for the next version, with metric definitions frozen before outcomes are observed:

- **rationale retention rate:** eligible labels with a valid persisted justification / eligible labels produced;
- **rubric-rule attribution distribution:** which frozen rules drive decisions;
- **ambiguity declaration rate:** fraction of decisions explicitly identifying ambiguity;
- **disagreement-cause taxonomy:** disagreement attributed to task ambiguity, metadata interpretation, rubric boundary, or apparent adjudicator error, with an explicit coding protocol;
- **resolution evidence completeness:** three-way conflicts for which all independent justifications were available to the resolver;
- **label/justification consistency audit:** whether the stated decisive evidence and rubric rule support the emitted label under a separately defined audit procedure.

These are diagnostic metrics. They should not be quietly folded into correctness scoring without a separately frozen contract.

## Required process change

The central process change is:

> **Evidence requirements must be tested end-to-end before an expensive or irreversible evaluation cohort begins.**

For each planned analysis, the study specification should name the exact source field required, the producer of that field, the persistence layer that retains it, and a preflight assertion proving it survives into the final evidence bundle.

This extends the existing project rule that every metric must identify its question, required data, source, capture status, oracle dependency, sample-size limits, and public reporting policy.

## Treatment of the existing v1 cohort

The completed v1 adjudication should remain immutable.

Do not:

- rerun A/B/C and pretend the new explanations are historical;
- infer rationales from labels;
- use treatment outputs to explain oracle decisions;
- revise the frozen oracle to make its provenance look more complete;
- hide the limitation from public methodology notes.

Do:

- retain the frozen oracle;
- disclose that original independent rationales were not persisted;
- bound claims about disagreement analysis accordingly;
- preserve any actual human resolution rationale that was recorded;
- version the corrected evidence contract for a subsequent study/adjudication cohort.

## Portfolio significance

This failure is useful to surface because it shows the comparative-evaluation project moving from **result collection** toward **evidence engineering**.

The important lesson is not that an LLM should emit more prose. It is that an evaluation system must preserve enough structured provenance to explain the decisions it later treats as ground truth.

The progression is:

```text
measure outputs
    ->
measure disagreement
    ->
build independent ground truth
    ->
discover missing decision provenance
    ->
make evidence completeness a preflight invariant
```

That is a stronger and more accurate description of the work than presenting the oracle freeze as an unqualified endpoint.

## Claim boundary

Safe public statement:

> The first frozen oracle retained independent labels but not the adjudicators' original decision justifications. That limited retrospective analysis of why adjudicators disagreed and reduced the evidence available during genuine three-way conflict resolution. The frozen v1 oracle is preserved as executed; the corrective design is to require compact structured justifications and verify their end-to-end persistence before future cohorts run.

Do not state that the oracle is invalid or that comparative results are known to be wrong. The documented failure concerns evidence completeness and adjudication provenance, not demonstrated label incorrectness.
