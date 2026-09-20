# Validation Report

## Result

`agent-workflow-comparative-eval` 0.1.0 source candidate is qualified for repository commit/release preparation.

## Library tests

- Python compile of `src/` and `tests/`: passed.
- Library unit/contract suite: **19 passed**.
- JSON Schema meta-validation for canonical and legacy schemas: passed.
- Installed-wheel smoke: passed.
- Source-distribution content smoke: passed.

## Consumer qualification

### agent-workflow-typesafe 0.1.1 adoption source

Executed with the real shared library on `PYTHONPATH` plus the Agent-Workflow public plugin API:

- **16 passed, 1 skipped**.
- The skipped test is the existing explicit live TypeSafe provider contract test; it requires an external credential/service and is not a shared-library responsibility.
- Base TypeSafe semantic behavior, plugin descriptor behavior, legacy evaluation facade, and neutral shared-library delegation passed.

### Agent-Workflow 0.10.1 adoption source

- Base/fallback migration suite with the shared library absent: **5 passed**.
- Real-library integration smoke: passed.
- Verified neutral observation construction, SQLite evidence persistence, shadow capture, delayed lifecycle outcome join, cohort reporting, and raw-input privacy boundary.

## Direct source-semantic parity

Passed against the reviewed original implementations:

- canonical JSON/SHA-256 behavior matches the TypeSafe 0.1.0 generic evaluation implementation;
- `routing-v1.0.0` and `skill-behavior-v1.0.0` resource bytes are identical to the TypeSafe plugin copies;
- Agent-Workflow usage normalization parity passed for API, cached-token/pricing, subscription/not-attributable, and missing-evidence vectors;
- deterministic paired bootstrap matches `agent_workflow.benchmarking.statistics`;
- 95% Wilson intervals match `agent_workflow.eval.compare`;
- observation input digests, normalized control/candidate results, authority flags, and privacy flags match the legacy implementation, with only the intended neutral schema namespace differing.

## Dependency audit

AST import audit passed: the library imports none of:

- `agent_workflow`
- `agent_workflow_typesafe`
- `typesafe_sdk`

Runtime dependency is limited to `jsonschema>=4.18,<5` plus the Python standard library.

## Scope boundaries retained

The library does **not** own:

- Agent Run/workflow lifecycle authority;
- routing/model/executor enforcement;
- host persistence policy;
- review or acceptance;
- TypeSafe/Jev projection, questions, SDK calls, credentials, or provider telemetry.

The source candidate intentionally does not invent a Git commit or release tag. A `library-release-handoff/v1` should be emitted only after this source is committed and tagged in the new repository.
