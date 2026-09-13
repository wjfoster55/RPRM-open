# A covering argument for the interacting lattice sector

Research continuation, 12 September 2026. Publication remains on hold.

The covering argument can be closed for a specified, genuinely interacting
quantum SU(2) lattice family. It controls all excited states, uniformly as
the finite lattice grows. It also admits an explicit small-interaction
interval. This is a fixed-lattice result, with the continuum problem still
open. The derivation below does not assert novelty in the literature.

The full direct proof is in [DIRECT_COVER_ATTEMPT.md](DIRECT_COVER_ATTEMPT.md).
The filename preserves its origin as an audited candidate. An independent
established-theorem route is in
[LITERATURE_STABILITY_AUDIT.md](LITERATURE_STABILITY_AUDIT.md).

## 1. Exact question and carrier

Let G be any finite connected nearest-neighbor subgraph of Z^d, d=2 or 3,
with at least one elementary square. Each edge is a distinct occurrence,
stored in its positive coordinate orientation. P is any set of distinct
elementary squares present in G. There are no periodic identifications,
external charges, matter fields, spin cutoffs, or independent copies of a
shared link. The theorem also gives a form inequality on graphs without a
square, but their physical excited sector may be empty.

Write

```text
Q_G = SU(2)^(E_G),                 mu_G = product normalized Haar,
H_ambient = L2(Q_G,mu_G),          H_phys = H_ambient^(SU(2)^(V_G)),
T_G = -(1/2) sum_e Delta_e,        a_p = (1/2)Tr(U_p),
H_G/E_el = A_G(r)+r|P|I,          A_G(r)=T_G-r sum_p a_p,
E_el=alpha hbar^2>0,              r=beta/E_el>=0.
```

The left generators are i sigma_k, so one SU(2) link is the unit round
three-sphere; -Delta has eigenvalues 4j(j+1). The one-link kinetic gap is
3/2. These are the accepted quantum bridge's conventions. The plaquette
potential is bounded and real; the operator domain is that of T_G and its
form domain is the first Sobolev space. Equality of vectors is equality
almost everywhere, rather than equality of coordinate descriptions.

The receiver is the energy of every normalized vector orthogonal to the
**actual interacting ground state**. With its normalized vector psi_G and
actual energy E_0,G, the desired statement is

```text
q_H[phi]-E_0,G ||phi||^2
    >= delta E_el (||phi||^2-|<psi_G,phi>|^2),             (C1)
```

for all vectors in the physical form domain, every admitted G, and a
constant delta>0 independent of G. q_H denotes the quadratic form; an
operator-domain assumption is not silently imposed on form-domain vectors.

## 2. What the official RPRM material contributed

The useful donor was the proof-donut's one-sided enclosure rule, together
with the requirement to retain shared occurrences and the whole requested
receiver. The previous relative-exclusion note already instantiated its
logical form: cover every possible cheap trial state by a larger family,
then exclude that entire family with a valid lower bound.

Here the larger family is the full link Hilbert space. Every physical
trial vector occurs there with the same operator, ground energy and norm.
The ambient ground state is positive and unique and therefore invariant
under all vertex gauge transformations. Consequently an ambient form
inequality transfers directly to the physical space. No reconstruction of
all physical eigenvectors, and no tensor factorization of the constrained
physical space, is required.

This does not reduce RPRM to a Hilbert-space inclusion. It is one realization
of the broader receiver-specific enclosure principle. See
[OFFICIAL_DOCS_TRANSFER.md](OFFICIAL_DOCS_TRANSFER.md) for the selected
official/current sources, their exact scope and hashes. It records selected
reading across the official map, not an assertion that every document or
every running research task was exhausted. BSD's coverage distinction and
the current expansion/compression results are donors of a proof obligation;
their mathematics is not imported as a Yang-Mills theorem.

## 3. The direct covering bound

Put m=2(d-1), the maximum number of elementary plaquettes containing one
link. For every admitted graph,

```text
0 <= r <= 1/(48m)  ==>  gap(H_G|H_phys)/E_el >= 1/2.      (C2)
```

Thus r<=1/96 in d=2 and r<=1/192 in d=3 suffice. The constants are
conservative sufficient bounds, not measured transition points or optimal
gaps. All spins and all sizes are included by the written argument.

The construction uses the real log vacuum u=log psi with Haar mean zero.
Expand u into tensor Peter-Weyl blocks u_J=Tr(B_J pi_J). Define

```text
lambda_J = sum_e 2j_e(j_e+1),
y(u) = max_e sum_(J: j_e>0) lambda_J ||B_J||_1.            (C3)
```

This norm counts every block touching a given link, including blocks
involving arbitrarily many links and arbitrarily large spins. Its energy
weight pays for derivatives. It is a new explicit function-space contract,
stronger than the earlier fixed-graph L2 expansion contract. The change is
justified by the missing receiver: pointwise joint response across the full
graph could not follow from an average L2 remainder alone.

Let Q remove the Haar mean. The exact log-vacuum equation is the fixed point

```text
u = r T^-1 S + (1/2) T^-1 Q |grad u|^2,   S=sum_p a_p.   (C4)
```

The crucial two estimates, proved in the direct note without any cutoff,
are

```text
y(T^-1 S) <= 8m,
y(T^-1 Q <grad u,grad v>) <= (8/3)y(u)y(v).              (C5)
```

The reason volume disappears is exact: multiplication can only use the
union of the input supports; differentiated inputs must share a link;
and T^-1 cancels the output energy weight in (C3). Counting from one fixed
link then charges each contribution to an already controlled input sum.
There is no multiplication by the total number of plaquettes.

At r<=1/(48m), the radius-1/4 ball maps to itself:
8mr+(4/3)(1/4)^2<=1/4. Its contraction factor is at most 2/3.
Banach contraction constructs the exact u with y(u)<=1/4. For each finite
graph the weighted series has two continuous derivatives, and elliptic
regularity makes it smooth. The positive function exp(u) satisfies the
Schrodinger equation with its exact energy shift

```text
E_A = -(1/2) integral |grad u|^2 dmu.
```

It is the true ground state. The scalar shift has not been neglected.

For any collective tangent vector v, the same norm gives

```text
|Hess u(v,v)| <= 2y(u)|v|^2.                              (C6)
```

The product source has Ricci tensor 2g regardless of its number of factors.
Normalize psi_hat=exp(u)/||exp(u)||_2. For the actual vacuum measure
dnu=psi_hat^2 dmu, its weighted curvature obeys

```text
Ric_nu = 2g-2 Hess u >= (2-4y(u))g >= g.                 (C7)
```

The weighted Bochner identity then bounds every nonconstant spectral
component of the ground-state-transformed operator. Its form is
(1/2) integral |grad f|^2 dnu, so (C7) yields (C1) with delta=1/2 on
the ambient space, hence on the physical space. This is the all-state
covering step; a finite list of tested directions is not used in its place.

The geometric inequality is standard. The particular local Fourier norm,
explicit constant chain and their application to this admitted lattice
family are written derivations in this continuation. Independent review
and finite exact checks corroborate them; they are not proof-assistant
certification or a claim of an unprecedented strong-coupling theorem.

## 4. Independent literature route and boundary correction

Yarotsky's published product-state stability result, in his explicit
[primary restatement](https://arxiv.org/pdf/math-ph/0411042), Theorem 1
and equation (5), covers infinite-dimensional on-site spaces, unbounded
gapped on-site operators and weak bounded interactions of fixed range.
Its constants do not depend on the finite volume. The matching theorem
uses empty boundaries; translation invariance is not needed here.

The exact adapter groups the d outgoing link rotors at each lattice site,
divides the kinetic operator by g_0=3/2, and pads the finite site set to
Lambda=V+{0,e_1,...,e_d}. Extra rotors are free with a unique constant vacuum.
Each actual plaquette survives the theorem's boundary-containment rule and
uses only its actual four links. The padded operator is exactly

```text
(A_G/g_0) tensor I + I tensor (T_dummy/g_0).
```

Tensoring with the dummy vacuum is an isometry intertwining the original
and extended operators. For b_d=binomial(d,2), the local normalized
perturbation is bounded by b_d r/g_0. The theorem consequently supplies
some graph-independent r_0(d)>0 with gap/E_el>=3/4 for r<r_0(d).
The audited primary statement does not supply numerical constants.
This existential interval must not be confused with the explicit
1/(48m) interval of the separate direct proof.

There was a real boundary trap: using the unpadded union support on a
three-dimensional unit cube discards three valid boundary faces. Adding
free rotors resolves it exactly, rather than changing the physical model.
The detailed audit preserves the initially rejected periodic-boundary
citation and explains why the matching source is needed.

## 5. What is now covered, and the remaining physical obligation

The physically justified refinement is complete on the same interval.
[CONDITIONAL_REFINEMENT.md](CONDITIONAL_REFINEMENT.md) uses the stronger
norm to supply exactly the missing CP8 receiver: a uniform sum of the
actual remainder's exterior oscillations. With t=8mr and

```text
Y(t)=(3/8)(1-sqrt(1-16t/3)),
W(t)=Y(t)-t-(4/3)t^2,
sum_(j!=e) epsilon_ej(G,r) <= (16/3)W(8mr)
                              <= (160/3)(8mr)^3,        (C9)
```

the accepted second-order head gives actual conditional influence rows
strictly below 1/12, uniformly in G. This controls every outside
configuration, not an average remainder. The direct spectral bound above
does not rely on assuming a conditional-to-spectral implication.

Volume growth at fixed admitted r is now covered: no sequence of finite
graphs and normalized actual-vacuum-orthogonal states can have relative
energy tending to zero. In particular, the assertion is stronger than
each finite graph having a gap whose value might shrink like 1/|G|.

This does not yet construct an infinite-volume physical representation
or a continuum field theory. Taking a limit requires a specified local
observable algebra, compatible limiting states and dynamics, and a passage
of the spectral inequality to the resulting physical representation.
The fixed-lattice small-r covering estimate is an input to such work.

There is a second, distinct limit: refining the lattice to recover
continuum physics. Changing an energy unit multiplies both coefficients
by the same factor and leaves r=beta/E_el unchanged. Changing the actual
bare theory along a refinement path generally changes r. In a common
3+1 dimensional Kogut-Susskind convention (natural units),

```text
H_E = g_b^2/(2a) sum_e J_e^2,
H_B = 2/(g_b^2 a) sum_p (1-a_p),
T = 2 sum_e J_e^2,
E_el = g_b^2/(4a),                 r = 8/g_b^4.           (C8)
```

This coefficient translation is derived from equations (56)-(57) of
[the primary Hamiltonian reference](https://scoap3-prod-backend.s3.cern.ch/media/files/84451/10.1103/PhysRevD.109.074501.pdf).
It states one convention explicitly rather than assuming factors of two
agree across sources. Along the usual weak-bare-coupling direction
g_b->0, r grows, and eventually leaves the proved interval. Rescaling
energy units cannot prevent that departure.

Geometrically, the source spheres remain curved, but the vacuum can bend
more strongly when the magnetic term dominates. Our proof works because
the kinetic geometry has a certified margin over that bending everywhere.
Losing this sufficient margin does **not** prove the physical gap closes.
It only ends this particular certificate. Anisotropic or gauge-physical
estimates could preserve the spectral question with a weaker hypothesis.

The concrete next obligation is to find a reference geometry, an
interacting block model, or another complete lower enclosure along a
specified increasing-r path, and prove that its retained physical form
still excludes all cheap collective sequences. A chart change alone is
insufficient: it must transport the kinetic form, the actual vacuum
measure, gauge constraint and physical energy comparison together.
Any generated longer-range or many-link interaction must enter the new
bound; it cannot be omitted because the final picture looks local.

There is a sharper diagnosis in [NEXT_OBLIGATION.md](NEXT_OBLIGATION.md):
the current fixed-point contraction stops while its geometric gap bound
would still be positive. Thus the first obstruction we can identify is
the strength of the construction estimate, rather than evidence that
the actual geometry or gap has failed.

Finally, a positive relative bound must remain positive against a fixed
physical reference energy on the chosen continuum path. Neither (C2)
nor the change of units in (C8) proves that nontrivial limiting theory
exists. The [official Yang-Mills problem statement](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf)
requires continuum existence and a positive mass gap. Those obligations
remain open here.

## 6. Evidence grades and preserved distinctions

- Established literature: Peter-Weyl harmonic analysis, Fourier algebra
  multiplication, Banach contraction, elliptic ground-state theory,
  weighted Bochner/Poincare reasoning, and product-state gap stability.
- Newly derived here: the explicit local norm estimates and threshold,
  their all-state physical transfer, and the exact finite-open-graph
  padding adapter. No literature-priority claim is made.
- Accepted starting evidence: YM1/YM2 separation results, the interacting
  quantum bridge, and the earlier connected-vacuum coefficients. Their
  original checkers and simulations were not rerun.
- Finite evidence: new rational constant controls, complete bounded
  graph/boundary controls and adversarial cases. They do not establish
  unrestricted analytic validity independently of the written proofs.
- Open: continuation toward increasing r, continuum construction and
  physical mass-gap survival. A failure of this sufficient certificate
  does not produce a separating witness against the true gap.

Original RPRM meanings, correlated ports and receiver boundaries are
retained. No complete microscopic solution fiber is being returned as
ONE; the result is a universal lower inequality on the stated carrier.
