"""Exact finite map audit. Input is a fresh GP log, not saved PASS data."""
import argparse
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path


def digits(n, base):
    out = []
    while n:
        n, d = divmod(n, base)
        out.append(d)
    return list(reversed(out or [0]))


def rev(n):
    return int(str(n)[::-1])


def v5(n):
    if not n:
        return None
    v = 0
    while n % 5 == 0:
        n //= 5
        v += 1
    return v


def half_turn(n):
    h = (n % 10) // 5
    return n + 5 * (1 - 2 * h)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--gp-log', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    payload = args.gp_log.read_text(encoding='utf-8')
    assert 'END_CARRY_KEY_06' in payload and '***' not in payload
    rows = []
    for line in payload.splitlines():
        if line.startswith('PADIC|'):
            _, tag, level, precision, lift = line.split('|')
            q = Fraction(lift)
            assert q.denominator == 1
            rows.append(dict(tag=tag, level=int(level), precision=int(precision),
                             residue=int(q) % (5**int(precision))))
    assert len(rows) == 9
    coeffs = [r for r in rows if r['tag'].endswith('b2')]
    for a in coeffs:
        for b in coeffs:
            assert (a['residue']-b['residue']) % 5**min(a['precision'], b['precision']) == 0
    final = next(r for r in coeffs if r['tag']=='classical_b2' and r['level']==6)
    assert final['precision'] == 5
    refined = final['residue']
    coordinate = next(r for r in rows if r['tag']=='coordinate_unit')
    transported = next(r for r in rows if r['tag']=='transported_coefficient')
    assert coordinate['residue']%5==4
    assert (transported['residue']*coordinate['residue']**2-refined)%3125==0
    old = refined % 625
    assert old == 426, 'Fresh calculation does not reproduce the prior displayed residue'

    # A complete reduction fiber: no candidate is discarded based on its appearance.
    lifts = [old + 625*t for t in range(5)]
    lift_rows = [dict(t=t, residue=r, base5=digits(r,5), reversed=rev(r),
                      reverse_plus_one=rev(r)+1, mirror_rule_holds=(rev(r)+1==3125))
                 for t,r in enumerate(lifts)]
    assert refined in lifts

    # Full seven-state proposed role chart, not a theorem identifying BSD inputs.
    chart = []
    for m in range(1,8):
        A,B,c = m-1,m+1,m+2
        alpha = 100*m+20+c
        beta = 100*c+20+B
        assert rev(alpha)+1 == beta
        assert c-2==m and B==c-1
        chart.append(dict(m=m,g=2,A=A,B=B,c=c,source=alpha,target=beta,
                          target_is_power5=beta in [5**n for n in range(1,5)]))
    assert len({r['source'] for r in chart})==7 and len({r['target'] for r in chart})==7
    meeting = [r for r in chart if r['target_is_power5']]
    assert len(meeting)==1

    # Integer coefficient acts on every residue; full finite cycle census.
    multiplier = old
    inverse = pow(multiplier,-1,625)
    assert v5(multiplier-1)==2
    unit = ((multiplier-1)//25)%25
    for x in range(625):
        a,t = x%25,x//25
        assert (multiplier*x)%625 == a+25*((t+unit*a)%25)
        assert inverse*((multiplier*x)%625)%625==x
    unseen=set(range(625)); cycles=[]
    while unseen:
        first=min(unseen); orbit=[]; x=first
        while x not in orbit:
            orbit.append(x); unseen.remove(x); x=multiplier*x%625
        assert x==first
        cycles.append(orbit)
    powers=[dict(k=k,mod125=pow(multiplier,k,125),mod625=pow(multiplier,k,625),
                 mod3125=pow(refined,k,3125)) for k in (0,1,5,10,15,20,25,125)]

    # Finite last-digit half-turn and integer +5 have distinct quotient behavior.
    failures=[]
    for n in range(625):
        assert (n+5)%625 == (n+625+5)%625
        if (half_turn(n+625)-half_turn(n))%625:
            failures.append(n)
    for n in range(1250):
        assert half_turn(half_turn(n)) == n
        assert (half_turn(n+1250)-half_turn(n))%1250==0
        # CRT repair: mod625 plus parity determines the mod1250 lift.
        assert n==(n%625)+625*((n-(n%625))//625)
        assert ((n-(n%625))//625) == ((n%2-(n%625)%2)%2)

    report={
        'status':'FINITE_OPERATION_AUDIT_AND_FRESH_COEFFICIENT_REFINEMENT_COMPLETED',
        'fresh_analytic_rows':rows,
        'coefficient':{'residue':refined,'modulus':3125,'absolute_precision':5,
                       'base5':digits(refined,5),'new_digit':(refined-old)//625},
        'coordinate_transport':{'from':6,'to':-4,'unit_mod3125':coordinate['residue']%3125,
                                'coefficient_mod3125':transported['residue']%3125,
                                'readback_to_original':refined,
                                'identity':'log5(4)+log5(6)=log5(1-25)',
                                'rank_two_scaling':'b_new=b_old/u^2; R_new=R_old/u^2'},
        'decimal_mirror':{'old_residue':old,'old_modulus':625,'reverse':rev(old),
                          'holds_at_four_digits':rev(old)+1==625,
                          'five_possible_lifts':lift_rows,
                          'precision_compatible_rule':'REFUTED_AT_NEXT_LEVEL'},
        'centered_chart':{'rows':chart,'complete_power5_intersection':meeting,
                          'scope':'NEW_ROLE_ASSIGNMENT; no curve-theorem forcing membership'},
        'endpoint_chart':{'input':[4,2,6],'reflected':[3,2,5],
                          'map':'(A,g,B)->(9-B,g,9-A)',
                          'not_coordinatewise_complement':'M(426)=573'},
        'multiplication':{'multiplier_mod625':multiplier,'inverse_mod625':inverse,
                          'affine_fiber_step':unit,
                          'cycle_counts':dict(sorted(Counter(map(len,cycles)).items())),
                          'cycles':cycles,'powers':powers,
                          'principle':'all units 1+25*u with 5 not dividing u share these orders'},
        'fiving':{'half_turn_descent_failure_count':len(failures),
                  'counterexample':[{'n':n,'image':half_turn(n),'image_mod625':half_turn(n)%625}
                                    for n in (426,1051)],
                  'strong_add5_images':[431,1056],
                  'repair':'integer residue mod1250, equivalently mod625 plus parity',
                  'canonical_section_noninvolution':[620,half_turn(620)%625,half_turn(0)%625]},
        'remaining_obligation':'Independently derived arithmetic law selecting the analytic coefficient or exact BSD comparison at all required precisions',
        'full_BSD':'OPEN','total_Sha':'OPEN'
    }
    args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('status','coefficient','full_BSD')},indent=2))


if __name__=='__main__':
    main()
