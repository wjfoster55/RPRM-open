# Independent review of the direct Fourier cover

Date: 2026-09-12.

Finalization note by the root reviewer: the normalized psi_hat clarification
below has been implemented in the delivered DC14. The final direct proof
also uses the exact ground-state form identity to identify the vacuum.
The original audit discussion is retained as the record of that correction;
the second direct-proof audit and final synthesis audit verify the revised
text.

Reviewed source: `research/ym2_covering_argument/DIRECT_COVER_ATTEMPT.md`, the full draft headed "Direct Fourier-norm construction and all-state gap bound", equations DC1-DC17.

**Disposition: PASS as a written analytic argument at the stated finite-lattice scope.** No load-bearing defect was found. The proof supplies a volume-uniform lower gap bound on the full, untruncated link Hilbert space, then on its all-vertex gauge-invariant subspace, for the explicit interval in DC1. This is an independent mathematical review, not a formal proof certificate or an empirical validation. One normalization notation should be made explicit, as recorded below; the surrounding prose already supplies the correct interpretation.

## Contract checked

The source is a finite product of full SU(2) link rotors with normalized Haar measure, at least one link, generators i sigma_k of unit length, and distinct elementary four-link plaquettes. The number of plaquettes incident to any link is bounded by m=2(d-1) for d=2 or 3. The operator is A(r)=-(1/2)Delta-r sum_p a_p, with 0<=r<=1/(48m). The receiver is the entire quadratic-form domain and the complete orthogonal complement of the exact ground state. No cut-off carrier or finite-spin approximation is used in the conclusion.

The proof introduces an explicit stronger function-space contract for log wavefunctions. That change is declared rather than silently inferred from an earlier L2 perturbative estimate. The dimension of each finite source may enter its smoothness and domain identifications. It does not enter the displayed contraction, Hessian, or final gap constants.

## 1. Coefficient norm and multiplication: DC2-DC3 pass

For a fixed finite graph, the nontrivial product irreducibles are countable and each coefficient matrix is finite dimensional. Peter-Weyl uniqueness makes the trace-coordinate convention well defined. Since lambda_J>=3/2 for J nontrivial,

    sum_(J!=0) b_J <= (2/3) sum_(J!=0) lambda_J b_J
                     <= (2/3)|E_G| ||u||_*.

Thus every coefficient sequence in X_G represents a uniformly convergent function. The weighted direct-sum argument in the draft proves completeness. The factor |E_G| in this fixed-graph equivalence is not used in the uniform bilinear estimate.

The multiplication proof is valid for general complex matrices, not merely positive ones. If W is the tensor coefficient in a unitarily decomposed representation, pinching onto its irreducible-type blocks satisfies

    sum_L ||P_L W P_L||_1 <= ||W||_1.

This follows by averaging unitary conjugations that remove off-diagonal blocks and then using the trace norm of a direct sum. On an isotypic block, partial trace over the multiplicity factor satisfies

    ||Tr_mult W_L||_1
      = sup_(||M||<=1) |Tr[W_L(I_mult tensor M)]|
      <= ||W_L||_1.

Combining this with ||B_J tensor C_K||_1=b_J c_K proves DC3 without a representation-dimension factor. At a link trivial in both inputs, the tensor product representation is trivial, so every output is trivial there. Output support is therefore a subset of the union of input supports. Cancellation of support can only remove output anchors; the proof never requires support equality.

The identification with the compact Fourier algebra is consistent with [Eymard's original paper](https://www.numdam.org/article/BSMF_1964__92__181_0.pdf). The finite-matrix argument above is sufficient for this proof and avoids needing a stronger external multiplication theorem.

## 2. Derivatives, inverse Laplacian, and anchored counting: DC4-DC5 pass

For spin j and a unit Lie-algebra direction, the generator has eigenvalues 2im, m=-j,...,j, and operator norm 2j. With lambda_(i,J)=2j_i(j_i+1),

    2j_i <= (2/3)lambda_(i,J),
    (2j_i)^2 <= 2lambda_(i,J).

The first inequality is sharp at j_i=1/2 and also valid at j_i=0. Differentiation preserves the multi-spin type and annihilates a component at every link where it is trivial.

For a nontrivial output L, the energy factor lambda_L in the anchored norm cancels the inverse eigenvalue from T^-1 exactly. The scalar output is discarded by Q before inversion. Thus no comparison between lambda_L and lambda_J+lambda_K is needed, and shrinking output support creates no small-denominator problem.

Fixing output anchor e, its indicator is at most the sum of the two input-anchor indicators. For the first contribution,

    sum_(K:i in supp K) (2j_i(K)) c_K
      <= (2/3) sum_(K:i in supp K) lambda_K c_K
      <= (2/3)||v||_*.

The three tangent directions give a factor 3. Summing the remaining derivative weights in J gives sum_i 2j_i(J)<=(2/3)lambda_J. Their combined factor is 3*(2/3)*(2/3)=4/3. The second anchor contribution gives another 4/3. Therefore the claimed bilinear constant 8/3 is correct. The differentiated link belongs to both input supports; no sum over all links is estimated by |E_G|.

The extension from finite Fourier sums is justified: X_G convergence controls each fixed-graph first derivative in the unweighted Fourier norm, and the displayed estimate makes the bilinear images Cauchy in X_G. Their limit agrees with the pointwise derivative product followed by the spectrally defined T^-1Q.

## 3. Source and contraction constants: DC6-DC10 pass

The four-matrix trace has 16 terms with coefficients 1/2. Each term is a coefficient on four distinct fundamental or dual-fundamental link representations. The norm bound 8 follows without identifying equal-valued but distinct links. Inversion changes the representation to the dual and does not change its coefficient norm or spin label. Every plaquette component has kinetic energy 4*(3/2)=6 and Haar mean zero.

Consequently the anchored inverse-source norm is bounded by 8 times the number of plaquettes incident to that anchor, proving 8m. The spatial graph may be open or have missing plaquettes; such omissions reduce incidence. Repeated plaquette occurrences would require a changed incidence bound, as the draft states.

On radius R=1/4, the nonlinear self-map bound is

    8mr+(4/3)R^2 <= 1/6+1/12 = 1/4,

and the Lipschitz constant is (8/3)R=2/3. Banach contraction therefore applies on the entire closed interval in DC1. The real subspace is closed and the map preserves it. Iteration from zero proves reality without requiring individual Fourier coefficient matrices to be real.

The scalar equation R=8mr+(4/3)R^2 has smaller root

    R_-=(3/8)(1-sqrt(1-128mr/3)).

Its strict interval and contraction factor in DC10 are correct. There is no claim of contraction at the discriminant-zero endpoint. The reported simpler DC1 endpoint lies strictly inside that interval.

## 4. Regularity, exact eigenfunction, and energy: DC11-DC12 pass

For each fixed finite graph, absolute summability of lambda_J b_J gives uniform convergence of all first derivatives. For any two individual tangent generators, the coefficient operator norm of their product is bounded by a constant times lambda_J: on the same link use (2j)^2<=2lambda_i, and on different links use 2ab<=a^2+b^2. Thus second derivatives converge uniformly too. In a finite smooth frame this establishes C2 regularity; noncommuting first derivatives introduce only controlled lower-order frame terms in coordinate charts.

The first-order derivative squares are C1, so the fixed-point PDE has a locally Holder right side. Schauder regularity first gives C^(2,alpha), then C^(3,alpha), and iteration gives smoothness. This is a fixed compact manifold without boundary, even though the spatial graph is open. No spatial boundary regularity assumption has been inserted.

Applying T to the fixed point yields

    Tu = rS + (1/2)|grad u|^2 - (1/2)integral |grad u|^2 dmu.

The scalar E in DC11 is therefore correct. The chain rule

    T(exp u) = exp(u)[Tu-(1/2)|grad u|^2]

proves DC12 exactly, including its energy shift and sign.

There is also a self-contained way to establish that this positive eigenfunction is the unique ground state. The transform in the next section, derived algebraically from its eigenfunction equation, gives a nonnegative form for A-E. Since exp(u) is an eigenfunction, E is the spectral bottom. Zero transformed form means grad f=0, hence f is constant on connected SU(2)^(E_G). This proves simplicity without importing a separate positivity theorem.

## 5. Metric and Hessian: DC13 passes

The declared metric has orthonormal Lie-algebra basis i sigma_k, bracket magnitude 2 for orthogonal basis vectors, and sectional curvature (1/4)||[X,Y]||^2=1 on each SU(2) factor. Thus each factor is the unit round S3 and has Ricci tensor 2g. The product Ricci tensor remains 2g independently of the number of factors.

At any point, extending v to a constant left-invariant field V gives nabla_V V=(1/2)[V,V]=0. Hence Hess u(v,v)=V^2u is valid for the diagonal quadratic form. It does not assert that every ordered second derivative is a Hessian entry.

In multi-spin J, the directional generator is bounded by sum_e 2j_e |v_e|. Weighted Cauchy-Schwarz gives

    (sum_e 2j_e |v_e|)^2
      <= lambda_J sum_(e in supp J) [(2j_e)^2/lambda_(e,J)]|v_e|^2
      <= 2lambda_J sum_(e in supp J)|v_e|^2.

Summing the absolute coefficients and exchanging nonnegative sums produces exactly 2||u||_*|v|^2. This includes vectors with components at arbitrarily many links of the finite graph. There is no omitted connection term or additional number-of-links factor.

## 6. Normalization and full spectral transfer: DC14-DC17 pass

For fully explicit notation set

    Z = integral exp(2u)dmu,
    psi_hat = exp(u)/sqrt(Z),
    dnu = psi_hat^2 dmu,
    Uf = psi_hat f.

Then U is unitary and the exact equations are

    U^-1(A-E)U = -(1/2)L,
    L = Delta+2 grad u dot grad,
    q_(A-E)[Uf] = (1/2) integral |grad f|^2 dnu.

**Notation clarification:** DC14 should use psi_hat in its quadratic-form left side. If its symbol psi still means the unnormalized exp(u), that one displayed equality requires a factor Z on its right side. The prose explicitly specifies the normalized multiplier and the final DC17 uses the normalized vacuum, so this is a removable notation ambiguity and does not change the argument or its constants.

The weighted potential in the convention dnu=e^(-w)dmu is w=-2u+log Z. Thus Ric_nu=Ric+Hess w=2g-2Hess u >= (2-4||u||_*)g. The sign agrees with the weighted Bochner identity; see [Wei and Wylie, *Comparison Geometry for the Smooth Metric Measure Spaces*, p. 3, equation (2.5), and p. 4, equation (3.2)](https://www.math.uchicago.edu/~shmuel/QuantCourse%20/Metric%20Space/comparison%20geo%20for%20smooth%20mm%20spaces.pdf).

Integration of that identity against nu gives integral(Lf)^2 >= kappa integral|grad f|^2. Applying this to each nonconstant eigenfunction of -L yields its eigenvalue at least kappa. Constants are exactly the zero eigenspace because the source is connected. Smooth positive density on a finite compact manifold gives compact resolvent, and the full eigenfunction expansion extends the inequality to the entire form domain. Complex functions are covered by real and imaginary parts.

This domain transfer is exact: psi_hat and its inverse are smooth and bounded on each finite compact source. Multiplication by them identifies the full H1 form domains. Their bounds may depend on the graph, but no such bound appears in the curvature or gap constant. Orthogonality to psi_hat corresponds precisely to zero nu mean.

Finally R<=1/4 gives kappa>=1; the factor 1/2 in the transformed Hamiltonian gives gap(A)>=1/2, exactly as in DC17. The broader bound 1-2R_->1/4 is also correct. Its nonsharp free value 1, compared with the true free gap 3/2, is consistent with retaining only the Ricci contribution.

Gauge transformations act by positive-measure-preserving isometries and commute with the operator. They preserve its unique positive normalized vacuum, so restriction to the reducing fixed subspace retains that vacuum and the same form inequality. This step does not assume that the constrained Hilbert space factors by links.

## Scope and verification record

The single-square hostile control has the stated exact moments and factors: integral a^2=1/4, integral a^3=0, N_exc a=4a, and Ta=6a. Its linear vacuum coupling correctly refutes the undressed excitation-number bound. The direct construction retains that coupling through its nonlinear vacuum equation.

The conclusion is a finite-lattice uniform inequality with explicit constants, all link spins, and the specified generator metric. It is not an infinite-volume GNS construction, a continuum limit, a result uniform in a continuum scaling trajectory, or a continuum mass-gap claim. These exclusions are actual coverage boundaries, not defects in the stated finite-lattice result.

This review checked the complete source argument and independently reconstructed the coefficient contractions, derivative constants, anchor counting, source bound, fixed-point radii, regularity passage, Hessian estimate, measure normalization, and spectral extension. The cited primary sources were checked for the applicable identities and attribution. No numerical test, simulation, spin truncation, package installation, or old repository verification suite was run. Only this review file was written for this audit.
