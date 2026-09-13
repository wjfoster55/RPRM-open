"""Randomized scene suite for the broadphase transfer test.

Families (mirroring the fluid suite's spirit):
  settled_stack   resting stacks/pyramids (pre-settled)           -> contact set stable
  slow_drift      co-moving clump / block drifting or falling      -> MOVING but contact
                  set invariant  (the "moving-but-exact" analog)
  near_miss       separated bodies passing fast, no collision      -> set empty, stable
  impact          bodies actively colliding / about to collide     -> set CHANGES
  jitter          a settling / lightly perturbed stack             -> mostly stable, some change
  free_fall       loose bodies falling toward others / floor       -> set changes on landing
  mixed           a bit of everything in one box

Each scene returns a World already advanced to the moment of interest.  The harness
then simulates it forward a number of steps, evaluating every island every step.
"""
from __future__ import annotations

import numpy as np

from sim import World, GRAVITY


def _settle(world, steps=250):
    for _ in range(steps):
        world.step()
    return world


def settled_stack(rng):
    W = rng.uniform(5, 9)
    H = 14.0
    r = rng.uniform(0.35, 0.6)
    x = rng.uniform(r + 0.5, W - r - 0.5)
    k = rng.integers(2, 6)
    fr = rng.uniform(0.4, 0.9)
    w = World(W=W, H=H, restitution=0.0, friction=fr)
    pos = [[x + rng.uniform(-0.02, 0.02), r + i * (2 * r + 0.001)] for i in range(k)]
    w.add_disks(pos, [[0, 0]] * k, [r] * k)
    return _settle(w)


def slow_drift(rng):
    """A co-moving group: either a horizontally drifting block on a frictionless
    floor, or a clump in free fall.  Contact set is invariant while it moves."""
    W = 40.0
    H = 40.0
    r = rng.uniform(0.35, 0.6)
    mode = rng.integers(0, 2)
    if mode == 0:
        # horizontal drift on frictionless floor: a short resting row moving sideways
        w = World(W=W, H=H, restitution=0.0, friction=0.0)
        k = rng.integers(2, 5)
        x0 = rng.uniform(3, 8)
        vx = rng.uniform(1.0, 5.0) * (1 if rng.random() < 0.5 else -1)
        pos = [[x0 + i * (2 * r + 0.002), r] for i in range(k)]
        w.add_disks(pos, [[vx, 0.0]] * k, [r] * k)
        # let it reach the floor cleanly then it drifts at constant vx
        for _ in range(3):
            w.step()
        return w
    else:
        # free-falling clump (contacts internal, all bodies same velocity)
        w = World(W=W, H=H, restitution=0.0, friction=0.5,
                  walls=("floor", "left", "right"))
        k = rng.integers(2, 5)
        x0 = rng.uniform(8, 30)
        y0 = rng.uniform(20, 34)
        vy = -rng.uniform(1.0, 4.0)
        # a small vertical chain, touching
        pos = [[x0, y0 + i * (2 * r + 0.001)] for i in range(k)]
        w.add_disks(pos, [[0.0, vy]] * k, [r] * k)
        return w


def near_miss(rng):
    W = 24.0
    H = 24.0
    w = World(W=W, H=H, restitution=0.0, friction=0.3,
              walls=("floor", "left", "right"))
    k = rng.integers(2, 5)
    pos, vel, rad = [], [], []
    for _ in range(k):
        r = rng.uniform(0.35, 0.6)
        pos.append([rng.uniform(2, W - 2), rng.uniform(6, H - 2)])
        ang = rng.uniform(0, 2 * np.pi)
        sp = rng.uniform(2, 7)
        vel.append([sp * np.cos(ang), sp * np.sin(ang)])
        rad.append(r)
    w.add_disks(pos, vel, rad)
    return w


def impact(rng):
    W = 16.0
    H = 16.0
    w = World(W=W, H=H, restitution=rng.uniform(0.0, 0.6), friction=0.4)
    # a projectile aimed at a target/stack
    r = rng.uniform(0.35, 0.55)
    tx = rng.uniform(5, 11)
    k = rng.integers(1, 4)
    pos = [[tx, r + i * (2 * r + 0.001)] for i in range(k)]
    vel = [[0, 0]] * k
    rad = [r] * k
    # projectile close and closing fast
    px = tx + rng.choice([-1, 1]) * rng.uniform(1.5, 3.0)
    py = rng.uniform(r, 3 * r)
    pvx = (tx - px) * rng.uniform(2.0, 5.0)
    pos.append([px, py]); vel.append([pvx, rng.uniform(-1, 1)]); rad.append(r)
    w.add_disks(pos, vel, rad)
    # pre-settle the target only a couple steps (keep projectile moving)
    return w


def jitter(rng):
    """A settling stack that has just been placed with small gaps/velocities: it
    micro-collides its way to rest -- some steps the contact set changes, many it
    does not."""
    W = rng.uniform(5, 9)
    H = 16.0
    r = rng.uniform(0.35, 0.55)
    x = rng.uniform(r + 0.5, W - r - 0.5)
    k = rng.integers(3, 6)
    w = World(W=W, H=H, restitution=rng.uniform(0.0, 0.3), friction=rng.uniform(0.3, 0.8))
    pos = [[x + rng.uniform(-0.05, 0.05), r + i * (2 * r + rng.uniform(0.03, 0.12))]
           for i in range(k)]
    w.add_disks(pos, [[0, 0]] * k, [r] * k)
    # a few steps so it is mid-settle, not fully at rest
    for _ in range(rng.integers(2, 20)):
        w.step()
    return w


def free_fall(rng):
    W = 14.0
    H = 20.0
    w = World(W=W, H=H, restitution=0.0, friction=0.5)
    # a resting base + a loose body falling onto it (set changes on landing)
    r = rng.uniform(0.4, 0.6)
    x = rng.uniform(3, W - 3)
    base = [[x, r]]
    w.add_disks(base, [[0, 0]], [r])
    _settle(w, 80)
    w.add_disks([[x + rng.uniform(-0.1, 0.1), rng.uniform(3, 8)]], [[0, -rng.uniform(0, 3)]], [r])
    return w


def mixed(rng):
    W = 18.0
    H = 20.0
    w = World(W=W, H=H, restitution=rng.uniform(0, 0.4), friction=rng.uniform(0.3, 0.8))
    # a settled pair
    r = rng.uniform(0.4, 0.55)
    x = rng.uniform(3, 6)
    w.add_disks([[x, r], [x, r + 2 * r + 0.001]], [[0, 0]] * 2, [r] * 2)
    _settle(w, 120)
    # a drifter and a faller
    w.add_disks([[W - 4, r]], [[-rng.uniform(1, 3), 0]], [r])
    w.add_disks([[rng.uniform(8, 14), rng.uniform(10, 16)]], [[0, -rng.uniform(0, 2)]], [r])
    return w


FAMILIES = {
    "settled_stack": settled_stack,
    "slow_drift": slow_drift,
    "near_miss": near_miss,
    "impact": impact,
    "jitter": jitter,
    "free_fall": free_fall,
    "mixed": mixed,
}


def generate(n_per_family, seed=0):
    rng = np.random.default_rng(seed)
    scenes = []
    for name, fn in FAMILIES.items():
        for _ in range(n_per_family):
            scenes.append((name, fn(rng)))
    rng.shuffle(scenes)
    return scenes
