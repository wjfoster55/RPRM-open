"""First digit of the independently defined MST arithmetic cofactor vector.

W = adj(G_MST) * (log_omega(P),log_omega(Q)). This is a scalar-normalized
arithmetic vector; comparison with the untrivialized BKS tensor is a written
theorem obligation, not an assertion that a tensor equals a modular scalar.
"""
import argparse
from datetime import datetime,timezone
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path


def det(M):return M[0][0]*M[1][1]-M[0][1]*M[1][0]
def transpose(M):return [list(c) for c in zip(*M)]
def multiply(A,B):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def vector(A,v):return [sum(x*y for x,y in zip(row,v)) for row in A]
def adj(M):return [[M[1][1],-M[0][1]],[-M[1][0],M[0][0]]]
def mod(v):return [x%5 for x in v]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--height-witness',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError('Preserve prior evidence')
    raw=args.height_witness.read_bytes()
    witness=json.loads(raw)
    h={k:witness['heights'][k]['h_MST_mod5'] for k in ('P','Q','P+Q')}
    G=[[-2*h['P'],h['P']+h['Q']-h['P+Q']],
       [h['P']+h['Q']-h['P+Q'],-2*h['Q']]]
    G=[[x%5 for x in row] for row in G]
    assert G==witness['MST_pairing_matrix_mod5'] and det(G)%5!=0
    logs={};log_rows={}
    for name in ('P','Q','P+Q'):
        row=witness['heights'][name]
        a,b,d=[int(row['integral_coordinates'][k]) for k in ('a','b','d')]
        t=Fraction(-a*d,b)
        assert t==Fraction(row['t']) and row['v5_t']>=1
        t25=t.numerator*pow(t.denominator,-1,25)%25
        assert t25%5==0
        ell=(t25//5)*pow(8,-1,5)%5
        logs[name]=ell
        log_rows[name]={'t_of_8R_mod25':t25,'log_omega_R_div5_mod5':ell,
                        'tail_bound':'log_omega(t)-t belongs to25 Z_5'}
    assert (logs['P']+logs['Q'])%5==logs['P+Q']
    ell=[logs['P'],logs['Q']]
    W=mod(vector(adj(G),ell))
    assert W!=[0,0]
    assert mod(vector(G,W))==mod([det(G)*x for x in ell])
    changes=0;finite_index=0
    for a,b,c,d in itertools.product(range(-3,4),repeat=4):
        U=[[a,b],[c,d]]
        determinant=det(U)
        if determinant==0:continue
        changed_G=multiply(multiply(transpose(U),G),U)
        changed_ell=vector(transpose(U),ell)
        returned=vector(U,vector(adj(changed_G),changed_ell))
        assert returned==[determinant**2*x for x in vector(adj(G),ell)]
        if abs(determinant)==1:changes+=1
        else:finite_index+=1
    result={'created_utc':datetime.now(timezone.utc).isoformat(),
            'status':'EXACT_ARITHMETIC_COFACTOR_VECTOR_READOUT',
            'definition':'W=adj(G_MST)*(log_omega(P),log_omega(Q))',
            'height_normalization':'MST bilinear pairing, cyclotomic functional log5/5',
            'formal_log_reads':log_rows,
            'Gram_matrix_mod5':G,'ell_div5_mod5':ell,'W_div5_coordinates_mod5':W,
            'W_coordinates_mod25':[5*x for x in W],
            'W_nonzero':True,'identity_G_times_W_equals_detG_times_ell_checked':True,
            'unimodular_basis_controls':changes,'finite_index_covariance_controls':finite_index,
            'basis_covariance':'represented W transforms by det(U)^2; GL2(Z) leaves it fixed',
            'BKS_tensor_comparison':'SEE_PADIC_HEIGHT_AUDIT; scalar conventions are explicit',
            'derived_Kato_vector_kappa':'OPEN_NOT_CONSTRUCTED',
            'direction_comparison_det_kappa_W':'OPEN',
            'exact_analytic_scalar_comparison':'OPEN',
            'P_coordinate_warning':'0 modulo25 is not a proof the P coordinate vanishes',
            'witness_sha256':hashlib.sha256(raw).hexdigest(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','ell_div5_mod5','W_div5_coordinates_mod5',
                                            'W_coordinates_mod25','W_nonzero')},indent=2))


if __name__=='__main__':main()
