# A first formal bridge: cube distinctions, fiving, and lawful reuse

**11 September 2026 · RCF01 · Proposed synthesis and exposed development checks**

This is a working note, not a submission-ready paper. It supplies one explicit
connection between recovered constructions. It does not replace William's fuller
meanings of Prestige One, fiving, FIVE_IS_SAFE, or dimensional splitting.
No mathematical novelty is asserted for interpolation, factorization, or the
closure arguments below. The candidate contribution here is their particular
operational connection and a way to investigate it.

## 1. What is inherited, and what is proposed here

The recovery supplies an exact Boolean-cube table/coefficient transform, a
half-decade fiving map, a separate strong winding representation, and a candidate
account of prestige absorption requiring operation descent and retained reopening.
It also supplies the distinct A5/B6/C7 Double-Stamp graph and its authored dwell
permissions. These are historical source reports; their original code was not
available in this package and was not rerun here.

This note proposes an explicit adapter from the **finite display component** of
fiving to one coordinate of a Boolean cube, then tests whether a partial cube
summary supports the resulting operation. It does not declare the ten-cycle and
the cube to be the same object, identify their grades, or identify either with the
Double-Stamp process.

Source anchors are the headings “Finite fiving donor and its exact inverse” and
“Prestige as acquired usable knowledge” in `sources/PRESTIGE-AND-NUMBER-OPERATIONS.md`,
and sections 1–2 of `sources/CUBES-AND-PI-CURVES.md`. The AD semantic correction is
in `sources/absolute-distinction/CURSOR_REVIEW_REPAIR.md`, section C. Old assignment
text inside those sources is historical material, not an active instruction.

## 2. The operational reuse condition

Let X be the admitted state family, C a retained representation, and Q the current
question. A decoder from C to Q exists on the reached image exactly when

    C(x) = C(y)  =>  Q(x) = Q(y).

For a declared partial operation T, lawful reuse also requires, for states with
the same representation:

    T is enabled on x iff it is enabled on y;
    when enabled, C(T(x)) = C(T(y)).

These conditions let T descend to a well-defined operation on retained states.
Induction then gives correctness for finite admitted operation sequences, provided
the successor remains in the declared carrier and every next step satisfies its
admission conditions. A current-answer agreement alone is insufficient.

This is the ordinary factorization/operation-preservation core already present in
William's work, not a new theorem of Absolute Distinction. It is a natural formal
obligation for the **exact reusable-capability branch** of Prestige One. It does
not settle how a closure is acquired, which questions matter, which operations to
admit, or how approximate prestige-based grouping should work.

A promoted envelope may store a hot summary plus an accessible cold artifact.
That can repair a missing hot operation by explicitly reopening/refining; it does
not make the hot summary itself sufficient. Count the cold read and the retained
storage. A hash with no available backing artifact is not a reopening procedure.

## 3. The cube and its deliberately partial view

Use rational-valued functions on X={0,1}^3, with coordinates (h,x,y). Every such
function has one exact multilinear representation:

    f(h,x,y) = a0 + ah*h + ax*x + ay*y
               + ahx*h*x + ahy*h*y + axy*x*y + ahxy*h*x*y.

This statement concerns the eight-site carrier, not unrestricted continuous
functions. Polynomial multiplication below is multiplication as functions on the
Boolean cube, so h^2=h, x^2=x, y^2=y.

Let C2 retain the seven coefficients of degree at most two and omit ahxy. This is
equivalent to retaining f on the seven sites B2 at which at most two coordinates
are 1. The equivalence follows from the forward/inverse subset transforms: each
coefficient of degree at most two uses only values at sites in B2, and each value
at a site in B2 uses only those coefficients.

The omitted space is one rational degree of freedom, not a mysterious center
value. A known lawful function class could constrain that coefficient; this note
first admits **all** rational-valued cube tables, so it does not assume such a
constraint for free.

### Positive result: C2 supports pointwise addition and multiplication

Addition of retained coefficients is exact. For multiplication, the product of
monomials indexed by subsets A and B has support A union B after Boolean
reduction. A term already involving all three coordinates cannot contribute a
lower-degree term through that union operation. Therefore all output coefficients
of degree at most two can be computed from the retained inputs alone.

Equivalently, the restriction to B2 is closed under pointwise addition and
multiplication. This is not an assertion about division, arbitrary symbolic
algebra, or global admission predicates.

A partial representation can therefore be genuinely useful and exactly reusable
for these operations. It need not be dismissed because it is not fully invertible.

## 4. An explicit finite fiving adapter

The recovered finite fiving map is F(d)=d+5 mod 10 with d=5h+r,
h in {0,1}, r in {0,...,4}. It toggles h and preserves r.

Use the enlarged carrier C10 × {0,1} × {0,1}. For each fixed r define

    A_r(h,x,y) = (5h+r, x, y).

A_r is a bijection onto its r-slice. Fiving on the first coordinate satisfies

    (F × id × id) A_r(h,x,y) = A_r(1-h,x,y).

Thus each of five invariant slices supplies a precise adapter to the cube
coordinate flip H(h,x,y)=(1-h,x,y). It is an authored adapter whose equation is
checked, not evidence that every historical use of fiving means a coordinate flip.

For the strong lift n=10w+5h+r, one fiving is

    (w,h,r) -> (w+h,1-h,r).

Two fivings return the finite display but give (w+1,h,r). This additional winding
is retained separately. The finite cube adapter is NOT an equivalence of complete
strong states, and no winding-dependent question is answered by it alone.

## 5. The new connecting example

Treat the flip as an input-view operation on laws: U_H(f)=f composed with H.
Consider

    f0(h,x,y) = h+x+y,
    f1(h,x,y) = h+x+y+hxy.

They have the same C2 summary. At (0,1,1), both read 2. After applying the flip,
that readout asks about the old site (1,1,1): the answers are 3 and 4.

Algebraically, the omitted difference transforms as

    hxy -> (1-h)xy = xy-hxy.

The xy part is now inside the retained degree-two view. Therefore

    C2(f0)=C2(f1), but C2(U_H(f0)) != C2(U_H(f1)).

No universal operation on C2 alone can reproduce that output for both laws.
This refutes **C2-only reuse under this added operation**, not fiving, not the cube,
and not Prestige One. Keeping ahxy, measuring the missing site, or explicitly
reopening a retained artifact repairs the missing distinction. A generic summary
with all coefficients works but achieves no coefficient-count compression here.

### Essential control: coherent coordinate transport is not a failure

The example keeps the retained receiver B2 fixed after changing the input view.
If a bijection H is instead accompanied by the coherently transported observation
set H^(-1)(B2), the old seven observations remain sufficient for that transported
question. Re-labeling the whole problem does not create information loss.

The package tests this distinction on all 48 coordinate-permutation/bit-flip
symmetries of the three-cube. This prevents conflating a lawful change of
coordinates with a new question that reaches previously unretained information.

## 6. General proposition: which future views require more information?

Let X be finite, Y contain at least two distinct values, and admit every function
f:X->Y. Retain the restriction C_S(f)=f|S for S subset X. Let an input map
H:X->X act by pullback f->f composed with H.

**Proposition.** The pullback has an exact action on C_S, with the same retained
set S, if and only if H(S) is a subset of S.

**Proof.** If H(S) is inside S, every needed value f(H(s)) is retained. Conversely,
if H(s)=u outside S for some s in S, choose two functions agreeing everywhere
except u. They have identical retained inputs and different retained outputs at s.
That prevents a well-defined output from the retained input alone. ∎

For a collection of admitted maps, repeatedly add their images to S. Because X is
finite, this process stops. Its result S* is the least forward-closed retained-site
superset. Retaining f|S* supports all finite sequences of those maps. Any smaller
retained-site superset fails for at least one arbitrary law and admitted next step.
This is a minimality claim in the stated **retained-site family**, not a universal
claim about encodings, bit complexity, discovery costs, or constrained law classes.

For the current three-cube, B2 plus the h-flip reaches the one missing vertex.
Thus S* is all eight sites. Under clamp-to-zero and coordinate permutations, B2 is
already closed. Under a flip or clamp-to-one, it is not.

This is a useful way to formulate the prestige question:

> Which distinctions must remain available so this unit can perform the work we
> are actually admitting, including the next changes of view?

## 7. FIVE_IS_SAFE supplies a separate enabledness example

A newly written structural check reconstructs the donor's three graphs:

    A5: two P3 paths with their centers identified (the four-leaf star);
    B6: split that center into two exchanged vertices joined by an edge;
    C7: subdivide the exchanged edge with a fixed midpoint.

Under the row-swap involution, their quotient counts
(vertices, edge orbits, inverted edges) are respectively

    A5: (3,2,0), B6: (3,3,1), C7: (4,3,0).

The donor declares dwell admitted at A5 and C7 and not at B6. The mere quotient
vertex count merges A5 and B6 but cannot determine whether dwell is enabled.
Retaining inversion/type distinguishes them for this question. The graph counts
are structural facts; the permission policy is supplied process semantics. No
physical safety theorem is inferred. This check does not yet prove the full
restart/midpoint commuting adapter or a universal 1/3/5/7 waiting law.

## 8. What was actually executed here

`check_bridge.py` uses the Python standard library and exact integer/rational
arithmetic. The active receipt is `results/assistant_development.json`.

- Twelve named checks passed.
- All 256 Boolean-valued cube tables were transformed and reconstructed over
  integer coefficients; 32 structured rational-valued tables were also checked.
- All 65,536 ordered pairs of Boolean-valued laws were checked for each compact
  addition and pointwise-multiplication operation.
- The fiving slice adapter was checked on 40 states; the strong arithmetic lift
  and inverse on 70 sampled lifted states. The all-integer lift identity is the
  algebra above; finite samples do not establish it by themselves.
- The partial-summary operation criterion was checked against all 128 two-member
  Boolean-table fibers for 16 named input maps (including a redundant identity
  permutation).
- Full-coefficient repair was checked for 4,096 law/map pairs.
- All 256 retained-site subsets were examined for the stated minimal repair.
- Coherent receiver transport was checked for 48 cube symmetries × 128 fibers.
- The graph structural counts and declared-enabledness collision were checked.

Actual subprocess controls confirm that reordered rows pass and omitted,
duplicated, or undeclared required IDs fail with nonzero exit status. These are
coverage checks, not proofs that every runner bug has been excluded.

An earlier eleven-check development build is retained under `provenance/build_00`.
It lacked the coherent-transport control and is not the active result.

These are exposed, constructed development checks. They are not independent
holdout confirmation, a replay of historical PASS receipts, empirical proof of a
universal RPRM mechanism, or a runtime benchmark. The general proofs and exact
finite checks are separate evidence types.

## 9. Next discriminators, not a foregone publication

The next worthwhile questions are not more copies of the same eight-site table.
Implement a small operation-aware promoted envelope and compare it with ordinary
full-table storage, memoization, and a generic exact quotient. Can it correctly
retain, reopen, or refuse when the operation family changes? Can retained original
donors share an actual interface? Does the graph restart rule connect to the
fiving splice under a checked map, or remain a separate useful mechanism?

Any efficiency claim must include construction, checking, storage, lookup,
reopening, invalidation, and repeated use. A correct null or a simpler baseline
win is a valid outcome. The source-defined concept remains preserved even when a
particular formal proposal fails.
