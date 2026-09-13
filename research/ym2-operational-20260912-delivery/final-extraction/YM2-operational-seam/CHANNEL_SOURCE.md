# Exact source channels and the anchor they retain

12 September 2026. New written derivation and exact finite coefficient
checks. Prior artifacts are unchanged.

**Result.** The adjacent-pair Fourier norm `24` is attained by actual
positive-coordinate plaquettes. It cannot be lowered uniformly. It can,
however, be allocated more accurately: its singlet channel loses the
shared link, and some bent pairs have a strictly smaller norm. These facts
lower the source coefficient in the existing actual-vacuum construction to

```text
||z2||_* <= kappa_m r^2,
kappa_2 = 61/12,
kappa_4 = 125/6 + 7 sqrt(3)/3,
kappa_m/m^2 <= (125+14 sqrt(3))/96 < 25/16.             (CS1)
```

Here `m=2(d-1)` is the maximum number of elementary plaquettes at a link,
with `d=2,3`. The old LV23 coefficients were `65/12` and `59/2`.
The all-input bilinear constant `K=1/3` is unchanged. CS1 concerns the
actual second-order source, including its exact output supports; it is
not an all-spin improvement of that bilinear constant.

## Contract and dependencies

The carrier is the positive-coordinate oriented square/cubic lattice,
or an admitted finite open subgraph, with distinct elementary plaquettes,
full vertex gauge invariance, normalized product Haar measure, no charges,
and the accepted SU(2) generators `i sigma_k`. Thus
`lambda_j=2j(j+1)` and `T=-Delta/2`. Link occurrences remain distinct.
Functions have their usual almost-everywhere equality; coefficient matrices
are unique in each product-group irreducible block.

The supplied norm convention is

```text
f_J(U)=Tr(B_J pi_J(U)),      ||f_J||_A=||B_J||_1,
||f||_*=max_e sum_(J:e in supp J) lambda_J ||B_J||_1.
```

There is no additional representation dimension factor outside `B_J`.
The operation being refined is the actual source

```text
z2=(r^2/72) T^-1 Q Gamma(S,S),      S=sum_p a_p.
```

The receiver retains the output channel, its Fourier trace norm, and
whether a specified anchor link remains in its support. `T^-1` divides
each nonzero channel by its total Casimir; this division cancels the
energy weight in the displayed anchored norm exactly once. This is a
forward coefficient calculation, not a solved interacting spectral fiber.
The full vacuum and continuum fibers remain OPEN.

Dependencies are the original coefficient convention and oriented source
calculation in
[`SOURCE_NORM_REFINEMENT.md`](accepted/research/ym2_conditional_construction/accepted/research/ym2_overlap_cover/accepted/estimate/SOURCE_NORM_REFINEMENT.md),
the exact local algebra LV5--LV10 and source summation in
[`LOCAL_VACUUM_ROUTE.md`](accepted/research/ym2_conditional_construction/LOCAL_VACUUM_ROUTE.md),
and the invariant-space bilinear theorem GN20 in
[`GAUGE_NORM_GAIN.md`](accepted/research/ym2_conditional_construction/GAUGE_NORM_GAIN.md).
The geometric meaning of the retained joint variable is supplied by
[`TWO_SQUARE_GEOMETRY.md`](accepted/research/ym2_conditional_construction/TWO_SQUARE_GEOMETRY.md)
and its failure to descend to two separate trace coordinates by
[`CONDITIONAL_OBSTRUCTION.md`](accepted/research/ym2_conditional_construction/CONDITIONAL_OBSTRUCTION.md).

## The two complete output channels

For two distinct adjacent plaquettes write `a=a_p`, `b=a_q`, and let `i`
be their unique common link. To avoid ambiguity with a chosen loop word,
define the outer-loop half trace by

```text
c=4 integral a b dmu_i.
```

The exact shared-link decomposition is

```text
f0=c/4,             f1=ab-c/4,
ab=f0+f1,
Gamma_i(a,b)=c-ab=3 f0-f1,                              (CS2)
T f0=9 f0,          T f1=13 f1.
```

Here `f0` has spin zero on `i` and spin one-half on all six exterior
links. The block `f1` has spin one on `i` and spin one-half on those six
links. These are the only channels, because the common fundamental pair
decomposes as `0 plus 1`; every exterior link occurs once. Both channels
have zero full Haar mean, so `Q` removes neither one.

Distinct blocks contribute additively to the Fourier norm, hence

```text
||Gamma_i(a,b)||_A = 3 ||f0||_A + ||f1||_A.             (CS3)
```

At the shared-link anchor, only the second term contributes after
`T^-1`. At any exterior-link anchor, both contribute. The distinction is
between two output supports of one joint source operation, rather than
two unrelated estimates of the same scalar.

## Exact coefficient singular values from vertex tensors

The derivation uses unitary changes of basis and permutations separately
within coefficient rows and columns. It does not assume that inverting
selected group coordinates preserves this nonabelian Fourier norm.

The union is a theta graph: four exterior vertices have degree two, and
the two endpoints of the common link have degree three. Vectorize the
coefficient matrix and group its endpoint indices by vertex. The coefficient
tensor of `ab`, with its two factors `1/2`, is a product of vertex delta
tensors with overall scalar `1/4`.

Choose the fundamental or dual representative dictated by each actual
traversal. At the shared link the representation is `U tensor conjugate(U)`.
Its singlet/triplet change of basis is unitary. Compress both coefficient
indices to channel `ell=0,1`. This inserts one Clebsch--Gordan tensor at
each shared endpoint; no other edge is fused. Because each external link
is still fundamental, the resulting vectorized coefficient factors by
the six vertices. This describes the unique actual coefficient in that
product-group irreducible block.

Write `d_ell=2ell+1`. Each degree-two tensor is an unnormalized invariant
pairing, with squared Hilbert norm `2`. Each shared-endpoint tensor is the
Clebsch--Gordan inclusion of the channel into two fundamental factors,
with squared Hilbert norm `d_ell`: the inclusion is isometric on its
`d_ell` orthonormal channel states. Therefore the coefficient has

```text
||B_ell||_HS = (1/4) (sqrt(2))^4 (sqrt(d_ell))^2
            = d_ell.                                   (CS4)
```

As a normalization check, the product-group dimension is `64 d_ell`.
Peter--Weyl orthogonality gives
`||f_ell||_L2^2=d_ell/64`; their sum is `1/16`, the Haar moment of
the product of two independent half traces.

It remains to compute the Schmidt rank of this vectorized coefficient
across its matrix row/column partition. At a vertex with both incoming
and outgoing incident edges, a degree-two or degree-three tensor has
exactly one edge on one side of the partition. Its reduced positive
matrix on that edge is scalar by gauge invariance and irreducibility.
Consequently all of its nonzero Schmidt coefficients are equal, and its
Schmidt rank is the dimension of that isolated edge. If all edges at
the vertex point in or all point out, its rank is one.

This applies equally to dual representatives. It requires neither a
gauge-invariant singular vector of the whole coefficient nor a chosen
coordinate basis for its singular vectors. Tensor products multiply
these ranks and their flat Schmidt spectra.

For one elementary square adjacent to the common link, its two exterior
vertices have one mixed vertex and one pure source/sink vertex in the
positive-coordinate orientation. Thus the four exterior vertices
together contribute Schmidt rank `2*2=4` in both channels.

Orient the shared edge positively. Each incident plaquette extends in
one positive or negative transverse coordinate direction. Call a pair
**same-side** when these two signs agree and **opposite-side** when they
differ. Agreement is possible only for different transverse axes; there
are no duplicated elementary plaquettes. This sign classification is
equivalently the following basis-independent orientation pattern at
the two shared endpoints:

| Pattern | Shared-endpoint tensor splits | Product of endpoint ranks, ell=0 | Product of endpoint ranks, ell=1 |
|---|---|---:|---:|
| Same-side | One pure vertex; at the other, the common edge is isolated | 1 | 3 |
| Opposite-side | At both vertices, one exterior fundamental edge is isolated | 4 | 4 |

In the singlet channel the common edge has dimension one; its removal
gives exactly the same ranks recorded in the table. Including the
exterior factor four, the complete ranks and singular values are

| Pattern | Channel | Rank | Each nonzero singular value | Trace norm |
|---|---|---:|---:|---:|
| Same-side | f0 | 4 | 1/2 | 2 |
| Same-side | f1 | 12 | sqrt(3)/2 | 6 sqrt(3) |
| Opposite-side | f0 | 16 | 1/4 | 4 |
| Opposite-side | f1 | 16 | 3/4 | 12 |

The singular values follow from CS4 and the flat spectrum. Therefore

```text
same-side:      ||Gamma_i(a,b)||_A=6+6 sqrt(3),
opposite-side:  ||Gamma_i(a,b)||_A=24.                   (CS5)
```

In particular the coplanar adjacent rectangle is an exact saturation
case for `24`. Opposite-side bent pairs also attain it. Same-side bent
pairs give the smaller value in CS5. Treating all adjacent pairs as
having that smaller value would fail on the ordinary rectangle.

## The self-pair norm 27 is exact

For one source plaquette the exact nonconstant self pairing is

```text
Q Gamma(a_p,a_p)=-chi_(1),p.
```

This is one block, with spin one on all four square edges. More generally,
for the raw character of the actual oriented four-edge word in a unitary
irreducible representation of dimension `n`, its coefficient is

```text
C=sum_(a,b,c,d) |b,c,c,d><a,b,d,a|
 =sum_(b,d) |v_(b,d)><w_(b,d)|,
v_(b,d)=sum_c |b,c,c,d>,   w_(b,d)=sum_a |a,b,d,a>.
```

Both families are separately orthogonal, with `n^2` members and norm
`sqrt(n)`. Thus `C` has `n^2` nonzero singular values equal to `n`.
The dual representatives at inverse edges are unitarily equivalent to
the declared SU(2) representatives. With `n=3`,

```text
||Q Gamma(a_p,a_p)||_A=27.                              (CS6)
```

This local value admits no further improvement in the retained norm.
One self pair contributes exactly `27/72=3/8` to each of its four
anchored source sums after inverse-energy cancellation.

## Anchor accounting and the source coefficient

An unordered distinct pair occurs twice in `Gamma(S,S)`, so its
contribution has prefactor `1/36`, not `1/72`. By CS2--CS5 its anchored
cost is as follows:

| Anchor position | Same-side pair | Opposite-side pair |
|---|---:|---:|
| The common link | sqrt(3)/6 | 1/3 |
| An exterior link | (1+sqrt(3))/6 | 2/3 |
| Outside the union | 0 | 0 |

For a simple orientation-independent improvement, bound these by `1/3`
at a common-link anchor and `2/3` at an exterior anchor. There are at most
`m(m-1)/2` pairs sharing an anchor, and at most `3m(m-1)` pairs having
it as an exterior link. This already gives

```text
kappa_m <= (3/8)m+(13/6)m(m-1).                         (CS7)
```

The positive-coordinate orientation gives a sharper count. At any link
in the full lattice there are `m/2` positive-side and `m/2` negative-side
incident squares. For pairs sharing the anchor, the same-side and
opposite-side counts are therefore `2 choose(m/2,2)` and `(m/2)^2`.

For exterior-anchor pairs, first choose the unique plaquette `p`
containing the anchor (`m` choices), then its common link with `q`
(`3` choices other than the anchor). At that link, among the other
plaquettes `q`, exactly `m/2-1` have the same side sign as `p` and
`m/2` have the opposite sign. This counts each unordered pair once:
exactly one of its two plaquettes contains the exterior anchor, and
distinct elementary plaquettes share at most one link.

Thus the four counts are

```text
shared same:    m(m-2)/4,    shared opposite:   m^2/4,
exterior same:  3m(m-2)/2,   exterior opposite: 3m^2/2.  (CS8)
```

Every allowed finite subgraph embeds in this full local incidence
pattern. Removing plaquettes only removes nonnegative contributions
from these bounds, so CS8 is sufficient at boundary links as well.

Combining the cost table, CS6, and CS8 gives

```text
kappa_m = 3m/8
 + [m(m-2)/4] sqrt(3)/6 + [m^2/4]/3
 + [3m(m-2)/2] (1+sqrt(3))/6 + [3m^2/2] (2/3)
 = 4m^2/3-m/8+7 sqrt(3)m(m-2)/24.                       (CS9)
```

For `m=2,4` this is CS1. The maximum normalized coefficient is at `m=4`.
The rational upper bound `25/16` follows from
`125+14 sqrt(3)<150`; squaring the positive comparison `14 sqrt(3)<25`
reduces it to `588<625`.

CS9 is a proved upper bound for the full source sum, using the triangle
inequality between contributing coefficients. The individual channel
norms and their support losses are exact; no optimality claim for the
global source coefficient is needed. Potential coincidences or
cancellations between different pairs can only lower this bound.

## Evidence, hostile boundaries, and continuation

The new executable [`channel_probe.py`](channel_probe.py) independently
constructs the two actual trace coefficients on eight occurrence factors,
then identifies the shared two factors by singlet/triplet compression.
It treats the full source polynomial, with no approximation to its
Fourier support and no truncation of the Hamiltonian's state space.

The singlet projector on `U tensor conjugate(U)` is the projector onto
`(|00>+|11>)/sqrt(2)`. Twice this projector, twice its complement, and
four times the product coefficient all have integer entries. The script
therefore checks the channel coefficients multiplied by 16 using exact
integer matrix products. Their Gram matrices obey `G^2=kG`; their traces
determine the exact ranks, with `k=16,144` for opposite-side channels and
`k=64,192` for same-side channels. Their entries are small enough that
these products lie within signed 64-bit integer arithmetic. The self
character check uses its full `81`-dimensional coefficient and verifies
`G^2=9G`, `Tr G=81`. No floating-point SVD is used.

Executed command:

```text
python -B research/ym2_operational_seam/channel_probe.py
```

Observed result: **PASS** for coplanar opposite-side, bent opposite-side,
and both same-side signs, the self-character matrix, and rational
arithmetic in CS8--CS9. The written tensor argument supplies orientation
coverage and basis independence; the finite checks verify its explicit
small matrices. No old checker, package installation, git action,
simulation, or publication was performed.

The hostile rectangle prevents a false universal improvement below
`24`; the shared-anchor case prevents charging its absent singlet
support; the same-side bent case prevents replacing all actual output
norms by a single orientation-blind equality. Selected coordinate
inversions, charges, non-elementary loops, duplicate plaquettes, and
additional lattice dimensions require their own contracts and counts.

For continuation, insert CS1 as the improved `h=kappa_m r^2` in the
unchanged actual correction equation LV13--LV14, with the independently
proved `K=1/3`. This transfers a rigorously smaller source defect while
retaining every all-spin iterate and the same norm. A second inverse
factor must not be inserted: the output Casimir already canceled in
the anchor cost table. The source-channel result alone proves neither
an optimal gap nor a continuum mass gap.
