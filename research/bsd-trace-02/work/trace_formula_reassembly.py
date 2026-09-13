"""Independent modular ledger and final-torsion-point check; no trace125 import.

This does not independently reconstruct every orbit point: it reconstructs
the finite CM group, verifies the final lifted point and primitive Gaussian
annihilator, and recomputes every supplied rho^5 term and its multiplicity.
The separate source audit and full orbit replay remain explicit dependencies.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json

M = 125
D = 16
ZERO = (0,)*D
ONE = (1,)+(0,)*(D-1)


def constant(n):
    return (n % M,)+(0,)*(D-1)


def plus(a,b):
    return tuple((x+y) % M for x,y in zip(a,b))


def minus(a,b):
    return tuple((x-y) % M for x,y in zip(a,b))


def times(a,b):
    # Direct cyclic indexing with the wrap factor, distinct from the
    # production convolution-then-fold implementation.
    out = [0]*D
    for j,x in enumerate(a):
        for k,y in enumerate(b):
            out[(j+k) % D] += x*y*(1 if j+k < D else 2)
    return tuple(x % M for x in out)


def power(a,n):
    out = ONE
    for digit in bin(n)[2:]:
        out = times(out,out)
        if digit == '1':
            out = times(out,a)
    return out


def inverse(a):
    assert any(x % 5 for x in a)
    # Unit group exponent divides 25*(5^16-1); this avoids the production
    # field inverse followed by Newton iteration.
    value = power(a,25*(5**16-1)-1)
    assert times(a,value) == ONE
    return value


def quotient(a,b):
    return times(a,inverse(b))


def curve(P):
    return P is None or times(P[1],P[1]) == minus(power(P[0],3),times(constant(1156),P[0]))


def opposite(P):
    return None if P is None else (P[0],minus(ZERO,P[1]))


def add(P,Q):
    if P is None:return Q
    if Q is None:return P
    x,y = P
    u,v = Q
    if x == u:
        if plus(y,v) == ZERO:return None
        assert y == v
        slope = quotient(minus(times(constant(3),times(x,x)),constant(1156)),times(constant(2),y))
    else:
        slope = quotient(minus(v,y),minus(u,x))
    xx = minus(minus(times(slope,slope),x),u)
    answer = (xx,minus(times(slope,minus(x,xx)),y))
    assert curve(answer)
    return answer


def multiply_point(n,P):
    if n < 0:return multiply_point(-n,opposite(P))
    result = None
    for digit in bin(n)[2:]:
        result = add(result,result)
        if digit == '1':result = add(result,P)
    return result


def gaussian(a,b,P):
    Q = multiply_point(b,P)
    iQ = None if Q is None else (minus(ZERO,Q[0]),times(constant(57),Q[1]))
    return add(multiply_point(a,P),iQ)


def gaussian_group():
    generators = [(67,2),(67,66),(65,2),(65,66)]
    group = {(1,0)}
    while True:
        expanded = group | {((a*c-b*d)%68,(a*d+b*c)%68)
                            for a,b in group for c,d in generators}
        if expanded == group:return group
        group = expanded


def main():
    root = Path(__file__).resolve().parent.parent
    data = (root/'evidence/trace125.json').read_bytes()
    receipt = json.loads(data)
    assert receipt['source_sha256'] == sha256((root/'work/trace125.py').read_bytes()).hexdigest()
    assert receipt['cm_action_source_sha256'] == sha256((root/'work/cm_action.py').read_bytes()).hexdigest()
    assert receipt['modulus'] == 125
    P = tuple(tuple(c) for c in receipt['lifted_point'])
    assert curve(P)
    assert [[x % 5 for x in c] for c in P] == receipt['residue_point']
    target = multiply_point(34,P)
    assert target is not None and target[1] == ZERO
    assert target[0] in [constant(0),constant(34),constant(-34)]
    assert multiply_point(68,P) is None
    primitive_actions = [(34,-34),(16,-4),(16,4)]
    assert all(gaussian(a,b,P) is not None for a,b in primitive_actions)
    G = gaussian_group()
    rows = receipt['orbit_terms']
    assert len(G) == len(rows) == 512
    assert {tuple(row['gaussian_action']) for row in rows} == G
    multiplicity = Counter(tuple(row['rho']) for row in rows)
    assert len(multiplicity) == 256 and set(multiplicity.values()) == {2}
    total = ZERO
    for row in rows:
        r = tuple(row['rho'])
        term = plus(times(constant(2),power(r,5)),times(constant(289),r))
        assert term == tuple(row['term'])
        total = plus(total,term)
    S = times(constant(63),total)
    assert S == tuple(receipt['trace_unit_multiple']) == constant(100)
    # Independent evaluation at the identity and the recorded involution.
    identity_r = quotient(P[1],times(constant(2),P[0]))
    assert identity_r == tuple(next(row['rho'] for row in rows if row['gaussian_action']==[1,0]))
    other = gaussian(33,34,P)
    assert other != P
    assert quotient(other[1],times(constant(2),other[0])) == identity_r
    output = {
        'status':'INDEPENDENT_LEDGER_AND_LIFTED_POINT_REASSEMBLY_PASSED',
        'input_receipt_sha256':sha256(data).hexdigest(),
        'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'production_source_sha256':receipt['source_sha256'],
        'field_arithmetic':'direct wrap multiplication; unit inverse by group exponent',
        'final_point_on_curve':True, 'same_residue_point':True,
        'point_34P_is_nonzero_2_torsion':True, 'point_68P_is_O':True,
        'all_three_primitive_CM_tests_pass':True,
        'independently_reconstructed_action_group_size':len(G),
        'all_512_terms_recomputed':True, 'distinct_rho_values':256,
        'each_rho_multiplicity':2, 'trace_residue_mod_125':100,
        'valuation_is_exactly_2':True,
        'identity_and_involution_evaluations_agree':True,
        'limitation':'Does not independently reconstruct all 512 rho coordinates from the point; source audit and separate full orbit replay are explicit dependencies.',
    }
    destination = root/'evidence/trace_formula_reassembly.json'
    if destination.exists():raise FileExistsError('Use a fresh output path')
    destination.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2))


if __name__ == '__main__':main()
