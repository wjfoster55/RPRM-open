#!/usr/bin/env python3
"""Independent E5 finite Euler check and exact rational central-derivative enclosure.

No supplied implementation imports, archived receipts, rank data, or ordinary
floating special functions enter this calculation. See INTERVAL_DERIVATION.md.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from math import isqrt
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
EXPERIMENT = HERE.parent
BITS = 80
SCALE = 1 << BITS
GRID = F(1, SCALE)


def q(value):
    return str(F(value))


def down(value, denominator=SCALE):
    value = F(value)
    return F(value.numerator * denominator // value.denominator, denominator)


def up(value, denominator=SCALE):
    value = F(value)
    return F(-((-value.numerator * denominator) // value.denominator), denominator)


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def primes_through(limit):
    flags = [True] * (limit + 1)
    flags[:2] = [False, False]
    for p in range(2, isqrt(limit) + 1):
        if flags[p]:
            flags[p*p:limit+1:p] = [False] * (((limit - p*p)//p) + 1)
    return [p for p, flag in enumerate(flags) if flag]


def local_prime_data(p):
    """At odd p use Euler's criterion, structurally distinct from root tables."""
    if p == 2:
        pairs = [(x, y) for x in range(2) for y in range(2)
                 if (y*y - x*x*x + 25*x) % 2 == 0]
        count = len(pairs) + 1
        return {"p": p, "projective_model_count": count,
                "trace": p+1-count, "status": "additive",
                "affine_pairs": pairs, "local_factor": "1"}
    chars = []
    for x in range(p):
        rhs = (x*x*x - 25*x) % p
        criterion = pow(rhs, (p-1)//2, p)
        chars.append(0 if criterion == 0 else (1 if criterion == 1 else -1))
    count = p + 1 + sum(chars)
    trace = p + 1 - count
    assert trace * trace <= 4*p  # finite consistency; not proof of all-p Hasse
    return {"p": p, "projective_model_count": count, "trace": trace,
            "status": "additive" if p == 5 else "good",
            "quadratic_character_sum": sum(chars),
            "local_factor": "1" if p == 5 else f"1-({trace})*T+{p}*T^2"}


def euler_coefficients(limit):
    pdata = {p: local_prime_data(p) for p in primes_through(limit)}
    result = {1: 1}
    for n in range(2, limit + 1):
        if n % 2 == 0 or n % 5 == 0:
            result[n] = 0
            continue
        remaining, value = n, 1
        for p in pdata:
            if remaining % p:
                continue
            exponent = 0
            while remaining % p == 0:
                remaining //= p
                exponent += 1
            previous, current = 1, pdata[p]["trace"]
            for unused in range(2, exponent + 1):
                previous, current = current, pdata[p]["trace"]*current-p*previous
            value *= current
        assert remaining == 1
        result[n] = value
    return result, list(pdata.values())


def atan_bounds(reciprocal, terms):
    # S_terms uses k=0,...,terms-1. The next alternating term supplies the
    # opposite bound because 0<1/reciprocal<1 and magnitudes decrease to zero.
    total = sum((F((-1)**k, (2*k+1)*reciprocal**(2*k+1))
                 for k in range(terms)), F(0))
    other = total + F((-1)**terms, (2*terms+1)*reciprocal**(2*terms+1))
    return min(total, other), max(total, other)


def constants():
    a5 = atan_bounds(5, 64)
    a239 = atan_bounds(239, 20)
    pi_lo_exact, pi_hi_exact = 16*a5[0]-4*a239[1], 16*a5[1]-4*a239[0]
    pi_lo, pi_hi = down(pi_lo_exact), up(pi_hi_exact)
    sqrt_n = isqrt(2*SCALE*SCALE)
    sqrt_lo, sqrt_hi = F(sqrt_n, SCALE), F(sqrt_n+1, SCALE)
    assert sqrt_lo*sqrt_lo < 2 < sqrt_hi*sqrt_hi
    alpha_lo, alpha_hi = down(pi_lo/(10*sqrt_hi)), up(pi_hi/(10*sqrt_lo))
    assert F(1, 5) < alpha_lo < alpha_hi < F(1, 4)
    assert F(7, 5) < sqrt_lo < sqrt_hi < F(3, 2)
    return (alpha_lo, alpha_hi), {
        "pi": [q(pi_lo), q(pi_hi)],
        "pi_method": "Machin pi=16 atan(1/5)-4 atan(1/239); alternating finite sums",
        "pi_arctangent_terms": [64, 20],
        "sqrt2": [q(sqrt_lo), q(sqrt_hi)],
        "sqrt2_integer_witness": {"r": sqrt_n, "scale": SCALE,
            "r_squared": sqrt_n*sqrt_n,
            "2_scale_squared": 2*SCALE*SCALE,
            "r_plus_1_squared": (sqrt_n+1)*(sqrt_n+1)},
        "alpha": [q(alpha_lo), q(alpha_hi)],
        "alpha_width": q(alpha_hi-alpha_lo),
        "coarse_alpha_bounds": ["1/5", "1/4"],
        "exp_minus_alpha_upper": "5/6",
        "rounding": "outward, denominator 2^80"
    }


def exp_minus(r):
    """Certified exp(-r) interval; only nonnegative exact rational arguments."""
    r = F(r)
    if r < 0:
        raise ValueError("exp_minus requires r >= 0")
    halvings = 0
    z = r
    while z > 1:
        z /= 2
        halvings += 1
    term, partial = F(1), F(1)
    even = None
    for k in range(1, 32):
        term *= -z / k
        partial += term
        if k == 30:
            even = partial
    lo, hi = down(partial), up(even)
    assert 0 <= lo <= hi <= 1
    for unused in range(halvings):
        lo, hi = down(lo*lo), up(hi*hi)
    return lo, hi


def baseline(coefficients, const_data):
    cutoff, alpha_lower, ratio = 20, F(1, 5), F(5, 6)
    assert coefficients[1] == 1
    other_positive = [n for n in range(2, cutoff+1) if coefficients[n] > 0]
    negative_rows = []
    for n in range(2, cutoff+1):
        if coefficients[n] < 0:
            magnitude_bound = F(2*abs(coefficients[n]), n)*ratio**n/(alpha_lower*n)
            negative_rows.append({"n": n, "a_n": coefficients[n],
                                  "absolute_term_bound": q(magnitude_bound)})
    neg_bound = sum((F(row["absolute_term_bound"]) for row in negative_rows), F(0))
    tail = 4*ratio**(cutoff+1)/(alpha_lower*(cutoff+1)*(1-ratio))
    leading = F(8, 9)
    lower = leading-neg_bound-tail
    # This advertised rational is compared only after recomputing every operand.
    advertised = F(615556405007957768183, 937494780448358006784)
    assert lower == advertised
    assert lower > F(13, 20)
    return {
        "task_id": "B02", "status": "CONFIRMED",
        "evidence_kind": ["INDEPENDENT_EXACT_FINITE_COMPUTATION", "WRITTEN_DERIVATION", "THEOREM_CITED"],
        "nonzero_through_20": {str(n): a for n, a in coefficients.items() if n <= 20 and a},
        "leading_lower": q(leading), "retained_negative_rows": negative_rows,
        "additional_positive_terms_ignored": other_positive,
        "negative_magnitude_bound": q(neg_bound), "entire_tail_after_20_bound": q(tail),
        "lower_bound": q(lower), "advertised_rational_reconstructed": lower == advertised,
        "margin_above_13_over_20": q(lower-F(13, 20)),
        "premises": [
            {"id": "MELLIN_IDENTITY", "support": "B01 separate source and normalization check; not inferred from finite arithmetic"},
            {"id": "ALPHA_RANGE", "support": "exact Machin and integer square-root enclosure in constants", "bounds": const_data["coarse_alpha_bounds"]},
            {"id": "EXP_RATIO", "support": "exp(alpha)>1+alpha>6/5, hence exp(-alpha)<5/6"},
            {"id": "ALL_N_COEFFICIENT_BOUND", "support": "Hasse theorem -> Euler roots -> |a_n|<=d(n)sqrt(n)<=2n, with additive factors 1; full written derivation"},
            {"id": "E1_UPPER", "support": "integral_x^infinity exp(-t)/t dt <= exp(-x)/x for every x>0"},
            {"id": "LEADING_TERM", "support": "alpha<1/4, exp(-t)>1/3 on (1/4,1), log(2)>2/3; hence 2E1(alpha)>8/9"},
            {"id": "COMPLETE_TAIL", "support": "geometric sum covering every n>=21; no sampled sign/zero extrapolation"}
        ]
    }


def e1_enclosure(x_lo, x_hi, panels_per_band):
    """Enclose E1(x) for any x in [x_lo,x_hi] by finite midpoint quadrature."""
    assert 0 < x_lo <= x_hi
    end = F(32)
    if x_lo >= end:
        # Permitted later-cutoff branch; no improper negative integration range.
        tail_bound = up(exp_minus(x_lo)[1] / x_lo)
        return F(0), tail_bound, {
            "x": [q(x_lo), q(x_hi)], "method": "direct positive integral tail",
            "lower": "0", "upper": q(tail_bound), "width": q(tail_bound),
            "alpha_input_loss": "0", "quadrature_error_bound": "0",
            "midpoint_exp_and_rounding_gap": "0", "integration_tail": q(tail_bound),
            "panels": 0, "bands": 0, "signed_head_width_contribution": None
        }
    alpha_loss = up((x_hi-x_lo)/x_lo)
    midpoint_lo = F(0)
    midpoint_hi = F(0)
    curvature = F(0)
    exp_uncertainty = F(0)
    panel_count, band_count = 0, 0
    left = x_lo
    while left < end:
        right = min(2*left, end)
        step = (right-left)/panels_per_band
        for index in range(panels_per_band):
            u = left + index*step
            midpoint = u + step/2
            exp_lo, exp_hi = exp_minus(midpoint)
            exact_panel_lo = step*exp_lo/midpoint
            exact_panel_hi = step*exp_hi/midpoint
            midpoint_lo += down(exact_panel_lo)
            midpoint_hi += up(exact_panel_hi)
            exp_uncertainty += up(exact_panel_hi-exact_panel_lo)
            # On this panel f'' is decreasing, so f''(u) is the maximum.
            exp_u_hi = exp_minus(u)[1]
            f2_upper = exp_u_hi*(1/u + 2/u**2 + 2/u**3)
            curvature += up(step**3*f2_upper/24)
            panel_count += 1
        left = right
        band_count += 1
    assert band_count <= 8 and panel_count <= 1024
    integration_tail = up(exp_minus(end)[1]/end)
    lo = midpoint_lo-alpha_loss
    hi = midpoint_hi+curvature+integration_tail
    rounding_allowance = 2*panel_count*GRID
    midpoint_gap = midpoint_hi-midpoint_lo
    assert midpoint_gap <= exp_uncertainty+rounding_allowance
    assert hi-lo == alpha_loss+midpoint_gap+curvature+integration_tail
    row = {
        "x": [q(x_lo), q(x_hi)], "integration_range": [q(x_lo), q(end)],
        "method": "midpoint with analytic second-derivative error bound",
        "lower": q(lo), "upper": q(hi), "width": q(hi-lo),
        "midpoint_lower": q(midpoint_lo), "midpoint_upper": q(midpoint_hi),
        "alpha_input_loss": q(alpha_loss),
        "quadrature_error_bound": q(curvature),
        "quadrature_bound_rounding_already_included_at_most": q(panel_count*GRID),
        "midpoint_exp_and_rounding_gap": q(midpoint_gap),
        "exp_evaluation_uncertainty_bound": q(exp_uncertainty),
        "midpoint_outward_rounding_allowance": q(rounding_allowance),
        "integration_tail": q(integration_tail),
        "panels": panel_count, "bands": band_count,
        "error_ledger_identity_checked": True
    }
    return lo, hi, row


def tail_premise(cutoff):
    return {
        "coefficient_domain": "every integer n >= 1",
        "coefficient_abs_upper": "2*n",
        "all_term_coefficient_bound": {
            "theorem": "Hasse bound, good Euler recurrence, coprime multiplicativity, additive factors 1",
            "proof_ref": "INTERVAL_DERIVATION.md#all-term-coverage",
            "scope": "E5 all n >= 1"
        },
        "e1_inequality": "E1(x)<=exp(-x)/x for every x>0",
        "alpha_lower": "1/5", "exp_minus_alpha_upper": "5/6",
        "starts_at": cutoff+1
    }


def promote_finite_head(claim):
    """Small E5-specific proof obligation check used by the actual K04 path."""
    head_lo, head_hi = map(F, claim["finite_head_interval"])
    cutoff = claim["cutoff"]
    assert head_lo <= head_hi
    premise = claim.get("tail_premise", {})
    required = ["all_term_coefficient_bound", "e1_inequality", "alpha_lower",
                "exp_minus_alpha_upper", "starts_at"]
    missing = [name for name in required if name not in premise]
    if missing:
        return {"status": "OPEN", "promotion": "REJECTED",
                "reason": "Finite head does not enclose the infinite sum without all omitted terms covered.",
                "missing": missing, "finite_head_interval": claim["finite_head_interval"],
                "infinite_sum_interval": None}
    assert premise["all_term_coefficient_bound"]["scope"] == "E5 all n >= 1"
    assert premise["coefficient_abs_upper"] == "2*n"
    assert premise["starts_at"] == cutoff+1
    a, ratio = F(premise["alpha_lower"]), F(premise["exp_minus_alpha_upper"])
    assert a == F(1, 5) and ratio == F(5, 6)
    tail = 4*ratio**(cutoff+1)/(a*(cutoff+1)*(1-ratio))
    return {"status": "CONFIRMED", "promotion": "SUPPORTED_WITH_CITED_THEOREM",
            "infinite_sum_interval": [q(head_lo-tail), q(head_hi+tail)],
            "tail_radius": q(tail)}


def attempt(cutoff, panels, alpha, coefficients):
    alpha_lo, alpha_hi = alpha
    lo, hi = F(0), F(0)
    rows = []
    ledger = {key: F(0) for key in ["alpha_enclosure", "retained_quadrature",
              "retained_exp_and_midpoint_rounding", "retained_integral_tails"]}
    for n, coefficient in coefficients.items():
        if not coefficient:
            continue
        e_lo, e_hi, row = e1_enclosure(n*alpha_lo, n*alpha_hi, panels)
        weight = F(2*coefficient, n)
        if weight >= 0:
            term_lo, term_hi = weight*e_lo, weight*e_hi
        else:
            term_lo, term_hi = weight*e_hi, weight*e_lo
        lo += term_lo
        hi += term_hi
        row.update({"n": n, "a_n": coefficient, "signed_weight": q(weight),
                    "term_interval": [q(term_lo), q(term_hi)],
                    "signed_head_width_contribution": q(term_hi-term_lo)})
        rows.append(row)
        for total_key, row_key in [
            ("alpha_enclosure", "alpha_input_loss"),
            ("retained_quadrature", "quadrature_error_bound"),
            ("retained_exp_and_midpoint_rounding", "midpoint_exp_and_rounding_gap"),
            ("retained_integral_tails", "integration_tail")]:
            ledger[total_key] += abs(weight)*F(row[row_key])
    assert hi-lo == sum(ledger.values())
    claim = {"curve_a_invariants": [0,0,0,-25,0], "requested_quantity": "c1=L'(E5,1)",
             "cutoff": cutoff, "finite_head_interval": [q(lo), q(hi)],
             "tail_premise": tail_premise(cutoff)}
    promoted = promote_finite_head(claim)
    raw_lo, raw_hi = map(F, promoted["infinite_sum_interval"])
    tail = F(promoted["tail_radius"])
    display_lo, display_hi = down(raw_lo, 10**6), up(raw_hi, 10**6)
    ledger["infinite_coefficient_tail_width"] = 2*tail
    ledger["signed_multiplication_and_summation_rounding"] = F(0)
    ledger["endpoint_export_enlargement"] = (raw_lo-display_lo)+(display_hi-raw_hi)
    assert display_hi-display_lo == sum(ledger.values())
    return {
        "cutoff": cutoff, "panels_per_band": panels, "retained_e1": rows,
        "finite_head_claim": claim, "tail_radius": q(tail),
        "raw_interval": [q(raw_lo), q(raw_hi)],
        "rational_interval": [q(display_lo), q(display_hi)],
        "width": q(display_hi-display_lo),
        "strictly_positive": display_lo > 0,
        "target_met": display_lo > 0 and display_hi-display_lo <= F(1, 100),
        "error_ledger_width_contributions": {key: q(value) for key, value in ledger.items()},
        "error_ledger_sum_checked": True,
        "total_panels": sum(row["panels"] for row in rows)
    }


def run_controls(coefficients, result, output):
    source_record = {"curve_a_invariants": [0,0,0,-25,0],
                     "coefficients": {str(n): a for n, a in coefficients.items() if n <= 20}}
    source_path = output/"evidence"/"controls"/"K03_original_coefficients.json"
    mutation_path = output/"evidence"/"controls"/"K03_mutated_a9.json"
    dump(source_path, source_record)
    changed_record = deepcopy(source_record)
    changed_record["coefficients"]["9"] = 0
    dump(mutation_path, changed_record)
    # Read the actual written representation through the recurrence check.
    loaded = json.loads(mutation_path.read_text(encoding="utf-8"))
    observed = loaded["coefficients"]["9"]
    computed = loaded["coefficients"]["3"]**2 - 3
    assert computed != observed
    k03 = {"id": "K03_EULER_RECURRENCE", "status": "CONFIRMED",
           "control_outcome": "FALSE_RECORD_REJECTED", "program_execution": "PASS",
           "actual_mutation": "coefficient record a9 changed to 0",
           "input_file": "evidence/controls/K03_mutated_a9.json",
           "observed_a9": observed, "a3": loaded["coefficients"]["3"],
           "required_a9_from_a3_squared_minus_3": computed,
           "mismatch": observed-computed}
    finite_claim = deepcopy(result["finite_head_claim"])
    original_path = output/"evidence"/"controls"/"K04_original_head_claim.json"
    mutation_path = output/"evidence"/"controls"/"K04_missing_all_term_premise.json"
    dump(original_path, finite_claim)
    del finite_claim["tail_premise"]["all_term_coefficient_bound"]
    dump(mutation_path, finite_claim)
    loaded = json.loads(mutation_path.read_text(encoding="utf-8"))
    outcome = promote_finite_head(loaded)
    assert outcome["status"] == "OPEN" and outcome["infinite_sum_interval"] is None
    k04 = {"id": "K04_NO_TAIL", "status": "CONFIRMED",
           "control_outcome": "INFINITE_CLAIM_OPEN_PROMOTION_REJECTED", "program_execution": "PASS",
           "actual_mutation": "deleted the all-term coefficient theorem from the same finite-head claim representation used by interval promotion",
           "input_file": "evidence/controls/K04_missing_all_term_premise.json",
           "before": promote_finite_head(result["finite_head_claim"]), "after": outcome,
           "meaning": "This rejects this finite-head promotion; it does not refute nonvanishing or invalidate an independently supplied proof."}
    return [k03, k04]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=EXPERIMENT)
    parser.add_argument("--budget", type=Path, default=HERE/"INTERVAL_BUDGET.json")
    args = parser.parse_args()
    start = time.monotonic()
    output = args.output_dir.resolve()
    budget_bytes = args.budget.read_bytes()
    budget = json.loads(budget_bytes)
    assert budget["coefficient_cutoffs_in_order"] == [40,80,160]
    assert budget["panels_per_doubling_band_in_order"] == [32,64,128]
    assert budget["dyadic_grid_bits"] == BITS
    assert budget["integration_upper_endpoint"] == "32"
    # No coefficients or E1 interval computation has been run before reading
    # this pre-existing declaration. Digest identifies bytes, not mathematics.
    run_meta = {"started_utc": datetime.now(timezone.utc).isoformat(),
                "budget_sha256": hashlib.sha256(budget_bytes).hexdigest(),
                "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "implementation": "work/analytic_check.py", "independence": "new standard-library implementation; no source-program imports, saved-result reads, arithmetic rank inputs or numerical target values"}
    coeff20, primes20 = euler_coefficients(20)
    alpha, const_data = constants()
    base = baseline(coeff20, const_data)
    print("Independent baseline reconstructed:", base["lower_bound"], flush=True)
    attempts = []
    selected = None
    coefficients, prime_data = None, None
    for cutoff in budget["coefficient_cutoffs_in_order"]:
        coefficients, prime_data = euler_coefficients(cutoff)
        for panels in budget["panels_per_doubling_band_in_order"]:
            print(f"Exact interval attempt M={cutoff}, K={panels}", flush=True)
            result = attempt(cutoff, panels, alpha, coefficients)
            attempts.append(result)
            print("Rational interval:", result["rational_interval"], "width:", result["width"], flush=True)
            if result["target_met"]:
                selected = result
                break
        if selected:
            break
    if selected is None:
        selected = min(attempts, key=lambda row: F(row["width"]))
    interval = {
        "task_id": "D01", "status": "CONFIRMED" if selected["target_met"] else "CONDITIONAL",
        "execution_outcome": "TARGET_MET" if selected["target_met"] else "BUDGET_EXHAUSTED_WITH_CERTIFIED_INTERVAL",
        "quantity": "c1=L'(E,1), E:y^2=x^3-25x over Q",
        "input_curve_a_invariants": [0,0,0,-25,0],
        "analytic_dependencies": "B01 checked conductor/sign/modularity/Mellin identity, plus Hasse and Euler-factor theorem as stated in INTERVAL_DERIVATION.md",
        "evidence_kind": "EXACT_RATIONAL_ENCLOSURE_WITH_WRITTEN_ERROR_PROOF_AND_CITED_THEOREMS",
        "inequality": "lower < c1 < upper", "lower": selected["rational_interval"][0],
        "upper": selected["rational_interval"][1], "width": selected["width"],
        "target_width": "1/100", "target_met": selected["target_met"],
        "selected_cutoff": selected["cutoff"], "selected_panels_per_band": selected["panels_per_band"],
        "constants": const_data, "error_ledger": selected["error_ledger_width_contributions"],
        "attempts": attempts, "budget": budget, "run": run_meta,
        "finite_coefficient_data": {"prime_data": prime_data,
            "all_coefficients": {str(n): value for n, value in coefficients.items()}},
        "not_used": ["arithmetic rank", "BSD predicted value", "archived PASS or result field", "ordinary floating E1", "external interval backend"]
    }
    controls = run_controls(coeff20, selected, output)
    receipt = {"run": run_meta, "B02": base, "D01": {
        "status": interval["status"], "interval_file": "DERIVATIVE_INTERVAL.json",
        "lower": interval["lower"], "upper": interval["upper"], "width": interval["width"],
        "cutoff": interval["selected_cutoff"], "panels_per_band": interval["selected_panels_per_band"]},
        "prime_data_through_20": primes20,
        "coefficients_through_20": {str(n): value for n, value in coeff20.items()},
        "controls": controls, "source_program_comparison": "root separately runs supplied programs; not part of this independent computation",
        "formal_proof_status": "NOT_RUN", "external_rigorous_backend": "NOT_RUN; standard-library exact enclosure completed",
        "elapsed_seconds_display_only": round(time.monotonic()-start, 3)}
    dump(output/"DERIVATIVE_INTERVAL.json", interval)
    dump(output/"evidence"/"analytic.json", receipt)
    print("B02, D01, K03 and K04 completed; exact evidence written.", flush=True)


if __name__ == "__main__":
    main()
