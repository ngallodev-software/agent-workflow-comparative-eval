# Comparative Evaluation — v2 Qualification Study-Identity Hotfix

**Date:** 2026-09-28  
**Checkpoint:** `comparative-study-v16`  
**Relationship to v15:** additive live-qualification failure record and tooling correction. v15 remains the record that the frozen v2 qualification tooling was released and ready to run.

## Observed live failure

The first full `routing-semantic-v2` IA-1 through IA-11 qualification attempt successfully created the frozen cohort runtime lock and then stopped before any qualification evidence run began.

Observed runtime lock:

- path: `/lump/apps/agent-workflow/.venv/.xdg/data/agent-workflow/routing-semantic-v2-qualification/runtime-lock.json`;
- SHA-256: `55bd5156194f9a8dbc0c05433a1130d4d6ad404c97d68c779a783d26769babd1`;
- module: `routing-semantic-v2-oracle-inspect` `2.0.0`;
- module SHA-256: `7c0f948e91dd9fd90c3b993220d9f53d3da65bdba162fe31605bc4dccc69ec27`;
- Inspect AI: `0.3.268`;
- Inspect SWE: `0.2.70`;
- Codex CLI: `0.158.0`, resolved once under the frozen `latest-at-cohort-start` policy;
- Docker: `29.8.1`;
- Docker Compose: `v5.5.1`;
- `frozen_for_cohort: true`.

Immediately after runtime-lock creation the qualifier failed with:

~~~text
error: unsupported Inspect qualification study: empty
~~~

No real A/B/C adjudication began.

## Root cause

`validate_abc_adjudication_module()` intentionally returns a flattened validated summary. Study identity is exposed as the top-level field:

~~~text
study_id
~~~

The live qualification path incorrectly treated that validated summary as though it were the raw module document and attempted to read:

~~~text
module["task"]["study_id"]
~~~

The same shape mismatch also existed in the later guard that requires a passing qualification before real Inspect adjudication.

The error therefore occurred before the synthetic IA qualification evidence directory was created. The frozen runtime lock itself was valid and remained bound to the unchanged module SHA.

## Correction

Benchmark `0.6.1` changes both affected qualification paths to resolve study identity from the validator's actual top-level `study_id`.

The patch also:

- centralizes the validated-study resolver;
- fails closed when study identity is absent or unsupported;
- adds regression coverage proving the validator summary is intentionally flat;
- updates `v2-qualify.sh` to require benchmark `0.6.1`.

Benchmark hotfix merge:

`05dbc2d782013a1f99957034b5de59ebe29b1778`

The benchmark CI passed:

- core tests/build;
- Inspect import and guardrail probe;
- agentic-Jev import.

Agent-Workflow's coordinated stack installer was then advanced from benchmark `0.6.0` to `0.6.1` without changing Agent-Workflow's own `0.11.12` runtime/API identity.

Agent-Workflow stack-pin merge:

`2a06934c184db6a8433cefe50dc5b8bc43309cab`

Its Linux Python 3.11/3.12/3.13, macOS, and Windows CI matrix passed.

## Runtime-lock disposition

The existing runtime lock is retained and should be reused.

Reason:

- its module SHA is unchanged;
- the Inspect/Inspect-SWE/Codex/Docker identities it froze are unchanged;
- the failure occurred after lock creation but before live qualification evidence execution;
- benchmark `0.6.1` changes qualification control-flow/identity lookup, not the adjudication module or runtime-lock semantics.

A rerun should therefore report that it is reusing:

~~~text
55bd5156194f9a8dbc0c05433a1130d4d6ad404c97d68c779a783d26769babd1
~~~

rather than resolving a new Codex cohort.

## Next action

Update the coordinated stack and rerun:

~~~bash
cd /lump/apps/agent-workflow
git pull --ff-only origin master
bash scripts/build-install-all.sh --venv /lump/apps/agent-workflow/.venv

cd /lump/apps/agent-workflow-benchmark

export CODEX_LB_BASE_URL='http://127.0.0.1:2455/v1'
export CODEX_LB_API_KEY='inspect-placeholder'
export V2_ADJUDICATION_MODEL='openai-api/codex-lb/deepseek-flash'

bash scripts/adjudication/v2-qualify.sh
~~~

Do not set `FORCE_V2_QUALIFICATION=1` for this rerun unless the script reports that qualification evidence already exists. The failed attempt did not reach the evidence-root creation point.

## Claim boundary

Safe claim:

> The first full v2 qualification attempt successfully froze the cohort runtime but exposed a benchmark study-identity plumbing defect before qualification execution. The defect was corrected in benchmark 0.6.1, the coordinated stack pin was updated, and the original frozen runtime lock remains valid for the rerun.

Not yet safe:

> routing-semantic-v2 has passed IA-1 through IA-11.

That statement remains blocked on the corrected live qualification run.
