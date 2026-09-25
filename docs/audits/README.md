# Comparative Evaluation Audits

This directory preserves dated study-readiness analyses as frozen source material for the public case study and later benchmark publication.

## 2026-09-24 — Phase 0 current-state audit

- **Audit:** [Phase 0 current-state audit and implementation plan](./2026-09-24-phase-0-current-state-audit-and-implementation-plan.md)
- **Audit date:** 2026-09-24
- **Portfolio publication snapshot:** 2026-09-24 19:06 PT
- **Purpose:** document the current evaluation architecture, evidence gaps, metric coverage, experimental-design requirements, repository responsibilities, and acceptance gate before the first full comparative-decision study.
- **Status:** frozen input to the next study-specification phase. Result-affecting changes should be captured in a new dated/versioned artifact rather than editing the historical analysis in place.
- **Portfolio case study:** https://ngallodev-software.uk/projects/agent-workflow-comparative-eval

The audit intentionally separates evaluator maturity from study maturity. It records that the neutral comparison library already contains substantial correctness, reliability, efficiency, calibration, and deterministic statistical machinery, while the missing maturity is primarily experimental and connective: frozen oracle data, lossless per-decision evidence persistence, and a dedicated benchmark study lane.

No effectiveness claim should be inferred from the audit itself. The acceptance gate requires independent labels, explicit denominators, paired uncertainty, privacy-safe publication, and publishability regardless of whether the semantic candidate outperforms the deterministic control.
