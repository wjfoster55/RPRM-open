"""Fresh rational arithmetic and exact finite readback of BKS reciprocity.

Standard library only. Finite congruences rely on the written sigma/log
proof and classical measure error bound, not on agreement of decimals.
"""
from fractions import Fraction as F
from math import gcd, isqrt
from pathlib import Path
import argparse
import hashlib
import json

MOD = 125

def point(x, y):
    R = (F(x), F(y))
    assert R[1]**2 == R[0]**3 - 1156*R[0]
    return R

def neg(R):
    return None if R is None else (R[0], -R[1])

def add(R, S):
    if R is None: return S
    if S is None: return R
    x, y = R; u, v = S
    if x == u:
        if y == -v: return None
        assert y == v and y != 0
        m = (3*x*x - 1156)/(2*y)
    else: m = (v-y)/(u-x)
    X = m*m-x-u
    return point(X, m*(x-X)-y)

def mul(n, R):
    if n < 0: return mul(-n, neg(R))
    S = None
    while n:
        if n & 1: S = add(S, R)
        n //= 2
        if n: R = add(R, R)
    return S

def res(x, modulus=MOD):
    x = F(x)
    return x.numerator * pow(x.denominator, -1, modulus) % modulus

def valint(n):
    if not n: return None
    n = abs(n); v = 0
    while n % 5 == 0: n //= 5; v += 1
    return v

def valuation(x):
    x = F(x)
    return None if not x else valint(x.numerator)-valint(x.denominator)

def encode(R):
    return None if R is None else list(map(str, R))

def height_and_log(R):
    S = mul(8, R)
    if S is None:
        return 0, 0, {"point": encode(R), "eight_times_point": None,
                      "height_mod125": 0, "log_div5_mod125": 0,
                      "reason": "torsion killed by 8, including identity"}
    x,y = S; d = isqrt(x.denominator)
    assert d*d == x.denominator and d > 0
    a = x.numerator; b = y*d**3
    assert b.denominator == 1
    b = b.numerator
    assert gcd(a,d) == gcd(b,d) == 1
    assert b*b == a**3 - 1156*a*d**4
    t = -x/y; u = t/d
    assert u == -F(a,b) and valuation(u) == 0 and valuation(t) >= 1
    component_checks = []
    for p in (2,17):
        if d % p == 0:
            component_checks.append({"p":p,"reduction":"O","smooth":True})
        else:
            xp=a*pow(d,-2,p)%p; yp=b*pow(d,-3,p)%p
            grad=((-3*xp*xp+1156)%p,2*yp%p)
            assert grad != (0,0)
            component_checks.append({"p":p,"reduction":[xp,yp],"gradient":grad})
    # log(u) = log(u^4)/4, exact log(5)=0 convention.
    # z^k/k for k>=4 has v5>=4. Sigma correction has v5>=4.
    # After dividing by 5*8^2, both errors lie in125 Z5.
    u625 = res(u,625); z = pow(u625,4,625)-1
    assert z % 5 == 0
    log_trunc = F(z)-F(z*z,2)+F(z*z*z,3)
    h = res(log_trunc/(20*64))
    # Evaluated formal-log tail v5>=5v5(t)-1, then divide by8*5.
    ell_div5 = res(t/40)
    return h,ell_div5, {"point":encode(R),"eight_times_point":encode(S),
        "a":str(a),"b":str(b),"d":str(d),"t":str(t),"v5_t":valuation(t),
        "u_mod625":u625,"z_mod625":z,"height_mod125":h,
        "log_div5_mod125":ell_div5,"bad_component_checks":component_checks,
        "height_error_in":"125 Z5","log_div5_error_in":"125 Z5"}

def det(A): return (A[0][0]*A[1][1]-A[0][1]*A[1][0]) % MOD
def adj(A): return [[A[1][1]%MOD,-A[0][1]%MOD],[-A[1][0]%MOD,A[0][0]%MOD]]
def mv(A,v): return [sum(a*x for a,x in zip(row,v))%MOD for row in A]
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(2))%MOD for j in range(2)] for i in range(2)]
def transpose(A): return list(map(list,zip(*A)))
def scale(c,v): return [c*x%MOD for x in v]
def solve(A,v):
    d = det(A)
    if d%5 == 0: raise ValueError("Gram determinant is not a 5-adic unit")
    return scale(pow(d,-1,MOD),mv(adj(A),v))

def parse_analytic(path):
    raw=path.read_text(encoding="utf-8")
    assert "END_RELATION_10_ANALYTIC" in raw and "***" not in raw
    rows={}
    for line in raw.splitlines():
        if line.startswith("PADIC|"):
            _,key,precision,value=line.split("|")
            rows[key]={"precision":int(precision),"residue_mod125":int(value)%MOD}
    for key in ("classical_b2","overconvergent_b2","five_C","log6_div5"):
        assert rows[key]["precision"] >= 3
    assert rows["classical_b2"]["residue_mod125"] == rows["overconvergent_b2"]["residue_mod125"]
    return rows

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--analytic-log",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists(): raise FileExistsError("Preserve earlier evidence")
    P=point(-2,48); Q=point(-16,120)
    hp,lp,p_row=height_and_log(P); hq,lq,q_row=height_and_log(Q)
    hs,ls,s_row=height_and_log(add(P,Q))
    G=[[-2*hp%MOD,(hp+hq-hs)%MOD],[(hp+hq-hs)%MOD,-2*hq%MOD]]
    ell5=[lp,lq]; regulator=det(G)
    assert regulator%5 != 0
    tests=[]
    for a,b in ((1,-1),(2,0),(0,2),(1,2),(-1,0),(0,0)):
        R=add(mul(a,P),mul(b,Q)); h,l,row=height_and_log(R)
        expected_h=(a*a*hp+b*b*hq+a*b*(hs-hp-hq))%MOD
        expected_l=(a*lp+b*lq)%MOD
        assert (h,l)==(expected_h,expected_l)
        tests.append({"coefficients":[a,b],"height":h,"log_div5":l,"details":row})
    torsion_tests=[]
    for T in (point(0,0),point(34,0),point(-34,0),None):
        assert add(T,T) is None
        assert height_and_log(T)[:2]==(0,0)
        assert height_and_log(add(P,T))[:2]==(hp,lp)
        torsion_tests.append(encode(T))
    counts={str(p):1+sum(1 for x in range(p) for y in range(p) if (y*y-x**3+1156*x)%p==0) for p in (3,5)}
    a5=6-counts["5"]; a3=4-counts["3"]
    assert (64*34**6)%5 != 0 and a5%5 != 0
    assert all((x*x-a3*x+3)%5 != 0 for x in range(5))
    analytic=parse_analytic(args.analytic_log)
    b2=analytic["classical_b2"]["residue_mod125"]
    five_C=analytic["five_C"]["residue_mod125"]
    d=analytic["log6_div5"]["residue_mod125"]
    A=five_C*b2*d*d%MOD
    five_lambda=A*pow(regulator,-1,MOD)%MOD
    W5=mv(adj(G),ell5)
    K=scale(five_lambda,W5)
    assert K==scale(A,solve(G,ell5))
    assert mv(G,K)==scale(A,ell5)
    covariance=[]
    for U in ([[1,0],[0,-1]],[[1,3],[0,1]],[[0,1],[1,0]],[[2,0],[0,1]]):
        Gu=mm(mm(transpose(U),G),U); lu=mv(transpose(U),ell5)
        Ku=scale(A,solve(Gu,lu)); old=mv(U,Ku)
        assert old==K
        Wu=mv(U,mv(adj(Gu),lu))
        assert Wu==scale(det(U)**2,W5)
        covariance.append({"basis_columns":U,"K_new_coordinates":Ku,"K_in_original_basis":old,
                           "W_div5_in_original_basis":Wu,"determinant":det(U)})
    singular_rejected=False
    try: solve([[1,1],[1,1]],[1,1])
    except ValueError: singular_rejected=True
    assert singular_rejected
    # K and K+125P share finite readout but are different exact vectors.
    assert [(K[0]+125)%125,K[1]%125]==K
    result={"status":"EXACT_FINITE_RECIPROCITY_READBACK","curve":"y^2=x^3-1156x",
       "modulus":MOD,"basis":[encode(P),encode(Q)],"G_mod125":G,"regulator_mod125":regulator,
       "ell_div5_mod125":ell5,"W_div5_mod125":W5,"analytic":analytic,
       "five_lambda_mod125":five_lambda,"A_five_C_b2_d_squared_mod125":A,
       "canonical_component_MST_class_mod125":K,"class_fiber":{"kind":"MANY","description":f"{K[0]}P+{K[1]}Q+125M"},
       "arithmetic_rows":{"P":p_row,"Q":q_row,"P+Q":s_row},"linear_quadratic_controls":tests,
       "torsion_controls":torsion_tests,"point_counts":counts,"a5":a5,"a3":a3,
       "irreducibility_control":"Frobenius3 polynomial has no root modulo5",
       "basis_controls":covariance,"singular_inversion_rejected":singular_rejected,
       "wrong_normalization_controls":{"omit_twist_factor_2":scale(2,K),
                                       "use_all_component_period":scale(pow(2,-1,MOD),K)},
       "new_precision_basis":"CM sigma uniqueness and evaluated formal-log tail",
       "canonical_class_computed_independently_from_Kato_cochains":False,
       "theorem_dependencies":["MST1.3 and1.1","BKS5.6,6.2","previous rank/saturation/Sha5 admission"],
       "complex_BSD_identity":"OPEN","total_Sha":"OPEN",
       "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       "analytic_log_sha256":hashlib.sha256(args.analytic_log.read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("status","G_mod125","regulator_mod125","ell_div5_mod125",
                       "W_div5_mod125","five_lambda_mod125","canonical_component_MST_class_mod125",
                       "complex_BSD_identity")},indent=2))

if __name__=="__main__": main()
