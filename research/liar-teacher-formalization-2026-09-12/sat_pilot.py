"""Bounded raw-CNF parity projection experiment; see SAT-PILOT.md."""
from collections import Counter
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import random
import sys

SEED = 20260912
ROOT = Path(__file__).resolve().parent


def variables(cnf):
    return {abs(lit) for clause in cnf for lit in clause}


def admit(blocks, boundary):
    if len(blocks) != 2 or len(set(boundary)) != len(boundary):
        raise ValueError("two blocks and distinct boundary IDs required")
    if any(type(v) is not int or v <= 0 for v in boundary):
        raise ValueError("boundary IDs must be positive integers")
    for cnf in blocks:
        if any(type(lit) is not int or lit == 0 for cl in cnf for lit in cl):
            raise ValueError("literals must be nonzero integers")
    if (variables(blocks[0]) & variables(blocks[1])) - set(boundary):
        raise ValueError("private scopes overlap")


def recognize(cnf, c):
    """Return equivalent XOR rows plus every unsupported normalized clause."""
    groups = {}
    for clause in cnf:
        c["input_clauses"] += 1
        c["input_literals"] += len(clause)
        seen = set()
        tautology = False
        for lit in clause:
            if type(lit) is not int or lit == 0:
                raise ValueError("invalid literal")
            c["normalization_set_probes"] += 2
            tautology |= -lit in seen
            seen.add(lit)
        if tautology:
            c["tautologies_dropped"] += 1
            continue
        c["normalization_sort_items"] += len(seen)
        normalized = tuple(sorted(seen, key=abs))
        support = tuple(map(abs, normalized))
        group = groups.setdefault(support, set())
        c["clause_set_probes"] += 2
        c["duplicate_clauses"] += normalized in group
        group.add(normalized)
    rows, residual = [], []
    for support, clauses in sorted(groups.items()):
        c["support_groups"] += 1
        parity = set()
        for clause in clauses:
            c["distinct_clause_parity_literal_visits"] += len(clause)
            parity.add(sum(lit < 0 for lit in clause) % 2)
        if support and len(clauses) == 1 << (len(support) - 1) and len(parity) == 1:
            mask = 0
            for v in support:
                c["mask_build_visits"] += 1
                mask |= 1 << (v - 1)
            rows.append((mask, 1 ^ next(iter(parity))))
            c["recognized_rows"] += 1
        else:
            residual.extend(sorted(clauses))
            c["residual_groups"] += 1
            c["residual_clauses"] += len(clauses)
    return rows, residual


def eliminate(rows, columns, c):
    """RREF on specified columns only; preserve the full row relation."""
    rows = list(rows)
    rank = 0
    for v in columns:
        bit = 1 << (v - 1)
        pivot = None
        for i in range(rank, len(rows)):
            c["coefficient_tests"] += 1
            if rows[i][0] & bit:
                pivot = i
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        mask, rhs = rows[rank]
        c["pivot_rows"] += 1
        for i, (other, value) in enumerate(rows):
            if i == rank:
                continue
            c["coefficient_tests"] += 1
            if other & bit:
                c["row_xors"] += 1
                c["xor_bit_spans"] += max(other.bit_length(), mask.bit_length()) + 1
                rows[i] = other ^ mask, value ^ rhs
        rank += 1
    return rows


def compact(rows):
    if (0, 1) in rows:
        return [(0, 1)]
    return sorted(set(row for row in rows if row != (0, 0)))


def project(rows, private, boundary, c):
    reduced = eliminate(rows, sorted(private), c)
    private_mask = sum(1 << (v - 1) for v in private)
    c["projection_row_tests"] += len(reduced)
    retained = [row for row in reduced if not row[0] & private_mask]
    c["private_free_rows_before_reduction"] += len(retained)
    return compact(eliminate(retained, boundary, c))


def algebra(blocks, boundary, panel):
    admit(blocks, boundary)
    recognition, work = Counter(), Counter()
    converted = [recognize(block, recognition) for block in blocks]
    if any(residual for _, residual in converted):
        return {"status": "UNRECOGNIZED", "recognition": dict(recognition)}
    rows = [part[0] for part in converted]
    if panel:
        messages = [project(row, variables(block) - set(boundary), boundary, work)
                    for row, block in zip(rows, blocks)]
        joined = compact(eliminate(messages[0] + messages[1], boundary, work))
        # Payload bit counts use dense boundary coordinates, not global IDs.
        payload = sum(len(message) * (len(boundary) + 1) for message in messages)
    else:
        messages, payload = None, None
        joined = compact(eliminate(rows[0] + rows[1],
                                   sorted(variables(blocks[0] + blocks[1])), work))
    return {"status": "SAT" if (0, 1) not in joined else "UNSAT",
            "recognition": dict(recognition), "gf2": dict(work),
            "messages": messages, "joined_boundary_rows": joined if panel else None,
            "dense_boundary_coefficient_bits_estimate": payload,
            "stored_message_mask_bit_spans": (sum(mask.bit_length() + 1
                for message in messages for mask, _ in message) if panel else None),
            "boundary_mapping_entries": len(boundary) if panel else None}


def dpll(cnf, assignment, c):
    """One engine used for whole-CNF and each point-boundary query."""
    c["recursive_calls"] += 1
    assignment = dict(assignment)
    while True:
        choice, unit = None, None
        for clause in cnf:
            c["clause_visits"] += 1
            missing, satisfied = [], False
            for lit in clause:
                c["literal_visits"] += 1
                value = assignment.get(abs(lit))
                if value is None:
                    missing.append(lit)
                elif value == (lit > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not missing:
                c["conflicts"] += 1
                return False
            if len(missing) == 1:
                unit = missing[0]
                break
            if choice is None:
                choice = abs(missing[0])
        if unit is not None:
            assignment[abs(unit)] = unit > 0
            c["unit_assignments"] += 1
            continue
        if choice is None:
            return True
        c["decisions"] += 1
        return any(dpll(cnf, assignment | {choice: bit}, c)
                   for bit in (False, True))


def raw_projection(cnf, boundary, c):
    """Independent oracle: full truth table of signed raw clauses."""
    scope = sorted(variables(cnf) | set(boundary))
    relation = set()
    for bits in product((False, True), repeat=len(scope)):
        c["complete_assignments"] += 1
        values = dict(zip(scope, bits))
        valid = True
        for clause in cnf:
            c["clause_checks"] += 1
            satisfied = False
            for lit in clause:
                c["literal_checks"] += 1
                if (lit > 0 and values[abs(lit)]) or (lit < 0 and not values[abs(lit)]):
                    satisfied = True
                    break
            if not satisfied:
                valid = False
                break
        if valid:
            relation.add(tuple(values[v] for v in boundary))
    return relation


def row_projection(rows, boundary):
    # Evaluate decoded equations directly at every boundary point.
    return {bits for bits in product((False, True), repeat=len(boundary))
            if all(sum(bit for v, bit in zip(boundary, bits)
                       if mask & (1 << (v - 1))) % 2 == rhs for mask, rhs in rows)}


def xor_cnf(support, rhs):
    return [tuple(-v if bit else v for v, bit in zip(support, bits))
            for bits in product((0, 1), repeat=len(support)) if sum(bits) % 2 != rhs]


def chain(boundary, start, rhs):
    clauses, head = [], boundary[0]
    for offset, v in enumerate(boundary[1:-2]):
        auxiliary = start + offset
        clauses.extend(xor_cnf((head, v, auxiliary), 0))
        head = auxiliary
    return clauses + xor_cnf((head, boundary[-2], boundary[-1]), rhs)


def fixture(b, rhs, transformed=False):
    boundary = list(range(1, b + 1))
    blocks = [chain(boundary, b + 1, 0), chain(boundary, 2 * b - 2, rhs)]
    if transformed:
        rng = random.Random(SEED + 100 * b + rhs)
        old = sorted(variables(blocks[0] + blocks[1]))
        new = old[:]
        rng.shuffle(new)
        mapping = dict(zip(old, new))
        flips = {v: rng.choice((-1, 1)) for v in old}
        flips[old[0]] = -1  # Every transformed case includes a complement.
        boundary = sorted(mapping[v] for v in boundary)
        blocks = [[[mapping[abs(lit)] * (1 if lit > 0 else -1) * flips[abs(lit)]
                    for lit in clause] for clause in block] for block in blocks]
        for block in blocks:
            for clause in block:
                rng.shuffle(clause)
            rng.shuffle(block)
    return blocks, boundary


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def check_case(name, blocks, boundary, finite=True):
    admit(blocks, boundary)
    panel, whole = algebra(blocks, boundary, True), algebra(blocks, boundary, False)
    result = {"name": name, "boundary_width": len(boundary),
              "raw_clauses": sum(map(len, blocks)),
              "raw_literals": sum(len(cl) for block in blocks for cl in block),
              "variables": len(variables(blocks[0] + blocks[1])),
              "input_sha256": digest([blocks, boundary]), "panel": panel,
              "whole_system_gaussian": whole, "independent_oracle": finite}
    assert panel["recognition"] == whole["recognition"], name
    if not finite:
        assert panel["status"] == whole["status"] != "UNRECOGNIZED", name
        result["validation"] = "dependent algebra agreement only; no exhaustive oracle"
        return result
    oracle_work, dpll_work, point_work = Counter(), Counter(), Counter()
    relations = [raw_projection(block, boundary, oracle_work) for block in blocks]
    expected = "SAT" if relations[0] & relations[1] else "UNSAT"
    direct = "SAT" if dpll(blocks[0] + blocks[1], {}, dpll_work) else "UNSAT"
    points = [set(), set()]
    for bits in product((False, True), repeat=len(boundary)):
        for i, block in enumerate(blocks):
            point_work["boundary_queries"] += 1
            if dpll(block, dict(zip(boundary, bits)), point_work):
                points[i].add(bits)
    assert points == relations and direct == expected, name
    if panel["status"] != "UNRECOGNIZED":
        projected = [row_projection(rows, boundary) for rows in panel["messages"]]
        assert projected == relations, name
        assert row_projection(panel["joined_boundary_rows"], boundary) == relations[0] & relations[1], name
        assert panel["status"] == whole["status"] == expected, name
    else:
        assert whole["status"] == "UNRECOGNIZED", name
    result.update(oracle_status=expected, oracle_work=dict(oracle_work),
                  projection_sizes=list(map(len, relations)),
                  projection_sha256=[digest(sorted(rel)) for rel in relations],
                  join_size=len(relations[0] & relations[1]),
                  whole_cnf_dpll={"status": direct, "work": dict(dpll_work)},
                  point_boundary={"status": expected, "work": dict(point_work),
                                  "point_messages": sum(map(len, points))},
                  boundary_memberships_checked=2 * (1 << len(boundary)))
    return result


def guards():
    checked = 0
    for k in (1, 2, 3):
        support = tuple(range(1, k + 1))
        clauses = xor_cnf(support, 0) + xor_cnf(support, 1)
        for include in product((False, True), repeat=len(clauses)):
            cnf = [cl for cl, keep in zip(clauses, include) if keep]
            rows, residual = recognize(cnf, Counter())
            expected_recognition = not cnf or (len(cnf) == 1 << (k - 1) and
                len({sum(lit < 0 for lit in cl) % 2 for cl in cnf}) == 1)
            assert (not residual) == expected_recognition
            if not residual:
                assert row_projection(rows, support) == raw_projection(cnf, support, Counter())
            checked += 1
    base = xor_cnf((1, 2, 3), 0)
    assert not recognize(base + [base[0]], Counter())[1]
    assert recognize(base[:-1] + [base[0]], Counter())[1]
    normalized = [tuple(cl) + (cl[0],) for cl in base] + [(1, -1)]
    assert recognize(normalized, Counter())[0] == recognize(base, Counter())[0]
    assert recognize([()], Counter())[1] == [()]
    assert not dpll([()], {}, Counter()) and dpll([], {}, Counter())
    # Affine but syntactically unrecognized (empty relation from both parities).
    assert algebra([base + xor_cnf((1, 2, 3), 1), []], [1, 2, 3], True)["status"] == "UNRECOGNIZED"
    try:
        admit([[(1, 3)], [(2, 3)]], [1, 2])
    except ValueError:
        pass
    else:
        raise AssertionError("shared private variable admitted")
    equations = [[], [((3,), 0)], [((1, 3), 0)],
                 [((1, 3), 0), ((2, 3), 1)],
                 [((1,), 0), ((2,), 1)],
                 [((1, 2), 0), ((2, 3), 0), ((1, 3), 1)]]
    rng = random.Random(SEED)
    supports = [s for k in (1, 2, 3) for s in combinations(range(1, 6), k)]
    for _ in range(32):
        equations.append([(s, rng.randrange(2)) for s in rng.sample(supports, 6)])
    for system in equations:
        cnf = [cl for support, rhs in system for cl in xor_cnf(support, rhs)]
        rows, residual = recognize(cnf, Counter())
        assert not residual
        projected = project(rows, variables(cnf) - {1, 2}, [1, 2], Counter())
        assert row_projection(projected, [1, 2]) == raw_projection(cnf, [1, 2], Counter())
    # Private-only contradictory rows exercise elimination independently of recognition.
    assert project([(4, 0), (4, 1)], {3}, [1, 2], Counter()) == [(0, 1)]
    return {"single_support_truth_tables": checked, "affine_projection_systems": len(equations),
            "missing_duplicate_normalization_empty_and_scope_guards": "PASS"}


def main():
    results = {"specification": "SAT-PILOT.md frozen specification",
               "seed": SEED, "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "evidence_grade": "finite tests; no general SAT complexity claim", "failures": []}
    try:
        results["guards"] = guards()
        results["finite_cases"] = [check_case(f"b{b}_right{rhs}_{variant}",
            *fixture(b, rhs, variant == "transformed"))
            for b in range(3, 9) for rhs in (0, 1) for variant in ("identity", "transformed")]
        assert all(case["panel"]["status"] != "UNRECOGNIZED" for case in results["finite_cases"])
        controls = [
            ("OR3_vs_000", [[(1, 2, 3)], [(-1,), (-2,), (-3,)]]),
            ("exactly_one_vs_111", [[(1, 2, 3), (-1, -2), (-1, -3), (-2, -3)],
                                     [(1,), (2,), (3,)]])]
        results["non_affine_controls"] = [check_case(name, blocks, [1, 2, 3]) for name, blocks in controls]
        assert all(case["panel"]["status"] == "UNRECOGNIZED" and case["oracle_status"] == "UNSAT"
                   for case in results["non_affine_controls"])
        results["scaling_cases"] = [check_case(f"b{b}_right{rhs}_algebra_only", *fixture(b, rhs), finite=False)
                                    for b in (16, 32, 64, 128) for rhs in (0, 1)]
        results["status"] = "PASS"
    except Exception as exc:
        results["status"] = "FAIL"
        results["failures"].append({"type": type(exc).__name__, "message": str(exc)})
        raise
    finally:
        (ROOT / "SAT-RESULTS.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {len(results['finite_cases'])} exhaustive cases, 2 non-affine controls, "
          f"{results['guards']['single_support_truth_tables']} recognizer truth tables, "
          f"{results['guards']['affine_projection_systems']} projection systems, 8 algebra-only cases")


if __name__ == "__main__":
    if not __debug__:
        sys.exit("Assertions must be enabled; do not use python -O")
    main()
