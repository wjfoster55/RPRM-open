"""Minimal but faithful 2D rigid-body sim (disks in a box) for broadphase questions.

The sim exists only to produce a *ground-truth* "contact set per step". It supports:
  - disks under gravity with restitution + Coulomb friction (with rotation),
  - static walls (floor, left, right, ceiling),
  - resting stacks, slow drift, bouncing, and colliding bodies.

Contacts are resolved with a standard sequential-impulse (Baumgarte-stabilized)
solver, which is enough to get stable resting stacks and believable impacts.

Everything is deterministic given the initial state, so ground truth is well-defined:
advancing one step and recomputing the contact set is the oracle.
"""
from __future__ import annotations

import numpy as np

# ---- World constants (a consistent unit system: radii ~ O(0.5), box ~ O(10)) ----
GRAVITY = 9.8
DT = 1.0 / 60.0

# Near-contact band that DEFINES the receiver's "contact set".  A pair (i,j) is in
# the contact set iff its surface gap < CONTACT_BAND.  This band is what both the
# certificate and the baselines must respect, so it is fixed and shared.
CONTACT_BAND = 0.03

# Solver detects/handles contacts a bit earlier than the receiver band so that
# resting bodies stay comfortably inside the band instead of buzzing across it.
SOLVE_BAND = 0.05
SLOP = 0.005          # penetration allowance before Baumgarte pushes out
BAUMGARTE = 0.2       # positional error feedback fraction
SOLVER_ITERS = 12


class World:
    """A box [0,W] x [0,H] containing N disks."""

    def __init__(self, W=10.0, H=10.0, gravity=GRAVITY, dt=DT,
                 restitution=0.0, friction=0.5, walls=("floor", "left", "right")):
        self.W = float(W)
        self.H = float(H)
        self.gravity = float(gravity)
        self.dt = float(dt)
        self.restitution = float(restitution)
        self.friction = float(friction)
        self.walls = tuple(walls)

        self.pos = np.zeros((0, 2))
        self.vel = np.zeros((0, 2))
        self.ang = np.zeros(0)
        self.omega = np.zeros(0)
        self.radius = np.zeros(0)
        self.inv_mass = np.zeros(0)
        self.inv_I = np.zeros(0)

    # ---- construction ----
    def add_disks(self, pos, vel, radius, density=1.0):
        pos = np.asarray(pos, float).reshape(-1, 2)
        vel = np.asarray(vel, float).reshape(-1, 2)
        radius = np.asarray(radius, float).reshape(-1)
        n = pos.shape[0]
        mass = density * np.pi * radius ** 2
        I = 0.5 * mass * radius ** 2
        self.pos = np.vstack([self.pos, pos])
        self.vel = np.vstack([self.vel, vel])
        self.ang = np.concatenate([self.ang, np.zeros(n)])
        self.omega = np.concatenate([self.omega, np.zeros(n)])
        self.radius = np.concatenate([self.radius, radius])
        self.inv_mass = np.concatenate([self.inv_mass, 1.0 / mass])
        self.inv_I = np.concatenate([self.inv_I, 1.0 / I])

    @property
    def n(self):
        return self.pos.shape[0]

    def copy(self):
        w = World(self.W, self.H, self.gravity, self.dt,
                  self.restitution, self.friction, self.walls)
        w.pos = self.pos.copy()
        w.vel = self.vel.copy()
        w.ang = self.ang.copy()
        w.omega = self.omega.copy()
        w.radius = self.radius.copy()
        w.inv_mass = self.inv_mass.copy()
        w.inv_I = self.inv_I.copy()
        return w

    # ---- contact detection ----
    def detect_contacts(self, band=SOLVE_BAND):
        """Return a list of contacts as dicts.

        Each contact: {a, b, normal(from a to b), gap, ra, rb}. Wall contacts use
        b = -1 minus a wall code and a synthetic normal.  Positive gap = separated;
        negative = penetration.
        """
        contacts = []
        n = self.n
        pos = self.pos
        rad = self.radius

        # disk-disk
        for i in range(n):
            for j in range(i + 1, n):
                d = pos[j] - pos[i]
                dist = np.hypot(d[0], d[1])
                gap = dist - (rad[i] + rad[j])
                if gap < band:
                    if dist > 1e-12:
                        nrm = d / dist
                    else:
                        nrm = np.array([0.0, 1.0])
                    ra = nrm * rad[i]
                    rb = -nrm * rad[j]
                    contacts.append(dict(a=i, b=j, normal=nrm, gap=gap, ra=ra, rb=rb))

        # disk-wall
        for i in range(n):
            x, y = pos[i]
            r = rad[i]
            # Normal convention: points from disk `a` toward wall `b` (a->b), matching
            # the disk-disk convention. ra points from a's center to the contact point.
            if "floor" in self.walls:
                gap = y - r
                if gap < band:
                    contacts.append(dict(a=i, b=self._wall_id("floor"),
                                         normal=np.array([0.0, -1.0]), gap=gap,
                                         ra=np.array([0.0, -r]), rb=np.zeros(2)))
            if "ceiling" in self.walls:
                gap = (self.H - y) - r
                if gap < band:
                    contacts.append(dict(a=i, b=self._wall_id("ceiling"),
                                         normal=np.array([0.0, 1.0]), gap=gap,
                                         ra=np.array([0.0, r]), rb=np.zeros(2)))
            if "left" in self.walls:
                gap = x - r
                if gap < band:
                    contacts.append(dict(a=i, b=self._wall_id("left"),
                                         normal=np.array([-1.0, 0.0]), gap=gap,
                                         ra=np.array([-r, 0.0]), rb=np.zeros(2)))
            if "right" in self.walls:
                gap = (self.W - x) - r
                if gap < band:
                    contacts.append(dict(a=i, b=self._wall_id("right"),
                                         normal=np.array([1.0, 0.0]), gap=gap,
                                         ra=np.array([r, 0.0]), rb=np.zeros(2)))
        return contacts

    @staticmethod
    def _wall_id(name):
        return {"floor": -1, "ceiling": -2, "left": -3, "right": -4}[name]

    # ---- one physics step ----
    def step(self):
        dt = self.dt
        # integrate velocity (gravity)
        self.vel[:, 1] -= self.gravity * dt

        contacts = self.detect_contacts(SOLVE_BAND)
        for c in contacts:
            c["jn_acc"] = 0.0
            c["jt_acc"] = 0.0
            # initial approach speed, used for restitution target (only real impacts)
            va = self._vel_at(c["a"], c["ra"])
            vb = self._vel_at(c["b"], c["rb"])
            vn0 = (vb - va) @ c["normal"]
            c["restitution_target"] = -self.restitution * vn0 if vn0 < -1.0 else 0.0

        # sequential impulse solver (velocity level) with ACCUMULATED impulses:
        # clamp the total normal impulse >= 0 (not each increment), which is what
        # makes resting stacks stable.
        for _ in range(SOLVER_ITERS):
            for c in contacts:
                self._solve_contact(c, dt)

        # integrate position
        self.pos += self.vel * dt
        self.ang += self.omega * dt

    def _vel_at(self, body, r):
        if body < 0:
            return np.zeros(2)
        v = self.vel[body]
        w = self.omega[body]
        return v + w * np.array([-r[1], r[0]])

    def _apply_impulse(self, body, r, P):
        if body < 0:
            return
        self.vel[body] += self.inv_mass[body] * P
        self.omega[body] += self.inv_I[body] * (r[0] * P[1] - r[1] * P[0])

    def _solve_contact(self, c, dt):
        a, b = c["a"], c["b"]
        n = c["normal"]
        t = np.array([-n[1], n[0]])
        ra, rb = c["ra"], c["rb"]

        # effective masses
        kn = self._eff_mass(a, ra, n) + self._eff_mass(b, rb, n)
        if kn <= 0:
            return

        # Baumgarte bias for penetration beyond slop (position stabilization)
        pen = -c["gap"]
        bias = 0.0
        if pen > SLOP:
            bias = BAUMGARTE / dt * (pen - SLOP)

        # --- normal impulse (accumulated + clamped) ---
        va = self._vel_at(a, ra)
        vb = self._vel_at(b, rb)
        vn = (vb - va) @ n
        djn = -(vn - c["restitution_target"] - bias) / kn
        new_jn = max(c["jn_acc"] + djn, 0.0)
        djn = new_jn - c["jn_acc"]
        c["jn_acc"] = new_jn
        Pn = djn * n
        self._apply_impulse(a, ra, -Pn)
        self._apply_impulse(b, rb, Pn)

        # --- friction impulse (accumulated + clamped to friction cone) ---
        kt = self._eff_mass(a, ra, t) + self._eff_mass(b, rb, t)
        if kt > 0:
            va = self._vel_at(a, ra)
            vb = self._vel_at(b, rb)
            vt = (vb - va) @ t
            djt = -vt / kt
            jtmax = self.friction * c["jn_acc"]
            new_jt = np.clip(c["jt_acc"] + djt, -jtmax, jtmax)
            djt = new_jt - c["jt_acc"]
            c["jt_acc"] = new_jt
            Pt = djt * t
            self._apply_impulse(a, ra, -Pt)
            self._apply_impulse(b, rb, Pt)

    def _eff_mass(self, body, r, dir):
        if body < 0:
            return 0.0
        rn = r[0] * dir[1] - r[1] * dir[0]
        return self.inv_mass[body] + self.inv_I[body] * rn * rn


def contact_set(world, band=CONTACT_BAND):
    """The RECEIVER's observable: the set of near-contact pairs.

    Returns a frozenset of frozensets/tuples identifying pairs. Disk-disk pairs are
    (i, j) with i<j; wall pairs are (i, wall_id).  Membership uses the fixed
    CONTACT_BAND, independent of the (slightly wider) solver band.
    """
    s = set()
    for c in world.detect_contacts(band):
        a, b = c["a"], c["b"]
        if b >= 0:
            s.add((min(a, b), max(a, b)))
        else:
            s.add((a, b))
    return frozenset(s)
