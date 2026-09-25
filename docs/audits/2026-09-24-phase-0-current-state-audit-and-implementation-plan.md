# Agent-Workflow Comparative Evaluation
## Phase 0 Current-State Audit and Implementation Plan
**Audit date:** September 24, 2026

## Executive conclusion

The comparative-evaluation ecosystem is substantially more mature at the **component level** than the current public evidence suggests. The handoff is correct that the central problem is not a lack of metrics: the neutral library already contains correctness, reliability, efficiency, calibration, and deterministic statistical machinery. The missing maturity is primarily **experimental and connective**—the system does not yet carry sufficiently rich per-decision evidence all the way from the live TypeSafe/Jev call into a frozen, independently labeled, benchmark-owned study and then into a first-class public report.

The current architecture also still respects the intended ownership split: Agent-Workflow owns application/lifecycle authority, comparative-eval owns neutral comparison semantics, benchmark owns experimental execution, and benchmark-results owns public evidence. That boundary should be preserved.

Three issues block a defensible comparative-decision study:

1. **No adequate frozen oracle corpus exists.** The packaged `routing-v1` corpus has only four routing cases and mixes decision dimensions. BM3–BM5 contain only three pre-treatment semantic qualification contexts each, with no independent decision oracle. Those calls demonstrate that the integration works; they do not establish correctness.
2. **Agent-Workflow currently throws away study-critical semantic evidence at the comparative persistence boundary.** The live TypeSafe receipt preserves Choice/Score confidence and distributions and Noul probability, but `_capture_routing_comparison()` persists mainly the composed route plus model/question-set identity. As a result, `comparative-eval.sqlite` cannot support the library's calibration metrics for normal routing observations.
3. **`agent-workflow-benchmark` has no dedicated comparative-decision study lane.** It knows how to qualify TypeSafe and collect sanitized audit metadata, but it does not currently automate frozen corpus → decision execution → oracle join → comparative-eval report → sanitized publication.

This agrees with the project's governing requirement to prioritize empirical completeness rather than simply accumulating more features.

### Audited HEADs

| Repository | Branch | HEAD | Current relevant version/state |
|---|---|---|---|
| `agent-workflow-comparative-eval` | `master` | `594d473351b8` | `0.1.0`; 19 library/contract tests reported passing |
| `agent-workflow` | `master` | `4595a2f18024` | `0.11.9`; built-in TypeSafe provider; `deterministic`, `typesafe`, `comparative` modes |
| `agent-workflow-benchmark` | `main` | `de3bf736e447` | `0.3.9`; requires Agent-Workflow `>=0.11.9,<0.12` |
| `agent-workflow-benchmark-results` | `main` | `241a2980a75a` | BM3–BM5 public evidence; TypeSafe qualification summaries published |

One maintenance issue surfaced immediately: comparative-eval's repository validation record was originally qualified against Agent-Workflow 0.10.1, and its README explicitly records independent compatibility through 0.11.4. Agent-Workflow is now 0.11.9. Requalification against the current consumer should therefore be part of P0 even though no incompatibility is presently evident.

---

# 1. Current-state architecture

```text
                         CURRENT APPLICATION PATH

 task text + routing metadata
             |
             +-----------------------+
             |                       |
             v                       v
 deterministic routing       Agent-Workflow built-in TypeSafe provider
    control                        routing/v2
                                   routing-state/v2
                                   |
                            one batched System One call
                                   |
                  +----------------+----------------+
                  |                |                |
                  v                v                v
              Choice           Noul             Score
          task_class     interaction_required  semantic_risk
                  |                |                |
                  +----------------+----------------+
                                   |
                         rich DecisionEvidence
                    probability / confidence /
                    distributions / model / hash
                                   |
                                   v
                         Agent-Workflow policy
                    thresholds + fallback + authority
                                   |
                     comparative mode keeps control
                       authoritative and creates
                     counterfactual candidate route
                                   |
                                   v
                             Scheduler
                                   |
                     _capture_routing_comparison()
                                   |
                      [INFORMATION LOSS HERE]
                  probabilities/distributions/fallback
                       not preserved in the neutral
                         comparative observation
                                   |
                                   v
                        comparative-eval.sqlite
                                   |
                                   v
                    comparative-eval 0.1.0 reports


                         CURRENT BENCHMARK PATH

 BM3 / BM4 / BM5 phase contexts
             |
             v
  3 pre-treatment TypeSafe qualification calls
             |
        +----+----+
        |         |
        v         v
 private raw    sanitized
 audit JSONL    public summary
        |         |
        |         v
        |   benchmark-results
        |
        X    semantic calls intentionally excluded
             from both paired benchmark treatments


                 MISSING CONNECTION FOR THIS PROJECT

 frozen labeled decision corpus
             |
             v
 current Agent-Workflow decision boundary
             |
             v
 per-seam neutral observations + request evidence
             |
             v
 independent oracle join
             |
             v
 comparative-eval report
             |
             v
 benchmark sanitizer / publication manifest
             |
             v
 benchmark-results/comparative-eval/...
```

This current separation is architecturally sound. The intended architecture explicitly says not to put lifecycle authority into comparative-eval or comparison semantics into provider-specific code.

The TypeSafe/Jev design also remains aligned with its intended programming model. Current TypeSafe documentation describes Choice as a defined-option decision with a probability distribution/confidence, Noul as a probability of yes, and Score as an ordered score with probability evidence; the application remains responsible for policy and control flow.

---

# 2. Feature/completeness matrix

| Capability | Current state | Assessment | Required action |
|---|---|---|---|
| Neutral observation/outcome/report contracts | Implemented in comparative-eval 0.1.0 | Strong foundation | Version rather than replace |
| Frozen dataset support + hashing | Implemented | Mechanism good, content inadequate | Add study-grade routing corpus |
| Pairing/cohort identity | Implemented | Foundation present | Strengthen mandatory study identity |
| Deterministic routing control | Implemented in Agent-Workflow | Ready | Freeze current version in study |
| Built-in TypeSafe provider | Implemented | Ready | Freeze question/projector/SDK/model identity |
| Three semantic seams | Implemented | Ready | Evaluate separately |
| Raw TypeSafe typed evidence | Captured in Agent-Workflow receipts/audit | Strong | Carry it across persistence boundary |
| Comparative mode | Implemented; deterministic remains authoritative | Ready | Use for evaluation |
| SQLite comparative persistence | Implemented | Partial | Persist seam-level semantic evidence |
| Independent oracle joining | Contract support exists | Partial | Build actual oracle corpus/protocol |
| Correctness functions | Implemented | Partial integration | Wire classification/ordinal reports |
| Reliability functions | Implemented | Partial integration | Add fallback/no-match/uncertainty accounting |
| Efficiency functions | Implemented | Partial data supply | Add TypeSafe usage/retry/cost evidence |
| Calibration functions | Implemented | Blocked by capture | Preserve probability vectors |
| Wilson intervals | Implemented | Not first-class in report | Wire to arm rates |
| Paired bootstrap | Implemented | Primarily efficiency today | Add paired correctness effect reporting |
| Tail metric sample gates | Documented | Partially enforced | Centralize eligibility policy |
| Minimum paired n policy | Described | Not consistently enforced by report generation | Enforce/report explicitly |
| Exclusion policy | Not study-grade | Missing | Version reason codes and denominators |
| Dedicated decision runner | None | Missing | Add benchmark lane |
| Corpus validation | Generic support | Incomplete | Add oracle/schema/leakage validation |
| Semantic evidence sanitizer | Audit counts/hashes exist | Partial | Add comparative report sanitizer |
| Public comparative-eval result structure | None | Missing | Add dedicated results tree |
| BM3–BM5 qualification evidence | Published | Useful integration evidence only | Keep as historical diagnostic evidence |
| Consumer compatibility qualification | Stale relative to AW 0.11.9 | Maintenance gap | Requalify before study |

The library should therefore be regarded as an **implemented evaluation engine with an immature study pipeline**, not an immature evaluator.

---

# 3. Metric coverage matrix

The project instructions require every metric to be tied to its question, data source, oracle dependency, sample limitations, and public representation.

| Metric | Question answered | Required evidence | Current coverage | Oracle? | Publication rule |
|---|---|---|---|---|---|
| Total / eligible / excluded | How much evidence actually contributed? | Case IDs, attempt status, exclusion reason | Partial | No | Always publish denominators |
| Task-class top-1 accuracy | Which implementation classifies task class correctly more often? | Normalized control, raw Choice, label | Functions exist; report incomplete | Yes | Per seam |
| Task-class confusion matrix | Where do classifications fail? | Same plus full taxonomy | Function exists; not wired into main report | Yes | Per seam |
| Control-only / candidate-only / both / neither | Where does each method add or lose value? | Paired outputs + label | Implemented | Yes | Core paired evidence |
| Interaction accuracy/precision/recall/F1 | Does Noul identify missing material interaction? | Control bool, Noul result, binary oracle | Functions exist; current persistence blocks semantic raw evidence | Yes | Per seam |
| Semantic-risk ordinal MAE | How far is the risk judgment from adjudicated level? | Control level, Score value, ordered oracle | Function exists; not wired | Yes | Per seam |
| Semantic-risk signed bias | Does candidate systematically over/under-rate risk? | Same | Function exists; not wired | Yes | Per seam |
| Within-one-level accuracy | How often is risk materially close? | Same | Function exists; not wired | Yes | Per seam |
| Disagreement rate | How often does semantics materially differ from heuristic control? | Paired raw outputs | Route-level agreement exists, seam-level incomplete | No | Distinguish from correctness |
| Candidate success/error/timeout | Is semantic evidence operationally reliable? | Attempt status | Implemented | No | Include failures in denominator |
| No-match rate | How often is the candidate unable to choose? | Choice status | Captured in receipt, not neutral report | No | Per seam |
| Uncertainty rate | How often does policy reject low-confidence evidence? | Confidence/probability + threshold | Receipt only | No | Separate raw quality from policy |
| Fallback rate/reason | How often is deterministic fallback used, and why? | Policy receipt | Receipt only | No | Reason-coded |
| Retry rate | How often does provider transport retry? | Provider telemetry | Not carried into comparative record | No | Request level |
| Provider latency | What runtime overhead does semantics add? | Provider elapsed | Captured | No | Request-level primary metric |
| First-output latency | Streaming responsiveness? | Streaming telemetry | Not naturally meaningful here | No | Report N/A, do not fabricate |
| Input/output/token usage | What inference budget is consumed? | TypeSafe usage | Library supports it; AW path does not currently supply it | No | Request-level |
| Billed/local cost | What does semantic inference cost? | Provider bill or versioned catalog | Library supports it; data path incomplete | No | Pin currency/catalog |
| Noul Brier | Are interaction probabilities calibrated? | P(yes) + binary truth | Library implemented; current persistence blocks it | Yes | Primary calibration metric |
| Noul ECE | How does stated probability track observed frequency? | P(yes) + truth + binning policy | Implemented without adequate study-level n guard | Yes | Publish only with preregistered sample/bin policy |
| Choice multiclass Brier | Is task-class probability mass calibrated? | Full Choice vector + truth | Implemented; current persistence blocks it | Yes | Per seam |
| Choice log loss | Does candidate assign probability to the correct class? | Full Choice vector + truth | Implemented; current persistence blocks it | Yes | Per seam |
| Score probability quality | Is risk-level probability mass useful? | Score level distribution + oracle level | Not integrated | Yes | Add ordinal/multiclass treatment |
| Wilson interval | What uncertainty surrounds an arm rate? | successes/n | Function exists, main report does not surface it consistently | Yes for correctness rates | Publish with n |
| Paired accuracy effect CI | What is uncertainty on candidate-control improvement? | Per-case paired correctness delta | Primitive exists; main correctness report lacks it | Yes | Required |
| Beneficial/harmful change rate | When semantics alters a decision, did that help? | Raw/control/candidate/oracle | Missing | Yes | Required operational-value section |
| Redundancy rate | How often does semantic evidence add no decision information? | Paired outputs | Derivable, not reported | No/Yes depending definition | Publish |
| Repeated-case stability | Does candidate vary across identical cases? | Repetitions | Registry mentions stability but report incomplete | Usually no | Secondary metric |

The first study should not invent metrics merely because they are available. The core publishable set is correctness + disagreement + reliability + request-level efficiency + applicable calibration + paired uncertainty. The handoff already requires these dimensions to remain distinct.

---

# 4. Instrumentation and data-flow audit

## A. TypeSafe provider: strong

`agent_workflow.semantic.typesafe` currently uses `routing/v2` with projector `routing-state/v2`. It batches the three decisions into one System One request and retains:

| Evidence | Current receipt/audit |
|---|---|
| Raw selected Choice | Yes |
| Choice confidence | Yes |
| Choice probability vector | Yes |
| Noul probability | Yes |
| Score value | Yes |
| Score confidence | Yes |
| Score distribution | Yes |
| Model identity | Yes |
| Question-set version | Yes |
| Request SHA | Yes |
| Source references | Yes |
| Provider elapsed | Yes |
| Error class | Yes |
| Raw redacted request/response private audit | Yes |
| Parsed usage/retry/cost propagated to comparison | No |

This is already consistent with the TypeSafe skill's guidance to preserve typed raw judgments and let deterministic application policy decide what to do with them.

## B. Decision policy: strong

Agent-Workflow correctly distinguishes:

`semantic evidence` → `policy candidate` → `applied decision`.

That separation is essential. For example, a Noul result can be a valid probability while still falling into the operational uncertainty band around the configured 0.8 threshold. Likewise, `semantic_risk` is deliberately non-automatable.

The study must preserve all three layers rather than judging Jev by whether the current policy accepted its answer.

## C. Comparative persistence: critical gap

Current `_capture_routing_comparison()` reads the rich decision receipts but records only limited semantic identity and the composed route:

```text
semantic identity:
    decision_id
    model
    question_set_version

candidate result:
    recommendation
    enforced_selection
```

It does **not** persist the per-decision:

```text
raw semantic answer
probability
confidence
probability distribution
no-match status
uncertainty/fallback reason
request hash
usage
retry evidence
```

Consequences:

- Brier/ECE cannot run from `comparative-eval.sqlite`.
- Choice multiclass Brier/log loss cannot run.
- Score ordinal analysis cannot operate at the semantic seam.
- Reliability cannot distinguish service failure, no-match, uncertainty, and policy fallback from the neutral evidence alone.
- Correctness is currently route-level rather than decision-level.
- A future report would have to improperly depend on the private provider audit to reconstruct data that should already exist in a sanitized neutral observation.

This should be the first instrumentation code fix.

## D. Batching/accounting gap

The production provider evaluates all three seams in **one batched request**. A rigorous study should preserve that production behavior.

That introduces an accounting requirement: if three per-decision observations each copy the entire provider token/cost/latency record, aggregate efficiency would triple-count the request.

The proper model is:

```text
semantic request evidence
  request_id / hash
  provider/model/sdk
  timing
  tokens
  retries
  cost
       |
       +---- routing.task_class observation
       +---- routing.interaction_required observation
       +---- routing.semantic_risk observation
```

Correctness/calibration are per decision. Provider overhead is primarily per **batched request**, with an explicitly labeled amortized “cost per eligible decision” only when useful.

## E. Oracle flow: capability exists, actual evidence does not

Comparative-eval supports `static-oracle` and `human-adjudication` outcome records, but no study-grade independent oracle is presently joined to the routing observations. This is the central reason current agreement cannot be called correctness.

## F. Benchmark collection: partial

The benchmark collector already does useful work:

- records package/runtime identities;
- records TypeSafe audit SHA;
- counts statuses and primitives;
- refuses to package evidence if the current API key bytes are found;
- preserves private raw evidence separately.

It does **not** yet treat these as first-class study artifacts:

```text
comparative database identity/hash
observation counts
oracle joins
exclusions
per-seam comparative reports
confidence intervals
calibration records
study manifest
```

That gap matches the handoff's collector audit.

## G. Public evidence: improved since the handoff, but still diagnostic

`agent-workflow-benchmark-results` now publishes sanitized TypeSafe summaries for BM3–BM5. Across those studies there are three pre-treatment qualification calls per study. BM3 exposes one task-class disagreement; BM4 and BM5 show route agreement.

These should **not** be pooled into a nine-case effectiveness dataset. They are repeated benchmark phase contexts, lack independent ground truth, and were deliberately outside the benchmark treatments.

The repository's current wording correctly says that no current benchmark demonstrates that Jev/TypeSafe improves product quality or execution cost.

---

# 5. Experimental-design gap analysis

| Priority | Gap | Why it matters | Resolution |
|---|---|---|---|
| P0 | No preregistered decision-study specification | Analysis choices could drift after seeing results | Freeze research questions, cohorts, exclusions, metrics and oracle protocol first |
| P0 | Four-case routing corpus is inadequate | Cannot support effectiveness or calibration claims | Build 100+ oracle-eligible cases per seam |
| P0 | No independent ground truth | Agreement with deterministic control is not correctness | Blinded independent adjudication |
| P0 | Per-seam probabilities are dropped | Calibration is impossible from canonical evidence | Persist raw typed semantic evidence |
| P0 | Three seams collapsed into `routing-advice/v1` | Different tasks/metrics become semantically mixed | Emit distinct decision observations |
| P0 | Batched provider request is not modeled explicitly | Cost/latency can be triple counted | Add shared request/batch identity |
| P0 | No frozen exclusion policy | Failures can silently bias denominators | Version exclusion reason taxonomy |
| P0 | No dedicated runner | Study cannot be reproduced by one controlled path | Add benchmark comparative-decision lane |
| P0 | No first-class sanitized report publication | Public evidence remains hand-assembled | Automate report/export manifest |
| P0 | Current consumer validation lags AW HEAD | Study stack compatibility is not freshly demonstrated | Requalify 0.1.0/next release against AW 0.11.9 |
| P1 | Correctness report omits available classification/ordinal metrics | Useful implemented metrics are dormant | Wire them into per-seam reporting |
| P1 | Wilson/minimum-n policies not consistently surfaced | Small samples can look more decisive than warranted | Centralize statistical eligibility |
| P1 | ECE lacks a study-level sample/bin policy | Calibration visualization can be unstable | Freeze ECE/reliability-diagram policy |
| P1 | Operational benefit/harm not computed | Accuracy delta alone does not show whether candidate changes matter | Add decision-change outcome matrix |
| P2 | Downstream causal effects remain observational | Shadow mode cannot prove runtime outcome causality | Later guarded experiment only after static evidence |

### Recommended first study unit

Use one **common frozen routing corpus** rather than three unrelated corpora, because production calls the three TypeSafe questions over shared state in one batch.

A case should have:

```text
case_id
dataset_version
public-safe task text
bounded metadata
difficulty tags
ambiguity tags
edge-case tags
oracle:
    task_class
    interaction_required
    semantic_risk
oracle_provenance
adjudication metadata
case hash
```

Each seam has an eligibility flag when a defensible oracle is possible. Target at least **100 oracle-eligible cases for each seam**, preferably 120–150 shared cases so exclusions do not pull a seam below 100. This exceeds the library's statistical minimum and gives materially better calibration evidence than the current four-case corpus. The handoff itself targets 50–100 initially and preferably 100+.

### Oracle protocol

| Seam | Proposed independent ground truth |
|---|---|
| `routing.task_class` | Independently authored label against the frozen five-class semantic taxonomy; blinded adjudication and tie-break where needed |
| `routing.interaction_required` | Binary adjudication using a precise definition of “material user decision or authorization missing from supplied state” |
| `routing.semantic_risk` | Ordered expert rubric for consequence of an incorrect interpretation, with adjudication notes and tie-break |

Oracle authors/adjudicators must not see deterministic or TypeSafe outputs until labels are frozen.

### Raw semantic quality versus operational policy

The study should publish both:

```text
RAW SEMANTIC QUALITY
Choice/Noul/Score versus independent oracle

and

OPERATIONAL POLICY VALUE
control decision
vs policy-projected semantic candidate
vs deterministic applied result
```

This prevents the current 0.8 policy threshold from being confused with model correctness.

For Noul, probability quality should be evaluated directly; the operational threshold is a separate policy analysis. For Score, the expected score/distribution should be evaluated as ordinal evidence even when Agent-Workflow correctly refuses to automate that high-consequence seam.

---

# 6. Prioritized implementation plan

This updates the handoff's Phase 0–7 plan rather than replacing it.

| Phase | Work | Exit condition |
|---|---|---|
| **0 — Audit** | Current HEAD audit, metric/data-flow audit, TypeSafe skill validation | **Complete in this report** |
| **1 — Freeze study specification** | Research questions; semantic taxonomies; evaluation unit; cohort identity; exclusion rules; sample target; oracle protocol; raw-vs-policy metrics; calibration policy; publication rules | Versioned spec committed before study results |
| **2 — Study-ready comparative contracts** | Per-decision observations; request/batch evidence; exclusions; correctness CIs; classification/ordinal report integration; sample eligibility | comparative-eval release passes tests and current consumer qualification |
| **3 — Preserve live evidence** | Convert rich AW receipts into neutral per-seam observations without losing probability/distribution/status; propagate usage/retries; shared batch ID | One synthetic/live case produces complete three-seam evidence + one deduplicated request record |
| **4 — Corpus and oracle tooling** | Dataset schema, validator, hashes, blinded labeling workflow, adjudication record | Frozen corpus with ≥100 oracle-eligible cases/seam |
| **5 — Dedicated benchmark lane** | Corpus validation, readiness, execution, oracle join, reporting, sanitizer, manifest, reproduction checks | One command can execute a development decision study end-to-end |
| **6 — Development study** | Run a small preregistered sample to uncover instrumentation defects only | Pipeline defects fixed through a new study/schema version where result-affecting |
| **7 — Full study + publication** | Run frozen full cohort, generate reports, verify hashes/secret safety, publish | Acceptance criteria below all pass |

Important sequencing rule: **do not build the full corpus before the schema/oracle protocol is frozen, and do not change result-affecting labels/questions/scoring after inspecting favorable or unfavorable full-study results.** A changed design becomes a new version.

---

# 7. Explicit repository-by-repository changes

## `agent-workflow-comparative-eval`

The next study-ready release should likely be versioned as a new minor release rather than silently changing 0.1.0 semantics.

| Change | Purpose |
|---|---|
| Add frozen decision-study dataset schema | Stable IDs, labels, provenance, tags, hashes, eligibility |
| Split/represent the three routing decision seams independently | Prevent meaningless aggregation |
| Add provider-request/batch evidence contract or equivalent deduplication key | Correct latency/token/cost accounting |
| Add structured exclusion records/reason codes | Auditable denominators |
| Wire `classification_metrics()` into reports | Task-class confusion/accuracy |
| Wire `ordinal_metrics()` into reports | Semantic-risk analysis |
| Surface Wilson intervals | Arm accuracy/reliability uncertainty |
| Add paired correctness effect + deterministic bootstrap CI | Primary paired effect evidence |
| Add beneficial/harmful/redundant disagreement matrix | Operational value |
| Preserve Noul/Choice/Score raw probability representations | Calibration |
| Add Score distribution evaluation | Risk probability quality |
| Enforce/report minimum-n and tail-metric eligibility | Prevent overinterpretation |
| Add calibration sample/bin policy | Stable ECE/reliability curves |
| Requalify against Agent-Workflow 0.11.9 and benchmark 0.3.9 | Current compatibility evidence |
| Mark existing four-case `routing-v1` as development/legacy corpus | Prevent accidental public-effectiveness use |

The current 19-test suite is a good contract foundation; the missing tests are mostly study semantics and current-consumer qualification rather than basic package quality.

## `agent-workflow`

No lifecycle authority should move.

Required changes are narrowly about **evidence projection**:

| Change | Purpose |
|---|---|
| Add a canonical conversion from `DecisionEvidence`/receipt → neutral comparative decision observation | Eliminate scheduler-specific lossy projection |
| Persist each live semantic seam separately | Per-decision correctness/calibration |
| Include raw value, probability, confidence, distribution, status, fallback and request hash | Preserve TypeSafe evidence |
| Add a stable provider request/batch ID | Link three decisions to one System One call |
| Extract provider usage/retry information where SDK evidence supports it | Efficiency accounting |
| Preserve post-policy candidate separately from raw semantic answer | Model quality vs operational policy |
| Keep deterministic applied result authoritative in comparative mode | Preserve safety/architecture |
| Extend invariants to prove raw task content/secrets remain absent from neutral SQLite | Maintain privacy boundary |
| Add current-version comparative persistence integration tests | Prevent future evidence loss |

The TypeSafe provider itself is comparatively strong and should not be rewritten. Its current `routing/v2` / `routing-state/v2` definitions should be explicitly frozen into the study cohort.

## `agent-workflow-benchmark`

Add a dedicated experimental lane; do not retrofit BM3–BM5 lifecycle studies.

Recommended surface:

```text
agent-workflow benchmark comparative-decision validate ...
agent-workflow benchmark comparative-decision run ...
agent-workflow benchmark comparative-decision report ...
agent-workflow benchmark comparative-decision publish-prepare ...
```

Exact CLI naming can follow the repository's existing parser conventions.

Responsibilities:

```text
validate frozen study spec
validate corpus and oracle hashes
verify current AW / comparative-eval / TypeSafe runtime
execute each case exactly according to frozen policy
hide oracle labels from both implementations
run one batched semantic request per case
persist per-seam observations
join oracle after inference
record every failure/exclusion
generate comparative-eval reports
construct sanitized public tree
secret-scan
construct publication manifest
verify the resulting public evidence
```

The existing TypeSafe audit collector can be reused for private provenance, but comparative results should be derived from canonical neutral observations—not by parsing private raw HTTP payloads.

## `agent-workflow-benchmark-results`

Add a first-class tree along the lines already proposed by the handoff:

```text
comparative-eval/
  routing-v1/
    README.md
    study-spec.json
    methodology/
      oracle-protocol.md
      exclusion-policy.md
      statistical-policy.md
    datasets/
      manifest.json
      routing-corpus-v1.json
    metrics/
      routing-task-class.json
      routing-interaction-required.json
      routing-semantic-risk.json
      request-efficiency.json
    analysis/
      disagreements.md
      calibration.md
      operational-value.md
    evidence/
      manifest.json
      source-identities.json
      hashes.json
    limitations/
      README.md
```

Do not publish raw TypeSafe audit bodies or secrets. The existing evidence policy already supports the correct pattern: publish sanitized aggregates/hashes and retain sensitive raw evidence privately.

README/portfolio claims should be updated **only after** the first full study passes the acceptance gate. The project objective explicitly requires evidence-backed claims rather than generalized Jev/TypeSafe assertions.

## Historical `agent-workflow-typesafe-ai`

No active implementation should move back into this repository. Use it only to establish provenance, migration compatibility, or historical schema lineage where necessary.

---

# 8. Acceptance criteria for the first publishable comparative-decision study

| Gate | Required condition |
|---|---|
| Specification freeze | Study spec, metric policy, corpus schema, oracle protocol and exclusions committed before full-study results are observed |
| Current-stack identity | Exact AW, comparative-eval, benchmark, TypeSafe SDK, resolved Jev model, question set, projector and policy versions recorded |
| Corpus size | At least 100 oracle-eligible cases for each live decision seam |
| Corpus quality | Straightforward, ambiguous, adversarial/borderline, incomplete, misleading-keyword and mixed-type cases represented |
| Independent truth | Oracle labels created independently of deterministic and semantic outputs |
| Blinding | Oracle/adjudicators do not see treatment results before labels are frozen |
| Leakage prevention | Oracle fields are provably absent from control and TypeSafe request state |
| Per-seam evidence | Task class, interaction and semantic risk preserved as separate evaluation units |
| Raw probability evidence | Choice/Score vectors and Noul probability survive into canonical neutral evidence |
| Raw/policy separation | Raw semantic judgment, policy candidate and applied result are separately represented |
| Attempt accounting | Every corpus case is successful, failed, timed out or excluded with a versioned reason; no silent drops |
| Failure denominator | Provider failures and timeouts remain reliability evidence rather than being removed from the denominator |
| Batch accounting | One TypeSafe request shared by three decisions is counted once for token/cost/latency totals |
| Correctness evidence | Per-seam arm accuracy/error metrics and control-only/candidate-only/both/neither counts generated |
| Statistical evidence | Sample size, confidence level, Wilson intervals and paired effect CI included where applicable |
| Tail metrics | p90 only when n≥20 and p95 only when n≥40; lower-n fields remain unavailable |
| Calibration | Brier/log-loss/ECE/reliability evidence only published when its predeclared eligibility/sample policy is met |
| Risk scoring | Ordered MAE/bias/within-one metrics reported for `semantic_risk` |
| Operational value | Disagreements classified as beneficial, harmful, or redundant against the oracle |
| Efficiency | Provider latency and token evidence complete or explicitly unavailable; cost uses provider billing or a versioned price catalog |
| Reproducibility | A fresh environment can regenerate the report from the frozen public-safe corpus/spec and recorded software versions |
| Determinism | Re-running report construction over identical observations/oracles yields identical metric content |
| Privacy | Raw provider bodies remain private; public tree passes secret/path review and hash verification |
| Public completeness | Machine-readable metrics, methodology, identities, limitations and hashes are all present |
| Claim discipline | No cross-seam headline accuracy is published without a defensible aggregation rule |
| Outcome neutrality | **Jev does not have to outperform deterministic control for the study to be publishable.** Publishability is an evidence-quality criterion, not a favorable-result criterion |

That last criterion is important. A rigorous result showing “no measurable improvement,” “improvement only on ambiguous task class,” or “better correctness at unacceptable overhead” is still a successful comparative-evaluation project. The primary success criterion is the ability to answer whether semantic decisions add measurable value, at what reliability/latency/token/cost overhead, with explicit uncertainty and limitations.

---

# Recommended frozen research questions

For Phase 1, the specification should freeze these questions before the full corpus is executed:

| ID | Research question |
|---|---|
| RQ1 | On independently labeled routing cases, how does TypeSafe `routing.task_class` correctness compare with current deterministic classification? |
| RQ2 | How does TypeSafe Noul evidence compare with deterministic heuristics for identifying genuinely missing material user interaction/authorization? |
| RQ3 | How accurately does TypeSafe `routing.semantic_risk` estimate independently adjudicated interpretation consequence, and is its probability evidence calibrated? |
| RQ4 | How often do semantic decisions disagree with deterministic control, and how often are those disagreements beneficial, harmful, or operationally redundant? |
| RQ5 | What are TypeSafe's success, no-match, uncertainty, fallback, timeout, error and retry rates under the frozen cohort? |
| RQ6 | What provider latency, token and cost overhead is incurred per batched case and per eligible decision? |
| RQ7 | Are the TypeSafe probability outputs sufficiently calibrated to support the existing or a future deterministic confidence policy? |

This design directly addresses the handoff's stated goal: move comparative evaluation from an implemented-but-lightly-exercised capability to a reproducible, statistically defensible evaluation system rather than merely adding more metrics.