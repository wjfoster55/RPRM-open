"""New exact finite controls for relational references and exclusion bounds.

No accepted checker is imported or rerun. General and infinite claims are
the written proofs in RELATIVE_WEB_AND_EXCLUSION.md, not finite tests.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent


def require(test, name):
    if not test:
        raise RuntimeError(name)


def compute():
    ratios = []
    for ell, extent, reference, rebase in (
        (F(1,8),F(2),F(1),F(3)),
        (F(2,7),F(11,3),F(5,2),F(1,4)),
        (F(3),F(3),F(7,5),F(9,2)),
    ):
        x, y = ell/reference, extent/reference
        require(y/x == extent/ell, 'length triangle')
        require(x*(reference/extent)*(extent/ell) == 1, 'cycle closure')
        xp, yp = x/rebase, y/rebase
        require(yp/xp == y/x, 'reference rebase invariant')
        gd = F(7,11)
        require((rebase*gd)*xp == gd*x and (rebase*gd)*yp == gd*y,
                'length-energy web rebase')
        ratios.append({'ell':str(ell),'L':str(extent),'d':str(reference),
                       'reference_factor':str(rebase),'x':str(x),'y':str(y),
                       'L_over_ell':str(y/x),'gap_d':str(gd),
                       'gap_ell':str(gd*x),'gap_L':str(gd*y)})
    hostile = []
    for n in (2,3,7,19):
        refinement = (F(1,n),F(1))
        enlargement = (F(1),F(n))
        require(refinement != enlargement, 'distinct reference relationships')
        require(refinement[1]/refinement[0] == enlargement[1]/enlargement[0] == n,
                'ratio-only hostile collision')
        gap, ea, eb = F(1,n), F(1,n), F(2,n)
        require(gap/ea == 1 and gap/eb == F(1,2) and eb/ea == 2,
                'co-scaling pairwise invariants')
        conversion = F(n+2,3)
        require((gap/conversion)/(ea/conversion) == gap/ea,
                'consistent unit conversion')
        hostile.append({'n':n,'same_L_over_ell':n,'gap_over_EA':'1',
                        'gap_over_EB':'1/2','gap_over_retained_Estar':str(gap)})
    matrix_controls = 0
    for rho in (F(-1),F(-3,4),F(0),F(2,5),F(1)):
        for x,y in ((F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),
                    (F(3,5),F(-4,5)),(F(1),F(1)),(F(1),F(-1))):
            norm2=x*x+y*y
            q=norm2-2*rho*x*y
            low=(1-abs(rho))*norm2
            sign=1 if rho>=0 else -1
            require(q-low == abs(rho)*(x-sign*y)**2,
                    'complete square lower-bound identity')
            require(q>=low>=0, 'positive form envelope')
            matrix_controls+=1
        # Non-unit exact vectors suffice for homogeneous Rayleigh ratios.
        sy=F(1) if rho>=0 else F(-1)
        require((2-2*rho*sy)/2 == 1-abs(rho),'sharp joint direction')
    spectra=[]
    for size in (1,2,5,13):
        values=[F(1,n) for n in range(1,size+1)]
        require(all(v>0 for v in values) and min(values)==F(1,size),
                'finite restriction exact gap')
        spectra.append({'excited_dimension':size,'exact_gap':str(min(values))})
    sources=[Path(__file__).resolve(),HERE/'RELATIVE_WEB_AND_EXCLUSION.md']
    return {'schema':'ym2-relative-web-exact-v1','status':'PASS',
            'evidence_grade':'Exact finite controls; general scope supplied by written proofs',
            'ratio_web_examples':ratios,'reference_hostile_controls':hostile,
            'quadratic_form_controls':matrix_controls,'finite_gap_controls':spectra,
            'not_claimed':['actual YM gap estimate','infinite coverage by finite testing',
                           'universal prime seam rule','proof-assistant certification'],
            'sources':[{'path':p.name,'sha256':sha256(p.read_bytes()).hexdigest()} for p in sources]}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write-results',action='store_true')
    args=parser.parse_args()
    receipt=compute()
    target=HERE/'RESULTS_RELATIVE_WEB.json'
    if args.write_results:
        target.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    else:
        require(json.loads(target.read_text(encoding='utf-8'))==receipt,'Full saved receipt mismatch')
    print('PASS: 3 reference webs, 4 reference collisions, 30 quadratic-form controls, 4 finite-gap controls')


if __name__=='__main__':
    main()
