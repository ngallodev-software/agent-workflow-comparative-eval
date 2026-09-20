FEATURE_SCHEMA = "agent-workflow-comparative-eval/eval-feature/v1"
OBSERVATION_SCHEMA = "agent-workflow-comparative-eval/comparison-observation/v1"
OUTCOME_SCHEMA = "agent-workflow-comparative-eval/comparison-outcome/v1"
REPORT_SCHEMA = "agent-workflow-comparative-eval/comparison-report/v1"

LEGACY_FEATURE_SCHEMA = "agent-workflow-typesafe/eval-feature/v1"
LEGACY_OBSERVATION_SCHEMA = "agent-workflow-typesafe/comparison-observation/v1"
LEGACY_OUTCOME_SCHEMA = "agent-workflow-typesafe/comparison-outcome/v1"
LEGACY_REPORT_SCHEMA = "agent-workflow-typesafe/comparison-report/v1"

LEGACY_TO_CANONICAL = {
    LEGACY_FEATURE_SCHEMA: FEATURE_SCHEMA,
    LEGACY_OBSERVATION_SCHEMA: OBSERVATION_SCHEMA,
    LEGACY_OUTCOME_SCHEMA: OUTCOME_SCHEMA,
    LEGACY_REPORT_SCHEMA: REPORT_SCHEMA,
}
CANONICAL_TO_LEGACY = {value: key for key, value in LEGACY_TO_CANONICAL.items()}
