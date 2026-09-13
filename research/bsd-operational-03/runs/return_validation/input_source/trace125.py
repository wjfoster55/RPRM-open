"""Exact E34 CM trace in the unramified ring (Z/m)[z]/(z^16-2).

Standard library only. No database, approximate constants or saved PASS input.
The primitive seed is arbitrary; the returned trace is a Gaussian-unit
multiple of the distinguished real-period trace. Its 5-adic valuation is
therefore the requested invariant. See TRACE_CALCULATION.md for the proof.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import random
import time
from cm_action import cm_group

Q = 5**16
N = 16


class F:
    """Exact coefficient-vector arithmetic; z^16=2, coefficient modulus m."""
    __slots__ = ('c', 'm')

    def __init__(self, value=0, mod=125):
        self.m = mod
        if isinstance(value, F):
            value = value.c
        if isinstance(value, int):
            value = [value]
        value = list(value)
        if len(value) > N:
            raise ValueError('Expected at most sixteen coefficients')
        self.c = tuple(x % mod for x in value) + (0,)*(N-len(value))

    def coerce(self, value):
        if isinstance(value, F):
            if value.m != self.m:
                raise ValueError('Mixed coefficient moduli')
            return value
        if isinstance(value, int):
            return F(value, self.m)
        return NotImplemented

    def __add__(self, other):
        other = self.coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return F([a+b for a,b in zip(self.c, other.c)], self.m)
    __radd__ = __add__

    def __neg__(self):
        return F([-a for a in self.c], self.m)

    def __sub__(self, other):
        other = self.coerce(other)
        return NotImplemented if other is NotImplemented else self + (-other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        other = self.coerce(other)
        if other is NotImplemented:
            return NotImplemented
        out = [0]*(2*N-1)
        for j,a in enumerate(self.c):
            if a:
                for k,b in enumerate(other.c):
                    if b:
                        out[j+k] += a*b
        for j in range(N, 2*N-1):
            out[j-N] += 2*out[j]
        return F(out[:N], self.m)
    __rmul__ = __mul__

    def __pow__(self, n):
        if n < 0:
            return self.inv()**(-n)
        out = F(1, self.m)
        base = self
        while n:
            if n & 1:
                out = out*base
            n //= 2
            if n:
                base = base*base
        return out

    def inv(self):
        reduction = F(self.c, 5)
        if not reduction:
            raise ZeroDivisionError('Nonunit in the unramified coefficient ring')
        inverse = reduction**(Q-2)
        if self.m != 5:
            inverse = F(inverse.c, self.m)
            # Two updates suffice from precision 5 to any m in {25,125}.
            inverse = inverse*(2-self*inverse)
            inverse = inverse*(2-self*inverse)
        if self*inverse != 1:
            raise ArithmeticError('Inverse certificate failed')
        return inverse

    def __truediv__(self, other):
        other = self.coerce(other)
        return NotImplemented if other is NotImplemented else self*other.inv()

    def __rtruediv__(self, other):
        return self.inv()*other

    def __eq__(self, other):
        other = self.coerce(other)
        return False if other is NotImplemented else self.c == other.c

    def __bool__(self):
        return any(self.c)

    def __repr__(self):
        return f'F({list(self.c)}, mod={self.m})'


class Jet:
    """First derivative, with exact ring coefficients (dual numbers)."""
    __slots__ = ('v', 'd')

    def __init__(self, value, derivative):
        self.v = value
        self.d = F(derivative, value.m)

    def coerce(self, x):
        return x if isinstance(x, Jet) else Jet(F(x, self.v.m), 0)

    def __add__(self, x):
        x = self.coerce(x)
        return Jet(self.v+x.v, self.d+x.d)
    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.v, -self.d)

    def __sub__(self, x):
        return self + (-self.coerce(x))

    def __rsub__(self, x):
        return self.coerce(x) - self

    def __mul__(self, x):
        x = self.coerce(x)
        return Jet(self.v*x.v, self.d*x.v+self.v*x.d)
    __rmul__ = __mul__

    def inv(self):
        u = self.v.inv()
        return Jet(u, -self.d*u*u)

    def __truediv__(self, x):
        return self*self.coerce(x).inv()

    def __pow__(self, n):
        if n == 0:
            return Jet(F(1, self.v.m), 0)
        return Jet(self.v**n, n*self.v**(n-1)*self.d)

    def __eq__(self, x):
        x = self.coerce(x)
        return self.v == x.v and self.d == x.d


def neg(P):
    return None if P is None else (P[0], -P[1])


def add(P, R):
    if P is None:
        return R
    if R is None:
        return P
    x,y = P
    u,v = R
    if x == u:
        if y == -v:
            return None
        if y != v:
            raise ArithmeticError('Unadmitted equal-x pair over a ring')
        slope = (3*x*x-1156)/(2*y)
    else:
        slope = (v-y)/(u-x)
    X = slope*slope-x-u
    return X, slope*(x-X)-y


def mul(n, P):
    if n < 0:
        return mul(-n, neg(P))
    R = None
    while n:
        if n & 1:
            R = add(R, P)
        n //= 2
        if n:
            P = add(P, P)
    return R


def cm_i(P):
    if P is None:
        return None
    x,y = P
    # i=2 mod5 has unique lift 57 mod125; its mod25 image is7.
    return -x, y*F(57, x.m)


def gaussian(a, b, P):
    return add(mul(a, P), cm_i(mul(b, P)))


def on_curve(P):
    return P is None or P[1]*P[1] == P[0]**3-1156*P[0]


def primitive(P):
    return (P is not None and on_curve(P) and mul(68, P) is None
            and gaussian(34,-34,P) is not None
            and gaussian(16,-4,P) is not None
            and gaussian(16,4,P) is not None)


def sqrt_field(a):
    if a.m != 5:
        raise ValueError('Square-root search is only in the residue field')
    if not a:
        return a
    if a**((Q-1)//2) != 1:
        return None
    odd = Q-1
    s = 0
    while odd % 2 == 0:
        odd //= 2
        s += 1
    z = F([0,1], 5)
    assert z**((Q-1)//2) == -1
    c = z**odd
    x = a**((odd+1)//2)
    t = a**odd
    while t != 1:
        i = 1
        power = t*t
        while power != 1:
            power = power*power
            i += 1
            if i >= s:
                raise ArithmeticError('Tonelli-Shanks invariant failed')
        b = c**(2**(s-i-1))
        x = x*b
        c = b*b
        t = t*c
        s = i
    assert x*x == a
    return x


def gaussian_power(z, n):
    out = (1,0)
    for _ in range(n):
        out = (out[0]*z[0]-out[1]*z[1], out[0]*z[1]+out[1]*z[0])
    return out


def find_seed(seed):
    rng = random.Random(seed)
    factors = []
    for pi in ((-1,2),(-1,-2)):
        real, imag = gaussian_power(pi, 16)
        assert (real-1) % 68 == 0 and imag % 68 == 0
        factors.append(((real-1)//68, imag//68))
    for attempt in range(1,65):
        x = F([rng.randrange(5) for _ in range(N)], 5)
        y = sqrt_field(x**3-1156*x)
        if y is None:
            continue
        R = (x,y)
        for a,b in factors:
            P = gaussian(a,b,R)
            # The Frobenius choice is only a search device. These direct
            # exact tests admit the point and its full Gaussian annihilator.
            if primitive(P):
                return P, {'attempt':attempt, 'search_factor':[a,b],
                           'raw_point':encode_point(R)}
    raise RuntimeError('OPEN: primitive-point search exhausted its bound')


def valuation(a):
    if not a:
        return {5:1,25:2,125:3}[a.m]
    out = 0
    coefficients = list(a.c)
    while all(c % 5 == 0 for c in coefficients):
        out += 1
        coefficients = [c//5 for c in coefficients]
    return out


def lift_point(P, modulus):
    x,y = [F(c.c, modulus) for c in P]
    rows = []
    for iteration in range(4):
        for _ in range(2):
            y = y-(y*y-x**3+1156*x)/(2*y)
        assert on_curve((x,y))
        tangent_y = (3*x*x-1156)/(2*y)
        image = mul(34, (Jet(x,1), Jet(y,tangent_y)))
        if image is None:
            raise ArithmeticError('Primitive seed unexpectedly maps to infinity')
        function = image[1]
        assert F(function.d.c,5)
        rows.append({'iteration':iteration,
                     'ordinate_34P_valuation_capped':valuation(function.v),
                     'derivative_is_unit':True})
        if not function.v:
            break
        x = x-function.v/function.d
    else:
        raise ArithmeticError('Hensel lift did not close')
    lifted = (x,y)
    assert primitive(lifted)
    assert encode_point(reduce_point(lifted,5)) == encode_point(P)
    image = mul(34,lifted)
    assert image is not None and image[1] == 0
    assert image[0] in (F(0,modulus),F(34,modulus),F(-34,modulus))
    return lifted, rows


def reduce_point(P, modulus):
    return None if P is None else tuple(F(x.c,modulus) for x in P)


def encode_point(P):
    return None if P is None else [list(x.c) for x in P]


def poly_gcd_mod5(a,b):
    def trim(p):
        while p and p[-1] == 0:
            p.pop()
        return p
    a,b = trim([x % 5 for x in a]), trim([x % 5 for x in b])
    while b:
        r = a[:]
        inv = pow(b[-1], -1, 5)
        while r and len(r) >= len(b):
            shift = len(r)-len(b)
            factor = r[-1]*inv % 5
            for j,x in enumerate(b):
                r[j+shift] = (r[j+shift]-factor*x) % 5
            trim(r)
        a,b = b,r
    return [x*pow(a[-1],-1,5) % 5 for x in a]


def field_certificate():
    z = F([0,1],5)
    assert z**Q == z
    gcd = poly_gcd_mod5([-2]+[0]*15+[1], (z**(5**8)-z).c)
    assert gcd == [1]
    assert z**((Q-1)//2) == -1
    # Rabin's criterion: 2 is the only prime divisor of degree16.
    return {'degree':16, 'size':Q, 'polynomial':'z^16-2',
            'z_to_5_power_16_equals_z':True,
            'gcd_with_z_to_5_power_8_minus_z':gcd,
            'z_is_quadratic_nonresidue':True,
            'evidence':'EXACT_RABIN_IRREDUCIBILITY_CRITERION'}


def trace_orbit(P):
    modulus = P[0].m
    G = cm_group()
    multiples = [None]
    for _ in range(1,68):
        multiples.append(add(multiples[-1],P))
    assert add(multiples[-1],P) is None
    imaginary = [cm_i(R) for R in multiples]
    total = F(0,modulus)
    points = set()
    rho_counts = {}
    rows = []
    for a,b in G:
        R = add(multiples[a],imaginary[b])
        assert R is not None and on_curve(R)
        encoded = tuple(tuple(x.c) for x in R)
        points.add(encoded)
        rho = R[1]/(2*R[0])
        rho_counts[rho.c] = rho_counts.get(rho.c,0)+1
        term = 2*rho**5+289*rho
        total += term
        rows.append({'gaussian_action':[a,b], 'rho':list(rho.c),
                     'term':list(term.c)})
    assert len(points) == 512
    assert len(rho_counts) == 256 and set(rho_counts.values()) == {2}
    trace = total/2
    assert all(c == 0 for c in trace.c[1:])
    # Independent aggregation on the 256-element image, justified by the
    # checked two-to-one cover. Do not silently discard multiplicities.
    distinct_sum = sum((2*F(c,modulus)**5+289*F(c,modulus)
                        for c in rho_counts), F(0,modulus))
    assert trace == distinct_sum
    involution_point = gaussian(33,34,P)
    assert involution_point != P
    assert involution_point[1]/(2*involution_point[0]) == P[1]/(2*P[0])
    return trace, rows, {'action_occurrences':len(G),
                         'distinct_points':len(points),
                         'distinct_rho_values':len(rho_counts),
                         'rho_fiber_size':2,
                         'trace_is_in_base_ring':True,
                         'distinct_image_sum_agrees':True,
                         'involution_fixes_rho':True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--modulus',type=int,choices=(25,125),default=125)
    parser.add_argument('--seed',type=int,default=3402)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Use a fresh output path')
    start = time.monotonic()
    certificate = field_certificate()
    print('Irreducible residue field certified.',flush=True)
    residue, search = find_seed(args.seed)
    print('Primitive Gaussian 68-division point certified.',flush=True)
    P,lifting = lift_point(residue,args.modulus)
    print('Prime-to-5 torsion lift certified.',flush=True)
    trace, orbit, checks = trace_orbit(P)
    result = {'status':'EXACT_TRACE_RESIDUE_COMPUTED',
              'curve':'Y^2=X^3-1156X',
              'modulus':args.modulus, 'seed':args.seed,
              'field_certificate':certificate, 'i':57 % args.modulus,
              'search':search, 'residue_point':encode_point(residue),
              'lifted_point':encode_point(P), 'lifting':lifting,
              'primitive_annihilator':'68 Z[i]', 'orbit_checks':checks,
              'trace_unit_multiple':list(trace.c),
              'valuation_capped':valuation(trace),
              'v5_exactly_2':args.modulus == 125 and valuation(trace) == 2,
              'distinguished_trace_sign_or_unit_fixed':False,
              'sha_conclusion':'REQUIRES_THEOREM_AUDIT_AND_INDEPENDENT_REPLAY',
              'full_BSD_identity':'OPEN', 'orbit_terms':orbit,
              'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'cm_action_source_sha256':hashlib.sha256(Path(__file__).with_name('cm_action.py').read_bytes()).hexdigest(),
              'elapsed_seconds':time.monotonic()-start}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','modulus','trace_unit_multiple',
                     'valuation_capped','v5_exactly_2','orbit_checks','elapsed_seconds')},indent=2))


if __name__ == '__main__':
    main()
