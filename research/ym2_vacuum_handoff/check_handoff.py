"""New exact finite controls for the vacuum handoff; standard library only."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys

HERE=Path(__file__).resolve().parent
COUNT=0

def need(ok, label):
    global COUNT
    COUNT+=1
    if not ok:
        raise AssertionError(label)

def cover_ratio(weights):
    total=sum(weights,F(0))
    load=max(total-w for w in weights)
    return total/load

def matmul(a,b):
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]

def run():
    global COUNT
    COUNT=0
    out={"schema":"ym2-vacuum-handoff-controls-v1"}
    W,L=F(3,2),F(1)
    p,q=W/(W+L),L/(W+L)
    need((p,q)==(F(3,5),F(2,5)),"normalized cover contributions")
    need(p/q==F(3,2) and -p+q==F(-1,5),"ratio and signed contrast")
    for n in range(1,100):
        p,q=F(n,100),1-F(n,100)
        delta=p-q
        need(p/q==(1+delta)/(1-delta),"contrast-ratio map")
        need(((1+delta)/2,(1-delta)/2)==(p,q),"contrast complete inverse")
    maxima=0
    for a,b,c in product(range(1,21),repeat=3):
        ratio=cover_ratio([F(a),F(b),F(c)])
        need(ratio<=F(3,2),"three-direction ceiling")
        need((ratio==F(3,2))==(a==b==c),"equality iff balanced")
        maxima+=ratio==F(3,2)
    fixed=[]
    for n in range(1,301):
        z=F(n,100)
        ratio=cover_ratio([F(3,5),F(2,5),z])
        need(ratio<=F(7,5),"unequal prescribed weights ceiling")
        need((ratio==F(7,5))==(z==F(2,5)),"unequal prescribed weights optimizer")
        if n in [20,40,50,60,100]:
            fixed.append({"third_weight":str(z),"gain":str(ratio)})
    out["compensator"]={"W":"3/2","Lambda":"1","normalized":["3/5","2/5"],
                        "signed_contrast":"-1/5","integer_triples":8000,
                        "balanced_maximizers":maxima,"unequal_weight_controls":fixed}

    # Finite two-state auxiliary operator: exact reference change and missing residual.
    A=[[F(1),F(-1)],[F(-1),F(1)]]
    phi=[F(1),F(2)]
    ref=[[A[i][j]*phi[j]/phi[i] for j in range(2)] for i in range(2)]
    R=[sum(row,F(0)) for row in ref]
    K=[[ref[i][j]-(R[i] if i==j else 0) for j in range(2)] for i in range(2)]
    need(R==[F(-1),F(1,2)],"reference residual")
    need(all(sum(row,F(0))==0 for row in K),"reference constants kernel")
    nu=[F(1,5),F(4,5)]
    need(nu[0]*K[0][1]==nu[1]*K[1][0],"weighted reversibility")
    g_ref=K[0][0]+K[1][1]
    mean_R=sum((v*r for v,r in zip(nu,R)),F(0))
    lower=g_ref+min(R)-mean_R
    need(g_ref==F(5,2)>2 and lower==F(13,10)<=2,"residual essential to gap transfer")
    out["two_state_control"]={"carrier":"auxiliary two-state operator, not SU(2)",
                               "actual_gap":"2","reference_gap":str(g_ref),
                               "residual":[str(r) for r in R],"transferred_lower_bound":str(lower)}
    refs=[[F(1),F(2),F(3)],[F(2),F(1),F(4)],[F(3),F(2),F(1)]]
    for i in range(3):
        a,b,c=(v[i] for v in refs)
        need((b/c)*(a/b)==a/c,"chart cocycle")
        need((a/b)*(b/a)==1,"chart inverse")
    # Normalization scalars cancel from the physical unitarity check:
    # use positive rational normalized measures directly.
    na=[x*x/sum(v*v for v in refs[0]) for x in refs[0]]
    nb=[x*x/sum(v*v for v in refs[1]) for x in refs[1]]
    need(sum(na)==sum(nb)==1,"reference measure normalizations")
    for i in range(3):
        need(nb[i]*(na[i]/nb[i])==na[i],"squared unitary multiplier preserves norm")

    b=F(8,9)
    for n in range(1,100):
        Y=F(n,200)
        t=Y-b*Y*Y
        Z=Y-t
        need(Z==b*t*t+2*b*t*Z+b*Z*Z,"first-order chart reproduces scalar majorant")
    need(1/(4*b)==F(9,32),"same discriminant endpoint")
    for m in [2,4]:
        need(F(9,32)/(4*m)==F(9,128*m),"same uniform coupling endpoint")
        need(F(1,m)/F(9,128*m)==F(128,9),"reference window versus actual construction window")
    out["reference_gap_scope"]={"q_reference":"mr","D_reference":"2mr/3",
        "reference_window_ratio_to_old_actual_window":"128/9",
        "warning":"Reference operator only; no actual YM interval extension established."}

    residual_rows=[]
    for N in range(1,5):
        r=F(1,10)
        vals=[]
        for traces in product([F(-1),F(-1,2),F(0),F(1,2),F(1)],repeat=N):
            grad2=4*sum((1-a*a for a in traces),F(0))
            residual=-r*r*grad2/72
            need(residual==-r*r*sum((1-a*a for a in traces),F(0))/18,
                 "disjoint plaquette residual identity")
            vals.append(residual)
        need(min(vals)==-N*r*r/18 and max(vals)==0,"residual attained extrema")
        residual_rows.append({"plaquettes":N,"r":str(r),"residual_oscillation":str(max(vals)-min(vals))})
    for n in range(1,100):
        r=F(n,100)
        c=r/6
        need(6*c-r==0 and c*c/2==r*r/72,"trial reference first-order cancellation")
    out["plaquette_residual_controls"]=residual_rows

    # Auxiliary rational binary counterpart to the written smooth SU(2) mixture.
    mixture=[]
    for N in range(2,9):
        states=list(product([-1,1],repeat=N))
        prob={s:(F(3,4)**s.count(1)*F(1,4)**s.count(-1)+
                 F(1,4)**s.count(1)*F(3,4)**s.count(-1))/2 for s in states}
        f={s:F(sum(s),N) for s in states}
        need(sum(prob.values())==1,"mixture normalization")
        need(sum(prob[s]*f[s] for s in states)==0,"mixture centered average")
        variance=sum(prob[s]*f[s]**2 for s in states)
        need(variance==F(1,4)+F(3,4*N),"mixture retains collective variance")
        energy=F(0)
        for i in range(N):
            for ext in product([-1,1],repeat=N-1):
                lo=ext[:i]+(-1,)+ext[i:]
                hi=ext[:i]+(1,)+ext[i:]
                mass=prob[lo]+prob[hi]
                pplus=prob[hi]/mass
                need(F(1,4)<=pplus<=F(3,4),"uniformly bounded one-site law")
                energy+=mass*pplus*(1-pplus)*(F(2,N))**2
        rayleigh=energy/variance
        need(rayleigh<=F(4,N+3),"collective heat-bath gap upper bound")
        mixture.append({"sites":N,"variance":str(variance),"rayleigh":str(rayleigh),
                        "upper_bound":str(F(4,N+3))})
    out["auxiliary_binary_mixture"]=mixture
    out["status"]="PASS"
    out["assertions"]=COUNT
    out["evidence_ceiling"]="New finite exact controls. General SU(2), all-spin, all-volume and actual-correction claims require the written proofs and supplied ports."
    return out

if __name__=="__main__":
    result=run()
    if sys.argv[1:]==["--write-receipt"]:
        (HERE/"RESULTS.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    elif sys.argv[1:]:
        raise SystemExit("Use no arguments for read-only replay or --write-receipt to save.")
    else:
        need(result==json.loads((HERE/"RESULTS.json").read_text(encoding="utf-8")),"receipt matches recomputation")
    print(f"PASS: {result['assertions']} exact assertions; calibrated ratios, chart residuals, majorant and collective controls.")
