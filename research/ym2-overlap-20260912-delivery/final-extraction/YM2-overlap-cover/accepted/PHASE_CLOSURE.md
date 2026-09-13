# A closed regular phase joint for the two-plaquette graph

12 September 2026. This strengthens the static join on one fixed spatial
graph. It derives a six-coordinate Hamiltonian on the regular part of the
zero-Gauss reduced phase space. The singular boundary remains a separate
contract. The derivation uses the full seven-link electric kinetic energy.

## 1. Carrier and retained question

Use the open graph of two neighboring square plaquettes, with six vertices
and seven oriented links, as fixed in [DYNAMICS.md](DYNAMICS.md). Every link
has configuration in `SU(2)`, with the bi-invariant metric
`<X,Y>=-Tr(XY)/2`; the generators `i sigma_alpha` have unit norm. The
Hamiltonian and constraints are

```text
H = (1/2) sum_(edge e,alpha) E_(e,alpha)^2 + 2-a-b,
Gauss_v = 0 at every one of the six vertices.
```

Gauge equality is the cotangent lift of the full vertex group `SU(2)^6`.
Links have independent named occurrences even when their values coincide.
The gauge tree has five links. Set `U=L=s c^-1 l^-1 a` and
`V=R=b r d^-1 s^-1`, both based at vertex B in the named-edge convention of
DYNAMICS.md. Then `VU=RL=b r d^-1 c^-1 l^-1 a` cancels the shared traversal
and is the six-edge outer word. Cyclicity gives `Tr(UV)=Tr(VU)`. Retain

```text
x=(a,b,w),  a=Tr(U)/2, b=Tr(V)/2, w=Tr(UV)/2,
Delta=1-a^2-b^2-w^2+2abw.
```

The static result gives the complete configuration quotient and its image.
Here restrict to the open regular domain

```text
D = {x: |a|<1, |b|<1, Delta>0}.
```

The trace coordinates are dimensionless; time, energy, and dual momenta use
the fixed reference normalization of the source Hamiltonian above. There
is no additional coupling or lattice-spacing rescaling in this result.
This is precisely the domain of independent vector parts of `U,V`.
In particular `|w|<1` there. It has a free residual `SO(3)` conjugation
action; equivalently the full vertex action has only its fixed diagonal
central kernel as stabilizer. The source phase carrier is the zero-Gauss
cotangent bundle over these configurations, modulo the full vertex gauge
group. The proposed retained carrier is `T*D`, with canonical momenta
`p=(p_a,p_b,p_w)` of the three trace coordinates. These momenta are not
unconstrained electric vectors on the two chord links.

The receiver retains all physical observables and Hamiltonian continuations
of this finite graph while the configuration stays in `D`, including fine
magnetic energy `2-a-b` and outer Wilson trace `w`. A bounded request may fix
finite initial energy and a finite time interval lying inside this domain.
Finite time alone does not guarantee that the regular chart remains enabled.

## 2. Why Gauss supplies exactly three canonical momenta

Let `Q=SU(2)^7`, and let `pi:Q_reg -> D` be the three-trace quotient map.
Its differential has rank three. The configuration gauge orbit has dimension
18, so the kernel of `d pi` is exactly the tangent space to that orbit.
For a cotangent vector `alpha_q`, zero Gauss means

```text
alpha_q(xi_Q(q))=0 for every infinitesimal vertex gauge motion xi_Q.
```

Thus `alpha_q` annihilates `ker d pi`. Elementary dual linear algebra gives
a unique `p in T*_(pi(q))D` with

```text
alpha_q = (d pi_q)^* p.                              (P1)
```

Conversely every such pullback has zero Gauss. Let `J_(i,e alpha)=D_(e alpha)x_i`
use the unit left-translation generator on the indicated link. Under the
metric identification, (P1) is the explicit reconstruction

```text
E_(e alpha) = sum_i J_(i,e alpha) p_i.               (P2)
```

The reverse decoder is `p=M(x)^-1 J E=M(x)^-1 dot x`, where `M=J J^T`
is positive definite on `D` as shown below. Thus these momenta are recovered
from the physical phase source and are not extra independently chosen data.

The canonical one-form pulls back as
`alpha_q(delta q)=p·delta x`. Its exterior derivative therefore gives the
ordinary canonical symplectic form in `(x,p)`. This proves the cotangent
reduction here directly; a gauge-fixed kinetic term is not assumed.

The complete source fiber for every `(x,p) in T*D` is **ONE physical gauge
class**. Construct a representative pair by writing `d=ab-w`,

```text
U=(a, sqrt(1-a^2), 0, 0),
V=(b, d/sqrt(1-a^2), sqrt(Delta)/sqrt(1-a^2), 0),
```

in the plus-i Pauli convention. Realize that pair in the declared tree
gauge and lift its momenta using (P2). All raw representatives are the full
vertex gauge orbit of this representative phase point. Completeness follows
from the static orbit classification and the uniqueness in (P1). There is
no physical mirror branch for a two-vector configuration pair. The reduced
dimension is six, equal to `42-2*18`; no reduction below the generic physical
degrees of freedom is claimed.

## 3. The full seven-edge cometric

The reduced kinetic energy is `(1/2)p^T M(x)p`, where `M=J J^T`. Explicitly,

```text
       [ 4(1-a^2)       w-ab          3(b-aw)  ]
M(x) = [ w-ab           4(1-b^2)      3(a-bw)  ].     (P3)
       [ 3(b-aw)        3(a-bw)       6(1-w^2) ]
```

Here is a direct way to audit every coefficient. A normalized trace of a
length-L simple loop has squared gradient `L(1-trace^2)`: each traversed
unit-metric link contributes `1-trace^2`. This gives the diagonal lengths
`4,4,6`. The two elementary boundaries overlap on exactly one link, with
opposite traversal; their scalar-gradient pairing is `w-ab`. The left
boundary and outer boundary have three equally oriented common links; each
contributes `b-aw`. The right and outer boundary likewise have three common
links, each contributing `a-bw`. These identities follow by cyclically
moving the differentiated link to the base and using
`Sc(AB)=Sc(A)Sc(B)-vec(A)·vec(B)`. Adjoint transport preserves the inner
product. The inverse of a backwards traversal supplies its minus sign.
This proves (P3) for arbitrary link representatives, not just a tree slice.

In particular replacing the original kinetic term by a naive independent
`(SU(2))^2` loop kinetic term would change these coefficients. Gauge fixing
does not remove the energy stored on tree links in a zero-Gauss lift.

Expansion of the determinant gives the exact polynomial identity

```text
det M = 6 Delta (16-6a^2-6b^2-w^2-3abw).             (P4)
```

The last factor is positive in `D`: because all three absolute trace values
are strictly below one, `6a^2+6b^2+w^2+3abw<16`. Since `M=J J^T`, (P4)
proves positive definiteness there. On the closed static image the last
factor is nonnegative and vanishes only at the four central corners
`|a|=|b|=|w|=1, abw=1`. Consequently `det M=0` on that image exactly when
`Delta=0`. Its rank is two on that boundary away from those corners: when
both factors are noncentral the `(a,b)` principal minor is
`15(1-a^2)(1-b^2)>0`; when `a=+/-1` and `b` is noncentral the `(b,w)` minor
is `15(1-b^2)^2>0`, with a symmetric argument for central `b`. At the
central corners `M=0`. The checker verifies the determinant as a polynomial
identity, in addition to finite exact full-link contractions.

## 4. Closed Hamiltonian and continuation proof

The complete regular reduced Hamiltonian is

```text
H_red(x,p) = (1/2)p^T M(x)p + 2-a-b.                (P5)
```

The original energy/transfer receiver has explicit readouts in this graph:

```text
U_E = (1/2)p^T M(x)p,
U_B = 2-a-b,
signed transfer = dot U_B = -(M(x)p)_a-(M(x)p)_b.
```

The signed transfer is separate from the symbol `J` used above for the
trace-coordinate Jacobian. All three readouts are retained throughout every
enabled regular continuation.

Writing `r=p_a, s=p_b, t=p_w`, its canonical equations are

```text
dot a = 4(1-a^2)r + (w-ab)s + 3(b-aw)t,
dot b = (w-ab)r + 4(1-b^2)s + 3(a-bw)t,
dot w = 3(b-aw)r + 3(a-bw)s + 6(1-w^2)t,

dot r = 4ar^2 + brs + 3wrt - 3st + 1,
dot s = 4bs^2 + ars - 3rt + 3wst + 1,
dot t = 6wt^2 - rs + 3art + 3bst.                  (P6)
```

Every right-hand side depends only on the retained six coordinates. The
source Hamiltonian is gauge invariant, preserves Gauss, and descends by
(P1) to (P5). Equality of the canonical forms proves that its projected
Hamiltonian vector field is (P6). Smooth ODE uniqueness on `T*D` then gives

```text
C(Phi_tau(q,E)) = Psi_tau(C(q,E))
```

for every source time segment whose configurations lie in `D`. The ordinary
inverse is the corresponding negative-time flow on such a segment. Enabled
times are exactly those for which the whole segment remains in this chart;
this property is constant on the complete gauge fiber. Hence this is an
operational quotient for the declared partial continuation operation, rather
than only matching initial derivatives. Energy, either plaquette trace,
and the joined trace can be read at every such time.

## 5. A boundary that the chart cannot silently cross

The polynomial expression (P6) itself can be evaluated outside `T*D`, but
that extension is not a proved representation of the singular physical
phase space. The regular configuration domain has not been shown invariant
under the full dynamics; this result does not assert its invariance.

A distinguishing hostile case has every link equal to the identity and a
nonzero divergence-free electric circulation around one square. Gauss holds,
the kinetic energy is positive, and `x=(1,1,1)`. But every trace differential
is zero there, so `J=0` and (P2) produces only zero electric field for every
finite `p`. The finite canonical chart therefore misses valid singular
phase states. This is a coverage failure at the declared boundary, not a
claim that the source evolution is undefined. A singular reduction or
overlapping additional phase charts are **OPEN** obligations for global
coverage. No longer graph, spatial coarse-graining, continuum limit,
quantization, or mass-gap result follows from this two-square chart.

## 6. Evidence and reproduction

The general cometric, cotangent fiber, canonical closure and boundary claims
above have written derivations. They are not formal proof-assistant results.
The adjacent standard-library checker independently differentiates the full
seven-link loop words with exact rational quaternion arithmetic. It checks
the cometric, Gauss of the lifted momenta, kinetic equality, gauge covariance,
and source versus reduced second derivatives on its stated finite examples,
plus the singular circulation control. It also expands the determinant
identity exactly as a multivariate polynomial. These are finite executable
checks and a polynomial identity check, not numerical time simulations or a
claim of universal tool soundness.

```powershell
python -I -B research/ym2_spatial_joint/check_phase.py
```

The machine-readable receipt is [RESULTS_PHASE.json](RESULTS_PHASE.json).
The default command recomputes and compares that receipt without writing
files. Add `--write-results` only to explicitly replace the saved receipt.
This file supplies the regular Hamiltonian that the static note alone does
not claim; it preserves that note's distinct static and singular boundaries.
