# Rank-two kernel: independent interval audit

This note records an independent calculus derivation for the coefficient
enclosure. Its carrier is a real parameter `b>0`, a positive real integration
coordinate, exact rational interval endpoints, and finitely many exact signed
Euler coefficients. The infinite coefficient tail is bounded separately.
The receiver is an enclosure of the completed Taylor coefficient
`lambda_2=Lambda''(1)/2`; its conversion to a coefficient of the uncompleted
L-function requires the exact lower-zero premise. This is an enclosure
operation, with no inverse or complete recovery of the L-function claimed.

For root number `w=+1`, formula (3) of
[ANALYTIC_BRIDGE.md](../bsd-general-01/ANALYTIC_BRIDGE.md) gives

\[
\lambda_2=\sum_{n\ge1}a_nJ_2(\alpha n),\qquad
J_2(b)=\int_1^\infty e^{-bu}(\log u)^2\,du.
\]

The factor `2/2!` is one. If `lambda_0=lambda_1=0`, then
`c_2=L''(1)/2=alpha lambda_2`. Neither `lambda_2` nor `c_2` equals the raw
second derivative without its factorial. The conductor, sign, Euler factors,
and theorems supplying the exact lower zeros are external mathematical
premises of this numerical audit, to be checked in their own source notes.

## 1. Original positive kernel and its derivatives

Put `L=log u` and `f_b(u)=exp(-bu)L^2`. Direct differentiation gives

\[
f_b''(u)=e^{-bu}\left[b^2L^2-\frac{4bL}{u}
                      +\frac{2(1-L)}{u^2}\right].             \tag{A1}
\]

In particular `f_b''(1)=2 exp(-b)>0`, but the second derivative need not stay
positive. Positivity of the kernel does **not** justify a one-sided midpoint
error. At `b=1,u=2`, direct interval arithmetic with
`2/3<log 2<7/10` gives the strict negative upper bound
`(7/10)^2-2*(2/3)+(1-2/3)/2=-203/300`.
Thus `b=1,u=2` is a distinguishing hostile case against the blanket convexity
rule. It does not refute the signed-error method below.

On any panel `[l,r]` with `1<=l<r`, write rational logarithm bounds as
`0<=L_l<=log l` and `log r<=L_r`. Define

\[
\begin{split}
P_-&=b^2L_l^2+2/r^2,& P_+&=b^2L_r^2+2/l^2,\\
Q_-&=4bL_l/r+2L_l/r^2,&Q_+&=4bL_r/l+2L_r/l^2.
\end{split}
\]

The bracket in (A1) lies in `[P_- - Q_+, P_+ - Q_-]`. Multiplying this
interval by an outward enclosure of `[exp(-br),exp(-bl)]`, with all four
endpoint products admitted, gives signed bounds `[D_-,D_+]` for `f_b''`
throughout the panel. Dependencies forgotten in these interval products
enlarge the enclosure; they do not invalidate it. A simpler absolute bound is

\[
B_2=e^{-bl}\left[b^2L_r^2+4bL_r/l+2(1+L_r)/l^2\right].       \tag{A2}
\]

Every exponential or logarithm used in an executable bound must itself be
outward enclosed; binary floating-point evaluations do not supply this step.

For completeness, the fourth derivative is

\[
f_b^{(4)}(u)=e^{-bu}\left[b^4L^2-8b^3L/u
 +12b^2(1-L)/u^2-4b(4L-6)/u^3+(22-12L)/u^4\right].          \tag{A3}
\]

It follows by the product rule and
`(L^2)'=2L/u`, `(L^2)''=2(1-L)/u^2`,
`(L^2)'''=(4L-6)/u^3`, `(L^2)''''=(22-12L)/u^4`.
Replacing each signed summand in (A3) by its absolute bound gives

\[
B_4=e^{-bl}\left[b^4L_r^2+8b^3L_r/l
 +12b^2(1+L_r)/l^2+4b(4L_r+6)/l^3+(22+12L_r)/l^4\right].   \tag{A4}
\]

## 2. Certified quadrature

For a panel of width `h=r-l` and midpoint `m`, Taylor's integral remainder
or the positive Peano kernel of the midpoint rule gives

\[
\frac{h^3D_-}{24}\le\int_l^r f_b(u)\,du-hf_b(m)
                         \le\frac{h^3D_+}{24}.               \tag{A5}
\]

For example, integrate the second-order Taylor remainder separately on the
two half-panels; the linear terms cancel and the total nonnegative weight is
`h^3/24`. Hence each panel may use its own signed bounds; no global sign of
curvature is required. An absolute error `h^3 B_2/24` is also valid.

Simpson's rule on one panel of total width `h` has absolute error at most
`h^5 B_4/2880`. Here `h` is the **entire** left-to-right panel width, not
the half-step between a midpoint and an endpoint. Either method can be
summed over geometric bands whose endpoints are rational. Refining every
band makes the total finite-range quadrature error tend to zero; the claimed
finite-head width must still be checked on the actual exact ledger.

If midpoint values are independently enclosed in `[v_i^-,v_i^+]`, sum
`h_i v_i^- + h_i^3 D_i^-/24` for a lower integral bound and
`h_i v_i^+ + h_i^3 D_i^+/24` for an upper integral bound, then include the
positive improper integral tail. Outward rounding of panel contributions
must be retained. An a priori positivity clamp `lower=max(0,lower)` is valid
for the individual `J_2` or `H` kernels, but not for a sum with signed `a_n`.

## 3. Parameter uncertainty and improper integral tails

The kernel decreases as `b` increases. For `b in [b_-,b_+]` with `b_->0`,
differentiation under its absolutely convergent integral and `log u<=u-1`
give

\[
|J_2'(b)|\le\int_1^\infty u e^{-bu}(u-1)^2du
               =e^{-b}(2/b^3+6/b^4).
\]

Thus an enclosure computed at `b_-` may reduce its lower endpoint by

\[
(b_+-b_-)e^{-b_-}(2/b_-^3+6/b_-^4).                          \tag{A6}
\]

The upper endpoint needs no parameter correction. For `b=alpha*n`, use
`b_+-b_-=n*(alpha_+-alpha_-)`; do not omit this factor `n`.

For an integral cutoff `U>=1`, concavity of the logarithm gives
`log(U+v)<=log U+v/U` for `v>=0`. Squaring preserves the inequality because
both sides are nonnegative, and termwise elementary integration yields

\[
0\le\int_U^\infty e^{-bu}(\log u)^2du\le
e^{-bU}\left[\frac{(\log U)^2}{b}
 +\frac{2\log U}{Ub^2}+\frac{2}{U^2b^3}\right].              \tag{A7}
\]

All variables in an implemented upper bound may be replaced by outward
intervals with directed arithmetic. The cruder global inequality
`J_2(b)<=2 exp(-b)/b^3` follows by taking `log u<=u-1` directly. It covers
the entire positive kernel if a large-`b` branch omits quadrature.

## 4. The integrated-by-parts kernel

An equivalent representation is

\[
H(b)=\int_b^\infty e^{-t}\frac{\log(t/b)}t\,dt,\qquad
J_2(b)=\frac{2}{b}H(b).                                     \tag{A8}
\]

Integration by parts first gives
`J_2(b)=(2/b) integral_1^infinity exp(-bu)log(u)/u du`; the substitution
`t=bu` gives (A8). Both boundary terms vanish, including at `u=1`.
The formula is independent of central vanishing. Consequently

\[
\lambda_2=\frac2\alpha\sum_{n\ge1}\frac{a_n}nH(\alpha n).
\]

Only after the lower coefficients vanish may this be multiplied by `alpha`
and called `c_2=2 sum (a_n/n) H(alpha n)`.

For `F_b(t)=exp(-t)log(t/b)/t`, writing `L=log(t/b)`,

\[
F_b''(t)=e^{-t}\left[
L(1/t+2/t^2+2/t^3)-(2/t^2+3/t^3)\right].                    \tag{A9}
\]

On `[l,r]` with `l>=b`, set
`P(t)=1/t+2/t^2+2/t^3` and `Q(t)=2/t^2+3/t^3`.
Both decrease. The bracket in (A9) is enclosed by
`[log(l/b) P(r)-Q(l), log(r/b) P(l)-Q(r)]`, using certified log bounds.
Multiply by the exponential interval using signed interval multiplication,
then apply (A5). At its lower endpoint,
`F_b''(b)=-exp(-b)(2/b^2+3/b^3)<0`; this is another exact hostile case
against a copied nonnegative-curvature rule from the E1 kernel.

The selected implementation uses Simpson quadrature on this transformed
kernel. Its fourth derivative, checked independently, is

\[
F_b^{(4)}(t)=e^{-t}\left[L P_4(t)-D_4(t)\right],             \tag{A9a}
\]

where

\[
\begin{split}
P_4(t)&=1/t+4/t^2+12/t^3+24/t^4+24/t^5,\\
D_4(t)&=4/t^2+18/t^3+44/t^4+50/t^5.
\end{split}
\]

Indeed, for `g(t)=log(t/b)/t`, successive derivatives are
`(1-L)/t^2`, `(2L-3)/t^3`, `(11-6L)/t^4`, `(24L-50)/t^5`;
then `F''''=exp(-t)(g-4g'+6g''-4g'''+g'''')`.
Both `P_4` and `D_4` are positive and decreasing. Hence its bracket on
`[l,r]` is enclosed by

\[
[\,\log(l/b)P_4(r)-D_4(l),\quad
   \log(r/b)P_4(l)-D_4(r)\,].                              \tag{A9b}
\]

Certified logarithm endpoints and all four products with the exponential
interval give `[D_-,D_+]` enclosing the fourth derivative. If `S` is the
Simpson value on this panel of entire width `h`, its signed error is

\[
\int_l^rF_b(t)dt-S\ \in\
[-h^5D_+/2880,\ -h^5D_-/2880].                             \tag{A9c}
\]

The reversal and minus signs matter. For the elementary control `f(t)=t^4`,
the error is exactly `-h^5/120`, because `f''''=24`; this catches a reversed
Simpson-error sign without relying on transcendental numerical evaluations.

The moving lower endpoint contributes zero when differentiating H, because
`log(b/b)=0`. Therefore

\[
H'(b)=-E_1(b)/b,\qquad
0\le H(b_-)-H(b_+)\le(b_+-b_-)e^{-b_-}/b_-^2.                \tag{A10}
\]

If the transformed tail starts at `T>=b`, the same tangent inequality
and `1/t<=1/T` give

\[
0\le\int_T^\infty F_b(t)dt\le
e^{-T}\left[\frac{\log(T/b)}T+\frac1{T^2}\right].             \tag{A11}
\]

The executed implementation uses the simpler upper bound `exp(-T)/b`.
This is also valid: for `t>=T>=b`, `log(t/b)<=t/b`, so
`F_b(t)<=exp(-t)/b`, whose integral beyond T is exactly `exp(-T)/b`.

Finally, `(2/alpha)` is a positive interval scalar, so its own uncertainty
must be included when converting a signed enclosure of the H-sum to
`lambda_2`. Its endpoints cannot automatically be paired lower/lower and
upper/upper if the H-sum crosses or lies below zero.

## 5. Omitted Euler coefficients

Let `A>0` satisfy `alpha>=A`, and let `q<1` satisfy `exp(-A)<=q`.
The theorem input `|a_n|<=d(n)sqrt(n)<=2n` and the global kernel bound above
give the complete suffix enclosure

\[
\left|\sum_{n>M}a_nJ_2(\alpha n)\right|
\le\frac{4q^{M+1}}{A^3(M+1)^2(1-q)}.                        \tag{A12}
\]

For a fixed integer `K>=M`, a sharper alternative uses no extra Euler
coefficients:

\[
\frac2{A^3}\sum_{n=M+1}^K
 \frac{d(n)\lceil\sqrt n\rceil q^n}{n^3}
 +\frac{4q^{K+1}}{A^3(K+1)^2(1-q)}.                         \tag{A13}
\]

Here `d(n)` is the exact elementary divisor count, and an integer square-root
witness certifies the ceiling. The first sum bounds unknown coefficients;
it is not an extension of the Euler head through K. The remainder covers
every n beyond K. Exact powers and outward rounding must be included in
the recorded tail. A numerical search that finds further vanishing
coefficients cannot replace either complete tail bound.

There is also an elementary global support refinement for the selected
`E_34: y^2=x^3-34^2x`. At a good odd prime `p=3 mod 4`, the change
`x -> -x` negates the cubic, while the quadratic character satisfies
`chi(-1)=-1`. The complete character sum cancels, including its zero-valued
fixed point, so `a_p=0`. The good-prime recurrence
`a_(p^j)=a_p a_(p^(j-1))-p a_(p^(j-2))` then makes every odd-exponent
coefficient vanish. Multiplicativity implies that a nonzero odd `a_n`
has every `3 mod 4` prime to an even exponent, hence `n=1 mod 4`.
The independently justified additive local factors at 2 and 17 give zero
whenever `2|n` or `17|n`. Therefore the finite positive sum in (A13) may
omit all indices failing `n=1 mod 4` or `17` not dividing `n`.
The unrestricted remainder in (A13) remains a valid overbound. This is a
global character-symmetry and recurrence proof; sampled vanishing traces
alone would not license this refinement.

For `J_n in [l_n,u_n]`, the signed head interval uses `a_n[l_n,u_n]` when
`a_n>=0` and `[a_n u_n,a_n l_n]` otherwise. Thus the head width equals
`sum |a_n| (u_n-l_n)` before any separately recorded rounding. Its union with
the complete symmetric tail is an enclosure; it is neither a proof of an
exact zero nor a complete solution fiber.

## Implementation and executed audit

The identities and inequalities (A1)–(A13) above are written calculus
derivations. They do not certify an executable implementation by themselves.
The implementation [work/interval.py](work/interval.py) has now been read
and checked against them. Its `fourth_bound`, `h_kernel`, `assemble_head`,
and `all_term_tails` implement the signed fourth-derivative bounds, Simpson
error reversal, parameter loss, positive improper tail, signed coefficient
weights, positive interval division by alpha, and complete coefficient tail
described above. The proof does not depend on a sampled derivative sign.

The elementary evaluations also have explicit global bounds. For
`v=(z-1)/(z+1)` and `1<=z<=2`, the positive atanh expansion for log(z)
has its remainder after T terms bounded by
`2 v^(2T+1)/((2T+1)(1-v^2))`. Here `T=32`; argument reduction writes
`x=2^s z`, retaining `s` times the independently enclosed log(2).
For exp(-x), repeated halving reaches `[0,1]`; alternating degree 31 and
degree 30 Taylor sums give lower and upper bounds, followed by outward
squaring. Every operation uses exact rationals and a directed `2^-80` grid.
The Machin arctangent sums are alternating exact rational enclosures.

The receipt [evidence/interval.json](evidence/interval.json) matches these
executed source bytes:

| Object | SHA-256 |
|---|---|
| `work/interval.py` | `87181b1ccc7622712b9f29dcb2f149abb3e0be685614535868fea3cab04c41c4` |
| `work/BUDGET.json` | `7e4724c15e8c5a23429067772ecc9f12b1298989299630bb2065751c7a325e6e` |

Hashes establish byte identity, not mathematical validity or the chronology
of a budget declaration. The budget records cutoffs 40, 80, 160 in that
order, 64 Simpson panels per doubling band, integral endpoint 32, and no
panel refinement. The first two cutoffs were skipped because their complete
tail widths already exceeded `1/100`. Cutoff 160 used 27 nonzero Euler terms
and 7,360 panels, producing

\[
\lambda_2\in
[1727579267/12500000,\ 13820780907/100000000]
=[138.20634136,\ 138.20780907].
\]

The exported width is exactly `146771/100000000=0.00146771<0.01`.
Before the infinite suffix is added, the finite completed head has width
`17109081260079645/1208925819614629174706176`, about `1.416e-8`.
The complete symmetric suffix radius is
`887158659065786629989/1208925819614629174706176`, about `0.000733841`.
These decimal displays are descriptive; the rational endpoints carry the
certificate.

The standard-library-only script [work/interval_audit.py](work/interval_audit.py)
has been run as
`python -I -B research/bsd-rank-two-01/work/interval_audit.py`.
Its exact symbolic differentiation reproduces (A9) and (A9a), four rational
panels verify the polynomial signed-Simpson controls, the original-J2
convexity hostile case has a strict rational upper bound below zero, and
integer square-root ceiling witnesses are checked for `1<=n<=4096`.
The receipt is [evidence/interval_audit.json](evidence/interval_audit.json).
These are bounded controls, separate from the written general quadrature
and tail proofs.

The same audit run also independently reassembled every recorded head term,
signed coefficient weight, width component, parameter correction, grid
rounding, complete divisor tail and final decimal export. It recomputed
divisor counts using paired divisors instead of the implementation's sieve,
and regenerated upper q-powers with integer grid arithmetic. Fresh execution
of `local_inputs.coefficients(160)` matched every admitted coefficient; an
additional independent quadratic-character sum matched every good-prime
trace through 160. Seven exp and six log controls used independent unscaled
or unreduced exact series whose very tight intervals are contained in the
implementation's reported elementary intervals.

**Result:** the implementation inspection and exact ledger audit passed.
This is written mathematics with reproducible exact rational computation
and finite hostile controls. It is not a formal proof, an independent second
execution of every Simpson panel, or a verification of the separate
arithmetic-rank and local-reduction theorem premises. Conditional on those
explicit premises, the interval does certify that the completed coefficient
`lambda_2` is strictly positive. The analytic-order and BSD consequences
must still be taken through their separately stated theorem bridges.
