"""Exact local plaquette incidence and rational conditional-head bounds.

Generate the complete elementary incidence star around one lattice edge
in dimensions two and three. This is a finite combinatorial certificate,
not a lattice simulation or a proof of actual-vacuum remainder control.
"""

from fractions import Fraction as F
from hashlib import sha256
from math import comb
from pathlib import Path
import argparse
import json


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def shift(point, axis, amount=1):
    out = list(point)
    out[axis] += amount
    return tuple(out)


def edge(left, right):
    return tuple(sorted((left, right)))


def plaquette_edges(plaquette):
    base, axes = plaquette
    i, j = axes
    pi, pj = shift(base, i), shift(base, j)
    pij = shift(pi, j)
    return frozenset((edge(base, pi), edge(base, pj), edge(pi, pij), edge(pj, pij)))


def incident_plaquettes(link):
    left, right = link
    differences = [right[i]-left[i] for i in range(len(left))]
    require(differences.count(1) == 1 and all(v in (0,1) for v in differences),
            "Input must be a positively oriented unit lattice edge")
    axis = differences.index(1)
    return frozenset((base, tuple(sorted((axis, other))))
                     for other in range(len(left)) if other != axis
                     for base in (left, shift(left, other, -1)))


def star_record(dimension):
    origin = (0,)*dimension
    center = edge(origin, shift(origin, 0))
    m = 2*(dimension-1)
    singles = incident_plaquettes(center)
    require(len(singles) == m, "Complete single-plaquette star")
    pairs = set()
    neighbor_counts = []
    for p in singles:
        neighbors = set().union(*(incident_plaquettes(link) for link in plaquette_edges(p)))
        neighbors.remove(p)
        require(len(neighbors) == 4*(m-1), "Complete adjacent-plaquette neighbors")
        neighbor_counts.append(len(neighbors))
        for q in neighbors:
            ep, eq = plaquette_edges(p), plaquette_edges(q)
            require(len(ep & eq) == 1 and len(ep | eq) == 7,
                    "An adjacent union must have one shared and seven total edges")
            pairs.add(tuple(sorted((p,q))))
    safe_pairs = 4*m*(m-1)
    double_counts = comb(m,2)
    require(len(pairs) == safe_pairs-double_counts, "Unordered pair double-count correction")
    require(len(pairs) == {2:7, 3:42}[dimension], "Independent explicit star count")
    both_contain_center = sum(center in plaquette_edges(p) and center in plaquette_edges(q)
                              for p,q in pairs)
    require(both_contain_center == double_counts, "Shared-center pairs")
    require(len(pairs)-both_contain_center == {2:6,3:36}[dimension],
            "Hostile both-plaquettes-only count must omit actual incident factors")

    # Sum per-exterior-edge factor incidences independently from factor sizes.
    outside_counts = {}
    for p in singles:
        for link in plaquette_edges(p)-{center}:
            outside_counts.setdefault(link,[0,0])[0] += 1
    for p,q in pairs:
        for link in (plaquette_edges(p)|plaquette_edges(q))-{center}:
            outside_counts.setdefault(link,[0,0])[1] += 1
    require(sum(n[0] for n in outside_counts.values()) == 3*m, "Single exposure sum")
    require(sum(n[1] for n in outside_counts.values()) == 6*len(pairs), "Pair exposure sum")
    linear_b = sum(F(2)*n[0]*F(2,3) for n in outside_counts.values())
    quadratic_b = sum(F(2)*n[1]*F(4,351) for n in outside_counts.values())
    safe_quadratic_b = F(64*m*(m-1),117)
    require(linear_b == 4*m and quadratic_b <= safe_quadratic_b, "Head oscillation row bound")
    safe_tv_quadratic = safe_quadratic_b/4
    require(safe_tv_quadratic == {2:F(32,117),3:F(64,39)}[dimension],
            "Exact head conditional row coefficients")
    return {
        "dimension": dimension,
        "max_plaquettes_per_edge": m,
        "single_plaquettes_incident_to_edge": len(singles),
        "neighbors_per_incident_plaquette": sorted(neighbor_counts),
        "adjacent_pair_factors_incident_to_edge": len(pairs),
        "safe_pair_overcount": safe_pairs,
        "shared_center_pair_double_counts": double_counts,
        "hostile_both_plaquettes_only_omitted_factors": len(pairs)-both_contain_center,
        "outside_edge_occurrences": len(outside_counts),
        "outside_single_factor_exposures": 3*m,
        "outside_pair_factor_exposures": 6*len(pairs),
        "exact_star_b_linear_coefficient": str(linear_b),
        "exact_star_b_quadratic_coefficient": str(quadratic_b),
        "safe_b_quadratic_coefficient": str(safe_quadratic_b),
        "safe_head_TV_row_linear_coefficient": str(linear_b/4),
        "safe_head_TV_row_quadratic_coefficient": str(safe_tv_quadratic),
        "pair_support_edge_sizes": [7],
        "passed": True,
    }


def compute():
    require(F(1,3)-F(1,72) == F(23,72) > 0, "Single head monotonicity on r<=1")
    require((F(1,3)-F(1,144))-(-F(1,3)-F(1,144)) == F(2,3),
            "Single head endpoint oscillation coefficient")
    require(F(2)*6*F(4,351) == F(16,117), "Pair-factor row oscillation coefficient")
    paths = [Path(__file__).resolve(), HERE/"NEXT_CONDITIONAL_PORTS.md",
             HERE/"CONNECTED_VACUUM.md",
             HERE/"accepted_sources"/"ym2_signed_differences"/"NEXT_CONNECTED_OBLIGATION.md"]
    return {
        "schema": "ym2_conditional_ports_local_incidence_v1",
        "status": "PASS",
        "evidence_grade": "Exact rational and finite local incidence checks",
        "coupling_interval_for_head_factor_bounds": "0<=r<=1",
        "single_factor_oscillation": "2r/3",
        "pair_factor_oscillation_bound": "4r^2/351",
        "safe_head_TV_row_bound": "m*r+16*m*(m-1)*r^2/117",
        "actual_vacuum_additional_term": "(1/4)*sum_j epsilon_ej(G,r)",
        "local_stars": [star_record(d) for d in (2,3)],
        "claim_boundary": "No actual remainder estimate, spectral-gap implication, simulation, or old-suite execution",
        "sources": [{"path": path.relative_to(HERE).as_posix(),
                     "sha256": sha256(path.read_bytes()).hexdigest()} for path in paths],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = compute()
    target = HERE/"RESULTS_CONDITIONAL_HEAD.json"
    if args.write_results:
        target.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    else:
        require(json.loads(target.read_text(encoding="utf-8")) == result,
                "Full saved conditional-port receipt differs")
    print("PASS: exact 2D/3D local incidence stars and conditional-head rational bounds")


if __name__ == "__main__":
    main()
