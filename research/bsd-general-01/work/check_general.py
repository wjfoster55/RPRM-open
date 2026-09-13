"""Exact finite controls for the general BSD starting note (standard library).

These tests support written algebraic arguments. They do not compute a general
elliptic-curve Selmer group or certify the BSD conjecture.
"""
from __future__ import annotations

import argparse
import importlib.util
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import factorial, gcd, prod
from pathlib import Path
import platform

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def residue(point, rank, torsion, modulus):
    require(modulus >= 1, "positive quotient modulus required")
    return tuple(point[i] % modulus for i in range(rank)) + tuple(
        point[rank + i] % gcd(t, modulus) for i, t in enumerate(torsion)
    )


def ball(rank, torsion, bound):
    # H=max(abs(free coordinates)); all finitely many torsion values retained.
    return list(product(*([range(-bound, bound + 1)] * rank),
                        *(range(t) for t in torsion)))


def quotient_order(rank, torsion, modulus):
    return modulus ** rank * prod(gcd(t, modulus) for t in torsion)


def kernel_order(cyclic_orders, modulus):
    return prod(gcd(t, modulus) for t in cyclic_orders)


def on_curve(point):
    return point is None or point[1] ** 2 == point[0] ** 3 - 25 * point[0]


def add(left, right):
    require(on_curve(left) and on_curve(right), "E5 point admission")
    if left is None:
        return right
    if right is None:
        return left
    x, y = left
    u, v = right
    if x == u and y == -v:
        return None
    slope = (3 * x * x - 25) / (2 * y) if left == right else (v - y) / (u - x)
    xx = slope * slope - x - u
    out = (xx, slope * (x - xx) - y)
    require(on_curve(out), "group law output admission")
    return out


def multiple(n, point):
    if n < 0:
        return multiple(-n, None if point is None else (point[0], -point[1]))
    out = None
    while n:
        if n & 1:
            out = add(out, point)
        n >>= 1
        if n:
            point = add(point, point)
    return out


def finite_quotients():
    cases = 0
    for rank, torsion, modulus in product(range(4), [(), (2, 2), (4, 3)], range(1, 13)):
        # Enumerate a full residue box in the source, independently of the formula.
        representatives = product(*([range(modulus)] * rank), *(range(t) for t in torsion))
        actual = {residue(p, rank, torsion, modulus) for p in representatives}
        require(len(actual) == quotient_order(rank, torsion, modulus), "quotient size")
        cases += 1
    return {"cases": cases, "rank_range": [0, 3], "moduli": [1, 12]}


def reconstruction():
    rank, torsion, bound = 2, (4, 3), 7
    target = (7, -4, 3, 2)
    points = ball(rank, torsion, bound)
    fibers, prior = [], set(points)
    for n in range(1, 7):
        modulus = factorial(n)
        c = residue(target, rank, torsion, modulus)
        current = {p for p in points if residue(p, rank, torsion, modulus) == c}
        require(current <= prior and target in current, "nested nonempty height fibers")
        fibers.append({"n": n, "modulus": modulus, "fiber_size": len(current)})
        prior = current
    require(prior == {target}, "factorial reconstruction uniqueness")
    binary = []
    for n in range(1, 7):
        modulus = 2 ** n
        c = residue(target, rank, torsion, modulus)
        current = {p for p in points if residue(p, rank, torsion, modulus) == c}
        binary.append({"n": n, "fiber_size": len(current)})
    require(current == {(7, -4, 3, t) for t in range(3)}, "prime-to-2 torsion fiber")
    require(residue((1,), 1, (), 2) == residue((-1,), 1, (), 2),
            "strict readback threshold collision")
    # These determinant-one Gram matrices have Rayleigh quotient 1/(N^2+1)
    # on (N,-1), so determinant alone cannot bound the smallest eigenvalue.
    gram_controls = []
    for value in (1, 10, 100):
        matrix = ((1, value), (value, value * value + 1))
        require(matrix[0][0] * matrix[1][1] - matrix[0][1] ** 2 == 1,
                "Gram determinant fixed")
        quadratic = value ** 2 - 2 * value ** 2 + value ** 2 + 1
        require(quadratic == 1, "Gram Rayleigh numerator")
        gram_controls.append({"N": value, "determinant": 1,
                              "least_eigenvalue_upper": str(F(1, value * value + 1))})
    return {"group": "Z^2 + Z/4 + Z/3", "height_bound": bound,
            "ball_size": len(points), "target": target,
            "factorial_fibers": fibers, "binary_fibers": binary,
            "binary_final_fiber": sorted(current), "Gram_controls": gram_controls,
            "threshold_equality_collision": [1, -1]}


def phantom_and_realizable():
    rows, previous = [], None
    bound = 40
    for n in range(1, 13):
        modulus = 2 ** n
        k = pow(3, -1, modulus)
        require((3 * k - 1) % modulus == 0, "inverse-of-3 quotient")
        if previous is not None:
            require(k % (modulus // 2) == previous, "compatible phantom classes")
        matches = [m for m in range(-bound, bound + 1) if (3 * m - 1) % modulus == 0]
        if modulus > 3 * bound + 1:
            require(not matches, "fixed height excluded")
        centered = min((k, k - modulus), key=abs)
        require(abs(centered) == (modulus - (-1) ** n) // 3, "minimal coefficient formula")
        rows.append({"n": n, "least_nonnegative": k, "centered": centered,
                     "bounded_witness_count": len(matches)})
        previous = k
    # Exact E5 checks are finite tests; global nonrealizability uses its proved
    # primitive generator, not this finite point calculation.
    p = (F(-4), F(6))
    e5_rows = []
    previous_k = previous_r = None
    for n in range(1, 6):
        modulus = 2 ** n
        k = pow(3, -1, modulus)
        r = multiple(k, p)
        ell = (3 * k - 1) // modulus
        require(add(multiple(3, r), multiple(-1, p)) == multiple(modulus * ell, p),
                "actual E5 residue witness")
        if previous_k is not None:
            step = (k - previous_k) // (modulus // 2)
            require(add(previous_r, multiple((modulus // 2) * step, p)) == r,
                    "actual E5 transition witness")
        height = max(abs(r[0].numerator), r[0].denominator)
        e5_rows.append({"n": n, "k": k, "height_bits": height.bit_length(),
                        "x": [str(r[0].numerator), str(r[0].denominator)],
                        "y": [str(r[1].numerator), str(r[1].denominator)]})
        previous_k, previous_r = k, r
    # Deliberately large chosen representatives still represent the constant 1.
    growing = [2 ** n + 1 for n in range(1, 13)]
    require(all(m % 2 ** n == 1 for n, m in enumerate(growing, 1)),
            "growing witnesses are not a nonrealizability certificate")
    for n in range(1, 41):
        modulus = 2 ** n
        explicit = (modulus + 1) // 3 if n % 2 else (2 * modulus + 1) // 3
        require(explicit == pow(3, -1, modulus), "40-level audit formula")
        require(min(explicit, modulus - explicit) == (modulus - (-1) ** n) // 3,
                "40-level minimum coefficient")
    for audit_bound in range(101):
        modulus = 2
        while modulus <= 3 * audit_bound + 1:
            modulus *= 2
        require(all((3 * m - 1) % modulus for m in range(-audit_bound, audit_bound + 1)),
                "101 fixed-bound audit exclusions")
    return {"abstract_levels": rows, "fixed_bound": bound, "e5_levels": e5_rows,
            "growing_representatives": growing, "common_small_representative": 1,
            "audit_levels": 40, "audit_fixed_bounds": 101,
            "universal_nonrealizability": "WRITTEN_PROOF: 3m=1 has no integer solution"}


def saturation():
    rows = []
    for n in range(1, 8):
        modulus = 2 ** n
        image = {(3 * a % modulus, b) for a, b in product(range(modulus), repeat=2)}
        require(len(image) == modulus ** 2, "odd index invisible at all tested binary levels")
        rows.append({"modulus": modulus, "image_size": len(image)})
    image3 = {(3 * a % 3, b) for a, b in product(range(3), repeat=2)}
    require(len(image3) == 3, "prime 3 detects index 3")
    independent_but_unsaturated = {(2 * a % 2, b) for a, b in product(range(2), repeat=2)}
    require(len(independent_but_unsaturated) == 2, "independence alone is not 2-saturation")
    return {"matrix": [[3, 0], [0, 1]], "integral_index": 3,
            "binary_levels": rows, "mod_3_image_size": 3,
            "independent_index_2_mod_2_image_size": 2}


def selmer_defects():
    rows = []
    # An abstract model, not an assertion that these groups are actual Sha groups.
    rank, torsion, obstruction = 1, (4, 3), (4, 4)
    for n in range(1, 6):
        modulus = 2 ** n
        mw = quotient_order(rank, torsion, modulus)
        defect = kernel_order(obstruction, modulus)
        selmer_model = mw * defect
        require(selmer_model // mw == defect, "normalized finite obstruction")
        rows.append({"n": n, "MW_quotient": mw, "Selmer_model": selmer_model,
                     "defect": defect})
    require(rows[1]["defect"] == rows[2]["defect"] == prod(obstruction), "stable full primary order")
    # Arbitrarily long finite stretches can conceal later stabilization.
    k = 6
    ambiguity = []
    for n in range(1, k + 2):
        first = 2 ** n * kernel_order((2 ** k, 2 ** k), 2 ** n)
        second = 2 ** (3 * n)
        require((first == second) == (n <= k), "finite slope ambiguity")
        ambiguity.append({"n": n, "rank1_finite_obstruction": first,
                          "rank3_zero_obstruction": second})
    # Verify the adjacent plateau implication over a finite family of groups.
    cases = 0
    for p in (2, 3, 5):
        for exponents in product(range(5), repeat=3):
            orders = tuple(p ** e for e in exponents)
            for n in range(1, 6):
                first = kernel_order(orders, p ** n)
                next_order = kernel_order(orders, p ** (n + 1))
                if first == next_order:
                    require(first == prod(orders), "adjacent defect stability")
                cases += 1
    return {"model_warning": "Abstract groups; no elliptic realization asserted",
            "finite_obstruction": obstruction, "defect_rows": rows,
            "slope_ambiguity": ambiguity, "plateau_finite_cases": cases}


def analytic_controls():
    # F(t)=t^4 + delta*t^2 obeys the even functional-equation symmetry,
    # vanishes to at least order two, and has fourth derivative 24 at zero.
    # A narrow interval for its second derivative need not prove it is zero.
    delta = F(1, 2 ** 60)
    epsilon = F(1, 2 ** 40)
    second = 2 * delta
    require(0 < second < epsilon, "nonzero hidden in a zero-containing interval")
    for t in [F(-2), F(-1, 3), F(0), F(1, 3), F(2)]:
        require(t ** 4 + delta * t ** 2 == (-t) ** 4 + delta * (-t) ** 2, "even symmetry")
    near_one = 1 + delta
    require(1 < near_one < 1 + epsilon and near_one.denominator != 1,
            "near-integer without theorem remains noninteger")
    return {"carrier": "polynomial analytic controls, not elliptic L-functions",
            "delta": str(delta), "second_derivative": str(second),
            "fourth_derivative": 24, "actual_order": 2,
            "zero_second_derivative_comparison_order": 4,
            "near_integer_control": str(near_one)}


def mellin_tail_controls():
    # Load this explicitly adjacent module even under Python's isolated mode.
    path = ROOT / "work" / "mellin_tail.py"
    spec = importlib.util.spec_from_file_location("bsd_general_mellin_tail", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cases = 0
    for a, k, cutoff in product((F(1, 5), F(1), F(3, 2)), range(7), (0, 1, 10, 40)):
        q, bound = module.tail_bound(a, k, cutoff)
        # Independently sum a substantial finite portion of the dominating tail.
        head = sum((4 * q ** n / (a ** (k + 1) * n ** k)
                    for n in range(cutoff + 1, cutoff + 81)), F(0))
        require(0 < head <= bound, "universal tail bounds finite dominant suffix")
        _, later = module.tail_bound(a, k, cutoff + 1)
        require(0 < later < bound, "tail decreases with cutoff")
        cases += 1
    rejected = 0
    for a, k, cutoff in ((F(0), 2, 40), (F(1), -1, 40), (F(1), 2, -1),
                        (0.2, 2, 40), (F(1), 2.0, 40)):
        try:
            module.tail_bound(a, k, cutoff)
        except ValueError:
            rejected += 1
    require(rejected == 5, "invalid tail inputs rejected")
    require(module.tail_bound(1, 2, 40) == module.tail_bound(F(1), 2, 40),
            "integer alpha remains exact rational")
    return {"finite_cases": cases, "invalid_inputs_rejected": rejected,
            "source_sha256": sha256(path.read_bytes()).hexdigest(),
            "example_only": [{"A": "1/5", "k": k, "M": cutoff,
                              "bound": str(module.tail_bound(F(1, 5), k, cutoff)[1])}
                             for k, cutoff in product((2, 4), (40, 80, 160))],
            "curve_assigned": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), "fresh output required; choose an unused path")
    checks = {
        "finite_quotients": finite_quotients(),
        "bounded_reconstruction": reconstruction(),
        "compatible_nonrational_tower": phantom_and_realizable(),
        "saturation_controls": saturation(),
        "selmer_defect_models": selmer_defects(),
        "analytic_nonimplication_controls": analytic_controls(),
        "mellin_tail_controls": mellin_tail_controls(),
    }
    result = {"status": "FINITE_CHECKS_PASS", "python": platform.python_version(),
              "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "general_BSD": "OPEN", "formal_verification": "NOT_RUN", "checks": checks}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "check_groups": list(checks),
                      "general_BSD": "OPEN", "output": str(args.output.resolve())}, indent=2))


if __name__ == "__main__":
    main()
