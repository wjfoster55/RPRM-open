#!/usr/bin/env python3
"""Exact development certificate for y^2=x(x-5)(x+5) over Q.

Standard-library only. Computes an exhaustive necessary mod-8 descent filter,
verifies rational witnesses saturating it, and exercises a constructive decoder
for E(Q)/2^n E(Q). The accompanying note supplies the universal proofs and
identifies the standard Kummer, Selmer, and Mordell-Weil theorem dependencies.
This is not a general Selmer solver or a BSD/L-function computation.

Run: python -B e5_descent.py --output E5_DESCENT_RECEIPT.json
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import isqrt
from pathlib import Path
import platform

Point = tuple[F, F] | None
Signature = tuple[int, int, int]
ROOTS = (0, 5, -5)
P: Point = (F(-4), F(6))
TORSION: tuple[Point, ...] = (None, (F(0), F(0)), (F(5), F(0)), (F(-5), F(0)))
T_NAMES = ('O', 'T0', 'Tplus', 'Tminus')


def require(test: bool, message: str) -> None:
    if not test:
        raise AssertionError(message)


def on_curve(p: Point) -> bool:
    return p is None or p[1]**2 == p[0]**3 - 25*p[0]


def neg(p: Point) -> Point:
    return None if p is None else (p[0], -p[1])


def add(p: Point, q: Point) -> Point:
    if not on_curve(p) or not on_curve(q):
        raise ValueError('Input not on the declared rational curve')
    if p is None:
        return q
    if q is None:
        return p
    x, y = p
    z, w = q
    if x == z:
        if y + w == 0:
            return None
        slope = (3*x*x-25)/(2*y)
    else:
        slope = (w-y)/(z-x)
    out = (slope*slope-x-z, F(0))
    out = (out[0], slope*(x-out[0])-y)
    require(on_curve(out), 'Group-law output is off-curve')
    return out


def mul(n: int, p: Point) -> Point:
    if n < 0:
        return mul(-n, neg(p))
    answer: Point = None
    while n:
        if n & 1:
            answer = add(answer, p)
        p = add(p, p)
        n //= 2
    return answer


def square_root(x: F) -> F:
    if x < 0:
        raise ValueError('No rational square root: negative')
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    if a*a != x.numerator or b*b != x.denominator:
        raise ValueError('Not a rational square')
    return F(a, b)


def squareclass(x: F) -> int:
    """Signed squarefree representative with support {2,5}; verify the remainder.

    The support restriction for this curve is proved in E5_DESCENT_NOTE.md.
    This avoids trial factoring potentially large point coordinates.
    """
    if x == 0:
        raise ValueError('Zero has no multiplicative squareclass')
    n, d = abs(x.numerator), x.denominator
    answer = -1 if x < 0 else 1
    for prime in (2, 5):
        parity = 0
        while n % prime == 0:
            n //= prime
            parity ^= 1
        while d % prime == 0:
            d //= prime
            parity ^= 1
        if parity:
            answer *= prime
    require(isqrt(n)**2 == n and isqrt(d)**2 == d,
            'Non-square prime support outside {2,5}')
    return answer


def delta(p: Point) -> Signature:
    if not on_curve(p):
        raise ValueError('Kummer signature needs a point on E')
    if p is None:
        return (1, 1, 1)
    x, _ = p
    values = []
    for e in ROOTS:
        if x == e:
            other = [r for r in ROOTS if r != e]
            values.append(F((e-other[0])*(e-other[1])))
        else:
            values.append(x-e)
    return tuple(squareclass(v) for v in values)  # type: ignore[return-value]


def signature_product(a: Signature, b: Signature) -> Signature:
    return tuple(squareclass(F(x*y)) for x, y in zip(a, b))  # type: ignore[return-value]


def halves(p: Point) -> list[Point]:
    """Bekker--Zarhin Sec.2 formula, independently checked by the chord law.

    Includes all four rational halves when p is divisible by 2.
    """
    if p is None:
        return list(TORSION)
    if delta(p) != (1, 1, 1):
        raise ValueError('Point is not in 2E(Q)')
    x, y = p
    roots = [square_root(x-e) for e in ROOTS]
    answers: set[tuple[F, F]] = set()
    for signs in product((-1, 1), repeat=3):
        r = [sign*root for sign, root in zip(signs, roots)]
        if r[0]*r[1]*r[2] != -y:
            continue
        a = r[0]*r[1]+r[0]*r[2]+r[1]*r[2]
        half = (x+a, -y-sum(r)*a)
        require(on_curve(half) and add(half, half) == p, 'Half formula fails')
        answers.add(half)
    require(len(answers) == 4, 'Expected exactly four distinct rational halves')
    return sorted(answers)


def encode(p: Point) -> object:
    return 'O' if p is None else {'x': str(p[0]), 'y': str(p[1])}


def primitive_modular_solutions(d: Signature, modulus: int) -> list[tuple[int, int, int, int]]:
    """Complete enumeration in (Z/modulus Z)^4; modulus is a power of two."""
    if modulus < 2 or modulus & (modulus-1):
        raise ValueError('Use a power-of-two modulus')
    out = []
    for u1, u2, u3, t in product(range(modulus), repeat=4):
        if not (u1 & 1 or u2 & 1 or u3 & 1 or t & 1):
            continue
        if (d[0]*u1*u1-d[1]*u2*u2-5*t*t) % modulus:
            continue
        if (d[2]*u3*u3-d[0]*u1*u1-5*t*t) % modulus:
            continue
        out.append((u1, u2, u3, t))
    return out


def compressed_modular_exists(d: Signature, modulus: int) -> bool:
    """Independent residue-set route, retaining whether a root can be odd."""
    buckets = []
    for weight in (*d, 1):
        b: dict[int, set[int]] = {}
        for u in range(modulus):
            b.setdefault(weight*u*u % modulus, set()).add(u % 2)
        buckets.append(b)
    for a, odd1 in buckets[0].items():
        for t2, oddt in buckets[3].items():
            odd2 = buckets[1].get((a-5*t2) % modulus)
            odd3 = buckets[2].get((a+5*t2) % modulus)
            if odd2 is not None and odd3 is not None:
                if any(1 in b for b in (odd1, odd2, odd3, oddt)):
                    return True
    return False


def build_representatives() -> list[dict]:
    reps = []
    for eps in (0, 1):
        for name, t in zip(T_NAMES, TORSION):
            q = add(mul(eps, P), t)
            reps.append({'epsilon': eps, 'torsion': name, 'point': q, 'signature': delta(q)})
    require(len({r['signature'] for r in reps}) == 8, 'The eight witnesses collide')
    return reps


def decode(p: Point, n: int, reps: list[dict]) -> dict:
    """Return (m,T,Remainder) with p=mP+T+2^n*Remainder, no rank input.

    n is an integer >=1. Class coordinates are (m mod 2^n,T). The remainder
    is retained separately and is necessary for exact source reconstruction.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError('n must be a positive integer')
    if not on_curve(p):
        raise ValueError('Input point is off the curve')
    index = {row['signature']: row for row in reps}
    current, number, first_t = p, 0, None
    steps = []
    for k in range(n):
        row = index[delta(current)]
        eps, t = row['epsilon'], TORSION[T_NAMES.index(row['torsion'])]
        if k == 0:
            first_t = t
        number += eps << k
        even = add(add(current, neg(mul(eps, P))), neg(t))
        hs = halves(even)
        nxt = hs[0]
        require(current == add(add(mul(eps, P), t), mul(2, nxt)), 'Step reconstruction')
        steps.append({'step': k, 'signature': list(row['signature']), 'bit': eps,
                      'torsion': row['torsion'], 'remainder': encode(nxt)})
        current = nxt
    rebuilt = add(add(mul(number, P), first_t), mul(1 << n, current))
    require(rebuilt == p, 'Full retained-remainder reconstruction failed')
    return {'m': number, 'torsion': T_NAMES[TORSION.index(first_t)],
            'remainder': encode(current), 'trace': steps}


def run() -> dict:
    D = (-10, -5, -2, -1, 1, 2, 5, 10)
    all_triples = sorted({(a, b, squareclass(F(a*b))) for a, b in product(D, repeat=2)})
    real_candidates = [d for d in all_triples if d[2] > 0 and d[0]*d[1] > 0]
    require(len(all_triples) == 64 and len(real_candidates) == 32, 'Candidate scope')
    filters = {}
    for modulus in (2, 4, 8):
        rows = []
        for d in real_candidates:
            sol = primitive_modular_solutions(d, modulus)
            independent = compressed_modular_exists(d, modulus)
            require(bool(sol) == independent, 'Modular routes disagree')
            rows.append({'signature': list(d), 'primitive_solution_count': len(sol),
                         'first_witness': list(sol[0]) if sol else None})
        filters[str(modulus)] = rows
    survivors = {tuple(r['signature']) for r in filters['8'] if r['primitive_solution_count']}
    require([sum(r['primitive_solution_count']>0 for r in filters[str(m)]) for m in (2,4,8)] == [32,16,8], 'Unexpected filter counts')
    reps = build_representatives()
    require(survivors == {r['signature'] for r in reps}, 'Upper/lower witnesses do not match')
    quad_witnesses = {
        (1,1,1):(1,1,1,0), (-1,-5,5):(0,1,1,1),
        (5,2,10):(1,0,1,1), (-5,-10,2):(1,1,0,1),
        (-1,-1,1):(2,3,1,1), (1,5,5):(5,1,3,2),
        (-5,-2,10):(1,5,2,3), (5,10,2):(3,2,5,1),
    }
    for d, (u,v,w,t) in quad_witnesses.items():
        require(d[0]*u*u-d[1]*v*v==5*t*t and d[2]*w*w-d[0]*u*u==5*t*t, 'Exact quad witness')
    for a, b in product(reps, repeat=2):
        require(delta(add(a['point'],b['point'])) == signature_product(a['signature'],b['signature']), 'Kummer product on witness set')
    # Four cosets give a shorter written proof than listing all 32 candidates.
    H = {r['signature'] for r in reps}
    coset_reps = ((1,1,1), (2,2,1), (1,2,2), (2,1,2))
    cosets = [{signature_product(c,h) for h in H} for c in coset_reps]
    require(set.union(*cosets) == set(real_candidates), 'Cosets do not cover V')
    require(sum(map(len,cosets)) == len(set.union(*cosets)) == 32, 'Cosets overlap')
    for c, mod in (((2,2,1),4), ((1,2,2),8), ((2,1,2),4)):
        require(not primitive_modular_solutions(c,mod), 'Excluded coset representative survives')
    q = mul(2,P)
    require(q == (F(1681,144),F(-62279,1728)), 'Double differs')
    require(delta(q)==delta(None)==(1,1,1), 'Coarse class mismatch')
    qs = halves(q)
    require(set(qs) == {add(P,t) for t in TORSION}, 'Halves do not match torsion orbit')
    require(all(delta(h)!=(1,1,1) for h in qs), 'Unexpected rational quarter')
    require(all(delta(t)!=(1,1,1) for t in TORSION[1:]), 'Unexpected rational 4-torsion')
    decoder_checks = []
    for m, j, n in product(range(-5,11), range(4), range(1,5)):
        r = add(mul(m,P), TORSION[j])
        got = decode(r,n,reps)
        require(got['m']==m%(1<<n) and got['torsion']==T_NAMES[j], 'Incorrect quotient coordinate')
        decoder_checks.append({'input_m':m,'input_torsion':T_NAMES[j],'level_n':n,
                               'output_m':got['m'],'output_torsion':got['torsion']})
    scope = {
        'method':'Exact rational arithmetic plus complete primitive residue enumeration; standard theorem dependencies in note',
        'no_rank_label_input':True, 'no_Sage_no_database_no_L_function':True,
        'computed': '32 real-admissible signatures, primitive mod-2/4/8 filters, eight exact rational realizations, rational halving and quotient decoder instances',
        'universal_proof_in_note': 'rank=1; Sha[2^n]=0 for all n; compatible 2-power Selmer quotient coordinates',
        'not_claimed':['general BSD theorem','new mathematical theorem','total Sha order','odd-prime saturation','P is a full integral generator','analytic rank or L-values','performance advantage'],
    }
    return {
        'status':'PASS', 'utc':datetime.now(timezone.utc).isoformat(),
        'python':platform.python_version(),'code_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'curve':{'a':-25,'b':0,'base_field':'Q','identity':'O'},'scope':scope,
        'initial_product_square_candidates':len(all_triples),'real_admissible':len(real_candidates),
        'modular_filters':filters,
        'four_cosets':[{'representative':list(c),'members':[list(h) for h in sorted(block)]} for c,block in zip(coset_reps,cosets)],
        'eight_realized_classes':[{'epsilon':r['epsilon'],'torsion':r['torsion'],'point':encode(r['point']),
                                  'signature':list(r['signature']), 'quadric_witness':list(quad_witnesses[r['signature']])} for r in reps],
        'coarse_vs_finer_example':{'P':encode(P),'Q_equals_2P':encode(q),'delta_Q':list(delta(q)),
                                 'halves_Q':[{'point':encode(h),'signature':list(delta(h))} for h in qs],
                                 'Q_level1':decode(q,1,reps),'Q_level2':decode(q,2,reps),
                                 'O_level2':decode(None,2,reps)},
        'decoder_tests':{'count':len(decoder_checks),'input_family':'mP+T, -5<=m<=10, T in E[2], n=1..4',
                         'records':decoder_checks},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('E5_DESCENT_RECEIPT.json'))
    args = parser.parse_args()
    receipt = run()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':receipt['status'],'real_candidates':32,'mod8_survivors':8,
                      'rationally_realized_classes':len(receipt['eight_realized_classes']),
                      'decoder_checks':receipt['decoder_tests']['count'],
                      'output':str(args.output)},indent=2))

if __name__ == '__main__':
    main()
