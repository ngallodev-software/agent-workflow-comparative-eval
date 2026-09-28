# Routing Semantic v2 — Methodological Replication

**Status:** design/implementation; not frozen  
**Study version:** `2.0.0-draft.2`  
**Relationship to v1:** new study identity; v1 remains immutable and published

## Purpose

`routing-semantic-v2` repairs the evidence-contract failures found during v1 before another real oracle cohort is run.

The first v2 cohort is intentionally a **methodological replication**, not a new task-domain claim. It is intended to reuse the exact 120 v1 case meanings under a new dataset identity so we can measure how much a rationale-complete oracle changes ground truth and whether the published v1 conclusions are stable.

## Adjudicator-model control

The methodological replication keeps the adjudicator model path matched to v1:

- model: `deepseek-flash`;
- provider path: `openai-api/codex-lb/deepseek-flash`;
- request mode: Responses API;
- no new reasoning-effort override.

This isolates the v2 evidence-contract changes from an adjudicator-model change. GPT-6 Luna is used only by the separate agent-directed Jev pilot.

## Required differences from v1

Every eligible A/B/C label must include a compact structured justification:

~~~json
{
  "label": 1,
  "justification": {
    "decisive_case_evidence": [
      "The request prepares an internal artifact and does not itself publish or mutate production state."
    ],
    "rubric_rule": "Moderate consequence when a wrong interpretation causes meaningful but recoverable downstream work.",
    "ambiguity": "none"
  }
}
~~~

The justification is authoritative evidence. Provider reasoning summaries are optional private execution evidence only.

Usage provenance must separate:

- final-output usage;
- aggregate multi-call session usage;
- provider request count;
- model call count.

## Qualification additions

Before any real v2 labels:

- **IA-9:** structured justification round-trip;
- **IA-10:** usage/provenance scope reconciliation;
- **IA-11:** optional reasoning-summary capability observation.

A real v2 cohort must not begin until IA-1 through IA-11 pass.

## What gets rerun

The oracle/adjudication process gets rerun against the same case content under a new v2 dataset/study identity.

The candidate/control inference should **not** automatically be rerun merely because the oracle machinery changed. First compare v1 and v2 oracle labels. If the v2 oracle changes enough labels to affect published conclusions, then rerun/re-score under a preregistered replication plan.

## Claim boundary

A v2 oracle replication can establish:

- label stability or instability;
- rationale completeness;
- disagreement mechanisms;
- provenance-accounting correctness.

It is not automatically a second independent effectiveness replication because the case content is reused.
