"""EXPERIMENTAL exact symbolic pitch, finite event, and integer-wave models."""
from itertools import permutations, combinations
from math import gcd


def integer(value, low, high, name):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} must be a plain integer in {low}..{high}")
    return value


def pitches(values, *, size=None):
    if size is not None:
        integer(size,1,12,"declared size")
    if type(values) not in (tuple,list) or not 1 <= len(values) <= 12 or (size is not None and len(values) != size):
        raise ValueError("pitch carrier requires a list/tuple of 1..12 tokens and the declared size")
    return tuple(integer(v,0,11,"pitch class") for v in values)


def multiset(values):
    return tuple(sorted(pitches(values)))


def distinct_set(values):
    """Lossy readout: intentionally forget both order and multiplicity."""
    return tuple(sorted(set(pitches(values))))


def labelled_fiber(values):
    """Complete labelled triple preimage under the unordered-multiset map."""
    result = sorted(set(permutations(pitches(values,size=3))))
    return {"disposition":"ONE" if len(result)==1 else "MANY", "values":[list(x) for x in result]}


def action(values, anchor=0, sign=1):
    values=pitches(values);integer(anchor,0,11,"anchor")
    if type(sign) is not int or sign not in (-1,1):raise ValueError("orientation must be -1 or 1")
    return tuple((sign*x+anchor)%12 for x in values)


def circular_distance(a,b):
    integer(a,0,11,"pitch class");integer(b,0,11,"pitch class")
    gap=abs(a-b)
    return min(gap,12-gap)


def matching(left,right):
    """Six occurrence assignments; retain all minimum-cost assignments."""
    left=pitches(left,size=3);right=pitches(right,size=3)
    scored=[]
    for p in permutations(range(3)):
        cost=sum(min(abs(left[i]-right[p[i]]),12-abs(left[i]-right[p[i]])) for i in range(3))
        scored.append((cost,p))
    minimum=min(cost for cost,_ in scored)
    assignments=[list(p) for cost,p in scored if cost==minimum]
    return {"distance":minimum,"assignment_fiber":{"disposition":"ONE" if len(assignments)==1 else "MANY","values":assignments}}


def interval_histogram(values):
    values=pitches(values)
    if len(set(values))!=len(values):raise ValueError("interval histogram requires distinct tokens")
    counts=[0]*6
    for a,b in combinations(values,2):counts[circular_distance(a,b)-1]+=1
    return tuple(counts)


def orbit(values):
    values=pitches(values)
    return tuple(sorted({multiset(action(values,a,s)) for a in range(12) for s in (-1,1)}))


def wave(values):
    if type(values) not in (list,tuple) or not 1<=len(values)<=64:raise ValueError("wave needs 1..64 integer samples")
    return tuple(integer(x,-1000000,1000000,"sample") for x in values)


def shift(values,k):
    values=wave(values);integer(k,-1000000,1000000,"shift")
    return tuple(values[(i+k)%len(values)] for i in range(len(values)))


def negate(values):
    return tuple(-x for x in wave(values))


def sum_waves(left,right):
    left=wave(left);right=wave(right)
    if len(left)!=len(right):raise ValueError("sample domains must match")
    return tuple(a+b for a,b in zip(left,right))


def event_context(events,q):
    if type(events) not in (list,tuple) or not 1<=len(events)<=16:raise ValueError("event mask needs 1..16 samples")
    events=tuple(integer(x,0,1,"event") for x in events)
    integer(q,1,16,"state modulus")
    return events,q


def event_step(events,q,state,*,inverse=False):
    events,q=event_context(events,q)
    if type(inverse) is not bool:raise ValueError("inverse flag must be boolean")
    if type(state) not in (list,tuple) or len(state)!=2:raise ValueError("state must be a phase/state pair")
    f=integer(state[0],0,len(events)-1,"phase");h=integer(state[1],0,q-1,"state")
    if inverse:
        previous=(f-1)%len(events)
        return previous,(h-events[previous])%q
    return (f+1)%len(events),(h+events[f])%q


def event_cycles(events,q):
    events,q=event_context(events,q);remaining={(f,h) for f in range(len(events)) for h in range(q)}
    cycles=[]
    while remaining:
        start=min(remaining);current=start;cycle=[]
        while current not in cycle:
            cycle.append(current);remaining.remove(current);current=event_step(events,q,current)
        if current!=start:raise RuntimeError("event map did not close a permutation orbit")
        cycles.append(cycle)
    return cycles


def event_invariant(events,q,state):
    events,q=event_context(events,q)
    event_step(events,q,state)  # Validate the supplied ports.
    f,h=state
    return (h-sum(events[:f]))%gcd(sum(events),q)


def timing_adapter(source,target,q,state):
    """Bijective same-length/same-total event-mask conjugacy, not equal timing."""
    source,q=event_context(source,q);target,_=event_context(target,q)
    event_step(source,q,state)
    if len(source)!=len(target) or sum(source)!=sum(target):raise ValueError("adapter requires equal length and event total")
    f,h=state
    return f,(h+sum(target[:f])-sum(source[:f]))%q
