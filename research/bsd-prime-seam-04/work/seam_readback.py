#!/usr/bin/env python3
"""Independent, stdlib-only finite readback for the E_34 prime seam.

Run with Python 3.10+: python -I -B seam_readback.py --witness W.json --output NEW.json
The output is created exclusively; an existing file is never overwritten.
Exit 0 means all declared finite checks passed; exit 1 means a check failed;
exit 2 means the fresh output could not be written or CLI admission failed.

The witness supplies only these rational-complex coordinates:
  local_factors.{5,13}.{real,imag}: [integer numerator, nonzero integer denominator]
  ratio_13_over_5.{real,imag}:      [integer numerator, nonzero integer denominator]
Other witness fields are ignored. Equivalent fractions are admitted.

No primary producer code, stored point counts, external package, or network is
used. The finite polynomial certificate is distinguished from its usual
Galois-theoretic interpretation. This does not verify BSD or Kolyvagin-prime
admissibility. No assertion about an unfinished global fiber is made.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from math import lcm
from pathlib import Path
import sys
from typing import Any


ComplexQ = tuple[Fraction, Fraction]
ONE: ComplexQ = (Fraction(1), Fraction(0))
PI: dict[int, ComplexQ] = {
    5: (Fraction(-1), Fraction(2)),
    13: (Fraction(-3), Fraction(2)),
}
EXPECTED_C: dict[int, ComplexQ] = {
    5: (Fraction(4, 5), Fraction(-3, 5)),
    13: (Fraction(63, 65), Fraction(-16, 65)),
}
EXPECTED_RATIO: ComplexQ = (Fraction(12, 13), Fraction(5, 13))


def cq_sub(a: ComplexQ, b: ComplexQ) -> ComplexQ:
    return a[0] - b[0], a[1] - b[1]


def cq_mul(a: ComplexQ, b: ComplexQ) -> ComplexQ:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def cq_conj(a: ComplexQ) -> ComplexQ:
    return a[0], -a[1]


def cq_inverse(a: ComplexQ) -> ComplexQ:
    norm = a[0] ** 2 + a[1] ** 2
    if norm == 0:
        raise ZeroDivisionError("zero complex denominator")
    return a[0] / norm, -a[1] / norm


def cq_json(a: ComplexQ) -> dict[str, list[int]]:
    return {
        "real": [a[0].numerator, a[0].denominator],
        "imag": [a[1].numerator, a[1].denominator],
    }


def original_complex_formula(pi: ComplexQ) -> tuple[ComplexQ, dict[str, Any]]:
    # Evaluate precisely the original formula; no Cayley-form substitution.
    first = cq_sub(ONE, cq_inverse(pi))
    second = cq_sub(ONE, cq_inverse(cq_conj(pi)))
    inverse_first = cq_inverse(first)
    result = cq_mul(inverse_first, second)
    return result, {
        "pi": cq_json(pi),
        "conjugate_pi": cq_json(cq_conj(pi)),
        "one_minus_inverse_pi": cq_json(first),
        "inverse_of_one_minus_inverse_pi": cq_json(inverse_first),
        "one_minus_inverse_conjugate_pi": cq_json(second),
        "result": cq_json(result),
    }


@dataclass(frozen=True)
class RawQ:
    """An unreduced integer numerator/denominator; p-factors stay visible."""

    numerator: int
    denominator: int = 1

    def inverse(self) -> RawQ:
        if self.numerator == 0:
            raise ZeroDivisionError("zero raw rational numerator")
        return RawQ(self.denominator, self.numerator)

    def subtract(self, other: RawQ) -> RawQ:
        return RawQ(
            self.numerator * other.denominator - other.numerator * self.denominator,
            self.denominator * other.denominator,
        )

    def multiply(self, other: RawQ) -> RawQ:
        return RawQ(self.numerator * other.numerator, self.denominator * other.denominator)

    def divide(self, other: RawQ) -> RawQ:
        return self.multiply(other.inverse())


def integer_valuation(n: int, p: int) -> int:
    if n == 0:
        raise ValueError("zero has no finite valuation; finite precision is insufficient")
    n = abs(n)
    result = 0
    while n % p == 0:
        result += 1
        n //= p
    return result


def residue(raw: RawQ, p: int, unit_power: int, lift_power: int) -> dict[str, Any]:
    """Return p^valuation times a unit modulo p^unit_power.

    Only the p-free part of the denominator is inverted. Original polynomial
    numerators and denominators evaluated at the Hensel lift are retained.
    The precision guard ensures their normalized residues are determined by
    the chosen embedding, not by the chosen integer lift representative.
    """
    vn = integer_valuation(raw.numerator, p)
    vd = integer_valuation(raw.denominator, p)
    if lift_power < unit_power + max(vn, vd):
        raise ValueError("insufficient Hensel precision for normalized quotient")
    modulus = p ** unit_power
    unit_n = raw.numerator // (p ** vn)
    unit_d = raw.denominator // (p ** vd)
    unit = (unit_n * pow(unit_d, -1, modulus)) % modulus
    return {
        "valuation": vn - vd,
        "unit_residue": unit,
        "unit_modulus": modulus,
        "unit_power": unit_power,
        "absolute_precision_exponent": unit_power + vn - vd,
        "numerator_valuation": vn,
        "denominator_valuation": vd,
        "raw_numerator_mod_unit_modulus": raw.numerator % modulus,
        "raw_denominator_mod_unit_modulus": raw.denominator % modulus,
    }


def same_residue(a: dict[str, Any], b: dict[str, Any]) -> bool:
    return (a["valuation"], a["unit_residue"], a["unit_modulus"]) == (
        b["valuation"], b["unit_residue"], b["unit_modulus"]
    )


def embed_coordinates(z: ComplexQ, root: int) -> RawQ:
    denominator = lcm(z[0].denominator, z[1].denominator)
    a = z[0].numerator * (denominator // z[0].denominator)
    b = z[1].numerator * (denominator // z[1].denominator)
    return RawQ(a + b * root, denominator)


def original_padic_formula(pi: ComplexQ, root: int) -> tuple[RawQ, dict[str, RawQ]]:
    pival = embed_coordinates(pi, root)
    barval = embed_coordinates(cq_conj(pi), root)
    first = RawQ(1).subtract(pival.inverse())
    second = RawQ(1).subtract(barval.inverse())
    inverse_first = first.inverse()
    result = inverse_first.multiply(second)
    return result, {
        "pi": pival,
        "conjugate_pi": barval,
        "one_minus_inverse_pi": first,
        "inverse_of_one_minus_inverse_pi": inverse_first,
        "one_minus_inverse_conjugate_pi": second,
        "C": result,
    }


def hensel_sqrt_minus_one(p: int, initial: int, power: int) -> tuple[int, list[dict[str, int]]]:
    if (initial * initial + 1) % p or (2 * initial) % p == 0:
        raise ValueError("initial square root is absent or singular")
    root, modulus = initial % p, p
    steps = [{"power": 1, "modulus": p, "root": root}]
    for exponent in range(2, power + 1):
        new_modulus = modulus * p
        candidates = [root + digit * modulus for digit in range(p)
                      if ((root + digit * modulus) ** 2 + 1) % new_modulus == 0]
        if len(candidates) != 1:
            raise ValueError(f"Hensel step at {p}^{exponent} is not unique")
        root, modulus = candidates[0], new_modulus
        steps.append({"power": exponent, "modulus": modulus, "root": root})
    return root, steps


class Audit:
    def __init__(self) -> None:
        self.checks: list[dict[str, Any]] = []
        self.errors: list[dict[str, str]] = []
        self.evidence: dict[str, Any] = {}

    def equal(self, name: str, actual: Any, expected: Any) -> None:
        self.checks.append({"name": name, "passed": actual == expected,
                            "actual": actual, "expected": expected})

    def section_error(self, section: str, exc: Exception) -> None:
        self.errors.append({"section": section, "type": type(exc).__name__, "message": str(exc)})


def verify_counts(audit: Audit) -> None:
    counts: dict[str, Any] = {}
    for p, expected_count in ((3, 4), (5, 8), (13, 20)):
        points = [[x, y] for x in range(p) for y in range(p)
                  if (y * y - (x ** 3 - 1156 * x)) % p == 0]
        count = 1 + len(points)
        trace = p + 1 - count
        discriminant = 64 * 34 ** 6
        audit.equal(f"good_reduction_{p}", discriminant % p != 0, True)
        audit.equal(f"point_count_{p}", count, expected_count)
        counts[str(p)] = {"affine_points": points, "point_at_infinity_count": 1,
                          "point_count": count, "trace": trace,
                          "discriminant_mod_p": discriminant % p}
        if p in PI:
            pi = PI[p]
            trace_q = pi[0] + cq_conj(pi)[0]
            norm = cq_mul(pi, cq_conj(pi))
            audit.equal(f"CM_trace_matches_fresh_count_{p}", [trace_q.numerator, trace_q.denominator], [trace, 1])
            audit.equal(f"CM_norm_{p}", cq_json(norm), cq_json((Fraction(p), Fraction(0))))

    trace3 = counts["3"]["trace"]
    trace13 = counts["13"]["trace"]
    poly3 = [3 % 5, (-trace3) % 5, 1]
    poly13 = [13 % 5, (-trace13) % 5, 1]
    evaluations3 = [(x * x - trace3 * x + 3) % 5 for x in range(5)]
    roots3 = [x for x, value in enumerate(evaluations3) if value == 0]
    roots13 = [x for x in range(5) if (x * x - trace13 * x + 13) % 5 == 0]
    product = [(1 * 3) % 5, (-(1 + 3)) % 5, 1]
    audit.equal("fresh_Frob3_quadratic_has_no_F5_roots", roots3, [])
    audit.equal("fresh_Frob13_polynomial_equals_X_minus_1_times_X_minus_3", poly13, product)
    audit.equal("fresh_Frob13_roots_mod_5", roots13, [1, 3])
    audit.evidence["point_counts"] = counts
    audit.evidence["finite_frobenius"] = {
        "coefficient_order": "constant, X, X^2",
        "Frob3_characteristic_mod5": poly3,
        "Frob3_values_at_0_through_4": evaluations3,
        "Frob3_roots_mod5": roots3,
        "irreducibility_scope": "A quadratic over F5 is irreducible exactly when it has no F5 root.",
        "Frob13_characteristic_mod5": poly13,
        "Frob13_roots_mod5": roots13,
        "representation_dependency": (
            "Interpreting X^2-a_q X+q as Frobenius on E34[5] uses the standard "
            "good-reduction Frobenius characteristic theorem for q != 5. Given "
            "that theorem, the irreducible q=3 polynomial rules out an invariant "
            "F5 line. This script verifies the finite certificate, not the theorem."
        ),
    }


def verify_complex(audit: Audit) -> dict[int, ComplexQ]:
    factors: dict[int, ComplexQ] = {}
    stages: dict[str, Any] = {}
    for p, pi in PI.items():
        factor, steps = original_complex_formula(pi)
        factors[p] = factor
        stages[str(p)] = steps
        audit.equal(f"original_complex_formula_C{p}", cq_json(factor), cq_json(EXPECTED_C[p]))
        audit.equal(f"complex_norm_C{p}", cq_json(cq_mul(factor, cq_conj(factor))), cq_json(ONE))
    ratio = cq_mul(factors[13], cq_inverse(factors[5]))
    audit.equal("independent_ratio_C13_over_C5", cq_json(ratio), cq_json(EXPECTED_RATIO))
    audit.equal("ratio_times_C5_recovers_C13", cq_json(cq_mul(ratio, factors[5])), cq_json(factors[13]))
    audit.evidence["original_complex_formula"] = stages
    audit.evidence["independent_ratio_13_over_5"] = cq_json(ratio)
    return factors


def verify_padic(audit: Audit, factors: dict[int, ComplexQ]) -> None:
    embeddings: dict[str, Any] = {}
    lift_power, unit_power = 16, 8
    ratio = cq_mul(factors[13], cq_inverse(factors[5]))
    for p, initial in ((5, 2), (13, 5)):
        root, lift_steps = hensel_sqrt_minus_one(p, initial, lift_power)
        audit.equal(f"Hensel_root_{p}_initial", root % p, initial)
        for step in lift_steps:
            audit.equal(f"Hensel_root_{p}_power_{step['power']}",
                        (step["root"] ** 2 + 1) % step["modulus"], 0)
        original: dict[str, RawQ] = {}
        closed: dict[str, RawQ] = {}
        factor_stages: dict[str, Any] = {}
        for factor_p, pi in PI.items():
            raw, stages = original_padic_formula(pi, root)
            name = f"C{factor_p}"
            original[name] = raw
            closed[name] = embed_coordinates(factors[factor_p], root)
            factor_stages[str(factor_p)] = {
                key: {"raw_numerator": value.numerator, "raw_denominator": value.denominator,
                      **residue(value, p, unit_power, lift_power)}
                for key, value in stages.items()
            }
        original["C13_over_C5"] = original["C13"].divide(original["C5"])
        closed["C13_over_C5"] = embed_coordinates(ratio, root)
        levels: list[dict[str, Any]] = []
        for exponent in range(1, unit_power + 1):
            values: dict[str, Any] = {}
            for name in original:
                lhs = residue(original[name], p, exponent, lift_power)
                rhs = residue(closed[name], p, exponent, lift_power)
                audit.equal(f"original_vs_coordinates_{name}_at_{p}^{exponent}", same_residue(lhs, rhs), True)
                # An additive congruence modulo p^exponent requires more unit
                # digits when valuation is negative. Retain that check too.
                extra_digits = max(0, -lhs["valuation"])
                lhs_absolute = residue(original[name], p, exponent + extra_digits, lift_power)
                rhs_absolute = residue(closed[name], p, exponent + extra_digits, lift_power)
                audit.equal(f"absolute_precision_{name}_at_{p}^{exponent}",
                            same_residue(lhs_absolute, rhs_absolute), True)
                values[name] = {"original_formula": lhs, "rational_coordinates": rhs,
                                "absolute_modulus_p_power": exponent,
                                "original_at_absolute_precision": lhs_absolute,
                                "coordinates_at_absolute_precision": rhs_absolute}
            levels.append({"power": exponent, "modulus": p ** exponent, "values": values})

        own = factor_stages[str(p)]
        audit.equal(f"oriented_pi{p}_is_unit_at_{p}", own["pi"]["valuation"], 0)
        audit.equal(f"oriented_conjugate_pi{p}_valuation_at_{p}", own["conjugate_pi"]["valuation"], 1)
        audit.equal(f"C{p}_valuation_at_own_prime", own["C"]["valuation"], -1)
        expected_valuations = {5: {"C5": -1, "C13": -1, "C13_over_C5": 0},
                               13: {"C5": 0, "C13": -1, "C13_over_C5": -1}}[p]
        for name, expected in expected_valuations.items():
            audit.equal(f"valuation_{name}_at_{p}", residue(original[name], p, 8, lift_power)["valuation"], expected)

        opposite_root = (-root) % (p ** lift_power)
        opposite, _ = original_padic_formula(PI[p], opposite_root)
        opposite_readout = residue(opposite, p, 8, lift_power)
        audit.equal(f"hostile_opposite_embedding_C{p}_valuation", opposite_readout["valuation"], 1)
        embeddings[str(p)] = {
            "initial_root": initial,
            "root_lift_power": lift_power,
            "hensel_steps": lift_steps,
            "original_formula_stages": factor_stages,
            "precision_levels": levels,
            "hostile_opposite_embedding": {"root": opposite_root, "readout": opposite_readout},
        }
    audit.evidence["padic_embeddings"] = embeddings


def rational_coordinate(value: Any, label: str) -> Fraction:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{label}: expected [integer numerator, nonzero integer denominator]")
    n, d = value
    if type(n) is not int or type(d) is not int or d == 0:
        raise ValueError(f"{label}: coordinates must be integers, with denominator nonzero")
    return Fraction(n, d)


def read_complex(value: Any, label: str) -> ComplexQ:
    if not isinstance(value, dict):
        raise ValueError(f"{label}: expected an object")
    return rational_coordinate(value["real"], label + ".real"), rational_coordinate(value["imag"], label + ".imag")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def verify_witness(audit: Audit, path: Path, factors: dict[int, ComplexQ]) -> None:
    data = path.read_bytes()
    witness = json.loads(data.decode("utf-8-sig"), object_pairs_hook=unique_object)
    if not isinstance(witness, dict):
        raise ValueError("witness must be a JSON object")
    audit.evidence["witness"] = {"path": str(path.resolve()), "sha256": hashlib.sha256(data).hexdigest(),
                                 "hash_scope": "Binds witness bytes; does not establish mathematical truth."}
    for p in (5, 13):
        try:
            got = read_complex(witness["local_factors"][str(p)], f"local_factors.{p}")
            audit.equal(f"witness_C{p}", cq_json(got), cq_json(factors[p]))
        except (KeyError, TypeError, ValueError) as exc:
            audit.section_error(f"witness.local_factors.{p}", exc)
    try:
        got = read_complex(witness["ratio_13_over_5"], "ratio_13_over_5")
        derived = cq_mul(factors[13], cq_inverse(factors[5]))
        audit.equal("witness_ratio_C13_over_C5", cq_json(got), cq_json(derived))
    except (KeyError, TypeError, ValueError) as exc:
        audit.section_error("witness.ratio_13_over_5", exc)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--witness", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="fresh JSON output file; never overwritten")
    args = parser.parse_args()
    audit = Audit()
    factors: dict[int, ComplexQ] = {}
    for section, operation in (("point_counts", lambda: verify_counts(audit)),
                               ("complex_arithmetic", lambda: factors.update(verify_complex(audit))),
                               ("padic_arithmetic", lambda: verify_padic(audit, factors)),
                               ("witness_readback", lambda: verify_witness(audit, args.witness, factors))):
        try:
            operation()
        except Exception as exc:
            audit.section_error(section, exc)
    failures = [check for check in audit.checks if not check["passed"]]
    passed = not failures and not audit.errors
    status = "PASS" if passed else "FAIL"
    summary = f"{status}: {len(audit.checks)} checks, {len(failures)} failed checks, {len(audit.errors)} errors."
    report = {
        "schema": "bsd-prime-seam-04-independent-readback-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "report": summary,
        "contract": {
            "curve": "E34: y^2 = x^3 - 1156*x; one point at infinity",
            "carrier": "Q(i), exact Fraction pairs; finite F_p enumerations; specified embeddings in Q_p",
            "equality": "exact rational-coordinate equality and declared finite modular congruences",
            "supplied_ports": "witness C5, C13, and C13/C5 rational-complex coordinates",
            "requested_readout": "independent agreement with original local-factor formula and finite certificates",
            "operation": "exact evaluation; inversions require nonzero inputs; output must be fresh",
            "receiver": "point counts, CM trace/norm, rational factors, oriented valuations, retained residues",
            "fiber_scope": "fixed-input deterministic finite readback; no global completion-fiber claim",
            "evidence_grade": "fresh exact finite computation; mathematical theorem dependency explicitly retained",
            "coverage": "q=3,5,13 point enumeration; original formula; both chosen p-adic embeddings through p^8",
            "hostile_case": "opposite square-root branch changes each own-prime C valuation from -1 to +1",
            "nonclaims": ["full BSD", "Kolyvagin-prime admissibility", "proof of the Frobenius characteristic theorem"],
            "padic_residue_convention": (
                "A value is p^valuation times unit_residue modulo unit_modulus. "
                "Its absolute precision is p^(unit_power+valuation). Extra unit "
                "digits are separately checked to ensure absolute precision p^k "
                "at every k=1,...,8. Denominators divisible by p are never inverted modulo p^k."
            ),
        },
        "checks": audit.checks,
        "failed_checks": failures,
        "errors": audit.errors,
        "evidence": audit.evidence,
    }
    try:
        # Serialize before exclusive creation to preserve a complete failure report.
        payload = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
    except Exception as exc:
        print(f"OUTPUT_ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        print(json.dumps(report, sort_keys=True), file=sys.stderr)
        return 2
    print(summary)
    print(str(args.output.resolve()))
    for failure in failures:
        print(f"FAILED: {failure['name']}", file=sys.stderr)
    for error in audit.errors:
        print(f"ERROR [{error['section']}]: {error['type']}: {error['message']}", file=sys.stderr)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
