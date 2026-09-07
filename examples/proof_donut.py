"""Run an explicit finite core/independent-checker demonstration (0BSD)."""

from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rprm.core import deterministic_quotient
from rprm.proof_donut import audit_finite_induction, audit_finite_quotient


def demonstration():
    states = (0, 1, 2, 3)
    summary = {x: x % 2 for x in states}
    observation = dict(summary)
    transition = {0: 1, 1: 0, 2: 3, 3: 2}
    core = deterministic_quotient(states, summary, observation, transition)
    independent = audit_finite_quotient(states, summary, observation, transition)
    invariant = audit_finite_induction(states, (0,), (transition,), (0, 1), (2, 3))
    altered = dict(transition)
    altered[2] = 2
    hostile = audit_finite_quotient(states, summary, observation, altered)
    return {
        "carrier": states, "initial": 0, "summary": summary,
        "observation": observation, "transition": transition,
        "core_quotient": core, "independent_quotient_audit": independent,
        "concrete_invariant": invariant, "changed_transition_audit": hostile,
        "meaning": "The two finite tables are checked independently. Induction uses the stated transition law; no claim of general RPRM consistency or physical origins follows.",
    }


if __name__ == "__main__":
    print(json.dumps(demonstration(), indent=2, sort_keys=True))
