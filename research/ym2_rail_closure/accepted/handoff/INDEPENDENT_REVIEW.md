# Independent review of the explicit trial-reference route

12 September 2026. **Disposition: PASS for the written finite-graph
mathematical claims in TR1–TR8 and the repaired scalar-majorant comparison.**
One distinction between an actual norm and its uniform upper bound was
reported during review and is corrected in the reviewed source. No
remaining mathematical defect was found at the declared scope.

This review independently checks the calculations and their use of the
accepted conditional and forest-cover arguments. It does not re-prove
every inherited YM theorem, run old verifiers, certify new checker output,
or establish a stronger coupling interval.

## 1. Source and inherited analytic inputs

The reviewed source is [TRIAL_REFERENCE.md](TRIAL_REFERENCE.md), SHA-256
`CCDC03F843BB5EB3D1627E4655E86E9CAC1BFED8074D13B58554A696A9C54C7A`.
The following inherited proof passages were also inspected:

- [BLOCK_COVER.md](accepted/overlap/BLOCK_COVER.md), sections 2–5:
  energy weights, uniform conditional block estimates, forest invariance
  and the factor `d/(d-1)`.
- [CONDITIONAL_GAP_EXTENSION.md](accepted/overlap/accepted/estimate/CONDITIONAL_GAP_EXTENSION.md),
  sections 2–4: probability total variation, matrix orientation in the
  continuous conditional-update proof, spectral-measure passage, and the
  one-link tilted Haar inequality.
- [SOURCE_NORM_REFINEMENT.md](accepted/overlap/accepted/estimate/SOURCE_NORM_REFINEMENT.md)
  and [COMBINED_REVIEW.md](accepted/overlap/accepted/estimate/COMBINED_REVIEW.md):
  the previously supplied source bound `4m` and bilinear bound `16/9`.

The new application requires those conditional arguments for a smooth
positive gauge-invariant reference density. Their proofs depend on the
conditional bounds, positivity and reversibility, rather than on the
reference being an eigenfunction. The forest identity is already stated
for every such invariant density. Thus this change of input is admitted.

## 2. Exact transport and spectral comparison: TR1–TR2

For `T=-Delta/2`, direct differentiation gives

```text
T(phi f)=phi T f-grad phi dot grad f+f T phi,
(T phi)/phi=T(log phi)-(1/2)|grad log phi|^2.
```

Both signs and the coefficient `1/2` in TR1 follow. The measure is
`phi^2 mu`, so `K_phi=T-grad log phi dot grad` has form
`(1/2) integral |grad f|^2 dnu_phi`. Multiplication by `phi` is unitary
between the two stated Hilbert spaces; strict positivity on a fixed
compact graph makes its smooth inverse legitimate on the relevant
Sobolev domains. None of this asserts a uniform multiplier bound over
growing graphs.

The constant function has norm one under `nu_phi` and is the zero mode
of `K_phi`. Min–max on the same physical Hilbert space gives
`E1(A)>=g_phi+inf R_phi`, while its Rayleigh quotient gives
`E0(A)<=nu_phi(R_phi)`. Subtraction has exactly the sign in TR2.
The excitation complement qualification is necessary: a tree with all
vertex gauge constraints has no physical first excitation.

If `R_phi` is constant, the nonnegative form of `K_phi` itself proves
that `phi` is a ground state, so the conclusion does not depend merely on
a suggestive similarity of trial and vacuum values. If `R_phi` is not
constant, omitting it changes the transported operator.

## 3. Trial cancellation and reference gap: TR3–TR4

Each of the four distinct links of an elementary plaquette contributes
`3/2` to the kinetic eigenvalue of its fundamental trace coordinate.
Thus `T a_p=6a_p`, with the adopted unit-round metric. The normalization
constant in `log phi_c=cS-constant` has zero derivative. Consequently

```text
R_c=(6c-r)S-(c^2/2)|grad S|^2,
c=r/6  ==>  R_r=-(r^2/72)|grad S|^2.
```

The reference log density is `2 log phi_r=(r/3)S+constant`. An edge
meets at most `m` plaquettes. A one-coordinate trace change costs at
most two per incident plaquette; a four-point mixed difference costs
at most four per common plaquette. Therefore

```text
D_i <= 2rm/3,
D_ij <= (4r/3)n_ij,
sum_(j!=i) n_ij <= 3m.
```

The probability-TV convention is load-bearing. The conditional tilt
bound is `tanh(D_ij/4)<=D_ij/4`, yielding `q<=mr`, with no extra factor
two. The accepted continuous update argument applies on every fixed
conditional block. A block's internal influence row cannot exceed the
full row, and its one-link conditional density is the same one with
exterior values fixed. Tilt comparison therefore gives
`C_ref=exp(2mr/3)/[3(1-mr)]` for every block when `mr<1`.

Finally, the physical forest-complement cover has total variance weight
`d/(d-1)` and unit edge load. Its derivative form has the factor `1/2`.
This yields precisely TR4. It proves a larger admissible window for the
reference diffusion gap; it does not establish a larger gap window for
the original interacting Hamiltonian without residual transfer.

## 4. The extensive witness is an admitted SU(2) construction: TR5–TR6

The proposed squares at horizontal coordinates `3k,3k+1`, joined along
the bottom row, form a connected open lattice subgraph. Each connection
passes through a bottom-row intermediate vertex without adding a top
edge across the gap. Its connecting edges are bridges and create no
extra elementary plaquette. Square edge sets are disjoint.

On one plaquette, multiplication by fixed SU(2) matrices and inversion
are isometries, so the round-sphere identity for the real trace coordinate
gives `|grad_i a_p|^2=1-a_p^2` on each of its four links. Summing gives
`4(1-a_p^2)`. Different squares have disjoint derivative supports, hence
their cross terms are exactly zero. TR3 now gives

```text
R_r=-(r^2/18) sum_p(1-a_p^2).
```

These extrema are realizable by actual link matrices. Put every link
equal to the identity to obtain all `a_p=1`. To obtain all `a_p=0`,
put one link of each square equal to `diag(i,-i)` and leave its other
links and every bridge equal to the identity. Orientation reversal
does not alter its zero trace. These are lawful configurations; gauge
invariance constrains physical functions and does not prohibit them.
Thus `inf R_r=-Nr^2/18`, `sup R_r=0` and the oscillation in TR5 are exact.

The distinct holonomies are independent Haar variables because they
depend on disjoint independent link sets. The reference density
factorizes as a product of `exp((r/3)a_p)` factors; bridge integration
contributes one. Hence the sharper TR2 loss is exactly
`(Nr^2/18) E_tilt[a^2]`.

Haar SU(2) is the round unit three-sphere, so symmetry of its four real
coordinates gives `E[a^2]=1/4`. Symmetry of `a` replaces the exponential
tilt in this even expectation by `cosh((r/3)a)`. Its covariance with
`a^2` is nonnegative: for two independent trace values `x,y`, both
`x^2-y^2` and `cosh(rx/3)-cosh(ry/3)` have the same sign, determined by
`|x|-|y|`. This proves `E_tilt[a^2]>=1/4` and the constant `Nr^2/72` in
TR6.

The conclusion is appropriately limited. Subtracting this loss from
the specific graph-independent lower certificate TR4 eventually yields
no positive certificate. This does not show that the actual gap closes,
that every possible reference-gap estimate fails, or that all residual
comparison methods must pay this bulk cost.

## 5. The actual correction and local ports: TR7–TR8

For the actual positive ratio `psi/phi_r=constant*exp(v)`,
`(K_phi exp(v))/exp(v)=K_phi v-(1/2)|grad v|^2`.
The eigenfunction equation therefore has the signs shown in TR7.
Integration is with respect to the **reference** measure, where
`nu_phi(K_phi v)=0`; it gives

```text
E0=nu_phi(R_r)-(1/2)nu_phi(|grad v|^2),
K_phi v=-Q_phi R_r+(1/2)Q_phi |grad v|^2.
```

An additive constant in `v` is its normalization freedom and disappears
from this equation. The projection is the reference-mean projection;
replacing it by Haar centering in this equation without transforming
the inverse would be invalid.

The actual log density is the reference log density plus `2v`, up to
its constant. Triangle inequalities for one-link and four-point mixed
oscillations give `D_actual<=2mr/3+d_v` and
`q_actual<=mr+b_v/4`. Applying the same conditional proof to the actual
vacuum, followed by its genuine ground-state form identity, gives TR8
with exactly the displayed exponent, row margin and factor `3/2`.
The supplied bounds must concern the actual solution `v`, uniformly
over the graph family. A trial correction or an `L2` Poisson estimate
does not supply those local supremum bounds.

## 6. The old majorant and the correction made during review

The original draft defined `t` as the actual norm bounded by `4mr` and
then called `t<9/32` equivalent to `r<9/(128m)`. An upper bound alone
does not give that equivalence on every graph. This was reported to the
author immediately. The reviewed text now defines `t:=4mr` as the
uniform source majorant, with `||w||_*<=t`, which repairs the statement.

With `b=8/9`, the three contributions after writing `u=w+v` cost
`bt^2`, `2btZ` and `bZ^2`. Their sum is `b(t+Z)^2`.
Thus `Y=t+Z` transforms the majorant exactly to `Y=t+bY^2`.
The smaller fixed point has contraction factor `2bY<1` under the
strict discriminant condition `t<1/(4b)=9/32`; with the repaired
definition this is `r<9/(128m)`. The source recentering by itself has
therefore not improved these absolute norm estimates. The anchored
formulation ignores additive log constants; it does not silently
replace the reference-mean projection of TR7.

All of these conclusions are written mathematical checks at the stated
finite-graph scope. Uniform local correction estimates, a better uniform
excitation comparison, and the continuum limit remain open.
