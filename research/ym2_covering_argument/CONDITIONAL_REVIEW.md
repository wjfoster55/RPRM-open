# Independent conditional-remainder review

Date: 2026-09-12.

**Disposition: PASS as a written finite-lattice argument, using the direct Fourier construction reviewed in DIRECT_COVER_REVIEW.md.** The refinement fills the actual remainder port CP8 on its stated small-coupling interval. It does not merely bound a polynomial substitute for the vacuum. No load-bearing correction is required.

Read together:

- `CONDITIONAL_REFINEMENT.md`, CR1-CR13;
- `DIRECT_COVER_ATTEMPT.md`, DC2-DC17;
- `../ym2_connected_vacuum/NEXT_CONDITIONAL_PORTS.md`, especially CP1, CP2, CP6 and CP8;
- `../ym2_connected_vacuum/CONNECTED_VACUUM.md`, CV12-CV14.

## Actual remainder estimate

Use m=2(d-1), t=8mr, b=4/3, and the smaller root Y of Y=t+bY^2. On 0<=r<=1/(48m), t<=1/6 and Y<=1/4.

Let s=rT^-1S, q=B(s,s)/2 and w=u-s-q, where u is the actual converged log-vacuum fixed point. Bilinearity gives exactly

    w = [B(u-s,u)+B(s,u-s)]/2.

The direct norm estimate implies

    ||u-s||_* <= Y-t,
    ||w||_* <= b(Y+t)(Y-t)
               = Y-t-bt^2 = W(t).

Thus CR5 bounds the actual remainder of a constructed function. It does not require identifying a formal series with a convergent series. Since t=Y(1-bY) and bY<=1/3, Y<=3t/2. Therefore W=b^2(Y+t)Y^2<=10t^3. At t=1/6 the values Y=1/4 and W=5/108 are correct.

## The old head matches exactly

The definition of F_head in CR3 is identical to CP2, including the coefficient -1/144 of a_p^2 and the connected-pair factor (4w_pq-3a_p a_q)/702. The support and orientation contract is the one declared in CV12.

With u1=S/6 and q=r^2 v2, the kinetic product rule yields

    v2 = T^-1Q(Su1) - Q(u1^2)/2.

The first term is the CV13 wavefunction coefficient. Subtracting the second gives the following exact coefficients:

| Term | Wavefunction coefficient | Subtraction | Surviving log-vacuum coefficient |
|---|---:|---:|---:|
| Centered self-square | 1/96 | 1/72 | -1/288 |
| Edge-disjoint unordered pair a_p a_q | 1/36 | 1/36 | 0 |
| Adjacent unordered pair a_p a_q | 1/39 | 1/36 | -1/468 |
| Adjacent outer loop w_pq | 1/351 | 0 | 1/351 |

The adjacent pair is exactly one half of C_pair. Consequently 2(s+q)=QF_head. Since log rho_G=2u-log integral exp(2u), the old remainder R_G is 2w plus a configuration-independent scalar. That scalar vanishes in the precise CP6 exterior-change oscillation. Haar-mean normalization of u and probability normalization of rho do not create an omitted second-order term.

## Complete exterior response and CP8

For each Fourier block of w, trivial representation at e means independence of U_e, and trivial representation at j means no response to replacing U_j. If both are present, the inside oscillation of its two-exterior difference is bounded by four sup norms. The factor 2 in R_G=2w+constant gives 8 times the coefficient trace norm.

Summing over every outside-link occurrence counts each block |supp J|-1 times. The all-spin inequality lambda_J>=(3/2)|supp J| gives

    sum_(j!=e) epsilon_ej
      <= 8 sum_(J:e in supp J)(|supp J|-1)||w_J||_A
      <= (16/3)||w||_*
      <= (16/3)W(8mr).

Uniform absolute Fourier convergence justifies all exterior suprema and termwise bounds. The support count includes blocks touching the entire finite graph and blocks generated at arbitrarily high order. No finite-range assertion about the true log vacuum is used. Smooth positive density defines the conditional law for every exterior, including exteriors lying in Haar-null sets.

This is the exact epsilon port in CP6 and CP8 on the original ambient product-link carrier. It is not a conditional law on an independently postulated product of gauge-invariant trace coordinates.

Combining with CP1 produces CR13. Its endpoint bound is

    sum_(j!=e)c_ej
      <= 1/48 + (m-1)/(16848m) + 5/81
      < 1/12,

because 1/12-1/48-5/81=1/1296 and (m-1)/(16848m)<1/16848=1/(13*1296). Thus eta(r)=(16/3)W(8mr) and theta=1/12 fill CP8 uniformly for d=2,3 on the stated interval. At r=0 both source and remainder vanish. The looser direct row estimate in CR12 is also valid.

The conditional inequality does not itself supply a Hamiltonian spectral gap. The separate direct proof supplies that conclusion through the ground-state transform and weighted Bochner identity. The refinement correctly keeps these two transfers distinct.

## Additional physical-convention spot check

Equation C8 of `COVERING_RESULT.md` agrees with the cited [primary Hamiltonian reference, D'Andrea et al., Phys. Rev. D 109, 074501, printed p. 074501-8, equations (56)-(57)](https://scoap3-prod-backend.s3.cern.ch/media/files/84451/10.1103/PhysRevD.109.074501.pdf). That page was read and visually inspected. For SU(2), Tr[2I-P-P^dagger]=4(1-a_p), giving magnetic coefficient 2/(g_b^2 a). With T=2 sum J_e^2, matching the electric coefficient g_b^2/(2a) gives E_el=g_b^2/(4a), hence r=8/g_b^4. The weak-bare-coupling direction therefore leaves the proved small-r interval. This check supports the stated convention only; it does not assert equality of coefficients across all conventions.

## Evidence boundary

The result closes the previously missing actual, graph-uniform conditional remainder at the written-proof level on finite open square/cubic graphs with distinct elementary plaquettes, all spins, and the declared metric. It does not close continuum or thermodynamic-limit obligations. The direct construction is an indispensable dependency, not something this remainder estimate independently proves.

No old checker, old receipt, simulation, or test suite was run or changed. No package was installed. Only this review file was written for this conditional audit.
