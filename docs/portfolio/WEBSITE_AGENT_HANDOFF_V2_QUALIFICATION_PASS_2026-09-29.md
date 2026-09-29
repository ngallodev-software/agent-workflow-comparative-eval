# Website Agent Handoff — routing-semantic-v2 qualification recovery

**Date:** 2026-09-29  
**Source study:** `routing-semantic-v2`  
**Public-safe status:** full live qualification passed; real v2 oracle cohort not yet run

## What changed

The methodological-replication oracle work reached its first complete live qualification
pass after two preserved integration failures.

The public timeline should keep the sequence intact:

1. v19 discovered that the pinned Inspect bridge could silently drop unsupported
   JSON Schema keywords, producing a malformed transported schema before any
   adjudication sample completed.
2. v20 progressed past that boundary but a synthetic C tiebreaker returned prose
   before its JSON object. The strict parser rejected it rather than salvaging the
   embedded JSON.
3. v21 added a sanitized loopback ingress diagnostic and reran the complete
   qualification. The retry passed IA-1 through IA-11.

Do not rewrite v19/v20 as obsolete mistakes. They are the evidence trail that led
to the stronger qualification boundary.

## Public-safe evidence from v21

The passing qualification reported:

- `qualified=true`;
- IA-1 through IA-11 all `pass`;
- primary A/B, qualification C, and the IA-9/10/11 evidence-preflight A/B/C all
  returned JSON-object-only terminal completions;
- a sanitized Codex-LB ingress capture observed 15 `POST /v1/responses`
  requests;
- every captured structured-output request used `text.format.type=json_schema`
  with `strict=true`;
- captured schema hashes matched the exact persisted primary/C schema artifacts;
- no prompt, response, tool argument, credential, or full schema was retained in
  the public-safe capture summary.

Agent-Workflow Benchmark PR #71 subsequently merged as
`9ef7f055b3475929ea95d3b2c7509b457c6299df`.

## Important interpretation boundary

Do not claim that v20's earlier prose-plus-JSON failure has been root-caused to
DeepSeek or Codex-LB.

The passing capture proves that the current strengthened path can transport the
strict schema correctly to Codex-LB ingress. The failed v20 attempt predates that
capture, so its exact provider-facing request is unknown.

Safe wording:

> A later captured retry verified the strict JSON-schema request end to end to
> the local provider gateway and passed all qualification gates. The earlier
> prose-plus-JSON failure remains preserved as intermittent enforcement evidence
> rather than being retroactively explained away.

Avoid wording such as:

- "DeepSeek ignored the schema";
- "Codex-LB dropped strict mode";
- "the provider bug was fixed";
- "structured output is now guaranteed."

## Suggested Lab Notes / timeline treatment

This milestone fits the existing editorial sequence:

**Belief / intended invariant**  
A frozen structured-output contract should either yield a whole JSON object or
fail closed before experimental evidence is admitted.

**Evidence**  
The first strengthened attempt failed on lossy schema transport; a later C
attempt returned prose plus JSON; the captured retry then showed exact
`json_schema + strict=true` transport and passed IA-1 through IA-11.

**What changed**  
The benchmark gained representability checks, strict whole-completion parsing,
durable private diagnostics, exact attempt identity, quiet logging, and a
sanitized ingress capture that hashes schemas without retaining prompts or
responses.

**Next action**  
Run the real `routing-semantic-v2` A/B/C oracle cohort under the now-qualified
contract. Preserve any recurrence instead of retrying it away silently.

## Source links

Use these repository artifacts as the public source of truth:

- `docs/checkpoints/2026-09-29-comparative-study-v19-v2-inspect-schema-bridge-failure.md`
- `docs/checkpoints/2026-09-29-comparative-study-v20-v2-native-structured-output-enforcement-failure.md`
- `docs/checkpoints/2026-09-29-comparative-study-v21-v2-full-qualification-pass.md`
- `docs/portfolio/COMPARATIVE_STUDY_PROGRESS.md`

The private qualification manifest, Inspect logs, raw completions, and host paths
must not be linked or published.
