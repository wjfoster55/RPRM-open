"""Exact synthetic latent laws for the water composition kit.

Ported from rprm-water look-away-continuation-v1 signals.py at content commit
90bf41040076af2b448ff5f52c512bbcbb0f2e26. Original software terms: treat as
0BSD-compatible original contribution in the public kit; see kit README.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F

TOL = F(1, 20)
CATALOGUE_VERSION = "complementary-clocks-v2-laws"
CONTRACT_VERSION = "look-away-continuation-v1-tol-1/20"
HORIZON_SCOPE = (F(0), F(12))
THRESH_PRIMARY = F(23, 2)  # 11.5
THRESH_AUX = F(11)


def triangle_unit(t: F, period: F, phase: F = F(0)) -> F:
    u = ((t + phase) / period) % 1
    if u <= F(1, 4):
        return 4 * u
    if u <= F(3, 4):
        return 2 - 4 * u
    return 4 * u - 4


def signal_value(kind: str, t: F) -> F:
    if kind == "const10":
        return F(10)
    if kind == "ramp":
        return F(10) + t / F(12)
    if kind.startswith("triangle_p4_phi"):
        if kind == "triangle_p4_phi_1_8":
            phase = F(1, 8)
        else:
            k = int(kind.replace("triangle_p4_phi", ""))
            phase = F(k, 2)
        return F(10) + triangle_unit(t, F(4), phase)
    if kind.startswith("step_at_"):
        rest = kind[len("step_at_") :]
        event = F(11, 2) if rest == "11_2" else F(int(rest))
        return F(10) if t < event else F(12)
    raise KeyError(kind)


def catalogue_ids() -> list[str]:
    ids = ["const10", "ramp"]
    ids += [f"triangle_p4_phi{k}" for k in range(8)]
    ids += [f"step_at_{e}" for e in (3, 4, 5, 6, 7, 8, 9)]
    ids += ["triangle_p4_phi_1_8", "step_at_11_2"]
    return ids


def step_event(kind: str) -> F | None:
    if not kind.startswith("step_at_"):
        return None
    rest = kind[len("step_at_") :]
    return F(11, 2) if rest == "11_2" else F(int(rest))


def triangle_phase(kind: str) -> F | None:
    if not kind.startswith("triangle_p4_phi"):
        return None
    if kind == "triangle_p4_phi_1_8":
        return F(1, 8)
    return F(int(kind.replace("triangle_p4_phi", "")), 2)


@dataclass(frozen=True)
class Bounds:
    lower: F
    upper: F
    lower_attained: bool
    upper_attained: bool

    def reaches(self, threshold: F) -> bool:
        return self.upper > threshold or (self.upper == threshold and self.upper_attained)


def require_horizon_in_scope(t0: F, t1: F) -> None:
    if t1 <= t0:
        raise ValueError(f"empty or inverted interval ({t0}, {t1}]")
    lo, hi = HORIZON_SCOPE
    if t0 < lo or t1 > hi:
        raise ValueError(f"horizon ({t0}, {t1}] outside supported fixture scope [{lo}, {hi}]")


def interval_bounds(kind: str, t0: F, t1: F) -> Bounds:
    require_horizon_in_scope(t0, t1)
    if kind == "const10":
        return Bounds(F(10), F(10), True, True)
    if kind == "ramp":
        return Bounds(signal_value(kind, t0), signal_value(kind, t1), False, True)
    if kind.startswith("step_at_"):
        event = step_event(kind)
        assert event is not None
        if event <= t0:
            return Bounds(F(12), F(12), True, True)
        if event > t1:
            return Bounds(F(10), F(10), True, True)
        return Bounds(F(10), F(12), True, True)
    phase = triangle_phase(kind)
    assert phase is not None
    candidates: list[tuple[F, bool]] = [
        (signal_value(kind, t0), False),
        (signal_value(kind, t1), True),
    ]
    n0 = int((t0 + phase) // 4) - 2
    n1 = int((t1 + phase) // 4) + 3
    for n in range(n0, n1 + 1):
        for r in (1, 3):
            t = F(4 * n + r) - phase
            if t0 < t <= t1:
                candidates.append((signal_value(kind, t), True))
    lo = min(value for value, _ in candidates)
    hi = max(value for value, _ in candidates)
    return Bounds(
        lo,
        hi,
        any(value == lo and attained for value, attained in candidates),
        any(value == hi and attained for value, attained in candidates),
    )


def endpoint_only_bounds(kind: str, t0: F, t1: F) -> Bounds:
    """Hostile control: endpoints only — can miss interior extrema."""
    require_horizon_in_scope(t0, t1)
    v0 = signal_value(kind, t0)
    v1 = signal_value(kind, t1)
    lo, hi = min(v0, v1), max(v0, v1)
    return Bounds(lo, hi, True, True)
