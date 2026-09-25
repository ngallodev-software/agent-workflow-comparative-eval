# Comparative Evaluation — Unified Continuation Checkpoint v3

**Date:** 2026-09-25  
**Checkpoint:** `comparative-study-v3`  
**Supersedes sequencing in:** `docs/checkpoints/2026-09-24-comparative-study-v2-checkpoint.md`

This checkpoint preserves all frozen study semantics from v2 and inserts one infrastructure qualification phase before the first real oracle adjudication.

## Governing rule

No real A/B oracle labels and no live TypeSafe/Jev comparative inference have been produced yet.

Therefore the adjudicator execution backend may still be improved **without changing the frozen study**, provided:

- corpus bytes/hash stay identical;
- blinded A/B authoring view bytes/hash stay identical;
- oracle protocol stays identical;
- output contracts stay identical;
- the backend is qualified before real labels are produced;
- the previous direct-Docker implementation remains a rollback/reference path.

## Current rollback/reference identities

| Repository | Branch | Commit | Meaning |
| --- | --- | --- | --- |
| `agent-workflow-comparative-eval` | master | `5652d24cdbd90c9d78c6ec5f9d7ddd39b008e15e` | canonical frozen oracle handoff |
| `agent-workflow-benchmark` | main | `0f5df45957eee12d6318b5a4b4590398aedc8083` | direct-Docker adjudication harness |
| `agent-workflow-benchmark` | main | `ac593ca879607bfd5ccbde81666fcb3c31b9aaa1` | A/B/C module contract + isolated-agent architecture |

Current Agent-Workflow and benchmark-results HEADs must still be re-audited before execution.

## Frozen semantic identities — unchanged

- study: `routing-semantic-v1`;
- study version: `1.1.0`;
- dataset: `routing-semantic-corpus-v1.0.0`;
- case count: 120;
- corpus SHA-256: `e4b33df3b3752b32cdb362833765cc8f0c9cc024473071209563d73284011280`;
- A/B authoring-view SHA-256: `a5a40224793a50d9371e9ae437e144b15812829ba1cd56a5564dc6ba28846a0a`;
- oracle protocol: `routing-semantic-oracle-v1.0.0`;
- TypeSafe question set: `routing/v2`;
- state projector: `routing-state/v2`.

Do not regenerate, relabel, or modify these during runtime integration.

## Why sequencing changed

The v2 checkpoint said the next action was:

`P0 — independent oracle`

Since then, the benchmark repository gained:

- a direct-Docker blinded A/B/C runner;
- a declarative A/B/C module schema;
- a routing-semantic-v1 module instance;
- isolation/credential guardrails;
- prior-art research identifying Inspect AI as a mature evaluation/sandbox orchestration framework.

Inspect AI can provide Docker sandbox lifecycle, model-provider abstraction, execution logging, retries/resume, and sandboxed CLI-agent bridging. Inspect SWE provides a Codex CLI adapter.

The implementation plan is owned by benchmark:

`docs/plans/2026-09-25-inspect-adjudication-integration-plan.md`

The direct-Docker runner remains the reference/rollback implementation.

## Revised phase map

### P0A — Inspect adjudication runtime integration and qualification

Complete before any real A/B labels.

Target runtime:

- `inspect-ai==0.3.268`;
- `inspect-swe==0.2.70`;
- Codex CLI `0.156.1`;
- Docker sandbox;
- host-side model/load-balancer credentials;
- sandboxed Codex connected through Inspect's agent bridge;
- web search/MCP/provider-side code execution withheld.

P0A must use only synthetic qualification fixtures, not the real 120-case authoring view for label generation.

Qualification must prove:

1. exact version/runtime identity;
2. user load-balancer connectivity;
3. provider credential absent from sandbox;
4. no `TYPESAFE_*` credential in adjudicator;
5. no repository or Docker socket mount;
6. no cross-agent filesystem visibility;
7. exact prompt/input/output-contract materialization;
8. deterministic parity with the reference backend using a stub agent;
9. A/B delayed-reveal behavior;
10. C dispute-only isolation;
11. failure/retry behavior does not violate role independence;
12. machine-readable qualification manifest is frozen.

If any required gate fails, use fresh direct-Docker A/B sessions for P0B.

Do not mix one backend's A pass with another backend's B pass in the same oracle cohort.

### P0B — independent oracle

After P0A is qualified:

1. verify canonical view SHA-256;
2. materialize identical A/B blinded inputs;
3. run A and B in separate fresh Inspect sandboxes/sessions;
4. validate both existing adjudication-pass/v1 artifacts;
5. compare only after both complete;
6. generate dispute-only C artifact;
7. run C only on disagreements in a fresh sandbox/session;
8. resolve true three-way conflicts under the frozen protocol;
9. preserve unresolved conflicts as `oracle_conflict_unresolved`;
10. freeze `oracle.json` and `oracle.json.manifest.json`;
11. validate the oracle against the frozen corpus;
12. archive Inspect execution provenance separately from the oracle.

### P1 — development instrumentation run

Unchanged from v2.

After oracle freeze, run a small live TypeSafe/Jev instrumentation check and verify:

- one provider request per case;
- three observations per successful case;
- unique request IDs;
- probability/distribution survival;
- failures preserved;
- oracle absent during inference;
- no secret/raw provider HTTP in public evidence;
- no latency/token/cost triple counting.

### P2 — full preregistered run

Unchanged from v2.

Run all 120 cases with exact runtime/study identities, join oracle only after inference, generate the report, inspect exclusions/eligibility, and prepare public-safe evidence regardless of outcome direction.

### P3 — sanitized publication

Publish:

- study/runtime identities;
- frozen oracle identity;
- denominators/exclusions;
- correctness/calibration/reliability/efficiency metrics;
- uncertainty;
- limitations;
- sanitized machine-readable evidence.

A favorable Jev outcome is not a publication gate.

### P4 — generic Inspect backend evaluation

Only after routing-semantic-v1 completes, determine whether the qualified Inspect backend should also execute:

- paired benchmark arms;
- blind implementation agents;
- independent scoring/reviewer panels;
- post-seal semantic evaluators.

Do not combine that migration with P0A.

## Inspect integration authority boundary

Inspect is execution infrastructure, not study authority.

Inspect may own:

- sandbox creation/destruction;
- Codex CLI process execution;
- model bridge;
- runtime limits;
- execution logs;
- retry/resume mechanics.

Agent-Workflow Benchmark must continue to own:

- module validation;
- frozen input hashes;
- A/B/C role identity;
- delayed reveal;
- disagreement extraction;
- majority/discussion logic;
- adjudication-pass contracts;
- oracle freeze;
- inference gate;
- publication/evidence contracts.

comparative-eval continues to own the neutral study/corpus/oracle semantics and evaluator/statistical contracts.

## Load-balancer credential direction

Preferred design:

~~~text
sandboxed Codex CLI
       |
       v
Inspect sandbox bridge on localhost
       |
       v
host Inspect model provider
       |
       v
user OpenAI-compatible load balancer
~~~

The load-balancer key/base URL should remain host-side where possible.

If the user's load balancer does not work with Inspect's OpenAI-compatible provider, implement an Inspect ModelAPI extension before falling back to exposing broad user Codex credentials in the sandbox.

## Do-not-regress additions

Retain every v2 do-not-regress item, plus:

- no real oracle labels during P0A qualification;
- no provider/load-balancer secret inside adjudicator sandbox;
- no TypeSafe credentials inside adjudicator sandbox;
- no web/MCP/provider-side code-execution capabilities;
- A/B use one qualified backend/runtime identity for the cohort;
- Inspect-native logs are supplementary, not the authoritative oracle contract;
- direct-Docker reference backend remains available until P0B completes.

## Next exact action

Implement benchmark P0A from:

`agent-workflow-benchmark/docs/plans/2026-09-25-inspect-adjudication-integration-plan.md`

Do not start `run-ab` on the real frozen 120-case authoring view until P0A produces a passing frozen qualification manifest.

## Immediate continuation summary

> The comparative study semantics remain frozen. The next action is no longer real A/B adjudication. First integrate and qualify Inspect AI/Inspect SWE as the preferred isolated adjudicator runtime using synthetic fixtures only, while retaining the merged direct-Docker runner as rollback. After the Inspect qualification manifest passes and is frozen, proceed to the real independent A/B/C oracle, then P1 instrumentation, P2 full inference, and P3 publication.
