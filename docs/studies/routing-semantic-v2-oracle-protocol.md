# Routing Semantic Oracle Protocol v2 — Draft

**Protocol identity:** `routing-semantic-oracle-v2-draft.1`  
**Status:** implementation draft; must be frozen before real adjudication

The v1 task-class, interaction-required, and semantic-risk rubrics remain semantically unchanged for the methodological replication. The material change is the evidence contract.

## Independent decision record

For every assigned seam, the adjudicator must emit:

1. the label;
2. one to three decisive case-evidence statements;
3. the rubric rule that determined the label;
4. an ambiguity value: `none`, `material`, or `insufficient_evidence`.

The evidence statements must reference only information present in the blinded case and supplied metadata. They must be concise conclusions, not hidden chain-of-thought.

## Blinding

A and B remain mutually blind.

C receives only the disputed case, supplied metadata, frozen rubric, and disputed decision IDs. C must not receive A/B labels or justifications before completing its own pass.

Treatment/control outputs, candidate probabilities, construction tags, repository state outside the frozen view, and private runtime context remain prohibited.

## Human three-way resolution

After A/B/C complete, genuine three-way conflicts must render all three independent labels and structured justifications to the human resolver.

The human resolution record remains separate and must include final status/label, rationale, and participants.

## Supplementary provider reasoning summaries

If the provider/runtime emits reasoning summaries, they may remain in private execution logs.

They are not the authoritative rationale and are not required for study validity.

## Usage provenance

The adjudication runtime must record final-output usage separately from aggregate session/model usage. A generic `usage` field whose scope is ambiguous is not valid v2 provenance.

## Preflight failure policy

Real adjudication must not begin unless synthetic qualification proves that structured justifications survive:

~~~text
model output
  -> pass wrapper
  -> schema validation
  -> A/B dispute detection
  -> blinded C execution
  -> human-resolution rendering
~~~
