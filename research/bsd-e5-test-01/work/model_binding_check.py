"""Independent K02 identity check; only the Python standard library is required.

The theorem certificate is bound to the exact rational Weierstrass model.  A
changed source is rejected before its conductor/sign could be reused.  This is
a finite contract check, not an elliptic-curve isomorphism or rank algorithm.
"""

import argparse
import copy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE_MODEL = {"field": "Q", "a_invariants": [0, 0, 0, -25, 0]}


def invariants(model):
    if model.get("field") != "Q":
        raise ValueError("This local control admits rational models only")
    values = model.get("a_invariants")
    if not isinstance(values, list) or len(values) != 5:
        raise ValueError("Expected five ordered Weierstrass coefficients")
    if any(type(value) is not int for value in values):
        raise ValueError("This local control admits integral coefficients only")
    a1, a2, a3, a4, a6 = values
    b2 = a1 * a1 + 4 * a2
    b4 = a1 * a3 + 2 * a4
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    c4 = b2 * b2 - 24 * b4
    c6 = -b2**3 + 36 * b2 * b4 - 216 * b6
    discriminant = -b2 * b2 * b8 - 8 * b4**3 - 27 * b6 * b6 + 9 * b2 * b4 * b6
    if discriminant == 0:
        raise ValueError("Singular model is not an elliptic curve")
    return {"c4": c4, "c6": c6, "discriminant": discriminant,
            "j": str(Fraction(c4**3, discriminant))}


def bind_e5_certificate(model):
    data = invariants(model)
    differences = [name for name in ("field", "a_invariants")
                   if model.get(name) != CERTIFICATE_MODEL[name]]
    if differences:
        return {"source_model": model, "invariants": data,
                "disposition": "REJECT_CERTIFICATE_NON_APPLICABILITY",
                "mismatching_fields": differences,
                "released_analytic_specialization": None,
                "reason": "The E5 theorem certificate requires its exact bound model."}
    return {"source_model": model, "invariants": data,
            "disposition": "ACCEPT_MODEL_IDENTITY",
            "mismatching_fields": [],
            "released_analytic_specialization": {
                "D": 5, "conductor": 800, "functional_equation_sign": -1,
                "evidence_kind": "THEOREM_CITED_WITH_WRITTEN_SPECIALIZATION",
                "proof_locator": "ANALYTIC_THEOREMS.md"}}


def run():
    plan_path = ROOT / "supplied" / "BSD_E5_CODEX_TEST_01" / "TEST_PLAN.json"
    plan_bytes = plan_path.read_bytes()
    original = json.loads(plan_bytes)["curve"]
    baseline = bind_e5_certificate(original)
    changed = copy.deepcopy(original)
    changed["a_invariants"][3] = -36
    mutation = bind_e5_certificate(changed)
    # Pull back the defining polynomial y^2-x^3-a4*x-a6 along x=5u,y=25v.
    # The requested change modifies the u coefficient of a real input polynomial.
    baseline_pullback = {"v^2": 625, "u^3": -125,
                         "u": -5 * original["a_invariants"][3]}
    changed_pullback = {"v^2": 625, "u^3": -125,
                        "u": -5 * changed["a_invariants"][3]}
    checks = {
        "baseline_identity_accepted": baseline["disposition"] == "ACCEPT_MODEL_IDENTITY",
        "real_a4_mutation": original["a_invariants"][3] == -25 and changed["a_invariants"][3] == -36,
        "changed_certificate_rejected": mutation["disposition"] == "REJECT_CERTIFICATE_NON_APPLICABILITY",
        "conductor_and_sign_withheld_for_changed_model": mutation["released_analytic_specialization"] is None,
        "same_j_is_insufficient_for_binding": baseline["invariants"]["j"] == mutation["invariants"]["j"] == "1728",
        "actual_polynomial_mismatch": changed_pullback["u"] - baseline_pullback["u"] == 55,
    }
    return {
        "control_id": "K02_MODEL_BINDING", "status": "CONFIRMED" if all(checks.values()) else "REFUTED",
        "evidence_kind": "INDEPENDENT_FINITE_CONTRACT_TEST",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "command": " ".join(sys.argv),
        "python_version": sys.version,
        "input_locator": str(plan_path.relative_to(ROOT)),
        "input_sha256": hashlib.sha256(plan_bytes).hexdigest(),
        "certificate_model": CERTIFICATE_MODEL,
        "baseline": baseline, "mutation": mutation,
        "polynomial_witness": {
            "coordinate_substitution": "x=5u, y=25v",
            "baseline_pullback": baseline_pullback,
            "changed_pullback": changed_pullback,
            "difference": "55u",
            "interpretation": "The D=5 polynomial identity no longer holds after the a4 mutation."},
        "checks": checks,
        "claim_ceiling": "The existing E5 certificate is inapplicable to the changed model. No changed-curve rank, conductor, root number, or L-value is asserted.",
        "hash_ceiling": "The input digest identifies bytes and is not the mathematical model check."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "evidence" / "model_binding.json")
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "CONFIRMED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
