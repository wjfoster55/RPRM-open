# Independent review of the operational source improvement

12 September 2026. Written mathematical review of `COMBINED_RESULT.md`,
`CHANNEL_SOURCE.md`, and `SPECTRAL_CHANNEL.md`, including inspection of
the new coefficient and incidence programs. This review writes only this
file. No old checker or BSD program was replayed. Section 7 binds the
final portable mathematical texts after their final inspection.

**Disposition:** no blocking mathematical defect found in the retained
channel/source bound or its stated finite-lattice construction and gap
consequences. The square-root coefficient is supported by the written
vertex-tensor argument, independently of the finite matrices. One minor
decimal-rounding correction was requested and is now applied. The conclusion relies on
the explicitly accepted all-spin norm, regularity and conditional-cover
theorems; the new finite source calculation does not replace them.

## 1. Exact review boundary and correction to the donor framing

I read the current candidate record, all three new mathematical notes,
both new probe programs, and the load-bearing sections of the accepted
`LOCAL_VACUUM_ROUTE.md`, `GAUGE_NORM_GAIN.md`,
`TWO_SQUARE_GEOMETRY.md`, and `CONDITIONAL_OBSTRUCTION.md` in
`research/ym2_conditional_construction/`.

The accepted `TWO_SQUARE_GEOMETRY.md` already proves that `(a,b,c)` is the
complete two-square gauge quotient and gives its exact reduced kinetic
operator. Its closure is an accepted result. An earlier version of
`BSD_DONOR.md` incorrectly described computing this closure as the next
new task. The coordinator has corrected that wording. The present new
content is the precise spectral response retained by the two channels,
their actual oriented coefficient norms and output supports, and the
resulting sharper source estimate. It must not be described as discovering
the already accepted `c` closure.

The broader RPRM operation-and-relation profile remains the stated donor
meaning. The current spectral receiver is one scoped realization. Neither
the finite BSD carry nor equality of numeral spellings enters the YM
proof as a premise.

## 2. Why the exact channel norm proof works

The source uses the unchanged coefficient convention
`f_J=Tr(B_J pi_J)`, Fourier norm `||B_J||_1`, and anchored energy weight
`lambda_J`. This convention matters: replacing the actual oriented
coefficient by a differently oriented loop estimate can alter this norm.

For adjacent squares the spin decomposition on their unique shared link
is exactly `0 plus 1`. It yields `f0=c/4` and `f1=ab-c/4`, with energies
9 and 13. Every exterior link remains fundamental; only `f0` loses the
shared link. The product rule gives `Gamma(a,b)=3f0-f1`. The signs cannot
cancel between these distinct full product-group Fourier blocks.

I checked the following argument for the numerical norms, rather than
inferring the result from the probe's four matrices:

1. The vectorized product coefficient factors into vertex tensors on the
   theta graph. The two half-trace normalizations give the scalar `1/4`.
   There are four degree-two exterior vertices and two shared endpoints.
2. A degree-two invariant pairing has Hilbert norm `sqrt(2)`. The
   shared-endpoint tensor in channel `ell` is a Clebsch--Gordan inclusion
   with squared Hilbert norm `d_ell=2ell+1`. The two inclusions therefore
   give `||B_ell||_HS=(1/4)(sqrt(2))^4 d_ell=d_ell`.
3. At a mixed vertex, one irreducible edge space is isolated on one side
   of the actual matrix row/column partition. Its reduced positive
   matrix commutes with the irreducible gauge action, hence is scalar.
   The nonzero Schmidt spectrum is flat and its rank is that edge's
   dimension. At a pure source/sink vertex the rank is one. These are
   local tensor statements; no individual singular vector of the whole
   Fourier coefficient is assumed gauge invariant.
4. Each exterior three-edge path contributes one mixed and one pure
   exterior vertex, so the four exterior vertices give total rank four.
   Same-sign transverse sides give shared-endpoint rank products one in
   the singlet channel and three in the triplet channel. Opposite signs
   give rank product four in both channels. The complete ranks are thus
   `(4,12)` and `(16,16)` respectively.
5. Flat singular values and the Hilbert norms then determine the trace
   norms uniquely. They are `(2,6 sqrt(3))` for same-side `f0,f1`, and
   `(4,12)` for opposite-side `f0,f1`. Multiplying the singlet norm by
   three gives source norms `6+6 sqrt(3)` and `24`.

Unitary basis changes on the appropriate representation or dual spaces
and separate row/column permutations preserve these calculations. No
unproved invariance under selected coordinate inversion is needed. The
coplanar rectangle is a real saturation case for the universal value 24;
using the smaller bent-pair value for every adjacent pair would be false.

The same-square character calculation is consistent with the original
coefficient convention: dimension `n` gives `n^2` orthogonal singular
directions with singular value `n`. At spin one, `n=3`, so the exact
norm is 27. The self contribution after its prefactor is `27/72=3/8`.

Inspection of `channel_probe.py` agrees with this argument. Its integer
matrix is `16 B_ell`; its Gram identities and traces recover the stated
singular values and ranks without a floating-point SVD. Those checks
corroborate the explicitly covered orientation classes. The tensor proof
and orientation classification supply the mathematical coverage.

## 3. Anchored support and exact incidence

In the anchored norm of `T^-1 Q Gamma`, the output eigenvalue cancels the
inverse eigenvalue once. For the shared anchor, the singlet is absent and
only the triplet trace norm is charged. For an exterior anchor, both
channels are charged. This is a strict source-specific refinement of the
older union-support estimate, with no change of norm and no second
inverse-energy factor.

The unordered distinct pair has prefactor `r^2/36`, because it occurs
twice in `Gamma(S,S)`. Its anchor costs are therefore:

| Position | Same-side | Opposite-side |
|---|---:|---:|
| Shared link | `sqrt(3)/6` | `1/3` |
| Exterior link | `(1+sqrt(3))/6` | `2/3` |

At a full lattice anchor, `m/2` adjacent squares have each transverse
sign. Common-link counts are `m(m-2)/4` same-side and `m^2/4`
opposite-side. An exterior-anchor pair is uniquely specified by its
plaquette containing the anchor, one of that square's three other edges,
and another square at that edge. Exactly one plaquette of this pair
contains the anchor. The counts are `3m(m-2)/2` and `3m^2/2`.

The uniqueness argument uses two actual elementary squares sharing at
most one edge. It rules out double counting in the exterior case.
For `m=2` the four counts are `(0,1,0,6)`; for `m=4` they are
`(2,4,12,24)`. Every positive-coordinate axis has the same local pattern.
The inspected incidence program implements this actual lattice geometry.
Removing plaquettes only removes nonnegative triangle-bound contributions,
which proves coverage at boundaries and for admitted open subgraphs.

Combining these costs with the self terms gives

```text
kappa_m = 4m^2/3-m/8+7 sqrt(3)m(m-2)/24.
```

Thus the dimension-two coefficient is `61/12` and the dimension-three
coefficient is `125/6+7 sqrt(3)/3`. The normalized coefficients satisfy

```text
kappa_2/2^2 = 61/48,
kappa_4/4^2 = (125+14 sqrt(3))/96 < 25/16.
```

The last strict comparison is exactly `14 sqrt(3)<25`, with positive
sides and squared comparison `588<625`. The notation `kappa_m` here is
indexed by plaquettes per link; `COMBINED_RESULT.md` sometimes indexes
the same two numbers by spatial dimension. Its explicit equations avoid
ambiguity.

This is an upper bound on the complete source sum, not a claim of global
norm optimality. Coincident contributions to one full Fourier block may
cancel; triangle inequality safely ignores that possible further gain.

## 4. Actual correction, ball margins, and the gap readout

The exact correction equation has source `h=(1/2)B(u0,u0)`, source head
`||u0||_*<=4x`, and the accepted invariant bilinear constant `1/3`.
Substitution of the improved source bound gives precisely

```text
M_x(Z)=(25/16)x^2+(4/3)xZ+Z^2/6,
L_x(Z)=(4x+Z)/3.
```

The factor in the mixed term follows by expanding the symmetric bilinear
map; there is no missing factor two. Reality and gauge invariance are
preserved by the complete iterates. The accepted Banach-space and elliptic
arguments, rather than a finite Taylor truncation, then construct the
actual positive vacuum when the displayed strict ball/contraction tests
hold.

I independently recomputed the endpoint values with exact rational
arithmetic in a new in-memory calculation:

| `x` | `Z` | `Z-M_x(Z)` | `L_x(Z)` | `q` bound | `D` bound |
|---|---|---|---|---|---|
| `1/3` | `7/20` | `1/2400` | `101/180` | `4/5` | `41/90` |
| `7/20` | `5/12` | `13/6912` | `109/180` | `163/180` | `23/45` |

The conditional conversions `q<=x+4Z/3` and `D<=2(x+Z)/3` match the
accepted LV25. In particular, the improved single-link factor uses the
nonzero invariant-block lower energy six; the collective bound retains
its separate all-spin support summation. An inverse-energy gain is not
being counted twice.

Both scalar majorants are monotone in nonnegative `x`. The strict endpoint
ball margins therefore give the claimed closed intervals. Substituting
the positive `1-q` margins into the accepted forest-cover theorem gives
OC3 and OC4 with their stated physical-sector qualification. For cubic
graphs the electric-unit bounds are respectively
`0.285343017635...` through `r=1/12` and `0.127463605559...` through
`r=7/80`. The coupling endpoint is multiplied by `21/20`, exactly 5%.

**Minor correction:** the reviewed combined note wrote the first decimal
as “about 0.2854.” To four decimal places it is **0.2853**. The exact
formula and every rational inequality are correct. This issue affects
presentation only. The coordinator has applied the correction, and the
updated `COMBINED_RESULT.md` was checked to read “about 0.2853.”

The smaller-root existence threshold is
`1/(4/3+5/sqrt(24))=0.4248171267...`. Conditional positivity requires
`Z<3(1-x)/4`. Substitution into `M_x(Z)-Z` gives exactly
`(21x^2+50x-21)/32`; its positive root is
`(sqrt(1066)-25)/21=0.3642693064...`. The conditional-radius cutoff
lies below the quadratic majorant's vertex throughout this interval,
so crossing this root really does lose simultaneous feasibility for
this scalar certificate. Neither threshold proves an actual gap closes.

## 5. Spectral continuation and its all-spin limitation

The accepted equations imply `h=ab-c/4` has energy 13 while `c` has
energy 9. The minimal invariant span generated by `ab` is therefore
`span{c,h}`, with `T^2=22T-117I`. Knowing `ab` and `T(ab)` reconstructs
both channels; this establishes minimality for the declared kinetic
receiver, not for the interacting Hamiltonian.

I checked the pointwise cancellation witnesses, their actual `Omega`
admission determinants, the resolvent formulas, the two-probe determinant
and inverse, and the local supremum argument. They are consistent.
The local supremum is a pointwise norm using the complete `c` fiber;
it cannot be substituted for the anchored Fourier norm. The latter
adds positive norms of distinct full output blocks. The `L2` formula
also uses orthogonality, giving `||B(a,b)||_2=7/156` consistently.

For the all-spin hostile family on one square, the actual character
product `chi_j chi_(1/2)=chi_(j-1/2)+chi_(j+1/2)` produces both complete
source channels, with coefficients `8(j+1)` and `-8j`, and positive
energies `8j^2-2` and `8j^2+16j+6`. Every link anchors both outputs.
For a fixed positive shift, the ratio of shifted to unshifted anchored
norm is a positive weighted average of `lambda/(lambda+z)` and tends
to one as `j` grows. This is a genuine bilinear-range obstruction to
a uniform factor below one, including on a fixed graph. It is not a
finite-spin observation extrapolated without a formula.

The interacting witness with equal `(c,h)` and unequal `a+b` gives
the claimed difference `-r/48` in `A(r)c`. It correctly limits the
kinetic operational quotient while preserving the accepted larger
`(a,b,c)` quotient.

## 6. Claims that remain outside this result

The source-weight improvement yields a larger sufficient coupling
interval and stronger explicit finite-lattice physical-gap certificate
using the accepted all-spin analytic machinery. The contribution is
not a new generic bilinear constant, an optimal endpoint, or an optimal
global source norm. The graph-uniform bound is in the inherited electric
units and does not construct an infinite-volume representation by itself.

The physical scaling relations `r=8/g_b^4` and
`E_el=g_b^2/(4a)` remain load-bearing. Along the stated small-bare-coupling
continuum route, `r` grows beyond these bounded windows. Continuum
existence, a nontrivial limiting quantum theory, and a positive limiting
excitation scale remain OPEN. No BSD theorem, spectral-shift analogy,
or finite channel census supplies those missing ports.

This is an independent written review and exact scalar check, not a
formal proof-assistant certificate or external peer review. The source
norm argument is accepted at its stated carrier and orientation contract.
Any change to the norm, loop family, charges, gauge constraints, output
support rule, or analytic dependency requires a corresponding new audit.

## 7. Final portable text inspection and SHA-256 bindings

Final inspection: 12 September 2026, approximately 18:48 America/Denver
(`2026-09-13 00:48 UTC`), after the coordinator froze the mathematical
files. I read `SOURCE_PROVENANCE.json`'s `link_remaps` and
`reviewed_files`, reread the final source/channel and combined proofs,
and checked the latest donor section I authored. All four hashes below
match the provenance record. All 15 declared link remaps resolve, and
their 12 distinct copied targets match the recorded byte counts and
SHA-256 hashes.

The changes must be described precisely: they were not literally only
link-target byte replacements. `CHANNEL_SOURCE.md`, `SPECTRAL_CHANNEL.md`
and `BSD_DONOR.md` also acquired CRLF line endings during portable
rewriting. Reversing the seven declared donor link replacements and
normalizing CRLF to LF exactly recovers my final authored donor hash
`8a22a59b6f44d3a737a3adfdafd964bf9ff2cc3e8d28ba2dd769fa455b031f28`.
This verifies that its latest column-handoff text, completed-task status,
hostile cases and claim limits are preserved without additional content
changes. The donor's section 6 historical source hashes remain dated
earlier observations; final copied-source hashes are separately recorded
in provenance.

The coefficient proof's mathematical content remains the content reviewed
above. The final spectral note additionally contains an explicit
resolvent formula and a reproducible exact-arithmetic excerpt that were
added after my initial read. I inspected both additions and include them
in this final written review. The formula is

```text
R_z f=[(22+z)f-Tf]/[(9+z)(13+z)] on W.
```

It follows directly by multiplying its numerator by `T+z`: the resulting
operator is `22T-T^2+(22z+z^2)I`, hence
`(117+22z+z^2)I` by SP4. This is the displayed denominator times the
identity. The arithmetic excerpt reproduces the already reviewed
admission determinants, separating responses and `L2` normalization.
Its reported PASS remains attributed execution evidence; no old checker
or BSD program was rerun during final binding. The combined result's
requested decimal correction to 0.2853 and the donor's accepted-closure
correction remain present.

The final copied `column_handoff_extended.json` also matches the latest
donor's recorded hash
`5df84c3ba6eca77c41f851ec4152a1b9ddd445fce9fb37b129cabee263a469c1`.
Its source binding was checked in the prior donor update. This preserves
the distinction between the completed finite operational audit and the
still-open BSD comparison or terminal-readout selection.

| Final file in this directory | Bytes | SHA-256 |
|---|---:|---|
| `CHANNEL_SOURCE.md` | 15281 | `ff817b7cb2700636e4ad1497120c6f67765d51d75ef5148fa237abc1c2361d38` |
| `SPECTRAL_CHANNEL.md` | 19294 | `d69f9413b85dfe6bb3ae64fb32fef32d731951eb8674765d95c709d2f2a19c01` |
| `COMBINED_RESULT.md` | 7189 | `db8c340ae3f8955ee439249e56a5752a6edb6d3ef7af9cfa862aa0bc293cefe3` |
| `BSD_DONOR.md` | 21257 | `54d161387b6172e7ba98109c3cae4fd3d28a1ff2ba1b2b897c934de3f9ef609c` |

No blocking mathematical issue was found in these final texts at their
declared contracts. This is a **written mathematical review**, with
bounded arithmetic checks and byte verification, **not a formal proof**.
The hashes bind the exact reviewed bytes; they do not establish the
truth of their contents independently of the written arguments or
expand any finite-lattice conclusion into a continuum mass-gap result.
