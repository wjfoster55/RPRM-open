"""Bounded exact corroboration for the direct YM covering argument.

Default mode recomputes and compares the adjacent deterministic receipt.
--write-results explicitly replaces that receipt. No prior checker is imported.
The analytic proof, all-spin quantifiers, and spectral closure are not certified
by these finite rational and combinatorial checks.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from math import comb
from pathlib import Path


class Checks:
    def __init__(self) -> None:
        self.count = 0

    def require(self, condition: bool, message: str) -> None:
        self.count += 1
        if not condition:
            raise RuntimeError(message)


def rational(value: F) -> str:
    return f"{value.numerator}/{value.denominator}"


def add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(left, right))


def unit(dimension: int, axis: int) -> tuple[int, ...]:
    return tuple(int(index == axis) for index in range(dimension))


def edge(left: tuple[int, ...], right: tuple[int, ...]):
    return tuple(sorted((left, right)))


def fixture(side_lengths: tuple[int, ...]):
    dimension = len(side_lengths)
    vertices = set(itertools.product(*(range(length + 1) for length in side_lengths)))
    directions = tuple(unit(dimension, axis) for axis in range(dimension))
    edges = set()
    for vertex in vertices:
        for direction in directions:
            neighbor = add(vertex, direction)
            if neighbor in vertices:
                edges.add(edge(vertex, neighbor))

    plaquettes = []
    for anchor in sorted(vertices):
        for i, j in itertools.combinations(range(dimension), 2):
            vi = add(anchor, directions[i])
            vj = add(anchor, directions[j])
            vij = add(vi, directions[j])
            boundary = frozenset((edge(anchor, vi), edge(vi, vij),
                                  edge(vij, vj), edge(vj, anchor)))
            if boundary <= edges:
                plaquettes.append((anchor, i, j, boundary))
    return dimension, vertices, tuple(sorted(edges)), tuple(plaquettes)


def check_spin_bounds(checks: Checks) -> dict:
    count_before = checks.count
    max_twice_spin = 128
    largest_ratio = F(0)
    derivative_equality = []
    for twice_spin in range(max_twice_spin + 1):
        spin = F(twice_spin, 2)
        lam = 2 * spin * (spin + 1)
        derivative = 2 * spin
        checks.require(derivative <= F(2, 3) * lam, "single-generator bound")
        checks.require(derivative * derivative <= 2 * lam, "single-edge Hessian bound")
        if spin:
            checks.require(lam >= F(3, 2), "nontrivial Casimir lower bound")
            ratio = derivative * derivative / lam
            checks.require(ratio < 2, "positive-spin Hessian ratio")
            largest_ratio = max(largest_ratio, ratio)
            if derivative == F(2, 3) * lam:
                derivative_equality.append(rational(spin))
        else:
            checks.require(lam == derivative == 0, "trivial representation")

    vector_cases = 0
    spin_choices = tuple(F(index, 2) for index in range(5))
    vector_choices = (F(-1), F(0), F(1))
    for spins in itertools.product(spin_choices, repeat=3):
        lambdas = tuple(2 * spin * (spin + 1) for spin in spins)
        for values in itertools.product(vector_choices, repeat=3):
            left = sum((2 * spin * abs(value) for spin, value in zip(spins, values)), F(0)) ** 2
            right = 2 * sum(lambdas, F(0)) * sum(
                (value * value for spin, value in zip(spins, values) if spin), F(0)
            )
            checks.require(left <= right, "three-edge weighted Cauchy-Schwarz control")
            vector_cases += 1

    # A unit trace-norm matrix coefficient at a highest-weight basis vector
    # has these exact derivative magnitudes at identity. The coefficient
    # norm remains one; the derivative magnitudes grow with spin.
    high_spin = F(64)
    first = 2 * high_spin
    second = first * first
    checks.require(first > 1 and second > 1, "unweighted high-spin hostile control")
    checks.require(first == 128 and second == 16384, "explicit high-spin derivative magnitudes")
    return {
        "twice_spin_range_inclusive": [0, max_twice_spin],
        "single_spin_cases": max_twice_spin + 1,
        "nonzero_derivative_equality_spins": derivative_equality,
        "maximum_checked_hessian_ratio": rational(largest_ratio),
        "three_edge_vector_cases": vector_cases,
        "unweighted_high_spin_control": {
            "spin": rational(high_spin), "coefficient_trace_norm": "1/1",
            "first_derivative_magnitude": rational(first),
            "second_derivative_magnitude": rational(second),
            "meaning": "finite hostile instance; unbounded growth follows from the written 2j and (2j)^2 formulas",
        },
        "assertions": checks.count - count_before,
    }


def check_contraction(checks: Checks) -> dict:
    count_before = checks.count
    radius = F(1, 4)
    rows = []
    for dimension in (2, 3):
        incidence = 2 * (dimension - 1)
        coupling = F(1, 48 * incidence)
        source = 8 * incidence * coupling
        nonlinear = F(4, 3) * radius * radius
        contraction = F(8, 3) * radius
        curvature = 2 - 4 * radius
        gap = curvature / 2
        checks.require(source == F(1, 6), "endpoint source contribution")
        checks.require(nonlinear == F(1, 12), "endpoint nonlinear contribution")
        checks.require(source + nonlinear == radius, "endpoint invariant ball")
        checks.require(contraction == F(2, 3) and contraction < 1, "endpoint contraction")
        checks.require(curvature == 1 and gap == F(1, 2), "endpoint Bochner gap")
        checks.require(F(4, 3) * radius * radius - radius + 8 * incidence * coupling == 0,
                       "endpoint scalar majorant root")
        checks.require(1 - F(128, 3) * incidence * coupling == F(1, 9),
                       "endpoint majorant discriminant")
        rows.append({"dimension": dimension, "m": incidence, "coupling": rational(coupling),
                     "radius": rational(radius), "source": rational(source),
                     "nonlinear": rational(nonlinear), "contraction": rational(contraction),
                     "weighted_Ricci_lower": rational(curvature), "gap_lower": rational(gap)})
    return {"rows": rows, "assertions": checks.count - count_before}


def check_graph_family(checks: Checks, name: str, side_lengths: tuple[int, ...],
                       expected_edges: int, expected_faces: int) -> dict:
    count_before = checks.count
    dimension, full_vertices, edges, plaquettes = fixture(side_lengths)
    checks.require(len(edges) == expected_edges, f"{name}: full edge count")
    checks.require(len(plaquettes) == expected_faces, f"{name}: full face count")
    m = 2 * (dimension - 1)
    anchor_bound = comb(dimension, 2)
    shape = ((0,) * dimension,) + tuple(unit(dimension, axis) for axis in range(dimension))
    face_histogram: dict[str, int] = {}
    empty_subsets = 0
    max_edge_incidence = 0
    max_anchor_incidence = 0

    for mask in range(1 << len(edges)):
        selected = frozenset(e for index, e in enumerate(edges) if mask & (1 << index))
        vertices = {vertex for e in selected for vertex in e}
        padded = {add(vertex, shift) for vertex in vertices for shift in shape}
        faces = tuple(p for p in plaquettes if p[3] <= selected)
        face_histogram[str(len(faces))] = face_histogram.get(str(len(faces)), 0) + 1
        if not selected:
            empty_subsets += 1
        checks.require(all(e[0] in padded for e in selected), f"{name}: outgoing blocks retained")
        edge_counts = {e: 0 for e in selected}
        anchor_counts: dict[tuple[int, ...], int] = {}

        for anchor, i, j, boundary in faces:
            checks.require(len(boundary) == 4 and boundary <= selected, f"{name}: complete face support")
            origins = {e[0] for e in boundary}
            common_support = {add(anchor, shift) for shift in shape}
            actual_support = {anchor, add(anchor, unit(dimension, i)),
                              add(anchor, unit(dimension, j))}
            checks.require(origins == actual_support, f"{name}: exact outgoing-block origins")
            checks.require(origins <= common_support, f"{name}: common interaction shape")
            checks.require(common_support <= padded, f"{name}: padded volume coverage")
            for e in boundary:
                edge_counts[e] += 1
            anchor_counts[anchor] = anchor_counts.get(anchor, 0) + 1

        local_max = max(edge_counts.values(), default=0)
        anchor_max = max(anchor_counts.values(), default=0)
        checks.require(local_max <= m, f"{name}: edge incidence bound")
        checks.require(anchor_max <= anchor_bound, f"{name}: source anchor bound")
        max_edge_incidence = max(max_edge_incidence, local_max)
        max_anchor_incidence = max(max_anchor_incidence, anchor_max)

    checks.require(empty_subsets == 1, f"{name}: empty subset admitted")
    checks.require(sum(face_histogram.values()) == (1 << len(edges)), f"{name}: complete subset census")
    dropped = [p for p in plaquettes
               if not {add(p[0], shift) for shift in shape} <= full_vertices]
    if dimension == 3:
        checks.require(len(dropped) == 3 and len(plaquettes) == 6,
                       "cube: unpadded common shape drops exactly three of six faces")
    else:
        checks.require(len(dropped) == 0, "two squares: no unpadded common-shape loss")

    return {
        "fixture": name, "dimension": dimension, "side_lengths": list(side_lengths),
        "full_vertices": len(full_vertices), "full_edges": len(edges),
        "full_plaquettes": len(plaquettes), "all_edge_subsets": 1 << len(edges),
        "empty_subsets": empty_subsets,
        "plaquette_count_histogram": face_histogram,
        "maximum_checked_edge_incidence": max_edge_incidence, "edge_incidence_bound": m,
        "maximum_checked_source_anchor_incidence": max_anchor_incidence,
        "source_anchor_bound": anchor_bound,
        "unpadded_common_shape_dropped_faces": len(dropped),
        "assertions": checks.count - count_before,
    }


def check_undressed_counterexample(checks: Checks) -> dict:
    count_before = checks.count
    rows = []
    for constant in (1, 2, 7, 100):
        t = F(1, 4 * constant)
        r = F(1)
        perturbation_abs = r * t / 2
        excitation_number = t * t
        kinetic = F(3, 2) * t * t
        proposed_bound = constant * r * excitation_number
        checks.require(perturbation_abs > proposed_bound, "undressed excitation-number bound fails")
        checks.require(perturbation_abs == 2 * proposed_bound, "exact hostile ratio")
        checks.require(kinetic == 6 * t * t * F(1, 4), "one-plaquette kinetic expectation")
        checks.require(excitation_number == 4 * t * t * F(1, 4), "one-plaquette excitation number")
        rows.append({"C": constant, "t": rational(t), "r": rational(r),
                     "absolute_perturbation_form": rational(perturbation_abs),
                     "excitation_number_form": rational(excitation_number),
                     "kinetic_form": rational(kinetic),
                     "proposed_CrN_bound": rational(proposed_bound), "violation_ratio": "2/1"})
    return {"rows": rows, "assertions": checks.count - count_before}


def compute_receipt() -> dict:
    checks = Checks()
    groups = {
        "spin_and_collective_hessian_controls": check_spin_bounds(checks),
        "contraction_endpoints": check_contraction(checks),
        "edge_subset_geometry": [
            check_graph_family(checks, "two_adjacent_square_plaquettes", (2, 1), 7, 2),
            check_graph_family(checks, "unit_three_dimensional_cube", (1, 1, 1), 12, 6),
        ],
        "undressed_vacuum_counterexamples": check_undressed_counterexample(checks),
    }
    return {
        "schema": "ym-covering-bounded-corroboration-v1",
        "status": "PASS",
        "evidence_grade": "FINITE_EXACT_RATIONAL_AND_COMBINATORIAL_CHECKS",
        "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_derivation_certified": False,
        "scope": "Finite spin/vector controls and complete edge-subset censuses of the two named fixtures only.",
        "not_certified": ["all-spin trace-norm multiplication", "all-graph anchored norm estimates",
                          "Banach fixed-point analytic construction", "elliptic regularity",
                          "Bochner identity and full spectral/form-domain closure",
                          "infinite-volume or continuum Yang-Mills theory"],
        "old_checkers_imported_or_run": False,
        "assertions": checks.count,
        "groups": groups,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-results", action="store_true",
                        help="Explicitly replace the adjacent deterministic receipt.")
    arguments = parser.parse_args()
    result = compute_receipt()
    result_path = Path(__file__).with_name("RESULTS_COVERING.json")
    if arguments.write_results:
        result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        action = "wrote"
    else:
        stored = json.loads(result_path.read_text(encoding="utf-8"))
        if stored != result:
            raise RuntimeError("Receipt mismatch: recomputed full deterministic result differs from saved JSON")
        action = "matched"
    print(f"PASS: {result['assertions']} exact bounded assertions; {action} RESULTS_COVERING.json")


if __name__ == "__main__":
    main()
