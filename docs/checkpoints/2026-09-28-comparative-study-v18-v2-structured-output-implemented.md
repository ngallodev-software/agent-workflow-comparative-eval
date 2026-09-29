# Comparative Evaluation — v2 Structured Final-Output Enforcement Implemented

**Date:** 2026-09-28  
**Checkpoint:** `comparative-study-v18`  
**Relationship to v17:** additive implementation milestone. v17 remains the historical record of the live framing-contract failure that motivated this change.

## Boundary at this checkpoint

Generation-time structured final-output enforcement has now been implemented and released for the `routing-semantic-v2` Codex/Inspect adjudication path.

This checkpoint does **not** claim that the strengthened runtime has passed live IA-1 through IA-11 qualification yet.

Real A/B/C remains blocked until the new runtime is frozen, the full qualification is rerun, and the resulting artifacts are inspected.

## Why this change exists

The v17 qualification attempt demonstrated a specific failure:

- the adjudicator returned a semantically complete JSON adjudication body;
- one prose sentence preceded that JSON;
- the strict whole-completion parser rejected the result.

The benchmark intentionally did not:

- strip the prose;
- search for the first JSON object;
- normalize fenced or mixed-format output;
- retry until the model happened to frame the answer correctly.

The stronger correction is to constrain the final response at generation time while retaining strict downstream validation.

## Upstream capability investigation

The relevant released/runtime versions were checked before implementation.

At this checkpoint:

- latest released Inspect-SWE: `0.2.71`;
- previously pinned Inspect-SWE: `0.2.70`;
- latest released Inspect AI observed during the investigation: `0.3.272`;
- benchmark continues to pin Inspect AI `0.3.268` for this study.

Neither Inspect-SWE `0.2.71` nor current Inspect-SWE `main` exposes a final-output-schema argument on `codex_cli()`.

Inspect AI has structured-response machinery, but that surface does not by itself constrain the final Codex CLI answer when the agent is executed through Inspect-SWE's bridged `codex_cli()` wrapper.

Codex CLI itself already supports:

~~~text
codex exec --output-schema <FILE>
~~~

No existing Inspect-SWE issue or pull request was found for exposing that exact capability through `codex_cli()`.

An upstream feature request was therefore filed:

**meridianlabs-ai/inspect_swe#176 — “Expose Codex final-output JSON schema (`--output-schema`) from `codex_cli()`”**

The local compatibility layer is intentionally temporary and should be retired once an appropriate upstream capability is released and qualified.

## Benchmark implementation

Benchmark `0.6.2` implements the strengthened boundary.

Merge:

`4b48eaf23b35f2cb7eb6b6458f1cadbf2e99044c`

### Pinned Inspect-SWE compatibility capability

The benchmark now contains a minimal compatibility layer for Inspect-SWE `0.2.71`.

It is deliberately fail-closed.

The patch applies only when the installed upstream `codex_cli.py` matches the exact released `0.2.71` Git blob:

`a5c5f21207d2fee496b8ef775c07757e2c524725`

If upstream source bytes differ, the patch refuses to mutate them.

The compatibility layer adds only the missing final-output-schema seam:

~~~python
codex_cli(..., output_schema=<JSON Schema>)
~~~

For headless Codex execution it:

1. serializes the supplied schema deterministically inside `CODEX_HOME`;
2. invokes native Codex with `--output-schema <schema-path>`;
3. leaves the existing Inspect-SWE bridge/model-accounting path intact.

Centaur mode is rejected when `output_schema` is supplied because that mode does not have the same unattended final-response boundary.

Capability identity:

`agent-workflow-benchmark/inspect-swe-codex-output-schema/v1`

### Exact per-view result schemas

The benchmark now derives the final-output JSON Schema from the actual assigned v2 view.

For A/B, the schema binds:

- the exact assigned case IDs;
- the exact required decision seams for each case;
- the allowed label domains for categorical, boolean, and ordinal seams;
- one structured justification for each assigned seam;
- `decisive_case_evidence` as 1-3 strings;
- each evidence string at most 320 characters;
- one bounded `rubric_rule`;
- the frozen `ambiguity` enum.

For C, the same mechanism derives a dispute-specific schema from the blinded dispute view rather than reusing the A/B schema.

### Defense in depth remains intact

Generation-time enforcement does not replace benchmark validation.

The post-generation chain remains:

~~~text
native Codex output-schema enforcement
  -> exact whole-completion JSON parse
  -> exact case/seam set validation
  -> label-domain validation
  -> structured-justification validation
  -> blindness/attestation checks
  -> IA evidence/provenance
~~~

A prose-prefixed JSON completion remains invalid and is covered by regression testing.

No permissive JSON extraction fallback was added.

### Runtime-lock strengthening

For `routing-semantic-v2`, the runtime lock must now include structured-output identity:

- mode: `codex-output-schema`;
- capability ID;
- patched Inspect-SWE source SHA-256;
- expected upstream Inspect-SWE Git blob SHA-1.

Runtime-lock loading verifies that the installed patched source still matches the frozen source hash.

Therefore the prior runtime lock:

`55bd5156194f9a8dbc0c05433a1130d4d6ad404c97d68c779a783d26769babd1`

is intentionally obsolete under the strengthened executable runtime.

It must be preserved as historical evidence and archived during the next deliberate qualification retry, not reused.

### Qualification evidence

The strengthened qualifier records:

- structured-output runtime identity in IA-1;
- primary A/B result-schema SHA in IA-2;
- C dispute-result-schema SHA in IA-7;
- structured-output enforcement plus A/B and C schema hashes in IA-9 evidence.

Schema artifacts are persisted alongside the Inspect logs.

## Automated verification

Benchmark CI passed before merge.

The strongest non-live runtime test used an actual installed Inspect-SWE `0.2.71` wheel and:

1. installed the benchmark Inspect extras;
2. applied the pinned compatibility patch;
3. verified Inspect AI `0.3.268`;
4. verified Inspect-SWE `0.2.71`;
5. introspected `inspect_swe.codex_cli` and confirmed the `output_schema` parameter exists;
6. verified the benchmark runtime-capability assertion;
7. ran the Inspect import/guardrail lane successfully.

The benchmark core unit/build lane and agentic-Jev import lane also passed.

The agentic-Jev runtime-lock schema was advanced to Inspect-SWE `0.2.71` so the shared Inspect runtime identity remains coherent.

This automated evidence proves installation, patch application, runtime introspection, schema generation, fail-closed parsing, and qualification wiring.

It does **not** substitute for a live Codex-LB/DeepSeek structured-output run.

## Coordinated Agent-Workflow installer

Agent-Workflow remains `0.11.12`; no Agent-Workflow runtime API or public contract was changed.

The coordinated stack installer was updated and merged at:

`38dc43360ff9853c71ca488ded9622ba18673343`

The installer now freezes:

- Agent-Workflow `0.11.12`;
- comparative-eval `0.3.1`;
- SpecGen `0.2.12`;
- benchmark `0.6.2`;
- Inspect AI `0.3.268`;
- Inspect-SWE `0.2.71`;
- TypeSafe SDK `0.6.0`.

After installing the benchmark wheel, the stack installer installs the exact Inspect runtime pins and applies the pinned Inspect-SWE output-schema compatibility patch.

Final stack verification asserts the structured-output capability before declaring the installation healthy.

The coordinated Agent-Workflow CI matrix passed Linux Python 3.11/3.12/3.13, macOS, and Windows before merge.

## Durable trackers

Two trackers now exist for the strengthened boundary:

1. **agent-workflow-benchmark#69** — local implementation/live-validation tracker. Keep open until live qualification proves the strengthened path.
2. **meridianlabs-ai/inspect_swe#176** — upstream request for native `codex_cli(output_schema=...)` support. The local compatibility patch should be retired when an upstream release provides an equivalent qualified capability.

## Next live action

Update the coordinated stack, then rerun qualification as a deliberate archived retry:

~~~bash
cd /lump/apps/agent-workflow
git pull --ff-only origin master

bash scripts/build-install-all.sh \
  --venv /lump/apps/agent-workflow/.venv

cd /lump/apps/agent-workflow-benchmark

export CODEX_LB_BASE_URL='http://127.0.0.1:2455/v1'
export CODEX_LB_API_KEY='inspect-placeholder'
export V2_ADJUDICATION_MODEL='openai-api/codex-lb/deepseek-flash'

FORCE_V2_QUALIFICATION=1 \
  bash scripts/adjudication/v2-qualify.sh
~~~

The forced retry is required because:

- the prior failed qualification evidence must be retained and archived;
- the prior runtime lock describes the pre-structured-output executable runtime;
- the strengthened runtime must freeze a new lock.

Expected early behavior is:

1. prior qualification evidence archived under a timestamped retry directory;
2. prior incompatible runtime lock archived with it;
3. a new v2 runtime lock created containing `structured_output` identity;
4. qualification executed under that new lock.

## Phase map

~~~text
routing-semantic-v2 2.0.0
  frozen study/dataset/protocol       COMPLETE
  frozen blinded authoring view       COMPLETE
  framing-contract failure            FOUND / PRESERVED
  upstream capability gap             CONFIRMED
  Inspect-SWE upstream request #176   OPEN
  local structured-output capability  IMPLEMENTED / RELEASED
  benchmark                           0.6.2 / RELEASED
  coordinated installer               RELEASED / CI GREEN
  new structured runtime lock         NEXT
  live IA-1..IA-11 qualification      NEXT
  qualification artifact review       BLOCKED ON LIVE RUN
  real A/B/C                          BLOCKED
~~~

## Claim boundary

Safe claim:

> Generation-time Codex final-output schema enforcement is implemented, byte-pinned to released Inspect-SWE 0.2.71, integrated into benchmark qualification/runtime evidence, and verified by automated installation and runtime-capability tests.

Not yet safe:

> The strengthened DeepSeek/Codex runtime has passed live IA-1 through IA-11 qualification.

That remains the next live proof.
