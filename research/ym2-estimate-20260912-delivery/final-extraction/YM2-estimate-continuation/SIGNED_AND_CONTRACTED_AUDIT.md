# Contracted-gradient improvement and signed-coupling audit

12 September 2026. A new written estimate continuing
[the accepted direct covering argument](accepted/DIRECT_COVER_ATTEMPT.md),
especially (DC2)--(DC5). The accepted packet is unchanged. No spin cutoff,
old verification suite, theorem-checker execution, installation, or
publication is used here.

**Result.** In exactly the Fourier norm and finite-graph carrier of that
argument, the bilinear constant improves from `8/3` to `16/9`:

```text
||T^-1 Q sum_(i,k) (D_(i,k)u)(D_(i,k)v)||_*
    <= (16/9) ||u||_* ||v||_*.                           (SC1)
```

The improvement uses the tensor-product structure of the two input
coefficients before irreducible pinching. Contracting the generators and
then retaining only the operator norm would not improve the uniform
constant: two fundamental spins saturate that weaker estimate. Keeping
their singlet and triplet weights gives the improvement proved below.
No gauge restriction or presumed cancellation between different input
blocks is needed.

With the unchanged source bound `||T^-1 S||_* <= 8m`, the closed interval

```text
|r| <= 7/(288m)  ==>  gap(T-rS) >= 1/2                  (SC2)
```

follows by the accepted ground-state and Bochner continuation. For
nonnegative `r`, this enlarges `1/(48m)=6/(288m)` by a factor `7/6`.
This is a sufficient bound; the optimal bilinear constant and optimal
coupling interval are not determined.

## 1. Contract and retained dependencies

- **Carrier and equality:** a finite open square or cubic lattice graph,
  `Q_G=SU(2)^(E_G)` with product normalized Haar measure, the full
  Peter--Weyl expansion, and almost-everywhere equality. The unit round
  three-sphere metric and generators `i sigma_k` are unchanged.
- **Supplied ports:** `u,v` in the mean-zero space `X_G` of (DC2), with
  `u_J=Tr(B_J pi_J)`, `v_K=Tr(C_K pi_K)`, `b_J=||B_J||_1`,
  `d_K=||C_K||_1`, and `lambda_(i,J)=2j_i(j_i+1)`.
- **Operation and direction:** contract the three derivative directions
  at a shared link, multiply the coefficient functions, remove their Haar
  mean, and invert `T` on the nonzero isotypic blocks.
- **Receiver:** the same anchored energy norm, followed by the same
  lower bound on the full orthogonal complement of the actual ground
  state. All spins and arbitrary coefficient matrices are included.
- **Inverse and fiber:** `T^-1` is the already defined inverse on
  mean-zero blocks. This estimate does not enumerate the interacting
  spectral fiber or define an inverse to coefficient multiplication.
- **Coverage and evidence:** the proof covers every half-integral pair
  by a fundamental-pair argument and a bound for every other pair.
  Evidence is a written derivation, with exact hostile cases below.
  The continuum and infinite-volume obligations retain their earlier
  open status.

The fixed-point regularity, positive-vacuum construction, form-domain
transfer, and weighted Bochner proof are reused at their accepted scope.
Only the load-bearing replacement for (DC5) and its scalar consequences
are developed here.

## 2. Contracting first: exact spin-channel eigenvalues

At a single shared link, write

```text
A_(j,k)=d pi_j(i sigma_k),
Omega_(j,l)=sum_(k=1)^3 A_(j,k) tensor A_(l,k).
```

The standard angular-momentum addition rule is

```text
V_j tensor V_l = direct_sum_(s=|j-l|,...,j+l) V_s,
```

with each summand occurring once. The Casimir identity follows by
expanding `sum_k(A_(j,k) tensor I+I tensor A_(l,k))^2` and using
`sum_k A_(j,k)^2=-4j(j+1)I`. Therefore, on the spin-`s` channel,

```text
Omega_(j,l) = omega_s I,
omega_s = 2[j(j+1)+l(l+1)-s(s+1)].                       (SC3)
```

This is the ordinary addition-of-angular-momentum identity; the
[graduate lecture notes, section 15.2](https://etneil.github.io/grad_qm_lec_notes/addition_J.html#addition-of-angular-momentum)
give the total-Casimir identity and the admitted spin range. The displayed
factor of two is derived here from this packet's generator normalization.

Put `a=min(j,l)` and `b=max(j,l)`. The extreme channel eigenvalues are

```text
omega_(b-a)=4a(b+1),        omega_(a+b)=-4ab,
||Omega_(j,l)||_op=4a(b+1).
```

For `j,l>0`, this yields

```text
||Omega_(j,l)||_op / (lambda_j lambda_l)
    = 1/[b(a+1)].                                      (SC4)
```

The maximum is `4/3` at `j=l=1/2`. For every other pair of nonzero
half-integral spins, either `a=1/2,b>=1`, or `a>=1,b>=1`, so the ratio
is at most `2/3`. If either spin is zero, the contracted derivative
vanishes.

Thus the contracted operator norm alone has the same uniform `4/3`
energy-normalized constant used per anchor side in (DC5). The exceptional
fundamental pair must be handled before discarding input structure.

## 3. Pinching retains a useful constraint on the fundamental pair

Fix multi-spins `J,K` and a shared link `i`. Reorder the representation
factors only for the calculation, and let `P_L` be the orthogonal
projections of `pi_J tensor pi_K` onto its irreducible product-group
summands. These summands have multiplicity one: at each link the
two-spin decomposition above has multiplicity one, and the full group
is the product of the link groups. In particular,

```text
Omega_i P_L = omega_(i,L) P_L.
```

For one input pair the contracted-gradient coefficient before pinching
is `(B_J tensor C_K) Omega_i`, with the side of multiplication depending
on the derivative convention. Its diagonal block is always

```text
omega_(i,L) P_L(B_J tensor C_K)P_L.                     (SC5)
```

The sum of the trace norms of these blocks is the Fourier norm of the
contracted-gradient function. Keeping any subset of output blocks can
only lower this sum, including when an anchor or `Q` removes blocks.

First take normalized rank-one coefficient matrices

```text
B_J=|x><y|,      C_K=|z><w|,
xi=x tensor z,  eta=y tensor w.
```

The vectors `x,y` may be entangled among the links of `J`, and `z,w`
may be entangled among those of `K`. Only the product between the two
input sides is used. The rank-one trace norm and Cauchy--Schwarz give

```text
sum_L |omega_(i,L)| ||P_L xi|| ||P_L eta||
 <= [sum_L |omega_(i,L)| ||P_L xi||^2]^(1/2)
    [sum_L |omega_(i,L)| ||P_L eta||^2]^(1/2)
 = [<xi,|Omega_i|xi><eta,|Omega_i|eta>]^(1/2).             (SC6)
```

Suppose now `j_i=l_i=1/2`. Let `F` swap just the two fundamental factors
at link `i`, acting as the identity on all other factors. The Pauli
identity `sum_k sigma_k tensor sigma_k=2F-I` gives

```text
Omega_i=I-2F=3P_singlet-P_triplet,
|Omega_i|=2I-F=I+2P_singlet.                             (SC7)
```

For the product vector `xi=x tensor z`, let `rho` and `sigma` be the
reduced density matrices at link `i` of `x` and `z`. They are positive
matrices of trace one even if the vectors have correlations with their
other links. The reduction on the two factors together is exactly
`rho tensor sigma`, hence the swap identity gives

```text
<xi,F xi>=Tr(rho sigma)>=0,
<xi,|Omega_i|xi>=2-Tr(rho sigma)<=2.                      (SC8)
```

Here `Tr(rho sigma)>=0` follows by writing it as
`Tr(rho^(1/2) sigma rho^(1/2))`. The same calculation applies to `eta`.
Equations (SC5)--(SC8) prove a Fourier norm bound of `2` for normalized
rank-one inputs.

For general complex coefficient matrices, take singular-value
decompositions of `B_J` and `C_K` separately. Apply the rank-one bound
to each product of singular terms and sum their nonnegative singular
values. Their sums are `b_J` and `d_K`, so

```text
||sum_k (D_(i,k)u_J)(D_(i,k)v_K)||_A <= 2 b_J d_K
  = (8/9)lambda_(i,J)lambda_(i,K)b_J d_K
                 when j_i=l_i=1/2.                    (SC9)
```

No positivity or separability is assumed of `B_J` or `C_K` themselves.
The product rank-one vectors arise in their separate singular-value
expansions. This is why arbitrary matrices and intra-input correlations
are covered.

For every other nonzero spin pair, ordinary trace-norm pinching and
(SC4) give a bound with coefficient `2/3`, which is smaller than `8/9`.
The uniform conclusion for every link and every pair is therefore

```text
||sum_k (D_(i,k)u_J)(D_(i,k)v_K)||_A
 <= (8/9)lambda_(i,J)lambda_(i,K)b_J d_K.                (SC10)
```

## 4. Anchored summation and the infinite expansion

Fix an output anchor `e`. Every reached output support is contained in
`supp J union supp K`, and differentiation at `i` requires that both
input supports contain `i`. The output energy cancels against `T^-1`
as in (DC5). Use the safe indicator bound

```text
1_(e in supp L) <= 1_(e in supp J)+1_(e in supp K).
```

For the first input-anchor indicator, (SC10) gives

```text
(8/9) sum_(J:e in supp J) b_J
      sum_i lambda_(i,J)
      sum_(K:i in supp K) lambda_(i,K)d_K
 <= (8/9)||v||_* sum_(J:e in supp J) lambda_J b_J
 <= (8/9)||u||_*||v||_*.
```

The second indicator contributes the same upper bound with the input
roles reversed. Taking the maximum over `e` proves (SC1) for finite
Fourier sums. The two sides are continuous under finite-sum approximation
in `X_G`, so the bilinear map extends with the same bound to all of
`X_G`. As in the accepted proof, the absolutely convergent first
derivative expansions identify the extended map with the displayed
derivative product followed by `T^-1 Q`.

Support loss and negative channel eigenvalues are preserved up to the
explicit norm estimate. No singlet component is mistaken for a
nontrivial representation on its original link. The two-input-anchor
overcount remains, so no optimality of `16/9` is asserted.

## 5. Fixed-point consequences and the sign of the coupling

Write `t=|r|`, retaining the accepted source bound `8m`. For

```text
F_r(u)=rT^-1 S+(1/2)B(u,u),
```

the radius-`R` ball obeys

```text
||F_r(u)||_* <= 8mt+(8/9)R^2,
||F_r(u)-F_r(v)||_* <= (16/9)R ||u-v||_* .               (SC11)
```

At `R=1/4`, the nonlinear contribution is `1/18` and the contraction
multiplier is `4/9`. The ball is invariant when

```text
8mt <= 1/4-1/18=7/36,
t <= 7/(288m).
```

The fixed point is real and gauge invariant for every real `r` in this
interval, including negative `r`. The unchanged positive-vacuum and
Bochner arguments yield

```text
<phi,(T-rS-E)phi>
 >= (1/2)[||phi||_2^2-|<psi_hat,phi>|^2]
```

for every vector in the full form domain. The restriction to the gauge
invariant subspace has exactly the same qualification concerning a
nonzero excited complement as the accepted result. This proves (SC2).

More generally the smaller scalar root is

```text
R_-(t)=(9/16)[1-sqrt(1-256mt/9)],
||u||_*<=R_-(t),          0<=t<9/(256m).                 (SC12)
```

Its contraction multiplier is strictly below one on the displayed open
interval. The inherited Bochner estimate is `gap>=1-2R_-(t)` wherever
this expression is positive, namely

```text
0<=t<5/(144m).                                          (SC13)
```

The contraction interval and the positive-Bochner-bound interval are
different. At the limit `t=9/(256m)`, the scalar radius would be `9/16`,
which exceeds `1/2`; no positive gap follows from that limiting radius.
Equation (SC13) is a pointwise positive lower bound in `t`, not a single
positive constant uniform up to its open upper endpoint.

The sign extension uses the absolute source norm and the real
fixed-point equation. It does not infer monotonicity of the actual gap
in `r`, and it does not turn signed channel eigenvalues into a favorable
quadratic-form inequality without accounting for their coefficients.

## 6. Exact hostile cases and remaining seam

1. **Operator norm alone cannot furnish the improvement.** For the
   fundamental singlet, `Omega=3`, and
   `3/(lambda_(1/2)^2)=4/3`. Thus replacing the three generator estimates
   by `||Omega||_op` and otherwise repeating (DC5) still gives `8/3`.
   The singlet vector is entangled between the two input sides, while
   the rank-one terms needed in the coefficient proof have product
   vectors on those sides.
2. **The local constant `2` is attained.** On one link take
   `u(U)=U_11`, `v(U)=U_22`. Each has Fourier norm one. The product
   vector `|up,down>` has singlet weight `1/2` and triplet weight
   `1/2`. Its contracted-gradient Fourier norm is therefore
   `3(1/2)+1(1/2)=2`. Equivalently,
   `sum_k(D_k u)(D_k v)=2-uv`; its scalar coefficient is `3/2` and
   its spin-one coefficient has trace norm `1/2`. The full local
   gradient bound cannot be replaced by a constant below `2`.
3. **Deleting the mean changes this hostile example.** On that single
   link `Q` deletes the scalar contribution `3/2`; the remaining norm
   is only `1/2`. Consequently case 2 is not a lower-bound witness for
   the complete anchored operator in (SC1). Its optimal norm remains
   undetermined.
4. **A wrong coefficient carrier breaks the key step.** If one
   independently allowed an arbitrary coefficient on
   `V_(1/2) tensor V_(1/2)` with trace norm one, the singlet projector
   would be allowed directly and the gradient norm would be `3`.
   It is essential that the function being estimated is a bilinear
   product with coefficient `B_J tensor C_K`.
5. **Higher spins are covered analytically.** The inequality
   `1/[b(a+1)]<=2/3` outside `(1/2,1/2)` covers every remaining
   half-integral pair; a finite enumeration is neither needed nor
   offered as evidence for this unrestricted step.

The completed successor is the smaller constant in the same norm and
the resulting explicit interval. Further improvement by exact anchor
accounting, signed summation over links, or gauge-specific coefficient
constraints remains OPEN. No conclusion about a continuum Yang--Mills
mass gap, novelty, or the exact interacting spectrum follows from this
estimate.
