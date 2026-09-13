"""Exact bounded controls for the all-finite-n product proof. Standard library.

Default recomputes and compares the saved receipt without writing.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
from math import comb
import argparse
import json

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def prod(items):
    result = F(1)
    for item in items:
        result *= item
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-results', action='store_true')
    args = parser.parse_args()
    rows = []
    totals = {'cubes': 0, 'complete_basis_eigenvectors': 0,
              'off_diagonal_orthogonality_controls': 0,
              'complete_sum_fibers': 0}
    for p in (F(1,2), F(3,5), F(1,5)):
        for n in range(1,5):
            states = list(product((0,1), repeat=n))
            weights = [prod(p if bit else 1-p for bit in s) for s in states]
            lookup = {state: i for i,state in enumerate(states)}
            require(sum(weights) == 1 and min(weights)>0, 'Invalid law')
            def inner(a,b):
                return sum(w*x*y for w,x,y in zip(weights,a,b))
            def conditional(values, axis):
                out = []
                for state in states:
                    low = list(state)
                    high = list(state)
                    low[axis], high[axis] = 0, 1
                    out.append((1-p)*values[lookup[tuple(low)]]+p*values[lookup[tuple(high)]])
                return out
            basis = []
            spectrum = []
            for mask in range(1<<n):
                subset = [i for i in range(n) if mask>>i & 1]
                values = [prod(F(state[j])-p for j in subset) for state in states]
                residual_sum = [F(0)]*len(states)
                energy = F(0)
                for axis in range(n):
                    averaged = conditional(values, axis)
                    residual = [x-y for x,y in zip(values,averaged)]
                    require(conditional(averaged,axis) == averaged, 'Conditional not idempotent')
                    require(inner(residual,averaged) == 0, 'Projection not orthogonal')
                    energy += inner(residual,residual)
                    residual_sum = [x+y for x,y in zip(residual_sum,residual)]
                require(residual_sum == [len(subset)*x for x in values], 'Wrong complete eigenmode')
                norm = inner(values,values)
                require(norm>0 and energy == len(subset)*norm, 'Wrong eigenmode energy')
                basis.append(values)
                spectrum.append(len(subset))
                totals['complete_basis_eigenvectors'] += 1
            for left,right in combinations(basis,2):
                require(inner(left,right) == 0, 'Distinct modes not orthogonal')
                totals['off_diagonal_orthogonality_controls'] += 1
            multiplicities = {str(k): spectrum.count(k) for k in range(n+1)}
            require(multiplicities == {str(k):comb(n,k) for k in range(n+1)}, 'Incomplete spectrum')
            summed = [sum(F(bit)-p for bit in s) for s in states]
            mean = sum(w*x for w,x in zip(weights,summed))
            variance = inner(summed,summed)-mean**2
            require(mean == 0 and variance == n*p*(1-p), 'Wrong sum variance')
            require(variance/F(n*n) == p*(1-p)/n, 'Wrong mean variance')
            for k in range(n+1):
                fiber = [s for s,value in zip(states,summed) if value==k-n*p]
                require(len(fiber)==comb(n,k) and all(sum(s)==k for s in fiber), 'Incomplete sum fiber')
                totals['complete_sum_fibers'] += 1
            density_ratio = max(weights)/min(weights)
            require(density_ratio == (max(p,1-p)/min(p,1-p))**n, 'Density ratio wrong')
            if p == F(3,5):
                require(density_ratio==F(3,2)**n and variance==F(6*n,25), 'Offset control failed')
            rows.append({'p':str(p),'n':n,'state_count':len(states),
                         'spectrum_multiplicities':multiplicities,
                         'sharp_residual_gap':1,'sharp_C_mix':1,
                         'one_coordinate_per_step_gap':str(F(1,n)),
                         'sum_variance':str(variance),'mean_variance':str(variance/F(n*n)),
                         'density_ratio':str(density_ratio)})
            totals['cubes'] += 1
    envelope = (1+F(3,5)**4)**6-1
    require(envelope > 1, 'Six disjoint squares must defeat this absolute envelope')
    tilt_rows = []
    for root_ratio in (F(3,2),F(2),F(5)):
        a, b, c = F(1),root_ratio**2,root_ratio
        w_low, w_high = (b-c)/(b-a),(c-a)/(b-a)
        require(w_low+w_high == 1 and w_low*a+w_high*b == c,'Wrong extremal tilt law')
        tv = (w_low*abs(a/c-1)+w_high*abs(b/c-1))/2
        exact = (root_ratio-1)/(root_ratio+1)
        require(tv == exact,'Sharp two-point tilt control failed')
        tilt_rows.append({'raw_density_values':[str(a),str(b)],
                          'base_probabilities':[str(w_low),str(w_high)],
                          'normalizer':str(c),'total_variation':str(tv)})
    result = {'status':'PASS','scope':'Exact finite complete-basis controls; all-n and tilt claims are the separate written proofs; not an SU2 vacuum',
              'counts':totals,'cases':rows,
              'six_square_absolute_support_envelope':str(envelope),
              'sharp_two_point_tilt_controls':tilt_rows}
    target = Path(__file__).with_name('RESULTS_STACKING.json')
    payload = json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.write_results:
        target.write_text(payload,encoding='utf-8')
    else:
        require(target.read_text(encoding='utf-8') == payload,'Receipt differs from fresh recomputation')
    print('PASS: complete product-basis controls; receipt '+('written' if args.write_results else 'compared_without_writing'))
    print(json.dumps(totals,sort_keys=True))

if __name__ == '__main__':
    main()
