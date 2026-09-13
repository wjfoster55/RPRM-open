"""Independent exact algebra and signed-Simpson controls for INTERVAL_AUDIT.md.

These controls check specific formulas and hostile cases. They do not turn
finite tests into a general quadrature theorem or audit the local Tate input.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def differentiate_exp_log(expression):
    """Differentiate exp(-t) sum c_(p,k) log(t/b)^p t^(-k)."""
    result = defaultdict(F)
    for (power, denominator_power), coefficient in expression.items():
        result[power, denominator_power] -= coefficient
        result[power, denominator_power + 1] -= denominator_power * coefficient
        if power:
            result[power - 1, denominator_power + 1] += power * coefficient
    return {key: value for key, value in result.items() if value}


def polynomial_simpson_error(power, left, right):
    midpoint, width = (left + right) / 2, right - left
    integral = (right**(power + 1) - left**(power + 1)) / (power + 1)
    simpson = width * (left**power + 4 * midpoint**power + right**power) / 6
    return integral - simpson


def read_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def direct_exp_bounds(x):
    """Independent unscaled Taylor sums, exact degrees 256 and 257."""
    term = total = F(1)
    for k in range(1, 257):
        term *= -x / k
        total += term
    return total - term*x/257, total


def direct_log_bounds(x):
    """Independent unreduced atanh series for the bounded controls x<=4."""
    v = (x-1)/(x+1)
    power, total = v, F(0)
    for j in range(128):
        total += 2*power/(2*j+1)
        power *= v*v
    return total, total + 2*power/(257*(1-v*v))


def audit_receipt():
    receipt_path = ROOT / "evidence" / "interval.json"
    if not receipt_path.exists():
        return {"status": "IMPLEMENTATION_RECEIPT_NOT_AVAILABLE"}
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    budget_path, source_path = ROOT / "work" / "BUDGET.json", ROOT / "work" / "interval.py"
    budget = json.loads(budget_path.read_text(encoding="utf-8"))
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    budget_hash = hashlib.sha256(budget_path.read_bytes()).hexdigest()
    assert receipt["source_sha256"] == source_hash
    assert receipt["budget_sha256"] == budget_hash
    assert budget["Euler_head_cutoffs_in_order"] == [40, 80, 160]
    assert budget["frozen_before_interval_execution"] is True
    assert budget["panels_per_doubling_band"] == 64
    assert budget["target_interval_width"] == "1/100"
    scale = 2**budget["dyadic_bits"]

    def floor_grid(x):
        return F((x.numerator*scale)//x.denominator, scale)

    def ceil_grid(x):
        return -floor_grid(-x)

    implementation = read_module("rank_two_interval_under_audit", source_path)
    for x in map(F, [0, "1/68", "1/3", 1, 3, 10, 32]):
        lower, upper = implementation.exp_minus(x)
        independent_lower, independent_upper = direct_exp_bounds(x)
        assert lower <= independent_lower <= independent_upper <= upper
    for x in map(F, [1, "11/10", "3/2", 2, 3, 4]):
        lower, upper = implementation.log_positive(x)
        independent_lower, independent_upper = direct_log_bounds(x)
        assert lower <= independent_lower <= independent_upper <= upper

    alpha_lo, alpha_hi = map(F, receipt["constants"]["alpha"])
    assert (alpha_lo, alpha_hi) == implementation.constants()[0]
    assert budget["conductor"] == 136**2 == receipt["conductor_input"]
    assert [row["cutoff"] for row in receipt["attempts"]] == [40, 80, 160]
    assert all(not row["head_executed"] for row in receipt["attempts"][:2])

    # Separate divisor enumeration by paired divisors, and integer grid powers.
    tail_q = F(receipt["attempts"][0]["tail"]["q_upper"])
    exp_lo, exp_hi = direct_exp_bounds(alpha_lo)
    assert exp_hi <= tail_q < 1
    q_integer = int(tail_q*scale)
    assert F(q_integer, scale) == tail_q
    power_integer = scale
    terms = {}
    last = budget["divisor_tail_cutoff"]
    for n in range(1, last+2):
        power_integer = (power_integer*q_integer+scale-1)//scale
        if n <= last and n % 4 == 1 and n % 17:
            root = isqrt(n)
            count = 2*sum(n % divisor == 0 for divisor in range(1, root+1))-(root*root == n)
            ceiling = root+(root*root != n)
            terms[n] = ceil_grid(2*count*ceiling*F(power_integer, scale)/(alpha_lo**3*n**3))
    remainder = ceil_grid(4*F(power_integer, scale)/(alpha_lo**3*(last+1)**2*(1-tail_q)))
    for attempt in receipt["attempts"]:
        row = attempt["tail"]
        finite = sum((v for n, v in terms.items() if n > attempt["cutoff"]), F(0))
        assert F(row["finite_divisor_majorant"]) == finite
        assert F(row["infinite_remainder"]) == remainder
        assert F(row["radius"]) == finite+remainder
        assert F(row["q_last_power_upper"]) == F(power_integer, scale)
        if not attempt["head_executed"]:
            assert 2*F(row["radius"]) > F(budget["target_interval_width"])

    chosen = receipt["attempts"][-1]
    cutoff = chosen["cutoff"]
    assert cutoff == receipt["selected_cutoff"] == 160
    local = read_module("rank_two_local_replay_under_audit", ROOT / "work" / "local_inputs.py")
    fresh_coefficients, fresh_primes = local.coefficients(cutoff)
    assert [fresh_coefficients[n] for n in range(1, cutoff+1)] == [chosen["all_coefficients"][str(n)] for n in range(1, cutoff+1)]
    # Independent character sums at every admitted good prime, not a stored PASS.
    for p, ap in fresh_primes.items():
        if p in (2, 17):
            assert ap == 0
            continue
        char_sum = sum((lambda v: 0 if v == 0 else (-1 if v == p-1 else 1))(
                       pow((x*x*x-1156*x) % p, (p-1)//2, p)) for x in range(p))
        assert -char_sum == ap

    total_low = total_high = F(0)
    counted_panels = 0
    expected_indices = [n for n in range(1, cutoff+1) if fresh_coefficients[n]]
    assert [term["n"] for term in chosen["head"]["terms"]] == expected_indices
    for term in chosen["head"]["terms"]:
        n, a, kernel = term["n"], term["a_n"], term["kernel"]
        assert a == fresh_coefficients[n]
        blo, bhi = map(F, kernel["b"])
        assert (blo, bhi) == (n*alpha_lo, n*alpha_hi)
        simlo, simhi = map(F, kernel["Simpson_sum"])
        errlo, errhi = map(F, kernel["signed_quadrature_error"])
        parameter, tail = F(kernel["parameter_loss"]), F(kernel["improper_integral_tail"])
        assert parameter == ceil_grid((bhi-blo)*implementation.exp_minus(blo)[1]/blo**2)
        assert tail == ceil_grid(implementation.exp_minus(F(32))[1]/blo)
        rawlo, rawhi = simlo+errlo-parameter, simhi+errhi+tail
        assert [rawlo, rawhi] == list(map(F, kernel["raw_H"]))
        assert rawhi-rawlo == F(kernel["width_before_nonnegative_clip"]) == sum(map(F, kernel["width_components"].values()))
        hlo, hhi = max(F(0), rawlo), rawhi
        assert [hlo, hhi] == list(map(F, kernel["H"]))
        weight = F(2*a, n)
        assert weight == F(term["weight"])
        tlo, thi = min(weight*hlo, weight*hhi), max(weight*hlo, weight*hhi)
        assert [tlo, thi] == list(map(F, term["scaled_term"]))
        total_low += tlo
        total_high += thi
        left, bands = blo, 0
        while left < 32:
            left = min(2*left, F(32))
            bands += 1
        assert kernel["bands"] == bands <= budget["maximum_bands_per_kernel"]
        assert kernel["panels"] == 64*bands
        counted_panels += kernel["panels"]
    assert [total_low, total_high] == list(map(F, chosen["head"]["scaled_head_alpha_times_lambda2"]))
    products = [x/y for x in [total_low, total_high] for y in [alpha_lo, alpha_hi]]
    head_lo, head_hi = floor_grid(min(products)), ceil_grid(max(products))
    assert [head_lo, head_hi] == list(map(F, chosen["head"]["completed_head"]))
    radius = F(chosen["tail"]["radius"])
    lo, hi = head_lo-radius, head_hi+radius
    assert [lo, hi] == list(map(F, chosen["raw_completed_interval"]))
    exported_lo = F(lo.numerator*10**8//lo.denominator, 10**8)
    exported_hi = F(-((-hi.numerator*10**8)//hi.denominator), 10**8)
    assert [exported_lo, exported_hi] == list(map(F, receipt["lambda2_interval"]))
    assert exported_lo > 0 and exported_hi-exported_lo <= F(1, 100)
    assert counted_panels == receipt["total_panels"] <= budget["maximum_total_panels"]
    return {"status": "PASSED", "source_sha256": source_hash,
            "budget_sha256": budget_hash,
            "receipt_sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
            "elementary_controls": {"exp": 7, "log": 6, "method": "independent unscaled/unreduced exact series contained in implementation bounds"},
            "fresh_local_coefficients_compared_through": cutoff,
            "independent_good_prime_character_sums_through": cutoff,
            "tail_reassembled_through": last,
            "nonzero_head_terms_reassembled": len(expected_indices),
            "total_panels": counted_panels,
            "lambda2_interval": [str(exported_lo), str(exported_hi)],
            "lambda2_width": str(exported_hi-exported_lo),
            "finite_head_width": str(head_hi-head_lo),
            "tail_radius": str(radius),
            "limitation": "Exact ledger assembly replay plus source inspection, not an independent replay of all Simpson panel evaluations or a formal proof"}


def main():
    derivative = {(1, 1): F(1)}
    derivatives = []
    for _ in range(4):
        derivative = differentiate_exp_log(derivative)
        derivatives.append(derivative)
    expected_second = {(1, 1): F(1), (1, 2): F(2), (1, 3): F(2),
                       (0, 2): F(-2), (0, 3): F(-3)}
    expected_fourth = {(1, 1): F(1), (1, 2): F(4), (1, 3): F(12),
                       (1, 4): F(24), (1, 5): F(24),
                       (0, 2): F(-4), (0, 3): F(-18),
                       (0, 4): F(-44), (0, 5): F(-50)}
    assert derivatives[1] == expected_second
    assert derivatives[3] == expected_fourth

    # The atanh series establishes 2/3 < log 2 < 25/36 < 7/10.
    log2_lower = F(2, 3)
    log2_upper = F(2, 3) + F(2, 81) / (1 - F(1, 9))
    assert log2_upper == F(25, 36) < F(7, 10)
    j2_curvature_bracket_upper = F(7, 10)**2 - 2 * log2_lower + (1 - log2_lower)/2
    assert j2_curvature_bracket_upper == F(-203, 300) < 0

    controls = []
    for left, right in [(F(0), F(1)), (F(1), F(2)),
                        (F(1, 17), F(2, 17)), (F(31, 8), F(4))]:
        width = right - left
        quartic_error = polynomial_simpson_error(4, left, right)
        assert quartic_error == -width**5/F(120)
        quintic_error = polynomial_simpson_error(5, left, right)
        lower = -width**5*(120*right)/2880
        upper = -width**5*(120*left)/2880
        assert lower <= quintic_error <= upper
        # The reversed, positive fourth-derivative sign fails at each quartic.
        assert not width**5/F(120) <= quartic_error
        controls.append({"panel": [str(left), str(right)],
                         "quartic_error": str(quartic_error),
                         "quintic_error": str(quintic_error),
                         "quintic_signed_error_bounds": [str(lower), str(upper)]})

    # Bounded arithmetic controls for ceiling-root witnesses used in the tail.
    for n in range(1, 4097):
        floor = isqrt(n)
        ceiling = floor + (floor*floor != n)
        assert (ceiling - 1)**2 < n <= ceiling**2
    result = {
        "grade": "EXACT_FINITE_ALGEBRA_AND_HOSTILE_CONTROLS",
        "scope": "Derivative identities and signed Simpson formula controls; written general bounds are in INTERVAL_AUDIT.md",
        "kernel": "exp(-t)*log(t/b)/t, t>=b>0",
        "second_derivative_matches": True,
        "fourth_derivative_matches": True,
        "polynomial_controls": controls,
        "blanket_positive_J2_curvature_refuted_at": {"b": "1", "u": "2", "bracket_upper": str(j2_curvature_bracket_upper)},
        "blanket_positive_H_curvature_refuted": "F_b''(b)=-exp(-b)*(2/b^2+3/b^3)<0",
        "ceil_sqrt_integer_witnesses_checked": [1, 4096],
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "implementation_receipt_audit": audit_receipt(),
    }
    target = ROOT / "evidence" / "interval_audit.json"
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": True, "receipt": str(target)}))


if __name__ == "__main__":
    main()
