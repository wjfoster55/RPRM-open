# A joint that evolves, and one scaling law for its whole family

12 September 2026. Follow-up to YM2, requested by William to clarify field
geometry and test joint/scaling reuse. The original YM2 packet and exported
ZIP remain unchanged. This is a research note, not a paper.

**Positive result:** a joint matrix of pairwise relationships closes exactly
under the homogeneous classical SU(2) evolution. On the invariant domain
`rank[A v]≥2`, it defines a gauge-invariant retained description for the
declared periodic theory and preserves the entire magnetic-energy trajectory.
A single amplitude/time covariance law transports this result across every
positive scale in its declared family. It does not require a separately
derived law for each amplitude.

The construction uses ordinary Gram matrices and the accepted Yang–Mills
equations. It is a derived application here, not a claim of literature novelty,
minimal storage, faster computation, or spatial coarse-graining. The two
smaller summaries disproved by YM2 remain disproved.

## 1. What direction through geometry actually means

The coordinates are **field-component values**, not positions of a particle
in physical space. On YM2's diagonal slice, `q=(q₁,q₂,q₃)` gives three gauge
field amplitudes, and `p=dot q` gives how each amplitude changes. Magnetic
energy is the landscape

`W(q)=(q₁²q₂²+q₁²q₃²+q₂²q₃²)/2`

in `g=V=1` reference units. Electric energy fixes `|p|²/2`, and transfer is
`J=∇W·p`. Thus electric energy tells the total speed through field-value
space; transfer tells the component of that motion across magnetic-energy
contours. Neither alone specifies the entire direction.

At `q₀=(1,1,0)`, use orthogonal tangent directions

`e_u=(1,−1,0)/√2`, `e_w=(0,0,1)`.

The first grows one amplitude while shrinking another; the second starts
growing the absent third component. The **exact** two-dimensional section is

\[
 W(q_0+u e_u+w e_w)
 =\tfrac12-\tfrac12u^2+\tfrac18u^4+w^2+\tfrac12u^2w^2.
\tag{1}
\]

Both directions have zero initial slope, but the directional curvatures at
the origin are `−1` and `+2`. This is a saddle, despite the complete potential
being nonnegative. Nonnegative energy does not mean convex energy everywhere.

For `p(θ)=sinθ e_u+cosθ e_w`, all directions have the same
`(U_E,U_B,J)=(1/2,1/2,0)`, while

\[
 K(\theta)=p^T(\nabla^2W)p-|\nabla W|^2
 =-3\sin^2\theta.
\tag{2}
\]

The `−|∇W|²=−2` term is the same actual force response in every direction.
The landscape's `+2` directional curvature cancels it for direction A;
the mixed direction B does not cancel it. Hence A's initial magnetic-energy
acceleration is zero even though its straight direction probe bends uphill.
The actual field trajectory is accelerated by the full equations and is not
the straight probe drawn across the surface.

YM2's rational pair is `θ_A=0` and `cosθ_B=1/3`:
`p_A=(0,0,1)`, `p_B=(2/3,−2/3,1/3)`, giving `K_A=0`, `K_B=−8/3`.
The interactive illustration uses this landscape and integrates the actual
three-component equations separately for its future-energy plot. The plot is
a numerical illustration; equations (1)–(2) and YM2's unequal-derivative proof
are exact.

## 2. Define the joint before discarding its internal relationships

Use the original homogeneous variables with `A` a 3×3 matrix whose columns
are the color vectors `A_i`, and `v` likewise. Fix `g>0`, `V=L³>0`, the same
periodic SU(2) gauge convention, and the same forward magnetic-energy receiver
as YM2. The source equations are

\[
 \dot A=v,\qquad \dot v=-AC,\qquad
 C=g^2\bigl((\operatorname{tr}S)I-S\bigr),\quad S=A^TA.
\tag{3}
\]

This follows from the accepted force
`f_i=g²Σ_{j≠i}(|A_j|²A_i−(A_i·A_j)A_j)` by collecting its columns.

Retain all three blocks together:

\[
 S=A^TA,\qquad T=A^Tv,\qquad U=v^Tv,\qquad
 G=\begin{pmatrix}S&T\\T^T&U\end{pmatrix}.
\tag{4}
\]

They record field–field relationships, field–electric relationships, and
electric–electric relationships. Their off-diagonal entries retain alignments
that a few energy totals discard. This is one joint Gram matrix, not three
independently selectable marginal tables.

Matrix rank, PSD and factorization statements use numerical components in
fixed reference units `ℓ₀`. Physically `S`, `T`, `U` have units `ℓ⁻²`, `ℓ⁻³`,
`ℓ⁻⁴`, respectively; the two source column types are not interchangeable.
Equivalently form the dimensionless Gram matrix of `[ℓ₀ A, ℓ₀² v]` before
testing PSD. This is a positive diagonal congruence of the displayed numerical
matrix and preserves its rank and positivity; no field is added to a velocity.

The admitted reached image is

\[
 G\succeq0,\qquad 2\le\operatorname{rank}G\le3,\qquad G\Omega G=0,
 \quad\Omega=\begin{pmatrix}0&I\\-I&0\end{pmatrix}.
\tag{5}
\]

These are joint compatibility conditions, not optional annotations. PSD and
rank produce a real factor `Z=[A v]` with `G=ZᵀZ`. Gauss is
`Avᵀ−vAᵀ=ZΩZᵀ=0`. To see equivalence with the last equation in (5), set
`M=ZΩZᵀ`. Then `GΩG=ZᵀMZ`. The latter being zero makes the bilinear form
of `M` vanish on `range Z`; `M` maps into that range and vanishes on its
orthogonal complement. Hence `M=0`, also at deficient rank. Conversely,
Gauss immediately gives `GΩG=0`. This proves sufficiency as well as necessity.

An instructive hostile case is `A=diag(1,2,3)`, `v=AB`, where
`B₁₂=B₂₁=1` and its other entries vanish. Gauss holds, but `T₁₂=1` and
`T₂₁=4`. **Gauss is not the condition that T be symmetric.** Replacing the
actual joint constraint by that shortcut would exclude valid interacting data
and can also admit invalid data; both directions are checked.

For a bounded operational request, retain initial finite `H_max`, a bound
`||A(0)||≤A_max`, a finite horizon and, when used, `0<λ_min≤λ≤λ_max<∞`.
The velocity and finite-time coordinate bounds from YM2 apply. Scaling changes
these caps: `H→λ⁴H`, `||A||→λ||A||`. We do not pretend every scaled state
remains inside the original YM2 cap of five. The visual uses base energy one,
`λ∈[1/2,2]`, and normalized time through 0.4, hence physical energy at most
16 and physical time at most 0.8 in reference units. Exact checker controls
have their separately stated finite states and scales.

## 3. Written closure proof

The product rule applied to (3) gives

\[
 \boxed{\dot S=T+T^T,\qquad
 \dot T=U-SC,\qquad
 \dot U=-CT-T^TC.}
\tag{6}
\]

Every right side is a polynomial in the retained joint. No new unretained
derivative appears. The observables are obtained directly:

\[
 U_E=\frac V2\operatorname{tr}U,\qquad
 U_B=\frac{Vg^2}{4}\left((\operatorname{tr}S)^2-\operatorname{tr}(S^2)\right),
 \qquad J=V\operatorname{tr}(CT).
\tag{7}
\]

For any admitted initial `G`, factor it into a constrained source using (5)
and evolve that source. Its Gram matrix obeys (6), providing existence and
preserving the reached image. Polynomial ODE uniqueness makes this Gram
trajectory independent of the selected factor. The source's energy and
finite-time bounds give global continuation for finite times. Therefore

`G(Φ_t x)=Ψ_t(G(x))`, and `U_B(Φ_t x)` is the readout (7) of `Ψ_t(G(x))`.

The retained update composes by addition of time and has inverse `Ψ_{−t}`
on its reached image. This proves preservation for all admitted finite time
continuations, not merely equality through the first few derivatives.

For comparison to YM2's first repair, differentiation of (7) also gives

\[
 K=V\left[g^2\{2(\operatorname{tr}T)^2-\operatorname{tr}(T^2)
 -\operatorname{tr}(T^TT)\}
 +\operatorname{tr}(CU)-\operatorname{tr}(SC^2)\right].
\tag{8}
\]

The bigger joint contains precisely the sorts of interaction contractions
the scalar summaries lost. Equation (6), rather than an indefinitely extended
list of such contractions, supplies the closure argument.

## 4. Physical equality, complete fibers and a gauge boundary

Equal Gram matrices have the complete representative fiber

`{R Z₀ : R∈O(3)}`.

Proof: map each column of one factor to the corresponding column of the
other. Equality of Gram matrices preserves squared norms of every linear
combination, so the map is well defined and isometric on the column span.
Extend it orthogonally to all of `R³`. This proves coverage, not just a list
of examples. At rank three the fiber has two `SO(3)` orbits; at rank two it
has one, since reflection on the unused orthogonal direction can change the
extension's determinant without changing any columns.

We must still account for the **full periodic gauge equality**, not only
constant rotations. On the admitted domain `rank Z≥2`, any smooth gauge
map taking homogeneous initial fields to homogeneous initial fields is
constant. Here is a direct proof:

- If `rank A≥2`, choose independent `A_i,A_j`. The spatially constant, gauge-covariant color
  vectors `F_ij`, `D_iF_ij`, `D_jF_ij` span color space: they are proportional
  to `b=A_i×A_j`, `A_i×b`, and `A_j×b`.
- If `rank v≥2`, two independent electric fields and their cross product
  supply a constant frame.
- In the remaining rank-two case, write `A_i=a_i n`, `v_j=b_j m`, with
  independent `n,m`. Choose any indices with `a_i b_j≠0`. Then `E_j=b_j m`
  and `D_iE_j=g a_i b_j n×m` are independent, and their cross product completes
  a constant frame. These indices need not coincide.

Gauge covariance sends each fixed frame to a fixed target frame, forcing
`Ad U(x)` to be spatially constant. The kernel of the adjoint map is the
discrete center; smoothness on the connected torus forces `U` to be constant.

This domain is invariant even if `A` becomes singular or magnetic energy
passes through zero. Indeed

\[
 \dot Z=Z\begin{pmatrix}0&-C\\I&0\end{pmatrix},
\tag{9}
\]

whose right fundamental matrix is invertible, preserving joint rank. Thus
all genuinely interacting initial fields (`U_B>0`) remain in the domain
where the gauge argument works. The checker includes the singular-potential
state `A=0,v=I`, which has joint rank three and is covered by (6).

Consequently the complete **physical** source fiber is `ONE` at joint rank
two and `MANY(two mirror branches)` at rank three. The latter are not generally
gauge copies. For example, at `A=v=I`, a common improper color reflection
changes the sign of the gauge-invariant pseudoscalar `Σ E_i·B_i`. Its magnetic
energy trajectory remains identical by the homogeneous O(3) symmetry. The
joint is therefore receiver-sufficient while omitting a physically meaningful
orientation that a stronger receiver could request.

Bare Gram data do not descend on the entire jointly commuting rank-one
periodic sector: constant Cartan representatives can be shifted by periodic
gauge transformations, changing `AᵀA`. This is why (5) explicitly excludes
that sector. It is not needed for the interacting theorem. Jointly collinear
`A,v` have `U_B(t)=0` identically and could be handled by a separate commuting
receiver tag, but a full source/holonomy classification there is not claimed.

## 5. Define scaling once, then reuse its transport law

For dimensionless `λ>0` at **fixed** `g,L,V`, define

\[
 A_\lambda(t)=\lambda A(\lambda t),\qquad
 v_\lambda(t)=\lambda^2v(\lambda t).
\tag{10}
\]

The force is cubic in `A`. Differentiating the first expression gives the
second; differentiating the second gives `λ³ dot v(λt)`, exactly the force
of `λA(λt)`. Gauss scales by `λ³` and remains zero. This proves, once for
the whole supplied family,

\[
 \Phi_t D_\lambda=D_\lambda\Phi_{\lambda t},\qquad
 D_\mu D_\lambda=D_{\mu\lambda}.
\tag{11}
\]

On the joint, the weights are `S→λ²S`, `T→λ³T`, `U→λ⁴U`, and

\[
 U_{B,\lambda}(t)=\lambda^4U_B(\lambda t),\qquad
 H_\lambda=\lambda^4H.
\tag{12}
\]

Transfer, acceleration and the third derivative have weights five, six and
seven. These powers are forced by the equations, not chosen independently at
each level. Doubling field-potential amplitude means quadrupling the electric
velocity amplitude, multiplying energy by sixteen, and running the same shape
twice as fast. Scaling every component by the same factor would generally be
a different, invalid dynamical transport. Scaling only one spatial amplitude
also fails this universal rule; an exact anisotropic countercontrol is included.

For `H>0`, choose a fixed reference energy `H_*` in the same units and retain
`λ=(H/H_*)^(1/4)`. Divide `S,T,U` by `λ²,λ³,λ⁴`, and use the clock
`τ=λt`. The normalized joint obeys the same equations at energy `H_*`.
One normalized solution therefore serves its entire scale orbit, provided
the scale and clock conversion remain available. A numerical trajectory still
needs sufficient duration/resolution for each requested query; a proof of the
transport is not a claim that computing its seed costs nothing.

Different normalized joint matrices describe different shapes. They do not
share a trajectory merely because their normalized total energies agree.

At zero energy the normalization is undefined. Such states have `v=0` and
commuting `A`, so they lie outside the interacting rank domain and need their
own static branch. Physical horizons and carrier caps also travel with (11):
to answer `t≤T` for `λ≤λ_max`, normalized evolution may be needed through
`λ_max T`. No performance advantage has been measured.

## 6. Size, the AD/SAT similarity and what remains open

The full joint stores 21 real entries: six in symmetric `S`, nine in `T`,
and six in symmetric `U`. That exceeds the original eighteen coordinates.
Its regular constrained intrinsic dimension is twelve, matching conventional
gauge-reduced mechanics. This is a closed relational description, not a
demonstrated storage compression.

Where `A` is invertible, a local twelve-entry chart does exist: write `v=AB`.
Gauss forces `B=Bᵀ`; retain symmetric positive-definite `S` and symmetric `B`.
Then `T=SB`, `U=BSB`, and

`dot S=BS+SB`, `dot B=−B²−C`.

That chart fails when `A` becomes singular, while the full Gram system remains
regular. For example `A=0,v=I` is valid source data, but `A⁻¹v` is undefined.
No globally minimal coordinate system is claimed. Separating eleven normalized
shape coordinates from one energy scale also leaves twelve generic degrees of
freedom for one state. The concrete advantage established here is **family
reuse**, not fewer degrees of freedom in an individual source.

William's AD/SAT comparison has a precise useful reading: prove that a rule
preserves the stated question for a defined family and allowed operations,
then reuse that rule for further members after checking its premises. In the
accepted AD1 specimen, a conditional rule could survive a qualifying source
change while the old numeric answer still needed replacement. Here the joint
update and scaling law survive every qualifying scale change while energy
values and the clock transform. The original Absolute Distinction idea is
broader than that specimen or this realization.

The accepted SAT02 record supports local structure-preserving replacement and
recovery within its supplied promise, with partial research status. It does
not establish a universal solver or full work-budget guarantee. We use that
as an analogy about **a proved family and a retained interface**, not as a
mathematical equivalence between SAT and Yang–Mills. Those accepted sources
were read, not rerun or changed.

The next issue changes depending on what “scaling” means:

1. **Amplitude scale within this homogeneous model:** the exact transport
   law above is proved. It works for a whole scale family without a new law
   at each amplitude.
2. **Joining spatial regions or changing resolution:** the missing obligation
   is to define an interface retaining enough cross-region information that
   spatial derivatives, interaction terms and Gauss still yield a closed
   update. Internal Gram data of separated pieces cannot simply be multiplied
   as independent marginals. Relative color orientation requires a declared
   connection/transport between locations; a local dot product across locations
   is not automatically gauge invariant. No spatial gluing theorem is proved.
3. **Quantum/continuum scaling:** a quantum construction and limiting spectral
   estimate are additional structures, not consequences of (10). The mass-gap
   question remains open in this work; this is a positive classical closure
   and scale-reuse result, not a negative mass-gap conclusion.

The reusable content is now concrete: a joint representation, its exact image
constraints, its update, its complete Gram-map source fibers on the admitted
domain, and a commuting scaling law. Extending the family requires proving the new interface and operations
meet those same obligations, not re-labeling an unchecked case as already solved.

## 7. Evidence and source locations

`check_joint.py` uses exact `Fraction` arithmetic and an independent source
vector recurrence versus the closed Gram recurrence. Full rows are in
`RESULTS.json`. It includes old separating states as regression examples for
the new joint, non-diagonal Gauss data, a rank crossing, improper reflection,
three rational scales, coupling/volume controls and hostile shortcuts. This is
new-joint verification, not a rerun of accepted YM1 or the old YM2 campaign.
The general statement is supplied by the written proof, not inferred from the
finite examples. Independent bounded mathematical review is retained in
`INDEPENDENT_REVIEW.md`.

Source laws: [YM2 model and derivation](../ym2_interacting_energy_transfer/MODEL_AND_DERIVATION.md),
and the inherited action in [Tong, chapter 2, pp.29–31](https://davidtong.org/pdfs/teaching/gauge-theory/gauge2.pdf).
The Gram closure, rank/gauge argument and scale transport above are derived
here using ordinary matrix algebra; no claim of first discovery is made.

Accepted analogy sources, consulted without activating those lanes:
[AD1 design](../rprm-consolidation-c2-20260912/ad/AD1_DESIGN.md),
[AD1 result](../rprm-consolidation-c2-20260912/ad/AD1_RESULT.md), and
[SAT02 accepted status](../ym2_interacting_energy_transfer/supplied/CODEX_YM2/sources/accepted/SAT02_M1_CLOSEOUT.md).
The modern-web accessibility guidance was read from an already cached package;
no installation or update was performed.
