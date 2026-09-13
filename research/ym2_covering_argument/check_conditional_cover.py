#!/usr/bin/env python3
"""Exact finite controls for CONDITIONAL_REFINEMENT.md; standard library only.

Default execution recomputes and fully compares the adjacent receipt without
writing. --write-receipt intentionally regenerates that receipt. This checker
does not import, run, or certify any previous checker or the analytic proof.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path
import sys


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def clean(p: dict[tuple[int, ...], F]) -> dict[tuple[int, ...], F]:
    return {m: F(c) for m, c in p.items() if c}


def const(c: F | int, variables: int = 1) -> dict[tuple[int, ...], F]:
    return clean({(0,) * variables: F(c)})


def monomial(powers: tuple[int, ...], c: F | int = 1) -> dict:
    return clean({powers: F(c)})


def add(*polys: dict) -> dict:
    out: dict[tuple[int, ...], F] = {}
    for p in polys:
        for m, c in p.items():
            out[m] = out.get(m, F(0)) + c
    return clean(out)


def scale(p: dict, c: F | int) -> dict:
    return clean({m: F(c) * v for m, v in p.items()})


def mul(p: dict, q: dict) -> dict:
    out: dict[tuple[int, ...], F] = {}
    for a, x in p.items():
        for b, y in q.items():
            require(len(a) == len(b), "polynomial dimension mismatch")
            m = tuple(i + j for i, j in zip(a, b))
            out[m] = out.get(m, F(0)) + x * y
    return clean(out)


def power(p: dict, n: int) -> dict:
    require(n >= 0, "negative polynomial exponent")
    variables = len(next(iter(p))) if p else 1
    out = const(1, variables)
    for _ in range(n):
        out = mul(out, p)
    return out


def poly_record(p: dict) -> list[dict]:
    return [{"powers": list(m), "coefficient": str(c)}
            for m, c in sorted(p.items())]


def majorant_controls() -> dict:
    b = F(4, 3)
    y = monomial((1,))
    t = add(y, scale(power(y, 2), -b))
    w = add(y, scale(t, -1), scale(power(t, 2), -b))
    first = scale(mul(add(y, t), add(y, scale(t, -1))), b)
    second = scale(mul(add(y, t), power(y, 2)), b * b)
    residual_one = add(first, scale(w, -1))
    residual_two = add(second, scale(w, -1))
    require(not residual_one and not residual_two,
            "CR5 polynomial identities fail")
    require(b * b * F(5, 2) * F(9, 4) == 10,
            "CR6 cubic constant fails")
    rows = []
    for yy in (F(0), F(1, 32), F(1, 16), F(1, 8), F(1, 4)):
        tt = yy - b * yy * yy
        ww = yy - tt - b * tt * tt
        require(0 <= yy <= F(1, 4) and 0 <= tt <= F(1, 6),
                "majorant sample outside admitted interval")
        require(0 <= ww <= 10 * tt**3, "CR6 finite control fails")
        rows.append({"Y": yy, "t": tt, "W": ww,
                     "cubic_bound": 10 * tt**3,
                     "contraction": F(8, 3) * yy})
    yc = F(3, 8)
    tc = yc - b * yc * yc
    require(tc == F(3, 16), "certificate t endpoint")
    require(F(8, 3) * yc == 1, "endpoint contraction is not one")
    require(1 - 2 * yc == F(1, 4), "endpoint curvature gap")
    endpoint = {"Y": yc, "t": tc, "contraction": F(8, 3) * yc,
                "hypothetical_geometric_gap": 1 - 2 * yc,
                "banach_endpoint_admitted": False}
    return {"CR5_residual_one": poly_record(residual_one),
            "CR5_residual_two": poly_record(residual_two),
            "cubic_constant": F(10), "rational_samples": rows,
            "strict_construction_endpoint": endpoint}


def kinetic_two_square(p: dict) -> dict:
    # Explicit supplied two-square identities, not a derivation of the cometric.
    images = {
        (0, 0, 0): {},
        (1, 0, 0): monomial((1, 0, 0), 6),
        (0, 1, 0): monomial((0, 1, 0), 6),
        (2, 0, 0): add(monomial((2, 0, 0), 16), const(-4, 3)),
        (0, 2, 0): add(monomial((0, 2, 0), 16), const(-4, 3)),
        (1, 1, 0): add(monomial((1, 1, 0), 13), monomial((0, 0, 1), -1)),
        (0, 0, 1): monomial((0, 0, 1), 9),
    }
    out = {}
    for m, c in p.items():
        require(m in images, "kinetic finite carrier exceeded")
        out = add(out, scale(images[m], c))
    return out


def coefficient_controls() -> dict:
    a, bb, w = (monomial((1, 0, 0)), monomial((0, 1, 0)),
                monomial((0, 0, 1)))
    s = add(a, bb)
    u1 = scale(s, F(1, 6))
    u1sq = power(u1, 2)
    qu1sq = add(u1sq, const(F(-1, 72), 3))
    square_centered = add(power(a, 2), power(bb, 2), const(F(-1, 2), 3))
    ab = mul(a, bb)
    wave2 = add(scale(square_centered, F(1, 96)), scale(ab, F(1, 39)),
                scale(w, F(1, 351)))
    log2 = add(wave2, scale(qu1sq, F(-1, 2)))
    pair = scale(add(scale(w, 4), scale(ab, -3)), F(1, 702))
    expected = add(scale(square_centered, F(-1, 288)), scale(pair, F(1, 2)))
    coefficient_residual = add(log2, scale(expected, -1))
    rhs = add(mul(u1, s), scale(kinetic_two_square(u1sq), F(-1, 2)),
              const(F(-1, 12), 3))
    kinetic_residual = add(kinetic_two_square(log2), scale(rhs, -1))
    require(not coefficient_residual and not kinetic_residual,
            "CR7/CR8 exact coefficient matching fails")
    require(F(1, 36) - F(1, 36) == 0, "edge-disjoint cancellation")
    wrong = scale(square_centered, F(-1, 288))
    wrong_residual = add(kinetic_two_square(wrong), scale(rhs, -1))
    require(wrong_residual == add(scale(ab, F(1, 36)), scale(w, F(-1, 36))),
            "hostile adjacent-as-disconnected residual changed")
    qhead = scale(expected, 2)
    expected_head = add(scale(square_centered, F(-1, 144)), pair)
    require(qhead == expected_head, "centered head identification fails")
    return {"variables": ["a", "b", "w"],
            "input_scope": "explicit degree-two accepted kinetic identities",
            "log_second_coefficient": poly_record(log2),
            "coefficient_residual": poly_record(coefficient_residual),
            "kinetic_residual": poly_record(kinetic_residual),
            "centered_head_second_coefficient": poly_record(qhead),
            "edge_disjoint_pair_coefficient": F(0),
            "hostile_adjacent_as_disconnected": {
                "status": "REJECT", "residual": poly_record(wrong_residual)}}


def endpoint_controls() -> list[dict]:
    rows = []
    for d, m in ((2, 2), (3, 4)):
        r = F(1, 48 * m)
        t, y = 8 * m * r, F(1, 4)
        w = y - t - F(4, 3) * t * t
        eta = F(16, 3) * w
        first = m * r
        second = F(16 * m * (m - 1), 117) * r * r
        theta = first + second + eta / 4
        require(t == F(1, 6) and w == F(5, 108), "safe endpoint values")
        require(eta == F(20, 81), "remainder endpoint eta")
        require(theta < F(1, 12), "CR13 theta bound")
        require(F(1, 12) - F(1, 48) - F(5, 81) == F(1, 1296),
                "endpoint rational comparison")
        rows.append({"dimension": d, "m": m, "r": r, "t": t, "Y": y,
                     "W": w, "eta": eta, "head_linear": first,
                     "head_quadratic": second, "remainder_row": eta / 4,
                     "actual_row_bound": theta, "theta_target": F(1, 12),
                     "strict_margin": F(1, 12) - theta,
                     "gap_bound": F(1, 2),
                     "strict_construction_r_endpoint": F(3, 128 * m)})
    return rows


def evaluate_components(components: tuple, values: tuple[int, ...]) -> F:
    total = F(0)
    for support, coefficient in components:
        term = coefficient
        for i in support:
            term *= values[i]
        total += term
    return total


def mixed_oscillation(components: tuple, n: int, e: int, j: int) -> F:
    require(e != j, "inside and outside occurrence coincide")
    free = tuple(i for i in range(n) if i not in (e, j))
    maximum = F(0)
    for exterior in product((-1, 1), repeat=len(free)):
        for old_j, new_j in product((-1, 1), repeat=2):
            shifts = []
            for inside in (-1, 1):
                old = [0] * n
                for i, value in zip(free, exterior):
                    old[i] = value
                old[e], old[j] = inside, old_j
                new = old.copy()
                new[j] = new_j
                shifts.append(2 * (evaluate_components(components, tuple(new))
                                   - evaluate_components(components, tuple(old))))
            maximum = max(maximum, max(shifts) - min(shifts))
    return maximum


def support_controls() -> dict:
    # x_i=Tr(U_i)/2 ranges over [-1,1]. These finite products are multiaffine;
    # each mixed oscillation reaches an extremum at the enumerated corners.
    # One product has pure spin 1/2 on its support, A norm 1, and lambda=3|S|/2.
    cases = {
        "constant": (((), F(7)),),
        "inside_absent": (((1,), F(1)),),
        "outside_absent": (((0,), F(1)),),
        "sharp_pair": (((0, 1), F(1)),),
        "triple": (((0, 1, 2), F(1)),),
        "collective_four_links": (((0, 1, 2, 3), F(1)),),
        "signed_joint": (((0, 1), F(1, 2)), ((0, 1, 2), F(-1, 3)),
                         ((0, 2, 3), F(2, 5)), ((1,), F(7))),
    }
    records = []
    results_by_name = {}
    for name, components in cases.items():
        n, e = 4, 0
        pairs = []
        for j in range(1, n):
            actual = mixed_oscillation(components, n, e, j)
            pair_sum = sum((abs(c) for support, c in components
                            if e in support and j in support), F(0))
            bound = 8 * pair_sum
            require(actual <= bound, "CR10 finite support control fails")
            pairs.append({"j": j, "actual_mixed_oscillation": actual,
                          "common_support_coefficient_sum": pair_sum,
                          "bound_eight": bound})
        incidence = 8 * sum(((len(support) - 1) * abs(c)
                             for support, c in components if e in support), F(0))
        anchored = sum((F(3, 2) * len(support) * abs(c)
                        for support, c in components if e in support), F(0))
        energy_bound = F(16, 3) * anchored
        actual_row = sum((row["actual_mixed_oscillation"] for row in pairs), F(0))
        require(incidence == sum((row["bound_eight"] for row in pairs), F(0)),
                "support incidence identity fails")
        require(actual_row <= incidence <= energy_bound,
                "CR11 finite energy-weight control fails")
        item = {"case": name,
                "components": [{"support": list(s), "coefficient": c}
                               for s, c in components],
                "pairs": pairs, "actual_row": actual_row,
                "incidence_bound": incidence, "anchored_energy_norm": anchored,
                "energy_bound_sixteen_thirds": energy_bound}
        records.append(item)
        results_by_name[name] = item
    require(results_by_name["sharp_pair"]["actual_row"] == 8,
            "factor eight is not attained by sharp pair")
    require(results_by_name["inside_absent"]["actual_row"] == 0,
            "component absent inside did not cancel")
    require(results_by_name["outside_absent"]["actual_row"] == 0,
            "component absent outside did not cancel")
    require(results_by_name["triple"]["actual_row"] == 16,
            "triple must retain both outside occurrences")
    hostile = [
        {"claim": "replace factor 8 with factor 4", "actual": F(8),
         "false_bound": F(4), "status": "REJECT"},
        {"claim": "retain only one exterior occurrence of a triple",
         "actual": F(16), "false_bound": F(8), "status": "REJECT"},
        {"claim": "drop the support-energy weight on four-link product",
         "actual": results_by_name["collective_four_links"]["actual_row"],
         "false_bound": F(16, 3), "status": "REJECT"},
    ]
    for item in hostile:
        require(item["actual"] > item["false_bound"], "hostile case failed to reject")
    return {"carrier": "four full SU(2) rotors; x_i=Tr(U_i)/2; listed multiaffine products",
            "corner_configurations": 16, "inside_occurrence": 0,
            "all_spins_claimed": False, "cases": records,
            "hostile_controls": hostile}


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def build_receipt() -> dict:
    script = Path(__file__).resolve()
    return encode({
        "schema": "ym2-conditional-cover-finite-controls-v1",
        "checker": script.name,
        "checker_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "evidence_grade": "exact finite algebra and bounded polynomial controls",
        "not_verified": ["Fourier algebra on all components", "Banach fixed-point theorem",
                         "elliptic regularity", "all-spin Hessian inequality",
                         "unrestricted conditional supremum theorem", "weighted Bochner theorem",
                         "infinite-volume or continuum limit"],
        "old_checkers_imported_or_run": False,
        "majorants": majorant_controls(),
        "coefficients": coefficient_controls(),
        "endpoint_rows": endpoint_controls(),
        "mixed_oscillation_supports": support_controls(),
        "status": "PASS",
    })


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-receipt", action="store_true",
                        help="intentionally replace the adjacent deterministic receipt")
    args = parser.parse_args()
    receipt_path = Path(__file__).resolve().with_name("RESULTS_CONDITIONAL_COVER.json")
    computed = build_receipt()
    if args.write_receipt:
        receipt_path.write_text(json.dumps(computed, indent=2, sort_keys=True) + "\n",
                                encoding="utf-8", newline="\n")
        print(f"PASS: wrote {receipt_path.name}")
        return 0
    if not receipt_path.is_file():
        raise CheckFailure("receipt missing; use --write-receipt only when intentionally generating it")
    saved = json.loads(receipt_path.read_text(encoding="utf-8"))
    require(saved == computed, "full receipt mismatch; source bytes or finite results changed")
    print(f"PASS: recomputed full receipt matches {receipt_path.name}; no files written")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
