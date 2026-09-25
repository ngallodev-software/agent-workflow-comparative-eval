"""Dependency-neutral comparative evaluation contracts and metrics."""
from .constants import *
from .identity import canonical_json, sha256, canonical_hash, cohort_key
from .contracts import schema_for, validate_record, known_schema_ids
from .legacy import upgrade_legacy_record, downgrade_typesafe_v1_record
from .datasets import load_corpus, load_dataset, list_datasets, dataset_manifest, dataset_document
from .registry import EvalFeature, FeatureRegistry, default_feature_registry
from .observations import observation, make_observation, validate_observation, run_static_cases
from .outcomes import outcome, make_outcome, validate_outcome, OutcomeJoiner
from .reports import comparison_report, build_report
from .usage import normalize_usage, empty_usage, aggregate_usage, NUMERIC_FIELDS
from .statistics import wilson_interval, paired_bootstrap_interval, paired_binary_deltas
from .timing import quantile, timing_summary
from .cohorts import group_by_cohort
from .pairing import assert_same_cohort
from .errors import ComparativeEvalError, ContractError, CohortError, ImmutableOutcomeConflict
from .study import (
    list_studies,
    load_study_spec,
    validate_decision_study_corpus,
    validate_decision_study_oracle_bundle,
    make_provider_request,
    make_exclusion,
    make_precomputed_decision_observation,
    build_decision_study_report,
)

__version__ = "0.2.0"
from .comparisons import ComparisonPolicy, compare_trials
from .metrics import (
    correctness_counts, binary_classification, classification_metrics, ordinal_metrics,
    brier_score, expected_calibration_error, multiclass_brier_score, multiclass_log_loss,
    arm_reliability, paired_efficiency,
)
