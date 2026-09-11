"""Compact circuit observers for the process-mechanics circuits kit.

RC paths use the standard library only. RLC affine reconstruction uses
NumPy+SciPy when available; otherwise the RLC section is SKIP/NOT_RUN.

Interface scope (I1):
- ``rc_exact_event`` integrates the piecewise-constant drive correctly when the
  hold/release switch falls inside a sample step (split at the switch).
- ``rc_exact_event_end_of_step`` preserves the historical end-of-step drive
  sampling used in prior experiment ports. Do not treat its mid-step-switch
  outputs as faithful continuous-drive events.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RCParams:
    R: float
    C: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "R", _positive_finite("R", self.R))
        object.__setattr__(self, "C", _positive_finite("C", self.C))

    @property
    def tau(self) -> float:
        return self.R * self.C


@dataclass(frozen=True)
class RLCParams:
    R: float
    L: float
    C: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "R", _finite("R", self.R))
        object.__setattr__(self, "L", _positive_finite("L", self.L))
        object.__setattr__(self, "C", _positive_finite("C", self.C))

    @property
    def omega0(self) -> float:
        return 1.0 / math.sqrt(self.L * self.C)

    @property
    def zeta(self) -> float:
        return self.R / 2.0 * math.sqrt(self.C / self.L)


def _finite(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _positive_finite(name: str, value: float) -> float:
    number = _finite(name, value)
    if number <= 0.0:
        raise ValueError(f"{name} must be positive")
    return number


def rc_step(v: float, u: float, dt: float, params: RCParams) -> float:
    v = _finite("v", v)
    u = _finite("u", u)
    dt = _finite("dt", dt)
    if dt < 0.0:
        raise ValueError("dt must be nonnegative")
    if dt == 0.0:
        return v
    alpha = math.exp(-dt / params.tau)
    return u + (v - u) * alpha


def u_at_time(t: float, hold_dur: float, u_hold: float, u_release: float) -> float:
    return u_hold if t <= hold_dur + 1e-15 else u_release


def _tie_event(v: float, v_th: float) -> int:
    """Sampled threshold event: v <= v_th counts as the event (ties included)."""
    return 1 if v <= v_th else 0


def rc_exact_event_end_of_step(
    v0: float,
    t0: float,
    horizon_steps: int,
    dt: float,
    hold_dur: float,
    u_hold: float,
    u_release: float,
    v_th: float,
    params: RCParams,
) -> int:
    """Historical grid port: apply end-of-step drive over the whole step.

    This matches prior experiment sample-grid semantics. Mid-step switches are
    not continuous-drive exact; use ``rc_exact_event`` for that contract.
    """
    if type(horizon_steps) is not int or horizon_steps < 1:
        raise ValueError("horizon_steps must be a positive int")
    v = _finite("v0", v0)
    t0 = _finite("t0", t0)
    dt = _positive_finite("dt", dt)
    hold_dur = _finite("hold_dur", hold_dur)
    u_hold = _finite("u_hold", u_hold)
    u_release = _finite("u_release", u_release)
    v_th = _finite("v_th", v_th)
    for step in range(1, horizon_steps + 1):
        t_abs = t0 + step * dt
        u = u_at_time(t_abs, hold_dur, u_hold, u_release)
        v = rc_step(v, u, dt, params)
        if _tie_event(v, v_th):
            return 1
    return 0


def rc_exact_event(
    v0: float,
    t0: float,
    horizon_steps: int,
    dt: float,
    hold_dur: float,
    u_hold: float,
    u_release: float,
    v_th: float,
    params: RCParams,
) -> int:
    """Return 1 if voltage reaches <= threshold within the horizon under the known plan.

    Piecewise-constant drive: when the hold/release switch falls inside a sample
    step, propagation is split at the switch so each subinterval uses the drive
    that applies on that subinterval. Sampled event uses endpoint comparison
    ``v <= v_th`` (ties count as the event).
    """
    if type(horizon_steps) is not int or horizon_steps < 1:
        raise ValueError("horizon_steps must be a positive int")
    v = _finite("v0", v0)
    t0 = _finite("t0", t0)
    dt = _positive_finite("dt", dt)
    hold_dur = _finite("hold_dur", hold_dur)
    u_hold = _finite("u_hold", u_hold)
    u_release = _finite("u_release", u_release)
    v_th = _finite("v_th", v_th)
    for step in range(1, horizon_steps + 1):
        t_start = t0 + (step - 1) * dt
        t_end = t0 + step * dt
        # Split when the switch falls strictly inside the step.
        if (t_start + 1e-15) < hold_dur < (t_end - 1e-15):
            dt1 = hold_dur - t_start
            dt2 = t_end - hold_dur
            v = rc_step(v, u_hold, dt1, params)
            v = rc_step(v, u_release, dt2, params)
        else:
            mid = 0.5 * (t_start + t_end)
            u = u_at_time(mid, hold_dur, u_hold, u_release)
            v = rc_step(v, u, dt, params)
        if _tie_event(v, v_th):
            return 1
    return 0


def rc_trajectory(
    v0: float,
    segments: list[tuple[float, float]],
    dt: float,
    params: RCParams,
) -> tuple[list[float], list[float]]:
    times = [0.0]
    vals = [_finite("v0", v0)]
    t = 0.0
    v = vals[0]
    for dur, u in segments:
        n = int(round(_finite("dur", dur) / _finite("dt", dt)))
        for _ in range(n):
            v = rc_step(v, _finite("u", u), dt, params)
            t += dt
            times.append(t)
            vals.append(v)
    return times, vals


def numpy_available() -> bool:
    try:
        import numpy  # noqa: F401
        import scipy.linalg  # noqa: F401
        return True
    except Exception:
        return False


def rlc_reconstruct_i(
    v_prev: float,
    v_now: float,
    u: float,
    lag_dt: float,
    params: RLCParams,
) -> dict[str, Any]:
    """Recover current from two timed voltages under constant drive.

    Rejects a singular observation map instead of inventing a current.
    """
    if not numpy_available():
        return {"status": "SKIP_OPTIONAL_DEPENDENCY", "reason": "numpy/scipy unavailable"}
    import numpy as np
    from scipy.linalg import expm

    v_prev = _finite("v_prev", v_prev)
    v_now = _finite("v_now", v_now)
    u = _finite("u", u)
    lag_dt = _finite("lag_dt", lag_dt)
    A = np.array([[0.0, 1.0 / params.C], [-1.0 / params.L, -params.R / params.L]], dtype=float)
    B = np.array([0.0, 1.0 / params.L], dtype=float)
    F = expm(A * lag_dt)
    g = np.linalg.solve(A, F - np.eye(2)) @ B
    f01 = float(F[0, 1])
    meta = {"F01": f01, "conditioning_ok": abs(f01) > 1e-12}
    if abs(f01) <= 1e-12:
        return {**meta, "status": "SINGULAR_OBSERVATION_MAP", "i_prev": None, "i_now": None}
    i_prev = (v_now - float(F[0, 0]) * v_prev - float(g[0]) * u) / f01
    x_prev = np.array([v_prev, i_prev])
    x_now = F @ x_prev + g * u
    return {
        **meta,
        "status": "ok",
        "i_prev": float(i_prev),
        "i_now": float(x_now[1]),
    }


def rlc_trajectory_optional(
    x0: tuple[float, float],
    segments: list[tuple[float, float]],
    dt: float,
    params: RLCParams,
) -> dict[str, Any]:
    if not numpy_available():
        return {"status": "SKIP_OPTIONAL_DEPENDENCY", "reason": "numpy/scipy unavailable"}
    import numpy as np
    from scipy.linalg import expm

    A = np.array([[0.0, 1.0 / params.C], [-1.0 / params.L, -params.R / params.L]], dtype=float)
    B = np.array([0.0, 1.0 / params.L], dtype=float)
    Ad = expm(A * dt)
    ZB = np.linalg.solve(A, Ad - np.eye(2)) @ B
    x = np.array([_finite("v", x0[0]), _finite("i", x0[1])], dtype=float)
    times = [0.0]
    volts = [float(x[0])]
    currents = [float(x[1])]
    t = 0.0
    for dur, u in segments:
        n = int(round(_finite("dur", dur) / _finite("dt", dt)))
        for _ in range(n):
            x = Ad @ x + ZB * _finite("u", u)
            t += dt
            times.append(t)
            volts.append(float(x[0]))
            currents.append(float(x[1]))
    return {"status": "ok", "times": times, "v": volts, "i": currents}
