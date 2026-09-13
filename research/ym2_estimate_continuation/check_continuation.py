"""New exact controls only; no accepted checker is imported or executed.

Default: recompute and compare the saved receipt, without writing.
--write-receipt: intentionally create this continuation's receipt.
Finite matrices do not certify the unrestricted written analysis.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import argparse
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def need(ok,label):
    if not ok: raise RuntimeError(label)

def mm(a,b):
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]

def tr(a): return sum((a[i][i] for i in range(len(a))),F(0))
def transpose(a): return list(map(list,zip(*a)))
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def times(a,c): return [[c*x for x in row] for row in a]
def plus(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]

def source_matrix():
    basis=list(product(range(2),repeat=4)); index={v:i for i,v in enumerate(basis)}
    m=[[F(0) for _ in basis] for _ in basis]
    for a,b,c,d in basis: m[index[b,c,c,d]][index[a,b,d,a]]+=1
    gram=mm(transpose(m),m)
    need(mm(gram,gram)==times(gram,4),'source partial isometry')
    need(tr(gram)==16,'source Gram trace')
    # Gram eigenvalues are 0 or 4; trace forces four eigenvalues 4.
    # B=M/2 therefore has four singular values 1, giving trace norm 4.
    plus_source=[[F(0) for _ in basis] for _ in basis]
    for a,b,c,d in basis: plus_source[index[b,c,d,a]][index[a,b,c,d]]+=1
    need(mm(transpose(plus_source),plus_source)==eye(16),'all-positive permutation hostile control')
    return {'dimension':16,'twice_B_gram_trace':16,'twice_B_gram_polynomial':'G^2=4G',
            'B_nonzero_singular_values':['1']*4,'actual_plaquette_A_norm':'4',
            'all_positive_word_A_norm':'8','same_norm_under_partial_inversion':'REJECT'}

def contracted_matrix():
    basis=list(product(range(2),repeat=2)); ix={v:i for i,v in enumerate(basis)}
    swap=[[F(0) for _ in basis] for _ in basis]
    for a,b in basis: swap[ix[b,a]][ix[a,b]]=1
    ident=eye(4)
    omega=plus(ident,times(swap,-2)); absolute=plus(times(ident,2),times(swap,-1))
    need(mm(swap,swap)==ident,'swap involution')
    need(mm(omega,omega)==mm(absolute,absolute),'absolute Omega square')
    singlet=times(plus(ident,times(swap,-1)),F(1,2))
    need(mm(singlet,singlet)==singlet and tr(singlet)==1,'singlet projector')
    need(mm(omega,singlet)==times(singlet,3),'singlet operator extremum')
    densities=[[[F(1),F(0)],[F(0),F(0)]],[[F(0),F(0)],[F(0),F(1)]],
               [[F(1,2),F(1,2)],[F(1,2),F(1,2)]],
               [[F(1,2),F(-1,2)],[F(-1,2),F(1,2)]],
               [[F(1,3),F(0)],[F(0),F(2,3)]]]
    values=[]
    for rho,sigma in product(densities,repeat=2):
        overlap=tr(mm(rho,sigma)); value=2-overlap
        need(0<=overlap<=1 and 1<=value<=2,'factored absolute channel control')
        values.append(value)
    need(max(values)==2,'sharp separable expectation')
    pairs=0
    for jj,kk in product(range(1,65),repeat=2):
        j,k=F(jj,2),F(kk,2); lo,hi=sorted([j,k])
        ratio=1/(hi*(lo+1))
        if (jj,kk)==(1,1): need(ratio==F(4,3),'fundamental exceptional pair')
        else: need(ratio<=F(2,3),'nonfundamental ratio control')
        pairs+=1
    need(F(2)/(F(3,2)**2)==F(8,9),'fundamental normalized constant')
    need(2*F(8,9)==F(16,9),'two input anchors')
    return {'density_pair_controls':len(values),'finite_spin_pairs':pairs,
            'unrestricted_operator_norm':'3','factored_expectation_max':'2',
            'new_bilinear_constant':'16/9',
            'entangled_singlet_as_product_input':'REJECT'}

def radii():
    old=[]
    for y in [F(0),F(1,8),F(1,4),F(1,3),F(3,8)]:
        t=y-F(4,3)*y*y; h=(1-F(8,3)*y)**2/F(16,3)
        need(t+h==F(3,16),'old recenter envelope')
        old.append({'radius':y,'source':t,'extra_source_supremum':h,'total':t+h})
    rows=[]
    for dimension,m in [(2,2),(3,4)]:
        for y in [F(1,4),F(3,8),F(1,2),F(9,16)]:
            t=y-F(8,9)*y*y; r=t/(4*m)
            contraction=F(16,9)*y
            row=F(4,3)*y; osc=F(8,3)*y
            prefactor=F(3,2)*(1-row)
            need(row<1 and prefactor>0,'conditional margin retained')
            if y==F(1,4):
                need(r==F(7,144*m) and 1-2*y==F(1,2),'new safe half-gap endpoint')
                tail=y-t-F(8,9)*t*t
                theta=m*r+F(16*m*(m-1),117)*r*r+F(4,3)*tail
                need(tail==F(16,729) and theta<F(1,12),'extended CP8 safe interval')
            if y==F(3,8): need(r==F(1,16*m) and prefactor==F(3,4) and osc==1,'middle gap')
            if y==F(1,2): need(r==F(5,72*m) and contraction==F(8,9),'curvature boundary')
            if y==F(9,16):
                need(r==F(9,128*m) and contraction==1,'new construction endpoint')
                need(prefactor==F(3,8) and osc==F(3,2),'positive limiting conditional gap')
            rows.append({'dimension':dimension,'incidence':m,'radius':y,'coupling':r,
                         'contraction':contraction,'Bochner_lower':1-2*y,
                         'conditional_row_upper':row,'conditional_gap_prefactor':prefactor,
                         'conditional_gap_negative_exponent':osc,
                         'endpoint_uses_spectral_continuity':y==F(9,16)})
    return {'recenter_controls':old,'new_radius_controls':rows}

def oscillation_orientation():
    c=[[F(0),F(2,5),F(2,5)],[F(4,5),F(0),F(0)],[F(4,5),F(0),F(0)]]
    d=[[F(1)],[F(0)],[F(0)]]
    correct=sum(x[0] for x in mm(transpose(c),d)); wrong=sum(x[0] for x in mm(c,d))
    need(max(map(sum,c))==F(4,5),'row sum')
    need(correct==F(4,5) and wrong==F(8,5),'transpose hostile control')
    return {'matrix':c,'oscillation_vector':d,'correct_C_transpose_l1':correct,
            'incorrect_C_l1':wrong,'transpose_omission':'REJECT'}

def encode(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [encode(v) for v in x]
    return x

def compute():
    return encode({'schema':'ym2-estimate-continuation-checks-v1','status':'PASS',
        'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_matrix':source_matrix(),'contracted_gradient':contracted_matrix(),
        'continuation':radii(),'oscillation_orientation':oscillation_orientation(),
        'old_checkers_run':False,
        'evidence_ceiling':'Finite rational controls. General matrix, Banach, probability, spectral and continuum claims require their written proofs.'})

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write-receipt',action='store_true')
    args=p.parse_args(); result=compute(); path=HERE/'RESULTS.json'
    if args.write_receipt: path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    else: need(json.loads(path.read_text(encoding='utf-8'))==result,'Full saved receipt mismatch')
    print('PASS: exact matrix, 4096 spin-pair, radius, conditional and hostile controls; '+
          ('receipt written.' if args.write_receipt else 'saved receipt matched; no files written.'))

if __name__=='__main__': main()
