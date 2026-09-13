# General BSD: exact analytic certificates and their remaining bridge

This note proves a general Mellin coefficient enclosure and a certificate
criterion, including an unconditional low-order exclusion obtained from a
published theorem. It does not prove general BSD or execute a new curve
calculation. Sources below were inspected on 12 September 2026.

**Contract.** The carrier is nonsingular elliptic curves E/Q with an exactly
specified model, their full Hasse–Weil L-functions, and independently proved
Mordell–Weil ranks. Analytic values lie in C; certificates use rational real
intervals. Supplied ports include the conductor N, root number w, correct local
Euler factors and their theorem justifications. Requested readouts are central
zero order m, leading coefficient c_m, and, separately, the full BSD identity.
Forward evaluation is enabled only after the model and normalization checks.
The receiver retains exact zeros separately from small enclosures, all omitted
terms, and every cited hypothesis. A finite head plus its error bound preserves
an enclosure, not the original L-function: no inverse or complete source fiber
is claimed. Missing coverage or exact vanishing leaves the readout **OPEN**.

## 1. The universal claims that need proofs

Write r=rank E(Q), m=ord_(s=1)L(E,s), and c_m=L^(m)(E,1)/m!.
The rank statement is m=r for every E/Q. Wiles's official Clay statement
distinguishes this from its refinement involving Sha and the leading
coefficient. His initially incomplete Euler product has the same central
order as the full L-function: the finitely omitted local polynomials are
nonzero at s=1. His notation L* adds the finite missing Euler factors;
it is not our archimedean completion Lambda below.
[Wiles, printed p.2](https://www.claymath.org/wp-content/uploads/2022/05/birchswin.pdf#page=2).

With the full Euler product, the required additional claims are

\[
\Sha(E/\mathbf Q)\text{ is finite},\qquad
c_r=\frac{\Omega_E\operatorname{Reg}_E
                 \#\Sha(E/\mathbf Q)\prod_p c_p}{\#E(\mathbf Q)_{\rm tors}^2}.
\tag{1}
\]

Here Omega integrates the absolute minimal invariant differential over all
E(R); Reg uses a basis of the full free group and the BSD height convention;
Reg=1 at r=0. These are the conventions explicitly used in
[Creutz–Miller, Theorem 1.1](https://arxiv.org/pdf/1105.4018v2#page=2) and
[Cremona, section 3.4](https://johncremona.github.io/book/fulltext/chapter3.pdf#page=10).
A subgroup of free index d has determinant d² Reg. An unsaturated subgroup
therefore changes the quotient in (1), even when its rank is correct.

There are three logically separate obligations:

1. **Order:** prove the lower coefficients vanish exactly and c_r is nonzero.
   Independent arithmetic rank r identifies the number to compare; it does
   not generally supply those analytic zeros.
2. **Finiteness:** prove finiteness of the actual cohomologically defined Sha.
   Naming a numerical quotient “analytic Sha” does not establish this.
3. **Value:** identify c_r with the arithmetic expression in (1), after
   matching all normalizations. Separate proofs of rank equality and finite
   Sha do not themselves identify this real number.

For an elementary hostile case to a numerical identification rule, an interval
(0.99,1.01) also contains 1+sqrt(2)/1000. If the BSD quotient is independently
known to be a positive integer, that interval isolates 1; it still identifies
the actual order of Sha only with an independently established connecting
identity. No finite positive-width real interval proves equality to 1 unaided.

The E5 completion supplied that identity through Creutz–Miller's theorem,
whose hypotheses are N<5000 and **analytic** rank at most one. It then isolated
the integer. Neither the hypothesis nor the identity extends to arbitrary
rank by reusing its numerical procedure. See the local
[E5 specialization](../bsd-e5-completion/BSD_SHA_THEOREMS.md).

## 2. General completed central coefficients

Modularity supplies the normalized weight-two newform
f(z)=sum_(n>=1) a_n exp(2*pi*i*n*z), with L(f,s)=L(E,s).
This is an established theorem for every E/Q, not a BSD hypothesis.
[Breuil–Conrad–Diamond–Taylor, Theorem A and introduction](https://www.math.u-psud.fr/~breuil/PUBLICATIONS/STW.pdf).
Set

\[
\alpha=2\pi/\sqrt N,\quad g(u)=f(iu/\sqrt N),\quad
\Lambda(s)=\alpha^{-s}\Gamma(s)L(E,s).
\]

The Fricke eigenvalue is -w: g(1/u)=w u²g(u). This sign convention and
Mellin normalization match
[Cremona, (2.8.5)–(2.8.6)](https://johncremona.github.io/book/fulltext/chapter2.pdf#page=23).
The following is the explicit derivation used here.

In a right half-plane, termwise Mellin integration gives
Lambda(s)=integral_0^infinity g(u)u^(s-1)du. Splitting at 1 and substituting
u=1/v on (0,1) yields

\[
\Lambda(1+t)=\int_1^\infty g(u)(u^t+w u^{-t})\,du
=\begin{cases}
2\int_1^\infty g(u)\cosh(t\log u)\,du,&w=+1,\\
2\int_1^\infty g(u)\sinh(t\log u)\,du,&w=-1.
\end{cases}                                                    \tag{2}
\]

The standard coefficient estimate |a_n|<=d(n)sqrt(n)<=2n makes g
exponentially decaying on u>=1. At a good prime it follows by expanding
the two Hasse-bounded Euler roots; a multiplicative bad factor has
a_(p^j)=(+/-1)^j, and an additive bad factor has a_(p^j)=0 for j>=1,
so the same bound includes every bad prime. These are the all-n steps
of the [E5 theorem audit](../bsd-e5-test-01/ANALYTIC_THEOREMS.md), with the
bad factors now admitted in their general forms. Hence, on each compact
t-set, an exponential times a fixed power of u and log(u) dominates every
derivative in (2). It defines an entire function and permits all the
interchanges below.

Define the **completed Taylor coefficient** and its integral kernel by

\[
\lambda_k=\Lambda^{(k)}(1)/k!,\qquad
J_k(b)=\int_1^\infty e^{-bu}(\log u)^k\,du\quad(b>0).
\]

Then, without any assumed central zero,

\[
\boxed{\lambda_k=\frac{1+w(-1)^k}{k!}
                     \sum_{n\ge1}a_nJ_k(\alpha n).}             \tag{3}
\]

Thus the opposite-parity coefficients vanish. The allowed-parity sums may
cancel: J_k>0 does not make a_n or g positive. Since L is not identically
zero and its completion factor is a unit near 1, m is finite, is also the
order of Lambda, and satisfies (-1)^m=w.

The conversion to raw L-coefficients is triangular. If
h(t)=alpha^(1+t)/Gamma(1+t)=sum h_j t^j, with h_0=alpha, then

\[
c_k=[t^k]L(E,1+t)=\sum_{j=0}^k h_j\lambda_{k-j}.               \tag{4}
\]

Consequently c_r=alpha lambda_r **only when all lambda_j for j<r vanish**.
Raw L(1+t) itself need not be even or odd. For r>=1 and those lower zeros,
integration by parts in J_r (both boundary terms vanish) gives

\[
c_r=\frac{2}{(r-1)!}\sum_{n\ge1}\frac{a_n}{n}
       \int_1^\infty e^{-\alpha n u}\frac{(\log u)^{r-1}}u\,du
\quad\text{when }w=(-1)^r.                                    \tag{5}
\]

For r=1 this recovers the E5 E1 formula. The lower-vanishing premise in
(5) is explicit also in
[Cremona, Proposition 2.13.1](https://johncremona.github.io/book/fulltext/chapter2.pdf#page=37).

**Written enclosure lemma.** Suppose exact rationals A>0 and 0<q<1 satisfy
alpha>=A and exp(-alpha)<=q. One universal choice is q=1/(1+A).
Let H_(k,M) be (3) truncated at n=M. For k>=0 and M>=0,

\[
|\lambda_k-H_{k,M}|\le
T_{k,M}:=\frac{4q^{M+1}}
 {A^{k+1}(M+1)^k(1-q)}.                                      \tag{6}
\]

Proof: log(u)<=u-1 gives
J_k(b)<=integral_1^infinity e^(-bu)(u-1)^k du
=k! e^(-b)/b^(k+1). Combine |1+w(-1)^k|<=2 and |a_n|<=2n,
then bound n^(-k) by (M+1)^(-k) throughout the geometric suffix.
Opposite parity has exact zero tail; (6) is a convenient uniform overbound.
This covers every omitted coefficient without inspecting its sign.

If a rigorous finite-head computation encloses H_(k,M) in [a,b], then
[a-T_(k,M),b+T_(k,M)] encloses lambda_k. For each fixed E,k the tail
tends to zero as M grows. With convergent certified head quadrature this
semidecides nonvanishing: a nonzero coefficient eventually has an interval
excluding zero. Exact vanishing is not certified merely because every
computed positive-width interval contains zero. The local
[E5 interval derivation](../bsd-e5-test-01/INTERVAL_DERIVATION.md) supplies
one worked head/error-ledger pattern; its E1 kernel and constants are specific
to k=1 and E5 and cannot be copied unchanged into (3).

## 3. What an independent rank supplies

**Finite analytic certificate criterion — written proof.** Fix E/Q with
independently proved rank r and root number w=(-1)^r. Supply exact proofs
lambda_k=0 for every k<r having (-1)^k=w, and a rigorous interval for
lambda_r excluding zero. Formula (3) kills the opposite parity, so (4)
proves m=r and c_r=alpha lambda_r. No BSD statement is an input. A positive
interval proves positive c_r; nonvanishing alone suffices for rank equality.
The arithmetic and analytic evidence may be separate without being separate
proofs of every established theorem they cite.

There are floor(r/2) potentially missing lower coefficients of the allowed
parity: k=0,2,...,r-2 for even r, or k=1,3,...,r-2 for odd r.
Arithmetic rank alone must not be substituted for their exact zero proofs.
There is, however, a useful **known-theorem reduction**. Wiles records
that analytic order m=0 or 1 implies rank E(Q)=m.
[Wiles, printed p.4](https://www.claymath.org/wp-content/uploads/2022/05/birchswin.pdf#page=4).
Taking the contrapositive, an independently proved rank at least two gives
m>=2. Parity then gives m>=2 for w=+1 and m>=3 for w=-1. This argument
uses the published low-analytic-rank theorem, not the unproved general
inequality m>=r.

| Independent arithmetic input | Sign | Exact zeros already supplied by these theorems | Additional certificate needed for m=r |
|---|---:|---|---|
| r=0 | +1 | Opposite parity | lambda_0 interval excludes 0 |
| r=1 | -1 | lambda_0=0 and all even coefficients | lambda_1 interval excludes 0 |
| r=2 | +1 | lambda_0=lambda_1=0 | lambda_2 interval excludes 0 |
| r=3 | -1 | lambda_0=lambda_1=lambda_2=0 | lambda_3 interval excludes 0 |
| r=4 | +1 | lambda_0=lambda_1=0 and odd coefficients | Exact lambda_2=0; lambda_4 interval excludes 0 |

For r>=2 this leaves floor(r/2)-1 allowed-parity exact zeros beyond the
low-rank theorem, when this number is positive. In particular the first
surviving obligation is lambda_2=0 for r=4,w=+1. A sign mismatch with
(-1)^r is not repaired by assigning the expected sign: it prevents use of
the criterion and requires checking the supplied arithmetic and sign proofs.

**Written negative control.** For r>=4, put b=2 if r is even and b=3 if
r is odd. The entire germ F_delta(t)=delta*t^b+t^r, with delta>0,
has the expected parity, order at least two, and coefficient of t^r exactly
1, but its true order is b<r. Delta can be smaller than any proposed
positive error tolerance. Thus parity, low-order exclusion, a positive
r-th coefficient and small lower same-parity coefficients do not imply
order r. This is a counterexample to that inference on its stated analytic
data; it is not claimed to be an elliptic-curve L-function or a counterexample
to BSD. Formula (4) adds a second guard: without lower zeros, a completed
r-th coefficient need not equal c_r/alpha.

## 4. One concrete next target and its stopping boundary

The next bounded target is a **rank-two certificate for one supplied E/Q**
whose exact arithmetic proof gives r=2 and whose checked root number is +1.
Implement a rational enclosure of

\[
\lambda_2=\sum_{n\ge1}a_n
              \int_1^\infty e^{-\alpha n u}(\log u)^2\,du.
\]

This is a specified new kernel, not an open-ended attempt to prove BSD.
The admission packet must bind that E, N, its bad Euler factors, independent
rank proof, and rational alpha bounds. Use at most M=40,80,160 coefficients
in that order, a predeclared finite quadrature budget, and the complete tail
(6). Success is an interval of width at most 1/100 excluding zero, with all
rounding and integral errors included. The theorem in section 3 then proves
rank equality for that input and supplies an enclosure for c_2=alpha lambda_2.
A negative interval would still certify order two; it would also conflict
with the positive leading coefficient predicted by (1), if all premises held.

Exhausting the declared budget with zero still enclosed is **OPEN**, not
vanishing or a failure of BSD. Missing rank, sign, Euler-factor or all-term
premises disables promotion to the rank conclusion; a finite head can remain
available. A changed-model certificate and a removed-tail certificate are
the two required rejecting controls. No curve has been selected or run in
this note. Even successful rank-two certification leaves finite Sha and
the leading-coefficient identity as separate obligations; Creutz–Miller's
rank-at-most-one application cannot close them.

**Evidence ceiling.** Equations (2)–(6), the certificate implication, the
contrapositive specialization and the analytic negative control are written
derivations using the cited established premises. The source theorems are
THEOREM_CITED. No formal proof, fresh numerical interval, general finiteness
theorem for Sha, or universal BSD proof is asserted.
