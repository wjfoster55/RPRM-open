"""Bounded YM2 exact checks and optional small trajectory illustration.

Python 3.10+, standard library only. Does not run supplied YM1 code.
Two independent routes: diagonal analytic contractions; full color-vector
power-series ODE recurrence. Fractions are exact; RK4 is illustration only.
"""
from fractions import Fraction as F
from itertools import combinations
from math import factorial, sqrt
from pathlib import Path
import argparse
import json

PAIRS = list(combinations(range(3), 2))
ZERO = (F(0), F(0), F(0))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c*x for x in a)


def diagonal(q):
    return [tuple(F(q[i]) if i == a else F(0) for a in range(3)) for i in range(3)]


def analytic(q, p, g=F(1), volume=F(1)):
    """Route 1: differentiate the diagonal potential, not the series solver."""
    q, p = list(map(F, q)), list(map(F, p))
    force = [g*g*q[i]*sum(q[j]**2 for j in range(3) if i != j) for i in range(3)]
    hess = [[g*g*(sum(q[k]**2 for k in range(3) if k != i) if i == j else 2*q[i]*q[j])
             for j in range(3)] for i in range(3)]
    hp = [dot(row, p) for row in hess]
    hf = [dot(row, force) for row in hess]
    cubic = 6*g*g*sum(q[i]*p[i]*p[j]**2+q[j]*p[j]*p[i]**2 for i, j in PAIRS)
    return dict(E=volume*dot(p, p)/2,
                B=volume*g*g*sum(q[i]**2*q[j]**2 for i, j in PAIRS)/2,
                J=volume*dot(force, p),
                K=volume*(dot(p, hp)-dot(force, force)),
                L=volume*(cubic-4*dot(p, hf)),
                force=force, hessian=hess, velocity_curvature=volume*dot(p, hp),
                force_norm_squared=volume*dot(force, force),
                cubic=volume*cubic, force_curvature=4*volume*dot(p, hf))


def scross(a, b, n):
    out = ZERO
    for k in range(n+1):
        if k < len(a) and n-k < len(b):
            out = add(out, cross(a[k], b[n-k]))
    return out


def sdot(a, b, n):
    return sum(dot(a[k], b[n-k]) for k in range(n+1) if k < len(a) and n-k < len(b))


def vector_series(a0, v0, order=6, g=F(1), volume=F(1)):
    """Route 2: A_i''=g² sum_j A_j x (A_j x A_i), vector convolution.

    No call to analytic(), no Hessian, and no precomputed energy derivatives.
    Coefficients are ordinary Taylor coefficients, not divided again by n!.
    """
    a = [[tuple(map(F, a0[i])), tuple(map(F, v0[i]))] for i in range(3)]
    for n in range(order-1):
        acc = []
        for i in range(3):
            row = ZERO
            for j in range(3):
                c = [scross(a[j], a[i], k) for k in range(n+1)]
                row = add(row, scross(a[j], c, n))
            acc.append(scale(g*g/F((n+1)*(n+2)), row))
        for i in range(3):
            a[i].append(acc[i])
    v = [[scale(k+1, a[i][k+1]) for k in range(order)] for i in range(3)]
    c = [[scross(a[i], a[j], n) for n in range(order+1)] for i, j in PAIRS]
    b = [volume*g*g*sum(sdot(s, s, n) for s in c)/2 for n in range(order+1)]
    e = [volume*sum(sdot(s, s, n) for s in v)/2 for n in range(order)]
    gauss = []
    for n in range(order):
        row = ZERO
        for i in range(3):
            row = add(row, scross(a[i], v[i], n))
        gauss.append(scale(volume, row))
    return dict(A=a, B_coefficients=b, E_coefficients=e,
                H_coefficients=[b[n]+e[n] for n in range(order)], Gauss_coefficients=gauss)


ROT = ((F(1,3), F(-2,3), F(2,3)),
       (F(2,3), F(2,3), F(1,3)),
       (F(-2,3), F(1,3), F(2,3)))


def rotate(a):
    return [tuple(dot(row, v) for row in ROT) for v in a]


STATES = [
    ('R3_A', (1,1,0), (0,0,1), (F(1,2), F(1,2), 0, 0, 0)),
    ('R3_B', (1,1,0), (F(2,3), F(-2,3), F(1,3)), (F(1,2), F(1,2), 0, F(-8,3), 0)),
    ('R4_plus', (1,1,1), (1,1,-2), (3, F(3,2), 0, -12, 36)),
    ('R4_minus', (1,1,1), (-1,-1,2), (3, F(3,2), 0, -12, -36)),
    ('R4_planar_plus', (1,2,0), (1,-2,0), (F(5,2), 2, 0, -28, 48)),
    ('R4_planar_minus', (1,2,0), (-1,2,0), (F(5,2), 2, 0, -28, -48)),
]


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def exact_checks():
    rows = []
    require(all(dot(ROT[i], ROT[j]) == int(i == j) for i in range(3) for j in range(3)), 'rotation orthogonal')
    require(dot(ROT[0], cross(ROT[1], ROT[2])) == 1, 'rotation proper')
    for name, q, p, expected in STATES:
        obs = analytic(q, p)
        require(tuple(obs[k] for k in ('E','B','J','K','L')) == expected, name+' expected row')
        require(obs['E']+obs['B'] <= 5 and dot(q, q) <= 9, name+' bounded initial enclosure')
        source, vel = diagonal(q), diagonal(p)
        normal = vector_series(source, vel)
        transported = vector_series(rotate(source), rotate(vel))
        for label, res in [('original', normal), ('gauge_rotated', transported)]:
            require([factorial(n)*res['B_coefficients'][n] for n in range(4)] ==
                    [obs[k] for k in ('B','J','K','L')], name+' '+label+' independent derivatives')
            require(res['E_coefficients'][0] == obs['E'], name+' electric energy')
            require(all(x == 0 for x in res['H_coefficients'][1:]), name+' energy series conservation')
            require(all(v == ZERO for v in res['Gauss_coefficients']), name+' Gauss series conservation')
        require(all(normal[k] == transported[k] for k in ('B_coefficients','E_coefficients','Gauss_coefficients')), name+' gauge invariant coefficients')
        for i in range(3):
            for n in range(7):
                require(rotate([normal['A'][i][n]])[0] == transported['A'][i][n], name+' flow covariance')
        rows.append(dict(name=name, q=q, p=p, A=source, velocity=vel, observables=obs,
                         series={k:v for k,v in normal.items() if k != 'A'},
                         rotated_A=rotate(source), rotated_velocity=rotate(vel),
                         gauge_transport='PASS', independent_derivatives='PASS'))
    # A different normalization tests factors, not a new physical witness pair.
    q, p = (1,2,0), (1,-2,0)
    scaled = analytic(q, p, g=F(2), volume=F(3))
    scaled_series = vector_series(diagonal(q), diagonal(p), g=F(2), volume=F(3))
    require([factorial(n)*scaled_series['B_coefficients'][n] for n in range(4)] ==
            [scaled[k] for k in ('B','J','K','L')], 'coupling/volume normalization')
    # Commuting sector must include aligned electric fields to remain commuting.
    comm_a = [(F(i),F(0),F(0)) for i in (1,2,3)]
    comm_v = [(F(i),F(0),F(0)) for i in (1,-1,2)]
    comm = vector_series(comm_a, comm_v)
    require(all(x == 0 for x in comm['B_coefficients']), 'commuting B=0')
    require(comm['E_coefficients'] == [F(3)]+[F(0)]*5, 'commuting electric conserved')
    require(all(x == ZERO for x in comm['Gauss_coefficients']), 'commuting Gauss')
    # Present flatness alone is not an invariant-sector condition.
    emerging = vector_series(diagonal((1,0,0)), diagonal((0,1,0)))
    require(emerging['B_coefficients'][:3] == [0,0,F(1,2)], 'initially flat countercontrol')
    # Exact rational points on the complete conditioned momentum circle:
    # p=(2 cos(theta), -cos(theta)+sqrt(3)sin(theta), -cos(theta)-sqrt(3)sin(theta)).
    # These selected rational points need no trigonometric evaluation.
    circle_rows=[]
    for p in ((2,-1,-1), (-2,1,1), (1,1,-2), (-1,-1,2)):
        obs=analytic((1,1,1), p)
        require(tuple(obs[k] for k in ('E','B','J','K')) == (3,F(3,2),0,-12), 'conditioned circle')
        require(obs['L'] == -18*p[0]*p[1]*p[2], 'conditioned cubic contraction')
        circle_rows.append(dict(p=p,L=obs['L']))
    # Direct derivative of Gauss at a nonsingular, non-diagonal sample off Gauss:
    # conservation identity is valid there too; conservation is not admission.
    arbitrary_a=[(F(1),F(2),F(0)),(F(0),F(1),F(3)),(F(2),F(0),F(1))]
    arbitrary_v=[(F(2),F(0),F(1)),(F(1),F(-1),F(0)),(F(0),F(2),F(1))]
    arbitrary=vector_series(arbitrary_a,arbitrary_v)
    require(all(x == 0 for x in arbitrary['H_coefficients'][1:]), 'generic energy identity')
    require(all(x == ZERO for x in arbitrary['Gauss_coefficients'][1:]), 'generic Gauss derivative identity')
    require(arbitrary['Gauss_coefficients'][0] != ZERO, 'off-constraint sample correctly distinguished')
    return dict(status='PASS', exact_method='fractions.Fraction; no sampled collision or numerical proof',
                claim='R3 and R4 fail future magnetic-energy readout', states=rows,
                normalization_control=dict(g=2,volume=3,observables=scaled),
                commuting_control={k:v for k,v in comm.items() if k != 'A'},
                initially_flat_countercontrol={k:v for k,v in emerging.items() if k != 'A'},
                conditioned_circle_samples=circle_rows,
                off_constraint_control={k:v for k,v in arbitrary.items() if k != 'A'},
                coverage='Written proofs supply general identities; finite checks are independent calibration. No YM1 rerun; no formal proof or spectral computation.')


def acceleration(q):
    return [-q[i]*sum(q[j]*q[j] for j in range(3) if j != i) for i in range(3)]


def trajectory(q0, p0, end, steps):
    y=list(map(float, q0+p0))
    h=end/steps
    initial=sum(v*v for v in y[3:])/2+sum(y[i]**2*y[j]**2 for i,j in PAIRS)/2
    max_drift=0.0
    def rhs(z):
        return z[3:]+acceleration(z[:3])
    for _ in range(steps):
        k1=rhs(y)
        k2=rhs([v+h*k/2 for v,k in zip(y,k1)])
        k3=rhs([v+h*k/2 for v,k in zip(y,k2)])
        k4=rhs([v+h*k for v,k in zip(y,k3)])
        y=[v+h*(a+2*b+2*c+d)/6 for v,a,b,c,d in zip(y,k1,k2,k3,k4)]
        energy=sum(v*v for v in y[3:])/2+sum(y[i]**2*y[j]**2 for i,j in PAIRS)/2
        max_drift=max(max_drift, abs(energy-initial))
    gauss=ZERO
    for a,p in zip(diagonal(y[:3]),diagonal(y[3:])):
        gauss=add(gauss,cross(a,p))
    return dict(t=end,steps=steps,q=y[:3],p=y[3:], B=sum(y[i]**2*y[j]**2 for i,j in PAIRS)/2,
                max_absolute_energy_drift=max_drift,Gauss_norm=float(sqrt(dot(gauss,gauss))))


def numeric_checks():
    rows=[]
    for name,q,p,_ in STATES[:4]:
        coarse=trajectory(q,p,0.01,100)
        fine=trajectory(q,p,0.01,200)
        difference=abs(coarse['B']-fine['B'])
        require(difference < 1e-10, name+' RK4 step comparison')
        require(max(coarse['max_absolute_energy_drift'],fine['max_absolute_energy_drift']) < 1e-10, name+' numeric energy drift')
        require(coarse['Gauss_norm'] == fine['Gauss_norm'] == 0, name+' diagonal Gauss')
        rows.append(dict(name=name,coarse=coarse,fine=fine,absolute_step_difference=difference))
    return dict(status='PASS',method='RK4, diagonal exact invariant sector; 1200 total steps',
                absolute_tolerance=1e-10,rows=rows,
                warning='Step comparison and energy drift are diagnostics, not rigorous error bounds. Exact unequal derivatives prove the result.')


def strings(value):
    if isinstance(value,F):
        return str(value)
    if isinstance(value,dict):
        return {k:strings(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [strings(v) for v in value]
    return value


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--numeric', action='store_true')
    args=parser.parse_args()
    result=dict(exact=exact_checks())
    if args.numeric:
        result['numeric_illustration']=numeric_checks()
    encoded=json.dumps(strings(result),indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(encoded,encoding='utf-8')
        print(json.dumps(dict(status='PASS',output=str(args.output),exact_states=6,gauge_transports=6,numeric=args.numeric)))
    else:
        print(encoded,end='')


if __name__ == '__main__':
    main()
