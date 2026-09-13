# Independent review of the combined estimate and conditional gap

Date: 2026-09-12.

**Disposition: PASS as a written analytic chain on the declared finite-lattice carrier.** The exact source norm 4 and contracted bilinear constant 16/9 are compatible. The conditional-law extension supplies a positive full-space gap throughout the improved construction interval and, by finite-graph spectral continuity, at its endpoint. No load-bearing defect was found. This is mathematical review with one exact source-matrix audit, not proof-assistant certification, a simulation result, or a novelty claim.

Reviewed files:

- `SOURCE_NORM_REFINEMENT.md`, including its exact coefficient convention and matrix arithmetic;
- `SIGNED_AND_CONTRACTED_AUDIT.md`, SC1-SC13;
- `CONDITIONAL_GAP_EXTENSION.md`, CG1-CG13;
- the inherited norm, regularity and form-domain arguments in `accepted/DIRECT_COVER_ATTEMPT.md`;
- the full-vacuum exterior-support estimate in `accepted/CONDITIONAL_REFINEMENT.md`;
- the accepted bounded-tilt lemma C4 in `../ym2_connected_vacuum/accepted_sources/ym2_signed_differences/NEXT_CONNECTED_OBLIGATION.md`.

## 1. Exact source norm and representation compatibility

For the actual elementary word a=(1/2)Tr(U1 U2 U3^-1 U4^-1), the representation U1 tensor U2 tensor conjugate(U3) tensor conjugate(U4) gives the coefficient

```text
B=(1/2)sum_(a,b,c,d)|b,c,c,d><a,b,d,a|.
```

The inverse-link indices and reversal required by Tr(B pi) were checked directly. Writing v_bd=sum_c|b,c,c,d> and w_bd=sum_a|a,b,d,a>, both families have Gram matrix 2I4. Thus B=sum_bd|vhat_bd><what_bd| is a rank-four partial isometry. Its singular values are four ones and twelve zeros, so its trace norm is exactly 4.

The equivalent fundamental representatives are obtained by fixed unitary conjugations using SU(2) pseudoreality. These conjugations preserve the coefficient trace norm and consistently conjugate the derivative matrices. The accepted norm contains no extra dimension factor beyond the one already absorbed into B.

An exact integer/rational 16-by-16 audit verified both the direct monomial expansion and, for M=2B, the identities

```text
N=M^T M,          N^2=4N,          Tr N=16.
```

Hence B*B=N/4 is an orthogonal projection of rank four. The different all-positive word has a half-permutation coefficient of trace norm 8; partial inversion cannot be treated as an isometry of this nonabelian Fourier algebra. The actual positive-coordinate plaquette convention is essential and is the convention supplied here.

All plaquette blocks have kinetic eigenvalue 6. Cancellation of this eigenvalue against T^-1 in the anchored norm gives

```text
||T^-1 S||_* <= 4m,               m=2(d-1).
```

This uses an exact finite coefficient block of the source, not a spin cutoff of the full model.

## 2. Contracted bilinear estimate

For nonzero spins j,l, put a=min(j,l), b=max(j,l). The total-Casimir identity gives the contracted-generator eigenvalues

```text
omega_s=2[j(j+1)+l(l+1)-s(s+1)].
```

Their maximum absolute value is 4a(b+1), with normalized ratio

```text
||Omega_(j,l)||/(lambda_j lambda_l)=1/[b(a+1)].
```

This ratio is at most 2/3 outside the fundamental pair (j,l)=(1/2,1/2), and is 4/3 at that pair. The formula covers all higher spins analytically.

The exceptional-pair argument was checked without assuming positivity or separability of the coefficient matrices. On a normalized rank-one term of their separate singular-value decompositions, the coefficient vectors have the form xi=x tensor z and eta=y tensor w. Each of x,y,z,w may have arbitrary correlations among its own links. The irreducible product-group output projections P_L are complete and multiplicity free. Weighted Cauchy-Schwarz bounds the sum of projected trace norms by

```text
[<xi,|Omega_i|xi><eta,|Omega_i|eta>]^(1/2).
```

For two fundamentals, Omega_i=I-2F and |Omega_i|=2I-F. The reduction of x tensor z on the two factors at link i is rho tensor sigma, even if x and z are individually entangled with their other links. Therefore

```text
<xi,|Omega_i|xi>=2-Tr(rho sigma)<=2,
```

and the same bound holds for eta. Summing the separate singular-value expansions proves the local norm constant 2 for arbitrary complex input coefficient matrices. It equals (8/9)lambda_(1/2)^2. The higher-spin bound 2/3 is smaller than 8/9.

The two input-anchor contributions then each cost at most 8/9. Output support is contained in the union of the two input supports, derivatives require a shared link, and T^-1 cancels the output energy weight. Thus

```text
||B(u,v)||_* <= (16/9)||u||_*||v||_*.
```

Changing the side on which derivative generators multiply a coefficient matrix does not change its scalar projected block. Removing the mean or losing output support only removes terms from this positive norm bound. The infinite Fourier expansion follows by the same norm-continuity argument as the accepted proof.

The exact source coefficient is among the arbitrary matrices admitted by this estimate. No source-specific separability condition is needed. The two improvements therefore apply together in the same function space.

## 3. Combined fixed point and the earlier curvature bound

For t=|r|, the combined scalar bounds are

```text
||F_r(u)||_* <= 4mt+(8/9)R^2,
Lip(F_r on radius R) <= (16/9)R.
```

At R=1/4, the nonlinear contribution is 1/18 and the Lipschitz constant is 4/9. The self-map condition is 4mt<=7/36, or t<=7/(144m). The inherited Hessian and Bochner argument consequently gives gap>=1/2 on that closed interval.

The smaller scalar root is

```text
Y(t)=(9/16)[1-sqrt(1-128mt/9)],
0<=t<9/(128m).
```

The fixed point is constructed throughout that interval, with Y tending to 9/16. The earlier Ricci-based gap lower bound 1-2Y is positive only for t<5/(72m). At the latter endpoint Y=1/2 and the contraction factor remains 8/9. This is an exhaustion of that particular curvature lower bound, not evidence that the actual gap closes. The conditional comparison below supplies the stronger continuation requested here.

## 4. Actual conditional influences and correct matrix orientation

The conditional extension assumes the smooth actual vacuum with ||u||_*<=Y<3/4. Its conditional laws belong to dnu=psi_hat^2 dmu, rather than to an exponential polynomial approximation. Full Fourier support counting gives

```text
c_ij <= 2 sum_(J:i,j in supp J)||u_J||_A,
q=max_i sum_j c_ij <= 4Y/3 < 1.
```

These estimates remain valid at the larger supplied radius. Their proof uses absolute summability and lambda_J>=(3/2)|supp J|, not the earlier numerical substitution Y<=1/4.

For real continuous f and the exact conditional-expectation projection P_i,

```text
delta_i(P_i f)=0,
delta_j(P_i f)<=delta_j(f)+c_ij delta_i(f),     j!=i.
```

The cost of replacing the conditional law is TV times the oscillation of the integrand, with no extra factor two under the stated TV convention. The accepted bounded-tilt proof TV<=tanh(osc(log tilt)/4) was read and its chord-bound normalization checked.

For P=(1/N)sum_i P_i, the oscillation column vector therefore evolves under

```text
M=(1-1/N)I+C^T/N.
```

The transpose is correct: changing the exterior at j changes the update at i by c_ij. The induced l1 norm of C^T uses exactly the supplied row bound q of C, not an unprovided column bound. Positivity and the uniformly convergent Poisson expansion yield

```text
sum_j delta_j(exp(t L_hb)f)
  <= exp[-(1-q)t] sum_j delta_j(f),
L_hb=sum_i(P_i-I).
```

This calculation applies on the continuous compact product space because each actual conditional kernel preserves continuous functions.

## 5. Full heat-bath spectral inequality

Each P_i is an orthogonal conditional-expectation projection in L2(nu). Hence H_hb=sum_i(I-P_i) is bounded, self-adjoint, and nonnegative, even though its summands need not commute. Each link updates at rate one.

For a centered real continuous f, the oscillation estimate gives

```text
||exp(-tH_hb)f||_2 <= D_f exp[-(1-q)t]
```

with D_f finite on each fixed graph. The spectral measure argument is valid: any nonzero spectral mass in [0,a], a<1-q, would give a lower bound proportional to exp(-2at) for the squared L2 norm and contradict this decay as t grows. A countable exhaustion removes all mass in [0,1-q).

Centered real continuous functions are dense in centered real L2(nu); bounded spectral projections extend the zero-projection conclusion to that entire subspace. Complex functions follow by real and imaginary parts. Thus the possibly graph-dependent D_f does not enter the spectral constant. This proof requires neither a finite-state approximation nor compact resolvent for H_hb.

The result is the exact variance inequality

```text
Var_nu(f) <= [1/(1-q)] sum_i nu[Var_(nu_i)(f)].
```

It also rules out any additional centered zero modes. The conditional-variance identity follows directly from orthogonality of P_i.

## 6. Conditional gradient comparison and quantum normalization

At every fixed exterior, the conditional log-density oscillation satisfies

```text
D_i=osc_(U_i)(2u)<=4 sum_(J:i in supp J)||u_J||_A<=8Y/3.
```

The Haar gradient Poincare constant on the declared unit S3 is 1/3. For a positive conditional density p with minimum a and maximum b, comparison of the variance infimum and Dirichlet integral gives the conditional constant b/(3a)=exp(D_i)/3. There is one density-ratio factor, not its square. Conditional normalization changes neither D_i nor b/a.

Combining the conditional inequalities and integrating over exteriors gives

```text
Var_nu(f) <= exp(8Y/3)/[3(1-q)] integral |grad f|^2 dnu.
```

The actual density is smooth and strictly positive on each finite compact source, so smooth functions are dense in the full weighted H1 form domain. Multiplication by psi_hat identifies this domain with the full quantum form domain. Its exact energy normalization is

```text
q_(A-E)[psi_hat f]=(1/2)integral |grad f|^2 dnu.
```

Therefore

```text
gap(A(r)) >= (3/2)(1-4Y/3)exp(-8Y/3).                   (RV1)
```

At Y=0 this gives the correct full-link free gap 3/2, checking both the Haar constant and the quantum factor 1/2. For Y approaching 9/16, it remains at least (3/8)exp(-3/2)>0. The physical restriction is valid because the unique positive normalized actual vacuum is gauge invariant; no tensor factorization of the constrained space is assumed.

## 7. Closed endpoint and final scope

Let r_*=9/(128m). Every interior r<r_* has the common lower bound (3/8)exp(-3/2). For each fixed finite graph, A(r)-A(s)=-(r-s)S is bounded with norm at most N_p|r-s|. The first two ordered eigenvalues are therefore continuous by min-max. Taking r upward to r_* separately for each fixed graph retains the same gap lower bound. The continuity modulus may depend on that graph; the resulting lower bound does not. No interchange of an unproved thermodynamic limit is required.

Consequently the reviewed nonnegative-coupling statement is

```text
0<=r<=9/(128m)
    ==> gap(A(r)) >= (3/8)exp(-3/2)>0,
m=2(d-1),     d in {2,3}.                              (RV2)
```

No endpoint X_G fixed point or endpoint bound on ||u||_* is asserted by the continuity step. It proves the spectral statement directly. As before, a physical sector with no excited complement satisfies the projected form inequality vacuously rather than having an asserted excited eigenvalue.

This closes uniform finite-graph coverage on RV2 with full link spins, the declared elementary-plaquette family, and the fixed metric and lattice energy scale. It does not establish an infinite-volume representation, a continuum limit, a continuum physical mass gap, or the optimal coupling threshold. In particular, the conditional extension replaces an exhausted sufficient comparison; it does not diagnose a phase transition at either earlier endpoint.

No further refinement was attempted after this requested extension. No accepted old file, old checker, old receipt, simulation, package installation, or git state was changed. This review was recorded only in `COMBINED_REVIEW.md`.
