"""Exact clarification checks: prior interval subtraction and keyring hub."""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
from hashlib import sha256
import argparse, json

root=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--output',type=Path,required=True)
args=ap.parse_args()
if args.output.exists():raise FileExistsError('Use a fresh output path')

# Attributed earlier enclosures from bsd-coefficient-05/TWO_SCALES.md.
# This is an exact new subtraction of those enclosures, not a new L/height run.
A=(F('6.38511803'),F('6.38518585'))
B1=(F('6.384593255'),F('6.385625424'))
D=(A[0]-B1[1],A[1]-B1[0])
assert D==(F('-0.000507394'),F('0.000592595'))
assert D[0]<0<D[1]

M=((0,1,1,1),(1,0,0,0),(1,0,0,0),(1,0,0,0))
degrees=[sum(r) for r in M]
automorphisms=[p for p in permutations(range(4))
               if all(M[i][j]==M[p[i]][p[j]] for i in range(4) for j in range(4))]
assert degrees==[3,1,1,1]
assert len(automorphisms)==6 and all(p[0]==0 for p in automorphisms)

# View along the y-axis: both distinct connector points map to (0,0).
points=((0,3,0),(0,-3,0))
assert points[0]!=points[1] and all(x*x+y*y==9 and z==0 for x,y,z in points)
projection=lambda p:(p[0],p[2])
assert projection(points[0])==projection(points[1])

# Satellite balls: squared projected-chord threshold is 1/12.
# For two axes 60 degrees apart, max-min squared correlation is 3/4,
# smaller than the required 11/12. This records the exact inequality
# used in the written orthographic uniqueness argument.
assert 1-F(1,12)==F(11,12)>F(3,4)

result={'status':'EXACT_CLARIFICATION_CHECKS_PASS',
    'earlier_input_intervals':{'analytic':list(map(str,A)),'arithmetic_sigma1':list(map(str,B1))},
    'difference_interval':list(map(str,D)),
    'difference_decimal':['-0.000507394','0.000592595'],
    'difference_equal_zero':'OPEN: interval includes both zero and nonzero values',
    'linking_degrees':degrees,'all_24_permutations_checked':True,
    'automorphisms':automorphisms,'all_automorphisms_fix_connector':True,
    'edge_on_distinct_points':points,'same_projection':projection(points[0]),
    'fresh_analytic_or_height_computation':False,
    'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
