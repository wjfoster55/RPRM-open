#!/usr/bin/env python3
"""Exact, exposed development checks for one proposed RPRM bridge.

Standard library only. Does not run or replace historical RPRM verifiers.
All input law tables and expected controls are development data, not holdouts.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
import sys
from fractions import Fraction
from typing import Callable, Sequence

ROOT = Path(__file__).resolve().parent
LOW = tuple(range(7))  # n=3, masks of degree <=2; bit0=h, bit1=x, bit2=y.


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def coeffs(table: Sequence) -> tuple:
    """Direct signed submask transform, exact on integer/rational entries."""
    require(len(table) == 8, 'This development carrier has exactly eight sites.')
    return tuple(sum(((-1) ** ((s.bit_count()-t.bit_count()))) * table[t]
                     for t in range(8) if t & s == t) for s in range(8))


def values(c: Sequence) -> tuple:
    """Independent evaluation formula, no transform inversion routine."""
    require(len(c) == 8, 'Eight coefficients required.')
    return tuple(sum(c[t] for t in range(8) if t & s == t)
                 for s in range(8))


def compact(table: Sequence) -> tuple:
    return coeffs(table)[:7]


def compact_product(a: Sequence, b: Sequence) -> tuple:
    """Multiply modulo x_i**2=x_i and discard degrees >2.

    Neither input contains the omitted coefficient or original table.
    """
    require(len(a) == len(b) == 7, 'Seven retained coefficients required.')
    out = [0] * 7
    for i in LOW:
        for j in LOW:
            union = i | j
            if union < 7:
                out[union] += a[i] * b[j]
    return tuple(out)


def pullback(table: Sequence, mapping: Sequence[int]) -> tuple:
    require(len(mapping) == 8 and all(type(x) is int and 0 <= x < 8 for x in mapping),
            'Input map must map the eight-site carrier into itself.')
    return tuple(table[mapping[s]] for s in range(8))


def input_maps() -> dict[str, tuple[int, ...]]:
    result = {'identity': tuple(range(8))}
    for i, label in enumerate(('h', 'x', 'y')):
        result[f'clamp_{label}_0'] = tuple(s & ~(1 << i) for s in range(8))
        result[f'clamp_{label}_1'] = tuple(s | (1 << i) for s in range(8))
        result[f'flip_{label}'] = tuple(s ^ (1 << i) for s in range(8))
    for perm in itertools.permutations(range(3)):
        result['perm_' + ''.join(map(str, perm))] = tuple(
            sum(((s >> perm[j]) & 1) << j for j in range(3)) for s in range(8))
    return result


def closure(start: set[int], maps: Sequence[Sequence[int]]) -> set[int]:
    reached = set(start)
    while True:
        nxt = reached | {m[s] for m in maps for s in reached}
        if nxt == reached:
            return reached
        reached = nxt


def graph_summary(vertices: set[str], edges: set[frozenset[str]],
                  swap: dict[str, str]) -> tuple[int, int, int]:
    require(set(swap) == vertices and set(swap.values()) == vertices, 'Bad graph action.')
    require(all(swap[swap[v]] == v for v in vertices), 'Action not an involution.')
    require(all(frozenset(swap[v] for v in e) in edges for e in edges),
            'Action does not preserve edges.')
    vorbits = {frozenset((v, swap[v])) for v in vertices}
    eorbits = {frozenset((e, frozenset(swap[v] for v in e))) for e in edges}
    inverted = sum(1 for e in edges
                   if frozenset(swap[v] for v in e) == e and all(swap[v] != v for v in e))
    return len(vorbits), len(eorbits), inverted


def run_cases() -> list[dict]:
    laws = list(itertools.product((0, 1), repeat=8))
    summaries = [compact(f) for f in laws]
    pairs: dict[tuple, list[tuple]] = {}
    for f, c in zip(laws, summaries):
        pairs.setdefault(c, []).append(f)
    rows: list[dict] = []

    def case(name: str, run: Callable[[], dict]) -> None:
        try:
            rows.append({'case_id': name, 'outcome': 'PASS', 'data': run()})
        except Exception as exc:
            rows.append({'case_id': name, 'outcome': 'FAIL',
                         'data': {'exception': type(exc).__name__, 'message': str(exc)}})

    def roundtrip() -> dict:
        for f in laws:
            require(values(coeffs(f)) == f, 'Boolean-table round trip failed.')
        for seed in range(32):
            f = tuple(Fraction((seed+3)*(i+1)-17, i+2) for i in range(8))
            require(values(coeffs(f)) == f, 'Rational-table round trip failed.')
        return {'complete_boolean_tables': len(laws), 'structured_rational_tables': 32}
    case('CB01_ROUNDTRIP', roundtrip)

    def fibers() -> dict:
        require(len(pairs) == 128, 'Unexpected fiber count.')
        for siblings in pairs.values():
            require(len(siblings) == 2, 'Unexpected fiber size.')
            require(siblings[0][:7] == siblings[1][:7] and siblings[0][7] != siblings[1][7],
                    'Wrong missing direction.')
        return {'summary_fibers': 128, 'members_per_fiber': 2,
                'unresolved_site_mask': 7}
    case('CB02_FIBERS', fibers)

    def arithmetic() -> dict:
        for i, f in enumerate(laws):
            for j, g in enumerate(laws):
                a, b = summaries[i], summaries[j]
                require(tuple(x+y for x, y in zip(a, b)) == compact(tuple(x+y for x, y in zip(f, g))),
                        'Summary addition failed.')
                require(compact_product(a, b) == compact(tuple(x*y for x, y in zip(f, g))),
                        'Summary multiplication failed.')
        return {'ordered_law_pairs': len(laws)**2,
                'operations': ['pointwise_addition', 'pointwise_multiplication'],
                'full_table_access_in_compact_operators': False}
    case('CB03_ARITHMETIC', arithmetic)

    def adapter() -> dict:
        for r in range(5):
            for h, x, y in itertools.product((0, 1), repeat=3):
                d = 5*h+r
                lhs = ((d+5) % 10, x, y)
                rhs = (5*(1-h)+r, x, y)
                require(lhs == rhs, 'Finite fiving/cube adapter does not commute.')
        return {'residue_slices': 5, 'adapter_cases': 40,
                'adapter': 'A_r(h,x,y)=(5*h+r,x,y)',
                'scope': 'finite display; not the strong winding state or Double-Stamp safety'}
    case('CB04_FIVING_ADAPTER', adapter)

    def winding() -> dict:
        checked = 0
        for w, h, r in itertools.product(range(-3, 4), (0, 1), range(5)):
            n = 10*w+5*h+r
            w1, h1, r1 = w+h, 1-h, r
            require(10*w1+5*h1+r1 == n+5, 'Strong plus-five encoding failed.')
            w2, h2 = w1+h1, 1-h1
            require((w2, h2, r1) == (w+1, h, r), 'Two fivings erased winding.')
            wi, hi = w1-(1-h1), 1-h1
            require((wi, hi, r1) == (w, h, r), 'Strong inverse failed.')
            checked += 1
        return {'lifted_states_checked': checked, 'two_steps': '(w,h,r)->(w+1,h,r)',
                'finite_return_is_strong_return': False}
    case('CB05_WINDING', winding)

    def collision() -> dict:
        f0 = tuple(s.bit_count() for s in range(8))
        f1 = tuple(s.bit_count() + int(s == 7) for s in range(8))
        flip = tuple(s ^ 1 for s in range(8))
        require(compact(f0) == compact(f1), 'Witness did not collide before fiving.')
        out0, out1 = pullback(f0, flip), pullback(f1, flip)
        require(compact(out0) != compact(out1), 'Witness did not separate after fiving.')
        require((f0[6], f1[6], out0[6], out1[6]) == (2, 2, 3, 4), 'Wrong concrete readouts.')
        delta = tuple(a-b for a, b in zip(coeffs(out1), coeffs(out0)))
        require(delta == (0,0,0,0,0,0,1,-1), 'Wrong transformed hidden term.')
        return {'same_present_readout': [2, 2], 'after_fiving_readout': [3, 4],
                'hidden_term': 'h*x*y', 'after_pullback': 'x*y-h*x*y',
                'verdict_on_C2_fiving_lift': 'REFUTED',
                'this_expected_refutation_is_a_successful_test': True}
    case('CB06_OPERATION_COLLISION', collision)

    def maps_test() -> dict:
        out = {}
        for name, m in input_maps().items():
            domain_condition = all(m[s] in LOW for s in LOW)
            observed = all(compact(pullback(fs[0], m)) == compact(pullback(fs[1], m))
                           for fs in pairs.values())
            require(observed == domain_condition, f'Closure criterion failed for {name}.')
            out[name] = 'LIFTS' if observed else 'DOES_NOT_LIFT'
        return {'all_same_summary_pairs_checked_per_map': len(pairs), 'map_verdicts': out}
    case('CB07_MAP_CLASSIFICATION', maps_test)

    def repaired() -> dict:
        maps = input_maps()
        for f in laws:
            stored = coeffs(f)
            for m in maps.values():
                # Reconstruct using stored coefficients, never the original law inside this branch.
                candidate = coeffs(tuple(sum(stored[t] for t in range(8) if t & m[s] == t)
                                         for s in range(8)))
                reference = coeffs(pullback(f, m))
                require(candidate == reference, 'Full-coefficient repair failed.')
        return {'laws': len(laws), 'maps': len(maps), 'law_map_pairs': len(laws)*len(maps),
                'repair': 'retain the missing coefficient (equivalently the missing site value)',
                'runtime_advantage_claimed': False}
    case('CB08_REPAIR', repaired)

    def minimality() -> dict:
        start = set(LOW)
        flip = tuple(s ^ 1 for s in range(8))
        reached = closure(start, [flip])
        require(reached == set(range(8)), 'Wrong reachable retained domain.')
        candidates = []
        for bits in itertools.product((0,1), repeat=8):
            subset = {s for s, b in enumerate(bits) if b}
            if start <= subset and all(flip[s] in subset for s in subset):
                candidates.append(subset)
        require(candidates == [set(range(8))], 'Repair not minimal among retained-site supersets.')
        return {'subsets_examined': 256, 'closed_supersets': 1,
                'initial_sites': 7, 'least_operation_closed_sites': 8,
                'scope': 'all arbitrary laws on this carrier; retained-site summary family'}
    case('CB09_MINIMAL_REPAIR', minimality)

    def probes() -> dict:
        for fs in pairs.values():
            for s in LOW:
                require(fs[0][s] == fs[1][s], 'Previously retained probe unexpectedly separates.')
            require(fs[0][7] != fs[1][7], 'New probe fails to separate.')
        repaired_keys = {(compact(f), f[7]) for f in laws}
        require(len(repaired_keys) == len(laws), 'Augmented observation not injective.')
        return {'redundant_probes_per_fiber': 7, 'distinguishing_site_mask': 7,
                'repaired_distinct_boolean_laws': len(repaired_keys)}
    case('CB10_DISTINGUISHING_PROBE', probes)

    def dwell_graphs() -> dict:
        def edge(a, b): return frozenset((a,b))
        leaves = {'a','b','c','d'}
        sigma = {'a':'c','c':'a','b':'d','d':'b'}
        A = graph_summary(leaves|{'o'}, {edge('o', v) for v in leaves}, sigma|{'o':'o'})
        stem = {edge('u','a'),edge('u','b'),edge('v','c'),edge('v','d')}
        B = graph_summary(leaves|{'u','v'}, stem|{edge('u','v')}, sigma|{'u':'v','v':'u'})
        C = graph_summary(leaves|{'u','v','m'}, stem|{edge('u','m'),edge('m','v')},
                          sigma|{'u':'v','v':'u','m':'m'})
        require((A,B,C) == ((3,2,0),(3,3,1),(4,3,0)), 'Double-Stamp structural counts disagree.')
        # Dwell permissions are the donor's declared process semantics, NOT inferred physical safety.
        admitted_dwell = {'A5': True, 'B6': False, 'C7': True}
        require(A[0] == B[0] and admitted_dwell['A5'] != admitted_dwell['B6'],
                'Enabledness collision absent.')
        return {'quotient_vertices_edges_inversions': {'A5': A, 'B6': B, 'C7': C},
                'declared_dwell_permissions': admitted_dwell,
                'vertex_count_only_summary': 'REFUTED_FOR_DWELL',
                'source_verifier_replayed': False,
                'safety_is': 'authored process admission, not a physical safety result'}
    case('CB11_ENABLEDNESS', dwell_graphs)
    return rows


def validate(rows: list[dict], required: list[str]) -> None:
    require(len(set(required)) == len(required), 'Duplicate required protocol IDs.')
    require(all(isinstance(row, dict) and isinstance(row.get('case_id'), str)
                and row.get('outcome') in ('PASS','FAIL') and isinstance(row.get('data'), dict)
                for row in rows), 'Malformed result schema.')
    ids = [row['case_id'] for row in rows]
    require(len(ids) == len(set(ids)), 'Duplicate emitted case IDs.')
    require(set(ids) == set(required), f'Coverage mismatch: missing={set(required)-set(ids)}, extra={set(ids)-set(required)}')
    require(all(row['outcome'] == 'PASS' for row in rows), 'At least one check failed.')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='New JSON path; no overwrite.')
    parser.add_argument('--control', choices=('none','omit','duplicate','unexpected','reorder'), default='none',
                        help='Actual emitted-row mutation used to test the aggregate coverage validator.')
    args = parser.parse_args()
    require(not args.output.exists(), 'Output already exists; use a fresh name.')
    protocol_bytes = (ROOT/'PROTOCOL.json').read_bytes()
    protocol = json.loads(protocol_bytes)
    rows = run_cases()
    if args.control == 'omit': rows = rows[:-1]
    elif args.control == 'duplicate': rows[-1] = rows[0].copy()
    elif args.control == 'unexpected': rows[-1] = rows[-1] | {'case_id':'UNDECLARED'}
    elif args.control == 'reorder': rows.reverse()
    error = None
    try:
        validate(rows, protocol['required_case_ids'])
    except ValueError as exc:
        error = str(exc)
    report = {'evidence_class': 'ASSISTANT_OR_LOCAL_DEVELOPMENT_CHECK_NOT_HOLDOUT',
              'status': 'FAIL' if error else 'PASS', 'coverage_error': error,
              'control': args.control, 'python': sys.version, 'platform': platform.platform(),
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'protocol_sha256': hashlib.sha256(protocol_bytes).hexdigest(),
              'historical_RPRM_verifiers_rerun': False, 'results': rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write('\n')
    print(json.dumps({'status':report['status'], 'control':args.control,
                      'emitted_cases':len(rows), 'output':str(args.output), 'error':error}))
    return 2 if error else 0


if __name__ == '__main__':
    raise SystemExit(main())
