# Routing Semantic v2 — Adjudication Evidence Contract Plan

**Date:** 2026-09-27  
**Status:** design follow-up; not part of frozen `routing-semantic-v1`  
**Purpose:** prevent the evidence-retention and provenance-scope failures discovered during the v1 oracle cohort.

## Non-goal

This document does **not** alter:

- `routing-semantic-v1`;
- `routing-semantic-corpus-v1.0.0`;
- `routing-semantic-oracle-v1.0.0`;
- the frozen v1 labels;
- the completed P2 study.

Any implementation derived from this plan must use new versioned schemas/protocol identities.

## Failure modes to correct

The v1 cohort established two distinct evidence-contract failures.

### 1. Structured rationale was absent from the authoritative pass

The actual A/B/C runtime produced provider/model reasoning summaries that survived in private Inspect logs.

However:

- the adjudicator prompt explicitly requested labels-only JSON;
- `adjudication.json` retained `case_id + labels`;
- human dispute resolution did not receive the retained reasoning summaries;
- the frozen oracle therefore has no authoritative per-decision structured rationale from each independent adjudicator.

The v2 fix must not depend on provider chain-of-thought or reasoning-summary availability.

### 2. Usage scope was ambiguous

Per-role provenance persisted final sample-output usage rather than aggregate multi-call session/model usage.

The resulting field was technically valid but semantically narrower than a reader could reasonably infer.

v2 must make usage scope explicit and preserve both scopes when available.

## Core design principle

> Every evidence item required by downstream adjudication, analysis, or publication must be named in the protocol, produced intentionally, preserved by a versioned schema, and exercised by a preflight round-trip assertion.

## Authoritative rationale contract

Every independently produced eligible label should include a compact structured justification.

Conceptual shape:

~~~json
{
  "case_id": "rsv2-001",
  "decisions": {
    "routing.semantic_risk": {
      "label": 1,
      "justification": {
        "decisive_case_evidence": [
          "the request changes repository behavior but does not directly cross a production/publication boundary"
        ],
        "rubric_rule": "moderate consequence: nontrivial but recoverable repository/system change",
        "ambiguity": "none"
      }
    }
  }
}
~~~

### Required fields

For every eligible decision:

- `label`;
- at least one bounded `decisive_case_evidence` item;
- one frozen-rubric rule identifier or normalized rule text;
- an explicit ambiguity state.

### Optional fields

If preregistered:

- bounded confidence category;
- secondary evidence;
- explicit competing interpretation.

Do not add free-form hidden-chain-of-thought requirements.

## Provider reasoning summaries

Provider/model reasoning summaries may be retained as **supplementary private execution evidence** when the runtime supports them.

They are not the authoritative rationale.

The study must remain valid if:

- the provider does not support summaries;
- the provider changes summary formatting;
- the harness suppresses summaries;
- summary capture fails while the structured rationale succeeds.

Runtime qualification should record summary capability separately from rationale-contract compliance.

## Independence rules

The v2 rationale contract must preserve the same independence boundary as v1:

- A cannot see B;
- B cannot see A;
- C cannot see A/B labels or justifications before producing its own decision;
- treatment/control outputs remain unavailable;
- construction tags remain unavailable unless deliberately part of a new frozen design;
- human resolution receives independent labels + structured justifications only after independent passes complete.

## Pass schema

Introduce a new adjudication-pass schema rather than weakening v1.

Suggested identity:

`agent-workflow-benchmark/decision-study-adjudication-pass/v2`

Each record should preserve, per decision seam:

- label;
- structured justification;
- decision timestamp if meaningful;
- optional supplementary reasoning-summary reference/hash, never the private text in a public-safe pass.

The v2 wrapper must reject labels that lack required justification fields.

## Dispute view and C

C's blinded dispute input should continue to include only:

- disputed case text;
- supplied metadata;
- frozen rubric/decision schema;
- disputed decision IDs.

It should not contain:

- A/B labels;
- A/B structured justifications;
- A/B reasoning summaries;
- treatment/control outputs.

Only after C completes should the resolution renderer assemble A/B/C labels and structured justifications for human review.

## Human-resolution artifact

The resolution worksheet should render:

1. verbatim case;
2. supplied metadata;
3. frozen rubric;
4. A label + structured justification;
5. B label + structured justification;
6. C label + structured justification;
7. human final status/label;
8. human rationale;
9. participants;
10. whether any supplementary reasoning summaries exist privately.

The human resolver must never be forced to use provider reasoning summaries.

## Usage/provenance contract

Provenance should distinguish at least:

~~~text
final_output_usage
aggregate_session_usage
provider_request_count
model_call_count
reasoning_summary_item_count
reasoning_token_count_if_reported
~~~

Every usage field must name its scope.

Do not overload a generic `usage` field with final-turn data when a multi-call session exists.

## Qualification additions

Add new synthetic gates before any v2 real adjudication cohort.

### IA-9 — structured-rationale round trip

Prove:

- model emits label + required structured justification;
- wrapper retains both;
- schema validates both;
- pass export retains both;
- dispute comparison does not leak justifications across agents;
- human resolution renderer displays them intact.

### IA-10 — provenance-scope accounting

Prove:

- final-output usage is recorded separately;
- aggregate session/model usage is recorded separately;
- model-call count is preserved;
- missing provider usage remains explicit rather than zero-filled;
- published evidence does not expose private reasoning-summary content.

### IA-11 — optional reasoning-summary capability

If supported by the runtime/provider:

- record whether summary capability is advertised;
- record whether summary events are observed;
- retain summaries only in private execution logs/evidence;
- prove that adjudication still succeeds if summaries are unavailable.

This gate is observational, not a prerequisite for authoritative rationale completeness.

## P0A failure policy

Qualification should fail before real labels if:

- any eligible decision lacks structured justification;
- rationale fields are dropped during wrapping;
- dispute rendering cannot preserve A/B/C justifications;
- provenance scope cannot distinguish final-output and aggregate session usage.

Do not spend a real cohort to discover these failures again.

## Publication boundary

P3/public artifacts should never include private provider reasoning summaries by default.

Public rationale policy must be frozen separately:

- full structured justifications;
- sanitized/quoted subset;
- aggregate taxonomy only;
- private only.

The default should be conservative.

The public oracle projection should remain separate from the private frozen oracle.

## Metrics enabled by v2

Potential preregistered diagnostic metrics:

- rationale retention rate;
- rubric-rule attribution distribution;
- ambiguity declaration rate;
- disagreement-cause taxonomy;
- label/justification consistency audit;
- human-resolution evidence completeness;
- reasoning-summary availability rate, strictly supplementary;
- aggregate-session versus final-output usage reconciliation.

None should be introduced post hoc after outcomes are observed.

## Implementation ownership

### agent-workflow-comparative-eval

Own:

- versioned study/protocol semantics;
- justification schema semantics;
- diagnostic metric definitions;
- public/private evidence policy.

### agent-workflow-benchmark

Own:

- Inspect/Codex prompt implementation;
- v2 pass schema;
- pass wrapping;
- qualification gates;
- dispute/human-resolution rendering;
- provenance scope capture;
- publication projection/verifier.

### Agent-Workflow

No new workflow authority should be introduced for this change.

## Exit criteria before a real v2 cohort

A real v2 cohort may start only when:

1. v2 study/protocol identities are frozen;
2. every decision justification round-trips in synthetic A/B/C tests;
3. human conflict review renders all independent justifications;
4. aggregate-session usage is independently verified;
5. private reasoning summaries are demonstrably optional;
6. publication redaction tests cover rationale/participant/reasoning evidence;
7. runtime/model identity is frozen;
8. no v1 artifact is modified or reinterpreted as v2 evidence.

## Relationship to v1

v1 remains the completed historical cohort.

Its failures are evidence motivating this design, not migration defects to be silently repaired in place.
