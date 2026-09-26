# Oracle Baseline API Usage — 2026-09-26

**Study:** `routing-semantic-v1`  
**Scope:** cumulative provider/API accounting for initial qualification and adjudication runs through and including P0B oracle freeze  
**Recorded:** 2026-09-26

## Execution provenance

The oracle-construction cohort was executed through:

```text
OpenAI Codex harness
        |
        v
codex-lb load balancer
        |
        v
DeepSeek-4.1-Flash API
```

The routed adjudicator alias/path used by the study tooling is:

`openai-api/codex-lb/deepseek-flash`

The provider/model identity associated with the API accounting supplied for these runs is **DeepSeek-4.1-Flash**.

## Cumulative provider/API metrics through oracle freeze

| Metric | Value |
| --- | ---: |
| Cost | **$0.07 USD** |
| API requests | **36** |
| Tokens | **726,263** |

## Scope boundary

These totals cover the initial adjudicator qualification and oracle-authoring/adjudication work through the P0B oracle freeze.

They **do not include**:

- P1 bounded TypeSafe/Jev instrumentation smoke traffic;
- P2 full comparative inference;
- P3 publication/sanitization work.

They therefore describe the cost and usage of establishing the independent oracle baseline, not the cost of the TypeSafe/Jev treatment and not comparative-study efficiency.

## Provenance and limitations

The aggregate values above were supplied by the project operator from provider/API accounting on 2026-09-26. They are recorded here as durable study provenance.

Raw provider traffic, credentials, and private billing artifacts are not committed. The repository does not independently reconstruct these totals from raw billing events, and no input/output-token split was supplied. Do not infer per-token pricing, treatment cost, or comparative efficiency from this record.

The machine-readable companion is `docs/evidence/oracle-baseline-api-usage-2026-09-26.json`.
