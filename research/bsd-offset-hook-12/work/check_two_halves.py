"""Exact complementary-gap and two-leg closure tests; no floating point."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


def affine_fiber(a, b, c, e):
    """All rational x satisfying c*(a*x+b)+e=x (total rational maps)."""
    coefficient, constant = c*a-1, c*b+e
    if coefficient:
        return {'kind': 'ONE', 'value': str(-constant/coefficient)}
    return {'kind': 'NONE'} if constant else {'kind': 'MANY', 'family': 'all rational x'}


def main():
    root = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', type=Path, default=root/'evidence/hooks.json')
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError('Use a new evidence path')
    data = json.loads(args.input.read_text(encoding='utf-8'))
    intervals, results = [], []
    for row in data['fresh_distance_rows']:
        low, high = map(F, row['distance'])
        width = high-low
        assert width > 0
        intervals.append((low, high))
        cases, unlabelled = [], {}
        for i in range(1, 8):
            t = F(i, 8)
            x = low+t*width
            left, right = x-low, high-x
            assert left+right == width
            assert left/width+right/width == 1
            assert low+left == high-right == x
            reflected = low+high-x
            assert reflected-low == right and high-reflected == left
            key = '|'.join(map(str, sorted((left/width, right/width))))
            unlabelled.setdefault(key, []).append(str(x))
            cases.append({'t': str(t), 'x': str(x), 'left_gap': str(left),
                          'right_gap': str(right), 'sum': str(width),
                          'readback': str(low+left), 'reflected_x': str(reflected)})
        assert len({c['x'] for c in cases}) == 7
        assert sorted(map(len, unlabelled.values())) == [1, 2, 2, 2]
        results.append({'depth': row['depth'], 'width': str(width),
                        'shape_only_fiber_on_test_carrier': {'kind': 'MANY', 'size': 7},
                        'cases': cases, 'unlabelled_pair_fibers': unlabelled})

    (l9, u9), (l10, u10) = intervals
    assert l9 < l10 < u10 < u9
    w9, w10 = u9-l9, u10-l10
    # Coordinate transfer, valid for the same x inside the smaller interval.
    slope, offset = w9/w10, (l9-l10)/w10
    transport = []
    for i in range(9):
        t10 = F(i, 8)
        x = l10+t10*w10
        t9 = (x-l9)/w9
        assert 0 <= t9 <= 1
        assert t10 == slope*t9+offset
        assert t9 == (t10-offset)/slope
        assert l9+t9*w9 == l10+t10*w10 == x
        transport.append({'x': str(x), 't9': str(t9), 't10': str(t10)})

    grid = [F(i, 2) for i in range(-4, 5)]
    affine_rows, counts = [], {'NONE': 0, 'ONE': 0, 'MANY': 0}
    for coeffs in product(range(-2, 3), repeat=4):
        a, b, c, e = map(F, coeffs)
        fiber = affine_fiber(a, b, c, e)
        counts[fiber['kind']] += 1
        actual = [x for x in grid if c*(a*x+b)+e == x]
        if fiber['kind'] == 'ONE':
            v = F(fiber['value'])
            assert c*(a*v+b)+e == v
            predicted = [v] if v in grid else []
        elif fiber['kind'] == 'MANY':
            predicted = grid
        else:
            predicted = []
        assert actual == predicted
        affine_rows.append({'a_b_c_e': list(coeffs), 'rational_fiber': fiber,
                            'finite_test_fiber': list(map(str, actual))})
    assert sum(counts.values()) == 625
    examples = []
    for name, coeffs in (
        ('two identity legs: every state closes', (1, 0, 1, 0)),
        ('complement followed by complement: every state closes', (-1, 1, -1, 1)),
        ('complement followed by halving: unique state 1/3', (-1, 1, F(1, 2), 0)),
        ('unit outward and imperfect return: no exact state', (1, 1, 1, F(-99, 100))),
    ):
        coeffs = tuple(map(F, coeffs))
        examples.append({'name': name, 'a_b_c_e': list(map(str, coeffs)),
                         'fiber': affine_fiber(*coeffs)})
    assert examples[2]['fiber'] == {'kind': 'ONE', 'value': '1/3'}
    assert examples[3]['fiber']['kind'] == 'NONE'
    result = {'status': 'COMPLEMENTARY_GAPS_AND_AFFINE_CLOSURE_VERIFIED',
              'created_utc': datetime.now(timezone.utc).isoformat(),
              'gap_models': results,
              'refinement_transfer': {'formula': 't10=slope*t9+offset',
                  'slope': str(slope), 'offset': str(offset),
                  'admitted_t9': [str((l10-l9)/w9), str((u10-l9)/w9)],
                  'cases': transport},
              'affine_total_rational_model': {'test_grid': list(map(str, grid)),
                  'coefficient_carrier': 'a,b,c,e each integer -2..2',
                  'fiber_kind_counts': counts, 'all_625_cases': affine_rows,
                  'examples': examples},
              'user_shape_rule': 'OPEN: these are two candidate interpretations',
              'BSD_multiplier': 'OPEN: neither model provides an analytic-to-height map',
              'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'input_sha256': sha256(args.input.read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'gap_cases': 14,
                      'refinement_readbacks': len(transport),
                      'affine_cases': sum(counts.values()), 'fiber_counts': counts,
                      'examples': examples}, indent=2))


if __name__ == '__main__':
    main()
