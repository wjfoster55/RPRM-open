"""Rigorous E34 period/regulator comparison; does NOT identify the order of Sha.

Elementary AGM enclosure structure is adapted openly from the earlier E5
work/bsd_factors.py, with sqrt(68) and the rank-two Gram determinant here.
Inputs are the fresh interval and generator receipts, whose source bytes
are bound. Their written proofs remain necessary mathematical dependencies.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCALE = 1 << 100


def down(x, scale=SCALE):
    x = F(x)
    return F(x.numerator * scale // x.denominator, scale)


def up(x, scale=SCALE):
    return -down(-x, scale)


def outward(interval, places=9):
    return [str(down(interval[0], 10 ** places)), str(up(interval[1], 10 ** places))]


def square_root(x):
    x = F(x)
    if x < 0:
        raise ValueError("nonnegative radicand required")
    m = isqrt(x.numerator * SCALE * SCALE // x.denominator)
    result = F(m, SCALE), F(m + 1, SCALE)
    assert result[0] ** 2 <= x < result[1] ** 2
    return result


def atan(reciprocal, terms):
    first = sum((F((-1) ** k, (2 * k + 1) * reciprocal ** (2 * k + 1))
                 for k in range(terms)), F(0))
    other = first + F((-1) ** terms, (2 * terms + 1) * reciprocal ** (2 * terms + 1))
    return min(first, other), max(first, other)


def period():
    x, y = atan(5, 64), atan(239, 20)
    pi = down(16 * x[0] - 4 * y[1]), up(16 * x[1] - 4 * y[0])
    sqrt2, sqrt68 = square_root(2), square_root(68)
    a = F(1), F(1)
    g = down(1 / sqrt2[1]), up(1 / sqrt2[0])
    steps = []
    for j in range(8):
        steps.append({"j": j, "arithmetic": list(map(str, a)), "geometric": list(map(str, g))})
        if j != 7:
            a, g = ((down((a[0] + g[0]) / 2), up((a[1] + g[1]) / 2)),
                    (square_root(a[0] * g[0])[0], square_root(a[1] * g[1])[1]))
    agm = g[0], a[1]
    omega = down(2 * pi[0] / (sqrt68[1] * agm[1])), up(2 * pi[1] / (sqrt68[0] * agm[0]))
    assert omega[1] - omega[0] < F(1, 10 ** 25)
    return omega, {"formula": "2*pi/(sqrt(68)*AGM(1,1/sqrt(2)))",
                   "minimal_differential": "dx/(2y)", "real_components": 2,
                   "pi": list(map(str, pi)), "sqrt2": list(map(str, sqrt2)),
                   "sqrt68": list(map(str, sqrt68)), "agm_steps": steps,
                   "omega": list(map(str, omega)), "omega_outward": outward(omega, 12)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--input-dir", type=Path, default=ROOT / "evidence")
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("Choose a fresh output path")
    generator_path = args.input_dir / "generator.json"
    interval_path = args.input_dir / "interval.json"
    generator = json.loads(generator_path.read_text())
    interval = json.loads(interval_path.read_text())
    assert generator["source_sha256"] == sha256((ROOT / "work/generator.py").read_bytes()).hexdigest()
    assert interval["source_sha256"] == sha256((ROOT / "work/interval.py").read_bytes()).hexdigest()
    assert generator["conclusion"]["free_index"] == 1
    assert interval["model"] == [0, 0, 0, -1156, 0]
    p = list(map(F, generator["gram"]["diagonal_P"]))
    q = list(map(F, generator["gram"]["diagonal_Q"]))
    b = list(map(F, generator["gram"]["off_diagonal_B"]))
    square_lo = F(0) if b[0] <= 0 <= b[1] else min(b[0] ** 2, b[1] ** 2)
    square_hi = max(b[0] ** 2, b[1] ** 2)
    reg = down(p[0] * q[0] - square_hi), up(p[1] * q[1] - square_lo)
    assert reg[0] > 0
    omega, period_receipt = period()
    # Local Tate proof: c2=c17=4; actual torsion has order4. Factors cancel.
    product_cp, torsion_order = 16, 4
    rhs = down(omega[0] * reg[0]), up(omega[1] * reg[1])
    c2 = tuple(map(F, interval["alpha_times_lambda2_interval"]))
    ratio = down(c2[0] / rhs[1]), up(c2[1] / rhs[0])
    # No assertion that this ratio is integral, or that it equals #Sha.
    contains_one = ratio[0] <= 1 <= ratio[1]
    controls = {}
    for name, multiplier in (("one_real_component", 2),
                             ("half_height_pairing_in_rank2", 4),
                             ("index3_subgroup_as_basis", F(1, 9))):
        wrong = ratio[0] * multiplier, ratio[1] * multiplier
        controls[name] = {"comparison_interval": outward(wrong),
                          "contains_one": wrong[0] <= 1 <= wrong[1],
                          "scope": "normalization sensitivity only"}
    result = {"status": "RIGOROUS_FACTOR_COMPARISON_ONLY", "model": interval["model"],
              "period": period_receipt, "regulator": list(map(str, reg)),
              "regulator_outward": outward(reg), "local_product": product_cp,
              "torsion_order": torsion_order, "rhs_without_sha": list(map(str, rhs)),
              "rhs_without_sha_outward": outward(rhs), "c2": list(map(str, c2)),
              "bsd_quotient": list(map(str, ratio)), "bsd_quotient_outward": outward(ratio),
              "contains_one": contains_one, "sha_order": "NOT_ESTABLISHED",
              "full_BSD_identity": "NOT_ESTABLISHED",
              "conditional_consequence": "IF the full BSD identity holds, the quotient isolates #Sha=1",
              "normalization_controls": controls,
              "dependencies": {"generator_receipt_sha256": sha256(generator_path.read_bytes()).hexdigest(),
                               "interval_receipt_sha256": sha256(interval_path.read_bytes()).hexdigest(),
                               "written_local_proof": "LOCAL_ANALYTIC_INPUTS.md"},
              "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "period": period_receipt["omega_outward"],
                      "regulator": result["regulator_outward"],
                      "quotient": result["bsd_quotient_outward"],
                      "sha_order": "NOT_ESTABLISHED"}, indent=2))


if __name__ == "__main__":
    main()
