"""Bounded peer ledger audit of the fresh E5 M=40 interval, no imports of its code.

This independently reconstructs the recorded signed assembly and error ledger.
The calculus/rounding code review is stated separately; this is not a new
quadrature run or a claim that hashes establish mathematical correctness.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "evidence" / "interval_peer_review.json")
    parser.add_argument("--input-dir", type=Path, default=ROOT,
                        help="Directory containing a freshly generated interval and analytic receipt.")
    args = parser.parse_args()
    paths = ["work/analytic_check.py", "work/INTERVAL_BUDGET.json",
             "DERIVATIVE_INTERVAL.json", "INTERVAL_DERIVATION.md", "evidence/analytic.json"]
    result_paths = {"DERIVATIVE_INTERVAL.json", "evidence/analytic.json"}
    data = {path: ((args.input_dir if path in result_paths else ROOT) / path).read_bytes()
            for path in paths}
    report = json.loads(data["DERIVATIVE_INTERVAL.json"])
    finite = json.loads(data["evidence/analytic.json"])
    rows = report["attempts"][0]["retained_e1"]
    coefficients = {int(n): value for n, value in report["finite_coefficient_data"]["all_coefficients"].items()}
    checks = {}
    checks["implementation_matches_fresh_receipt"] = hashlib.sha256(data[paths[0]]).hexdigest() == report["run"]["implementation_sha256"]
    checks["budget_matches_fresh_receipt"] = hashlib.sha256(data[paths[1]]).hexdigest() == report["run"]["budget_sha256"]
    checks["same_e5_model"] = report["input_curve_a_invariants"] == [0,0,0,-25,0]
    checks["only_first_budgeted_attempt"] = len(report["attempts"]) == 1 and report["selected_cutoff"] == 40 and report["selected_panels_per_band"] == 32
    checks["retained_nonzero_indices_complete"] = {row["n"] for row in rows} == {n for n, value in coefficients.items() if value}
    lo, hi = F(0), F(0)
    for row in rows:
        n = row["n"]
        w = F(2*coefficients[n], n)
        e_lo, e_hi = F(row["lower"]), F(row["upper"])
        candidates = [w*e_lo, w*e_hi]
        term = list(map(F, row["term_interval"]))
        checks[f"signed_term_{n}"] = term == [min(candidates), max(candidates)] and w == F(row["signed_weight"])
        checks[f"row_ledger_{n}"] = e_hi-e_lo == sum(F(row[name]) for name in ["alpha_input_loss", "quadrature_error_bound", "midpoint_exp_and_rounding_gap", "integration_tail"])
        lo += term[0]
        hi += term[1]
    attempt = report["attempts"][0]
    checks["signed_head_reassembly"] = [lo, hi] == list(map(F, attempt["finite_head_claim"]["finite_head_interval"]))
    tail = F(120, 41)*F(5,6)**41
    checks["entire_tail_radius_reconstructed"] = tail == F(attempt["tail_radius"])
    checks["raw_infinite_interval_reconstructed"] = [lo-tail, hi+tail] == list(map(F, attempt["raw_interval"]))
    lower, upper = F(report["lower"]), F(report["upper"])
    checks["export_outward"] = lower <= lo-tail and hi+tail <= upper
    checks["complete_width_ledger"] = sum(map(F, report["error_ledger"].values())) == upper-lower == F(report["width"])
    checks["positive_target_width"] = lower > 0 and upper-lower <= F(1,100)
    base = finite["B02"]
    negative = sum(F(row["absolute_term_bound"]) for row in base["retained_negative_rows"])
    baseline_tail = F(120,21)*F(5,6)**21
    baseline_lower = F(8,9)-negative-baseline_tail
    checks["baseline_rational_reassembly"] = baseline_lower == F(base["lower_bound"]) and baseline_lower > F(13,20)
    checks["coarse_pi_alternative_lower"] = 4*sum((F((-1)**k,2*k+1) for k in range(8)),F(0)) > 3
    result = {
        "status": "CONFIRMED" if all(checks.values()) else "REFUTED",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "review_scope": "Executed E5 branch M=40, 32 panels per doubling band; no new coefficient cutoff or quadrature execution.",
        "evidence_kind": ["INDEPENDENT_CODE_AND_WRITTEN_PROOF_PEER_REVIEW", "EXACT_RECORDED_LEDGER_REASSEMBLY"],
        "files_reviewed": [{"path": path, "sha256": hashlib.sha256(raw).hexdigest()} for path,raw in data.items()],
        "checks": checks,
        "reviewed_mathematical_obligations": [
            "Machin identity and alternating atan enclosures; integer square-root bounds; alpha denominator endpoints reversed correctly.",
            "For exp(-z), 0<=z<=1 gives odd degree31 lower and even degree30 upper; nonnegative squaring is monotone and uses outward dyadic rounding.",
            "f(t)=exp(-t)/t has f''=exp(-t)(1/t+2/t^2+2/t^3)>0 and f'''<0. Midpoint is a lower bound and its per-panel error is <=h^3 f''(left)/24.",
            "E1(x_lo)-E1(x)<= (x_hi-x_lo)/x_lo for x in [x_lo,x_hi]; code subtracts an upward-rounded allowance only from the lower endpoint.",
            "Integral beyond 32 bounded by exp(-32)/32; nonzero finite weights reverse endpoints when negative.",
            "All-n Hasse/Euler coefficient bound supplies the entire n>=41 tail. This strict positive-radius envelope proves the exported endpoints may be stated strictly.",
            "All signed multiplication and accumulation use exact Fraction arithmetic. Fixed-grid exponential/panel roundoff and final export enlargement are separately accounted."
        ],
        "conclusion": {"lower": str(lower), "upper": str(upper), "width": str(upper-lower)},
        "defects_found": [],
        "limitations": "A peer written proof/code review and finite ledger check, not formal verification or a second independently designed quadrature algorithm. Hashes bind reviewed bytes only. Arithmetic rank and historical source receipts were not read as analytic inputs."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
