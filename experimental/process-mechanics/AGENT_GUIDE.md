# Agent guide — process-mechanics kits

## Task contract

1. State carrier, admitted context, known vs hidden ports, readout, and cost.
2. Keep NONE/ONE/MANY (core fibers) distinct from OPEN_INCOMPLETE,
   EMPTY_FAMILY, JOIN_OK, ADMISSION_ERROR, SKIP_OPTIONAL_DEPENDENCY, PARTIAL.
3. Do not promote hub method/transfer/algorithm/biology IDs.
4. New demos are `NEW_ILLUSTRATIVE_DEMO` unless a frozen source port was checked.
5. Do not contact authors, reopen C1 figure digitization, or push public branches.

## Imports

```python
from rprm.process_mechanics import (
    validate_context,
    filter_candidates,
    validate_and_join,
    admit_measurement,
)
```

## Minimal reuse snippets

Water join status:

```python
from fractions import Fraction as F
from rprm.process_mechanics import ChildSummary  # via intervals
# Prefer water/example.py compose_partition(cid, n)
```

Candidate filter:

```python
from rprm.process_mechanics import filter_candidates
filter_candidates(rows, [{"D": 0.10}], tol=0.01)
```

Measurement admission:

```python
from rprm.process_mechanics import admit_measurement
admit_measurement(arithmetic_ok=True, calibration_ok=False, coverage_ok=False, estimator_equivalence_ok=False)
```

## Verification

Each kit `check.py` writes PASS/FAIL JSON. Missing optional NumPy/SciPy must be
SKIP for RLC, never silent PASS. Playground UI review defaults to NOT_RUN.
