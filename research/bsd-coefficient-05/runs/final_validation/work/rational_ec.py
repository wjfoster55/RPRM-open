"""Exact rational group arithmetic on the fixed E34 model."""
from fractions import Fraction as Q
from math import gcd, isqrt


def point(x,y):
    P=(Q(x),Q(y))
    if not on_curve(P):
        raise ValueError('Point is not on E34')
    return P


def on_curve(P):
    return P is None or P[1]**2 == P[0]**3-1156*P[0]


def neg(P):
    return None if P is None else (P[0],-P[1])


def add(P,R):
    if P is None:return R
    if R is None:return P
    x,y=P; u,v=R
    if x == u:
        if y == -v:return None
        assert y == v and y != 0
        slope=(3*x*x-1156)/(2*y)
    else:slope=(v-y)/(u-x)
    X=slope*slope-x-u
    result=(X,slope*(x-X)-y)
    assert on_curve(result)
    return result


def mul(n,P):
    if n<0:return mul(-n,neg(P))
    R=None
    while n:
        if n&1:R=add(R,P)
        n//=2
        if n:P=add(P,P)
    return R


def primitive_integral(P):
    if P is None:raise ValueError('Infinity has no affine denominator triple')
    x,y=P
    d=isqrt(x.denominator)
    assert d*d == x.denominator
    a=x.numerator
    b=y*d**3
    assert b.denominator == 1
    b=b.numerator
    assert d>0 and gcd(a,d)==gcd(b,d)==1
    assert b*b == a**3-1156*a*d**4
    return a,b,d


def encode(P):
    return None if P is None else [str(c) for c in P]


def valuation_integer(n,p):
    if not n:raise ValueError('Zero has infinite valuation')
    n=abs(n);v=0
    while n%p==0:n//=p;v+=1
    return v


def valuation(q,p):
    q=Q(q)
    return valuation_integer(q.numerator,p)-valuation_integer(q.denominator,p)


def residue(q,m):
    q=Q(q)
    return q.numerator*pow(q.denominator,-1,m)%m
