# Routing Semantic v1 — Independent Oracle Adjudication Protocol

**Study:** routing-semantic-v1  
**Corpus:** routing-semantic-corpus-v1.0.0  
**Case count:** 120  
**Status:** frozen before live comparative inference

## Adjudicator input

Adjudicators receive only the output of oracle_authoring_view().

They may see:

- case ID;
- request text;
- declared routing metadata;
- the frozen task-class taxonomy;
- the frozen semantic-risk rubric;
- oracle eligibility and this adjudication protocol.

They must not see:

- corpus construction tags/strata;
- deterministic routing outputs;
- TypeSafe/Jev outputs;
- probability or confidence evidence;
- comparison reports;
- earlier benchmark qualification outcomes.

## Label 1: routing.task_class

Choose exactly one label:

| Label | Meaning |
| --- | --- |
| implementation | The primary requested outcome is to create or modify executable behavior, code, configuration, data transformation, tests as part of a change, or another implementation artifact. |
| diagnosis | The primary requested outcome is to investigate, trace, explain, or determine the cause/state of a problem without a required implementation change. |
| review | The primary requested outcome is to evaluate an existing or proposed artifact for defects, security, correctness, compatibility, compliance, or readiness. |
| documentation | The primary requested outcome is explanatory/reference/runbook/release-note/documentation content rather than executable behavior. |
| other | The primary requested outcome is planning, coordination, prioritization, handoff, organization, or another activity not captured above. |

### Mixed-intent rule

Classify by the **primary requested deliverable**, not the first verb.

Use these fixed precedence rules when the request genuinely combines activities:

1. If the task explicitly requires making a code/config/behavior change, classify as implementation, even if investigation or review is a prerequisite.
2. Otherwise, if the requested final deliverable is an assessment/audit/verdict on an artifact, classify as review.
3. Otherwise, if the requested final deliverable is root-cause/state understanding, classify as diagnosis.
4. Otherwise, if the requested final deliverable is documentation, classify as documentation.
5. Otherwise classify as other.

Do not use the declared task_type metadata as an oracle label. Treat it as observed evidence that may be stale or wrong.

## Label 2: routing.interaction_required

Choose true only when a **material user decision, authorization, or preference is missing from the supplied state and is required before the requested action can be completed responsibly**.

Typical true cases include:

- choosing between materially incompatible product/API behaviors;
- authorizing production/public/irreversible action when authorization is not already present;
- selecting an effective date, authoritative source, or policy choice that changes external behavior;
- approving publication/claim language when publication itself is requested.

Choose false when:

- the request is analysis/review/preparation only;
- authorization or the relevant policy decision is already explicitly supplied;
- an implementation detail can be resolved from repository evidence or normal engineering judgment without changing product policy;
- the task can safely proceed to a bounded artifact without an external user choice.

A stale requires_interaction metadata flag is evidence, not ground truth.

## Label 3: routing.semantic_risk

Label the **consequence of acting on a materially wrong interpretation of this request**, not generic code complexity.

| Level | Meaning |
| ---: | --- |
| 0 | Low consequence. Local/easily reversible work; a wrong interpretation would mainly cause small rework or documentation correction. |
| 1 | Moderate consequence. A wrong interpretation could cause meaningful wasted work, behavioral incompatibility, incorrect analysis, or a nontrivial but recoverable repository/system change. |
| 2 | High consequence. A wrong interpretation could affect production state, security/authorization, credentials, destructive/irreversible data, public claims, financial/billing behavior, or another high-impact boundary. |

Risk is semantic consequence only. Do not substitute deterministic security checks or lifecycle authority for this label.

## Independent adjudication procedure

1. Freeze and hash the 120-case inference corpus.
2. Export the blinded oracle-authoring view.
3. Adjudicator A labels all three seams for every eligible case independently.
4. Adjudicator B labels all three seams for every eligible case independently and without seeing A's labels.
5. Compare A/B labels only after both complete their independent pass.
6. Exact agreements become provisional oracle labels.
7. Every disagreement is sent to Adjudicator C, who independently labels the disputed seam without seeing treatment outputs.
8. If two of three independent labels agree, that majority label becomes the provisional oracle label.
9. If all three disagree on a categorical seam, or the three ordinal risk labels are 0/1/2, conduct a recorded adjudication discussion using only the case, frozen rubric, and independent rationales.
10. If a conflict cannot be resolved under the frozen rubric, mark it oracle_conflict_unresolved; do not invent a label to preserve sample size.
11. Freeze the final oracle bundle and its SHA-256 **before live comparative inference begins**.
12. The inference runner receives the corpus only. The frozen oracle is first loaded during post-inference reporting.

## Adjudication record

Each final oracle record should preserve, under its free-form provenance / adjudication objects:

- adjudicator identifiers or pseudonyms;
- independent A/B labels;
- C label when required;
- whether majority or discussion resolved the case;
- concise rationale for resolved disagreements;
- adjudication timestamp;
- protocol version;
- final freeze identity.

Do not include candidate/control outputs in the oracle provenance.

## Quality checks before freeze

The oracle bundle must pass:

- all case IDs belong to the frozen corpus;
- no duplicate case IDs;
- matching dataset version;
- every oracle-eligible seam has a label unless explicitly unresolved;
- only the frozen task-class labels are used;
- semantic-risk labels are integers 0–2;
- the bundle is marked frozen: true;
- the oracle hash is recorded independently of the inference run.

The study remains valid if the final oracle causes Jev/TypeSafe to outperform, match, or underperform deterministic control. The adjudication protocol is not changed in response to study outcomes.
