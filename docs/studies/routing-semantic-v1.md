# Routing Semantic Comparative Study v1

**Study ID:** `routing-semantic-v1`  
**Study version:** `1.1.0`  
**Status:** preregistered implementation specification

## Purpose

This study evaluates the three live Agent-Workflow routing semantic seams against the current deterministic control without giving either implementation access to the independent oracle. It is a decision-quality study, not a lifecycle benchmark and not an attempt to produce a favorable TypeSafe/Jev result.

The frozen application seams are:

| Decision | Type | Primary correctness view |
| --- | --- | --- |
| `routing.task_class` | Choice | five-class accuracy/confusion plus paired change analysis |
| `routing.interaction_required` | Noul | binary classification plus probability calibration |
| `routing.semantic_risk` | Score | ordinal error/bias plus level-distribution calibration |

Agent-Workflow remains authoritative. Comparative mode applies deterministic control and records the semantic candidate as shadow/counterfactual evidence.

## Frozen research questions

1. How does TypeSafe task-class correctness compare with deterministic classification?
2. How does TypeSafe interaction-required evidence compare with deterministic heuristics?
3. How accurately and how calibratably does TypeSafe semantic-risk evidence match independently adjudicated consequence?
4. When candidate and control disagree, is the change beneficial, harmful, or redundant against the oracle?
5. What success, no-match, uncertainty, fallback, timeout, error, and retry rates occur?
6. What latency, token, and cost overhead is attributable to the one batched semantic request per case?
7. Are probability outputs calibrated well enough to motivate a separately versioned confidence-policy study?

## Experimental unit

One case contains only public-safe task text and bounded routing metadata. The production-style semantic candidate asks all three TypeSafe questions in one batched request. That request is then projected into three decision observations.

Request-level latency/tokens/cost are counted once. They are never copied into three decision totals.

## Oracle independence and blinding

The inference corpus and oracle are separate artifacts. The inference runner receives no oracle fields. Oracle authors/adjudicators must not see deterministic or semantic outputs before the oracle is frozen.

The oracle covers:

- task class under the frozen five-class taxonomy;
- whether a material user decision or authorization is genuinely missing;
- consequence of acting on an incorrect semantic interpretation on the frozen 0–2 risk rubric.

Any result-affecting change to labels, rubric, exclusion rules, metrics, or question meanings requires a new study or dataset version.

## Sample and statistical policy

The target is 120 shared cases and at least 100 oracle-eligible cases per seam.

- confidence level: 95%;
- paired bootstrap: 10,000 deterministic resamples;
- p90 is eligible only at n >= 20;
- p95 is eligible only at n >= 40;
- ECE/reliability-diagram publication requires n >= 100 for the seam;
- every corpus case is accounted for as eligible, failed, or excluded with a reason code.

Provider failures remain reliability evidence and are not silently removed from denominators.

## Raw semantic quality versus operational policy

The study separates three layers:

```text
raw TypeSafe evidence
        |
        v
Agent-Workflow policy candidate
        |
        v
applied decision
```

Raw Choice/Noul/Score quality is evaluated against the oracle. Operational policy value is evaluated separately. This prevents the current confidence threshold or non-automatable risk seam from being mistaken for model correctness.

## Exclusion policy

Allowed reason codes are frozen in the machine-readable study specification. Silent exclusions are forbidden. Oracle absence/conflict, inference leakage, execution failure, service failure, invalid provider contracts, and cohort mismatches remain visible in the study manifest.

## Publication policy

Raw provider HTTP evidence and credentials remain private. Public evidence may include public-safe inputs, sanitized case-level decision evidence, aggregate metrics, hashes, exact software/model/question-set/projector identities, exclusion counts, limitations, and reproducibility instructions.

A favorable semantic result is not required for publication. Evidence quality is the acceptance criterion.


## Frozen inference corpus

The canonical inference corpus is packaged as:

`resources/studies/routing-semantic-v1.corpus.json`

Dataset version: `routing-semantic-corpus-v1.0.0`  
Case count: **120**

The corpus is public-safe and contains no oracle labels. It deliberately spans:

- clear single-intent tasks;
- absent routing metadata;
- stale or misleading declared task type;
- material authorization/choice gaps;
- stale interaction flags where no new decision is required;
- production/security high-consequence contexts;
- mixed-intent tasks;
- terse and ambiguous requests.

Construction tags exist only for later stratified analysis. They are not sent to Agent-Workflow's decision provider and are removed from the oracle-authoring view.

## Independent oracle handoff

`oracle_authoring_view()` produces the adjudicator artifact. It contains the frozen decision taxonomy/rubric plus only case ID, request text, declared metadata, and oracle eligibility.

The authoring view excludes:

- construction tags;
- deterministic control outputs;
- TypeSafe/Jev outputs;
- probability/confidence evidence;
- comparison results.

Oracle adjudication must be performed without access to treatment outputs. The resulting frozen oracle remains a separate artifact and is first joined after inference.

### Frozen adjudicator handoff identity

The exact blinded artifact for independent A/B adjudication is committed at:

`docs/studies/artifacts/routing-semantic-v1/oracle-authoring-view.json`

Identity:

- corpus SHA-256: `e4b33df3b3752b32cdb362833765cc8f0c9cc024473071209563d73284011280`
- authoring-view SHA-256: `a5a40224793a50d9371e9ae437e144b15812829ba1cd56a5564dc6ba28846a0a`
- cases: **120**
- oracle protocol: `routing-semantic-oracle-v1.0.0`

The adjacent `oracle-authoring-view.manifest.json` records the source commit, corpus/spec blob identities, hashes, case count, and blinding flags. Adjudicators A and B must receive this exact file; do not regenerate or modify it after adjudication begins.
