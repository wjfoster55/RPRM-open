#!/usr/bin/env python3
"""Regression suite for the ORACLE spill/retention contract (truth_solver).

Reconstructs the PR#9 review's `fluid_pr9_spill_regression` probe (which was NOT
shipped) plus additional spill geometries. Each case has an analytically-known
quasistatic zero-inertia answer; we assert the independent oracle reproduces it.

THE HEADLINE REGRESSION (finding #1). A two-compartment container: the left
compartment holds 6 units up to the divider crest, the right compartment is wider
and starts empty, and 8 units are placed in the left. The correct quasistatic
answer is 6 left / 2 right. The PR#9 oracle found a single global water height
whose reachable region held 8 units, then rescaled to conserve mass; because
reachable capacity JUMPS 6->18 when the level crosses the divider, that rescale
was a large WRONG redistribution -> 2.667 left / 5.333 right, with total mass
still exactly 8 (so mass-conservation never caught it). The fixed oracle fills the
lowest reachable basin to its crest and spills only the EXCESS into connected
lower basins iteratively.

Run:  /workspace/.venv/bin/python experiments/test_spill_regression.py
   or  /workspace/.venv/bin/python -m pytest experiments/test_spill_regression.py
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from truth_solver import settle_truth  # noqa: E402

TOL = 0.05   # cell-masses; the oracle is exact to numerical precision here


def _box(H, W):
    walls = np.zeros((H, W), bool)
    walls[0, :] = walls[-1, :] = True
    walls[:, 0] = walls[:, -1] = True
    return walls, np.zeros((H, W))


def _place(mass, walls, x0, x1, n):
    """Place exactly `n` unit-mass cells into columns [x0, x1), stacked from the
    floor up (downfall settles them anyway; this just guarantees the volume)."""
    H = mass.shape[0]
    placed = 0
    for y in range(H - 2, 0, -1):
        for x in range(x0, x1):
            if placed >= n:
                return
            if not walls[y, x] and mass[y, x] == 0:
                mass[y, x] = 1.0
                placed += 1


# ---------------------------------------------------------------------------
def scene_two_compartment():
    """Left holds 6 to the crest; right wider+empty; 8 placed left -> 6 / 2."""
    H, W = 10, 12
    walls, mass = _box(H, W)
    xd = 4                       # divider column
    crest_h = 2                  # divider rises 2 cells above the floor
    walls[H - 1 - crest_h:H - 1, xd] = True
    for x in range(1, xd):       # 8 units in the left compartment (cols 1..3)
        mass[H - 2, x] = 1.0
        mass[H - 3, x] = 1.0
    mass[H - 4, 1] = 1.0
    mass[H - 4, 2] = 1.0
    rest = settle_truth(mass, walls)
    left = rest[:, 1:xd].sum()
    right = rest[:, xd + 1:W - 1].sum()
    return [("two_compartment left", left, 6.0),
            ("two_compartment right", right, 2.0),
            ("two_compartment total", rest.sum(), 8.0)]


def scene_cascade_nested():
    """Three equal compartments (each holds 6 to its crest); 14 placed in the
    leftmost -> 6 / 6 / 2 (iterated spill through nested basins)."""
    H, W = 10, 16
    walls, mass = _box(H, W)
    crest_h = 2
    d1, d2 = 4, 8
    walls[H - 1 - crest_h:H - 1, d1] = True
    walls[H - 1 - crest_h:H - 1, d2] = True
    _place(mass, walls, 1, d1, 14)   # 14 units into the leftmost compartment
    rest = settle_truth(mass, walls)
    c0 = rest[:, 1:d1].sum()
    c1 = rest[:, d1 + 1:d2].sum()
    c2 = rest[:, d2 + 1:W - 1].sum()
    return [("cascade left", c0, 6.0),
            ("cascade mid", c1, 6.0),
            ("cascade right", c2, 2.0),
            ("cascade total", rest.sum(), 14.0)]


def scene_utube():
    """Connected vessels equalize to the SAME level (spill-and-merge)."""
    H, W = 22, 30
    walls, mass = _box(H, W)
    walls[3:H - 1, 1:W - 1] = True
    xL, xR, sw = 5, 20, 5
    floor = H - 3
    for y in range(3, floor):
        walls[y, xL:xL + sw] = False
        walls[y, xR:xR + sw] = False
    walls[floor:H - 1, xL:xR + sw] = False
    for y in range(6, floor):            # fill only the LEFT shaft
        mass[y, xL:xL + sw] = 1.0
    mass[walls] = 0
    rest = settle_truth(mass, walls)
    lh = rest[:, xL:xL + sw].sum() / sw
    rh = rest[:, xR:xR + sw].sum() / sw
    return [("utube equalizes (|lh-rh|)", abs(lh - rh), 0.0)]


def scene_tilted_terraces():
    """A tilted/stepped floor: a high left terrace with a 2-tall retaining lip on
    its downhill edge, stepping down to a deep right terrace. The left terrace
    retains water up to its lip crest; the excess spills down the step into the
    deep right terrace. The lip pocket is 3 cols x 2 rows (capacity 6); pour 12 ->
    left retains 6, the excess 6 spills into the right terrace."""
    H, W = 12, 12
    walls, mass = _box(H, W)
    # Left terrace: a solid slab at row 6 spanning cols 1..4 (and solid beneath),
    # so water rests on rows 5,4,3,... above it.
    walls[6, 1:5] = True
    walls[7:H - 1, 1:5] = True
    # Retaining lip on the terrace's downhill (right) edge: a 2-tall wall at col 4
    # rows 4,5. The retained pocket is cols 1..3 x rows 4,5 = 6 cell-masses.
    walls[4:6, 4] = True
    # Right terrace uses the box floor (deep). Pour 12 units onto the left terrace.
    _place(mass, walls, 1, 4, 12)
    mass[walls] = 0
    rest = settle_truth(mass, walls)
    left = rest[:, 1:4].sum()
    right = rest[:, 5:W - 1].sum()
    return [("terraces total", rest.sum(), 12.0),
            ("terraces left retains to crest", left, 6.0),
            ("terraces right receives spill", right, 6.0)]


def scene_retention_no_spill():
    """A TALL divider with insufficient volume: water is RETAINED entirely on the
    left, right stays dry (no spurious spill)."""
    H, W = 14, 16
    walls, mass = _box(H, W)
    xd = 6
    walls[2:H - 1, xd] = True            # near-full-height divider
    for y in range(H - 5, H - 1):        # a modest pool on the left
        mass[y, 1:xd] = 1.0
    mass[walls] = 0
    rest = settle_truth(mass, walls)
    right = rest[:, xd + 1:W - 1].sum()
    return [("retention right stays dry", right, 0.0)]


SCENES = [scene_two_compartment, scene_cascade_nested, scene_utube,
          scene_tilted_terraces, scene_retention_no_spill]


def _run():
    ok = True
    for scene in SCENES:
        for name, got, want in scene():
            passed = abs(float(got) - float(want)) <= TOL
            ok = ok and passed
            print(f"  [{'PASS' if passed else 'FAIL'}] {name}: "
                  f"got={float(got):.3f} want={float(want):.3f}")
    print("\nSPILL REGRESSION:", "ALL PASS" if ok else "FAILURES PRESENT")
    return ok


# pytest entry points ---------------------------------------------------------
def test_two_compartment_6_2():
    for name, got, want in scene_two_compartment():
        assert abs(float(got) - float(want)) <= TOL, name


def test_cascade_nested():
    for name, got, want in scene_cascade_nested():
        assert abs(float(got) - float(want)) <= TOL, name


def test_utube_equalizes():
    for name, got, want in scene_utube():
        assert abs(float(got) - float(want)) <= TOL, name


def test_tilted_terraces():
    for name, got, want in scene_tilted_terraces():
        assert abs(float(got) - float(want)) <= TOL, name


def test_retention_no_spill():
    for name, got, want in scene_retention_no_spill():
        assert abs(float(got) - float(want)) <= TOL, name


if __name__ == "__main__":
    sys.exit(0 if _run() else 1)
