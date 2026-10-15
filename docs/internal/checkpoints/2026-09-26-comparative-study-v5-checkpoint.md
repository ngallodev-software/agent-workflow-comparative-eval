# Comparative Evaluation — P1 Completion / P2 Handoff

**Date:** 2026-09-26  
**Checkpoint:** `comparative-study-v5`  
**Supersedes execution sequencing in:** `docs/checkpoints/2026-09-26-comparative-study-v4-checkpoint.md`

## Phase state

P0A and P0B remain complete. The independent oracle remains frozen and validated.

## Oracle-baseline execution provenance and API accounting

The initial qualification/adjudication runs through and including P0B oracle freeze used this execution path:

`OpenAI Codex harness -> codex-lb load balancer -> DeepSeek-4.1-Flash API`

The adjudication runtime path/alias recorded elsewhere remains `openai-api/codex-lb/deepseek-flash`.

Cumulative provider/API metrics through oracle freeze:

- cost: **$0.07 USD**;
- API requests: **36**;
- tokens: **726,263**.

Scope boundary: these metrics cover the oracle-baseline work through P0B freeze only. They exclude the P1 TypeSafe/Jev smoke, P2 full comparative inference, and P3 publication. The values are operator-recorded provider/API accounting; committed raw billing traffic is not the source artifact.

Durable evidence: `docs/evidence/oracle-baseline-api-usage-2026-09-26.md` and `docs/evidence/oracle-baseline-api-usage-2026-09-26.json`.

P1 development instrumentation smoke is now complete and passed.

Verified P1 evidence:

- cases: 8;
- observed cases: 8;
- provider requests: 8;
- per-seam observations: 24;
- exclusions: 0;
- verification status: `pass`;
- source corpus SHA-256: `e4b33df3b3752b32cdb362833765cc8f0c9cc024473071209563d73284011280`.

The P1 artifact is explicitly marked `development_only: true`.

## P1 invariants that passed

The completed smoke verified:

1. one provider request per observed case;
2. three observations per observed case;
3. unique provider request IDs;
4. semantic probability/distribution evidence survives persistence;
5. failures remain explicit evidence;
6. the oracle is absent during inference;
7. public-safe persistence preserves the privacy boundary;
8. request-level usage is not triple-counted across seams;
9. question set identity is `routing/v2`;
10. projector identity is `routing-state/v2`.

P1 therefore validates the evidence path needed for the full study. It does **not** provide comparative-effectiveness results because the smoke sample is deliberately below the preregistered study threshold.

## P2 is now unblocked

The next execution step is the full preregistered 120-case comparative study.

Preferred operator entry point in Agent-Workflow Benchmark:

~~~bash
bash scripts/decision-study/p2-all.sh
~~~

The P2 workflow must preserve these rules:

- execute the exact frozen 120-case corpus;
- do not provide the frozen oracle to inference;
- preserve exact `routing/v2` question-set identity;
- preserve exact `routing-state/v2` projector identity;
- retain every provider/control failure as explicit evidence;
- preserve request-level latency/token/cost accounting;
- join the frozen oracle only after inference completes;
- generate correctness, calibration, disagreement, reliability, and efficiency reports;
- inspect denominators, exclusions, uncertainty, and limitations before publication.

## Current claim boundary

Safe to state publicly now:

- the independent oracle is frozen and validated;
- oracle-baseline API accounting through freeze is recorded as $0.07 USD, 36 DeepSeek-4.1-Flash API requests, and 726,263 tokens via the OpenAI Codex harness -> `codex-lb` path;
- the live TypeSafe/Jev instrumentation path passed a bounded development smoke;
- P1 produced 8 provider requests and 24 per-seam observations with 0 exclusions;
- the smoke verified oracle separation, privacy boundaries, probability persistence, and request-level accounting;
- P2 is now ready to run.

Still not safe to claim:

- TypeSafe/Jev is more accurate than deterministic routing;
- TypeSafe/Jev reduces routing errors;
- semantic routing is better calibrated;
- latency/cost overhead is acceptable or superior;
- either arm won;
- the full 120-case study has been executed.

Those require P2 evidence.

## Website synthesis handoff

The current website-agent source is:

`docs/portfolio/WEBSITE_AGENT_HANDOFF_2026-09-26.md`

It now distinguishes:

~~~text
P0A  COMPLETE
P0B  COMPLETE
P1   PASS
P2   UNBLOCKED / NOT YET RUN
P3   PENDING P2
~~~

Website synthesis may present P1 as an evidence-path validation milestone, but must not reinterpret the development smoke as an outcome study.

## Immediate continuation summary

> The blinded independent oracle is frozen and validated. The bounded live P1 instrumentation smoke passed with 8 cases, 24 observations, 8 provider requests, and 0 exclusions. All persistence, privacy, oracle-separation, probability, request-identity, and accounting checks passed. The full 120-case P2 comparative study is now unblocked; run `bash scripts/decision-study/p2-all.sh` from Agent-Workflow Benchmark.
