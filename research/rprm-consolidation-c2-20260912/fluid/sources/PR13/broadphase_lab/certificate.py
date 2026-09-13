"""Receiver, islands, ground-truth oracle, and the four decision methods.

RECEIVER  Q : "does the contact set (the set of near-contact pairs) change on the
              next step?"  A method that certifies "no change" earns the right to
              REUSE the cached contact manifold for its island and SKIP the full
              broadphase/narrowphase recompute for that island.

DECISION UNIT: per ISLAND per STEP (exactly what an engine decides before sleeping
              an island).  An island = a connected component of the disk-disk
              contact graph; a body with no disk-disk contact is a singleton island.

The four methods (all decide, from the state at step t, "reuse this island's cached
contact set" = predict no change):

  naive        velocity-threshold sleeping: max body speed in island < tau_v.
               (the strawman the fluids result beat ~14x; NOT addition-guarded)

  pure_ca      faithful conservative advancement / speculative contacts: for every
               currently-SEPARATED pair, a safe time-of-impact bound proves it
               cannot close within dt.  CA has no certificate for *existing* contact
               persistence, so it can only certify islands with NO existing contacts
               (free/near-miss bodies).  This is CA used exactly as engines use it:
               a guard against NEW contacts / tunnelling.

  ca_sleeping  the SOPHISTICATED INCUMBENT actually shipped in mature engines:
               CA addition-guard  AND  velocity-threshold island sleeping for the
               existing contacts.  (speculative contacts + sleeping islands)

  P            the RPRM certificate:  CA addition-guard  AND  a resting/force-balance
               persistence certificate for every existing contact (predicted gap,
               under a gravity-aware acceleration bound, stays inside the contact
               band => the contact cannot be lost this step).

ca_sleeping and P share the SAME addition guard.  They differ ONLY in how they
certify that existing contacts persist: velocity-threshold (ca_sleeping) vs a
gravity-aware kinematic force-balance bound (P).  That isolates the transfer test.
"""
from __future__ import annotations

import numpy as np

from sim import World, contact_set, CONTACT_BAND, GRAVITY, DT


# ----------------------------------------------------------------------------
# Islands
# ----------------------------------------------------------------------------
def compute_islands(world: World, band=CONTACT_BAND):
    """Connected components of the disk-disk contact graph. Returns list of sets of
    body indices. Bodies with no disk-disk contact are singleton islands."""
    n = world.n
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    cs = world.detect_contacts(band)
    for c in cs:
        a, b = c["a"], c["b"]
        if a >= 0 and b >= 0:
            union(a, b)

    groups = {}
    for i in range(n):
        groups.setdefault(find(i), set()).add(i)
    return list(groups.values())


def incident_pairs(cset, island):
    """Contact-set pairs with at least one endpoint in `island` (an int set)."""
    out = set()
    for p in cset:
        a, b = p
        if a in island or (b >= 0 and b in island):
            out.add(p)
    return frozenset(out)


# ----------------------------------------------------------------------------
# Ground truth oracle
# ----------------------------------------------------------------------------
def island_truth_changed(world: World, island):
    """TRUTH: advance a copy one step; did the set of contact-set pairs incident to
    this island's bodies change?  (additions to outside bodies included)."""
    cset0 = contact_set(world)
    inc0 = incident_pairs(cset0, island)
    w2 = world.copy()
    w2.step()
    cset1 = contact_set(w2)
    inc1 = incident_pairs(cset1, island)
    return inc0 != inc1


# ----------------------------------------------------------------------------
# Shared kinematic primitives (the certificate math)
# ----------------------------------------------------------------------------
def _pair_gap_vel(world, i, j):
    """surface gap and normal relative *linear* speed (rate of gap change) for a
    disk-disk pair. Positive sep_speed = separating (gap growing)."""
    d = world.pos[j] - world.pos[i]
    dist = float(np.hypot(d[0], d[1]))
    gap = dist - (world.radius[i] + world.radius[j])
    if dist > 1e-12:
        n = d / dist
    else:
        n = np.array([0.0, 1.0])
    sep_speed = float((world.vel[j] - world.vel[i]) @ n)   # >0 => separating
    rel_speed = float(np.hypot(*(world.vel[j] - world.vel[i])))
    return gap, sep_speed, rel_speed


def _wall_gap_vel(world, i, wall):
    r = world.radius[i]
    x, y = world.pos[i]
    vx, vy = world.vel[i]
    if wall == -1:      # floor
        return y - r, vy          # sep_speed = vy (>0 moving up/away)
    if wall == -2:      # ceiling
        return (world.H - y) - r, -vy
    if wall == -3:      # left
        return x - r, vx
    if wall == -4:      # right
        return (world.W - x) - r, -vx
    raise ValueError(wall)


def _effective_speeds(world, dt, restitution_bound=2.0):
    """Per-body speed bound that accounts for impulsive momentum transfer within the
    step: a body touching / about to touch a fast neighbour can be launched during
    the step (a secondary impact), and in a dense pile that launch can travel through
    a CHAIN of contacts.  We form reachable clusters (bodies in contact or reaching
    each other this step) and bound every member's effective speed by its own speed
    plus a restitution factor times the FASTEST speed in its cluster.  A resting pile
    (all speeds ~0) inflates to ~0; a pile being struck inflates to the striker's
    speed -- exactly the cases where single-step CA is otherwise unsound ('unmodeled
    impulse exceeds |v|.dt').

    Deliberately conservative (may over-refuse in churny piles).  Shared by ALL CA
    methods (pure CA, CA+sleeping, P), so it cannot bias the head-to-head."""
    n = world.n
    speed = np.hypot(world.vel[:, 0], world.vel[:, 1])
    band = CONTACT_BAND
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(n):
        for m in range(i + 1, n):
            d = world.pos[i] - world.pos[m]
            dist = float(np.hypot(d[0], d[1]))
            if dist < 1e-12:
                continue
            gap = dist - (world.radius[i] + world.radius[m])
            nrm = d / dist
            approach = abs(float((world.vel[m] - world.vel[i]) @ nrm))
            if gap <= approach * dt + band:      # in contact or reaching this step
                ri, rm = find(i), find(m)
                if ri != rm:
                    parent[ri] = rm

    cluster_max = {}
    for i in range(n):
        r = find(i)
        cluster_max[r] = max(cluster_max.get(r, 0.0), speed[i])

    veff = speed.copy()
    for i in range(n):
        veff[i] = speed[i] + restitution_bound * cluster_max[find(i)]
    return veff


def _addition_guard(world, island, dt, a_bound, slack):
    """CA / speculative-contacts: prove NO currently-separated pair incident to the
    island can close (gap -> < CONTACT_BAND) within dt.  Uses effective speeds that
    bound one-bounce momentum transfer (soundness under impulsive acceleration)."""
    band = CONTACT_BAND
    n = world.n
    isl = island
    others = [k for k in range(n) if k not in isl]
    veff = _effective_speeds(world, dt)

    checked = set()
    members = list(isl)
    for idx, i in enumerate(members):
        for j in members[idx + 1:]:
            gap, sep, rel = _pair_gap_vel(world, i, j)
            if gap >= band:
                key = (min(i, j), max(i, j))
                if key in checked:
                    continue
                checked.add(key)
                max_close = (veff[i] + veff[j]) * dt + 0.5 * a_bound * dt * dt + slack
                if gap - max_close < band:
                    return False
        for j in others:
            gap, sep, rel = _pair_gap_vel(world, i, j)
            if gap >= band:
                max_close = (veff[i] + veff[j]) * dt + 0.5 * a_bound * dt * dt + slack
                if gap - max_close < band:
                    return False
    for i in isl:
        for wall in (-1, -2, -3, -4):
            wname = {-1: "floor", -2: "ceiling", -3: "left", -4: "right"}[wall]
            if wname not in world.walls:
                continue
            gap, sep = _wall_gap_vel(world, i, wall)
            if gap >= band:
                max_close = veff[i] * dt + 0.5 * a_bound * dt * dt + slack
                if gap - max_close < band:
                    return False
    return True


def _persistence_forcebalance(world, island, cset, dt, a_bound, slack, v_rel_tol=0.2):
    """P's resting / force-balance certificate.

    An existing contact can only DISAPPEAR next step if the two bodies separate past
    the band.  That happens either (i) kinematically -- the gap grows past the band,
    which we bound with a gravity + centrifugal (shear) acceleration term -- or (ii)
    dynamically -- a contact impulse drives them apart.  A resting/co-moving contact
    in *force balance* carries ~zero RELATIVE velocity; a contact being impacted or
    rebounding carries large relative velocity.  So the sound, receiver-relative
    condition is: every incident contact has small RELATIVE velocity (force balance,
    NOT small absolute speed -- that is the whole point vs velocity sleeping) AND its
    predicted gap stays inside the band.

    This is the rigid-contact analog of the fluid P_geo clauses: it certifies MOVING
    islands (drift, free fall) whose bodies co-move, while refusing impact churn."""
    band = CONTACT_BAND
    inc = incident_pairs(cset, island)
    for p in inc:
        a, b = p
        if b >= 0:
            d = world.pos[b] - world.pos[a]
            dist = float(np.hypot(d[0], d[1]))
            gap = dist - (world.radius[a] + world.radius[b])
            dv = world.vel[b] - world.vel[a]
            n = d / dist if dist > 1e-12 else np.array([0.0, 1.0])
            sep = float(dv @ n)                      # normal separation rate
            v_tan = float(np.hypot(*(dv - (dv @ n) * n)))
            rel_speed = float(np.hypot(*dv))
            # centrifugal/shear growth of distance at 2nd order: v_tan^2 / dist
            a_shear = (v_tan * v_tan) / max(dist, 1e-6)
            gap_next_max = gap + max(sep, 0.0) * dt + 0.5 * (a_bound + a_shear) * dt * dt + slack
            if rel_speed > v_rel_tol:
                return False   # not in force balance -> impact/rebound may reorganize
        else:
            gap, sep = _wall_gap_vel(world, a, b)
            rel_speed = abs(sep)                     # only NORMAL motion breaks a wall contact
            gap_next_max = gap + max(sep, 0.0) * dt + 0.5 * a_bound * dt * dt + slack
            if rel_speed > v_rel_tol:
                return False
        if gap_next_max >= band:
            return False   # contact could be lost kinematically -> not certifiable
    return True


# ----------------------------------------------------------------------------
# The four methods.  Each returns a bool: "certify NO change for this island".
# ----------------------------------------------------------------------------
def method_naive(world, island, cset, tau_v):
    speed = max((float(np.hypot(*world.vel[i])) for i in island), default=0.0)
    return speed < tau_v


def method_pure_ca(world, island, cset, dt=DT, a_bound=GRAVITY, slack=0.0):
    # CA can only certify islands with NO existing contacts (it has no persistence
    # certificate).  Then it must prove no new contact forms.
    inc = incident_pairs(cset, island)
    if len(inc) > 0:
        return False
    return _addition_guard(world, island, dt, a_bound, slack)


def method_ca_sleeping(world, island, cset, tau_v, dt=DT, a_bound=GRAVITY, slack=0.0):
    # SOPHISTICATED INCUMBENT (strongest realistic engine technique): CA addition
    # guard, PLUS certify the island if EITHER it has no existing contacts (pure CA
    # handles it, e.g. fast near-miss fly-bys) OR it is slow enough to sleep
    # (velocity-threshold island sleeping handles the existing contacts).  This is
    # the union of speculative-contacts + sleeping islands, given its best shot.
    if not _addition_guard(world, island, dt, a_bound, slack):
        return False
    inc = incident_pairs(cset, island)
    if len(inc) == 0:
        return True   # CA proves no new contact and there are none to lose
    speed = max((float(np.hypot(*world.vel[i])) for i in island), default=0.0)
    return speed < tau_v


def method_P(world, island, cset, dt=DT, a_bound=GRAVITY, slack=0.0):
    # RPRM certificate: CA addition guard + force-balance persistence for existing
    # contacts.
    if not _addition_guard(world, island, dt, a_bound, slack):
        return False
    return _persistence_forcebalance(world, island, cset, dt, a_bound, slack)
