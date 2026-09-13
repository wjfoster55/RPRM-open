"""Exact E34 rank-two completed coefficient enclosure; no floating arithmetic.

Uses freshly counted Euler coefficients and proved outward elementary bounds.
Source theorem inputs and actual analytic rank implications are separate.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
import json
from math import isqrt
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
BUDGET_PATH = ROOT / "work/BUDGET.json"
BUDGET = json.loads(BUDGET_PATH.read_text())
SCALE = 1 << BUDGET["dyadic_bits"]
MODEL = [0, 0, 0, -1156, 0]


def down(x):
    x = F(x)
    return F(x.numerator * SCALE // x.denominator, SCALE)


def up(x):
    return -down(-x)


def pair(lo, hi):
    assert lo <= hi
    return [str(lo), str(hi)]


def multiply_intervals(a, b):
    products = [x * y for x in a for y in b]
    return down(min(products)), up(max(products))


@lru_cache(maxsize=None)
def exp_minus(x):
    x = F(x)
    if x < 0:
        raise ValueError("exp argument must be nonnegative")
    halves = 0
    z = x
    while z > 1:
        z /= 2
        halves += 1
    term = total = F(1)
    even = None
    for k in range(1, 32):
        term *= -z / k
        total += term
        if k == 30:
            even = total
    lo, hi = max(F(0), down(total)), up(even)
    for _ in range(halves):
        lo, hi = down(lo * lo), up(hi * hi)
    assert 0 <= lo <= hi <= 1
    return lo, hi


def log_unit(z):
    assert 1 <= z <= 2
    v = (z - 1) / (z + 1)
    v2 = v * v
    power, total = v, F(0)
    terms = BUDGET["log_series_terms"]
    for j in range(terms):
        total += 2 * power / (2 * j + 1)
        power *= v2
    remainder = 2 * power / ((2 * terms + 1) * (1 - v2))
    return down(total), up(total + remainder)


LOG_TWO = log_unit(F(2))


@lru_cache(maxsize=None)
def log_positive(x):
    x = F(x)
    if x < 1:
        raise ValueError("this kernel admits logarithm arguments >=1")
    shifts, z = 0, x
    while z >= 2:
        z /= 2
        shifts += 1
    lo, hi = log_unit(z)
    return down(lo + shifts * LOG_TWO[0]), up(hi + shifts * LOG_TWO[1])


def atan(reciprocal, terms):
    total = sum((F((-1) ** k, (2 * k + 1) * reciprocal ** (2 * k + 1))
                 for k in range(terms)), F(0))
    other = total + F((-1) ** terms, (2 * terms + 1) * reciprocal ** (2 * terms + 1))
    return min(total, other), max(total, other)


def constants():
    a, b = atan(5, 64), atan(239, 20)
    pi = (down(16 * a[0] - 4 * b[1]), up(16 * a[1] - 4 * b[0]))
    alpha = (down(pi[0] / 68), up(pi[1] / 68))
    assert F(3, 68) < alpha[0] <= alpha[1] < F(22, 476)
    assert 136 ** 2 == BUDGET["conductor"]
    return alpha, {"pi": pair(*pi), "alpha": pair(*alpha),
                   "identity": "alpha=2*pi/sqrt(18496)=pi/68",
                   "pi_method": "Machin identity, alternating atan enclosures"}


def primes(limit):
    return [n for n in range(2, limit + 1) if all(n % d for d in range(2, isqrt(n) + 1))]


def euler_coefficients(limit):
    records = []
    traces = {}
    for p in primes(limit):
        # Root-multiplicity table rather than Euler's quadratic-character formula.
        roots = [0] * p
        for y in range(p):
            roots[y * y % p] += 1
        count = 1 + sum(roots[(x ** 3 - 1156 * x) % p] for x in range(p))
        status = "additive" if p in (2, 17) else "good"
        a_p = 0 if status == "additive" else p + 1 - count
        if status == "good":
            assert a_p * a_p <= 4 * p
            if p % 4 == 3:
                assert a_p == 0
        traces[p] = a_p
        records.append({"p": p, "projective_model_count": count,
                        "local_type": status, "a_p": a_p})
    coefficients = {1: 1}
    for n in range(2, limit + 1):
        if n % 2 == 0 or n % 17 == 0:
            coefficients[n] = 0
            continue
        remaining, result = n, 1
        for p in traces:
            exponent = 0
            while remaining % p == 0:
                exponent += 1
                remaining //= p
            if not exponent:
                continue
            old, current = 1, traces[p]
            for _ in range(2, exponent + 1):
                old, current = current, traces[p] * current - p * old
            result *= current
        assert remaining == 1
        coefficients[n] = result
        if n % 4 != 1:
            assert result == 0
    return coefficients, records


def divisor_counts(limit):
    counts = [0] * (limit + 1)
    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            counts[multiple] += 1
    return counts


def all_term_tails(alpha_lo):
    last = BUDGET["divisor_tail_cutoff"]
    counts = divisor_counts(last)
    q = exp_minus(alpha_lo)[1]
    assert 0 < q < 1
    q_power = F(1)
    terms = {}
    for n in range(1, last + 2):
        q_power = up(q_power * q)
        if n <= last and n % 4 == 1 and n % 17:
            ceil_root = isqrt(n)
            if ceil_root ** 2 < n:
                ceil_root += 1
            terms[n] = up(2 * counts[n] * ceil_root * q_power / (alpha_lo ** 3 * n ** 3))
    remainder = up(4 * q_power / (alpha_lo ** 3 * (last + 1) ** 2 * (1 - q)))
    # q_power is an upper bound for q^(last+1), not an asserted exact power.
    rows = {}
    for cutoff in BUDGET["Euler_head_cutoffs_in_order"]:
        finite_majorant = sum((v for n, v in terms.items() if n > cutoff), F(0))
        rows[cutoff] = {"radius": str(finite_majorant + remainder),
                        "finite_divisor_majorant": str(finite_majorant),
                        "infinite_remainder": str(remainder),
                        "last_divisor_index": last, "q_upper": str(q),
                        "q_last_power_upper": str(q_power),
                        "support": "n%4=1 and n%17 != 0",
                        "all_term_premise": "Hasse/Euler |a_n|<=d(n)sqrt(n); CM support proof"}
    return rows


def fourth_bound(left, right, b):
    log_lo = log_positive(left / b)[0]
    log_hi = log_positive(right / b)[1]
    def positive(t):
        return 1 / t + 4 / t ** 2 + 12 / t ** 3 + 24 / t ** 4 + 24 / t ** 5
    def negative(t):
        return 4 / t ** 2 + 18 / t ** 3 + 44 / t ** 4 + 50 / t ** 5
    bracket = (log_lo * positive(right) - negative(left),
               log_hi * positive(left) - negative(right))
    exponential = (exp_minus(right)[0], exp_minus(left)[1])
    return multiply_intervals(exponential, bracket)


def integrand(t, b):
    lo, hi = multiply_intervals(exp_minus(t), log_positive(t / b))
    return down(lo / t), up(hi / t)


def h_kernel(blo, bhi):
    assert 0 < blo <= bhi < BUDGET["transformed_integral_end"]
    end = F(BUDGET["transformed_integral_end"])
    panels = BUDGET["panels_per_doubling_band"]
    low = high = errlo = errhi = F(0)
    left, band_count, panel_count = blo, 0, 0
    while left < end:
        right = min(2 * left, end)
        width = (right - left) / panels
        for j in range(panels):
            a = left + j * width
            c = a + width
            middle = (a + c) / 2
            fa, fm, fc = integrand(a, blo), integrand(middle, blo), integrand(c, blo)
            low += down(width * (fa[0] + 4 * fm[0] + fc[0]) / 6)
            high += up(width * (fa[1] + 4 * fm[1] + fc[1]) / 6)
            f4lo, f4hi = fourth_bound(a, c, blo)
            errlo += down(-width ** 5 * f4hi / 2880)
            errhi += up(-width ** 5 * f4lo / 2880)
            panel_count += 1
        left = right
        band_count += 1
    assert band_count <= BUDGET["maximum_bands_per_kernel"]
    alpha_loss = up((bhi - blo) * exp_minus(blo)[1] / blo ** 2)
    improper_tail = up(exp_minus(end)[1] / blo)
    raw_lo, raw_hi = low + errlo - alpha_loss, high + errhi + improper_tail
    lower, upper = max(F(0), raw_lo), raw_hi
    assert 0 <= lower <= upper
    row = {"b": pair(blo, bhi), "H": pair(lower, upper),
           "Simpson_sum": pair(low, high), "signed_quadrature_error": pair(errlo, errhi),
           "parameter_loss": str(alpha_loss), "improper_integral_tail": str(improper_tail),
           "raw_H": pair(raw_lo, raw_hi), "panels": panel_count, "bands": band_count,
           "width_before_nonnegative_clip": str(raw_hi - raw_lo),
           "width_components": {"elementary_rounding": str(high - low),
                                "quadrature": str(errhi - errlo),
                                "parameter": str(alpha_loss), "improper_tail": str(improper_tail)}}
    assert raw_hi - raw_lo == sum(map(F, row["width_components"].values()))
    return lower, upper, row


def assemble_head(coefficients, alpha, cutoff, kernels):
    slo = shi = F(0)
    terms = []
    for n in range(1, cutoff + 1):
        a = coefficients[n]
        if not a:
            continue
        if n not in kernels:
            kernels[n] = h_kernel(n * alpha[0], n * alpha[1])
        lo, hi, row = kernels[n]
        weight = F(2 * a, n)
        termlo, termhi = min(weight * lo, weight * hi), max(weight * lo, weight * hi)
        slo += termlo
        shi += termhi
        terms.append({"n": n, "a_n": a, "weight": str(weight),
                      "scaled_term": pair(termlo, termhi), "kernel": row})
    completed = multiply_intervals((slo, shi), (1 / alpha[1], 1 / alpha[0]))
    return {"scaled_head_alpha_times_lambda2": pair(slo, shi),
            "completed_head": pair(*completed), "terms": terms}


def admit_model(model):
    if model != MODEL:
        raise ValueError("The supplied local/rank proof is bound to E34, not this model")


def full_interval(head, tail):
    if tail is None or "all_term_premise" not in tail:
        raise ValueError("A finite head cannot certify the infinite L-function without a proved tail")
    lo, hi = map(F, head["completed_head"])
    radius = F(tail["radius"])
    return lo - radius, hi + radius


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("Choose a new receipt path")
    start = time.monotonic()
    admit_model(BUDGET["curve_a_invariants"])
    alpha, const = constants()
    tails = all_term_tails(alpha[0])
    attempts, kernels, selected = [], {}, None
    for cutoff in BUDGET["Euler_head_cutoffs_in_order"]:
        tail = tails[cutoff]
        radius = F(tail["radius"])
        if 2 * radius > F(BUDGET["target_interval_width"]):
            attempts.append({"cutoff": cutoff, "status": "OPEN_WITH_THIS_TAIL_BOUND",
                             "head_executed": False, "tail": tail,
                             "reason": "Twice this tail radius already exceeds target width"})
            print(f"M={cutoff}: current certified tail too wide; advancing prescribed cutoff", flush=True)
            continue
        coefficients, prime_data = euler_coefficients(cutoff)
        head = assemble_head(coefficients, alpha, cutoff, kernels)
        lo, hi = full_interval(head, tail)
        # Outward decimal export uses exact rational ceiling/floor, not floats.
        export_lo = F(lo.numerator * 10 ** 8 // lo.denominator, 10 ** 8)
        export_hi = F(-((-hi.numerator * 10 ** 8) // hi.denominator), 10 ** 8)
        success = export_hi - export_lo <= F(BUDGET["target_interval_width"]) and (export_lo > 0 or export_hi < 0)
        attempt = {"cutoff": cutoff, "status": "ENCLOSURE_SUCCEEDED" if success else "OPEN",
                   "head_executed": True, "tail": tail, "head": head,
                   "all_coefficients": {str(n): a for n, a in coefficients.items()},
                   "prime_data": prime_data, "raw_completed_interval": pair(lo, hi),
                   "completed_interval": pair(export_lo, export_hi),
                   "completed_width": str(export_hi - export_lo)}
        attempts.append(attempt)
        print(f"M={cutoff}: {attempt['status']}; completed width {attempt['completed_width']}", flush=True)
        if success:
            selected = attempt
            break
    total_panels = sum(row[2]["panels"] for row in kernels.values())
    assert total_panels <= BUDGET["maximum_total_panels"]
    controls = {}
    try:
        admit_model([0, 0, 0, -1155, 0])
    except ValueError as exc:
        controls["changed_model"] = {"status": "REJECTED", "reason": str(exc)}
    if selected:
        try:
            full_interval(selected["head"], None)
        except ValueError as exc:
            controls["removed_tail"] = {"status": "NOT_PROMOTED", "reason": str(exc),
                                        "finite_head_preserved": selected["head"]["completed_head"]}
    scaled = None
    if selected:
        scaled = pair(*multiply_intervals(tuple(map(F, selected["completed_interval"])), alpha))
    result = {"status": "CERTIFIED_COEFFICIENT_INTERVAL" if selected else "OPEN",
              "created_utc": datetime.now(timezone.utc).isoformat(), "model": MODEL,
              "conductor_input": BUDGET["conductor"], "root_number_input": 1,
              "constants": const, "attempts": attempts,
              "selected_cutoff": selected["cutoff"] if selected else None,
              "lambda2_interval": selected["completed_interval"] if selected else None,
              "alpha_times_lambda2_interval": scaled,
              "raw_c2_requires": "Exact lower zeros, justified separately from proved rank>=2 and published low-rank theorem",
              "total_panels": total_panels, "controls": controls,
              "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "budget_sha256": sha256(BUDGET_PATH.read_bytes()).hexdigest(),
              "elapsed_seconds": time.monotonic() - start,
              "formal_verification": "NOT_RUN", "general_BSD": "OPEN"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "selected_cutoff": result["selected_cutoff"],
                      "lambda2_interval": result["lambda2_interval"],
                      "alpha_times_lambda2_interval": scaled,
                      "total_panels": total_panels, "output": str(args.output.resolve())}, indent=2), flush=True)


if __name__ == "__main__":
    main()
