"""Independent reviewer's exact scalar recurrence; no YM2 imports or writes.

Prints six rows rather than issuing PASS/FAIL itself. Final export tooling
compares these rows against the independent review's expected output.
"""
from fractions import Fraction as Q
from math import factorial

def multiply(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c

def independent(q,p):
    a=[[Q(x),Q(y)] for x,y in zip(q,p)]
    for k in range(5):
        nxt=[]
        for i in range(3):
            acc=Q(0)
            for j in range(3):
                if j!=i: acc-=multiply(a[i],multiply(a[j],a[j]))[k]
            nxt.append(acc/((k+1)*(k+2)))
        for i in range(3): a[i].append(nxt[i])
    b=[Q(0)]*7
    for i in range(3):
        for j in range(i+1,3):
            term=multiply(multiply(a[i],a[i]),multiply(a[j],a[j]))
            for n in range(7): b[n]+=term[n]/2
    return tuple(str(c) for c in b)

for name,q,p in [
    ('A',(1,1,0),(0,0,1)),
    ('B',(1,1,0),(Q(2,3),Q(-2,3),Q(1,3))),
    ('+',(1,1,1),(1,1,-2)),
    ('-',(1,1,1),(-1,-1,2)),
    ('planar+',(1,2,0),(1,-2,0)),
    ('planar-',(1,2,0),(-1,2,0))
]:
    print(name,independent(q,p))
