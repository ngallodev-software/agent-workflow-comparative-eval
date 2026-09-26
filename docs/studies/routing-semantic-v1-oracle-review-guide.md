# Routing Semantic v1 — Oracle Reviewer Guide

> **Status:** non-normative reviewer aid.  
> **Authority:** the frozen [oracle protocol](routing-semantic-v1-oracle-protocol.md) and machine-readable study specification remain authoritative. This guide explains how to read the existing frozen artifacts; it does not change labels, rubrics, or the study protocol.

## What the reviewer is doing

The independent oracle assigns ground-truth labels to three routing decisions using only the blinded case information and frozen rubric.

For each disputed seam, answer the applicable oracle question from the case prompt and supplied metadata. Do not use knowledge of the real repository, deployment pipeline, credentials, benchmark outputs, deterministic control, TypeSafe/Jev output, or other information that was not present in the frozen authoring view.

The independent oracle is intentionally separate from both implementations being compared.

## How to read one authoring-view case

A case looks conceptually like:

```json
{
  "case_id": "rsv1-050",
  "metadata": {
    "change_scope": "analysis-only",
    "environment": "repository",
    "requires_interaction": false,
    "risk": "low",
    "task_type": "coordination"
  },
  "oracle_eligible": {
    "routing.interaction_required": true,
    "routing.semantic_risk": true,
    "routing.task_class": true
  },
  "task": "Identify which repository artifacts are suitable for a public case study and which should remain private."
}
```

### `task`

This is the **verbatim request being labeled**. It is the primary evidence.

Do not silently replace it with knowledge of what a similarly worded request might mean in the real Agent-Workflow ecosystem.

### `metadata`

Metadata is **supplied context and evidence**, not an answer key.

Fields such as `task_type`, `requires_interaction`, and `risk` may be stale, incomplete, or intentionally misleading. The frozen protocol explicitly requires the adjudicator to apply the rubric rather than copy metadata values.

Examples:

- `"risk": "low"` is evidence, but it does not automatically mean `routing.semantic_risk = 0`.
- `"requires_interaction": false` is evidence, but it does not automatically mean `routing.interaction_required = false`.
- `"task_type": "coordination"` is evidence, but it does not automatically determine `routing.task_class`.

### `oracle_eligible`

This map answers only:

> **Which oracle questions require labels for this case?**

It does **not** contain the labels.

For example:

```json
"oracle_eligible": {
  "routing.interaction_required": true,
  "routing.semantic_risk": true,
  "routing.task_class": true
}
```

means all three seams must be labeled. It does not mean that the correct values for those seams are `true`.

### `decision_seams`

The top-level `decision_seams` array in the authoring view defines the allowed answer space and machine-readable meaning for each seam. It is the structured companion to the prose rubric in the frozen oracle protocol.

### `oracle_policy`

This records the frozen protocol identity and high-level oracle rules. It is not a per-case answer.

### `blinding`

The blinding object documents information intentionally excluded from adjudicators, including construction tags and control/candidate outputs.

If information was excluded by the blinding contract, it must not be reintroduced during human conflict resolution.

## The three oracle questions

### 1. `routing.task_class`

**Question:**

> What is the primary requested deliverable of this case?

Allowed labels:

- `implementation`
- `diagnosis`
- `review`
- `documentation`
- `other`

Use the frozen mixed-intent precedence in the oracle protocol. In particular, classify by the primary requested deliverable rather than the first verb.

### 2. `routing.interaction_required`

**Question:**

> Is a material user decision, authorization, or preference missing from the supplied state and required before the requested action can be completed responsibly?

Answer `true` or `false` under the frozen protocol.

This is not asking whether interaction would be convenient. It asks whether a material external choice or authorization is actually required.

### 3. `routing.semantic_risk`

**Question:**

> What is the consequence of acting on a materially wrong interpretation of this request?

This is **semantic consequence**, not generic code complexity.

| Level | Frozen meaning |
| ---: | --- |
| 0 | Low consequence. Local/easily reversible work; mostly small rework or documentation correction. |
| 1 | Moderate consequence. Meaningful wasted work, behavioral incompatibility, incorrect analysis, or a nontrivial but recoverable repository/system change. |
| 2 | High consequence. Production state, security/authorization, credentials, destructive/irreversible data, public claims, financial/billing behavior, or another high-impact boundary. |

### Public/private and deployment examples

The label depends on what the **case itself authorizes or requires**.

- A request to **identify or recommend** which artifacts might later be publishable can still be analysis-only. A wrong interpretation may be reviewable and reversible before publication.
- A request that **actually publishes, releases, exposes, or changes a public claim** crosses a higher-impact boundary.
- A request that explicitly involves credentials, secrets, destructive data, production state, privileged authorization, or an irreversible action can support level 2.
- Do not assume that a repository change is automatically deployed to production. If automated deployment is relevant, that fact must be supplied in the frozen case.
- Do not assume that an artifact contains credentials or secrets merely because the real repository may contain them. The case must provide that information.

When the supplied evidence does not distinguish these consequences well enough, an unresolved oracle conflict is preferable to importing outside knowledge.

## What to use during three-way conflict resolution

The frozen protocol requires recorded adjudication when A/B/C produce no majority.

Use only:

1. the verbatim case prompt;
2. the metadata supplied in that case;
3. the applicable frozen decision-seam rubric;
4. the independent A/B/C labels;
5. independent adjudicator rationales when they were preserved by the adjudication implementation.

Do not use:

- deterministic control output;
- TypeSafe/Jev output;
- probability/confidence evidence;
- construction tags;
- live repository contents not present in the case;
- private credentials or local-machine state;
- knowledge of which label would improve study metrics.

If the frozen evidence cannot support a defensible resolution, record the conflict as unresolved rather than inventing a label to preserve sample size.

## Important implementation note for the current P0B cohort

The frozen protocol says three-way discussion may use independent rationales. The current A/B/C Inspect output contract preserves labels but does **not** preserve adjudicator rationales; the adjudicator prompt explicitly requested labels-only JSON.

Therefore the current cohort's recorded human resolution has access to the case, supplied metadata, frozen rubric, and independent labels, but not the original adjudicators' rationales.

This is an implementation limitation that should be reported with the study. A future version of the adjudication contract should preserve concise independent rationales without exposing cross-adjudicator or treatment information.

Do not reconstruct or invent rationales for the completed A/B/C passes.

## Authoritative references

- [Routing Semantic v1 study overview](routing-semantic-v1.md) — purpose, blinding, sample policy, independent oracle handoff, and study identity.
- [Frozen independent oracle adjudication protocol](routing-semantic-v1-oracle-protocol.md) — authoritative label definitions, mixed-intent rules, semantic-risk rubric, and A/B/C adjudication procedure.
- [Machine-readable study specification](../../src/agent_workflow_comparative_eval/resources/studies/routing-semantic-v1.study.json) — exact decision-seam contracts, research questions, oracle policy, evidence policy, and exclusions.
- [Oracle authoring-view schema](../../src/agent_workflow_comparative_eval/schemas/oracle-authoring-view.schema.json) — structural contract for the blinded adjudicator artifact.
- [Decision-study case schema](../../src/agent_workflow_comparative_eval/schemas/decision-study-case.schema.json) — structural definition of `task`, `metadata`, and `oracle_eligible`.
- [Frozen oracle authoring view](artifacts/routing-semantic-v1/oracle-authoring-view.json) — exact 120-case blinded artifact used by A/B.

The frozen authoring-view bytes must not be edited to improve reviewer usability. Human-facing review tools should render clearer questions and explanations around the frozen artifact instead.
