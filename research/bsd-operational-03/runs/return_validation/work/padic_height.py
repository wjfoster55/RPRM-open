"""E34 cyclotomic 5-adic height modulo5, via a proved sigma error bound.

No p-adic decimal approximation or stored expected height is an input.
The interpretation of these exact residues uses Mazur-Stein-Tate (2006),
equation(1.1), Theorem1.3 and Algorithm3.4. See PADIC_HEIGHT_AUDIT.md.
"""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
from rational_ec import Q,point,add,mul,neg,primitive_integral,encode,valuation,residue


def non_singular_reduction(P,p):
    a,b,d=primitive_integral(P)
    if d%p==0:
        return {'prime':p,'reduction':'O','nonsingular':True}
    x=a*pow(d,-2,p)%p
    y=b*pow(d,-3,p)%p
    assert (y*y-x**3+1156*x)%p==0
    dx=(-3*x*x+1156)%p
    dy=2*y%p
    assert (dx,dy)!=(0,0)
    return {'prime':p,'reduction':[x,y],'gradient':[dx,dy],'nonsingular':True}


def height_mod5(R):
    multiple=mul(8,R)
    a,b,d=primitive_integral(multiple)
    t=-multiple[0]/multiple[1]
    assert valuation(t,5)>=1
    u=t/d
    assert u == -Q(a,b) and valuation(u,5)==0
    u25=residue(u,25)
    fourth=pow(u25,4,25)
    assert fourth%5==1
    # log5(u)/5 = (u^4-1)/(4*5) modulo5. The log tail and
    # sigma(t)/t-1 are divisible by25 before dividing by5.
    log_div5=((fourth-1)//5)*pow(4,-1,5)%5
    value=log_div5*pow(8**2,-1,5)%5
    local=[non_singular_reduction(multiple,p) for p in (2,17)]
    return value, {'point':encode(R),'eight_times_point':encode(multiple),
                   'integral_coordinates':{'a':str(a),'b':str(b),'d':str(d)},
                   't':str(t),'v5_t':valuation(t,5),
                   'unit_t_over_d_mod25':u25,'u_fourth_mod25':fourth,
                   'log5_unit_div5_mod5':log_div5,
                   'h_MST_mod5':value,'bad_prime_connected_component_checks':local,
                   'sigma_log_error_div5_in':'5 Z_5',
                   'logarithm_tail_div5_in':'5 Z_5'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError('Preserve earlier evidence')
    P=point(-2,48); R=point(-16,120); T0=point(0,0)
    base={'P':P,'Q':R,'P+Q':add(P,R)}
    values={};rows={}
    for label,S in base.items():values[label],rows[label]=height_mod5(S)
    a=values['P'];c=values['Q']
    b=(values['P+Q']-a-c)*pow(2,-1,5)%5
    H=[[a,b],[b,c]]
    gram=[[(-2*x)%5 for x in row] for row in H]
    det_H=(a*c-b*b)%5
    det_MST=(gram[0][0]*gram[1][1]-gram[0][1]**2)%5
    assert det_H != 0 and det_MST != 0
    controls=[]
    for m,n in ((1,-1),(2,0),(0,2),(1,2),(-1,0)):
        S=add(mul(m,P),mul(n,R))
        actual,row=height_mod5(S)
        predicted=(m*m*a+2*m*n*b+n*n*c)%5
        assert actual==predicted
        controls.append({'coefficients':[m,n],'predicted_mod5':predicted,**row})
    torsion_value,torsion_row=height_mod5(add(P,T0))
    assert torsion_value==a
    count=1+sum(1 for x in range(5) for y in range(5) if (y*y-x**3+1156*x)%5==0)
    ap=6-count
    assert (64*34**6)%5!=0 and ap%5!=0 and 8%5!=0
    result={'created_utc':datetime.now(timezone.utc).isoformat(),
            'status':'EXACT_CYCLOTOMIC_HEIGHT_RESIDUES_AND_NONVANISHING',
            'curve':'y^2=x^3-1156x','prime':5,'modulus_for_unit_log':25,
            'multiplier':8,'point_count_mod5':count,'a5':ap,
            'height_convention':'h(P)=-(P,P)_MST/2, cyclotomic functional log5/5',
            'heights':rows,'polar_half_h_matrix_mod5':H,
            'polar_half_determinant_mod5':det_H,
            'MST_pairing_matrix_mod5':gram,'MST_determinant_mod5':det_MST,
            'cyclotomic_pairing_nondegenerate_on_span_P_Q':True,
            'quadratic_covariance_controls':controls,
            'torsion_translation_control':torsion_row,
            'theorem_dependencies':['MST equation1.1','MST Theorem1.3','quadratic extension of h',
                                    'previous global minimality and rank2 proof'],
            'Bockstein_conclusion':'SEE_SEPARATE_BKS_HYPOTHESIS_AUDIT',
            'full_complex_BSD_identity':'OPEN','total_Sha':'OPEN',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'rational_ec_sha256':hashlib.sha256(Path(__file__).with_name('rational_ec.py').read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','MST_pairing_matrix_mod5',
                          'MST_determinant_mod5','full_complex_BSD_identity')},indent=2))


if __name__=='__main__':main()
