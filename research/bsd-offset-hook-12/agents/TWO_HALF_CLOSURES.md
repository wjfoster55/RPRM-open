# Two partial closures joined at two seams

Date: 2026-09-12 local. Evidence: elementary written theorems, exact countermodels, and independent finite replay. No height recurrence was rerun. This report treats the user's “69” as a proposed arrangement of two complementary partial paths, not as a search for literal digits 6 and 9. The models below are candidate definitions; they do not claim to be the user's unique intended operation.

**Two complementary simple arcs can force a whole turn.** Joining two marked seams in the proper orientation closes a geometric cycle, and requiring both arcs to be simple and complementary fixes its winding to one. To determine a scalar carried around that cycle, the two transport laws must also agree at both seams. Those equations may have NONE, ONE, or MANY compatible states.

The newly written anchor `2.0430` is numerically different from the previously certified `2.0340`. The theorems keep anchors symbolic; the reviewed numerical evidence retains its earlier certified bounds. This report does not silently identify those two anchor values.

## 1. A precise two-seam candidate

Supply two distinct seam occurrences A and B and two directed paths:

```text
P: A -> interior of P -> B
Q: B -> interior of Q -> A
```

Their interiors are disjoint; they share only the identified endpoints A and B. Retain path identity, departure and arrival roles, orientation, and the rule identifying the two copies of each seam. Under these conditions their union is one directed cycle. For an exact finite version, take path lengths m,n>=1, with N=m+n edges. Each path's interior vertices occur only once. For m=n=1 this is the directed two-edge cycle, retaining both edge occurrences.

A “half-open” ownership convention can assign A and P's interior to P, and B and Q's interior to Q. Each path then owns its departure seam and excludes its arrival seam from its owned vertices. **The arrival port is still retained and checked.** Half-open ownership prevents double counting; it does not remove the second seam condition.

This gives an actual construction that a two-part drawing can represent. If the paths revisit an interior vertex, share another point, or are glued using different endpoint identifications, the resulting graph may have extra loops, a retraced segment, or a different topology. Those are alternative carriers, not failures of this construction.

## 2. Positive complementary-arc theorem

Supply the finite oriented circle `Z/NZ`, N>=2, with successor `i -> i+1 mod N`, and distinct marked seam phases a,b. An edge is identified by its departure position i. Put

\[
 s=(b-a)\bmod N,\quad 1\le s\le N-1.
\]

Let P follow the successor from a to b without a repeated edge, and Q follow that same global successor from b back to a without a repeated edge. Their lengths and edge occurrences are

\[
 \ell_P=s,\quad E_P=\{a,a+1,\ldots,a+s-1\}\pmod N,
\]
\[
 \ell_Q=N-s,\quad E_Q=\{b,b+1,\ldots,b+N-s-1\}\pmod N.
\]

**Theorem.** The two edge sets are disjoint, their union is the whole circle, and every edge is traversed exactly once. Thus the combined path has lifted length N and winding ONE(1). For supplied marked a,b and the fixed successor, the two simple paths are uniquely determined.

**Proof.** Reading the N consecutive departure positions `a,a+1,...,a+N-1` modulo N visits every circle position once. The first s positions give P; the remaining N-s give Q, since `a+s=b mod N`. They therefore partition all edge occurrences. Their summed lifted length is s+(N-s)=N, so the winding is one.

The conditions are doing real work. Endpoints and local arrow labels `A -> B`, `B -> A` alone do not select these two arcs. The second leg could retrace the first in the reverse global direction, returning with zero net winding. It could also make extra turns before arriving. Complementary simple forward arcs exclude both possibilities.

With a supplied finite turn budget K and missing tags `q_P,q_Q in {0,...,K}`, the complete family of forward lifted lengths consistent with those same seam phases is

\[
 (s+q_PN,\ N-s+q_QN),\qquad
 \text{winding}=1+q_P+q_Q.
\]

The simple-arc hypothesis sets both tags to zero. Without it, a modular return does not recover the tags. The rooted phases can also retain a global-rotation ambiguity if the origin mark is removed.

If every edge has a supplied length ell, the traveled distance is `ell*N*(1+q_P+q_Q)`. If ell is missing, fixing the winding does not determine that metric distance. For example, ell=1 and ell=2 give the same finite incidence and orientation data but different circumference. A known circle constant can determine scale only through a supplied metric relation and its other required inputs.

## 3. Exact transport at both seams

Geometric seam identity and the state carried through a seam are different ports. Let X be the state carrier at A and Y the state carrier at B. Supply relations

\[
 P\subseteq X\times Y,\qquad Q\subseteq Y\times X.
\]

Each relation includes the enabledness and endpoint conditions of its entire partial path. The complete two-seam closure fiber is

\[
 \boxed{\mathcal C=\{(x,y): (x,y)\in P\ \text{and}\ (y,x)\in Q\}.}
\]

**Two-seam gluing theorem.** This fiber contains exactly the state assignments that close both seams. Its proof is direct in both directions: a closed assignment uses the same y at the joined B seam and the same x at the joined A seam, giving the two displayed memberships; every pair with those memberships supplies such an assignment. For a finite supplied relation table, exhaustive intersection gives its complete NONE, ONE, or MANY fiber. An incomplete search is OPEN.

For deterministic partial transports `F:X ⇀ Y`, `G:Y ⇀ X`, this becomes

\[
 \mathcal C=\{(x,F(x)):\ x\in\operatorname{dom}F,
 F(x)\in\operatorname{dom}G,\ G(F(x))=x\}.
\]

Thus closure is a fixed-point equation for the actual composite, including both paths. Drawing the endpoint A in the same place at departure and return does not replace that equation. In a nondeterministic model, the same x can have several compatible middle states or internal traces. Retain those witnesses if the receiver needs them.

A requested scalar readout R is determined exactly when the complete fiber is nonempty and R is constant on it. The geometric path can be unique while the transported state is MANY, or the state can be unique while several internal traces remain possible.

## 4. Complete affine forward/return fibers

First explicitly admit total rational transports, with exact supplied rational coefficients:

\[
 F(x)=ax+b,\qquad G(y)=cy+e,\qquad x,y\in\mathbb Q.
\]

This is a declared symbolic carrier, not an implicit numerical search limit. The fixed-point equation is

\[
 (1-ca)x=cb+e.
\]

**Affine closure theorem.** The complete joint fiber is:

- If `1-ca != 0`: ONE(`x*`, `a*x*+b`), where `x*=(cb+e)/(1-ca)`.
- If `1-ca = 0` and `cb+e != 0`: NONE.
- If both quantities are zero: MANY(`{(x,a*x+b): x in Q}`), with complete coverage given by that parameterization.

**Proof.** Substitute F into G and rearrange the equation. A nonzero coefficient permits exactly one division. A zero coefficient with nonzero right side is impossible. When both vanish, every rational x satisfies the equation, and y is uniquely F(x). These alternatives exhaust the coefficients and all possible x.

For a bounded real or rational application, explicitly supply intervals I,J with endpoint membership, and require x in I and F(x) in J. The same algebra applies, but the unique candidate must pass those admission conditions. In the identity-composite case the complete family is parameterized by `K={x in I: a*x+b in J}`. Classify K by its actual cardinality; a half-open endpoint can exclude a would-be unique solution. If F or G has other enabledness conditions, intersect with those too.

| Forward F | Return G | Composite | Complete x fiber |
|---|---|---|---|
| `x` | `y` | `x` | All admitted x |
| `1-x` | `1-y` | `x` | All admitted x |
| `1-x` | `y/2` | `(1-x)/2` | ONE(`1/3`) |
| `x+1` | `y-99/100` | `x+1/100` | NONE |

The first three rows can be admitted on `[0,1]` with their appropriate reached intermediate values. The last row is the stated total-rational example. In the unique row the joint closure is `(x,y)=(1/3,2/3)`. This shows exactly how two different legs can lock a value. Exact inverse legs instead reconstruct every input: inverse transport is valuable retention, but does not select one source merely by returning correctly.

These are equations derived from supplied laws. Their closed form does not make the proof logically circular. Conversely, fitting the return law to a desired answer and then checking that same fitted answer closes does not independently establish that the law describes the original arithmetic problem.

## 5. Complementary gaps: a shape that survives changing suffixes

A second candidate starts with an actual bounded interval `L<U`, width w=`U-L`, and one missing point x in `[L,U]`. Retain the labeled gaps

\[
 p=x-L,\qquad q=U-x.
\]

Then p,q>=0 and

\[
 p+q=w,\qquad x=L+p=U-q.
\]

Conversely every pair `(p,q)=(t*w,(1-t)*w)` with `0<=t<=1` gives exactly one compatible x=`L+t*w`. This is the complete joint fiber over the supplied interval. If x is admitted in `[L,U)` instead, use `0<=t<1`; seam ownership changes the endpoint inclusion, not the equation.

The two gaps really do fit together. What is determined depends on what the shape retains:

- Retain only “two complementary pieces close to the whole,” while forgetting their split ratio: every admitted t remains compatible.
- Retain the labeled numerical split t, with L and w: ONE(`L+t*w`). A geometric display that faithfully retains this measured split can determine the point.
- Retain the unordered numerical pair `{t,1-t}`: the complete source fiber is `{L+t*w, L+(1-t)*w}`, after deduplication and admission. It has one member at t=1/2 and otherwise two when both are admitted.
- Add a separately justified balance law p=q: ONE at the midpoint. Drawing similar halves does not by itself supply this law.

Translation and positive scaling preserve t: replacing `(L,U,x)` by `(alpha*L+beta,alpha*U+beta,alpha*x+beta)` with alpha>0 leaves the normalized split unchanged. The absolute coordinate is recovered when its anchor and scale are retained.

For the same x in two nested intervals, the normalized split generally changes. Write `t9=(x-L9)/w9`, `t10=(x-L10)/w10`. Exact substitution gives

\[
 \boxed{t_{10}=\frac{w_9}{w_{10}}t_9+\frac{L_9-L_{10}}{w_{10}},}
\]

with inverse obtained by division by `w9/w10>0`. The domain is precisely the old normalized coordinates of the smaller interval. Thus the complementary relation can persist through refinement while its numerical split and rendered digits change. Disappearance of a literal endpoint substring does not refute this structural candidate. Whether this is the user's intended measured shape remains OPEN.

## 6. Why the loop alone does not establish a BSD scalar equality

The unique affine example already provides a sharp control. On bounded rational states in `[0,1]`, append a separate bit r in `{0,1}` and let both legs retain it:

\[
 \widehat F(x,r)=(1-x,r),\qquad
 \widehat G(y,r)=(y/2,r).
\]

The complete closed fiber consists of exactly

```text
((1/3,0), (2/3,0))
((1/3,1), (2/3,1)).
```

Both have the same uniquely locked x and y and identical path geometry. The readout r differs. This is a complete finite countermodel to determining an independent scalar from geometric or x-coordinate closure alone. It does not claim two different values of the actual, already-defined BSD target; it shows which implication is absent from the stated loop premises.

A successful arithmetic application would supply the actual two transport laws from its arithmetic/analytic data, establish that the actual source satisfies both seam equations, and prove that every compatible closed assignment has the required BSD readout. A supplied identity between actual quantities can accomplish this. A geometric return by itself, or an inverse chosen solely to undo a coordinate encoding, does not provide those additional equations.

## 7. Independent checks of the new paired-path evidence

Read-only review of [check_two_halves.py](C:/github/RPRM-open/research/bsd-offset-hook-12/work/check_two_halves.py) and [two-halves.json](C:/github/RPRM-open/research/bsd-offset-hook-12/evidence/two-halves.json) passed:

- Source and input hashes match current bytes.
- All 14 gap test points, their labeled readbacks, and unordered-pair fibers recompute exactly. Each seven-point carrier has fiber sizes `1,2,2,2` after forgetting left/right order.
- All nine refinement readbacks preserve the same x; the slope, offset, inverse, and admitted old-coordinate interval recompute exactly.
- All 625 coefficient tuples in `{-2,-1,0,1,2}^4` occur once. Their total-rational classifications and every comparison with the nine-point half-integer test grid match independently recomputed results.
- Counts are 575 ONE, 40 NONE, and 10 MANY. Independently, `ca=1` has just `(a,c)=(1,1),(-1,-1)` in this coefficient set. These yield 50 choices of b,e, of which 10 have `cb+e=0`; the remaining 575 tuples have a nonzero fixed-point coefficient. This explains the counts without treating the finite x-grid as coverage of all rationals.
- All four named affine examples agree with the written classification.

Reviewed hashes:

```text
check_two_halves.py
4af1c4f012603f8ea0874f7cc00cf005f13da04aa655ee1690a9c289f1bdda5f

input hooks.json
19f204ed8c3243188fbf97ab8c9c3b550f5af77d20014985e264d94c63c80378

two-halves.json
88bb64bb0dc39dc0e9b932e8015f67a9811408a1165189ea034dc07b564d8bbf
```

This review verifies the paired-path calculations against the supplied enclosures; it does not repeat the height calculation. Neither reviewed model asserts that vanished digit hooks refute the user's proposed shape. The user-specific grammar and the actual BSD bridge remain OPEN.

## 8. Standalone finite replay of complementary simple arcs

The following complete, standard-library-only replay tests all 572 ordered distinct seam pairs for N=2..12. For each pair it verifies exact edge coverage once. It then checks all nine additional-turn tag pairs `qP,qQ in {0,1,2}`, for 5,148 tagged cases, confirming that extra turns increase every edge's multiplicity and the winding by `qP+qQ`.

```python
from collections import Counter
from itertools import product

seam_cases = turn_cases = 0
for n in range(2, 13):
    for a, b in product(range(n), repeat=2):
        if a == b:
            continue
        s = (b-a) % n
        t = (a-b) % n
        assert 0 < s < n and 0 < t < n and s+t == n
        first = [(a+i) % n for i in range(s)]
        second = [(b+i) % n for i in range(t)]
        assert (a+s) % n == b and (b+t) % n == a
        assert not (set(first) & set(second))
        assert Counter(first+second) == Counter({i: 1 for i in range(n)})
        seam_cases += 1
        for qP, qQ in product(range(3), repeat=2):
            first = [(a+i) % n for i in range(s+qP*n)]
            second = [(b+i) % n for i in range(t+qQ*n)]
            winding = 1+qP+qQ
            assert len(first)+len(second) == n*winding
            assert Counter(first+second) == Counter({i: winding for i in range(n)})
            turn_cases += 1
assert (seam_cases, turn_cases) == (572, 5148)
print('PASS:', seam_cases, 'simple seam pairs;', turn_cases, 'retained-turn cases')
```

Only this new report was written in this subtask. The written theorem covers every declared N and distinct seam pair; these finite tests are complementary execution evidence.
