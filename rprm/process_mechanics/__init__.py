"""Small typed adapters for process-mechanics kits.

These wrap common context, candidate-filter, interval-join and measurement-
admission patterns used by two or more topic kits. They do not replace
``rprm.core`` fiber dispositions (NONE/ONE/MANY) or invent probabilistic
semantics from row counts.

Evidence grades of callers remain the caller's responsibility.
"""

from .candidates import CandidateFilterResult, filter_candidates, opposing_witness_step
from .context import ContextRecord, ContextValidation, validate_context
from .intervals import ChildSummary, IntervalBounds, JoinOutcome, combine_bounds, validate_and_join
from .measurement import MeasurementAdmission, admit_measurement

__all__ = [
    "CandidateFilterResult",
    "ChildSummary",
    "ContextRecord",
    "ContextValidation",
    "IntervalBounds",
    "JoinOutcome",
    "MeasurementAdmission",
    "admit_measurement",
    "combine_bounds",
    "filter_candidates",
    "opposing_witness_step",
    "validate_and_join",
    "validate_context",
]
