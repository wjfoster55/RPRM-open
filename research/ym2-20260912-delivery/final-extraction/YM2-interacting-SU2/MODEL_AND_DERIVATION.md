# YM2: interacting SU(2) energy-transfer research

Date: 12 September 2026. Publication remains on hold.

**Result.** On an exact, constrained homogeneous sector of classical pure SU(2),
`R3=(U_E,U_B,J)`, with `J=dU_B/dt`, does not determine the future magnetic-energy
trajectory. Adding the physically defined acceleration `K=d²U_B/dt²` repairs
the first exhibited distinction but also fails the future receiver. Two exact
counterexamples and a complete *conditioned* momentum-circle fiber expose the
missing curvature and cubic interaction contractions.

These are written derivations in this run, independently calibrated with exact
rational calculations. They are not formal proofs checked by a proof assistant,
a claim of literature novelty, or quantum spectral results. The physical model
is established Yang–Mills mechanics. YM1 remains accepted starting evidence;
its checker was not rerun. See [SOURCES.md](SOURCES.md) for precise source locations.

## 1. Contract and scope

| Item | Declared contract |
|---|---|
| Theory | Classical pure SU(2), real time, no matter, no mass term, natural units `c=ℏ=1` |
| Space | Cubic torus of fixed side `L>0`, volume `V=L³`, trivial SU(2) bundle, smooth strictly periodic fields and gauge maps |
| Representatives | Temporal gauge `A_0=0`; three spatially constant color vectors `A_i(t)∈R³`, with velocities `v_i=dot A_i` |
| Constraint | `G=Σ_i A_i×Π_i=0`, where the integrated canonical momenta are `Π_i=V v_i` |
| Physical equality | Full time-independent strictly periodic SU(2) gauge equivalence, restricted to homogeneous initial representatives; no quotient by time reversal or spatial rotations |
| Parameters | `g,L,V`, units and gauge/boundary convention stay fixed when comparing states |
| Supplied ports | An attained exact summary `R3` (or `R4=(R3,K)`) and a positive elapsed time `t` |
| Missing port / receiver | `Q_t([A,v])=U_B(Φ_t[A,v])`, for every admitted `t` in a fixed finite horizon |
| Operation | Deterministic Hamiltonian flow `Φ_t`; full-state inverse `Φ_{−t}` exists; a summary inverse/update is not assumed |
| Evidence | Written equations and counterexample proofs; exact finite replay; small explicitly nonrigorous trajectory illustration |

The homogeneous carrier before quotient is 18 real coordinates `(A,v)`, with
three Gauss constraints. On regular orbits, reduction by three color gauge
directions leaves 12 physical phase-space dimensions. Singular orbits need not
have this dimension; no uniform coordinate chart is claimed. The diagonal
six-coordinate invariant slice below is used to exhibit witnesses, not as a
gauge fixing or a parametrization of every homogeneous solution. The receiver
claim being tested remains the one on the full homogeneous constraint surface.

For the explicit examples choose a reference length `ℓ₀`, `L=ℓ₀`, `g=1`, and
`E_max=5/ℓ₀`. All displayed numbers use `A` in `ℓ₀⁻¹`, `v` in `ℓ₀⁻²`, and
time in `ℓ₀`. Admit initial representatives with `||A(0)||≤3/ℓ₀` and
`H≤E_max`, and inspect `0≤t≤ℓ₀`. All witnesses lie strictly inside these
initial bounds. This is a continuous carrier, not a finite enumeration.

**A finite energy cap is not a coordinate cap.** Commuting flat directions
allow arbitrarily large `A` with zero magnetic energy. Instead, positivity of
the Hamiltonian gives

\[
 \|v(t)\|\le\sqrt{2E_{\max}/V},\qquad
 \|A(t)\|\le\|A(0)\|+\sqrt{2E_{\max}/V}\,|t|.
\]

Thus this operational horizon is enclosed by
`||A||≤(3+√10)/ℓ₀` and `||v||≤√10/ℓ₀²`. The initial coordinate cap is a
representative-based selection, not a new gauge-invariant observable or a
reflecting boundary. We use the full smooth flow during the horizon, without
stopping it when it leaves the initial cap. Repeated forward updates can be
admitted with a retained elapsed clock and total elapsed time at most `ℓ₀`;
enabledness is identical for both members of every tested fiber. Polynomial
local existence plus the displayed finite-time bounds excludes finite-time
blowup, so the homogeneous flow in fact exists for every finite real time.

## 2. Action, normalization and constraints

Use Hermitian `T_a=σ_a/2`,
`[T_a,T_b]=i ε_abc T_c`, `tr(T_aT_b)=δ_ab/2`, and Minkowski signature `+---`.
Write `A_μ=A_μ^a T_a` and

\[
 F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu-ig[A_\mu,A_\nu],
 \qquad S=-\frac14\int F^a_{\mu\nu}F^{a\mu\nu}\,dt\,d^3x.
\tag{1}
\]

This is the coupling-inside-curvature convention obtained by the explicit
rescaling in [Tong, chapter 2, pp.29–30](https://davidtong.org/pdfs/teaching/gauge-theory/gauge2.pdf).
Define `E_i=F_{0i}` and `B_i=ε_ijk F_jk/2`. In temporal gauge, `E_i=v_i`.
This declared electric-sign convention differs from the spatial-vector
convention used in YM1; `U_E` and the definition `J=dot U_B` are unambiguous.

The homogeneous magnetic fields and density are

\[
 B_1=gA_2\times A_3,\quad B_2=gA_3\times A_1,\quad B_3=gA_1\times A_2,
 \qquad W(A)=\frac{g^2}{2}\sum_{i<j}|A_i\times A_j|^2.
\tag{2}
\]

Substitution and spatial integration, with no fitted term, give

\[
 L_{\rm hom}=V\left(\frac12\sum_i|v_i|^2-W(A)\right),\quad
 \Pi_i=Vv_i,\quad H=\sum_i\frac{|\Pi_i|^2}{2V}+VW(A)=U_E+U_B.
\tag{3}
\]

Let `f=∇_A W`. The identity
`|a×b|²=|a|²|b|²−(a·b)²` gives componentwise

\[
 f_i=g^2\sum_{j\ne i}\bigl(|A_j|^2A_i-(A_i\cdot A_j)A_j\bigr),\qquad
 \dot A_i=v_i,\quad\dot v_i=-f_i.
\tag{4}
\]

The canonical Poisson bracket has `{A_i^a,Π_j^b}=δ_ijδ_ab`, or
`{A_i^a,v_j^b}=δ_ijδ_ab/V`. Equation (4) therefore also follows from (3).
Do not call `v` canonical momentum except when the displayed numerical `V=1`
has already been adopted.

One must vary `A_0` before discarding it. In the homogeneous Lagrangian before
temporal gauge, `F_0i=dot A_i+g A_0×A_i`. Its `A_0` equation is
`Σ_i A_i×v_i=0`, equivalently `G=0`. The spatial covariant-divergence Gauss
law is exactly this condition. Preservation is direct:

\[
 \dot G=V\sum_i(v_i\times v_i-A_i\times f_i)=0.
\tag{5}
\]

Indeed `A_i×f_i=−g²Σ_{j≠i}(A_i·A_j)A_i×A_j`, whose unordered pair terms
cancel. Conservation is not the same as satisfaction: nonzero Gauss data
would remain nonzero and are not admitted physical initial data. Also

\[
 \dot H=V\sum_i(v_i\cdot(-f_i)+f_i\cdot v_i)=0.
\tag{6}
\]

This is an **exact invariant ansatz for classical initial data**. Spatial
derivatives vanish, and the nonlinear remaining terms in the full field
equations stay spatially constant. Equations (4) and (5) supply every field
equation for these initial data. Products of zero Fourier modes do not generate
nonzero modes. This is not a strong-coupling approximation, a claim that generic
inhomogeneous fields approach this sector, or a quantum truncation theorem.
The existence of homogeneous Yang–Mills mechanics is inherited from prior
work, including [Pavel, p.1, equations (1)–(4)](https://arxiv.org/pdf/hep-th/0701283).

For comparison with volume-absorbed literature coordinates, set
`Q=√V A`, `P=√V v`. Then `H=|P|²/2+(g²/(2V))Σ|Q_i×Q_j|²` and `P=dot Q`.
No volume factor has been absorbed without declaration. In our original
coordinates `[g]=1`, `[A]=ℓ⁻¹`, `[v]=ℓ⁻²`, `[Π]=ℓ`, `[W]=ℓ⁻⁴`,
`[U_E]=[U_B]=ℓ⁻¹`, `[J]=ℓ⁻²`, `[K]=ℓ⁻³`, `[dot K]=ℓ⁻⁴`.
There is no fixed Maxwell wave number in this homogeneous interacting sector.

## 3. Gauge and torus issues

For our convention,
`A_i^U=U A_i U⁻¹−(i/g)(∂_i U)U⁻¹`. Temporal gauge preserves time-independent
strictly periodic `U(x)`. Constant transformations induce a simultaneous proper
color rotation of **both** `A_i` and `v_i`; they preserve cross products, all
energies, and the flow. The exact checker transports all six witness states
with a rational proper rotation and checks the resulting non-diagonal fields.

Constant rotations are not a complete classification of periodic gauge
equivalence. In commuting sectors, coordinate-dependent periodic gauge maps can
relate constant Cartan potentials. For example, a strictly periodic
`exp(4π i x T_3/L)` shifts the corresponding constant `A_x` by
`4π T_3/(gL)` in this convention. The map with `2π` is periodic only up to
the center and is outside the strictly periodic convention chosen here.
Not every periodic shift is topologically large: see
[van Baal, pp.260–261, §1](https://www.lorentz.leidenuniv.nl/research/vanbaal/DECEASED/HOME/JOUR/NPB369_259.pdf).
We need no global gauge-fixing theorem or fundamental-domain construction.

A trivial bundle is not trivial holonomy. A straight cycle at fixed transverse
coordinates has `Hol_i=exp(igLA_i)` for a homogeneous representative, with trace
invariant under strictly periodic gauge transformations. We retain these
representatives and do not set their holonomies to the identity. Within each
separating pair below the initial `A` is identical, hence their initial spatial
holonomies are identical as well. Their electric data differ.

Although a general gauge transform can leave the homogeneous form, energies
and their full dynamical derivatives are gauge invariant. If two homogeneous
initial representatives are gauge equivalent, gauge covariance and uniqueness
make their full solutions gauge equivalent; all `Q_t` agree. Thus a differing
`K` or `dot K` rules out **all** admitted gauge identifications, not just
constant rotations. Spatial axes are retained as part of the setup. Continuous
index-rotation symmetry of the mechanical expression does not enlarge the
cubic torus's geometric symmetry group and is not declared gauge.

## 4. Test the summary before numerical evolution

Treat the nine components of `A` as ordinary Euclidean coordinates. Let
`M=∇²W` and `N=∇³W`. Differentiating (3) using (4) gives

\[
 J=\{U_B,H\}=V f\cdot v,\qquad \dot U_E=-J,\qquad\dot U_B=J,
\tag{7}
\]
\[
 K=\dot J=V\bigl(v^{\mathsf T}Mv-f\cdot f\bigr).
\tag{8}
\]

The first two summary derivatives factor through `R3`. The third needs the
velocity-curvature contraction and force norm. A symbol for `K` does not prove
it is determined by `R3`; section 5 supplies an exact refutation.

An independent field expression makes the interaction content visible. Put
`C_ij=A_i×A_j`, `D_ij=v_i×A_j+A_i×v_j`, and
`E_ij=−f_i×A_j−A_i×f_j+2v_i×v_j`. Then

\[
 J=Vg^2\sum_{i<j}C_{ij}\cdot D_{ij},\qquad
 K=Vg^2\sum_{i<j}(|D_{ij}|^2+C_{ij}\cdot E_{ij}).
\tag{9}
\]

These follow just by differentiating `U_B=Vg²Σ|C_ij|²/2` twice, separately
from the Hessian calculation. The vector-series checker computes the full
ODE with nested cross products and then substitutes into (2), without calling
the Hessian formulas. Both routes agree exactly on the displayed data.

## 5. Exact separating pair for R3

Choose the invariant diagonal slice
`A_1=q_1 e_1, A_2=q_2 e_2, A_3=q_3 e_3`, and similarly `v_i=p_i e_i`.
Orthogonality makes each force parallel to its original color axis, so the
slice stays invariant. Gauss is zero term by term. At `g=V=1`,

\[
 W(q)=\tfrac12(q_1^2q_2^2+q_1^2q_3^2+q_2^2q_3^2),\qquad
 \ddot q_i=-q_i\sum_{j\ne i}q_j^2.
\tag{10}
\]

Here `p=dot q` is the diagonal velocity. The restricted gradient and Hessian are
`f_i=q_iΣ_{j≠i}q_j²`, `M_ii=Σ_{j≠i}q_j²`, `M_ij=2q_iq_j` for `i≠j`.

| State | q | p | U_E | U_B | J | K |
|---|---|---|---:|---:|---:|---:|
| A | (1,1,0) | (0,0,1) | 1/2 | 1/2 | 0 | 0 |
| B | (1,1,0) | (2/3,−2/3,1/3) | 1/2 | 1/2 | 0 | −8/3 |

For this common `q`,

\[
 f=(1,1,0),\qquad
 M=\begin{pmatrix}1&2&0\\2&1&0\\0&0&2\end{pmatrix},\qquad |f|^2=2.
\]

Both velocities have norm one and `f·p=0`. However, `p_AᵀMp_A=2` and
`p_BᵀMp_B=−2/3`. Thus (8) gives the two exact values in the table.
`A_1×A_2=e_3`, so the non-Abelian magnetic interaction and magnetic energy are
strictly positive. The other two commutators initially vanish; this does not
make the sector Abelian. In fact the third component starts moving and becomes
coupled. Both electric energies are positive as well.

Let `b_A(t),b_B(t)` be the actual magnetic energies. Equal values and first
derivatives but unequal second derivatives imply

\[
 b_A(t)-b_B(t)=\frac43 t^2+o(t^2).
\tag{11}
\]

Therefore there exists `δ>0` such that `b_A(t)>b_B(t)` for every `0<t<δ`.
This follows from the definition of the nonzero limit of the difference
divided by `t²`; it is not an approximate numerical collision. Polynomial ODEs
give analytic solutions near the initial states, more regularity than needed.
Since such times are admitted in the common operational horizon, no decoder
of `R3` can give the whole future magnetic-energy receiver on this carrier.

**Mechanism.** `J=0` says the velocity is momentarily tangent to an
equal-magnetic-energy surface. It does not tell how that surface bends in the
chosen direction. At this `q`, the Hessian has eigenvalues `3,−1,2` along
`(1,1,0)`, `(1,−1,0)`, and `(0,0,1)`. State A moves along the third direction;
state B has a substantial component along the negative-curvature direction.
Their force term is identical. The lost term is exactly their different
velocity orientation relative to this interaction curvature. A nonnegative
quartic potential need not have a positive-semidefinite Hessian everywhere.

## 6. One justified refinement, and its exact failure

Retain the actual gauge-invariant acceleration `K=dot J`; call the new
description `R4=(U_E,U_B,J,K)`. This adds one scalar of units `ℓ⁻³`, and no
energy term or changed equation of motion. It separates A and B and determines
the second-order local magnetic-energy jet `U_B+Jt+Kt²/2` exactly as Taylor
data. It supplies no uniform Taylor-remainder bound merely by being retained.

The next derivative follows by the product rule, including both force terms:

\[
 \dot K=V\bigl(N[v,v,v]-4v^{\mathsf T}Mf\bigr)=:\mathcal L.
\tag{12}
\]

In detail, differentiating `vᵀMv` contributes `N[v,v,v]−2vᵀMf`, and
differentiating `−f·f` contributes another `−2vᵀMf`. On the diagonal slice,

\[
 N[p,p,p]=6g^2\sum_{i<j}(q_i p_i p_j^2+q_j p_j p_i^2).
\tag{13}
\]

This is an interaction contraction derived from the same potential. It is not
an invented observable chosen from the eventual future answer.

| State | q | p | (U_E,U_B,J,K) | 𝓛=U_B''' |
|---|---|---|---|---:|
| + | (1,1,1) | (1,1,−2) | (3,3/2,0,−12) | 36 |
| − | (1,1,1) | (−1,−1,2) | (3,3/2,0,−12) | −36 |

Now **all three** `A_i×A_j` are nonzero. Here `f=(2,2,2)` and
`M=2·11ᵀ`. Since `Σp_i=0`, both `pᵀMp` and `pᵀMf` vanish. But
`N[p,p,p]=−6Σp_i³=−18p_1p_2p_3` on this plane, giving `±36`. Consequently

\[
 b_+(t)-b_-(t)=12t^3+o(t^3),
\tag{14}
\]

which is positive for every sufficiently small positive time. This refutes
future closure of `R4`, not merely a proposed formula for its update.
The initially equal `q_i` do **not** remain equal: the velocities are unequal.
We did not replace the model by an equal-amplitude symmetric orbit.

The transformation `p→−p` is time reversal. It relates past to future, whereas
the receiver supplies the same forward time to both states. It is not a
gauge identification. Magnetic energy and `K` are even under this reversal;
`J` is odd but is zero here. The next odd derivative survives and distinguishes
the futures. All initial spatial holonomies still agree.

As a control outside equal initial amplitudes, take `q=(1,2,0)` and
`p_±=±(1,−2,0)`. Both give `(U_E,U_B,J,K)=(5/2,2,0,−28)` but
`𝓛_±=±48`. The exact checker includes both. This is a second check of the
same refinement, not another repair or a new research campaign.

### A complete conditioned fiber, not just two points

With the **additional supplied source condition** `q=(1,1,1)` in this
diagonal slice, the complete momentum fiber for
`R4=(3,3/2,0,−12)` is the circle

\[
 p_1+p_2+p_3=0,\qquad p_1^2+p_2^2+p_3^2=6,
\]
\[
 p(\theta)=2\bigl(\cos\theta,\cos(\theta-2\pi/3),
                         \cos(\theta+2\pi/3)\bigr),\quad
 \theta\in\mathbb R/(2\pi\mathbb Z).
\tag{15}
\]

Necessity comes from `U_E=3` and `J=2Σp_i=0`. These two conditions force
`pᵀMp=0`, so `K=−12` automatically. Conversely every vector on this circle
obeys all four supplied values and Gauss. The cosine/sine coefficient vectors
form an orthogonal equal-length basis of the plane, proving the parametrization
covers the whole circle. With this fixed full-rank `A`, curvature spans all
three color directions; a gauge transformation preserving this `A` must act
trivially in the adjoint and cannot identify different momenta on the circle.

The entire next-derivative image is also explicit:

\[
 \mathcal L(\theta)=-18p_1p_2p_3=-36\cos(3\theta),\qquad
 \mathcal L\text{ ranges over }[-36,36].
\tag{16}
\]

Thus `MANY(circle)` is justified for this *conditioned* source aperture, and
`MANY([-36,36])` for its next-derivative aperture. Neither statement is a
claimed complete fiber of `R4` over all homogeneous gauge fields. For that
larger fiber we have certified distinct members and have not solved the full
inverse problem. Its complete parametrization remains OPEN.

### The next mathematical obligation

The four-coordinate refinement has derived partial update equations
`dot R4=(−J,J,K,𝓛)`, but its last entry is not a function of `R4`. Any further
candidate summary supporting the same forward receiver must at least separate
states with different `𝓛`, including the continuum (16), and must prove
preservation under its own subsequent derivatives and enabled continuations.
It may use a better joint invariant description instead of a derivative list.
This task stops after the one tested refinement. Whether retaining `𝓛` itself,
or another finite collection of interaction invariants, yields a closed useful
description has not been proved or disproved here. No infinite hierarchy is
claimed necessary; no globally minimal representation is claimed.

The conventional full `(A,Π)` constrained state already provides a constructive
update by (4), and the diagonal `(q,p)` state provides it on its own invariant
slice. That is the fallback reopening information, not a compressed discovery.
Three or four scalars are smaller than these conventional states, but real
coordinate counts are not a proof of bit cost, minimality, or impossibility of
a different encoding. Retaining only `R3` or `R4` leaves actual source ambiguity;
retaining the source permits recomputation. Missing source files would instead
be an evidence-availability problem, not an empty mathematical fiber.

## 7. Controls and executable evidence

The commuting control has `A_i=a_i n`, `v_i=b_i n` for one fixed color unit
vector `n`. Every commutator and force vanishes, Gauss is zero, and
`A_i(t)=(a_i+b_i t)n`, `U_B=J=K=0`, with constant `U_E`. The checker uses
`a=(1,2,3)`, `b=(1,−1,2)` as a separate control contract, not the bounded witness
enclosure of section 1. Unlike YM1's nonzero-frequency Maxwell mode, this
homogeneous commuting sector has no spatial curl or restoring oscillator term.

Requiring only initially commuting `A` is insufficient for that control:
`q=(1,0,0)`, `p=(0,1,0)` has `U_B(0)=0`, Gauss zero, but
`U_B(t)=t²/2+O(t⁴)`. Its initially electric second component creates a nonzero
commutator. The invariant simpler sector needs the jointly aligned `A` and `v`.

`check_ym2.py` runs six exact source rows, all six consistently rotated copies,
an independent full color-vector Taylor recurrence through degree six,
conservation checks through all completely known coefficients, a changed
`g=2,V=3` normalization control, commuting and initially-flat controls, circle
samples, and a generic off-Gauss identity control explicitly marked inadmissible.
The latter tests conservation of Gauss without confusing it with Gauss being zero.

The ordinary Taylor coefficients follow from the ODE recurrence, and direct
substitution gives

\[
 b_A(t)=\tfrac12-\tfrac56t^4+O(t^6),\quad
 b_B(t)=\tfrac12-\tfrac43t^2+\tfrac{71}{54}t^4+O(t^6),
\]
\[
 b_\pm(t)=\tfrac32-6t^2\pm6t^3+\tfrac{33}{2}t^4
                       \mp\tfrac{33}{5}t^5+O(t^6).
\tag{17}
\]

Independent reviewer calculations used a scalar diagonal recurrence rather
than the author's vector recurrence; see [review/INDEPENDENT_MATH.md](review/INDEPENDENT_MATH.md).
Those are independent implementations, not independent experimental samples.

An optional RK4 illustration uses four trajectories to `t=0.01ℓ₀`, with
100 and 200 steps each: 1,200 steps total, not a campaign. The declared
absolute diagnostic tolerance is `10⁻¹⁰` for step comparison and energy drift.
Gauss is structurally zero in this diagonal numerical representation; that
check alone is not a test of arbitrary constrained numerical integration.
All full output rows, exact coefficients, tolerances, and measured errors are
in [RESULTS.json](RESULTS.json). The written unequal-derivative argument proves
separation for sufficiently small positive times. Numeric checks neither
certify an explicit interval radius `δ` nor prove a global error bound.

## 8. What travels back to RPRM

The source laws, carriers and gauge meanings remain the ordinary Yang–Mills
ones. RPRM's question is which relationships survive a retained description and
remain usable for a continuation. Here the failure is precise: electric energy,
magnetic energy, and transfer lose an interaction-curvature distinction, and
the first repair still loses an odd cubic interaction distinction.

A seam here is relative to this observation and operation. No seam substance,
seam-energy charge, new physical law or mass term was introduced. Prestige One
continues to include acquired usable relationship/access, retained construction
and a route to reopen when a stronger operation requires it. A scalar summary,
a proof certificate, a file hash, and this narrow realization do not replace
that broader source meaning. Other recovered concepts and their open seams
are preserved in the supplied packet without activating other lanes.

This is a completed negative sufficiency result with a completed bounded repair
test. It is useful because it identifies exactly why YM1's successful signed
transfer repair does not carry over automatically. It does not prove that
interacting physics has no useful reduced description. The separate quantum
ambition and its remaining bridge are stated in [PROBLEM_BRIDGE.md](PROBLEM_BRIDGE.md).
