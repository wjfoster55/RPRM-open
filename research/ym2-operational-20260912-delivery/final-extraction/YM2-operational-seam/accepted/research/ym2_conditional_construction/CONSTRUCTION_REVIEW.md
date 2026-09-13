# Independent audit of the new actual-vacuum construction

12 September 2026. Independent written review of
[LOCAL_VACUUM_ROUTE.md](LOCAL_VACUUM_ROUTE.md), LV3--LV27, and
[GAUGE_NORM_GAIN.md](GAUGE_NORM_GAIN.md), including its final section 8,
GN14--GN22. The latter's `1/3` bilinear estimate supersedes its earlier
`4/9` estimate. Both have been checked. No old file or old verifier was
changed or rerun.

**Disposition:** the reviewed new estimates and their stated
fixed-point consequences follow at their declared finite-graph,
full-SU(2), all-spin scope. The source-specific construction using the
accepted `16/9` bound already supplies an actual vacuum and uniform
physical gap on `0<=r<=1/(12m)`. The independently checked gauge
coefficient argument improves the bilinear constant to `1/3`; its
combination with the source estimate is justified below. This is a
written mathematical audit, not a formal-proof or simulation receipt.

## 1. Norm, operator, and inherited analytic ports

The audit retains the accepted Fourier coefficient convention
`u_J=Tr(B_J pi_J)`, coefficient trace norm `b_J=||B_J||_1`, and

```text
lambda_J=sum_i 2j_i(j_i+1),
||u||_*=max_e sum_(J:e in supp J) lambda_J b_J,
B(u,v)=T^-1 Q Gamma(u,v),       T=-Delta/2.
```

The exact source bound is `||T^-1 S||_*<=4m`, with
`m=2(d-1)` and `d in {2,3}`. The zero mode is removed by `Q` before
inversion. Output energy weights cancel their inverse once in the
bilinear estimate. No second inverse factor is introduced.

The accepted sources read for this audit were
[DIRECT_COVER_ATTEMPT.md](accepted/research/ym2_overlap_cover/accepted/estimate/accepted/DIRECT_COVER_ATTEMPT.md),
DC2--DC12, and the original
[SIGNED_AND_CONTRACTED_AUDIT.md](accepted/research/ym2_estimate_continuation/SIGNED_AND_CONTRACTED_AUDIT.md),
especially SC3--SC10. The source coefficient and conditional/forest
transfer remain the explicitly supplied dependencies in the reviewed
notes. This audit checks the new adapters against those retained
contracts; it does not assign formal-proof status to the inherited
analytic results.

For fixed finite graphs, the norm controls absolutely convergent
derivatives through order two, as DC2/DC11 state. The fixed-point
equation therefore produces the pointwise elliptic equation and its
smooth positive solution after the accepted regularity continuation.
Gauge-invariant whole-isotypic truncations remain in the same normed
space. Thus the strengthened bilinear estimate is applied to the actual
iterates, rather than only to a finite polynomial ansatz.

## 2. Audit of the source-specific second-order estimate

The self-plaquette identities in LV6 have the correct metric factors:

```text
Gamma(a_p,a_p)=3-chi_(1),p,
chi_(1),p=4a_p^2-1,       T chi_(1),p=16 chi_(1),p.
```

The character coefficient in LV10 has `n^2` orthogonal right vectors
and `n^2` orthogonal left vectors, each of norm `sqrt(n)`. Normalizing
both families identifies exactly `n^2` singular values equal to `n`.
Its trace norm is consequently `n^3`; for spin one it is `27`.
This argument uses the oriented four-link word and its dual factors;
it does not assume that arbitrarily inverting individual arguments
preserves the Fourier norm. The corresponding self-source anchored
contribution is exactly bounded by `27/72=3/8` per plaquette.

For a pair of distinct adjacent plaquettes, the independently derived
[two-square obstruction](CONDITIONAL_OBSTRUCTION.md) gives
`Gamma_i(a_p,a_q)=c-a_p a_q`. The formulas

```text
T(a_p a_q)=13a_p a_q-c,       Tc=9c,
T^-1(c-a_p a_q)=(4c-3a_p a_q)/39
```

agree with LV7--LV9, including both the six-link singlet and seven-link
spin-one pieces. Every distinct unordered pair occurs twice in
`Gamma(S,S)`, so the norm prefactor is `1/36`. The accepted local
fundamental estimate is `2*4*4=32`, giving `8/9` per adjacent pair.

For a fixed anchor `e`, each plaquette containing it has at most
`4(m-1)` distinct neighbors. Two plaquettes both containing `e`
are counted twice by this incidence procedure. Subtracting exactly
`choose(k_e,2)` corrects that duplication once. Since two distinct
elementary squares share at most one link, there is no additional
duplicate through a second shared link. The resulting upper bound
`4k_e(m-1)-k_e(k_e-1)/2` increases for `0<=k_e<=m`, yielding
`(7/2)m(m-1)`. Boundary omissions only reduce the count.

This verifies

```text
kappa_m=(3/8)m+(28/9)m(m-1),
kappa_2=251/36,       kappa_4=233/6,
kappa_m/m^2 <= 5/2.
```

The estimate is source specific. It does not assert that the general
bilinear constant has changed merely because the correction was
recentered.

## 3. Audit of the first completed construction interval

With `s=rS/6` and `u=s+v`, the exact equation is

```text
v=z2+B(s,v)+(1/2)B(v,v),       z2=(1/2)B(s,s).
```

The residual is retained. This is not a claim that the second-order
polynomial solves the vacuum equation. At `r<=1/(12m)`, the old
accepted constant `K=16/9` gives `||s||_*<=1/3` and
`||z2||_*<=5/288`. For `Z=1/20`, exact arithmetic gives

```text
5/288+4/135+1/450=1063/21600<1/20,
K(1/3+1/20)=92/135<1.
```

Thus the closed correction ball is invariant and the map is a strict
contraction, including the stated endpoint. Reality, mean-zero gauge
invariance, regularity, and the positive-ground-state identity then
identify the actual vacuum. The corresponding full-space Bochner
bound `1-2(1/3+1/20)=7/30` is correctly normalized.

The all-exterior conditional conversions
`d_v<=(8/3)Z`, `b_v<=(16/3)Z` follow respectively from one-link and
four-value differences together with `lambda_J>=(3/2)|supp J|`.
Combining these with the explicit first-order reference gives

```text
D_actual<=17/90,       q_actual<=3/20,
gap_phys(A)>=[51d/(40(d-1))]exp(-17/90).
```

These are collective-response and actual-vacuum estimates, not a gap
claim inferred from conditional compatibility alone. The physical
excited-complement qualification remains necessary.

## 4. Audit of the gauge support bound and the 4/9 estimate

Each link isotypic projection commutes with its left and right gauge
translations. Every nonzero Fourier block of an invariant function is
therefore itself invariant. Vectorizing its coefficient exposes a
vertex invariant tensor, which requires the spin on any one incident
edge to be at most the sum of the other incident spins.

For an occupied link of spin `l`, the other edges at its two endpoints
have total spin at least `2l`. Their outer endpoints are all distinct:
simple graphs exclude parallel edges, and a shared outer endpoint at
the two original vertices would make a triangle. Applying the vertex
constraint at these outer endpoints counts edges outside the first
neighborhood at most twice. The total spin away from the chosen edge
is consequently at least `3l`. Since `2s(s+1)>=3s` for every
half-integral `s>=0`,

```text
lambda_K >= lambda_l+9l = l(2l+11) >= 6.
```

This proves GN6 without assuming that every occupied edge belongs to
one simple cycle. The equality examples on a fundamental square and
the spin-one central edge of a two-square theta graph have energies
6 and 13 and verify the load-bearing normalizations.

GN9 then uses either the accepted exceptional fundamental bound 2
or the all-spin operator bound `4min(j,l)(max(j,l)+1)`. Its three
cases exhaust the nonzero half-integral spins, and all inequalities
have the stated direction. Each asymmetric anchor sum costs `2/9`.
The two safe input-anchor indicators give `4/9`, as claimed.

## 5. Audit of the stronger coefficient argument: constant 1/3

The written convention in GN14 is consistent. Gauge invariance of
`Tr(B_J pi_J(U))` implies `R_J(g)B_J=B_J L_J(g)`. Taking adjoints
shows that `B_J^*B_J` commutes with `L_J` and `B_J B_J^*` commutes
with `R_J`. Functional calculus gives the same invariance for
`|B_J|` and `|B_J^*|`.

Partial trace over the other links eliminates their unitary
conjugations. Source gauge transformations then force the selected
link marginal of `|B_J|` to commute with the entire spin representation;
target transformations do the same for `|B_J^*|`. Irreducibility fixes
both marginals to `b_J I/(2j+1)`.

This does not make the individual singular vectors invariant.
The proof correctly applies Cauchy--Schwarz a second time after
summing their singular-value weights. Those weighted sums are exactly
the positive matrices just controlled. This validates GN16's bound

```text
||Gamma_i(u_J,v_K)||_A<=c(j,l)b_J d_K,
c(j,l)=Tr|Omega_(j,l)|/[(2j+1)(2l+1)].
```

The fundamental singlet/triplet dimensions give `c(1/2,1/2)=3/2`.
For every spin pair, the trace pairing of the generators gives

```text
normalized_Tr(Omega^2)=(4/3)lambda_j lambda_l,
c(j,l)<=sqrt((4/3)lambda_j lambda_l).
```

For target spin `l=1/2,j>=1`, this is at most `lambda_j`, while
`lambda_K>=6`. For `l>=1`, the gauge support bound yields

```text
lambda_K^2/lambda_l
 >= [l/(2(l+1))](2l+11)^2 >= 169/4 > 32.
```

Together with `lambda_j>=3/2`, this proves
`c(j,l)<=lambda_j lambda_K/6`. The fundamental pair satisfies that
same inequality exactly at its lower energy bound. Zero differentiated
spins contribute zero. Both anchor sums therefore cost `1/6`, giving
the reviewed all-spin estimate

```text
||B(u,v)||_*<=(1/3)||u||_*||v||_* on X_G^inv.
```

The continuation to the closed invariant normed space uses the same
whole-isotypic truncations and derivative identification as before.
The generic radius `R=3[1-sqrt(1-8m|r|/3)]` and interval
`|r|<3/(8m)` then follow from `R=4m|r|+R^2/6`. The GN22 radius
`1/4` endpoint `23/(384m)` and positive-curvature interval
`|r|<11/(96m)` also check by direct substitution.

## 6. Checked composition with the refined local source

Both plaquette inputs satisfy the stronger coefficient premises. Their
local pairing bound is now `(3/2)*4*4=24`. Replacing only the
distinct-pair estimate in section 2 gives

```text
||z2||_*<=kappa_m^inv r^2,
kappa_m^inv=(3/8)m+(7/3)m(m-1),
kappa_2^inv=65/12,       kappa_4^inv=59/2,
kappa_m^inv/m^2<=59/32.
```

This composition retains the same source, inverse, gauge subspace,
and support count. Hence it is compatible with the newly proved
`K=1/3` in the full correction equation. A simple checked closed
choice is

```text
x=mr<=1/3,       ||s||_*<=4/3,       Z=3/7.
```

Its ball and Lipschitz bounds are

```text
59/288+4/21+3/98 = 3/7-37/14112 < 3/7,
(1/3)(4/3+3/7)=37/63<1.                              (RV1)
```

There is also a sharper conditional density bound available because
every nonzero invariant Fourier block has energy at least 6:

```text
d_v<=4 sum_(J:i in supp J)b_J <= (2/3)||v||_*.
```

The old mixed bound `b_v<=(16/3)||v||_*` remains valid. Combining
these with the explicit reference gives at RV1

```text
D_actual<=2x/3+(2/3)Z<=32/63,
q_actual<=x+(4/3)Z<=19/21,
gap_phys(A)>=[d/(7(d-1))]exp(-32/63).                  (RV2)
```

Thus this reviewed composition itself supplies a closed actual
finite-graph construction and a positive volume-uniform physical
gap for `0<=r<=1/(3m)`, with the same physical-complement
qualification. RV1 is a strict contraction at its endpoint. It does
not rely on a positive Bochner bound for the comparatively larger
total log norm. A different endpoint may optimize these sufficient
constants; no such optimization is needed for RV1--RV2.

The subsequently written LV22--LV27 addendum was also read. Its open
construction endpoint `12/[m(16+sqrt(177))]` follows from the same
quadratic discriminant using `kappa_m^inv/m^2<=59/32`. Its choice
`x=1/3,Z=4/9` has ball margin `71/7776`, Lipschitz factor `16/27`,
conditional row bound `25/27`, and density bound `14/27`; every value
checks. RV1--RV2 use a smaller valid correction radius at that same
coupling. The addendum's alternative `x=1/4,Z=3/16` also checks, with
ball margin `1/256`, Lipschitz factor `19/48`, row bound `1/2`, and
density bound `7/24`. Its stronger gap on that smaller interval is
`[3d/(4(d-1))]exp(-7/24)`. These written addendum conclusions pass
the same independent audit.

## 7. Hostile boundaries and verification scope

- Full gauge invariance includes every boundary vertex. Boundary
  charges or omitted constraints invalidate the vertex and marginal
  arguments at those vertices.
- Triangle-free simple graphs are load bearing. A fundamental triangle
  has energy `9/2` and refutes the unchanged inverse-energy bound 6.
- Arbitrary one-link coefficient functions need not satisfy the
  intertwiner marginal constraints. Their unrestricted local pairing
  constant 2 is compatible with the physical local constant `3/2`.
- The two retained plaquette traces alone do not form a closed kinetic
  representation. The actual iterates admit the merged loop and all
  later generated invariant blocks; the construction does not assert
  a finite-range log vacuum.
- A finite-order residual is not discarded. The explicit extensive
  third-order witness in LV20 remains consistent with the convergent
  infinite correction.

A new standard-library rational calculation checked both kappa
families, the original radius fractions, the RV1 margin and contraction
factor, and the RV2 endpoint constants. Its result was PASS. It did
not enumerate spins, prove convergence by sampling, or rerun an old
verification suite. The all-spin, smooth, gauge and volume-uniform
implications rest on the written inequalities above and their stated
accepted analytic dependencies. Optimal constants, the unrestricted
strong-coupling domain, an infinite-volume vacuum representation, and
the continuum mass-gap problem remain OPEN.

## 8. Final combined statement and exact reviewed byte bindings

The final [COMBINED_RESULT.md](COMBINED_RESULT.md) and
[TWO_SQUARE_GEOMETRY.md](TWO_SQUARE_GEOMETRY.md) were read independently
after their mathematical text was complete. No mathematical defect was
found. This final audit includes the following checks.

The combined C1 uses precisely the reviewed `mr<=1/3,Z=3/7` ball,
its strict margin `37/14112`, and contraction factor `37/63`.
Its actual conditional constants are `q<=19/21` and `D<=32/63`, so
the forest factor gives `d/[7(d-1)] exp(-32/63)`. The dimension-three
and dimension-two endpoints and stated decimal approximations agree
with these expressions. C2 agrees with the separately reviewed
`mr<=1/4,Z=3/16` construction. The old closed uniform-gap endpoint
`9/(128m)` is justified by the accepted BLOCK_COVER O13 fixed-graph
eigenvalue-continuity argument; it does not require an old endpoint
Fourier contraction. Thus the endpoint ratio `128/27` compares
sufficient gap intervals in the same dimensionless parameter.

For the open construction boundary C11, the centered quadratic has
discriminant

```text
Delta(x)=(1-4x/3)^2-(59/48)x^2.
```

On its positive small-x branch the strict condition is exactly
`x<12/(16+sqrt(177))`. Equality loses the strict contraction supplied
by the smaller scalar root; it does not prove failure of the actual
vacuum. For C12 define

```text
F_x(Z)=(59/32)x^2+(4/3)xZ+Z^2/6,
Z_thr=(3/4)(1-x).
```

Direct expansion gives

```text
32[F_x(Z_thr)-Z_thr]=30x^2+50x-21.
```

Its positive zero is `(sqrt(1255)-25)/30`. Below that zero,
`Z_thr` lies strictly between the scalar roots, so the smaller root
admits a slightly larger contractive radius still satisfying `q<1`.
The comparison lies on the required branch: that zero is less than
`7/20`, while C11's threshold exceeds `2/5`; the influence threshold
also lies below the quadratic vertex throughout this region.
At equality C12 supplies no positive q margin, as the final text
correctly states. Neither estimate boundary is identified with an
actual closing of the physical gap.

For the two-square geometry, the quaternion Gram condition gives
exactly `D=1-a^2-b^2-c^2+2abc>=0`, and simultaneous SU(2)
conjugation supplies the full ordered-pair gauge quotient. Conditional
Haar axis integration gives constant density `2/pi^2`, with quotient
volume `pi^2/2`. The seven-link derivative calculation agrees with
every displayed metric entry. Its divergence is
`(-12a,-12b,-18c)`, which reproduces the drifts `(6a,6b,9c)`.
The normal identity `G grad D=-D(8a,8b,12c)` and determinant
factorization are consistent with that matrix; the quadratic form
inherits its domain from the gauge-invariant source manifold rather
than an independently chosen flat boundary condition. The free
physical gap 6, the nonzero second-order coefficient `c/351`, the
energy coefficient `-1/12`, and the stated exact polynomial-reference
residual all agree with the independently derived identities in this
audit and its obstruction note. Quotient completeness is not used as
a substitute for solving the vacuum equation.

After the portability link remap, SHA-256 was independently computed
from the four final files below and compared with
[SOURCE_PROVENANCE.json](SOURCE_PROVENANCE.json). All four agree.
For the two files changed by that remap, reversing only their recorded
Markdown link-target substitutions reproduced the exact pre-remap
hashes observed during the mathematical review. This independently
checks that their intervening changes were link-target changes only.

| Final reviewed file | SHA-256 |
|---|---|
| [COMBINED_RESULT.md](COMBINED_RESULT.md) | `7ad46c4e96b84bcada64875d07452738b059aa62a2778799b103b7b7feb9eb40` |
| [TWO_SQUARE_GEOMETRY.md](TWO_SQUARE_GEOMETRY.md) | `9d290bdad62f22c2d1101e5cf1a7ade92fdf27f6ad149437a15c32f6cf9399b8` |
| [GAUGE_NORM_GAIN.md](GAUGE_NORM_GAIN.md) | `0ae7da9697b5bb9ce798444fc7a9e8fc25b872d9bc00500b0f9e43652d264e94` |
| [LOCAL_VACUUM_ROUTE.md](LOCAL_VACUUM_ROUTE.md) | `6fc392e3f75716b289bcf39e9ee75f0a81bce47766090453531e33e9cd7405ba` |

The new source-binding check returned PASS. The hashes identify the
reviewed bytes; they do not establish the truth of their contents.
This final pass did not rerun an old checker or the root task's new
construction checker. The claims remain written finite-lattice proofs
with independent agent review and separately recorded exact controls,
subject to the scope and open limits stated above.
