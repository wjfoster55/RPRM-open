# An exact finite-graph quantum bridge and its gap boundary

12 September 2026. This note changes the carrier explicitly from classical
phase states to wavefunctions. It gives an exact representation of a chosen
quantum Hamiltonian on the same open two-square graph and a positive
spectral-gap lower bound in a stated parameter region. The derivations use
standard compact-group representation theory and the variational principle;
no mathematical novelty, numerical spectrum, or continuum mass gap is claimed.

**Result.** With the full seven-link electric operator, gauge invariance at
all six vertices, generators `i sigma_k`, and coefficients `alpha>0`,
`hbar>0`, `beta>=0`, the physical quantum gap satisfies

```text
gamma = E_1-E_0 >= 6 alpha hbar^2 - 2 beta.                 (Q1)
```

This is informative when `beta < 3 alpha hbar^2`. In the explicitly chosen
reference quantization `alpha=beta=hbar=1`, it gives `gamma>=4` in reference
energy units. This choice of Planck parameter is additional quantum input,
not a measured scale or a consequence of classical reduction.

## 1. Contract and the source quantum model

Use the exact graph, loop words, open boundary, and full vertex action from
[GLOBAL_TREE_PHASE.md](GLOBAL_TREE_PHASE.md). In particular, no boundary
charge is admitted. Let `Q=SU(2)^7`, with product normalized Haar measure
`mu_Q`. The Hilbert spaces are

```text
H_kin  = L^2(Q,mu_Q),
H_phys = {psi in H_kin : psi(g.q)=psi(q) for every g in SU(2)^6},
```

where equality of wavefunctions means almost-everywhere equality. The
gauge-invariance statement is equality in `L^2`. Gauge averaging is the
orthogonal projection onto `H_phys`; it is not a gauge fixing at singular
configurations. All irreducible spins are admitted: this is an infinite
dimensional Hilbert space on a finite graph, without a spin cutoff.

Let `D_(e,k)` be the left-invariant derivative along the unit generator
`T_k=i sigma_k` on edge occurrence `e`, and fix

```text
<X,Y> = -Tr(XY)/2,
Delta_e = sum_(k=1)^3 D_(e,k)^2,
T = -(alpha hbar^2/2) sum_e Delta_e,
V = beta [(1-a)+(1-b)],
H = T+V,                                                    (Q2)
```

where `a=Tr(U)/2`, `b=Tr(V_loop)/2` are the elementary plaquette half traces.
Here `V_loop` names the right holonomy; the unqualified `V` in (Q2) names
the potential operator. The coefficient choice quantizes the classical
Hamiltonian `alpha sum_e |E_e|^2/2 + beta(2-a-b)` on the unreduced compact
source, then restricts to invariants. It does not assume that a quantization
chosen directly on an arbitrary reduced chart would be equivalent.

The nonpositive Laplacian on the closed compact manifold `Q` has its usual
self-adjoint realization. Since `0<=V<=4 beta` is smooth and gauge invariant,
`H` is self-adjoint on the Laplacian domain, has compact resolvent, and
preserves `H_phys`. Its restriction has compact resolvent as well. Its
quadratic form domain is `H^1(Q) intersect H_phys`.

The requested receiver is the physical spectrum, energy expectation, and
all Schrödinger continuations `exp(-itH/hbar)` of this particular model.
The supplied ports are the graph, Haar measure, gauge action, generator
normalization, coefficients, and operator domain. The interacting
eigenfunctions and exact gap remain missing ports. A lower bound on the gap
does not return a complete solved eigenfunction fiber.

This is the established Hamiltonian lattice-gauge setup of
[Kogut and Susskind (1975)](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.11.395).
The fixed-graph invariant Hilbert-space construction and its complete
spin-network basis are described in
[Baez, *Spin Network States in Gauge Theory*, Section 2, Lemma 3](https://arxiv.org/pdf/gr-qc/9411007).

## 2. The exact trace Hilbert space, including the boundary domain

Let `x=(a,b,w)`, with `w=Tr(U V_loop)/2`, and define

```text
delta(x) = 1-a^2-b^2-w^2+2abw,
K = {x in [-1,1]^3 : delta(x)>=0}.
```

The [static join](accepted_sources/ym2_spatial_joint/STATIC_JOIN.md) classifies every
configuration gauge orbit by `x`, including the singular boundary. Write
`pi:Q->K` for this quotient. The pushforward probability measure is

```text
dmu_K = (2/pi^2) da db dw on K.                            (Q3)
```

To derive (Q3), change link variables to a tree and its two based holonomies.
Successive Haar-preserving translations show that the latter are independent
Haar `SU(2)` variables after integration over the tree. One Haar quaternion's
scalar `a` has density `(2/pi)sqrt(1-a^2)` on `[-1,1]`. Conditional on their
scalars, the two unit vector directions are independent and uniform on
`S^2`; their cosine `z` is uniform on `[-1,1]`. Since

```text
w=ab-sqrt(1-a^2)sqrt(1-b^2) z,
```

the Jacobian cancels both square roots and leaves `2/pi^2`. The exceptional
central and collinear loci have Haar measure zero. The same formula implies
`Vol(K)=pi^2/2`, so it is normalized.

Consequently

```text
W:L^2(K,mu_K)->H_phys,  W f=f o pi                         (Q4)
```

is unitary. Norm equality is the pushforward identity. Surjectivity follows
because a measurable gauge-invariant function descends almost everywhere
through the complete compact-group orbit quotient. The inverse is descent
through this quotient, unique up to null sets. Individual point values at
the singular boundary are not extra quantum states in `L^2`.

Use the full-link cometric from
[PHASE_CLOSURE.md, (P3)](accepted_sources/ym2_spatial_joint/PHASE_CLOSURE.md):

```text
       [ 4(1-a^2)       w-ab          3(b-aw)  ]
M(x) = [ w-ab           4(1-b^2)      3(a-bw)  ].
       [ 3(b-aw)        3(a-bw)       6(1-w^2) ]
```

For a smooth function of the trace variables, the source chain rule gives

```text
sum_e Delta_e(f o pi) = (L f) o pi,
L f = sum_(i,j) M_ij partial_i partial_j f
      -12a partial_a f -12b partial_b f -18w partial_w f
    = div(M grad f).                                      (Q5)
```

Here each distinct edge traversed by a simple trace loop contributes `-3`
times that trace. The loop lengths are `4,4,6`, which give the three drift
coefficients. Direct differentiation also gives
`sum_i partial_i M_ij=(-12a,-12b,-18w)_j`, verifying the divergence form
against the independently derived constant measure.

Thus the exact transported operator is

```text
H_K = -(alpha hbar^2/2) div(M grad) + beta(2-a-b),
Dom(H_K)=W^-1[H^2(Q) intersect H_phys].                    (Q6)
```

Equivalently, define the form by closing the source smooth invariant core
under its form norm, then transport it with `W`. This specifies the behavior
at every singular boundary without choosing an extra Dirichlet or Neumann
condition there. The differential expression alone would leave an operator
domain obligation. The core can be described as the descents of
`C^infinity(Q) intersect H_phys`; no regular-coordinate extension is assumed
to describe all elements of that core or of the final operator domain.

The intertwining relation is on the complete operator domains. Functional
calculus therefore gives, for all real `t`,

```text
W exp(-it H_K/hbar) = exp(-it H/hbar) W.                   (Q7)
```

This closes a quantum continuation receiver for the chosen model. It is
stronger than matching a classical symbol or matching finitely many
derivatives. It does not assert that classical and quantum state carriers
are invertibly related.

## 3. The exact electric gap is fixed by the shortest closed loop

In the stated metric, `SU(2)` is the unit round `S^3`. Its spin-`j` matrix
coefficients have `-Delta` eigenvalue

```text
c_j=4j(j+1),   j=0,1/2,1,...;
c_0=0, c_(1/2)=3.                                        (Q8)
```

The normalization can also be checked without a convention lookup:
`sum_k T_k^2=-3 I` in the fundamental representation, hence each fundamental
matrix coefficient has eigenvalue `3`. The factor four relative to the
`j(j+1)` convention is explicitly discussed in
[Jakobs et al., Section III.4, equation (42)](https://arxiv.org/html/2304.02322v2#S3.SS4).

Peter--Weyl decomposition on the seven independent link variables
diagonalizes `T` by edge labels `j_e`, with eigenvalue

```text
(alpha hbar^2/2) sum_e 4j_e(j_e+1).                       (Q9)
```

Gauge invariance requires a singlet intertwiner at every vertex. In a
nonzero invariant basis vector, consider the support consisting of edges
with `j_e>0`. A vertex cannot have exactly one incident support edge:
a single nontrivial irreducible representation, tensored with trivial
representations, has no invariant vector. Thus every vertex incident to
the support has degree at least two in that support. A nonempty finite
graph with this property contains a cycle. The open two-square graph has
no cycle shorter than four edges. Hence every nonconstant invariant basis
vector has at least four nonzero edge labels and costs at least

```text
(alpha hbar^2/2) * 4 * 3 = 6 alpha hbar^2.
```

This argument uses every spin label; it is not an enumeration below a
cutoff. The constant is the unique all-trivial vector. The half trace of
either elementary plaquette is nonconstant, gauge invariant, mean zero,
and obeys `-sum_e Delta_e a=12a` or the same identity for `b`. These vectors
attain the lower bound. Therefore

```text
lambda_0(T|H_phys)=0,
lambda_1(T|H_phys)=6 alpha hbar^2.                        (Q10)
```

Equivalently, for the inherited form domain on `K`,

```text
integral_K (grad f)^* M grad f dmu_K
  >= 12 integral_K |f-integral_K f dmu_K|^2 dmu_K.         (Q11)
```

The one-link kinetic eigenvalue `3 alpha hbar^2/2` is a useful normalization
check but is not the physical first excitation on this graph: its endpoints
would carry unsatisfied gauge transformation indices. Conversely, adding
boundary charges, a self-loop, a short periodic identification, or changing
the edge metric changes the proof's contract and can change the gap.

## 4. A rigorous interacting lower bound

Order eigenvalues on `H_phys` with multiplicities as `E_0<=E_1<=...`.
Since `V>=0`, the min--max principle yields

```text
E_1(H)>=lambda_1(T)=6 alpha hbar^2.
```

The normalized constant is an admissible ground-state trial vector. Haar
symmetry gives `integral a=integral b=0`, hence

```text
E_0(H)<=<1,H1>=2 beta.
```

Subtracting proves (Q1). These are separate variational estimates; the
constant trial function is not assumed to be the interacting ground state,
and mean-zero functions are not assumed orthogonal to that unknown ground
state. Using only `||V||<=4 beta` would give the weaker subtraction
`6 alpha hbar^2-4 beta`; the exact Haar trial average removes that loss.

For every fixed finite `beta`, a positive gap exists in this model even
where (Q1) becomes nonpositive. Indeed, the heat semigroup of `H` on the
connected compact source is positivity improving (the positive heat kernel
and the bounded real Feynman--Kac weight suffice). Its lowest eigenfunction
is therefore strictly positive and simple. Gauge transformations fix the
unique normalized positive ground state, so it belongs to `H_phys`.
Compact resolvent then isolates that eigenvalue in the physical spectrum.
This argument gives no uniform quantitative lower bound as parameters or
the graph change. A nonpositive right side in (Q1) means that this particular
estimate is inconclusive, not that the actual finite-graph gap vanishes.

## 5. Relational scaling retains a quantum ratio

Write `T_0=-(1/2)sum_e Delta_e` and `B=2-a-b`. The exact scalar-factor
normalization is

```text
H = alpha hbar^2 [T_0+rB],
r = beta/(alpha hbar^2),
gamma/(alpha hbar^2) >= 6-2r.                            (Q12)
```

Thus the useful region is the dimensionless condition `r<3`. The reference
choice `alpha=beta=hbar=1` selects `r=1` and gives the lower bound `4`;
it cannot represent every parameter choice by a change of labels.

In the classical system with `beta>0`, the electric rescaling
`P=sqrt(alpha/beta) E` puts the energy into the form
`H/beta=sum_e |P_e|^2/2+B`. Under quantization, however, electric components
are `E_(e,k)=-i hbar D_(e,k)`, so the same rescaling produces

```text
P_(e,k)=-i hbar_eff D_(e,k),
hbar_eff=hbar sqrt(alpha/beta),
r=1/hbar_eff^2.                                          (Q13)
```

The commutator with a configuration multiplication operator scales by the
same factor. The classical energy normalization therefore retains a changed
quantum commutation scale. Setting both normalized energy coefficients and
`hbar_eff` to one would change the quantum model unless its supplied ratio
already permits it. Equations (Q12)--(Q13) identify exactly which relational
parameter survives the passage to the quantum receiver.

## 6. The next exact missing inequality

Let `psi_0>0` be the normalized physical ground state descended to `K`,
and let `dnu=psi_0^2 dmu_K`. The ground-state transform, obtained by expanding
the quadratic form and using `H_K psi_0=E_0 psi_0`, gives

```text
<psi_0 f,(H_K-E_0)psi_0 f>
  = (alpha hbar^2/2) integral_K (grad f)^* M grad f dnu.
```

Consequently the exact interacting gap is

```text
gamma = (alpha hbar^2/2)
  inf [ integral_K (grad f)^* M grad f dnu
        / integral_K |f|^2 dnu ],                        (Q14)
```

where the infimum is over nonzero `f` with `integral f dnu=0` and
`psi_0 f` in the inherited form domain. This is a weighted Poincare problem
for the full interacting vacuum measure. Local potential curvature, the
cometric determinant, or closure of a classical trajectory does not itself
bound this ratio: its denominator and its low-energy directions depend on
the full vacuum and all allowed fluctuations.

For this fixed graph, (Q14) is an exact reformulation with a uniquely
specified operator. For a mass-gap research program, the useful next
obligation is a quantitative lower bound that survives a declared graph
family, its boundary conditions, its vacuum measures, and physical energy
rescaling. A two-face bound cannot simply be added across a shared edge:
the shared link is one occurrence, the Gauss constraints are joint, and
the vacuum measure need not factor into independent two-face measures.

## 7. Why this estimate does not pass unchanged to continuum Yang--Mills

On a finite open square or cubic lattice graph with no cycles shorter than
four, containing at least one square, the same support argument gives the
same free kinetic gap. If there are `N_p` simple plaquettes and each has
coefficient `beta`, the constant trial energy is `N_p beta`. The direct
extension of this proof is only

```text
gamma_graph >= 6 alpha hbar^2 - N_p beta.                 (Q15)
```

At fixed positive `beta` this lower bound loses positivity as the volume
increases. This is a limitation of the estimate; it is not a proof of a
vanishing infinite-volume gap.

For the usual four-dimensional Hamiltonian continuum scaling, in units
`hbar=1`, the electric and magnetic prefactors have the forms
`alpha=c_E g_0^2/a_lat` and `beta=c_B/(g_0^2 a_lat)`, with fixed positive
normalization constants. Their opposing powers of the bare coupling are
visible already in the lattice Hamiltonian in
[Jakobs et al., equation (1)](https://arxiv.org/html/2304.02322v2#S1).
No specific `c_E,c_B` is imported without converting the generator metric
and plaquette convention. The ratio `beta/alpha` grows like `g_0^-4`, so
the weak-bare-coupling route leaves the positivity region of (Q1) even
before volume growth is addressed. Restoring physical units cannot turn a
negative lower bound into a positive one.

The official problem asks for a nontrivial quantum theory on four-dimensional
space-time, its axiomatic properties, and a finite positive vacuum spectral
gap. It identifies uniform finite-volume control as relevant to the
infinite-volume construction. These requirements are stated in
[Jaffe and Witten, *Quantum Yang--Mills Theory*, Sections 4--6](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf).
The present two-square graph does not yet provide a three-spatial-dimensional
family, a renormalization prescription, convergence of quantum observables,
or a uniform limit of (Q14). Those are explicit **OPEN** obligations.

A sharp control on overinterpretation is to keep the same graph and
`beta=0`, but replace `alpha` by `epsilon alpha`. Every classical quotient
identity, Haar quotient, and spin-network support statement still holds,
while the quantum gap is exactly `6 epsilon alpha hbar^2` and tends to zero.
Thus exact relational closure alone cannot supply a scale-independent gap.
The retained energy coefficients and limit contract are essential.

## 8. Proof-donut landing and evidence

The [proof-donut obligations](accepted_sources/rprm/proof-donut.md) have concrete
occupants here: complete configuration quotient, Haar pushforward,
source operator domain, the unitary map (Q4), operator and time-evolution
intertwining, complete spin-network coverage, and the variational bound.
In the [LIFT--SPIN--LAND contract](accepted_sources/rprm/operations.md#9-liftspinland),
`W`, the source quantum evolution, and `W^-1` form a correct lift, operation,
and landing for the reduced **quantum** receiver. This uses a proved
intertwining equation, not just the existence of an inverse coordinate map.

Equations (Q3)--(Q15) have written derivations, not proof-assistant
certificates. The cometric is reused at its stated scope from the adjacent
classical derivation; (Q5) adds its quantum drift and measure. The earlier
seven-link cometric proof is included as accepted source evidence. Its old
suite was not rerun. This packet's new tree checker independently checks
six regular cometric bridges against the full seven-link Jacobian.

The bounded [quantum checker](check_quantum.py) supplies a separate exact
finite certificate in [RESULTS_QUANTUM.json](RESULTS_QUANTUM.json). It
exhausts all `2^7=128` support subsets: one is empty, 123 have a degree-one
vertex, and four nonempty subsets pass the necessary no-leaf condition.
They are the left square, right square, outer cycle, and all seven edges;
the minimum support size is four. The receipt retains each subset, its
vertex degrees, and a rejecting vertex when one exists. Passing the
no-leaf test is not a sufficient intertwiner criterion: its explicit
control puts spin `1/2` on all seven edges, which fails the central-parity
condition at the two trivalent vertices despite passing the degree test.

The checker also computes the fundamental identity `sum_k T_k^2=-3I` and
all nine metric pairings using exact Gaussian integers. Exact polynomial
differentiation gives the three cometric drift coefficients; these agree
with the independent `-3` per edge rule on the explicitly verified simple
loop words of lengths `4,4,6`.

```powershell
python -I -B research/ym2_global_phase_joint/check_quantum.py
python -I -O -B research/ym2_global_phase_joint/check_quantum.py
```

Both commands recompute and compare the saved receipt without writing;
`--write-results` explicitly replaces it. Verification conditions remain
active in optimized Python. These finite checks supply the graph support,
matrix normalization, and polynomial steps. The analytic inputs remain
Peter--Weyl completeness, the `SU(2)` Casimir formula at every spin,
intertwiner representation theory, operator domains, the variational
principle, and positivity improvement. Neither checker verifies those
general results or the continuum obligations. No numerical simulation,
eigensolver run, or spin truncation is used. The bounded quantum bridge
lands at a rigorously specified finite-graph operator and estimate; the
continuum vacuum-and-gap fiber remains **OPEN**.
