#!/usr/bin/env python3
"""Independent, bounded review checks; does NOT import the unprovided Cursor prototype."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile


def require(condition: bool, explanation: str) -> None:
    if not condition:
        raise AssertionError(explanation)


def polynomial_coefficients(table: tuple[int, ...]) -> tuple[int, ...]:
    """Successive finite differences, not the starter's explicit submask sum."""
    require(len(table) == 8, "Eight cube sites required")
    work = list(table)
    for axis in (1, 2, 4):
        for site in range(8):
            if site & axis:
                work[site] -= work[site ^ axis]
    return tuple(work)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--returned', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output exists; choose a fresh output file.')
    rows = []

    def record(case_id: str, check):
        try:
            details = check()
            rows.append({'case_id': case_id, 'status': 'PASS', 'details': details})
        except Exception as exc:
            rows.append({'case_id': case_id, 'status': 'FAIL', 'error': f'{type(exc).__name__}: {exc}'})

    def counterexample():
        first = tuple(s.bit_count() for s in range(8))
        second = tuple(s.bit_count() + (s == 7) for s in range(8))
        low = lambda t: polynomial_coefficients(t)[:7]
        require(low(first) == low(second), 'Initial summaries must agree')
        f1, f2 = tuple(first[s ^ 1] for s in range(8)), tuple(second[s ^ 1] for s in range(8))
        require(low(f1) != low(f2), 'Fixed-receiver flip must expose hidden information')
        require((first[6], second[6], f1[6], f2[6]) == (2, 2, 3, 4), 'Concrete readout mismatch')
        return {'before': [2, 2], 'after': [3, 4]}
    record('RV01_CONCRETE_OPERATION_WITNESS', counterexample)

    def composed_arithmetic():
        h = tuple(s & 1 for s in range(8))
        x = tuple((s >> 1) & 1 for s in range(8))
        y = tuple((s >> 2) & 1 for s in range(8))
        hx = tuple(a*b for a,b in zip(h,x))
        p = tuple(a*b for a,b in zip(hx,y))
        require(polynomial_coefficients(hx)[3] == 1, 'h*x must contain a degree-two term')
        require(polynomial_coefficients(p) == (0,0,0,0,0,0,0,1), 'Product must be hxy')
        require(polynomial_coefficients(p)[:7] == (0,)*7, 'Hot product equals zero summary')
        flipped = tuple(p[s ^ 1] for s in range(8))
        require(polynomial_coefficients(flipped) == (0,0,0,0,0,0,1,-1), 'Hidden term must enter degree two')
        require(flipped[6] == 1, 'After flip, (0,1,1) reads 1')
        return {'chain': '(h*x)*y', 'hot_summary': [0]*7,
                'full_product_coefficients': list(polynomial_coefficients(p)),
                'flipped_product_coefficients': list(polynomial_coefficients(flipped)),
                'affine_class_not_closed_under_multiplication': True,
                'scope': 'Mathematical regression specification; no claim about unprovided implementation.'}
    record('RV02_COMPOSITION_AND_CLASS_ESCAPE', composed_arithmetic)

    def output_fibers():
        laws = list(itertools.product((0,1), repeat=8))
        fibers = {}
        for f in laws:
            fibers.setdefault(polynomial_coefficients(f)[:7], []).append(f)
        require(len(fibers) == 128 and all(len(v) == 2 for v in fibers.values()), 'Wrong Boolean source fibers')
        zero = (0,)*8
        spike = (0,)*7 + (1,)
        independent_sums = {tuple(a+b for a,b in zip(f,g)) for f,g in itertools.product((zero,spike), repeat=2)}
        correlated_sums = {tuple(2*a for a in f) for f in (zero,spike)}
        require(len(independent_sums) == 3 and len(correlated_sums) == 2, 'Incorrect sum-family cardinality')
        require({polynomial_coefficients(f)[:7] for f in independent_sums} == {(0,)*7}, 'Output hot summary not unique')
        require(any(2 in f for f in independent_sums), 'Boolean inputs must be allowed to leave the Boolean-valued family under Q addition')
        return {'original_Boolean_source_fibers':128, 'members_each':2,
                'independent_input_sum_possible_full_outputs':3,
                'same_source_added_to_itself_possible_full_outputs':2,
                'hot_output_summaries':1,
                'lesson':'Exact query/summary output does not imply a unique underlying object; source correlation and output carrier matter.'}
    record('RV03_QUERY_VERSUS_OBJECT_FIBERS', output_fibers)

    def id_checker_scope():
        script = args.returned / 'check_ids.py'
        payload = json.loads((args.returned / 'CONCEPT_REGISTER.json').read_text())
        require(len(payload['entries']) == 13, 'Expected current 13 IDs')
        with tempfile.TemporaryDirectory(prefix='rcf01-review-') as temp:
            root=Path(temp)
            (root/'check_ids.py').write_bytes(script.read_bytes())
            # This is intentionally destructive only to a throwaway copy.
            skeletal = {'entries':[{'id':e['id']} for e in payload['entries']]}
            (root/'CONCEPT_REGISTER.json').write_text(json.dumps(skeletal))
            result = subprocess.run([sys.executable,'-B',str(root/'check_ids.py')],capture_output=True,text=True,timeout=10)
            require(result.returncode == 0, 'Checker scope changed: inspect rather than assert an obsolete limitation')
        return {'ID_only_copy_checker_exit': result.returncode,
                'interpretation':'Checker checks ID coverage, not meaning/source/artifact survival. This is a limitation, not evidence that current entries lost meaning.'}
    record('RV04_ID_ONLY_CHECKER_SCOPE', id_checker_scope)

    report={'evidence_class':'INDEPENDENT_ASSISTANT_REVIEW_OF_AVAILABLE_MATH_AND_CHECKER',
            'cursor_prototype_executed':False,'historical_donors_executed':False,
            'python':sys.version,'platform':platform.platform(),
            'review_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'status':'PASS' if all(row['status']=='PASS' for row in rows) else 'FAIL',
            'checks':rows}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x',encoding='utf-8') as file:
        json.dump(report,file,indent=2); file.write('\n')
    print(json.dumps({'status':report['status'],'checks':len(rows),'output':str(args.output)}))
    return 0 if report['status']=='PASS' else 1

if __name__=='__main__':
    raise SystemExit(main())
