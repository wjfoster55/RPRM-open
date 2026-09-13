# The 0.6/0.4 compensator and the three-block factor

12 September 2026. Independent numeric and cover-weight audit. New written
algebra and bounded exact checks; the existing Yang–Mills hypotheses and
conditional estimates are reused at their stated scope.

**There is an exact coupling.** The three-block physical variance-to-load
ratio is `3/2`. Normalizing its numerator and denominator jointly gives
`(3/(3+2),2/(3+2))=(0.6,0.4)`, whose signed contrast is `-0.2` when the
first role is negated. This preserves the ratio exactly. The original
three block weights remain `(1/2,1/2,1/2)`: putting `0.6` and `0.4` into
two of those weight ports is a different operation, and its best possible
completion has factor `7/5`, below `3/2`.

## 1. Contract and source dependencies

The numeric carrier is the bounded rational simplex
`P={(p,q):p,q in Q, p>=0, q>=0, p+q=1}`. Equality is exact rational
equality. The ratio readout additionally requires `q>0`. For positive
ratios below, both coordinates are positive. These are declared scalar
roles; the signs, a probability interpretation, and repeated occurrence
composition do not follow from the bare numerals.

The cover carrier consists of the three labeled positive rational weights
`a=w_yz`, `b=w_xz`, `c=w_xy`, with common scale immaterial to the requested
ratio. For a bounded representative take `a+b+c=1`. Equivalently one may
use the energy-normalized representative below. Retain a finite open
nearest-neighbor subgraph of `Z^3`, **with at least one edge in every
coordinate direction**, a nonzero centered physical subspace, the full
vertex gauge constraints, and the actual positive invariant vacuum from
[BLOCK_COVER.md](accepted/overlap/BLOCK_COVER.md), sections 1–5.
No spin cutoff is introduced. The three direction-complement blocks have
forest exteriors. Their physical residuals are therefore all `I-J`.

The supplied analytic port is the same positive scalar conditional
gradient constant `C_0` for each inside derivative. The receiver is the
cover's physical gap certificate, including its overlap energy charge.
The ratio below does not determine the vacuum, a spectral eigenfunction,
or a stronger coupling interval.

The recovered complementary-lane and seam contracts are in
[ZERO-AND-RAILS.md](accepted/donors/ZERO-AND-RAILS.md).
The explicitly additive history model is in
[Expansion, compression, and the next expansion](accepted/donors/expansion-compression-2026-09-12/README.md),
section 2. That directory has no `THEORY.md` at the time of this audit.
Historical source wording, current source theorems, and the new adapter
defined here retain their separate attribution.

## 2. One exact parameterization of the halves and discrepancy

Define the oriented discrepancy and ratio by

```text
delta = p-q,                 -1 <= delta <= 1,
p = (1+delta)/2,
q = (1-delta)/2,
kappa = p/q = (1+delta)/(1-delta),       enabled when delta<1.
```

Adding and subtracting the sum-one law proves the inverse formulas.
Conversely, the displayed formulas generate every admitted pair exactly
once. For any supplied rational `delta` in `[-1,1]`, the complete pair
fiber is `ONE(((1+delta)/2,(1-delta)/2))`. For a supplied rational finite
`kappa>=0`, the complete ratio fiber is

```text
ONE((kappa/(1+kappa), 1/(1+kappa))),
delta = (kappa-1)/(kappa+1).
```

Negative ratios are outside this positive-pair contract; division at
`q=0` is disabled. A supplied pair outside the simplex is an admission
error, rather than a failed search for a compensator.

At the requested values,

```text
p=3/5, q=2/5:
delta=1/5,
p/q=3/2,
(-p)+q=-1/5.
```

Thus `1.5`, `0.6`, `0.4`, and `-0.2` fit one lawful relation once the
ports and orientation are fixed. In the recovered note's `S=0.4,R=0.6`
convention, `S-R=-0.2`; this corresponds to `S=q,R=p` here. The ratio of
the signed endpoints themselves is `(-p)/q=-3/2`. Calling it positive
`3/2` means the unsigned magnitude ratio `p/q`.

The half decomposition is

```text
(p,q) = (1/2,1/2) + (delta/2,-delta/2).
```

An additive balance operation transfers `delta/2` from the first role
to the second, yielding `(1/2,1/2)`. For `(0.6,0.4)` this transfer is
`0.1`. The signed endpoint pair `(-p,q)` has span one and midpoint
`-delta/2`; translating the coordinate chart by `delta/2` sends its
endpoints to `(-1/2,+1/2)`. If the old reference was zero, its translated
coordinate is now `delta/2`. Retaining that reference preserves the
original distances `p,q`; resetting the reference to the new midpoint
changes the distance-ratio question to one.

For the separately declared additive bit history, this same correction
has a precise cumulative form. With `k=sum_i b_i`, `b_i in {0,1}`, and
supplied finite length `n`,

```text
sum_i (b_i-p) = k-n/2-n delta/2.
```

At `p=0.6`, conversion to the half-centered sum adds `n/10`. This is
an exact coordinate compensation for that sum receiver. Repeated
coordinate occurrences are summed here because this model explicitly
admits addition. In the phase receiver modulo one, `-p` and `q` coincide
because their difference is one; recovering the total still requires
the retained winding/length information specified in the source model.

## 3. Three-block weights: the entire optimization is elementary

For the declared three-direction cover, put

```text
W=a+b+c,
load_x=b+c,   load_y=a+c,   load_z=a+b,
Lambda=max(load_x,load_y,load_z)=W-min(a,b,c).
```

All three loads actually occur because all directions are present. The
forest identity gives the physical residual constant `delta_w=W`.
The common derivative estimate gives `M_w=C_0 Lambda`. Consequently
the certificate is

```text
gap_phys(H)/E_el >= W/(2 C_0 Lambda),
kappa_cover=W/Lambda.
```

The three pair loads sum to `2W`. Their maximum is at least their
average, so

```text
Lambda >= 2W/3,              kappa_cover <= 3/2.
```

Equality in maximum-at-least-average holds exactly when the three
loads are equal. Subtracting their equations gives `a=b=c`.
Conversely any common positive weight attains `3/2`. This proves
optimality and its equality case over the whole positive weight
family, without relying on numerical search.

If the normalization requires every original edge to have charge one,
the joint equations are

```text
b+c=1,  a+c=1,  a+b=1,
```

with complete fiber `ONE((1/2,1/2,1/2))`. Here `W=3/2`. Under the
different normalization `W=1`, the unique optimum is
`ONE((1/3,1/3,1/3))`, with `Lambda=2/3`. Both represent the same
certificate. Each shared link has two occurrences; the half is the
positive weight that charges those two occurrences once.

The specific unequal proposal has a complete answer too. Fix
`a=3/5,b=2/5` and allow the missing positive third weight `c=t`:

```text
kappa_cover(t) = (1+t)/max(1,3/5+t)
              = 1+t                  for 0<t<=2/5,
              = (1+t)/(3/5+t)         for t>=2/5.
```

The first branch increases and the second decreases; their common
maximum is `7/5` at the unique missing weight `ONE(t=2/5)`.
No third positive weight restores `3/2` while those first two weights
remain fixed. Splitting **one** duplicated contribution into `0.6+0.4`
does charge it once, but that single equation does not solve all three
coupled load equations above.

| Block weights `(a,b,c)` | Loads `(x,y,z)` | `W/Lambda` |
|---|---|---|
| `(1/2,1/2,1/2)` | `(1,1,1)` | `3/2` |
| `(3/5,2/5,1/2)` | `(9/10,11/10,1)` | `15/11` |
| `(3/5,2/5,2/5)` | `(4/5,1,1)` | `7/5` |
| `(3/5,2/5,3/5)` | `(1,6/5,1)` | `4/3` |
| `(3/5,3/5,3/5)` | `(6/5,6/5,6/5)` | `3/2` |

## 4. The exact adapter from cover gain to the complementary pair

Define a new typed adapter from the certified cover quantities:

```text
p=W/(W+Lambda),
q=Lambda/(W+Lambda),
delta=(W-Lambda)/(W+Lambda).
```

Then `p+q=1` and `p/q=W/Lambda` identically. This is a normalization
of **physical residual strength and maximum energy load**. For the
balanced cover,

```text
(W,Lambda)=(3/2,1)  ->  (p,q)=(3/5,2/5)
                              -> delta=1/5,
                              -> signed -p+q=-1/5.
```

This coupling gives the numeric intuition a concrete receiver. It
also records why the half-weighted three-cover scheme and the 6:4
pair can describe the same ratio while occupying different ports.
The construction does not independently select `0.6` as a vacuum
parameter; it computes `0.6` from a proved cover ratio.

The adapter forgets common scale. For a supplied positive pair `(p,q)`,
the complete positive `(W,Lambda)` preimage is
`MANY({(s p,s q):s in Q, s>0})` before cover compatibility is imposed. For
the present three-weight carrier, cover compatibility requires
`1<kappa=p/q<=3/2`, or equivalently `0<delta<=1/5`.

There is also a complete bounded normalized weight fiber. Set `W=1`
and `mu=1-1/kappa`. It consists of every labeled permutation of

```text
(mu,t,1-mu-t),        mu<=t<=1-2mu,
```

with rational parameters. Every such triple has minimum `mu` and
therefore the required ratio; conversely every compatible triple
has an entry equal to its minimum and occurs in this family. At
`kappa=3/2`, this reduces to the single balanced triple. For
`1<kappa<3/2`, it is a complete MANY family. Values outside that
ratio interval have no positive three-weight completion under this
contract. This is a solved weight fiber, not a solved spectral fiber.

## 5. Hostile boundaries and the next useful obligation

**An unchanged number can hide a changed receiver.** In the source
paper's product-Haar control on `SU(2)^3` without gauge restriction,
the three coordinate-pair blocks with weights `1/2` still have
`W=3/2,Lambda=1`, hence the same normalized pair `(0.6,0.4)`. A
centered function of the first coordinate has zero residual in the
block omitting that coordinate. The actual residual constant is one,
not `W`. With `C_0=1/3`, the correct certificate is `3/2`, whereas
substituting `W` incorrectly would claim `9/4`. Thus the adapter
preserves the certified physical cover ratio only with its forest
and gauge premises retained. For a general cover its actual numerator
must be the proved `delta_w`, which need not equal the total weight.

**The dimension and cover incidence matter.** In two dimensions the
direction-cover ratio is two. If a purported three-direction graph
has only `x,y` edges, the third pair load need not occur: only
`b+c` and `a+c` constrain the maximum. Taking `a=b=1,c=1/10` gives
ratio `21/11>3/2`. This does not contradict section 3, which required
all three directions. The source's optimized two-square cover also
achieves a different finite-graph factor. Neither `3/2` nor its
normalized `0.6/0.4` pair is a universal constant across those changes.

**Equal halves and signed offsets are active operations.** The
additive transfer, chart translation with retained reference, and
positive cover normalization above all have exact laws. None
supplies a signed-variance subtraction rule. Using negative cover
weights would change the positive residual-form contract and would
require a fresh proof of the inequality, its enabledness, and its
energy charge.

The algebra, the weight optimum, and the complete scalar/weight fibers
are new written derivations in this note. A new in-memory exact
`fractions.Fraction` check verified the five table rows and their
ratio/discrepancy identities, all `20^3=8,000` positive integer weight
triples with entries at most 20, and the `0.6/0.4/t` bound at 1,000
positive rational values `t=k/100`. These finite checks confirm
arithmetic; the written proofs establish the full stated families.
No previous checker campaign was replayed, and no spectral computation
or new vacuum construction was performed.

The next obligation is **OPEN**: give an analytic compensator that
changes a currently limiting vacuum or conditional estimate, together
with the actual positive residual numerator and every charged
derivative contribution. For a proposed parameter-dependent weighting,
the comparison is `delta_w/M_w` with its proved conditional constants;
with the present common `C_0` and three direction blocks, unequal
weights have already been exhausted and cannot improve `3/2`.
A compensator acting on a retained vacuum remainder would instead
need a state/reference map and a bound on that remainder in the next
conditional operation. The numeric relation provides a precise
coordinate for auditing that proposal; it does not close the missing
analytic port by itself.
