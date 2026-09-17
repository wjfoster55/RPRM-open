"""F3 certificates for the pinned model-B breach receiver.

Frozen F2 Layer B (`sill_need` CERTIFIED_NO) remains refuted. This module
does not restore it. Official static routing is:

- Layer A on *unit-normalized* occupancy (surviving F2 result)
- Unit-isolation NO: exactly one water cell, not on R_catwalk
- otherwise UNRESOLVED, then the existing limited-exact continuation

Evidence grades are declared in CLAIM.md. V >= 2 remains OPEN for a static
NO bound because same-row support injection is admitted.
"""
from __future__ import annotations

from f2_import import bound


def normalize_unit_occupancy(mass, walls):
    """Match pinned normalizeForModel(B): every positive-mass non-wall cell
    becomes occupancy 1 before any certificate or rollout comparison."""
    out = []
    for i, m in enumerate(mass):
        if walls[i]:
            out.append(0.0)
        elif m > 0:
            out.append(1.0)
        else:
            out.append(0.0)
    return out


def unit_water_count(mass, walls):
    n = 0
    for i, m in enumerate(mass):
        if walls[i]:
            continue
        if m > 0:
            n += 1
    return n


def isolation_verdict(layers, n_water, theta):
    """CERTIFIED_NO only for a unique unit cell outside R_catwalk.

    Written proof in DERIVATION.md: a unique occurrence cannot inject a
    floor for another occurrence, so every actual stepB move is a catwalk
    move. R_catwalk is the reverse reachable set on that graph.
    """
    if n_water == 0:
        return {
            "verdict": "UNRESOLVED",
            "reason": "no_water_defer_to_A",
            "n_water": 0,
        }
    if n_water >= 2:
        return {
            "verdict": "UNRESOLVED",
            "reason": "n_ge_2_support_injection_admitted",
            "n_water": n_water,
        }
    if layers["A"]["verdict"] == "CERTIFIED_YES":
        return {
            "verdict": "CERTIFIED_YES",
            "reason": "monitor_mass_gt_theta_now",
            "n_water": 1,
        }
    if layers["A"]["verdict"] == "CERTIFIED_NO":
        return {
            "verdict": "UNRESOLVED",
            "reason": "A_already_no",
            "n_water": 1,
        }
    w_cat = layers["stats"]["water_in_R_catwalk"]
    if w_cat > theta:
        return {
            "verdict": "UNRESOLVED",
            "reason": "unique_cell_on_R_catwalk",
            "n_water": 1,
        }
    return {
        "verdict": "CERTIFIED_NO",
        "reason": "unique_cell_not_on_R_catwalk",
        "n_water": 1,
    }


def evaluate_f3(walls, mass, monitor, W, H, theta, dx=None, crest_y=None):
    mass_n = normalize_unit_occupancy(mass, walls)
    n_water = unit_water_count(mass_n, walls)
    layers = bound.evaluate_layers(
        walls, mass_n, monitor, W, H, theta, dx=dx, crest_y=crest_y,
    )
    iso = isolation_verdict(layers, n_water, theta)
    old_b = layers["B"]
    official, reason = official_static_verdict_f3(layers, iso)
    return {
        "normalized_mass": mass_n,
        "n_water": n_water,
        "A": layers["A"],
        "B_refuted": old_b,
        "isolation": iso,
        "failed_gap_adjacent": layers["failed_gap_adjacent"],
        "stats": layers["stats"],
        "static": official,
        "static_reason": reason,
        "layers_raw": layers,
    }


def official_static_verdict_f3(layers, iso):
    """A first; isolation NO second; never the refuted B sill_need branch."""
    if layers["A"]["verdict"] == "CERTIFIED_YES":
        return "CERTIFIED_YES", "A:" + layers["A"]["reason"]
    if layers["A"]["verdict"] == "CERTIFIED_NO":
        return "CERTIFIED_NO", "A:" + layers["A"]["reason"]
    if iso["verdict"] == "CERTIFIED_NO":
        return "CERTIFIED_NO", "ISO:" + iso["reason"]
    return "UNRESOLVED", "ISO:" + iso["reason"]
