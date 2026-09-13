"""Exact universal omitted-coefficient bound from ANALYTIC_BRIDGE.md (6).

The caller must certify alpha=2*pi/sqrt(N) >= alpha_lower and the correct
elliptic-curve Euler coefficients. This utility does not certify those inputs,
compute a finite integral head, or infer an analytic rank.
"""
import argparse
from fractions import Fraction
import json


def tail_bound(alpha_lower, coefficient, cutoff):
    if (not isinstance(alpha_lower, (int, Fraction)) or
            not isinstance(coefficient, int) or not isinstance(cutoff, int)):
        raise ValueError("exact rational alpha and integer order/cutoff required")
    alpha_lower = Fraction(alpha_lower)
    if alpha_lower <= 0 or coefficient < 0 or cutoff < 0:
        raise ValueError("positive alpha bound and nonnegative integer order/cutoff required")
    q = 1 / (1 + alpha_lower)
    bound = 4 * q ** (cutoff + 1) / (
        alpha_lower ** (coefficient + 1) * (cutoff + 1) ** coefficient * (1 - q)
    )
    return q, bound


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alpha-lower", type=Fraction, required=True)
    parser.add_argument("--coefficient", type=int, required=True)
    parser.add_argument("--cutoff", type=int, required=True)
    args = parser.parse_args()
    q, bound = tail_bound(args.alpha_lower, args.coefficient, args.cutoff)
    print(json.dumps({
        "status": "CONDITIONAL_EXACT_TAIL_BOUND",
        "alpha_lower": str(args.alpha_lower), "q_upper": str(q),
        "completed_Taylor_order": args.coefficient, "cutoff": args.cutoff,
        "tail_bound": str(bound),
        "requires": ["proved alpha >= alpha_lower", "correct elliptic L-function",
                     "all-n coefficient bound |a_n| <= 2n"],
        "finite_head": "NOT_COMPUTED", "analytic_rank": "NOT_INFERRED"
    }, indent=2))


if __name__ == "__main__":
    main()
