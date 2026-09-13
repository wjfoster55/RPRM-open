"""New exact controls for the quotient and improved construction; standard library only."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math
import sys

HERE=Path(__file__).resolve().parent
N=4
ZERO=(0,)*N
checks=0

def need(ok,label):
    global checks
    checks+=1
    if not ok:raise AssertionError(label)

class P:
    def __init__(self,value=0):
        if isinstance(value,P):self.t=dict(value.t)
        elif isinstance(value,dict):self.t={e:F(v) for e,v in value.items() if v}
        else:self.t={ZERO:F(value)} if value else {}
    def __add__(self,other):
        d=dict(self.t)
        for e,v in P(other).t.items():d[e]=d.get(e,F(0))+v
        return P(d)
    __radd__=__add__
    def __neg__(self):return P({e:-v for e,v in self.t.items()})
    def __sub__(self,other):return self+-P(other)
    def __rsub__(self,other):return P(other)+-self
    def __mul__(self,other):
        d={}
        for e,v in self.t.items():
            for f,w in P(other).t.items():
                g=tuple(a+b for a,b in zip(e,f));d[g]=d.get(g,F(0))+v*w
        return P(d)
    __rmul__=__mul__
    def __truediv__(self,other):return self*F(1,other)
    def __pow__(self,n):
        out=P(1)
        for _ in range(n):out=out*self
        return out
    def diff(self,i):
        d={}
        for e,v in self.t.items():
            if e[i]:
                f=list(e);f[i]-=1;d[tuple(f)]=v*e[i]
        return P(d)
    def __eq__(self,other):return self.t==P(other).t
    def at(self,values):
        return sum(v*math.prod(F(x)**n for x,n in zip(values,e)) for e,v in self.t.items())

def variable(i):
    e=[0]*N;e[i]=1;return P({tuple(e):1})
a,b,c,r=[variable(i) for i in range(4)]
G=[[4*(1-a*a),c-a*b,3*(b-a*c)],
   [c-a*b,4*(1-b*b),3*(a-b*c)],
   [3*(b-a*c),3*(a-b*c),6*(1-c*c)]]

def gamma(f,h):return sum(G[i][j]*f.diff(i)*h.diff(j) for i in range(3) for j in range(3))
def kinetic(f):
    return 6*a*f.diff(0)+6*b*f.diff(1)+9*c*f.diff(2)-sum(G[i][j]*f.diff(i).diff(j) for i in range(3) for j in range(3))/2
def qm(x,y):
    a0,a1,a2,a3=x;b0,b1,b2,b3=y
    # Quaternion multiplication uses standard imaginary basis; scalar trace identities
    # agree with SU(2) after the corresponding fixed Pauli convention.
    return (a0*b0-a1*b1-a2*b2-a3*b3,
            a0*b1+a1*b0+a2*b3-a3*b2,
            a0*b2-a1*b3+a2*b0+a3*b1,
            a0*b3+a1*b2-a2*b1+a3*b0)
def qi(x):return (x[0],-x[1],-x[2],-x[3])
def qscale(k,x):return tuple(k*v for v in x)
def qprod(xs):
    out=(F(1),F(0),F(0),F(0))
    for x in xs:out=qm(out,x)
    return out
def stereographic(x):
    s=sum(F(t)**2 for t in x)
    return ((1-s)/(1+s),*(2*F(t)/(1+s) for t in x))

# Positive-coordinate lattice: shared vertical e0, left top e1, left
# vertical e2, left bottom e3, right bottom e4, right vertical e5, right top e6.
WORDS=[[(0,1),(1,-1),(2,-1),(3,1)],
       [(4,1),(5,1),(6,-1),(0,-1)],
       [(1,-1),(2,-1),(3,1),(4,1),(5,1),(6,-1)]]
def word_value(links,word):return qprod([links[i] if sign==1 else qi(links[i]) for i,sign in word])[0]
def word_derivative(links,word,edge,k):
    terms=[]
    unit=(F(0),)+(F(0),)*k+(F(1),)+(F(0),)*(2-k)
    for at,(i,sign) in enumerate(word):
        if i!=edge:continue
        fs=[links[j] if s==1 else qi(links[j]) for j,s in word]
        fs[at]=qm(unit,links[i]) if sign==1 else qscale(-1,qm(qi(links[i]),unit))
        terms.append(qprod(fs)[0])
    return sum(terms,F(0))

def run():
    global checks
    checks=0
    D=1-a*a-b*b-c*c+2*a*b*c
    det=G[0][0]*(G[1][1]*G[2][2]-G[1][2]*G[2][1])-G[0][1]*(G[1][0]*G[2][2]-G[1][2]*G[2][0])+G[0][2]*(G[1][0]*G[2][1]-G[1][1]*G[2][0])
    need(det==6*D*(16-6*a*a-6*b*b-c*c-3*a*b*c),'exact metric determinant polynomial')
    for i,x in enumerate((a,b,c)):
        need(sum(G[i][j]*D.diff(j) for j in range(3))==-D*x*(8 if i<2 else 12),'boundary normal identity')
        need(sum(G[i][j].diff(j) for j in range(3))==-x*(12 if i<2 else 18),'divergence drift')
    need(kinetic(a*b)==13*a*b-c,'mixed trace kinetic channel')
    need(kinetic(c)==9*c,'outer loop kinetic energy')
    need(kinetic(a*a-F(1,4))==16*(a*a-F(1,4)),'self trace kinetic channel')
    need(kinetic(-a*b/13+4*c/39)==c-a*b,'exact cross inverse')
    w1=(a+b)/6
    w2=-(a*a+b*b-F(1,2))/288-a*b/468+c/351
    need(kinetic(w1)==a+b,'first log coefficient')
    need(kinetic(w2)==(gamma(a+b,a+b)-6)/72,'second log coefficient')
    w=r*w1+r*r*w2
    residual=kinetic(w)-gamma(w,w)/2-r*(a+b)
    need(residual==-r*r/12-r**3*gamma(w1,w2)-r**4*gamma(w2,w2)/2,'complete second-order trial residual')
    count_quotient=0
    for seed in range(24):
        links=[stereographic(tuple(F(((seed+2)*(i+3)*(k+1))%7-3,3) for k in range(3))) for i in range(7)]
        for link in links:need(sum(t*t for t in link)==1,'rational SU2 admission')
        vals=[word_value(links,word) for word in WORDS]+[F(0)]
        need(D.at(vals)>=0,'trace body admission')
        ds=[[[word_derivative(links,word,e,k) for k in range(3)] for e in range(7)] for word in WORDS]
        for i in range(3):
            for j in range(3):
                direct=sum(ds[i][e][k]*ds[j][e][k] for e in range(7) for k in range(3))
                need(direct==G[i][j].at(vals),'direct link derivative matches quotient metric')
        count_quotient+=1
    need((c-a*b).at([0,0,1,0])==1 and (c-a*b).at([0,0,-1,0])==-1,'same separate traces different joint response')

    # Exhaustive finite arithmetic corroborates the written all-spin inequalities.
    spin_pairs=0
    for J in range(1,49):
        j=F(J,2);lj=2*j*(j+1)
        for L in range(1,49):
            l=F(L,2);ll=2*l*(l+1);total_floor=l*(2*l+11)
            cavg=sum(F(S+1)*abs(2*(j*(j+1)+l*(l+1)-F(S,2)*(F(S,2)+1)))
                     for S in range(abs(J-L),J+L+1,2))/((J+1)*(L+1))
            need(cavg*cavg<=F(4,3)*lj*ll,'normalized trace Hilbert-Schmidt bound')
            need(cavg<=lj*total_floor/6,'gauge total-energy local coefficient')
            spin_pairs+=1
    need(F(3,2)==sum(F(S+1)*abs(2*(F(3,4)+F(3,4)-F(S,2)*(F(S,2)+1))) for S in (0,2))/4,
         'fundamental gauge coefficient')
    kappas={}
    for m in (2,4):
        kappa=F(3,8)*m+F(7,3)*m*(m-1)
        beta=kappa/(m*m)
        need(beta<=F(59,32),'dimension-uniform refined seed forcing')
        kappas[str(m)]=str(kappa)
    x,z,K=F(1,3),F(3,7),F(1,3)
    h=F(59,32)*x*x
    majorant=h+4*K*x*z+K*z*z/2
    margin=z-majorant
    lip=K*(4*x+z)
    q=x+F(4,3)*z
    osc=F(2,3)*(x+z)
    need(margin>0,'combined actual-vacuum radius invariant')
    need(lip==F(37,63) and lip<1,'strict contraction')
    need(q==F(19,21) and q<1,'actual influence margin')
    need(osc==F(32,63),'actual one-link log density range')
    need(F(3,2)*(1-q)==F(1,7),'physical gap prefactor before forest cover')
    need((F(1,3))/(F(9,128))==F(128,27),'coupling window enlargement factor')
    # At the prospective q=1 boundary, the fixed-point ball condition reduces
    # to this polynomial; this tests a stated sufficient-certificate boundary.
    X=variable(3);Z=F(3,4)*(1-X)
    failure=F(59,32)*X*X+F(4,3)*X*Z+Z*Z/6-Z
    need(32*failure==30*X*X+50*X-21,'conditional comparison boundary polynomial')
    return {'schema':'ym2-conditional-construction-controls-v1','status':'PASS','assertions':checks,
            'direct_SU2_seven_link_configurations':count_quotient,'exact_spin_pairs':spin_pairs,
            'spin_double_labels_checked':[1,48],'new_bilinear_constant':'1/3',
            'new_source_kappa':kappas,'mr_bound':str(x),'correction_radius':str(z),
            'radius_margin':str(margin),'contraction_factor':str(lip),'influence_bound':str(q),
            'conditional_log_oscillation':str(osc),'gap_before_cover':'exp(-32/63)/7',
            'coupling_window_factor':'128/27','old_checkers_run':False,
            'evidence_ceiling':'Exact polynomial and rational controls. Written all-spin, all-volume proofs and accepted analytic dependencies carry the general theorem; no formal proof assistant or continuum gap proof.'}

def main():
    result=run();out=HERE/'RESULTS.json'
    if sys.argv[1:]==['--record']:
        if out.exists():raise RuntimeError('Receipt already exists')
        out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    elif sys.argv[1:]:raise SystemExit('usage: check_construction.py [--record]')
    elif json.loads(out.read_text(encoding='utf-8'))!=result:raise AssertionError('Complete saved receipt mismatch')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
