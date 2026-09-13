"""Exact finite ingredients of the two-square quantum gap derivation.

Standard library only. Exhausts all 128 edge supports, computes the
fundamental Pauli normalization using Gaussian integers, and differentiates
the stated cometric as an exact polynomial. It does not enumerate spin
labels, approximate eigenvalues, or verify the analytic spectral theorem.
"""

from pathlib import Path
import argparse
import json


EDGES = ("a", "b", "c", "d", "l", "s", "r")
VERTICES = tuple("ABCDEF")
ENDS = {
    "a": ("A", "B"), "b": ("B", "C"), "c": ("D", "E"),
    "d": ("E", "F"), "l": ("A", "D"), "s": ("B", "E"),
    "r": ("C", "F"),
}


def require(condition, message):
    """Keep every verification active under Python's optimized mode."""
    if not condition:
        raise RuntimeError(message)


def support_certificate():
    rows = []
    passed = []
    expected = {
        frozenset(("a", "c", "l", "s")): "left_square",
        frozenset(("b", "d", "s", "r")): "right_square",
        frozenset(("a", "b", "c", "d", "l", "r")): "outer_cycle",
        frozenset(EDGES): "all_seven_edges",
    }
    for mask in range(1 << len(EDGES)):
        support = [edge for i, edge in enumerate(EDGES) if mask & (1 << i)]
        degrees = {vertex: 0 for vertex in VERTICES}
        for edge in support:
            for vertex in ENDS[edge]:
                degrees[vertex] += 1
        leaves = [vertex for vertex in VERTICES if degrees[vertex] == 1]
        if not support:
            outcome = "empty_support"
        elif leaves:
            outcome = "excluded_by_degree_one_vertex"
        else:
            outcome = "passes_necessary_no_leaf_condition"
            passed.append(frozenset(support))
        rows.append({
            "mask": mask,
            "support": support,
            "vertex_degrees": [degrees[vertex] for vertex in VERTICES],
            "outcome": outcome,
            "degree_one_witness": leaves[0] if leaves else None,
        })
    require(len(rows) == 128, "Incomplete support census")
    require(set(passed) == set(expected), "Unexpected no-leaf support family")
    minimum = min(map(len, passed))
    require(minimum == 4, "No-leaf minimum support size differs from four")
    survivors = [
        {"name": expected[support], "support": [e for e in EDGES if e in support],
         "edge_count": len(support)}
        for support in passed
    ]
    # This control distinguishes a necessary degree test from a sufficient
    # spin-intertwiner test. At a vertex an odd number of fundamental factors
    # changes sign under the central element -I and therefore has no singlet.
    odd_vertices = [
        vertex for vertex in VERTICES
        if sum(vertex in ENDS[e] for e in EDGES) % 2
    ]
    require(odd_vertices == ["B", "E"], "Changed trivalent vertex control")
    return {
        "support_subsets_exhausted": len(rows),
        "empty_supports": 1,
        "excluded_nonempty_supports": sum(
            row["outcome"] == "excluded_by_degree_one_vertex" for row in rows
        ),
        "nonempty_no_leaf_supports": survivors,
        "minimum_nonempty_no_leaf_edges": minimum,
        "necessary_not_sufficient_control": {
            "support": list(EDGES),
            "passes_no_leaf": True,
            "proposed_edge_spin": "1/2 on every edge",
            "odd_fundamental_degree_vertices": odd_vertices,
            "gauge_invariant_singlet_possible": False,
            "analytic_reason": "The central element -I acts by -1 at B and E.",
        },
        "census": rows,
        "passed": True,
    }


# Gaussian integer arithmetic: (real, imaginary), never floating point.
ZERO = (0, 0)
ONE = (1, 0)
I = (0, 1)
MINUS_I = (0, -1)
MINUS_ONE = (-1, 0)


def gadd(*values):
    return (sum(z[0] for z in values), sum(z[1] for z in values))


def gmul(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def mmul(a, b):
    return tuple(tuple(gadd(*(gmul(a[i][k], b[k][j]) for k in range(2)))
                       for j in range(2)) for i in range(2))


def pauli_certificate():
    generators = (
        ((ZERO, I), (I, ZERO)),
        ((ZERO, ONE), (MINUS_ONE, ZERO)),
        ((I, ZERO), (ZERO, MINUS_I)),
    )
    products = [[mmul(a, b) for b in generators] for a in generators]
    summed = tuple(tuple(gadd(*(products[k][k][i][j] for k in range(3)))
                         for j in range(2)) for i in range(2))
    require(summed == (((-3, 0), ZERO), (ZERO, (-3, 0))),
            "Fundamental generator Casimir differs from three")
    traces = [[gadd(products[i][j][0][0], products[i][j][1][1])
               for j in range(3)] for i in range(3)]
    require(all(traces[i][j] == (-2 * int(i == j), 0)
                for i in range(3) for j in range(3)),
            "Generators are not orthonormal for -Tr(XY)/2")
    return {
        "arithmetic": "Gaussian integers (real, imaginary)",
        "generators": generators,
        "sum_generator_squares": summed,
        "trace_pair_products": traces,
        "orthonormal_for_negative_half_trace": True,
        "fundamental_negative_laplacian_eigenvalue": 3,
        "passed": True,
    }


def polynomial_add(*values):
    result = {}
    for poly in values:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {key: value for key, value in result.items() if value}


def derivative(poly, axis):
    result = {}
    for powers, coefficient in poly.items():
        if powers[axis]:
            reduced = list(powers)
            reduced[axis] -= 1
            result[tuple(reduced)] = coefficient * powers[axis]
    return result


def polynomial_rows(poly):
    return [{"powers_a_b_w": list(powers), "coefficient": coefficient}
            for powers, coefficient in sorted(poly.items())]


def drift_certificate():
    aa = {(0, 0, 0): 4, (2, 0, 0): -4}
    bb = {(0, 0, 0): 4, (0, 2, 0): -4}
    ww = {(0, 0, 0): 6, (0, 0, 2): -6}
    ab = {(0, 0, 1): 1, (1, 1, 0): -1}
    aw = {(0, 1, 0): 3, (1, 0, 1): -3}
    bw = {(1, 0, 0): 3, (0, 1, 1): -3}
    metric = ((aa, ab, aw), (ab, bb, bw), (aw, bw, ww))
    computed = [polynomial_add(*(derivative(metric[i][j], i) for i in range(3)))
                for j in range(3)]
    # Independent loop-side expectation: every distinct edge in a simple
    # fundamental trace contributes -3 times that trace.
    words = (
        (("s", 1), ("c", -1), ("l", -1), ("a", 1)),
        (("b", 1), ("r", 1), ("d", -1), ("s", -1)),
        (("b", 1), ("r", 1), ("d", -1), ("c", -1), ("l", -1), ("a", 1)),
    )
    require(all(len({edge for edge, sign in word}) == len(word) for word in words),
            "Loop-edge drift rule requires distinct edges")
    vertex_walks = []
    for word in words:
        directed = [ENDS[edge] if sign == 1 else ENDS[edge][::-1]
                    for edge, sign in word]
        require(all(directed[i][1] == directed[(i + 1) % len(word)][0]
                    for i in range(len(word))), "Trace word is not a closed path")
        vertices = [endpoints[0] for endpoints in directed]
        require(len(set(vertices)) == len(vertices), "Trace word is not a simple cycle")
        vertex_walks.append(vertices + [vertices[0]])
    expected = []
    for axis, word in enumerate(words):
        powers = tuple(int(i == axis) for i in range(3))
        expected.append({powers: -3 * len(word)})
    require(computed == expected, "Cometric divergence and loop drift disagree")
    return {
        "arithmetic": "exact integer sparse polynomials in a,b,w",
        "cometric": [[polynomial_rows(poly) for poly in row] for row in metric],
        "words": words,
        "verified_simple_vertex_walks": vertex_walks,
        "distinct_loop_edge_counts": list(map(len, words)),
        "computed_column_divergence": [polynomial_rows(poly) for poly in computed],
        "expected_loop_drift": [polynomial_rows(poly) for poly in expected],
        "passed": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-results", action="store_true",
                        help="replace the saved receipt; default recomputes and compares without writing")
    args = parser.parse_args()
    support = support_certificate()
    pauli = pauli_certificate()
    drift = drift_certificate()
    result = {
        "scope": "complete finite support census, exact Pauli products, exact polynomial drift",
        "conventions": {"edge_order": EDGES, "vertex_order": VERTICES,
                        "edge_endpoints": ENDS, "metric": "-Tr(XY)/2", "pauli": "+i sigma"},
        "support_certificate": support,
        "pauli_certificate": pauli,
        "drift_certificate": drift,
        "conditional_electric_bound_coefficient": {
            "minimum_support_edges": support["minimum_nonempty_no_leaf_edges"],
            "fundamental_casimir": pauli["fundamental_negative_laplacian_eigenvalue"],
            "twice_bound_in_units_alpha_hbar_squared": (
                support["minimum_nonempty_no_leaf_edges"]
                * pauli["fundamental_negative_laplacian_eigenvalue"]
            ),
            "kinetic_prefactor": "alpha*hbar^2/2",
            "result": "6*alpha*hbar^2",
            "analytic_inputs": [
                "Peter-Weyl gives a complete invariant spin-network basis.",
                "A vertex with one nontrivial incident representation has no singlet.",
                "All nontrivial SU(2) spins have Casimir 4*j*(j+1)>=3.",
                "An elementary loop trace attains the bound.",
            ],
        },
        "not_certified": [
            "Analytic operator domains, Haar pushforward, or unitary equivalence.",
            "Peter-Weyl completeness or a general representation-theory theorem.",
            "Interacting eigenvalues, min-max principle, or positivity improvement.",
            "A volume-uniform bound or continuum Yang-Mills mass gap.",
        ],
        "all_passed": True,
    }
    target = Path(__file__).with_name("RESULTS_QUANTUM.json")
    payload = json.dumps(result, indent=2) + "\n"
    if args.write_results:
        target.write_text(payload, encoding="utf-8")
    else:
        require(target.read_text(encoding="utf-8") == payload,
                "Saved quantum receipt differs from recomputed results")
    action = "written" if args.write_results else "compared_without_writing"
    print("PASS: all 128 supports, four nonempty no-leaf supports with minimum four edges; "
          "exact Pauli Casimir and metric; three exact cometric divergence identities.")
    print(f"Receipt {action}: {target}")


if __name__ == "__main__":
    main()
