"""Small exact checks of recovered cube mathematics and a photon calibration.

This does not run the archive's historical suites and is not a Yang-Mills
simulation. The photon examples use dimensionless energy units with c = 1.
"""
from itertools import product
from pathlib import Path
import json
import sympy as sp

# Reconstruct the explicitly stated ternary second-difference checks.
points = list(product((-1, 0, 1), repeat=3))
index = {point: i for i, point in enumerate(points)}
rows, center_rows = [], []
for c in points:
    for d in points:
        if d == (0, 0, 0):
            continue
        # d and -d denote the same unoriented line.
        if next(value for value in d if value != 0) < 0:
            continue
        left = tuple(a-b for a, b in zip(c, d))
        right = tuple(a+b for a, b in zip(c, d))
        if left not in index or right not in index:
            continue
        row = [0] * len(points)
        row[index[left]], row[index[c]], row[index[right]] = 1, -2, 1
        rows.append(row)
        if c == (0, 0, 0):
            center_rows.append(row)
full, center = sp.Matrix(rows), sp.Matrix(center_rows)
counterfeit = sp.zeros(len(points), 1)
counterfeit[index[(-1, -1, -1)]] = -1
counterfeit[index[(1, 1, 1)]] = 1
assert center * counterfeit == sp.zeros(len(center_rows), 1)
failed_full_checks = sum(v != 0 for v in full * counterfeit)

# A Boolean cube of two photon energies and their relative orientation.
# a,b=0/1 select photon energies 1/2. d=0/1 selects parallel/antiparallel.
# M^2 = (E1+E2)^2 - |p1+p2|^2 = 4*d*(1+a)*(1+b).
addresses = list(product((0, 1), repeat=3))
values = {}
for a, b, d in addresses:
    E1, E2 = 1 + a, 1 + b
    p1, p2 = E1, E2 * (1 - 2*d)
    values[(a, b, d)] = (E1 + E2)**2 - (p1 + p2)**2
    assert values[(a, b, d)] == 4*d*(1+a)*(1+b)
scars = {}
for s in addresses:
    scars[s] = sum((-1)**(sum(s)-sum(t)) * values[t]
                   for t in addresses if all(x <= y for x,y in zip(t,s)))
for s in addresses:
    assert values[s] == sum(scars[t] for t in addresses
                            if all(x <= y for x,y in zip(t,s)))

report = {
    'scope': 'Fresh exact finite checks only; no historical suite rerun; no Yang-Mills simulation or proof.',
    'ternary_cube': {
        'cells': len(points), 'full_lines': full.rows, 'center_lines': center.rows,
        'full_rank': full.rank(), 'center_rank': center.rank(),
        'full_nullity': full.cols-full.rank(), 'center_nullity': center.cols-center.rank(),
        'extra_center_blind_dimensions': full.rank()-center.rank(),
        'antipodal_counterfeit_center_failures': 0,
        'antipodal_counterfeit_full_failures': failed_full_checks,
    },
    'photon_cube': {
        'variables': {'a':'E1=1+a','b':'E2=1+b','d':'parallel=0, antiparallel=1'},
        'units': 'energy normalized to a common energy unit; c=1; output is normalized invariant mass squared',
        'values': {''.join(map(str,s)): values[s] for s in addresses},
        'anchored_coefficients': {''.join(map(str,s)): scars[s] for s in addresses},
        'full_111': values[(1,1,1)],
        'through_grade_two_111': sum(v for s,v in scars.items() if sum(s)<=2),
        'missing_three_way_coefficient': scars[(1,1,1)],
    }
}
assert report['ternary_cube']['full_nullity'] == 4
assert report['ternary_cube']['center_nullity'] == 14
assert failed_full_checks == 12
assert report['photon_cube']['full_111'] == 16
assert report['photon_cube']['through_grade_two_111'] == 12
out = Path(__file__).with_name('YANG_MILLS_CONNECTION_CHECKS.json')
out.write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
