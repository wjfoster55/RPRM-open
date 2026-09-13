# Gauge admissibility improves the vacuum construction norm

12 September 2026. New written proof; no old file, old checker, installation,
simulation, campaign, or git operation is used.

**Result.** Section 8 proves the strengthened constant `1/3`, improving
the unrestricted-space constant `16/9` by a factor `16/3`. It also proves
the local fundamental contracted constant `3/2`. The simpler independent
support argument in sections 2--7 first gives the following weaker bound,
which is preserved to make the two sources of improvement explicit.
On the gauge-invariant subspace of the accepted Fourier space,

```text
||B(u,v)||_* <= (4/9)||u||_*||v||_*,
B(u,v)=T^-1 Q sum_(i,k)(D_(i,k)u)(D_(i,k)v).              (GN1)
```

This improves the unrestricted-space constant `16/9` by a factor four.
It retains the same norm and the same actual-vacuum equation. In particular,
with the exact source bound `||T^-1 S||_*<=4m`, it constructs the smooth
positive actual vacuum for

```text
|r| < 9/(32m),
||u||_* <= (9/4)[1-sqrt(1-32m|r|/9)].                   (GN2)
```

The inherited curvature argument gives `gap>=1/2` on the closed interval
`|r|<=17/(288m)`, and a positive lower bound whenever `|r|<1/(9m)`.
These latter bounds hold for the full excited complement as well as its
physical restriction. The improvement in constructing `u` uses gauge
invariance; the subsequent curvature estimate is a pointwise inequality
on the full source manifold. The constants are sufficient, with no
optimality claim.

## 1. Contract and exact dependencies

- **Carrier and equality:** a finite open square or cubic lattice graph,
  distinct edges and plaquettes, full vertex gauge invariance including
  boundary vertices, `SU(2)^(E_G)` with product normalized Haar measure,
  all half-integral spins, and almost-everywhere equality. There are no
  external charges. The graph is simple and triangle-free.
- **Supplied ports:** the accepted generator convention `i sigma_k`,
  `lambda_j=2j(j+1)`, `lambda_J=sum_i lambda_(j_i)`, coefficients
  `u_J=Tr(B_J pi_J)`, `b_J=||B_J||_1`, and
  `||u||_*=max_e sum_(J:e in supp J) lambda_J b_J`.
- **Operation:** the bilinear map in GN1, on the closed mean-zero
  gauge-invariant subspace `X_G^inv` of the original `X_G`.
- **Receiver:** the same norm, convergence of the actual log vacuum,
  and the inherited all-state weighted Bochner bound. No interacting
  spectral enumeration is requested or supplied.
- **Inverse and fiber:** `T^-1` divides every nonzero block by
  `lambda_J`; `Q` removes the scalar block before inversion. The
  interacting spectral fiber and any stronger optimal norm remain OPEN.
- **Coverage and evidence:** the estimates below cover every admitted
  spin, coefficient matrix, and finite graph in the stated class by
  written inequalities. They are written proofs, not a formal certificate
  or evidence about a continuum limit.

The inherited function-space, regularity, positive-ground-state, and
Bochner arguments are [DIRECT_COVER_ATTEMPT.md](accepted/research/ym2_overlap_cover/accepted/estimate/accepted/DIRECT_COVER_ATTEMPT.md),
especially DC2 and DC8--DC17. The exceptional fundamental-pair estimate
is SC9 in [SIGNED_AND_CONTRACTED_AUDIT.md](accepted/research/ym2_overlap_cover/accepted/estimate/SIGNED_AND_CONTRACTED_AUDIT.md).
The source coefficient is SN4 in
[SOURCE_NORM_REFINEMENT.md](accepted/research/ym2_overlap_cover/accepted/estimate/SOURCE_NORM_REFINEMENT.md).
Those files remain unchanged.

## 2. Why a nonzero invariant Fourier block obeys vertex constraints

Gauge transformations act by left and right translations on individual
link variables. Each link's Peter--Weyl isotypic projection commutes with
both translations. Consequently every `u_J` of a gauge-invariant function
is itself gauge invariant.

Vectorize the matrix `B_J` and reorder its representation and dual factors
by their incident vertices. The gauge action then acts separately at each
vertex on the tensor product of its incident spin spaces, with duals as
determined by the edge orientations. A nonzero invariant coefficient
requires a nonzero invariant tensor at every vertex. This does not say
that an arbitrary singular vector of `B_J` is gauge invariant, and the
proof below never imposes that false extra condition.

For any incident edge carrying spin `l`, an invariant tensor requires

```text
l <= sum_(other edges f at that vertex) j_f.              (GN3)
```

Indeed the tensor product of all the other spin factors must contain
spin `l` in order to couple it to the trivial representation. Repeated
SU(2) spin addition bounds every reached spin by the sum of its input
spins. SU(2) duals have the same spin. This proves the necessary condition
GN3 directly from the same spin-addition rule used in SC3.

Only this necessary condition is used. It need not characterize the full
invariant tensor space, its parity restrictions, or its multiplicities.

## 3. A link forces a lower bound on the total physical Casimir

Fix a nonzero admissible block `K` and an occupied edge `i={v,w}` carrying
spin `l>0`. Let `A` be the other edges incident to `v` or `w`. GN3 at these
two endpoints gives

```text
sum_(f in A) j_f >= 2l.                                 (GN4)
```

Let `Z` be the outer endpoints of the edges in `A`. Include zero-spin
edges in this notation if desired; they contribute zero. Since the graph
is simple and triangle-free, every vertex in `Z` is distinct from `v,w`
and is the outer endpoint of exactly one edge in `A`. Apply GN3 there to
that one incident edge. All of its other incident edges lie outside
`A union {i}`. Summing over `Z` counts each such other edge at most twice,
so, writing `C=E_G minus (A union {i})`,

```text
sum_(f in A) j_f <= 2 sum_(f in C) j_f,
sum_(f != i) j_f >= (3/2) sum_(f in A) j_f >= 3l.         (GN5)
```

The possible overlaps between the outer endpoint neighborhoods are
precisely why the factor two is present; they have not been treated as
independent edges. For every half-integral `s>=0`,
`lambda_s=2s(s+1)>=3s`. Keep the chosen edge's exact Casimir and apply this
inequality to all other edges. The result is

```text
lambda_K >= lambda_l+9l = l(2l+11).                     (GN6)
```

In particular every nonzero invariant block satisfies `lambda_K>=6`.
This statement is stronger than merely observing that a nonempty
gauge-invariant support contains a cycle. A physical support can also
contain bridges, so the proof does not assume that each occupied edge
belongs to a simple cycle.

Two exact controls show that GN6 is substantive and correctly normalized.
The fundamental Wilson loop on one square has four spins `1/2`, total
Casimir `6`, and equality in GN6. Two adjacent squares give a seven-edge
theta graph. Assign spin `1` to their common edge and spin `1/2` to the
six outer edges. The two trivalent endpoints admit the `1,1/2,1/2`
invariant, and each remaining vertex admits the `1/2,1/2` invariant.
Thus this is a nonzero admissible spin-network block, with total Casimir
`4+6(3/2)=13`, again equality in GN6 for the chosen spin-one edge.

## 4. One anchor side costs at most 2/9

Write `j=j_(i,J)>0`, `l=j_(i,K)>0`, and
`Gamma_i(u_J,v_K)=sum_k(D_(i,k)u_J)(D_(i,k)v_K)`.
The accepted contracted spin-channel calculation gives

```text
||Gamma_i(u_J,v_K)||_A <= 4a(b+1)b_J d_K,
a=min(j,l), b=max(j,l), d_K=||C_K||_1.                  (GN7)
```

It follows by multiplicity-free irreducible pinching and the operator
norm of the contracted generator. It is valid for arbitrary coefficient
matrices. For `j=l=1/2`, the stronger accepted bound is

```text
||Gamma_i(u_J,v_K)||_A <= 2 b_J d_K.                     (GN8)
```

It uses the separate singular-value decompositions of `B_J,C_K`, with
product vectors between the two input sides. We import GN8 at exactly
that proved carrier, without strengthening its assumptions.

We claim the asymmetric estimate

```text
||Gamma_i(u_J,v_K)||_A
  <= (2/9)lambda_(i,J) lambda_K b_J d_K                 (GN9)
```

whenever the `K` block is physically admissible. All spins are covered:

1. If `j=l=1/2`, GN8 and GN6 give
   `(2/9)lambda_j lambda_K >= (2/9)(3/2)6=2`.
2. If `l=1/2` and `j>=1`, GN7 divided by `lambda_j` gives
   `2(j+1)/[2j(j+1)]=1/j<=1`. Meanwhile
   `(2/9)lambda_K>=4/3`, so GN9 follows.
3. If `l>=1`, GN7 divided by `lambda_j` is
   `2(l+1)/(j+1)` when `j<=l`, and `2l/j` when `j>=l`.
   In either case it is at most `(4/3)(l+1)`.
   GN6 gives `lambda_K>=6(l+1)`, since

   ```text
   l(2l+11)-6(l+1)=2l^2+5l-6 >= 1  for l>=1.
   ```

   Therefore `(4/3)(l+1)<=(2/9)lambda_K`, as required.

If either differentiated spin is zero, the left side vanishes. There is
no spin cutoff or finite enumeration in this proof.

## 5. Anchored summation, gauge closure, and the full bilinear estimate

Every output support lies in `supp J union supp K`. The output energy
weight cancels exactly against `T^-1`. For a fixed anchor `e`, retain the
safe bound

```text
1_(e in supp L) <= 1_(e in supp J)+1_(e in supp K).
```

For the first anchor side, GN9 gives

```text
(2/9) sum_(J:e in supp J) b_J sum_i lambda_(i,J)
                  sum_(K:i in supp K) lambda_K d_K
 <= (2/9)||v||_* sum_(J:e in supp J) lambda_J b_J
 <= (2/9)||u||_*||v||_*.
```

For the second anchor side exchange `J,K` and use physical admissibility
of `J`. Adding the two sides proves GN1 for finite invariant Fourier
sums. The two-input-anchor overcount is still present. The improvement
comes from retaining the whole physical input energy in each anchored
sum, using GN6, instead of discarding that constraint.

The mean-zero invariant subspace is closed in `X_G`. Finite truncation by
whole isotypic blocks preserves gauge invariance and converges in its
norm. The link metrics are bi-invariant, so vertex gauge transformations
are isometries preserving each contracted link gradient pairing.
Consequently `Gamma_i`, their sum, `Q`, and `T^-1` preserve gauge
invariance. The finite-sum bilinear estimate therefore extends to
`X_G^inv` with the stated constant, and the accepted absolutely convergent
derivative expansions identify its extension with GN1.

## 6. Actual-vacuum and gap consequences

Set `t=|r|`. The real gauge-invariant fixed-point map

```text
F_r(u)=rT^-1 S+(1/2)B(u,u)
```

has, on a radius-`R` ball in `X_G^inv`, the estimates

```text
||F_r(u)||_* <= 4mt+(2/9)R^2,
Lip(F_r) <= (4/9)R.                                    (GN10)
```

The smaller solution of `R=4mt+(2/9)R^2` is GN2. Its contraction factor
is `1-sqrt(1-32mt/9)<1` when `t<9/(32m)`. Iteration from zero therefore
converges, and the inherited fixed-graph regularity argument makes `u`
smooth. The function `psi=exp(u)`, normalized in Haar `L^2`, is the
strictly positive actual ground state of `A(r)=T-rS`, with its actual
energy subtracted in the ground-state transform. These conclusions do
not require the curvature lower bound to be positive.

Using the accepted pointwise Hessian estimate on this constructed `u`
then gives

```text
gap(A(r)) >= 1-2R(t)
 = 1-(9/2)[1-sqrt(1-32mt/9)]                            (GN11)
```

whenever the displayed right side is positive. This holds exactly on
`t<1/(9m)`. The bound applies to every vector orthogonal to the actual
ground state in the full form domain, with the inherited physical-sector
qualification if its excited complement is empty.

For the convenient fixed radius `R=1/4`, GN10 has contraction factor
`1/9`. The invariant-ball condition is

```text
4mt <= 1/4-(2/9)(1/16)=17/72,
t <= 17/(288m)  ==>  gap(A(r))>=1/2.                    (GN12)
```

The previous exact-source, unrestricted-bilinear interval was
`t<=7/(144m)=14/(288m)`. GN12 enlarges it by `17/14`. Both signs of real
`r` are included. At `t=1/(9m)`, the constructed radius is `1/2` and the
contraction factor remains `2/9`; only the stated curvature certificate
reaches zero there. No vanishing of the actual gap is inferred.

## 7. Inverse norm, hostile boundaries, and remaining room

GN6 also gives the sharp physical inverse bound

```text
||T^-1 f||_* <= (1/6)||f||_*   for f in X_G^inv.          (GN13)
```

The fundamental square block attains equality. However, one cannot
multiply GN1 by an additional `1/6` using GN13: in the bilinear proof the
output `lambda_L` has already canceled its inverse, and the controlled
gradient norm is the unweighted anchored coefficient norm. Such a second
factor would require a different proved bound on the gradient in the
energy-weighted norm.

The support hypothesis matters. If arbitrary one-link coefficients are
allowed, their nonzero total Casimir can be `3/2`; GN6 and the physical
inverse constant fail. If triangular cycles are admitted instead, the
fundamental triangle has Casimir `9/2`, which also refutes the unchanged
`1/6` inverse claim and the outer-neighborhood step GN5. Boundary charges
or omitted vertex gauge constraints invalidate GN3 at those vertices.

This note does not claim that `4/9` is optimal. The local fundamental
bound `2` can be attained by unrestricted one-link coefficient functions,
but that hostile example is not a physical gauge-invariant input. No
simultaneous physical saturation of the local estimate and both anchor
sides is asserted. Exact anchor accounting, correlations imposed by
physical coefficient tensors, and source-specific higher-order bounds
can therefore still improve this result. Their optimal constants remain
OPEN. Nothing here resolves an infinite-volume or continuum obligation.

Verification performed: written all-spin case split, explicit graph
incidence counting with overlaps retained, exact equality cases for GN6,
and algebraic substitution in the fixed-point and gap inequalities.
No old test suite or computational campaign was run.

## 8. Gauge-averaged coefficient marginals improve 4/9 to 1/3

There is a second gain beyond the support constraints. It comes from
positive matrices associated with the whole Fourier coefficient, and
does not require its individual singular vectors to be invariant.

Orient the graph and let

```text
L_J(g)=tensor_e pi_(j_e)(g_(source e)),
R_J(g)=tensor_e pi_(j_e)(g_(target e)).
```

The gauge action on the representation matrix is
`pi_J(U^g)=L_J(g) pi_J(U) R_J(g)^*`. Invariance of
`Tr(B_J pi_J(U))` and uniqueness of its coefficient matrix imply

```text
R_J(g) B_J = B_J L_J(g).                                (GN14)
```

It follows that `B_J^*B_J` commutes with `L_J(g)` and `B_J B_J^*`
commutes with `R_J(g)`. Functional calculus gives the same statements
for `|B_J|=sqrt(B_J^*B_J)` and
`|B_J^*|=sqrt(B_J B_J^*)`. Trace out all links except an occupied link
`i`. A gauge transformation at its source acts in `L_J` on that link
and possibly other traced-out links; invariance of partial trace shows
that the reduced matrix of `|B_J|` commutes with every `pi_j(h)`.
The target vertex supplies the same conclusion for `|B_J^*|` using
`R_J`. Irreducibility and the trace `b_J` therefore give

```text
Tr_(other links)|B_J| = b_J I_(2j+1)/(2j+1),
Tr_(other links)|B_J^*| = b_J I_(2j+1)/(2j+1).            (GN15)
```

The argument is unaffected by correlations among links and works for
arbitrary complex invariant coefficients. Vanishing coefficients can
simply be omitted.

For a fixed link write `Omega=sum_k A_(j,k) tensor A_(l,k)` and
`d_j=2j+1`. The rank-one Cauchy--Schwarz estimate SC6, followed by
Cauchy--Schwarz over the separate singular-value expansions of `B_J,C_K`,
gives

```text
||Gamma_i(u_J,v_K)||_A
 <= {Tr[(|B_J^*| tensor |C_K^*|)|Omega|]
      Tr[(|B_J| tensor |C_K|)|Omega|]}^(1/2).
```

Here `|Omega|` acts on the two selected link factors and as identity
elsewhere. To see the second Cauchy--Schwarz step explicitly, for
singular-value weights `s_a,t_b` and the rank-one expectations `p_ab,q_ab`
from SC6, it is
`sum_(a,b) s_a t_b sqrt(p_ab q_ab)
 <= sqrt[(sum s_a t_b p_ab)(sum s_a t_b q_ab)]`.
The two sums are exactly the displayed positive-matrix traces.
GN15 now evaluates both traces, yielding the uniform local estimate

```text
||Gamma_i(u_J,v_K)||_A <= c(j,l)b_J d_K,
c(j,l) = Tr|Omega|/(d_j d_l).                            (GN16)
```

For two fundamental spins, the singlet eigenvalue is `3` with dimension
one and the triplet eigenvalue is `-1` with dimension three. Hence

```text
c(1/2,1/2)=(3+3)/4=3/2.                                (GN17)
```

For all spins, normalized trace Cauchy--Schwarz bounds
`c(j,l)^2<=Tr(Omega^2)/(d_j d_l)`. Rotational invariance and the Casimir
identity give

```text
Tr(A_(j,k) A_(j,h))/d_j = -(2/3)lambda_j delta_(k,h),
Tr(Omega^2)/(d_j d_l) = (4/3)lambda_j lambda_l,
c(j,l) <= sqrt[(4/3)lambda_j lambda_l].                 (GN18)
```

The first identity follows because the trace pairing is rotationally
invariant and its sum over `k=h` is `-2lambda_j`. Thus this all-spin
step is derived from the declared generator normalization.

Combining GN6 with GN17--GN18 proves the improved asymmetric bound

```text
||Gamma_i(u_J,v_K)||_A
 <= (1/6)lambda_(i,J) lambda_K b_J d_K.                  (GN19)
```

The exhaustive cases are:

1. `j=l=1/2`: the right-side coefficient is at least
   `(1/6)(3/2)6=3/2`, exactly GN17.
2. `l=1/2,j>=1`: GN18 gives `c<=sqrt(2lambda_j)<=lambda_j`,
   since `lambda_j>=4`. GN6 gives `lambda_K>=6`.
3. `l>=1,j>=1/2`: GN6 gives

   ```text
   lambda_K^2/lambda_l
    >= [l/(2(l+1))](2l+11)^2 >= 169/4 > 32.
   ```

   Here `l/(l+1)>=1/2` and `2l+11>=13`.
   Together with `lambda_j>=3/2`, this implies
   `lambda_j lambda_K^2>=48lambda_l`, precisely the squared
   inequality `sqrt[(4/3)lambda_j lambda_l]
   <=lambda_j lambda_K/6`.

Zero differentiated spins again give zero. Repeating the unchanged
two-anchor summation in section 5 with `1/6` in place of `2/9` proves

```text
||B(u,v)||_* <= (1/3)||u||_*||v||_*  on X_G^inv.          (GN20)
```

Its scalar actual-vacuum bounds, with the exact source `4m`, are

```text
||F_r(u)||_* <= 4mt+R^2/6,       Lip(F_r)<=R/3,
R(t)=3[1-sqrt(1-8mt/3)],         0<=t<3/(8m).            (GN21)
```

The same positive-ground-state construction therefore works on this
larger interval. The inherited full-manifold curvature inequality gives
`gap>=1-2R(t)>0` when `t<11/(96m)`. At radius `R=1/4` the contraction
factor is `1/12`, and

```text
t <= 23/(384m)  ==>  gap(A(r))>=1/2.                    (GN22)
```

Indeed `1/4-(1/4)^2/6=23/96`, while
`1/2-(1/2)^2/6=11/24`. Divide these source budgets by `4m`.
These are scalar sufficient intervals; source-specific recentering can
use GN20 and GN17 and need not stop at the zero-centered majorant.

GN20 supersedes GN1 as the best uniform bilinear constant proved in this
note. All the earlier conclusions remain valid. The earlier single-link
unrestricted hostile example does not contradict GN17: its coefficient
matrices do not satisfy GN14--GN15. Optimality of GN20 is still OPEN.
