class ComparativeEvalError(Exception):
    """Base error for the dependency-neutral evaluation library."""


class ContractError(ComparativeEvalError, ValueError):
    """A record does not satisfy its declared comparison contract."""


class CohortError(ComparativeEvalError, ValueError):
    """Evidence from unlike cohorts was combined."""


class ImmutableOutcomeConflict(ComparativeEvalError):
    """A caller attempted to change an already joined immutable outcome."""
