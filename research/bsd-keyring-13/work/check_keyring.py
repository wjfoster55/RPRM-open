"""Exact decimal-block and carry tests for the proposed three-plus-one keyring."""
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse
import json


def value(integer, middle, tail, w, m):
    return F(integer) + F(middle, 10**w) + F(tail, 10**(w+m))


def recover(x, w, m):
    scaled = x * 10**(w+m)
    assert scaled.denominator == 1 and scaled >= 0
    integer, rem = divmod(scaled.numerator, 10**(w+m))
    middle, tail = divmod(rem, 10**m)
    return integer, str(middle).zfill(w), str(tail).zfill(m)


def carry(integer, middle, tail, w, m):
    tail_carry, new_tail = divmod(tail, 10**m)
    integer_carry, new_middle = divmod(middle+tail_carry, 10**w)
    return (integer+integer_carry, new_middle, new_tail), (tail_carry, integer_carry)


def main():
    root = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', type=Path, default=root/'inputs/hooks12.json')
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError('Use a new evidence path')
    source = json.loads(args.input.read_text(encoding='utf-8'))
    rows = []
    for record in source['fresh_distance_rows']:
        words = record['distance_display12']
        assert all(s.startswith('2.0340') for s in words)
        tails = [s[len('2.0340'):] for s in words]
        assert all(len(t) == 8 for t in tails)
        bounds = [value(2, 340, int(t), 4, 8) for t in tails]
        assert bounds == list(map(F, record['distance']))
        for x, tail in zip(bounds, tails):
            assert recover(x, 4, 8) == (2, '0340', tail)
        rows.append({'depth': record['depth'], 'integer_block': '2.',
                     'middle_block': '0340', 'joint_tail_block': tails,
                     'widths': [4, 8], 'readback': list(map(str, bounds)),
                     'decimal_readback': words})

    # Complete finite topology fiber: all ordered two-digit tail pairs.
    intervals = set()
    for a in range(100):
        for b in range(a, 100):
            low, high = value(2, 340, a, 4, 2), value(2, 340, b, 4, 2)
            assert low <= high
            assert recover(low, 4, 2) == (2, '0340', str(a).zfill(2))
            assert recover(high, 4, 2) == (2, '0340', str(b).zfill(2))
            intervals.add((low, high))
    assert len(intervals) == 5050
    controls = [{'tails': [str(a).zfill(2), str(b).zfill(2)],
                 'interval': list(map(str, (value(2, 340, a, 4, 2), value(2, 340, b, 4, 2))))}
                for a, b in ((0, 1), (0, 2), (48, 71))]

    # One-carry input carrier: I=2, P=0..9, T=0..19, widths 1,1.
    # Normalized integer remains in {2,3}; both carry tags are retained.
    carry_rows = []
    for middle in range(10):
        for tail in range(20):
            original = (2, middle, tail)
            normalized, tags = carry(*original, 1, 1)
            assert value(*original, 1, 1) == value(*normalized, 1, 1)
            tc, ic = tags
            back = (normalized[0]-ic, normalized[1]+10*ic-tc, normalized[2]+10*tc)
            assert back == original
            carry_rows.append({'input': original, 'normalized': normalized, 'carry_tags': tags})
    assert len(carry_rows) == 200
    actual_boundary = []
    for original in ((2, 340, 10**8), (2, 9999, 10**8)):
        normalized, tags = carry(*original, 4, 8)
        assert value(*original, 4, 8) == value(*normalized, 4, 8)
        actual_boundary.append({'input': original, 'normalized': normalized, 'carry_tags': tags})

    r, radius = F(3, 4), F(3)
    # Exact symbolic geometric conditions; these inequalities do not replace
    # the spanning-disk written linking proof retained in the agent report.
    assert 0 < r < radius
    assert (2*r)**2 < 3*radius**2
    result = {'status': 'DECLARED_BLOCK_READBACK_AND_CARRY_VERIFIED',
              'created_utc': datetime.now(timezone.utc).isoformat(),
              'actual_height_input_replayed': False, 'attributed_interval_records': rows,
              'geometry_parameters': {'connector_radius': str(radius), 'satellite_radius': str(r),
                  'satellite_ball_center_distance_squared': str(3*radius**2),
                  'sum_of_ball_radii_squared': str((2*r)**2)},
              'topology_only_fiber': {'carrier': 'I=2,P=0340,w=4,m=2,0<=a<=b<100',
                  'kind': 'MANY', 'size': len(intervals), 'examples': controls},
              'carry_carrier': 'I=2,P=0..9,T=0..19,w=m=1, one carry buffer',
              'carry_cases': carry_rows, 'actual_width_boundary_controls': actual_boundary,
              'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'input_sha256': sha256(args.input.read_bytes()).hexdigest(),
              'claim_ceiling': 'Exact positional encoding and candidate topology; BSD loop maps OPEN'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status', 'attributed_interval_records', 'topology_only_fiber', 'actual_width_boundary_controls')}, indent=2))
    print('Carry cases: 200 exact readbacks')


if __name__ == '__main__':
    main()
