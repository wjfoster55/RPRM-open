"""Fresh exact controls, standard library only. Prints JSON; writes nothing.

Sparse integer contractions independently check the new dense matrix probe.
Written proofs, not the number of assertions, supply general coverage.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json

HERE=Path(__file__).resolve().parent
assertions=0
def need(ok, message):
    global assertions
    assertions+=1
    if not ok: raise AssertionError(message)
def plus(A,B):
    C=dict(A)
    for k,v in B.items(): C[k]=C.get(k,0)+v
    return {k:v for k,v in C.items() if v}
def mul(A,B):
    rows={}
    for (k,j),v in B.items(): rows.setdefault(k,[]).append((j,v))
    C={}
    for (i,k),v in A.items():
        for j,w in rows.get(k,()): C[i,j]=C.get((i,j),0)+v*w
    return {k:v for k,v in C.items() if v}
def scale(A,k): return {p:v*k for p,v in A.items() if v*k}
def transpose(A): return {(j,i):v for (i,j),v in A.items()}
def tr(A): return sum(v for (i,j),v in A.items() if i==j)
def encode(ds,base=2):
    n=0
    for d in ds:n=base*n+d
    return n
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def signs(vertices):
    ans=[]
    for a,b in zip(vertices,vertices[1:]+vertices[:1]):
        dif=[y-x for x,y in zip(a,b) if x!=y]
        need(len(dif)==1 and abs(dif[0])==1,'admitted lattice edge')
        ans.append(dif[0])
    return ans
def indices(v,sgn):
    pairs=[(v[i],v[(i+1)%4]) if s>0 else (v[(i+1)%4],v[i])
           for i,s in enumerate(sgn)]
    return tuple(a for a,b in pairs),tuple(b for a,b in pairs)
def coefficient(p,q):
    v=(0,0,0);w=(1,0,0)
    sp=signs([v,w,add(w,p),add(v,p)])
    sq=signs([w,v,add(v,q),add(w,q)])
    B={}
    for ip in product(range(2),repeat=4):
        for iq in product(range(2),repeat=4):
            rp,cp=indices(ip,sp);rq,cq=indices(iq,sq)
            k=(encode(cp[:1]+cq[:1]+cp[1:]+cq[1:]),
               encode(rp[:1]+rq[:1]+rp[1:]+rq[1:]))
            B[k]=B.get(k,0)+1
    return B
def matrix_controls():
    p0={(a*64+k,b*64+k):1 for a in (0,3) for b in (0,3) for k in range(64)}
    p1=plus({(i,i):2 for i in range(256)},scale(p0,-1))
    records=[]
    for p,q,kind in [((0,1,0),(0,-1,0),'opposite'),
                     ((0,1,0),(0,0,-1),'opposite'),
                     ((0,1,0),(0,0,1),'same'),
                     ((0,-1,0),(0,0,-1),'same')]:
        B=coefficient(p,q)
        for ell,P in enumerate((p0,p1)):
            C=mul(mul(P,B),P); G=mul(transpose(C),C)
            rank,eigen,hs=((16,16,1),(16,144,9))[ell] if kind=='opposite' else ((4,64,1),(12,192,9))[ell]
            need(mul(G,G)==scale(G,eigen),'exact Gram minimal polynomial')
            need(tr(G)==256*hs,'exact Hilbert-Schmidt norm')
            need(F(tr(G),eigen)==rank,'exact rank from positive Gram')
            records.append({'pattern':kind,'spin':ell,'rank':rank,
                            'singular_value_squared':str(F(eigen,256))})
    C={}
    for a,b,c,d in product(range(3),repeat=4):
        key=encode((b,c,c,d),3),encode((a,b,d,a),3)
        C[key]=C.get(key,0)+1
    G=mul(transpose(C),C)
    need(mul(G,G)==scale(G,9) and tr(G)==81,'full oriented spin-one character')
    return records
def source_controls():
    spec=importlib.util.spec_from_file_location('fresh_incidence',HERE/'incidence_probe.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    records=[]
    for d in (2,3):
        m=2*(d-1)
        expected={'shared':{'same':m*(m-2)//4,'opposite':m*m//4},
                  'outside':{'same':3*m*(m-2)//2,'opposite':3*m*m//2}}
        for k in range(d):
            row=mod.census(d,k)
            need(row['counts']==expected,'complete coordinate-star census')
            records.append(row)
        R=F(3*m,8)+F(expected['shared']['opposite'],3)+F(expected['outside']['same'],6)+F(2*expected['outside']['opposite'],3)
        S=F(expected['shared']['same']+expected['outside']['same'],6)
        need((R,S)==((F(61,12),F(0)) if d==2 else (F(125,6),F(7,3))),'source exact radical pair')
        need(F(25,16)*m*m-R>0 and (F(25,16)*m*m-R)**2>3*S*S,'source rational bound, exact')
    return records
def spectral_controls():
    # Ordered basis (ab,c); exact T and its proposed channel vectors.
    T={(0,0):F(13),(1,0):F(-1),(1,1):F(9)}
    h={(0,0):F(1),(1,0):F(-1,4)}; c={(1,0):F(1)}
    need(mul(T,h)==scale(h,13),'triplet kinetic eigenvector')
    need(mul(T,c)==scale(c,9),'singlet kinetic eigenvector')
    gamma=plus(scale(c,F(3,4)),scale(h,-1))
    need(gamma=={(0,0):F(-1),(1,0):F(1)},'complete cross response')
    I={(0,0):F(1),(1,1):F(1)}
    p9=scale(plus(scale(I,13),scale(T,-1)),F(1,4))
    p13=scale(plus(T,scale(I,-9)),F(1,4))
    need(mul(p9,p9)==p9 and mul(p13,p13)==p13 and mul(p9,p13)=={},'complete channel projectors')
    need(mul(T,T)==plus(scale(T,22),scale(I,-117)),'minimal kinetic polynomial')
    D=lambda a,b,c:1-a*a-b*b-c*c+2*a*b*c
    need(D(F(1,2),F(1,2),F(1,4))==F(9,16),'first witness physical admission')
    need(D(F(1,2),F(1,2),F(3,16))==F(143,256),'second witness physical admission')
    need(D(F(3,4),F(1,3),F(1,4))==F(7,18),'interacting hostile physical admission')
    need(-F(1,4)*(F(3,4)+F(1,3)-1)==-F(1,48),'interacting quotient separation')
    need(F(9,64*81)+F(3,64*169)==F(7,156)**2,'orthogonal L2 response norm')
    for z in [F(n,3) for n in range(31)]:
        inv=plus(scale(c,F(3,4)/(9+z)),scale(h,-1/(13+z)))
        shifted=plus(T,{(0,0):z,(1,1):z})
        need(mul(shifted,inv)==gamma,'resolvent intertwining')
        at=lambda vec,a,b,cc:sum(value*(a*b if i==0 else cc) for (i,j),value in vec.items())
        need(at(inv,F(1,2),F(1,2),F(1,4))==F(3,4)/((9+z)*(13+z)),'zero instantaneous response witness')
        need(at(inv,F(1,2),F(1,2),F(3,16))==-z/(16*(9+z)*(13+z)),'fixed-scale zero witness')
    for z1 in range(6):
        for z2 in range(z1+1,7):
            det=F(1,(9+z1)*(13+z2))-F(1,(13+z1)*(9+z2))
            need(det==F(4*(z2-z1),(9+z1)*(13+z1)*(9+z2)*(13+z2)) and det>0,'two probe exact inverse')
            for X,Y in [(F(3,5),F(-7,4)),(F(0),F(0)),(F(9,64),F(-13,64))]:
                g1=X/(9+z1)+Y/(13+z1);g2=X/(9+z2)+Y/(13+z2)
                w1=(9+z1)*(13+z1)*g1;w2=(9+z2)*(13+z2)*g2
                f=(w2-w1)/(z2-z1);A=(z2*w1-z1*w2)/(z2-z1)
                need(((A-9*f)/4,(13*f-A)/4)==(X,Y),'full two-probe decoder')
    # Actual character-product range, no asserted finite spin cutoff.
    for j in [F(n,2) for n in range(2,66)]:
        lam=lambda q:8*q*(q+1)
        lm,lp=lam(j-F(1,2)),lam(j+F(1,2))
        need(lam(j)+6-lm==8*(j+1),'negative-step channel coefficient')
        need(lam(j)+6-lp==-8*j,'positive-step channel coefficient')
        # Unnormalized square characters have Fourier norm (2l+1)^3.
        wm=8*(j+1)*(2*j)**3;wp=8*j*(2*j+2)**3
        for z in (F(1),F(7,3),F(20)):
            ratio=(wm*lm/(lm+z)+wp*lp/(lp+z))/(wm+wp)
            need(lm/(lm+z)<ratio<1,'true bilinear-range smoothing ratio')
    return {'resolvent_values':31,'two_probe_pairs':21,'character_spin_examples':64,
            'zero_current_nonzero_inverse':'1/156','fixed_scale_zero_later':'-z/[16(9+z)(13+z)]'}
def ball_controls():
    records=[]
    for x,z,margin,lip,q,D in [(F(1,3),F(7,20),F(1,2400),F(101,180),F(4,5),F(41,90)),
                              (F(7,20),F(5,12),F(13,6912),F(109,180),F(163,180),F(23,45))]:
        M=F(25,16)*x*x+F(4,3)*x*z+z*z/6
        need(z-M==margin and margin>0,'actual correction invariant ball')
        need((4*x+z)/3==lip<1,'all-spin Lipschitz certificate')
        need(x+F(4,3)*z==q<1,'actual collective response')
        need(F(2,3)*(x+z)==D,'actual conditional density')
        records.append({'x':str(x),'Z':str(z),'margin':str(margin),'Lipschitz':str(lip),'q':str(q),'D':str(D),'gap_prefactor_without_d_over_d_minus_one':str(F(3,2)*(1-q))})
    for x in [F(n,50) for n in range(51)]:
        z=F(3,4)*(1-x)
        need(32*(F(25,16)*x*x+F(4,3)*x*z+z*z/6-z)==21*x*x+50*x-21,'conditional margin polynomial')
    need(F(7,20)/F(1,3)==F(21,20),'5 percent interval extension')
    return records
if __name__=='__main__':
    result={'schema':'ym2-operational-controls-v1','status':'PASS',
            'matrix_channels':matrix_controls(),'incidence':source_controls(),
            'spectral':spectral_controls(),'certificates':ball_controls(),
            'old_checkers_executed':False}
    result['assertions']=assertions
    print(json.dumps(result,indent=2))
