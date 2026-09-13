# Overlapping conditional blocks with the energy counted once

12 September 2026. New written derivation; publication remains on hold.

The overlap idea gives a concrete improvement on the existing physical gap
certificate. On an open cubic graph, use three blocks: all links in the
`xy`, `xz`, and `yz` directions. Each actual link occurs in two blocks.
Assign weight `1/2` to each block. The weighted derivative energies then
count every link exactly once. Each omitted direction is a forest, and
gauge invariance makes each block's conditional residual detect the entire
physical variance. The resulting lower bound is `3/2` times the previous
conditional physical bound, on the same proved coupling interval.

This conclusion uses an actual shared-variable cover and its conditional
laws. The half is a positive counting weight. No negative probability,
independent duplicate link, new physical region, or deformation of the
Hamiltonian is introduced.

## 1. Contract, supplied results, and the new port

Retain the finite connected nearest-neighbor subgraph `G` of `Z^d`,
`d=2` or `3`, its positively oriented links `E`, distinct retained square
plaquettes, configuration space `Q=SU(2)^E`, product Haar probability
`mu`, unit-round-`S^3` metric, and gauge transformations at every vertex.
All spins are admitted. The operator and energy units remain

```text
H/E_el = T+r sum_p(1-a_p),       T=-Delta/2,
E_el=alpha hbar^2>0,            r=beta/E_el>=0,
m=2(d-1).
```

The actual normalized positive invariant vacuum is `psi_0`, and
`dnu=psi_0^2 dmu`. Equality is equality in `L^2(nu)`. Let `H_phys` be the
closed gauge-invariant subspace, and let `H_phys,0` be its centered part.
An excited-gap statement assumes this latter space is nonzero; on a tree
with gauge constraints at every vertex the physical excited complement is
absent and the form inequality is vacuous.

The accepted inputs are the actual-vacuum construction and the
single-link influence, tilt, and form identities in
[RESULT.md](accepted/estimate/RESULT.md) and
[CONDITIONAL_GAP_EXTENSION.md](accepted/estimate/CONDITIONAL_GAP_EXTENSION.md).
Their existing proof and tests are reused at their stated scope. The
weighted residual formulation below extends the already identified
operator in
[DIFFERENCE_PROJECTION.md](accepted/DIFFERENCE_PROJECTION.md),
sections 1–2. The weighted comparison itself is an elementary extension
of that glue inequality, not a newly named solution to its mixing port.
The additional result is the forest-complement identity, together with
a uniform conditional block estimate and the direction cover.

The receiver is a lower bound on the original physical excitation energy,
on the entire physical form domain. Conditional refresh is an auxiliary
operation used in its proof. The residual map's missing source is retained
as a joint Hilbert-space fiber; this task does not enumerate interacting
eigenfunctions or return a complete spectral `ONE`/`MANY` answer.

## 2. Weighted block theorem and exact overlap normalization

Supply finitely many block occurrences `B subset E` and weights `w_B>0`.
An edge shared by two blocks is the same original coordinate in both.
Repeated block occurrences retain their weights and identities. Define

```text
P_B f = E_nu[f | U_(E\B)],       R_B=I-P_B,
v_B(f)=||R_B f||_2^2,
D_w f=(sqrt(w_B) R_B f)_B,
A_w=sum_B w_B R_B = D_w* D_w,
delta_w=inf_(0 != f in H_phys,0) <f,A_w f>/||f||_2^2.       (O1)
```

Conditional expectations are orthogonal projections. They commute with
the full vertex gauge action: every fixed gauge transformation preserves
`nu` and maps the outside-link sigma algebra onto itself. Consequently
`P_B`, `R_B`, and `A_w` reduce `H_phys,0`. Their sharp physical variance
constant is `1/delta_w`, with infinity when `delta_w=0`.

Suppose the following conditional derivative estimates are supplied,
uniformly in the exterior, with nonnegative coefficients `c_(B,e)`:

```text
Var_(nu_B(.|outside))(g)
 <= sum_(e in B) c_(B,e)
       integral |grad_e g|^2 dnu_B(.|outside).             (O2)
```

It suffices to prove these for smooth functions and extend by form
closure. They may be stronger estimates specifically for admissible
physical restrictions, provided that restriction is proved. Put

```text
k_e=sum_(B:e in B) w_B c_(B,e),       M_w=max_e k_e.
```

For centered physical functions, integration of (O2) gives the complete
chain

```text
delta_w Var_nu(f)
 <= sum_B w_B v_B(f)
 <= sum_e k_e integral |grad_e f|^2 dnu
 <= M_w integral |grad f|^2 dnu.                           (O3)
```

Thus, for `delta_w>0` and `M_w>0`, the original ground-state form identity
implies

```text
gap_phys(H)/E_el >= delta_w/(2 M_w).                       (O4)
```

The energy collection `k_e` is exact. Replacing it by its maximum is an
explicit comparison and need not be sharp for the physical subspace.
The infimum defining `delta_w` is sharp for the residual form; (O4) need
not be the sharp quantum gap.

For a common block constant `c_(B,e)=C_0`, the denominator is
`2 C_0 max_e sum_(B:e in B) w_B`. Uniformly multiplying all weights
multiplies both numerator and denominator by the same number. Replacing
one block of weight `w` by two identical occurrences of weights `w/2`
leaves every operator and energy count unchanged. Keeping weight `w` on
both doubles that block's variance contribution and its energy charge.
Duplicating all blocks therefore gives no gain in (O4).

More generally, a proposed new cover improves this certificate exactly
when its proved ratio `delta_w/M_w` improves. A larger unnormalized sum
of residuals alone does not establish that comparison. Signed
inclusion–exclusion of derivative energies also does not license
subtracting already proved upper bounds on variances.

When `delta_w>0`, the inverse on the reached centered residual range is
`f=A_w^-1 D_w* D_w f`. Without centering the reached source fiber is
`f+ker D_w`; constants always lie in that kernel. These are the same
inverse/fiber distinctions as the prior residual theorem.

## 3. A uniform conditional estimate for every block

Suppose the accepted actual-vacuum port supplies

```text
psi_0=exp(u)/||exp(u)||_2,        ||u||_*<=Y<3/4.
```

For the full actual one-link conditionals, the accepted estimates give

```text
q=max_i sum_(j != i) c_ij <= 4Y/3 <1,
D_i=osc log(dnu_i/dmu_i) <= 8Y/3.                         (O5)
```

Here `c_ij` measures the total-variation change of the conditional law
at `i` when only outside coordinate `j` changes. Fix *any* block `B` and
*any* exterior configuration `z`. Its conditional law `nu_B(.|z)` is
a smooth positive measure on the compact product `SU(2)^B`.

Conditioning again on all coordinates of `B` except `i` gives precisely
the original one-link conditional law at `i`, with `z` held fixed.
Therefore its internal influence coefficients obey

```text
c_ij^(B,z) <= c_ij,   i,j in B,
max_(i in B) sum_(j in B) c_ij^(B,z) <= q.                (O6)
```

Its one-link log-density oscillation is still at most `8Y/3`. There is
no factor `|B|` in either estimate. One does not compare the entire
block density with product Haar by its total oscillation.

For completeness, apply the accepted continuous-state argument on this
fixed compact block. The single-site conditional projections have
bounded reversible generator `sum_(i in B)(P_i^(B,z)-I)`. The vector of
coordinate oscillations contracts under its semigroup with matrix
`exp[t((C^(B,z))^T-I)]`; its `l^1` norm decays at least as
`exp[-(1-q)t]`. The same self-adjoint spectral-measure argument, on the
dense centered continuous functions, gives

```text
Var_(nu_B(.|z))(g)
 <= [1/(1-q)] sum_(i in B)
       nu_B(.|z)[Var_(nu_i(.|all other links))(g)].
```

The product-Haar one-link Poincare constant is `1/3`. The one-link tilt
comparison in (O5) gives `exp(8Y/3)/3` for every conditional one-link
law. Combining the two estimates yields, uniformly in `B` and `z`,

```text
Var_(nu_B(.|z))(g)
 <= C_0(Y) integral sum_(i in B) |grad_i g|^2 dnu_B(.|z),
C_0(Y)=exp(8Y/3)/[3(1-4Y/3)].                            (O7)
```

Thus (O2) holds with `c_(B,e)=C_0(Y)` for every block, including extensive
or disconnected blocks. The proof uses the actual conditional laws.
It does not assume that the block vacuum is the ground state of a
separately chosen block Hamiltonian, or that freezing the exterior
preserves its own independent gauge group.

The sole analytic extension of the accepted conditional proof is applying
its already supplied bounds to these conditional product manifolds.
The uniformity follows from (O6), not from a volume-independent bound on
the full block's density oscillation.

## 4. Forest complements see all physical variance

**Lemma.** If the outside-edge set `F=E\B` is a forest, then on the
physical space

```text
P_B=J,       Jf=nu(f),       R_B=I-J.                     (O8)
```

This holds for any smooth positive gauge-invariant density `nu`, not
only product Haar and not only a perturbative vacuum.

**Proof.** As shown in section 2, `P_B f` is physical whenever `f` is
physical. It also depends only on links in `F`. The vertex gauge group
acts transitively on all assignments of group elements to a forest:
choose a root in each component and recursively choose vertex gauge
elements to send every forest link to the identity. The recursion never
has a cycle-consistency condition. Equivalently, the same procedure
maps any one forest assignment to any other.

For a smooth invariant `f`, the conditional mean is smooth because the
conditional density is smooth and strictly positive on a compact
product. It is an invariant function of the forest variables, and hence
is constant by transitivity. Conditional expectation preserves its
mean, so that constant is `nu(f)`. Smooth physical functions are dense
in the physical `L^2` subspace: first approximate by smooth functions,
then average over the compact vertex gauge group. Boundedness of
conditional expectation extends the identity to all physical `L^2`
functions. This also handles the ordinary almost-everywhere convention.

Consequently, if every block complement is a forest and
`W=sum_B w_B`, then

```text
A_w|H_phys,0 = W I,       delta_w=W,
sum_B w_B v_B(f)=W Var_nu(f).                            (O9)
```

This is an exact mixing input, not a small-correlation assumption. Each
of these block refreshes separately replaces the conditional mean of a
physical observable by its full mean. Full, nonphysical observables
need not satisfy this identity.

## 5. Direction cover: the half-weighted overlap improves the bound

For `k=1,...,d`, let `F_k` be all present links parallel to coordinate
direction `k`, and set

```text
B_k=E\F_k,             w_k=1/(d-1).                     (O10)
```

Each `F_k` is a disjoint union of finite straight paths and isolated
vertices, hence a forest, even for an irregular finite subgraph. An edge
in direction `j` belongs to exactly the `d-1` blocks with `k != j`.
It follows that

```text
sum_(k:e in B_k) w_k=1 for every original edge e,
W=sum_k w_k=d/(d-1),
delta_w=d/(d-1),             M_w=C_0(Y).                 (O11)
```

In three dimensions the blocks are `yz`, `xz`, and `xy` directions.
Each edge occurs twice, each occurrence has weight `1/2`, and the total
energy charge is exactly one. The weighted physical variance is `3/2`
times the full physical variance because all three residuals equal
`I-J`. In two dimensions the two complementary direction blocks are
disjoint; their weights are one, and the physical variance factor is two.

Combining (O4), (O7), and (O11) proves the all-state physical bound

```text
gap_phys(H)/E_el
 >= [d/(d-1)] (3/2)(1-4Y/3) exp(-8Y/3).                 (O12)
```

This improves the earlier conditional physical certificate by the exact
factor `d/(d-1)` whenever its actual-vacuum norm port is supplied.
The gain comes from the forest gauge constraint and a proved uniform
block estimate, with the overlap charged exactly. It is not obtained
by duplicating the earlier singleton residuals.

Substitute the accepted construction radius

```text
Y(r)=(9/16)(1-sqrt(1-128mr/9)),
0<=r<r_*:=9/(128m).
```

It gives `Y<9/16`, and as `r` approaches `r_*`, the right side of (O12)
has the positive limit

```text
[d/(d-1)] (3/8) exp(-3/2).
```

On each fixed finite graph, the physical restriction has compact
resolvent and a common operator domain; the bounded plaquette potential
gives min-max continuity of its first two eigenvalues in `r`. The
vacuum is invariant and unique by the accepted construction/positivity
argument. Passing to the endpoint therefore gives

```text
d=2,  0<=r<=9/256:
    gap_phys(H) >= (3/4) exp(-3/2) E_el
                 approximately 0.16734762 E_el;

d=3,  0<=r<=9/512:
    gap_phys(H) >= (9/16) exp(-3/2) E_el
                 approximately 0.12551072 E_el.          (O13)
```

The endpoint requires no new assertion of an endpoint Fourier-norm
construction. The limit is taken separately for each finite graph,
while the final displayed constants are independent of its size.

There is also an exact ceiling for this particular cover method. Write
`n_E=|E|`, `n_V=|V|`, and `Lambda=max_e sum_(B:e in B) w_B` on a
connected graph with at least one cycle. Every forest has at most
`n_V-1` edges, so every forest-complement block has at least
`n_E-n_V+1` edges. Consequently

```text
n_E Lambda >= sum_e sum_(B:e in B) w_B
           = sum_B w_B |B|
           >= (n_E-n_V+1) W,

W/Lambda <= n_E/(n_E-n_V+1).                             (O13a)
```

On the finite box with vertices `{1,...,n}^d`, `n>=2`, there are
`n_V=n^d` vertices and `n_E=d(n-1)n^(d-1)` edges. The last ratio tends
to `d/(d-1)` as the boxes grow. Thus the factor in (O12) is the best
uniform factor attainable by forest-complement covers if the only
analytic input is the same scalar block constant `C_0` for every
inside derivative. Better finite-graph factors are possible below.
A larger uniform improvement requires additional analytic or physical
energy information beyond this common-constant cover comparison.

## 6. Exact hostile controls and an actual two-square instance

### Shared product coordinates: a false factor is exposed

Use the explicitly declared control carrier `SU(2)^3` with product Haar,
without a gauge restriction. Take the three pairs `{1,2}`, `{1,3}`,
`{2,3}`, each of weight `1/2`. Each coordinate has weighted load one,
and each block has sharp gradient constant `1/3`.

Let `f(U)=Re(U_1[1,1])`, a nonconstant first spherical harmonic of the
first coordinate. It is centered, and `-Delta f=3f`. The two blocks
containing coordinate 1 have residual `f`; the other block has residual
zero. Thus

```text
<f,A_w f>/||f||^2 =1,
(1/2) integral |grad f|^2 / Var(f)=3/2.                 (O14)
```

These are exact identities on continuous `SU(2)` variables. To check the
whole residual spectrum, decompose the product `L^2` space orthogonally
by its nonempty active-coordinate subsets `S`. Each residual is identity
when its block meets `S`, and zero otherwise. The weighted eigenvalue
is `1` for `|S|=1` and `3/2` for `|S|>=2`; constants have eigenvalue zero.
Therefore `delta_w=1`, and (O4) gives the exact free full-space gap `3/2`.
Incorrectly setting all three residuals to `I-J` would claim `9/4` and
is refuted by (O14). Forest gauge invariance is a load-bearing hypothesis.

The literal false-factor-two control uses one Haar `SU(2)` coordinate
and two identical whole-coordinate blocks of weight one. Here
`delta_w=2` but `M_w=2/3`, so (O4) still gives `3/2`. Omitting the
second energy charge would claim three, refuted by the same first
harmonic. Giving both occurrences weight `1/2` returns `delta_w=1`
and `M_w=1/3`, with the same correct bound.

### Two adjacent plaquettes: actual shared link, exact normalization

Take two adjacent elementary squares. The graph has six vertices and
seven links: three private left links, three private right links, and
one shared link. Either plaquette boundary used as a block leaves the
three private links of the other plaquette outside; those links form a
path. Thus both plaquette-block residuals equal `I-J` on the physical
space for every actual positive invariant vacuum. With weights `1/2`,
their physical residual gap is one. The shared edge also has load one,
while each private edge has load `1/2`. Bound (O4) gives `1/(2C_0)`.
Two plaquette pictures alone do not double this gap certificate.

For a sharper finite cover, take all complements of spanning trees.
Every such block has two edges. There are nine blocks formed from one
left-private and one right-private edge, and six formed from the shared
edge and one private edge. Give each of the former weight `5/63` and
each of the latter weight `1/21`. Their total weight is one and

```text
load(shared) =6/21=2/7,
load(any private edge)=3(5/63)+1/21=2/7.                (O15)
```

Every complement is a spanning tree, so `delta_w=1` exactly and
`M_w=(2/7)C_0`. The resulting certificate is

```text
gap_phys(H)/E_el >= 7/(4 C_0).                          (O16)
```

The maximum load `2/7` is optimal among probability weights on these
two-edge blocks: their seven loads sum to two, so their maximum is at
least their average `2/7`. This is an exact finite improvement of the
cover comparison. It does not assert optimality among all possible
physical gap proofs.

At Haar, `C_0=1/3`, so (O16) gives `21/4`. The exact free physical gap
of this graph is six. Indeed, in the complete invariant Peter–Weyl
decomposition, a nontrivial spin support has no vertex incident to
exactly one nontrivial edge: such a vertex cannot carry an invariant
tensor. Every finite nonempty support therefore contains a cycle, of
length at least four. Each occupied edge contributes at least `3/2`
to `T`, giving a lower bound six. The fundamental character of either
square holonomy attains six. This is an all-spin written argument,
not a cutoff calculation. It checks the normalization and shows that
even the optimized two-edge cover does not exhaust the energy constraint.

For this very small graph a direct bounded-potential comparison can
also be stronger: `0<=V=r(2-a_L-a_R)<=4r`, the free physical first
excitation is six, and the constant Haar trial state gives ground energy
at most `2r`. Hence `gap_phys(H)/E_el>=6-2r` when this is positive.
The finite cover calculation should therefore be read as a sharp
control of the stated cover method, not as a superior small-graph
spectral computation.

## 7. Boundaries, proof status, and what remains open

The direction-cover improvement (O12) is a written theorem using the
accepted actual-vacuum norm, conditional influence, and form results.
The complete normalization, forest identity, conditional block transfer,
and two exact controls are proved above. No old verifier, spin truncation,
numerical eigensolver, simulation, installation, publication, or git
mutation was used. The rational weights in (O15) are checked directly
by the displayed finite sums; no checker soundness is being assumed.

The necessary boundaries are explicit:

- An exterior containing a cycle can retain nonconstant gauge-invariant
  holonomy information. Its conditional projection need not equal `J`.
  Periodic coordinate-direction loops therefore invalidate the direction
  forest argument unless an appropriate new cover is supplied.
- Removing some vertex gauge constraints, admitting boundary charges,
  or retaining nonphysical observables changes the invariant receiver.
  Forest-link assignments can then carry retained information; (O8)
  must be proved anew or omitted.
- The blocks in (O10) are generally extensive and disconnected. Their
  conditional estimate is uniform because of (O6)–(O7), not because
  they are small local neighborhoods or efficiently sampled updates.
- The factor improvement strengthens the energy bound within the
  existing constructed-vacuum window. It does not extend the interval
  supplying `Y(r)`, prove a uniform local inverse past it, or establish
  a continuum mass gap. Those ports remain **OPEN**.

The proposed overlapping picture therefore earns a specific mathematical
continuation: preserve the shared links, choose forest-complement blocks,
and split their repeated energy contributions with positive weights. The
improved physical variance-to-energy ratio follows from that complete
contract.
