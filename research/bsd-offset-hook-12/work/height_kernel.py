"""Fresh E34 canonical-height distance enclosures and exact basis controls.

Standard-library rational arithmetic; no saved heights, L-values or database input.
The uniform canonical-height tail theorem is an attributed written dependency.
"""
import argparse
from datetime import datetime,timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import gcd,isqrt
from pathlib import Path
import json

A=1156
C0=5345344
C1=1338649
DEPTH=8
TERMS=48
MANTISSA_BITS=96


def require(condition,message):
    if not condition:raise AssertionError(message)


def admit(P):
    if P is not None:
        x,y=P
        require(y*y==x*x*x-A*x,'point admission')


def negate(P):return None if P is None else (P[0],-P[1])


def add(P,Q):
    admit(P);admit(Q)
    if P is None:return Q
    if Q is None:return P
    x,y=P;z,w=Q
    if x==z and y==-w:return None
    slope=(3*x*x-A)/(2*y) if P==Q else (w-y)/(z-x)
    xx=slope*slope-x-z
    R=(xx,slope*(x-xx)-y)
    admit(R)
    return R


def coords(P):return (1,0) if P is None else (P[0].numerator,P[0].denominator)


def ln_small(r):
    require(1<=r<=2,'normalized log domain')
    z=(r-1)/(r+1);term=z;total=F(0)
    for j in range(TERMS):
        total+=2*term/(2*j+1)
        term*=z*z
    tail=2*term/((2*TERMS+1)*(1-z*z))
    return total,total+tail


LN2=ln_small(F(2))


def ln_integer(h):
    require(h>=1,'positive logarithm integer')
    e=h.bit_length()-1
    if e<=MANTISSA_BITS:
        low=high=F(h,1<<e)
    else:
        m=h>>(e-MANTISSA_BITS)
        low=F(m,1<<MANTISSA_BITS)
        high=F(m+1,1<<MANTISSA_BITS)
    ll=ln_small(low)[0];uu=ln_small(high)[1]
    return e*LN2[0]+ll,e*LN2[1]+uu


def plus(x,y):return x[0]+y[0],x[1]+y[1]
def minus(x,y):return x[0]-y[1],x[1]-y[0]
def scale(x,a):return (x[0]*a,x[1]*a) if a>=0 else (x[1]*a,x[0]*a)
def times(x,y):
    products=[a*b for a in x for b in y]
    return min(products),max(products)
def square(x):
    lo,hi=x
    return (F(0) if lo<=0<=hi else min(lo*lo,hi*hi),max(lo*lo,hi*hi))
def intersect(x,y):
    result=max(x[0],y[0]),min(x[1],y[1])
    require(result[0]<=result[1],'certified intervals incompatible')
    return result


def decimal_interval(x,digits=10):
    unit=10**digits
    low=(x[0].numerator*unit)//x[0].denominator
    high=-((-x[1].numerator*unit)//x[1].denominator)
    def show(n):
        sign='-' if n<0 else '';n=abs(n)
        return sign+str(n//unit)+'.'+str(n%unit).zfill(digits)
    return [show(low),show(high)]


def sqrt_interval(x,digits=10):
    require(x[0]>=0,'sqrt interval lower endpoint')
    unit=10**digits
    lo=isqrt(x[0].numerator*unit*unit//x[0].denominator)
    hi=isqrt(x[1].numerator*unit*unit//x[1].denominator)
    if hi*hi*x[1].denominator<x[1].numerator*unit*unit:hi+=1
    return F(lo,unit),F(hi,unit)


def height(P):
    admit(P);a,b=coords(P);rows=[];chord=P
    for j in range(DEPTH):
        h=max(abs(a),b)
        ff=(a*a+A*b*b)**2;gg=4*a*b*(a*a-A*b*b)
        g=gcd(ff,gg);m=max(ff,abs(gg))
        require(g>0 and C0%g==0,'gcd bound')
        require(h**4<=m<=C1*h**4,'raw height bound')
        aa,bb=ff//g,gg//g
        if bb<0:aa,bb=-aa,-bb
        require(gcd(aa,bb)==1 and bb>=0,'primitive output')
        if j<3:
            chord=add(chord,chord)
            require((aa,bb)==coords(chord),'independent chord readback')
        rows.append({'j':j,'gcd':g,'H_before_bits':h.bit_length(),
                     'H_after_bits':max(abs(aa),bb).bit_length(),
                     'chord_checked':j<3})
        a,b=aa,bb
    h=max(abs(a),b);lk=scale(ln_integer(h),F(1,4**DEPTH))
    lower=lk[0]-ln_integer(C0)[1]/(3*4**DEPTH)
    upper=lk[1]+ln_integer(C1)[1]/(3*4**DEPTH)
    # Nonnegativity is a canonical-height theorem, not inferred from a sample.
    result=max(F(0),lower),upper
    return result,{'initial_point':None if P is None else list(map(str,P)),
                   'depth':DEPTH,'steps':rows,'last_primitive_x_hex':[hex(a),hex(b)],
                   'height_interval':decimal_interval(result)}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args()
    if args.output.exists():raise FileExistsError('Use a new evidence path')
    P=(F(-2),F(48));Q=(F(-16),F(120))
    S=add(P,Q);T=add(P,negate(Q))
    require(T==(F(162),F(-2016)),'computed P-Q')
    require(add(T,Q)==P,'difference readback')
    points={'P':P,'Q':Q,'PplusQ':S,'PminusQ':T,'O':None,
            'T0':(F(0),F(0)),'Tplus':(F(34),F(0)),'Tminus':(F(-34),F(0))}
    intervals={};ledgers={}
    for name,point in points.items():
        intervals[name],ledgers[name]=height(point)
        print('height completed: '+name,flush=True)
    p,q,s,d=(intervals[name] for name in ('P','Q','PplusQ','PminusQ'))
    pair_from_distance=scale(minus(plus(p,q),d),F(1,2))
    pair_from_sum=scale(minus(s,plus(p,q)),F(1,2))
    pairing=intersect(pair_from_distance,pair_from_sum)
    regulator=minus(times(p,q),square(pairing))
    parallelogram=minus(plus(s,d),scale(plus(p,q),2))
    require(parallelogram[0]<=0<=parallelogram[1],'parallelogram consistency')
    for name in ('O','T0','Tplus','Tminus'):
        require(intervals[name][0]==0,'torsion height enclosure')
    # Exact rational basis-change controls in a supplied positive Gram model.
    pp,qq,bb=F(2),F(3),F(1,2);rr=pp*qq-bb*bb
    matrix_cases=0;unimodular=0
    for aa,cc,ee,ff in product(range(-2,3),repeat=4):
        pnew=aa*aa*pp+2*aa*cc*bb+cc*cc*qq
        qnew=ee*ee*pp+2*ee*ff*bb+ff*ff*qq
        bnew=aa*ee*pp+(aa*ff+cc*ee)*bb+cc*ff*qq
        det=aa*ff-cc*ee
        require(pnew*qnew-bnew*bnew==det*det*rr,'determinant transport')
        matrix_cases+=1;unimodular+=abs(det)==1
    shear=[]
    for n in range(-3,4):
        qn=plus(plus(q,scale(pairing,2*n)),scale(p,n*n))
        bn=plus(pairing,scale(p,n))
        dn=minus(plus(p,qn),scale(bn,2))
        # These intervals are transports through a proved pairing law.
        shear.append({'n':n,'basis':'P,Q+nP','squared_distance_interval':decimal_interval(dn),
                      'regulator':'exactly unchanged by determinant-one basis transport'})
    result={'created_utc':datetime.now(timezone.utc).isoformat(),
        'status':'CERTIFIED_HEIGHT_DISTANCE_AND_BASIS_CONTROLS_COMPLETED',
        'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'curve':'y^2=x^3-1156x','height_convention':'full limit 4^-k log H_x(2^k P)',
        'parameters':{'depth':DEPTH,'atanh_terms':TERMS,'mantissa_bits':MANTISSA_BITS,
                      'C0':C0,'C1':C1},'point_ledgers':ledgers,
        'arithmetic_seam':{'squared_distance':decimal_interval(d),
             'distance':decimal_interval(sqrt_interval(d)),
             'pairing_from_difference':decimal_interval(pair_from_distance),
             'pairing_from_sum':decimal_interval(pair_from_sum),
             'pairing_intersection':decimal_interval(pairing),
             'regulator':decimal_interval(regulator),
             'regulator_positive_certified':regulator[0]>0,
             'area':decimal_interval(sqrt_interval(regulator)) if regulator[0]>=0 else None,
             'parallelogram_residual_enclosure':decimal_interval(parallelogram),
             'parallelogram_reason':'Quadratic-height theorem; interval overlap is a consistency check only'},
        'basis_controls':{'integer_matrices':matrix_cases,'unimodular_matrices':unimodular,
                          'shear_intervals':shear,
                          'Q_reversal':'B changes sign, D becomes H(P+Q), regulator unchanged'},
        'scope':'Independent arithmetic distance and pairing enclosure; no analytic coefficient, Sha order or full BSD identity computed',
        'full_BSD_or_general_closure':'OPEN'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'seam':result['arithmetic_seam'],
                      'integer_matrix_controls':matrix_cases},indent=2))


if __name__=='__main__':main()
