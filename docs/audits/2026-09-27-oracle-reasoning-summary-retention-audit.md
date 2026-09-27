# Oracle Reasoning-Summary Retention Audit — Evidence Existed Outside the Authoritative Pass

**Date:** 2026-09-27  
**Study:** `routing-semantic-v1`  
**Classification:** methodological correction / evidence-path audit  
**Status:** post-freeze retrospective audit; frozen v1 oracle remains unchanged

## Executive summary

A follow-up audit of the retained private Inspect execution logs corrected an important overstatement in the 2026-09-26 decision-provenance postmortem.

The original finding was correct at the **authoritative adjudication-contract** level: the A/B/C `adjudication.json` passes preserved labels but no structured per-decision justification, and the human three-way-resolution workflow therefore did not receive the independent adjudicators' rationales.

However, the broader statement that the adjudicators' reasoning evidence was not retained anywhere was too strong.

The retained private Inspect `.eval` logs contain provider/model **reasoning-summary** events for the completed A/B/C cohort. Raw hidden chain-of-thought was not exposed. The summaries are supplementary execution evidence, not fields in the frozen adjudication pass and not evidence that was available to the human resolver at the time.

Therefore the precise failure is:

> The cohort retained reasoning-summary evidence in private execution logs, but the authoritative adjudication contract and resolution tooling failed to promote a bounded decision justification into the durable pass consumed by downstream adjudication.

This is still a material evidence-engineering failure. It is not a complete historical data-loss event.

## What the audit established

The retained cohort evidence establishes all of the following:

1. the Codex/Inspect bridge did not prevent reasoning-summary evidence from reaching the Inspect transcript;
2. the underlying provider path produced human-readable reasoning summaries during the actual cohort;
3. the authoritative adjudication prompt nevertheless required labels-only JSON and explicitly prohibited explanations/additional fields;
4. the pass wrapper parsed the final completion and retained only `case_id` plus `labels`;
5. the human conflict-resolution worksheet was generated from those reduced pass artifacts and therefore did not expose the private reasoning summaries;
6. the frozen oracle was produced from the labels/resolution procedure actually executed and must not be rewritten after P2.

## Raw reasoning versus reasoning summaries

This audit does **not** establish that hidden chain-of-thought was available or should have been collected.

The retained Inspect events expose provider-generated **reasoning summaries** while raw reasoning tokens remain redacted/opaque. Future study design should continue to avoid depending on hidden chain-of-thought.

The required evidence for a future cohort should be an explicit, bounded, provider-neutral **structured decision justification** produced alongside each label.

Reasoning summaries may be retained privately as supplementary execution evidence, but they should not be the authoritative rationale contract.

## Why the original human-resolution limitation remains real

The private summaries were not part of the adjudication pass consumed by the resolution tooling.

Consequently, the completed human resolution still operated on the reduced evidence set documented at the time:

- frozen case prompt;
- supplied metadata;
- frozen rubric;
- A/B/C labels.

Finding supplementary summaries later does not make them contemporaneous resolution evidence.

They must not be retroactively injected into `routing-semantic-oracle-v1.0.0`.

## Corrected evidence model

~~~text
provider/model execution
        |
        +--> private Inspect reasoning-summary events  [retained]
        |
        +--> final labels-only completion
                    |
                    v
             pass wrapper
                    |
                    v
        adjudication.json: case_id + labels
                    |
                    v
             resolution workflow
~~~

The broken edge was not model capability. It was promotion of useful execution evidence into the authoritative decision-provenance contract.

## Additional accounting finding

The same private-log audit surfaced a separate instrumentation issue in oracle provenance accounting.

The per-role `inspect-provenance.json` files persisted `sample.output.usage`, which represents the final output usage exposed on the sample output, rather than the aggregate model usage for the full multi-call adjudication session.

Therefore those provenance usage fields must not be interpreted as complete A/B/C session-token totals.

The existing operator-recorded provider/API accounting through oracle freeze remains the public aggregate accounting source:

- 36 API requests;
- 726,263 tokens;
- $0.07 USD provider/API cost.

A future runtime/provenance contract should persist both final-output usage and aggregate session/model usage with unambiguous field names.

## Required correction to the 2026-09-26 postmortem

The earlier postmortem remains useful because it accurately records what the normal adjudication artifacts and human resolver had available.

Where it says or implies that original reasoning evidence was never retained anywhere, read that as superseded by this audit.

The durable limitation is now:

- authoritative per-decision structured justification: **not retained**;
- private reasoning-summary execution evidence: **retained**;
- available to the original human resolution workflow: **no**;
- raw hidden chain-of-thought: **not claimed / not required**;
- safe to retrofit into frozen oracle: **no**.

## Future cohort requirements

A future versioned oracle contract should fail qualification unless:

1. every eligible label has a bounded structured justification;
2. label and justification are produced in the same independent pass;
3. the structured justification survives pass wrapping and schema validation;
4. dispute/C orchestration preserves independence;
5. human resolution tooling renders the independent justifications;
6. supplementary reasoning summaries, when supported, are separately tagged as execution evidence rather than authoritative rationales;
7. P0A verifies the complete rationale round-trip;
8. runtime/provenance accounting records aggregate model/session usage separately from final-output usage.

## Claim boundary

Safe public wording:

> The first oracle cohort's labels-only pass contract omitted structured decision justifications from the artifacts used by human resolution. A later audit found that private Inspect logs had retained provider reasoning summaries, so the problem was not that the harness could not expose explanatory evidence; the evaluation pipeline failed to promote it into the authoritative decision record. The frozen oracle remains unchanged, and future cohorts will require explicit structured justifications with end-to-end persistence checks.

Do not publish the private reasoning-summary text or use it to revise the frozen v1 oracle.


## Follow-up design

The versioned follow-up design is tracked in:

`docs/plans/routing-semantic-v2-adjudication-evidence-contract.md`

It requires provider-neutral structured justifications, explicit final-output versus aggregate-session usage scopes, new preflight round-trip gates, and optional/private treatment of provider reasoning summaries.
