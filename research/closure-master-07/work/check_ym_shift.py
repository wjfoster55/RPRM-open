"""Exact, bounded gate for a proportional spectral shift.

This standard-library program checks scalar arithmetic from the closure-07
YM audit. It does not construct a Yang-Mills vacuum, run a lattice campaign,
or certify any continuum estimate. It imports no research-lane code.

For v = F(v), preserving the original equation after replacing T by
(1 + alpha) T requires G(v) = (F(v) + alpha v) / (1 + alpha).
The positive ball and Lipschitz majorants therefore transform as
M_alpha = (M + alpha Z)/(1 + alpha),
L_alpha = (L + alpha)/(1 + alpha).
Their two margins divide by (1 + alpha), preserving their signs.

Run from any directory, with Python 3.10 or newer:
  python -I -B check_ym_shift.py --output /path/to/new_receipt.json
Without --output, the complete receipt is printed to stdout.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform


def run_checks() -> dict:
    checked: list[str] = []

    def require(condition: bool, label: str) -> None:
        if not condition:
            raise AssertionError(label)
        checked.append(label)

    # Independent exact expected endpoint values from the audit.
    cases = (
        (F(1, 3), F(7, 20), F(1, 2400), F(101, 180)),
        (F(7, 20), F(5, 12), F(13, 6912), F(109, 180)),
        (F(2, 5), F(3, 5), F(-3, 100), F(11, 15)),
    )
    alphas = (F(1, 2), F(1), F(3))
    majorant_rows = []
    for index, (x, radius, expected_margin, expected_lipschitz) in enumerate(cases):
        majorant = F(25, 16) * x * x + F(4, 3) * x * radius + radius * radius / 6
        lipschitz = (4 * x + radius) / 3
        margin = radius - majorant
        gap = 1 - lipschitz
        require(margin == expected_margin, f"case_{index}: original_ball_margin")
        require(lipschitz == expected_lipschitz, f"case_{index}: original_lipschitz")
        shifted_rows = []
        for alpha in alphas:
            prefix = f"case_{index}/alpha_{alpha}"
            shifted_majorant = (majorant + alpha * radius) / (1 + alpha)
            shifted_lipschitz = (lipschitz + alpha) / (1 + alpha)
            shifted_margin = radius - shifted_majorant
            shifted_gap = 1 - shifted_lipschitz
            require(shifted_margin == margin / (1 + alpha), f"{prefix}: ball_margin_identity")
            require(shifted_gap == gap / (1 + alpha), f"{prefix}: lipschitz_gap_identity")
            require((shifted_margin > 0) == (margin > 0), f"{prefix}: strict_ball_sign")
            require((shifted_margin < 0) == (margin < 0), f"{prefix}: failed_ball_sign")
            require((shifted_gap > 0) == (gap > 0), f"{prefix}: contraction_gap_sign")
            shifted_rows.append(
                {
                    "alpha": str(alpha),
                    "M_alpha": str(shifted_majorant),
                    "L_alpha": str(shifted_lipschitz),
                    "ball_margin": str(shifted_margin),
                    "lipschitz_gap": str(shifted_gap),
                    "strict_ball_passes": shifted_margin > 0,
                    "strict_lipschitz_passes": shifted_gap > 0,
                }
            )
        majorant_rows.append(
            {
                "x": str(x),
                "Z": str(radius),
                "M": str(majorant),
                "L": str(lipschitz),
                "ball_margin": str(margin),
                "lipschitz_gap": str(gap),
                "strict_ball_passes": margin > 0,
                "strict_lipschitz_passes": gap > 0,
                "shifts": shifted_rows,
            }
        )

    # On the actual two-channel kinetic energies, the isolated inverse
    # decreases, while reinserting the transported residual restores v.
    inverse_rows = []
    for energy in (F(9), F(13)):
        source = F(1)
        solution = source / energy
        alpha = F(1)
        isolated = source / ((1 + alpha) * energy)
        residual = alpha * energy * solution
        restored = (source + residual) / ((1 + alpha) * energy)
        require(isolated == solution / 2, f"energy_{energy}: isolated_half")
        require(restored == solution, f"energy_{energy}: exact_residual_transport")
        require(isolated != solution, f"energy_{energy}: dropping_residual_changes_equation")
        inverse_rows.append(
            {
                "lambda": str(energy),
                "alpha": str(alpha),
                "source": str(source),
                "original_solution": str(solution),
                "isolated_shifted_inverse": str(isolated),
                "retained_residual": str(residual),
                "restored_solution": str(restored),
            }
        )

    # Selected members of the already derived one-square high-spin family.
    # These finite checks do not establish its unrestricted asymptotic law.
    spin_rows = []
    for spin in (F(1), F(3, 2), F(10), F(100)):
        energies = (8 * spin * spin - 2, 8 * spin * spin + 16 * spin + 6)
        factors = []
        for channel, energy in zip(("minus", "plus"), energies):
            require(energy > 0, f"spin_{spin}/{channel}: positive_energy")
            factor = energy / (energy + energy)
            require(factor == F(1, 2), f"spin_{spin}/{channel}: proportional_shift_factor")
            factors.append(str(factor))
        spin_rows.append(
            {
                "j": str(spin),
                "lambda_minus": str(energies[0]),
                "lambda_plus": str(energies[1]),
                "alpha": "1",
                "isolated_inverse_factors": factors,
            }
        )

    # A generic positive scalar obstruction, not an asserted YM eigenmode.
    scalar_multiplier = F(3, 2)
    alpha = F(1)
    transported_multiplier = (scalar_multiplier + alpha) / (1 + alpha)
    require(transported_multiplier == F(5, 4), "positive_scalar: exact_multiplier")
    require(transported_multiplier > 1, "positive_scalar: remains_noncontracting")

    return {
        "schema": "closure-master-07-ym-proportional-shift-v1",
        "status": "PASS",
        "scope": {
            "evidence_grade": "bounded exact rational arithmetic checks",
            "majorant_cases": "three stated x,Z pairs, each at alpha=1/2,1,3",
            "local_inverse_cases": "energies 9 and 13 with source 1 and alpha=1",
            "high_spin_samples": "j=1,3/2,10,100; two stated output-energy formulas",
            "hostile_control": "negative ball margin retained; generic positive scalar multiplier 3/2",
            "exclusions": [
                "No old YM or BSD checker was executed.",
                "No complete nonlinear vacuum or lattice campaign was computed.",
                "No universal operator-norm or continuum mass-gap proof is supplied.",
                "No rejection of all nonuniform or structured relative-scale estimates is claimed.",
            ],
        },
        "majorant_cases": majorant_rows,
        "local_inverse_transport": inverse_rows,
        "high_spin_samples": spin_rows,
        "positive_scalar_hostile_control": {
            "original_multiplier": str(scalar_multiplier),
            "alpha": str(alpha),
            "transported_multiplier": str(transported_multiplier),
            "strict_contraction": False,
            "carrier": "generic one-dimensional linear fixed-point map, not a claimed YM eigenmode",
        },
        "check_count": len(checked),
        "checks": checked,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write the fresh receipt to this JSON path.")
    args = parser.parse_args()
    receipt = run_checks()
    receipt["execution"] = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    serialized = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(serialized, end="")
    else:
        args.output.write_text(serialized, encoding="utf-8", newline="\n")
        print(json.dumps({"status": receipt["status"], "check_count": receipt["check_count"], "output": str(args.output.resolve())}))


if __name__ == "__main__":
    main()
