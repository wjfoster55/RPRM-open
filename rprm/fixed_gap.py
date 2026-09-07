"""Exact fixed-gap Fermat fibers (0BSD; Python standard library only).

Supply exact Python integers n >= 2 and s,d > 0; the missing port is the
positive integer a in a**n + (a+s)**n = (a+s+d)**n. MANIFESTO III.2.3 proves
that the complete fiber is NONE or ONE, inside the derived bracket
[0, 2*n*(s+d)]. Zero is a sign sentinel, not an admitted source value.

This per-aperture decision has no arbitrary height cutoff. It does not
assert that every gap pair is empty or prove unrestricted FLT. Arbitrary
precision arithmetic still consumes finite time and memory; exceptions or
interruption are unfinished computation, never an empty-fiber result.
"""

from __future__ import annotations

from .core import AdmissionError


def _residual(a: int, n: int, s: int, d: int) -> int:
    return a**n + (a + s)**n - (a + s + d)**n


def decide_fixed_gap(n: int, s: int, d: int) -> dict:
    """Return a complete integer fiber with an exact bisection receipt.

    ``fiber`` lists the possible a values; ``source`` reconstructs
    (a, a+s, a+s+d, n) for ONE and is None for NONE. ``trace`` records the
    bracket before each midpoint evaluation. The final endpoints are
    adjacent with D(L) < 0 <= D(U), even when a midpoint is an exact zero.

    Types are admitted without coercion: bool, floats, fractions and int
    subclasses are rejected. Mathematical bounds are derived from inputs;
    there is no resource budget that could be confused with completeness.
    """
    for name, value, minimum in (("n", n, 2), ("s", s, 1), ("d", d, 1)):
        if type(value) is not int or value < minimum:
            raise AdmissionError(f"{name} must be an exact int >= {minimum}")

    bound = 2 * n * (s + d)
    lower, upper = 0, bound
    lower_residual = _residual(lower, n, s, d)
    upper_residual = _residual(upper, n, s, d)
    if not lower_residual < 0 < upper_residual:
        raise RuntimeError("Derived endpoint signs failed")
    initial = {"lower": lower, "upper": upper,
               "lower_residual": lower_residual, "upper_residual": upper_residual}
    trace = []
    while upper - lower > 1:
        midpoint = (lower + upper) // 2
        value = _residual(midpoint, n, s, d)
        trace.append({"lower": lower, "upper": upper,
                      "midpoint": midpoint, "residual": value})
        if value < 0:
            lower, lower_residual = midpoint, value
        else:
            upper, upper_residual = midpoint, value

    # D itself need not increase. For a>0, D(a)/a**n strictly increases:
    # 1 - sum(comb(n,k)*((s+d)**k-s**k)/a**k, k=1..n).
    # Hence the signs exclude both positive integer tails outside the final
    # adjacent bracket, or establish uniqueness of the exact upper zero.
    one = upper_residual == 0
    return {
        "schema": "rprm-fixed-gap-fiber/v1",
        "status": "ONE" if one else "NONE",
        "parameters": {"n": n, "s": s, "d": d},
        "missing_port": "positive integer a",
        "fiber": (upper,) if one else (),
        "source": (upper, upper + s, upper + s + d, n) if one else None,
        "derived_bound": bound,
        "initial_bracket": initial,
        "final_bracket": {"lower": lower, "upper": upper,
                          "lower_residual": lower_residual, "upper_residual": upper_residual},
        "trace": tuple(trace),
        "bisection_rounds": len(trace),
        "residual_evaluations": 2 + len(trace),
        "scope": "Complete positive-integer a fiber for these supplied n,s,d only; "
                 "coverage uses the written normalized-monotonicity and endpoint proof in MANIFESTO III.2.3.",
    }
