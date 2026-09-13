# Geometric overlap: shared charts, physical folds, and the actual YM form

12 September 2026. Written derivation at the existing finite-graph Yang–Mills contract. This note interprets the proposed squeezed 4×4 mango/grid picture through two distinct mathematical models. It does not assume that the picture has already selected one of them.

The useful exact construction is an overlapping two-component representation of one function. It preserves the full source and its norm. With ordinary componentwise differentiation it has an explicitly computable localization cost; with the derivative transported as well, it preserves the original energy exactly. A physical contact between previously distinct sites requires a separately supplied contact law. Section 7 separately audits a block-cover estimate that uses gauge constraints to improve a previously available lower bound.

## 1. Contract and source boundary

| Port | Admitted object or obligation |
|---|---|
| Source carrier | A finite open square or cubic lattice graph \(G\), with distinct elementary four-link plaquettes; \(Q_G=SU(2)^{E_G}\) with the product metric in which each factor is the unit round \(S^3\). |
| Equality | Points of \(Q_G\) have ordinary product equality. Hilbert-space functions are equal almost everywhere. Gauge equivalence is imposed by restricting to invariant functions, with the inherited form domain. |
| Existing operation | \(T=-\tfrac12\Delta\), \(A(r)=T-r\sum_p a_p\), \(a_p=\tfrac12\operatorname{Tr}U_p\), with generators \(i\sigma_k\). |
| Supplied measure | The **actual** normalized positive ground state \(\widehat\psi_G\) and \(d\nu=\widehat\psi_G^2d\mu\), where \(\mu\) is normalized product Haar measure. The following identities apply wherever that ground state and the inherited domain are supplied. |
| Receiver | Source reconstruction; \(L^2(\nu)\) norm; actual energy above the ground state; the entire mean-zero form domain if a gap is discussed. |
| Additional supplied ports | Real smooth gauge-invariant multipliers \(\chi_1,\chi_2\) satisfying \(\chi_1^2+\chi_2^2=1\). |
| Requested readout | Whether overlap creates additional independent states or improves the original Rayleigh quotient, and the exact cost of a nonconstant overlap. |
| Unfilled physical-fold ports | Which distinct material occurrences contact, their orientation, interaction law and strength, any changed incidence/metric, and the resulting Hamiltonian and domain. |

Write

\[
\mathcal H=L^2(Q_G,\nu),\qquad
\mathcal E(f)=\frac12\int_{Q_G}|\nabla f|^2\,d\nu.
\tag{GO1}
\]

The corresponding physical subspace is \(\mathcal H_{\rm inv}\). All statements below restrict to it when the multipliers are invariant. The accepted ground-state transformation is

\[
U f=\widehat\psi_G f,\qquad
q_{A(r)-E_G}[Uf]=\mathcal E(f),\qquad
\operatorname{Var}_{\nu}(f)=\|Uf\|^2-|\langle\widehat\psi_G,Uf\rangle|^2.
\tag{GO2}
\]

This is the previously derived form identity, not a product-vacuum approximation: [DIRECT_COVER_ATTEMPT.md, §6 and DC14](accepted/estimate/accepted/DIRECT_COVER_ATTEMPT.md), and [CONDITIONAL_GAP_EXTENSION.md, §5](accepted/estimate/CONDITIONAL_GAP_EXTENSION.md). The factor \(1/2\) is retained throughout. Returning to \(H=\alpha\hbar^2[A(r)+rN_p]\) multiplies all these energy identities by \(\alpha\hbar^2\).

## 2. Two kinds of overlap

### 2.1 Two charts describe the same source point

Let \(V_1,V_2\) cover a source manifold and let \(\varphi_i:V_i\to W_i\) be coordinate charts. On an overlap, the supplied transition is

\[
t_{21}=\varphi_2\circ\varphi_1^{-1}.
\]

Local scalar formulas \(f_i\) describe one global function exactly when

\[
f_1(z)=f_2(t_{21}(z))
\quad\text{on the shared domain}.
\tag{GO3}
\]

The duplicate chart addresses refer to one point. The compatibility condition is joint: independently selecting both chart values would introduce states absent from the source. The transition inverse, and the cocycle condition if more charts are introduced, retain which point is shared. Metric and measure must also be transported, including the appropriate coordinate Jacobian; a chart change cannot reset the energy tensor to an unrelated identity matrix.

The two-component construction below is a global representation of this duplication mechanism. It need not be a two-chart atlas of all of \(Q_G\): two genuine coordinate charts are not asserted to cover every product \(SU(2)^{E_G}\). It uses two overlapping **components** over a common source, optionally localized inside a separately supplied cover. This distinction prevents a local geometric picture from creating an unsupported global atlas claim.

The official source contract explicitly requires overlap maps, formula agreement, topology and coverage for geometric gluing: [core.md, §11](accepted/rprm/core.md). [Operations O03](accepted/rprm/operations.md#o03) proves rebracketing of fixed finite seam records with all witnesses retained. O03 does not itself prove a smooth gluing theorem or justify changing the next fit law during attachment.

### 2.2 A physical fold puts distinct source occurrences at the same location

For an exact model of a doubled footprint, start with the sheet \([0,4]^2\), divided into 16 labeled unit cells. The piecewise fold

\[
F(x,y)=(|x-2|,y,0)
\tag{GO4}
\]

has an eight-cell planar footprint with two layers away from the crease. It retains 16 material cell occurrences. Generic footprint points have the two source preimages \((2-u,y)\) and \((2+u,y)\); at the crease the two expressions coincide. Equal rendered positions do not imply equal field values on the two material occurrences. Retaining the side label recovers the source point; dropping it gives exactly the displayed preimage fiber.

Three further choices have different consequences:

1. If \(F\) is only a rendering and the original state, metric and Hamiltonian are retained, the fold changes the picture while preserving the existing dynamics.
2. If contact identifies the two source values, that is a new constraint and usually a quotient or restriction. It must say which occurrences are identified and whether their dynamics respects the identification.
3. If both values remain independent and contact couples them, a coupling law must be added. The existing sheet already had two occurrences; bending alone does not necessarily add degrees of freedom. Introducing new sheet or field variables would enlarge the carrier as well.

For example a prescribed contact term \(\kappa|v_L-v_R|^2\) has definite effects only after \(v_L,v_R,\kappa\), their units and kinetic terms are fixed. It is not implied by the contact drawing. In the existing lattice YM model, placing two drawn plaquettes on top of each other does not add a link, alter a plaquette holonomy, or alter the product metric. Changing those objects is a new explicit model contract.

Thus the proposed “double cells” can be exact as doubled **occurrences in a footprint**. Whether those occurrences are two descriptions of one point, two material sites, or two newly independent degrees of freedom is a load-bearing choice.

## 3. Exact overlapping embedding and its complete inverse structure

Define

\[
J:\mathcal H\longrightarrow\mathcal H\oplus\mathcal H,
\qquad Jf=(\chi_1f,\chi_2f).
\tag{GO5}
\]

Since the sum of the multiplier squares is one,

\[
\|Jf\|^2
=\int(\chi_1^2+\chi_2^2)|f|^2\,d\nu
=\|f\|^2.
\tag{GO6}
\]

Its adjoint, which is also its decoder on the reached image, is

\[
J^*(g_1,g_2)=\chi_1g_1+\chi_2g_2,
\qquad J^*J=I.
\tag{GO7}
\]

The exact compatibility carrier is

\[
\operatorname{Ran}J
=\{(g_1,g_2):\chi_2g_1-\chi_1g_2=0\ \nu\text{-a.e.}\}.
\tag{GO8}
\]

To verify sufficiency, set \(f=\chi_1g_1+\chi_2g_2\). Then
\(g_1-\chi_1f=\chi_2(\chi_2g_1-\chi_1g_2)=0\), and the second component follows in the same way. This proof also handles zeros of either multiplier without dividing by them. Consequently the complete inverse fiber of \(J\) is **ONE** \((J^*g)\) for compatible \(g\), and **NONE** for incompatible \(g\).

In contrast, the decoder on the unrestricted larger space has the complete fiber

\[
(J^*)^{-1}(f)
=\{Jf+(-\chi_2h,\chi_1h):h\in\mathcal H\}.
\tag{GO9}
\]

The orthogonal matrix with columns \((\chi_1,\chi_2)^T\) and \((-\chi_2,\chi_1)^T\) proves coverage of this family. It is **MANY** whenever \(\mathcal H\ne\{0\}\). The transverse \(h\) is the extra freedom produced by forgetting compatibility. One cannot count it as a physical excitation supplied by the original state.

## 4. The weighted IMS identity and the sign of the seam term

On \(\mathcal H\oplus\mathcal H\) let the componentwise form be

\[
\mathcal E_{\oplus}(g_1,g_2)=\mathcal E(g_1)+\mathcal E(g_2).
\]

For a complex-valued smooth \(f\), the product rule gives

\[
\sum_i|\nabla(\chi_i f)|^2
=\sum_i\chi_i^2|\nabla f|^2
+|f|^2\sum_i|\nabla\chi_i|^2
+2\operatorname{Re}\!\left(\overline f\,\nabla f\cdot\sum_i\chi_i\nabla\chi_i\right).
\]

The last sum vanishes because \(\sum_i\chi_i\nabla\chi_i=\tfrac12\nabla1=0\). Integrating against the **same actual** ground-state measure proves

\[
\boxed{\mathcal E_{\oplus}(Jf)
=\mathcal E(f)+\frac12\int\sum_{i=1}^2|\nabla\chi_i|^2|f|^2\,d\nu.}
\tag{GO10}
\]

No differentiation of the density is needed: this is a pointwise product-rule identity before integration. On each finite compact \(Q_G\), smooth multipliers and their derivatives are bounded, so multiplication is continuous on the inherited \(H^1\) form domain. Smooth approximation therefore extends GO10 to that entire domain, including its invariant part.

GO10 is the weighted Dirichlet-form version of the established **IMS localization formula**. A directly inspected author-hosted reference is Gerald Teschl, [*Mathematical Methods in Quantum Mechanics*, 2009 online edition, Lemma 11.3, printed p. 243](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf#page=255). That lemma gives the ordinary Laplacian identity for a smooth quadratic partition of unity. The weighted form specialization and its normalization are derived above; neither IMS nor the sum-of-squares isometry is a new theorem claimed by this note.

There are two equivalent ways to preserve the original energy receiver on the compatible image:

\[
\mathcal E_{\rm transported}(g)=\mathcal E(J^*g),
\qquad g\in\operatorname{Ran}J,
\tag{GO11}
\]

or, using GO10,

\[
\mathcal E_{\rm transported}(Jf)
=\mathcal E_{\oplus}(Jf)-\frac12\int\sum_i|\nabla\chi_i|^2|f|^2\,d\nu.
\tag{GO12}
\]

The localization term is nonnegative in the componentwise form, and is **subtracted** when a componentwise lower bound is transferred back to the original energy. It is a potential error to control, not an automatically earned improvement of the YM energy.

For the gap receiver, the exact transported vacuum is \(J1\), and

\[
\|Jf\|^2-|\langle J1,Jf\rangle|^2=\operatorname{Var}_{\nu}(f).
\tag{GO13}
\]

Variable multipliers generally do not send a globally mean-zero function to two individually mean-zero components: \(\int f\,d\nu=0\) need not imply \(\int\chi_i f\,d\nu=0\). Any proof that sums local gap estimates must also control these localized mean terms. Norm preservation alone does not discharge that obligation.

## 5. Half weights, a smooth bend, and an explicit YM evaluation

### Constant overlap

For \(\chi_1=\chi_2=1/\sqrt2\),

\[
Jf=(f/\sqrt2,f/\sqrt2),\qquad
\|Jf\|=\|f\|,\qquad
\mathcal E_{\oplus}(Jf)=\mathcal E(f).
\tag{GO14}
\]

Each component carries half of the squared norm and half of the energy. The amplitude is \(1/\sqrt2\), while the mass weight is \(1/2\). With weights \(1/2,1/2\) at the amplitude level, the unadjusted squared norm would instead be \(\|f\|^2/2\). Using literal copies \((f,f)\) doubles both squared norm and energy; the Rayleigh quotient is unchanged.

The half in this construction is a declared component mass share. It is distinct from the centered coordinates \(x-1/2\) or the balanced pair readout \(S-R=0\) recovered in [ZERO-AND-RAILS.md, “Centered half”](accepted/rprm/ZERO-AND-RAILS.md). A negative coordinate or a sign in one component does not supply negative norm or free energy.

### Nonconstant rotation of the two components

For a supplied smooth real function \(\theta\), set

\[
\chi_1=\cos\theta,\qquad \chi_2=\sin\theta.
\]

Then the precise “bend” identity is

\[
\sum_i|\nabla\chi_i|^2=|\nabla\theta|^2.
\tag{GO15}
\]

This rotates the two-component direction as the source changes. The sign of \(\sin\theta\) is allowed in a quadratic partition and does not change the sign of GO15. Such two global multipliers are not necessarily compactly supported chart cutoffs. A requested local cover must additionally supply subordinate supports and coverage.

If the derivative is transported with this rotation, the apparent cost disappears exactly. Let
\(R_\theta=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}\), so \(Jf=R_\theta(f,0)^T\). Define

\[
\nabla^{(\theta)}g=R_\theta\nabla(R_\theta^Tg).
\]

Then \(\nabla^{(\theta)}Jf=(\chi_1\nabla f,\chi_2\nabla f)\), and its form is exactly GO11. This is an explicitly transported representation of the existing derivative, not an additional physical YM gauge field.

The recovered Bishop-frame construction likewise retains bend functions and initial frame data to reconstruct a curve; it does not identify two bend amplitudes with a complete independent geometry: [CUBES-AND-PI-CURVES.md, §7](accepted/rprm/CUBES-AND-PI-CURVES.md). Its curve reconstruction and the component rotation here are different typed operations.

### An actual four-link plaquette coordinate

Choose any admitted elementary plaquette \(p\), and set

\[
\theta(U)=s\,a_p(U),\qquad s\in\mathbb R.
\]

Here \(s\) is an auxiliary dimensionless representation parameter, not the YM coupling \(r\). Because \(a_p\) is smooth and gauge invariant, both multipliers preserve the physical form domain. The accepted full link metric gives

\[
|\nabla a_p|^2=4(1-a_p^2),\qquad
Ta_p=6a_p,\qquad T(a_p^2)=16a_p^2-4.
\tag{GO16}
\]

The gradient coefficient is established for the actual links, not a substituted independent loop rotor: [PHASE_CLOSURE.md, §3](accepted/PHASE_CLOSURE.md). The two kinetic identities are retained in [REVIEW_PERTURBATION.md, §3](accepted/REVIEW_PERTURBATION.md). They also cross-check the normalization through

\[
T(a_p^2)=2a_pTa_p-|\nabla a_p|^2
=12a_p^2-4(1-a_p^2)=16a_p^2-4.
\]

Consequently the exact overlap cost is

\[
\mathcal E_{\oplus}(Jf)-\mathcal E(f)
=2s^2\int(1-a_p^2)|f|^2\,d\nu,
\qquad
0\le\mathcal E_{\oplus}(Jf)-\mathcal E(f)\le2s^2\|f\|^2.
\tag{GO17}
\]

This bound does not replace \(\nu\) by Haar measure and is uniform in the number of links for this one-plaquette multiplier choice. For several varying coordinates or cutoffs, their total gradient cost must be bounded explicitly; this single-coordinate estimate does not provide that broader bound.

For comparison, on a single unit-metric \(SU(2)\) rotor with scalar coordinate \(a=\tfrac12\operatorname{Tr}U\), the corresponding values are \(|\nabla a|^2=1-a^2\), \(Ta=\tfrac32a\), and \(T(a^2)=4a^2-1\). Four distinct differentiated links account for the factors in GO16. A single open link trace is not generally invariant under independent gauge actions at both endpoints; this auxiliary rotor calculation cannot silently replace the physical plaquette.

## 6. Distinguishing controls and evidence grade

| Control | Exact outcome | What it distinguishes |
|---|---|---|
| Same function in two components with weights \(1/\sqrt2\) | Identical norm, energy and Rayleigh quotient | Redundant descriptions do not create an extra coercive direction. |
| Independent transverse component \((-\chi_2h,\chi_1h)\) | Decoder returns zero; compatibility fails unless \(h=0\) | The unrestricted doubled carrier contains additional states. |
| Nonconstant \(\theta=s a_p\), source vacuum \(f=1\), \(s\ne0\) | Original energy is zero; componentwise energy is \(2s^2\int(1-a_p^2)d\nu>0\); GO12 subtracts it exactly | The localization cost cannot be counted as physical vacuum energy or a gap gain. Strict positivity follows from positive density and the nonempty open set \(\lvert a_p\rvert<1\). |
| Piecewise fold GO4 with two unequal values at paired material sites | Equal footprint location, two unequal retained source values | Physical contact does not supply chart compatibility. |
| A general localized gap argument | Local means and the summed gradient penalty must both be controlled | Overlap alone is insufficient to transfer a stronger lower bound. |

**Evidence grade:** written algebraic and form-domain proofs, using the exact previously accepted finite-graph YM identities. The sheet map is an explicit illustrative geometry. The IMS identity is established mathematics with an inspected reference. No old verification suites were rerun, and no claim of a newly executed numerical experiment or formal proof is made.

**Completed readout:** the compatible overlap representation is exactly reconstructible, and its norm and energy transport are solved by GO6–GO17. Constant overlap earns no improvement in the existing Rayleigh quotient; variable overlap carries the displayed localization and centering obligations. This does not rule out a sharper estimate from a useful, explicitly controlled overlapping decomposition.

**Open boundary for the geometric models:** a physical fold or a general cover-based gap theorem needs the additional contact or cover data and its estimates. Section 7 supplies those data for one specific forest-complement block cover. This note does not supply a continuum limit, a physical mass-gap theorem, or an unbounded new geometric law.

## 7. Independent audit of the forest-complement block cover

This is a separate estimate on the original YM form, proposed in the concurrent block-cover lane and checked here against the inherited conditional proof. It uses conditional expectations over groups of original links. Its gain does not follow from the redundant component embedding GO5.

Assume all vertex gauge transformations are imposed, with no boundary charges, and the actual invariant measure satisfies the inherited CG1 norm port
\[
\|\!u\!\|_*\le Y<3/4,\qquad
C_0=\frac{e^{8Y/3}}{3(1-4Y/3)}.
\tag{GO18}
\]

For a subset of links \(B\), put \(F=E_G\setminus B\) and let
\[
P_B f=\mathbb E_\nu[f\mid U_F],\qquad J_0f=\nu(f).
\]
Here \(J_0\) is the constant projection; it is distinct from the two-component embedding \(J\).

### Conditional expectation and the forest seam

Gauge transformations preserve \(\nu\) and preserve the sigma-algebra generated by \(U_F\). The defining integral property of conditional expectation therefore gives \(P_B V_g=V_gP_B\) for every gauge pullback \(V_g\). Thus \(P_Bf\) is invariant when \(f\) is invariant.

If the exterior subgraph \(F\) is a forest, its link assignments form one orbit of the full vertex gauge action. To see this, choose one root in each tree and choose its gauge matrix arbitrarily; recursively choose the gauge matrix at each child to send the connecting edge to identity. No cycle introduces a consistency obstruction. The residual root choices do not alter the conclusion that every forest assignment can be sent to the identity assignment.

It follows that every invariant function of \(U_F\) is constant. One can state this first for smooth functions and extend in \(L^2(\nu)\); alternatively the gauge-invariant marginal on forest assignments is the Haar probability on this transitive compact homogeneous space. Since conditional expectation preserves the global mean,
\[
\boxed{P_B=J_0\quad\hbox{on }\mathcal H_{\rm inv}
       \quad\hbox{whenever }E_G\setminus B\hbox{ is a forest}.}
\tag{GO19}
\]

This is an equality of the projections on the physical subspace, not on all of \(L^2(\nu)\).

### Why the same conditional Poincaré constant applies inside every block

Fix any exterior assignment \(x_F\). Smooth positivity of the full density supplies a smooth positive conditional law \(\nu_B(\cdot\mid x_F)\) on the full product of link rotors in \(B\). For each \(i\in B\), the single-site conditional law of this block measure is exactly the original law at site \(i\), with \(x_F\) fixed and the other block coordinates supplied.

Accordingly, its internal influence coefficients satisfy
\[
c^{B,x_F}_{ij}\le c_{ij}\quad(i,j\in B),\qquad
\max_{i\in B}\sum_{j\in B}c^{B,x_F}_{ij}\le4Y/3,
\]
and every one-site conditional log-density oscillation remains at most \(8Y/3\). The existing heat-bath and single-site comparison proof, [CONDITIONAL_GAP_EXTENSION.md, §§2–4](accepted/estimate/CONDITIONAL_GAP_EXTENSION.md), therefore applies with \(|B|\) sites and the same \(C_0\), uniformly in the fixed exterior. No bound on a newly expanded Fourier series of the conditional logarithm is required.

Integrating its conditional Poincaré inequality over the exterior gives
\[
\langle f,(I-P_B)f\rangle
\le C_0\int\sum_{e\in B}|\nabla_e f|^2\,d\nu.
\tag{GO20}
\]
This holds first for smooth functions and then on the full form domain by density. For an empty block, both sides vanish. The block conditional law need not itself be invariant under every original vertex gauge transformation; the conditional inequality is proved on the full block product, while GO19 uses equivariance of the original conditional-expectation operator.

### Directional forests and exact edge loads

On a finite open subgraph of the square or cubic lattice, let \(F_k\) contain all edges parallel to direction \(k\), and let \(B_k=E_G\setminus F_k\), for \(k=1,\ldots,d\). Each \(F_k\) is a disjoint union of paths and isolated vertices, hence a forest. Assign every block the weight \(w_k=1/(d-1)\). Each edge lies in exactly \(d-1\) of the blocks, giving the exact load
\[
\sum_{k:e\in B_k}w_k=1.
\]
Using GO19, the corresponding physical block operator is exactly
\[
\sum_{k=1}^d w_k(I-P_{B_k})
=\frac{d}{d-1}(I-J_0)
\quad\hbox{on }\mathcal H_{\rm inv}.
\tag{GO21}
\]
Summing GO20 with those weights yields
\[
\frac{d}{d-1}\operatorname{Var}_\nu(f)
\le C_0\int|\nabla f|^2\,d\nu.
\]
Thus the dimensionless physical energy form obeys
\[
\boxed{\mathcal E(f)\ge
\frac{d}{2(d-1)C_0}\operatorname{Var}_\nu(f),
\qquad f\in\mathcal H_{\rm inv}\cap H^1.}
\tag{GO22}
\]

The multiplicative improvement over the inherited full-product bound \(1/(2C_0)\) is \(3/2\) in three dimensions and \(2\) in two dimensions. The three three-dimensional blocks really overlap; the two two-dimensional blocks are disjoint. The mechanism is the exactly computed physical block operator together with unit edge load, so the gain cannot be attributed to overlap by itself. The physical Hamiltonian and its spectrum are unchanged; what improves is the certified lower bound.

**Audit result:** the argument is sound at the supplied finite-graph, all-vertex-invariant, smooth-positive-density and CG1 norm contract. It neither enlarges the interval in which the existing construction supplies \(Y\), nor improves the full ambient sector by GO21. Its endpoint extension, if used, must retain the existing fixed-graph spectral-continuity argument.

**Hostile boundaries:** freezing gauge transformations at boundary vertices can destroy forest transitivity; a periodic directional subgraph can contain cycles; arbitrary noninvariant functions need not have constant \(P_Bf\). Any of those changes invalidates the automatic GO19 step. If the entire graph is a forest, the physical subspace has only the vacuum line, so GO22 remains a valid form inequality with no nonzero physical excited complement. These are scope boundaries, not failures inside the stated contract.
