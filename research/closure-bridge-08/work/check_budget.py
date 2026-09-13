"""Bounded paired-budget tests and nonterminating controls, using exact fractions."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args()
    if args.output.exists():raise FileExistsError('Choose a new evidence path')
    cases=[]
    for budget in range(11):
        for cost in (F(1,2),F(2,3),F(1),F(3)):
            x=F(0);y=F(budget);steps=0
            while y>=cost:
                x+=cost;y-=cost;steps+=1
                if x+y!=budget or y<0:raise AssertionError('budget preservation')
            if steps!=F(budget)//cost:raise AssertionError('exact step count')
            cases.append({'budget':budget,'minimum_step_cost':str(cost),
                          'completed_steps':steps,'remaining':str(y),
                          'terminal_predicate':'remaining < cost, supplied for this toy process'})
    contraction=[]
    for k in range(17):
        y=F(1,2**k);x=1-y
        if not(y>0 and x+y==1):raise AssertionError('bounded nonterminal control')
        contraction.append({'k':k,'x':str(x),'y':str(y),
                             'next_consumption':str(y/2)})
    reset=[];x=0;y=2;incoming=0
    for k in range(13):
        if x+y!=2+incoming:raise AssertionError('source flux retained')
        reset.append({'k':k,'completed':x,'remaining_display':y,'incoming_budget':incoming})
        if y==0:y=2;incoming+=2
        x+=1;y-=1
    result={'created_utc':datetime.now(timezone.utc).isoformat(),
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'status':'PAIRED_BUDGET_AND_HOSTILE_CONTROLS_CHECKED',
            'constant_cost_cases':cases,
            'shrinking_cost_infinite_family':{'formula':'x_k=1-2^-k, y_k=2^-k',
                'samples':contraction,'terminal_y_zero':'Never at any finite integer k'},
            'replenished_budget_control':reset,
            'claim_ceiling':'Supplied finite budgets and exact sample arithmetic; written proof supplies parameterized statements. No domain budget inferred.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'constant_cost_cases':len(cases),
                      'shrinking_cost_samples':len(contraction),'flux_samples':len(reset)}))


if __name__=='__main__':main()
