# Agent-Directed Jev Pilot v1

**Status:** development pilot; no effectiveness claim  
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
