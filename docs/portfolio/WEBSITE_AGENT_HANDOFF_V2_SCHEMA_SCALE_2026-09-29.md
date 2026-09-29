# Website Agent Handoff — v2 real-schema scale boundary

**Date:** 2026-09-29  
**Source study:** `routing-semantic-v2`  
**Public-safe status:** v21 qualification passed; real A/B/C has **not** started and is re-blocked by a later pre-live scale discovery

## Timeline update

Preserve the existing v19 → v20 → v21 sequence.

Add v22 after v21:

- v21 remains the first full IA-1 through IA-11 qualification pass for benchmark
  0.6.3, including sanitized proof that strict JSON-schema controls reached
  Codex-LB ingress.
- Before any real v2 oracle label was produced, a real-cohort readiness review
  examined the 120-case output schema.
- All 120 frozen cases share the same three eligible decision seams.
- The 0.6.3 schema generator nevertheless repeated the complete record schema
  once per case.
- The repeated representation serialized to 225,971 characters; the equivalent
  eligibility-grouped representation serialized to 3,310 characters, a 98.54%
  reduction while preserving all 120 allowed case identities.
- Benchmark 0.6.4 introduces the representation-only grouped strategy
  `eligibility-grouped-case-enum/v1`.
- A fresh live qualification is required before real A/B because the model-facing
  schema implementation changed.

## Editorial framing

This is another example of the project’s intended timeline style:

**Belief / intended invariant**  
The two-case full qualification established the structured-output contract and
transport needed before the real cohort.

**Evidence**  
At real-cohort readiness review, the 120-case schema expanded to roughly 226 KB
because an identical record shape was repeated per case.

**What changed**  
Cases are grouped by identical eligible-decision sets; exact case coverage remains
an unchanged deterministic post-generation invariant. The new schema strategy is
version-bound into qualification evidence so the older pass cannot authorize the
new implementation.

**Next action**  
Pass CI for benchmark 0.6.4, rerun the full private qualification with sanitized
ingress proof, then—and only then—start real A/B.

## Public claim boundary

Safe:

> The first full qualification passed, but a later pre-cohort scale review found
> that the same schema representation expanded unnecessarily at 120 cases. The
> implementation was compacted by eligibility shape and deliberately requires
> requalification before real labels are produced.

Avoid:

- “v21 was invalid”;
- “the qualification failed to catch a bug” without the scale qualification;
- “the 226 KB schema would definitely have failed at the provider”;
- “real v2 A/B is running”;
- “the provider imposed a schema-size limit.”

The evidence establishes unnecessary schema expansion and an untested real-scale
boundary. It does not establish that a provider would reject the 226 KB schema.

## Source artifacts

- `docs/checkpoints/2026-09-29-comparative-study-v21-v2-full-qualification-pass.md`
- `docs/checkpoints/2026-09-29-comparative-study-v22-v2-real-schema-scale-boundary.md`
- `docs/portfolio/COMPARATIVE_STUDY_PROGRESS.md`

Do not publish private qualification manifests, host paths, model completions,
Inspect logs, or raw ingress artifacts.
