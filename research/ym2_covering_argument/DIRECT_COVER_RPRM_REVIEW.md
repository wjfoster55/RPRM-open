# Independent review of the direct Fourier covering argument

12 September 2026. **Disposition: no blocking mathematical finding in
DC2–DC17 at the declared finite-graph, small-magnetic-coupling scope.**
The local Fourier multiplication estimate, weighted fixed-point estimate,
fixed-graph regularity passage, collective Hessian bound, and full spectral
landing survive this independent written audit. Two minor scope/notation
clarifications are listed below. This is a mathematical review of a written
proof, not a proof-assistant certificate or a probability of correctness.

Reviewed source:
`C:/github/RPRM-open/research/ym2_covering_argument/DIRECT_COVER_ATTEMPT.md`.
The initially retrieved candidate SHA-256 was
`aae45427b158c5bb4625a41014a767f4fd46b396071df46bae6e6cb863b8bdc7`
at `2026-09-12T19:43:10.5239230Z`. The candidate contains 416 lines in that
retrieval. The analytic review changed only this review file, made no
candidate edit, and ran no earlier checker or numerical spectrum calculation.

**Reviewed refresh:** the parent then clarified coefficient names,
normalization, the tree-only physical sector and form-domain transport, and
replaced the positivity-improvement dependency with direct ground-state
identification through the exact form identity. I reread the revised proof;
these changes are valid. Its SHA-256 is
`1e30640bb3c837938447b769942295f3f357453f06fe8b9b5a5de6546d788df0`
at `2026-09-12T19:49:37.8269258Z`, with 433 lines. The added link to
`CONDITIONAL_REFINEMENT.md` is a separate result; its derivation was not
part of this second review. The DC2–DC17 disposition remains unchanged.

## 1. Fourier coefficient space and multiplication

For the finite product group, irreducibles are the external tensor products
indexed by all multi-spins J. Matrix coefficient independence gives a unique
matrix B_J in the displayed convention `u_J=Tr(B_J pi_J)`. There is no
missing dimension factor once B_J is defined by this equality; switching to
the usual Fourier transform merely puts the dimension factor in B_J.

Put `W(u)=sum_(J!=0) lambda_J ||B_J||_1`. Every nonzero J has nonempty
support and `lambda_J>=3/2`. Therefore, for the nonempty finite edge set,

```text
||u||_* <= W(u)
        <= sum_e sum_(J containing e) lambda_J ||B_J||_1
        <= |E_G| ||u||_*,
sum_(J!=0)||B_J||_1 <= (2/3)W(u).
```

These inequalities justify both completeness and uniform reconstruction of
the continuous function. The volume factor appears only in a fixed finite
graph's norm-equivalence/topology argument. It does not enter DC5 or DC13.
The real mean-zero subspace is closed and is an admissible Banach space for
the real fixed-point problem.

I checked DC3 directly, independently of the general Fourier-algebra citation.
For a fixed pair J,K, let a unitary change of representation identify
`pi_J tensor pi_K` with `direct_sum_L(I_(m_L) tensor pi_L)`, and set
`D=U*(B_J tensor C_K)U` in that decomposition. Off-diagonal blocks make no
contribution to the represented function. Its L coefficient is precisely
`Tr_(multiplicity)(D_LL)`. Trace-norm pinching and partial trace give

```text
sum_L ||Tr_(multiplicity)(D_LL)||_1
 <= sum_L ||D_LL||_1
 <= ||D||_1
 = ||B_J||_1 ||C_K||_1.
```

Partial trace is contractive here even for a non-Hermitian complex matrix:
duality pairs it with `I tensor M`, whose operator norm equals `||M||`.
There is no multiplicity factor to insert. Pinching is contractive because
it is an average of unitary conjugations, and the trace norm of the resulting
block diagonal matrix is the sum of its block trace norms. Thus the argument
does not require positivity of the Fourier matrices.

If both inputs are trivial at an edge, their tensor product is trivial there.
Every reached output support is consequently contained in the union of the
two input supports. Shrinking support or a scalar output is permitted. This
is the exact support statement needed later; equality of supports is neither
assumed nor needed. Absolute convergence and finite Fourier-sum approximation
extend the finite block argument to the stated coefficient space.

The general Banach-algebra background is also consistent with Eymard's
original construction, especially chapter 3, proposition 3.4 and definition
3.5. The proof above supplies the particular matrix estimate required here.
[Eymard, original paper](https://www.numdam.org/article/BSMF_1964__92__181_0.pdf).

## 2. The anchored bilinear estimate really is independent of volume

For every nonzero half-integer j,

```text
2j/[2j(j+1)] = 1/(j+1) <= 2/3.
```

Each unit generator derivative therefore has Fourier norm at most
`2j_i b_J`, with zero contribution when edge i is absent. A product of
derivatives is supported only on pairs sharing the differentiated edge i.

For an anchored output edge e, the output energy weight cancels the inverse
kinetic multiplier for every nonzero output L. Projecting out L=0 does not
increase the sum. Bounding the output indicator by
`1_(e in J)+1_(e in K)` gives two terms. One is bounded by

```text
sum_(J containing e) b_J sum_i 3(2j_i(J))
                     sum_(K containing i)(2j_i(K)) c_K
 <= (2/3)||v||_* sum_(J containing e)b_J sum_i 3(2j_i(J))
 <= (4/3)||v||_* sum_(J containing e)lambda_J b_J
 <= (4/3)||u||_*||v||_*.
```

The second term reverses u,v and gives the same bound. DC5's constant
`8/3` is correct. In particular, no sum over every edge was replaced by
an unproved fixed constant: it was absorbed into the input energy
`lambda_J=sum_i lambda_(i,J)`. This is the main coverage-sensitive step.

All sums used for these bounds are nonnegative majorants, so regrouping is
legitimate. For fixed G, the derivative series are absolutely convergent in
the Fourier algebra, their finite sum of products is well defined, and
`T^-1 Q` maps its nonconstant Fourier components to the claimed output.

## 3. Plaquette input and fixed-point constants

A four-link half trace has 16 matrix-entry products, each with coefficient
1/2. Each entry is a rank-one coefficient of norm one. An inverse entry
uses the unitary dual representation, so it has the same norm; equivalence
of the SU(2) dual to the fundamental representation introduces no norm loss.
The four link occurrences are distinct, making each product an external
tensor coefficient with trace norm one. Thus the conservative bound 8 in
DC6 is valid. Every term is in the four-fundamental isotypic component and
has `lambda_J=4*(3/2)=6`.

It follows that `||T^-1 S||_*<=8m`, where m bounds the number of elementary
plaquette occurrences through each edge. Coefficient collisions can only
improve this triangle bound. The dependence on incidence, rather than on
total plaquette count, is proved for the actual source S.

For `R=1/4` and `r<=1/(48m)`,

```text
8mr+(4/3)R² <= 1/6+1/12=1/4,
(1/2)*(8/3)*(||u||_*+||v||_*) <= (8/3)R=2/3.
```

The map preserves the closed ball and is strictly contractive, including
the stated closed coupling endpoint. The majorant root in DC10 solves
`R=8mr+(4/3)R²`, with discriminant `1-128mr/3`; its strict interval and
contraction multiplier are correct. Picard iteration from zero selects
a real gauge-invariant fixed point. This is a convergent mathematical
construction, without a claim that its coefficient work or storage has
uniform finite computational cost.

## 4. C² convergence and identification of the actual vacuum

For fixed G, `W(u)<infinity` controls every first and second derivative in
the global left-invariant frame. For two edge directions, products of
generator norms are bounded by a constant times lambda_J; in one edge,
`(2j)^2<=2 lambda_(e,J)`, and distinct-edge products satisfy the corresponding
Cauchy--Schwarz bound. The Weierstrass majorant test therefore gives uniform
convergence of the derivative series through order two. Uniform convergence
of these derivatives of finite smooth Fourier sums proves `u in C²`, not
merely a formal derivative identity.

Applying T to the fixed point is justified by this convergence. Haar mean
zero of every a_p and removal of the scalar output give exactly

```text
T u = rS+(1/2)|grad u|²-(1/2)integral|grad u|² dmu.
```

The sign and scalar vacuum energy are correct. Since u is C², its gradient
square is C¹. On each fixed compact graph manifold this is locally Lipschitz,
hence Holder; elliptic Schauder regularity first gives C^(2,alpha), and then
bootstraps the semilinear equation to smoothness. No graph-independent
Schauder constant is used to establish the eventual spectral constant.

The exponential `exp(u)` is a smooth strictly positive eigenfunction of
the actual operator T-rS. The initial draft identified it with the ground
state using the accepted positivity-improving compact-source Schrodinger
result. The refreshed proof instead uses the exact form identity directly:
positive smooth `psi_hat` and its reciprocal map the entire H¹ form domain
onto itself, and `A-E` becomes one half of the nonnegative weighted gradient
form. Its zero space is exactly `psi_hat` times constants on the connected
product manifold. Thus E is the bottom eigenvalue and is simple without
that extra positivity-improvement dependency. This is valid. Uniqueness of
the small Banach-ball fixed point alone would not identify every possible
vacuum; the full form argument supplies that missing identification and
makes it unnecessary to prove that an independently unknown ground state's
logarithm belonged to the selected Banach ball.

## 5. Collective Hessian control and full spectral coverage

The diagonal Hessian computation is sound. Any tangent vector at a point
extends to a constant left-invariant field V; the bi-invariant product metric
gives `nabla_V V=0`. Thus `Hess u(v,v)=V²u` at that point. This avoids the
incorrect entrywise identification of noncommuting second derivatives with
a symmetric Hessian.

The spin-J generator along v has norm at most
`sum_e 2j_e|v_e|`. Weighted Cauchy--Schwarz gives

```text
(sum_e 2j_e|v_e|)²
 <= 2 lambda_J sum_(e in supp J)|v_e|².
```

Summing the trace-norm majorants therefore gives
`|Hess u(v,v)|<=2||u||_*|v|²`, including tangent vectors spread over all
links. No independent-plaquette or finite-support restriction is imposed
on those vectors. With `||u||_*<=1/4`, the weighted Ricci tensor is at least
`[2-4||u||_*]g>=g`; the unit-sphere/product-metric factors are consistent
with the source Casimir convention.

For the weight `exp(2u)`, the sign is correct: the weighted Laplacian is
`L=Delta+2 grad u dot grad` and weighted Ricci is `Ric-2 Hess u`.
The weighted Bochner identity and its eigenfunction integration agree with
the primary derivation in Wei and Wylie's sections 2–3, especially equation
2.5. [Wei–Wylie, comparison geometry](https://www.math.uchicago.edu/~shmuel/QuantCourse%20/Metric%20Space/comparison%20geo%20for%20smooth%20mm%20spaces.pdf).

Compactness and smooth strict positivity give the full weighted eigenbasis,
kernel consisting of constants, and closed form domain. The bound on each
nonzero eigenvalue passes to arbitrary form-domain functions by spectral
expansion and closure. The ground-state transform then covers every actual
normalized vacuum-orthogonal quantum state, including arbitrarily high
spins. This is the complete spectral coverage step. The fixed-point ansatz
restricts how the vacuum is constructed; it does not restrict the excitation
receiver to that ansatz.

Gauge symmetry fixes the unique positive normalized ground state. Restricting
the full form inequality to invariants is a valid one-sided exclusion
adapter. It does not require the invariant subspace itself to be a tensor
product or a globally regular coordinate chart.

## 6. Nonblocking clarifications, resolved in the reviewed refresh

1. In DC14, label the multiplying wavefunction explicitly as the normalized
   `psi_0=exp(u)/||exp(u)||_2`. The text already says the transform uses the
   normalized wavefunction, and DC17 explicitly uses it. If the displayed
   form identity were read with the earlier unnormalized `psi=exp(u)`, its
   right side would instead carry `||exp(u)||_2²`. This is a notation
   clarification, not a change to the bound.
2. A finite tree with full gauge invariance at every vertex has only the
   constant physical sector. On such a graph, the restricted form inequality
   is valid but there is no physical first excited eigenvalue E1. Either
   state the physical conclusion as spectral exclusion/the form inequality,
   adopt the `inf empty=+infinity` gap convention, or restrict a finite
   physical-gap claim to graphs with a nonconstant physical sector. The full
   edge-space gap is nonvacuous for every graph with at least one link.

Neither point invalidates the all-state form bound for the intended
nontrivial lattice gauge sectors. Both are now explicitly resolved in the
433-line source bound above; they are retained here as the review history,
not outstanding corrections.

## 7. RPRM coverage and evidence disposition

The proof meets the source/receiver distinction in the official
`docs/proof-donut.md` and Manifesto II.5.2 in a substantive way. It supplies
the missing local-to-whole inequality instead of borrowing coverage from
a count of successful examples. Its complete source is the full finite
product group; its all-spin Fourier sums construct the actual vacuum;
its collective Hessian estimate and complete spectral basis cover the
whole excitation form domain. The operator, measure, derivative metric,
vacuum energy, gauge inclusion and physical energy multiplier are retained.

The all-volume statement has the correct quantifiers: for every finite
admitted G, there is a smooth ground state u_G obeying the same local norm
bound, and every such graph has the same gap lower bound at the stated r.
This does not assert a common infinite-volume Hilbert space or interchange
an infinite-volume limit with the Fourier/elliptic arguments. Fixed-graph
regularity and normalization may have volume-dependent constants without
weakening the proved uniform Hessian and spectral constants.

The resulting reviewed written claim is `gap(A(r))>=1/2` for
`0<=r<=1/[48*2(d-1)]`, with the physical form restriction and original
energy multiplier as stated. It excludes all arbitrarily cheap collective
excitations within that finite-graph family and coupling interval. The
weak-bare-coupling continuum direction, physical-scale uniformity and
continuum theory construction remain outside it. Failure of the sufficient
small-r estimate elsewhere would be OPEN, not evidence of actual gaplessness.

No finite computation can establish the unrestricted trace-norm,
fixed-point, elliptic, Bochner or spectral-closure assertions audited here.
Their evidence grade is written proof plus this independent written review,
with standard analytic dependencies identified. The earlier Fourier-free,
two-square and conditional-head receipts retain their separate grades and
were not rerun or promoted by this review. The source hash binds bytes only.
