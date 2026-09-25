# Comparative Evaluation — Unified Continuation Checkpoint

**Date:** 2026-09-24  
**Checkpoint:** `comparative-study-v2`  
**Supersedes / incorporates:** `docs/checkpoints/2026-09-24-comparative-study-v1-checkpoint.md`

This checkpoint is the new canonical continuation handoff for Comparative-Eval-AW. It carries forward the v1 checkpoint and adds the merged implementation, frozen corpus, dataset-ownership cleanup, and independent-oracle protocol.

## New-thread bootstrap

Read the Comparative Evaluation Project Instructions first, then this checkpoint. Treat current GitHub default-branch HEADs as authoritative and re-audit them before changing code. Continue from **Next exact actions**. Preserve the frozen study/corpus/oracle boundaries. Use the TypeSafe/Jev implementation skill and current TypeSafe documentation where relevant. Do not infer or claim Jev/TypeSafe effectiveness before the independent oracle is frozen and the preregistered study is run.

## Governing boundaries

- Agent-Workflow owns workflow/lifecycle/policy/side effects.
- TypeSafe/Jev supplies typed semantic evidence only.
- comparative-eval owns neutral contracts, frozen study/dataset semantics, metrics and statistics.
- benchmark owns experimental execution/evidence/sanitization/publication preparation.
- benchmark-results owns public evidence and limitations.
- historical agent-workflow-typesafe-ai is provenance, not the current runtime boundary.

Locked principles:

1. Agreement is not correctness.
2. Oracle labels are separate from inference input.
3. One batched provider request is counted once even when it yields three decision observations.
4. Raw semantic evidence, policy candidate, and applied result are separate layers.
5. Provider failure/no-decision remains effectiveness/reliability evidence.
6. Candidate attempt accuracy counts no-decision/error as not-correct; answered-only accuracy is separate.
7. Calibration is conditional on usable answered probability evidence.
8. A favorable Jev result is not required for publication.
9. Portfolio language must distinguish implementation completion from empirical results.

## Current default-branch state

| Repository | Branch | HEAD | Version / role | CI |
| --- | --- | --- | --- | --- |
| agent-workflow-comparative-eval | master | `678dbc5c908beb60a5fa69fb0faa20b30e7313d5` | 0.2.0 evaluator + study/corpus ownership | `36093550334` success |
| agent-workflow | master | `052244dffdc1c69a1d41bcc6b9a7d58686ebe0d7` | 0.11.10 runtime/application authority | `36092429733` success |
| agent-workflow-benchmark | main | `96f0139d6f206b070223ddf74b0b987fb4d879b9` | 0.4.0 study execution | `36093619761` success |
| agent-workflow-benchmark-results | main | `0a3cccc329a43b3d73b785b5be918f4043c5ca02` | public evidence/status | `36093737243` success |

Merged work:

- comparative-eval PR #2: study-grade evaluator foundation.
- Agent-Workflow PR #33: lossless semantic evidence persistence.
- benchmark PR #31: preregistered comparative-decision lane.
- benchmark-results PR #5: public evidence scaffold.
- comparative-eval PR #3: neutral dataset ownership + frozen 120-case corpus.
- benchmark PR #32: shared neutral dataset contracts + corpus/oracle export commands.

## Implementation carried forward from v1

### comparative-eval 0.2.0

- provider-neutral observation/outcome/report contracts;
- provider-request contract;
- explicit exclusions;
- Choice/Noul/Score per-decision evidence;
- correctness/classification/ordinal/calibration/reliability metrics;
- Wilson intervals and deterministic paired bootstrap;
- request-level efficiency;
- sample eligibility;
- timeout/error/no-decision retained in attempt-level denominators.

### Agent-Workflow 0.11.10

- preserves TypeSafe request ID, projector version, request hash, model/question identity, probability/confidence/distributions and usage;
- emits three neutral routing observations instead of one lossy composed-route observation;
- stores one provider-request record for one batched Jev call;
- centralizes receipt -> neutral evidence in `routing_comparison_records()`;
- deterministic control remains authoritative in comparative mode;
- raw task text is not persisted in neutral SQLite evidence.

### benchmark 0.4.0

Commands:

- `decision-study-validate`
- `decision-study-run`
- `decision-study-report`
- `decision-study-publish-prepare`

The run command cannot receive an oracle. `run-manifest.json` records `oracle_seen_during_inference: false`.

## Post-v1 work now complete

### Neutral dataset ownership

comparative-eval now owns:

- `agent-workflow-comparative-eval/decision-study-corpus/v1`
- `agent-workflow-comparative-eval/decision-study-oracle-bundle/v1`
- `agent-workflow-comparative-eval/oracle-authoring-view/v1`
- nested case/oracle validation;
- duplicate ID checks;
- dataset identity checks;
- frozen-oracle validation;
- packaged study corpus;
- blinded oracle-authoring view.

Benchmark duplicate corpus/oracle schemas were deleted. Benchmark retains execution/publication schemas and consumes the evaluator contracts.

### Frozen corpus

- Study: `routing-semantic-v1`
- Study version: `1.1.0`
- Dataset: `routing-semantic-corpus-v1.0.0`
- Cases: **120**
- Every case is oracle-eligible for all three seams.
- Oracle labels are absent from the inference corpus.

Canonical corpus:

`src/agent_workflow_comparative_eval/resources/studies/routing-semantic-v1.corpus.json`

Coverage includes clear implementation/diagnosis/review/docs/planning cases, missing metadata, stale/misleading task type, missing authorization, stale interaction flags, high-consequence production/security tasks, mixed-intent requests, and terse/ambiguous edge cases.

Construction tags are retained for later stratified analysis but are removed from the oracle-authoring view.

### Study spec 1.1.0

The rubric was clarified and versioned **before live inference**.

Task-class labels:

- implementation
- diagnosis
- review
- documentation
- other

Mixed-intent precedence:

1. executable behavior/code/config change required -> implementation;
2. otherwise final assessment/audit/verdict -> review;
3. otherwise root-cause/state understanding -> diagnosis;
4. otherwise documentation deliverable -> documentation;
5. otherwise other.

Declared `task_type` is observed evidence, not ground truth.

Interaction oracle: true only when a material user decision, authorization, or preference is missing and required before the requested action can responsibly complete. Declared `requires_interaction` is evidence, not truth.

Semantic-risk oracle measures consequence of acting on a materially wrong interpretation:

- 0 low/easily reversible;
- 1 moderate/recoverable meaningful impact;
- 2 high production/security/authorization/credential/destructive/public-claim/financial boundary.

### Independent oracle protocol

Canonical document:

`docs/studies/routing-semantic-v1-oracle-protocol.md`

Protocol:

1. Freeze/hash corpus.
2. Export blinded oracle-authoring view.
3. A labels all seams independently.
4. B labels all seams independently without seeing A.
5. Compare only after both passes.
6. Agreements become provisional labels.
7. Disagreements go to independent C.
8. Two-of-three agreement becomes provisional final.
9. Three-way conflicts use recorded adjudication with only the case, frozen rubric and independent rationales.
10. Unresolved conflicts become `oracle_conflict_unresolved`.
11. Freeze final oracle bundle and SHA-256 **before live comparative inference**.
12. Oracle first enters the pipeline during post-inference reporting.

### Blinded oracle-authoring view

Includes:

- case ID;
- request text;
- declared metadata;
- oracle eligibility;
- frozen decision taxonomy/rubric;
- oracle policy.

Excludes:

- construction tags;
- deterministic outputs;
- Jev outputs;
- probabilities/confidence;
- comparison results;
- earlier benchmark qualification outcomes.

### Export/run flow

```bash
agent-workflow benchmark decision-study-corpus-export ./routing-corpus.json
agent-workflow benchmark decision-study-oracle-view-export ./oracle-authoring-view.json

agent-workflow benchmark decision-study-validate ./routing-corpus.json

# after independent oracle freeze
agent-workflow benchmark decision-study-validate ./routing-corpus.json --oracle ./oracle.json

# oracle is not passed here
agent-workflow benchmark decision-study-run ./routing-corpus.json ./run

# oracle first enters here
agent-workflow benchmark decision-study-report ./run ./oracle.json

agent-workflow benchmark decision-study-publish-prepare ./run ./oracle.json ./public
```

## Frozen sample/statistical policy

- target shared cases: 120;
- minimum oracle-eligible per seam: 100;
- confidence: 95%;
- deterministic paired bootstrap: 10,000 resamples;
- p90 only at n >= 20;
- p95 only at n >= 40;
- ECE only at n >= 100.

Decision seams:

| Decision | Type | Primary quality view |
| --- | --- | --- |
| `routing.task_class` | Choice | five-class accuracy/confusion, paired correctness, multiclass Brier/log loss |
| `routing.interaction_required` | Noul | binary accuracy/precision/recall/F1, paired correctness, Brier/ECE |
| `routing.semantic_risk` | Score | MAE, signed bias, within-one-level, paired absolute-error effect, distribution calibration |

Production TypeSafe/Jev asks the three questions in one batch:

- one case -> one provider request;
- one provider request -> three decision observations;
- provider latency/tokens/cost/retries counted once.

## TypeSafe/Jev implementation rules retained

- Choice: defined option set + probability/confidence evidence.
- Noul: probability of yes; no invented separate confidence.
- Score: ordered levels represented by weighted score/distribution and confidence.
- One coherent judgment per question.
- Bounded relevant state.
- Batch independent questions over the same state.
- Typed output is not truth.
- Application retains authority.
- Thresholds require empirical evaluation.
- Preserve raw typed evidence separately from policy composition.
- Version questions, state projection, policy and study identity.

Current runtime identity:

- question set: `routing/v2`
- projector: `routing-state/v2`

## Current empirical status

Completed:

- study infrastructure;
- lossless evidence path;
- evaluator/benchmark/publication stack;
- cross-repository qualification;
- neutral corpus ownership;
- 120-case frozen public-safe corpus;
- study spec 1.1.0;
- frozen oracle rubric;
- frozen A/B/C adjudication protocol;
- blinded oracle-authoring export.

Not completed:

- independent A/B adjudication;
- C adjudication of disagreements;
- final frozen oracle bundle/hash;
- live TypeSafe/Jev inference over the frozen corpus;
- development instrumentation receipt on the frozen corpus;
- full study report;
- empirical public results.

No current artifact supports a claim that Jev improves correctness, latency, tokens, cost, or downstream quality. BM3-BM5 qualification calls remain integration evidence and must not be pooled into this study.

## Next exact actions

### P0 — independent oracle

1. Export `oracle-authoring-view.json`.
2. Give the identical blinded artifact + frozen protocol to independent A and B.
3. Collect independent labels.
4. Compare only after both complete.
5. Route disagreements to C.
6. Resolve under the frozen protocol.
7. Preserve unresolved conflicts explicitly.
8. Build `decision-study-oracle-bundle/v1`.
9. Validate it against `routing-semantic-corpus-v1.0.0`.
10. Freeze it and record SHA-256.

**Do this before live comparative inference.**

### P1 — development instrumentation run

After oracle freeze, run a small instrumentation check and verify:

- one provider request per case;
- three observations per successful case;
- unique request IDs;
- probability/distribution survival;
- failures preserved;
- oracle absent during inference;
- no secrets/raw provider HTTP in public evidence;
- no latency/token/cost triple-counting.

Development run is not a generalized effectiveness result.

### P2 — full preregistered run

Run all 120 cases. Preserve exact Agent-Workflow, benchmark, comparative-eval, TypeSafe SDK, model, question-set, projector, decision-profile, corpus and oracle identities. Join oracle only after inference. Generate report, inspect exclusions/eligibility, then publish sanitized evidence regardless of outcome direction.

## Portfolio-safe material

Safe to render now:

- `docs/portfolio/COMPARATIVE_STUDY_PROGRESS.md`
- `docs/studies/routing-semantic-v1.md`
- `docs/studies/routing-semantic-v1-oracle-protocol.md`
- benchmark `docs/COMPARATIVE_DECISION_STUDY.md`
- benchmark-results `comparative-eval/routing-semantic-v1/IMPLEMENTATION_STATUS.md`
- benchmark-results methodology/limitations pages.

Safe claims: architecture implemented/merged; lossless three-seam evidence; one-request accounting; structural oracle separation; 120-case corpus frozen; spec 1.1.0 frozen; independent adjudication protocol frozen; blinded oracle export implemented; ready for independent oracle adjudication then live execution.

Do not present candidate-vs-control effectiveness numbers until the oracle-backed run exists.

## Do-not-regress checklist

- deterministic control authoritative in comparative mode;
- independent oracle unavailable during inference;
- construction tags absent from adjudicator view;
- candidate/control outputs absent from adjudicator view;
- one batched provider request counted once;
- three semantic seams reported separately;
- timeout/error/no-decision retained in attempt-level effectiveness;
- answered-only accuracy separate;
- calibration conditional on usable answered probability evidence;
- explicit exclusions/reason codes;
- minimum-n gates;
- stable case IDs/dataset version;
- exact runtime identities captured;
- no raw TypeSafe HTTP or secrets in public output;
- unfavorable/null Jev result remains publishable;
- post-freeze result-affecting changes require a new version.

## Immediate continuation summary

> The code stack is merged and green. The study design is frozen at `routing-semantic-v1/1.1.0`. The inference corpus is frozen at `routing-semantic-corpus-v1.0.0` with 120 cases. The blinded oracle-authoring workflow and independent A/B/C adjudication protocol are ready. No oracle-backed live Jev study has been run yet. Continue by producing and freezing the independent oracle before any live comparative inference.
