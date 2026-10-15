# Comparative Evaluation — P0B Completion / P1 Handoff

**Date:** 2026-09-26  
**Checkpoint:** `comparative-study-v4`  
**Supersedes execution sequencing in:** `docs/checkpoints/2026-09-25-comparative-study-v3-checkpoint.md`

## Completion state

The independent-oracle phase is complete on the private Debian host evidence path.

Operator-reported completed gates:

- P0A authenticated Inspect qualification completed against `openai-api/codex-lb/deepseek-flash`;
- IA-1 through IA-8 reported passing;
- the previously frozen runtime lock was preserved across adjudicator-model correction;
- real A/B adjudication completed against the exact frozen authoring view;
- A/B disagreements were extracted only after both passes completed;
- independent C adjudication completed on the blinded dispute-only view;
- genuine three-way conflicts were human-resolved under the frozen rubric;
- `oracle.json` was frozen;
- `oracle.json.manifest.json` was produced;
- the final oracle validated successfully against the frozen 120-case corpus.

The private adjudication artifacts remain outside the repository. This checkpoint does not reproduce their contents or publish private execution evidence.

## Frozen identities — unchanged

- study: `routing-semantic-v1`;
- study version: `1.1.0`;
- dataset: `routing-semantic-corpus-v1.0.0`;
- case count: 120;
- corpus SHA-256: `e4b33df3b3752b32cdb362833765cc8f0c9cc024473071209563d73284011280`;
- A/B authoring-view SHA-256: `a5a40224793a50d9371e9ae437e144b15812829ba1cd56a5564dc6ba28846a0a`;
- oracle protocol: `routing-semantic-oracle-v1.0.0`;
- TypeSafe question set: `routing/v2`;
- state projector: `routing-state/v2`;
- qualified adjudicator model: `openai-api/codex-lb/deepseek-flash`.

Do not regenerate or relabel the frozen oracle for P1/P2.

## Methodological limitation discovered during P0B

The frozen protocol permits independent adjudicator rationales during genuine three-way discussion, but the current Inspect A/B/C output contract persisted labels only. The completed cohort therefore preserved the independent labels but not the original model rationales.

Human three-way resolution used only:

- the verbatim frozen case;
- supplied metadata;
- the frozen decision-seam rubric;
- independent A/B/C labels.

Do not reconstruct or invent missing model rationales after the fact. Preserve this as a study limitation and correct the adjudication contract only in a future versioned study/cohort.

## Next phase: P1 development instrumentation smoke

Do **not** begin the full 120-case P2 run immediately.

P1 must first exercise a bounded live TypeSafe/Jev sample and verify the evidence chain before committing provider calls and study execution to the full corpus.

Required P1 assertions:

1. exactly one semantic provider request per successfully attempted case;
2. three per-seam observations per successful case;
3. provider request IDs are unique across cases;
4. Choice/Noul/Score probabilities or distributions survive canonical persistence;
5. provider and control failures remain explicit evidence rather than disappearing;
6. the frozen oracle is not loaded or visible during inference;
7. private credentials and raw provider HTTP are absent from public-safe evidence;
8. latency/token/cost accounting occurs once per batched request, not once per seam;
9. runtime identity reports the frozen `routing/v2` question set and `routing-state/v2` projector;
10. the smoke run can be discarded/repeated without modifying the frozen corpus or oracle.

## Important implementation gap before P1

The current `agent-workflow benchmark decision-study-run` implementation iterates every case in the supplied corpus. It does not currently provide a bounded case-count/sample selector suitable for the intended P1 smoke check.

Therefore the next engineering action is to add a deterministic, explicitly development-only P1 smoke path that:

- derives a small sample from the frozen corpus without mutating the canonical corpus;
- records the selected case IDs and source corpus hash;
- preserves the same runtime/question-set/projector path used by P2;
- cannot be confused with or published as the preregistered full study;
- validates the ten P1 assertions above;
- leaves the P2 full-run command unchanged.

Do not use the current all-cases `decision-study-run` command as a substitute for P1.

## P2 after P1 passes

Once the P1 instrumentation smoke passes:

1. execute all 120 frozen cases with the exact runtime/study identities;
2. keep the frozen oracle absent during inference;
3. join the frozen oracle only after inference completes;
4. generate correctness, calibration, disagreement, reliability, and request-efficiency metrics;
5. inspect every exclusion and denominator;
6. preserve uncertainty and limitations regardless of result direction;
7. prepare public-safe evidence.

## P3 after P2 completes

Publish sanitized evidence only:

- study/runtime identities;
- frozen corpus/oracle identities;
- denominators and exclusions;
- correctness/calibration/reliability/efficiency metrics;
- uncertainty;
- limitations;
- sanitized case-level evidence and reproducibility instructions.

A favorable TypeSafe/Jev result is not a publication gate.

## Immediate continuation summary

> P0A and P0B are complete. The independent oracle is frozen and validated. The next step is **not** the full 120-case comparative run; it is a bounded P1 live TypeSafe/Jev instrumentation smoke test. The current `decision-study-run` command runs the whole supplied corpus, so a deterministic development-only P1 smoke path should be implemented and verified first.
