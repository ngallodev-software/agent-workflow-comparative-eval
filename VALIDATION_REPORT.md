# Validation Report

## Result

agent-workflow-comparative-eval 0.2.0 is qualified as the integration candidate for the routing-semantic-v1 comparative-decision study infrastructure.

This qualification covers library contracts/reporting and the current consumers. It does not constitute a completed Jev/TypeSafe effectiveness study; the independently frozen oracle corpus and full study run remain separate future evidence.

## Library validation

GitHub Actions run 36091963459 completed successfully at comparative-eval head 5d9543e071939e94ff9c9263a9253e1cb9cace7d.

- Python 3.11: 22 passed.
- Python 3.13: 22 passed.
- Wheel/source build: passed.
- JSON Schema meta-validation: covered by the contract suite.
- Legacy neutral-schema readers: passed.
- Decision-study contracts/reporting: passed.
- One provider request shared across three decision observations is deduplicated by request_id.
- Attempt-level candidate correctness retains timeout/error/no-decision cases in the denominator.
- Answered-only correctness and calibration are reported separately.
- Sample eligibility and calibration minimum-n gates are machine-readable.

## Current consumer qualification

### Agent-Workflow 0.11.10

Agent-Workflow head 1388dbf31672c55dd35c0fcc3a3293fbaf4cc69d passed CI run 36087815880 while installing the real comparative-eval 0.2.0 integration branch.

- Linux Python 3.11/3.12/3.13 full suites: passed.
- macOS Python 3.12 full suite: passed.
- Windows Python 3.12 release suite: passed.
- Linux Python 3.11 full suite: 307 passed.
- Technical release checks: passed.
- sdist/wheel build: passed.

The integration verifies:

- three lossless per-seam observations for routing.task_class, routing.interaction_required, and routing.semantic_risk;
- one shared provider-request record for the batched TypeSafe/Jev call;
- request ID, projector version, raw probabilities/confidence/distributions, request hash, and usage evidence surviving into DecisionEvidence/receipts;
- deterministic control remaining authoritative in comparative mode;
- raw task text not being persisted in the neutral SQLite evidence store;
- runtime and benchmark consumers sharing the same receipt-to-neutral-evidence projection.

### agent-workflow-benchmark 0.4.0

Benchmark head 1205b83d2621be3e6bcb566feaf6650d6fc88885 passed CI run 36087979473 against the Agent-Workflow 0.11.10 and comparative-eval 0.2.0 integration branches.

- Benchmark suite: 75 passed.
- sdist/wheel build: passed.
- Decision-study validation/run/report/publication test path: passed without network calls.

The benchmark integration verifies:

- inference execution has no oracle argument;
- run-manifest records oracle_seen_during_inference=false;
- oracle-like keys in inference metadata are rejected;
- one batched provider request yields three decision observations but one request-level usage/latency record;
- post-inference oracle joining is a separate reporting step;
- below-threshold development evidence is marked study_eligible=false.

### Historical agent-workflow-typesafe 0.1.1

The historical standalone provider compatibility remains recorded for legacy schema/adoption provenance. It is not the current runtime ownership boundary.

## Dependency audit

The comparative-eval library imports none of:

- agent_workflow
- agent_workflow_typesafe
- typesafe_sdk

Runtime dependency remains jsonschema>=4.18,<5 plus the Python standard library.

## Scope boundaries retained

The library does not own:

- Agent Run/workflow lifecycle authority;
- routing/model/executor enforcement;
- host persistence policy;
- review or acceptance;
- TypeSafe/Jev projection, question definitions, SDK calls, credentials, or provider transport.

Agent-Workflow owns workflow/application policy. TypeSafe/Jev supplies typed semantic evidence. The benchmark owns experimental execution. This library owns provider-neutral evidence and comparison semantics.

## Remaining empirical gate

The implementation stack is qualified, but the first publishable comparative-decision result still requires:

1. frozen public-safe routing corpus;
2. independently authored/blinded oracle;
3. at least 100 oracle-eligible cases per seam, target 120 shared cases;
4. development instrumentation run;
5. full preregistered study;
6. sanitized public evidence publication.

No current qualification result establishes that Jev/TypeSafe improves correctness, latency, token use, cost, or downstream software quality.
