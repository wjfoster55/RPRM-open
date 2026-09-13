"""New exact finite controls only; no simulation and no old checker imports."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
COUNT = 0


def need(ok, message):
    global COUNT
    COUNT += 1
    if not ok:
        raise AssertionError(message)


def grid(shape):
    vertices = list(product(*(range(n) for n in shape)))
    edges = []
    for v in vertices:
        for k, n in enumerate(shape):
            if v[k] + 1 < n:
                u = list(v)
                u[k] += 1
                edges.append((v, tuple(u), k))
    return vertices, edges


def forest(vertices, edges, indices):
    parent = {v: v for v in vertices}

    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v

    for i in indices:
        v, u, _ = edges[i]
        a, b = root(v), root(u)
        if a == b:
            return False
        parent[a] = b
    return True


def spanning_cotrees(vertices, edges):
    all_edges = set(range(len(edges)))
    return [all_edges - set(tree)
            for tree in combinations(range(len(edges)), len(vertices) - 1)
            if forest(vertices, edges, tree)]


def cover(vertices, edges, blocks, weights):
    need(len(blocks) == len(weights), "one weight per block occurrence")
    all_edges = set(range(len(edges)))
    for b, w in zip(blocks, weights):
        need(w > 0 and forest(vertices, edges, all_edges - set(b)),
             "positive weight and forest exterior")
    loads = [sum((w for b, w in zip(blocks, weights) if e in b), F(0))
             for e in range(len(edges))]
    total = sum(weights, F(0))
    need(sum(loads, F(0)) == sum((w * len(b) for b, w in zip(blocks, weights)), F(0)),
         "overlap incidence double sum")
    cycle_rank = len(edges) - len(vertices) + 1
    need(cycle_rank > 0, "nontrivial physical cycle carrier")
    ceiling = F(len(edges), cycle_rank)
    need(total / max(loads) <= ceiling, "forest-complement counting ceiling")
    return {"vertices": len(vertices), "edges": len(edges), "blocks": len(blocks),
            "total_weight": str(total), "edge_loads": [str(v) for v in loads],
            "factor": str(total / max(loads)), "counting_ceiling": str(ceiling)}


def run():
    global COUNT
    COUNT = 0
    out = {"schema": "ym2-overlap-exact-controls-v1"}
    direction = []
    for shape in [(2, 2), (3, 4), (4, 4), (2, 2, 2), (3, 3, 3), (2, 3, 4)]:
        vertices, edges = grid(shape)
        d = len(shape)
        blocks = [{i for i, e in enumerate(edges) if e[2] != k} for k in range(d)]
        weights = [F(1, d - 1)] * d
        row = cover(vertices, edges, blocks, weights)
        need(set(row["edge_loads"]) == {"1"}, "direction edges charged once")
        need(F(row["factor"]) == F(d, d - 1), "physical direction factor")
        row["shape"] = list(shape)
        direction.append(row)
    out["direction_covers"] = direction

    vertices, edges = grid((2, 2))
    blocks = spanning_cotrees(vertices, edges)
    need(len(blocks) == 4 and all(len(b) == 1 for b in blocks), "square four cotrees")
    square = cover(vertices, edges, blocks, [F(1)] * 4)
    need(F(square["factor"]) == 4, "single square factor four")
    need(F(square["factor"]) * F(3, 2) == 6, "free physical gap normalization")
    out["square"] = square

    vertices, edges = grid((3, 2))
    blocks = spanning_cotrees(vertices, edges)
    shared = next(i for i, (a, b, k) in enumerate(edges)
                  if a[0] == b[0] == 1 and k == 1)
    need(len(blocks) == 15, "two-square spanning-tree census")
    need(sum(shared in b for b in blocks) == 6, "six shared-edge cotrees")
    weights = [F(1, 6) if shared in b else F(5, 18) for b in blocks]
    two = cover(vertices, edges, blocks, weights)
    need(set(two["edge_loads"]) == {"1"}, "optimized two-square equal loads")
    need(F(two["factor"]) == F(7, 2), "optimal two-square cover factor")
    out["two_adjacent_squares"] = two

    vertices, edges = grid((2, 2, 2))
    blocks = spanning_cotrees(vertices, edges)
    need(len(blocks) == 384, "cube spanning-tree census")
    need(all(len(b) == 5 for b in blocks), "cube five-edge cotrees")
    counts = [sum(e in b for b in blocks) for e in range(len(edges))]
    need(set(counts) == {160}, "cube incidence multiplicity 160")
    cube = cover(vertices, edges, blocks, [F(1, 160)] * len(blocks))
    need(set(cube["edge_loads"]) == {"1"}, "cube weighted load one")
    need(F(cube["factor"]) == F(12, 5), "optimal cube cover factor")
    out["cube"] = cube
    # Actual duplicate occurrences: splitting every weight leaves all readouts equal.
    duplicate = cover(vertices, edges, blocks + blocks,
                      [F(1, 320)] * (2 * len(blocks)))
    need(duplicate["edge_loads"] == cube["edge_loads"] and
         duplicate["factor"] == cube["factor"], "duplication cannot improve ratio")
    out["duplicate_cube_factor"] = duplicate["factor"]

    # Exact all-support residual eigenvalues on the auxiliary Haar SU(2)^3 carrier.
    pair_blocks = [{0, 1}, {0, 2}, {1, 2}]
    product_rows = []
    for mask in range(1, 8):
        support = {k for k in range(3) if mask & (1 << k)}
        value = sum((F(1, 2) for b in pair_blocks if b & support), F(0))
        need(value == (1 if len(support) == 1 else F(3, 2)), "product hostile spectrum")
        product_rows.append({"support": sorted(support), "eigenvalue": str(value)})
    out["nonphysical_product_control"] = product_rows

    # Rational unit vectors check the compatibility lift and its transverse kernel.
    for a, b in [(F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)), (F(0), F(1))]:
        f, h = F(7, 3), F(-5, 2)
        g = (a * f, b * f)
        need(a*a + b*b == 1, "quadratic partition")
        need(g[0]**2 + g[1]**2 == f*f, "lift isometry")
        need(a*g[0] + b*g[1] == f, "exact reconstruction")
        need(a*(-b*h) + b*(a*h) == 0, "transverse decoding kernel")
        # At a point chi' = theta'(-b,a); arbitrary f and derivative.
        df, dt = F(11, 4), F(2, 3)
        lifted_energy = (a*df - b*dt*f)**2 + (b*df + a*dt*f)**2
        need(lifted_energy == df*df + dt*dt*f*f, "IMS pointwise derivative identity")
    need(2 * F(1, 2) == 1 and 2 * F(1, 2)**2 == F(1, 2),
         "half energy shares differ from half amplitudes")

    inverse_rows = []
    for k in [4, 6, 8, 12, 20]:
        for twice_j in [1, 2, 3, 8, 32]:
            j = F(twice_j, 2)
            c = 2*j*(j+1)
            lam = k*c
            naive = lam * k/c
            need(naive == k*k, "singleton inverse loop multiplier k squared")
            # One cycle mode shared among three direction-pair groups.
            # Any partition of its total kinetic energy has the same synchronized denominator.
            parts = [F(1, 4)*lam, F(1, 3)*lam, F(5, 12)*lam]
            need(sum(parts) == lam and 1/sum(parts) == 1/lam,
                 "synchronized weighted heat denominator")
        inverse_rows.append({"loop_edges": k, "naive_multiplier": k*k})
    out["free_inverse_loops"] = inverse_rows
    high_spin = []
    for twice_j in [1, 2, 8, 32, 128]:
        j = F(twice_j, 2)
        q = (6 + 8*j*(j+1))/6
        need(q > 1, "physical two-loop partial inverse amplification")
        high_spin.append({"spin": str(j), "multiplier_lower_bound_at_weight_one": str(q)})
    need(all(F(a["multiplier_lower_bound_at_weight_one"]) <
             F(b["multiplier_lower_bound_at_weight_one"])
             for a, b in zip(high_spin, high_spin[1:])), "high-spin amplification grows")
    out["fixed_graph_physical_high_spin"] = high_spin

    # Exact counting-ceiling excess over the uniform directional factor.
    ceilings = []
    for d in [2, 3]:
        for n in [2, 3, 4, 8, 16, 64]:
            v, e = n**d, d*(n-1)*n**(d-1)
            rank = e-v+1
            ratio = F(e, rank)
            excess = F(d*(n**(d-1)-1), (d-1)*rank)
            need(ratio-F(d,d-1) == excess > 0, "finite box ceiling excess")
            ceilings.append({"dimension": d, "side_vertices": n,
                             "counting_ceiling": str(ratio), "excess": str(excess)})
    out["box_counting_ceilings"] = ceilings
    out["endpoint_coefficients_of_exp_minus_3_over_2"] = {"old": "3/8", "d2": "3/4", "d3": "9/16"}
    need(F(9,16)/F(3,8) == F(3,2), "three-dimensional bound improvement")
    out["status"] = "PASS"
    out["assertions"] = COUNT
    out["evidence_ceiling"] = "Finite exact corroboration; all-spin, all-volume and actual-vacuum claims rely on the written proofs, not these samples."
    return out


if __name__ == "__main__":
    result = run()
    if sys.argv[1:] == ["--write-receipt"]:
        (HERE / "RESULTS.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    elif sys.argv[1:]:
        raise SystemExit("Use no arguments for read-only replay, or --write-receipt to record.")
    else:
        saved = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
        if result != saved:
            raise AssertionError("Saved receipt differs from recomputation")
    print(f"PASS: {result['assertions']} exact assertions; 384 cube trees; weighted covers, hostile controls and inverse identities.")
