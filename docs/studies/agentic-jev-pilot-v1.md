# Agent-Directed Jev Pilot v1

**Status:** development pilot; no effectiveness claim  
**Study version:** `0.1.0-draft.2`  
**Target:** 24 public-safe repository tasks × 3 arms

## Research question

V1 tested **application-directed Jev** at three predefined routing seams.

This pilot tests a different architecture:

> If Codex has TypeSafe decision guidance and a callable Jev primitive, where does the coding agent itself decide Jev is useful?

## Arms

| Arm | Codex | TypeSafe skill | Live Jev tool |
| --- | --- | --- | --- |
| A — baseline | yes | no | no |
| B — skill only | yes | yes | no |
| C — skill + Jev | yes | yes | yes |

Arm B is required because otherwise an observed behavior change could be caused by the skill instructions rather than the live Jev calls.

## Frozen coding-agent treatment

All three arms use the same coding-agent identity:

- model: **GPT-6 Luna**;
- provider path: `openai-api/codex-lb/gpt-6-luna`;
- reasoning effort: **high**;
- API path: Responses API;
- Codex model configuration: `gpt-6-luna`;
- minimum Codex CLI version: `0.155.0`.

Reasoning effort is supplied through Inspect's generation configuration. It is not stored inside provider/model-construction arguments.

This pilot is a new exploratory treatment, so it does not inherit the DeepSeek adjudicator identity from routing-semantic-v1/v2. DeepSeek remains the v2 adjudication model to preserve methodological-replication continuity; Luna is frozen only for the new agent-directed Jev pilot.

The same Luna/runtime/reasoning identity is mandatory across A/B/C. The treatment changes are therefore restricted to TypeSafe skill availability and live Jev availability.

## Harness boundary

Keep the existing Inspect/Inspect-SWE Codex harness.

For Arm C, expose one host-side Inspect bridged tool backed by the TypeSafe SDK. The sandbox sees only the MCP tool. `TYPESAFE_API_KEY` stays on the host and is never injected into the Codex container.

The frozen skill snapshot comes from:

- repository: `typesafe-ai/skills`;
- commit: `65a39f393687675ce170e6094757de20370365b9`;
- release: `v0.5.7`.

## Tool contract

The tool accepts:

- bounded JSON state;
- one or more typed TypeSafe questions using `choice`, `noul`, and/or `score`;
- an optional requested model.

It returns only normalized typed answers, probabilities/confidence where supplied, resolved model, request identity, usage, and duration.

It must redact secret-like state fields before transport/logging and must record an append-only private tool-call receipt.

## Pilot tasks

Do not freeze the final 24 tasks until the harness passes a synthetic tool qualification.

Task authoring should intentionally include plausible opportunities for:

- interaction/escalation;
- tool or skill selection;
- test prioritization;
- retrieval/context relevance;
- semantic consequence/risk;
- evidence sufficiency;
- ambiguous task classification;
- selection among candidate implementation/recovery strategies.

The pilot is exploratory. Opportunity tags are authoring metadata and must not be shown to the agent.

## Evidence to collect

For every arm/task:

- exact model/runtime identity;
- skill identity/hash and whether it was installed;
- tool availability;
- Jev tool-call count;
- primitive mix;
- request hash/id;
- latency/token/status;
- sanitized question/state shape;
- immediate action before/after tool result where observable;
- terminal task evidence.

## Exit criterion

The pilot ends with a decision about the full study, not a leaderboard.

The next study should freeze only those agentic Jev seams that show enough frequency, interpretability, and potential downstream consequence to justify controlled measurement.
