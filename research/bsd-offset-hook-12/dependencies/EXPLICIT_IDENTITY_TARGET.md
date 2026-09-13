# E34: the explicit analytic–height identity still to prove

Date: 2026-09-12. This note supplies a common exact target for the next
experiment. It expands the established analytic coefficient and the
arithmetic regulator into convergent expressions, and proves a sufficient
telescoping-certificate criterion for their equality. It does **not**
establish that equality or identify the total order of Sha.

The curve is \(E/\mathbb Q:y^2=x^3-1156x\), with
\(P=(-2,48)\), \(Q=(-16,120)\), and
\(S=P+Q=(2178/49,65472/343)\). The preceding
[analytic proof](input_source/ANALYTIC_PROOF.md) proves analytic
order two, using an independently proved arithmetic rank two. The
[integral-basis proof](input_source/GENERATOR_PROOF.md) proves
\(E(\mathbb Q)=\mathbb ZP\oplus\mathbb ZQ\oplus E(\mathbb Q)_{\rm tors}\),
where the torsion order is 4. Those are unchanged dependencies here.

**Contract.** Exact rational group points, their primitive projective
abscissas, real logarithmic heights, and the full complex L-function are
different carriers. The supplied ports include the actual model,
conductor, local factors, sign, integral basis, and their proofs. The
requested new readout is an equality of real constants, followed
separately by identification with a cohomological group order. The
receiver retains the height convention, real components, every gcd
correction, all omitted tails and the limit boundary. The source points
are retained: abscissas alone forget the ordinate sign, while the
particular height receiver is invariant under it. Neither an inverse
from analytic moments to points nor one from heights to points is
claimed. Missing comparison or boundary proofs leave the identity OPEN.

## 1. The exact target with every normalization fixed

Let \(\alpha=\pi/68\), so
\(\Lambda(s)=\alpha^{-s}\Gamma(s)L(E,s)\). The proved lower zeros
allow the second raw Taylor coefficient to be written as

\[
c^{\rm an}_2=\frac{L''(E,1)}2
=\alpha\lambda_2
=\alpha\sum_{n\ge1}a_nJ_2(\alpha n),\qquad
J_2(b)=\int_1^\infty e^{-bu}(\log u)^2\,du.
\tag{1}
\]

Here the \(a_n\) are from the full Euler product for this curve:
the factors at 2 and 17 are 1. The Mellin completion and derivative
formula match Cremona's equations (2.8.5), (2.13.1) and Proposition
2.13.1. His formula's lower-vanishing hypothesis is already proved for
this input; it is not supplied by the expansion itself.
[Cremona, chapter 2](https://johncremona.github.io/book/fulltext/chapter2.pdf#page=36)

For a rational point \(R\), use the **full logarithmic x-height**

\[
q_R=\lim_{j\to\infty}4^{-j}\log H_x(2^jR),\qquad
B=\frac{q_S-q_P-q_Q}{2},\qquad
\mathcal R=q_Pq_Q-B^2.
\tag{2}
\]

This \(q\) is twice the convention that places a factor \(1/2\)
before the limit. The pairing in (2) has diagonal \(q_R\). Halving
every entry of its rank-two Gram matrix divides its determinant by four.
The full convention and determinant agree with Cremona §3.4, printed
pages 71–72. Because \(P,Q\) are an integral basis, \(\mathcal R\)
is the regulator for that convention. A subgroup of index \(d\)
would instead have determinant \(d^2\mathcal R\).
[Cremona, height normalization](https://johncremona.github.io/book/fulltext/chapter3.pdf#page=10)

Take the minimal differential \(\omega=dx/(2y)\) and the period over
**both** real components:

\[
\Omega=\int_{E(\mathbb R)}|\omega|
=2\int_{34}^\infty\frac{dx}{\sqrt{x(x^2-1156)}}.
\tag{3}
\]

The [factor comparison](input_source/FACTOR_COMPARISON.md) derives
this convention and the period evaluation. Both Tamagawa numbers are
4, so \((\prod_pc_p)/|E(\mathbb Q)_{\rm tors}|^2=16/16=1\).
Thus the remaining full-BSD equality, **if Sha is finite**, is exactly

\[
\boxed{\alpha\sum_{n\ge1}a_nJ_2(\alpha n)
=\Omega\left[q_Pq_Q-\frac{(q_S-q_P-q_Q)^2}{4}\right]
\#\Sha(E/\mathbb Q).}
\tag{4}
\]

For comparison without silently assuming finiteness, introduce a
specified candidate positive integer \(\sigma\) and the real defect

\[
\mathscr D_\sigma=c^{\rm an}_2-\Omega\sigma\mathcal R.
\tag{5}
\]

Proving \(\mathscr D_1=0\) would prove a real-constant identity. To
call it the full formula with \(\#\Sha=1\), a proof must also
establish finiteness and identify the actual cohomological group order.
No integral value or group order is obtained by naming the quotient
\(c^{\rm an}_2/(\Omega\mathcal R)\).

## 2. An explicit convergent logarithmic series for each height

For \(R_j=2^jR\), let \((a_j:b_j)\) be the primitive projective
abscissa, with \(b_j>0\) at affine points and \((1:0)\) at \(O\).
Set \(H_j=\max(|a_j|,b_j)\), \(h_j=\log H_j\), and define

\[
F_j=(a_j^2+1156b_j^2)^2,\quad
G_j=4a_jb_j(a_j^2-1156b_j^2),\quad
g_j=\gcd(F_j,G_j)>0,\quad M_j=\max(F_j,|G_j|).
\tag{6}
\]

Reduce \((F_j:G_j)\) by \(g_j\) and normalize its sign. The
duplication formula then gives \(H_{j+1}=M_j/g_j\). This remains
projective when \(G_j=0\), so no affine division by zero is needed.
Define the exact positive rational \(\rho_j=M_j/H_j^4\), and the
real correction

\[
\begin{aligned}
\delta_{R,j}&=h_{j+1}-4h_j
=\log\frac{M_j}{g_jH_j^4}\\
&=\log\rho_j-\nu_2(g_j)\log2-\nu_{17}(g_j)\log17.
\end{aligned}
\tag{7}
\]

The last equality uses the proved gcd bound below; thus the prime
corrections are kept explicitly rather than lost during reduction.
The curve-specific elementary estimates are

\[
g_j\mid C_0=2^6 17^4=5345344,\qquad
1\le\rho_j\le C_1=(1+1156)^2=1338649.
\tag{8}
\]

For completeness, the gcd bound's coverage is as follows. At a prime
other than 2 or 17, a common divisor of \(F,G\) would divide both
\(a^2+1156b^2\) and one of \(4,a,b,a^2-1156b^2\), contradicting
primitivity. At 17, if \(17\nmid a\), \(F\) is a unit; if
\(v_{17}(a)\ge2\), \(v_{17}(F)=4\); if \(a=17c\) with
\(c,b\) units, either \(c^2+4b^2\) is a unit and
\(v_{17}(F)=4\), or \(c^2-4b^2\) is a unit and
\(v_{17}(G)=3\). At 2, odd \(a\) gives odd \(F\);
\(v_2(a)\ge2\) gives \(v_2(F)=4\); and \(a=2c\),
\(c,b\) odd, gives \(F=16(c^2+289b^2)^2\) with valuation 6,
since the bracket is 2 modulo 8. The primitive cases \(a=0\) and
\(b=0\) give gcds \(34^4\) and 1. These exhaust the exceptions.
At \((a,b)=(34,1)\), the gcd attains \(C_0\).

Also \(F\ge H^4\), \(F\le C_1H^4\), and
\(|G|\le4\cdot1156H^4\le C_1H^4\), proving the second bound.
Consequently

\[
-\log C_0\le\delta_{R,j}\le\log C_1.
\tag{9}
\]

For every finite \(k\), exact telescoping gives

\[
h_0+\sum_{j=0}^{k-1}4^{-j-1}(h_{j+1}-4h_j)=4^{-k}h_k.
\]

The bounded corrections make the series absolutely convergent, so

\[
\boxed{q_R=h_0+\sum_{j\ge0}4^{-j-1}
\left(\log\rho_j-\nu_2(g_j)\log2-\nu_{17}(g_j)\log17\right).}
\tag{10}
\]

This is a derived expansion of the canonical limit, whose existence,
quadraticity and torsion properties are the cited height theorems.
Milne IV §4, Lemma 4.6, Theorem 4.7 and Lemma 4.11 establish those
facts in the same full-height normalization.
[Milne, height limit and parallelogram law](https://www.jmilne.org/math/Books/ectext6.pdf#page=129)

At \(O\), all corrections and heights are zero. For the three
two-torsion abscissas, the first duplication reaches \(O\), the first
correction is \(-4h_0\), and (10) gives zero exactly. For \(P,Q,S\)
the initial logarithms are respectively \(\log2,\log16,\log2178\).
Each actual affine point must first satisfy the curve equation;
primitivity of an arbitrary rational abscissa alone does not establish
the existence of its ordinate.

Let \(s_{R,k}=4^{-k}h_k\). Summing the entire geometric suffix in
(9) gives the uniform, all-point estimate

\[
-\frac{\log C_0}{3\cdot4^k}\le q_R-s_{R,k}
\le\frac{\log C_1}{3\cdot4^k}.
\tag{11}
\]

No finite observation of small gcds licenses a smaller universal
constant. A change of model, height convention, or coordinate reduction
must retain or rederive its correction terms.

## 3. Expanded determinant and a complete comparison tail

Put \(u_{R,0}=h_{R,0}\) and
\(u_{R,j+1}=4^{-j-1}\delta_{R,j}\). Then
\(\sum_j|u_{R,j}|<\infty\). With
\(v_j=u_{S,j}-u_{P,j}-u_{Q,j}\), products may be expanded as

\[
\mathcal R=\sum_{i,j\ge0}
\left(u_{P,i}u_{Q,j}-\frac14v_iv_j\right).
\tag{12}
\]

Absolute convergence justifies the two-index expansion and rearrangement.
Combining (1) and (12) makes the candidate identity fully explicit:

\[
\alpha\sum_{n\ge1}a_nJ_2(\alpha n)
=\Omega\sigma\sum_{i,j\ge0}
\left(u_{P,i}u_{Q,j}-\frac14v_iv_j\right).
\tag{13}
\]

This exposes the exact sums to compare; expanding both sides does not
supply the comparison.

For height cutoff \(k\), write
\(p_k=s_{P,k}\), \(q_k=s_{Q,k}\), \(s_k=s_{S,k}\),
\(b_k=(s_k-p_k-q_k)/2\), and
\(\mathcal R_k=p_kq_k-b_k^2\). Since \(C_0>C_1\), set
\(e_k=\log C_0/(3\cdot4^k)\). Each height error is at most
\(e_k\) in absolute value and the pairing error is at most
\(3e_k/2\). Expanding the product and square proves

\[
|\mathcal R-\mathcal R_k|
\le e_k(|p_k|+|q_k|+3|b_k|)+\frac{13}{4}e_k^2
=:T^{\rm ht}_k.
\tag{14}
\]

For analytic cutoff \(m\), put
\(A_m=\alpha\sum_{n=1}^m a_nJ_2(\alpha n)\), with \(A_0=0\).
If certified rationals satisfy \(0<A\le\alpha\le U\) and
\(e^{-\alpha}\le q<1\), the bounds
\(|a_n|\le2n\) and \(J_2(b)\le2e^{-b}/b^3\) give

\[
|c^{\rm an}_2-A_m|
\le\frac{4Uq^{m+1}}{A^3(m+1)^2(1-q)}=:T^{\rm an}_m.
\tag{15}
\]

One valid choice is \(q=1/(1+A)\). More efficient certified bounds
are possible, as in the prior analytic calculation. Every omitted
coefficient is covered regardless of its sign. For fixed positive
\(\sigma\), (14)–(15) imply

\[
|\mathscr D_\sigma-(A_m-\Omega\sigma\mathcal R_k)|
\le T^{\rm an}_m+\Omega\sigma T^{\rm ht}_k.
\tag{16}
\]

For execution, replace positive \(\Omega\) in the bound by a
certified upper endpoint, and evaluate finite logs, integrals and the
period with outward rounding. Equation (16) proves convergence and
enclosures. A fixed positive-width enclosure containing zero does not
establish \(\mathscr D_\sigma=0\).

## 4. A precise sufficient telescoping certificate

The two sides have different natural continuations: adding Euler terms
to \(A_m\), and doubling the three points to refine \(\mathcal R_k\).
Here is one exact contract that would connect them. It is a sufficient
criterion, not a constructed bridge for E34.

Choose explicit increasing cutoffs \(m_k\to\infty\). Define height
increments

\[
u_k=4^{-k-1}\delta_{P,k},\quad
v_k=4^{-k-1}\delta_{Q,k},\quad
w_k=\frac{4^{-k-1}\delta_{S,k}-u_k-v_k}{2}.
\]

Thus \((p_{k+1},q_{k+1},b_{k+1})=(p_k+u_k,q_k+v_k,b_k+w_k)\),
and ordinary expansion proves the exact increment identity

\[
\mathcal R_{k+1}-\mathcal R_k
=p_kv_k+q_ku_k+u_kv_k-2b_kw_k-w_k^2=:\Delta_k.
\tag{17}
\]

A sufficient certificate supplies explicit real correction potentials
\(V_k\), together with proofs of all three statements:

1. **Initial boundary:** \(A_{m_0}-\Omega\sigma\mathcal R_0=V_0\).
2. **Exact matching rule for every \(k\ge0\):**
   \[
   \alpha\sum_{m_k<n\le m_{k+1}}a_nJ_2(\alpha n)
   =\Omega\sigma\Delta_k+V_{k+1}-V_k.
   \tag{18}
   \]
3. **Terminal boundary:** a proved explicit bound
   \(|V_k|\le\eta_k\) with \(\eta_k\to0\).

By induction, (17)–(18) and the initial boundary imply
\(A_{m_k}-\Omega\sigma\mathcal R_k=V_k\) for every \(k\).
Equations (11) and (15) then permit passage to the limit; the terminal
boundary yields \(\mathscr D_\sigma=0\). This proves the certificate
criterion.

The potentials must be specified sufficiently to prove both the exact
rule and their boundary estimate without assuming the desired equality.
Defining \(V_k\) to be the observed defect makes the matching rule a
tautology and leaves the terminal boundary as the original problem.
Finite checks of (18) also do not establish its unbounded quantifier.
An applicable theorem, an exact symbolic relation valid for all stages,
or another independently justified continuation is required.

The cutoffs must cover every analytic term; each height update must
include its actual gcd; and no exceptional group point, omitted prime,
boundary term or normalization factor may disappear in the match.
This criterion would prove the real identity for the specified
\(\sigma\). Finiteness and identification of \(\sigma\) with
the actual Sha order remain part of a full-BSD proof unless the
certificate's external theorem explicitly supplies them.

## 5. Directed half-steps and coarse zero as retained operations

William's corrected signed movement is
\(0.6\to0.4\) with step \(-0.2\); its half-step is
\(-0.1\), reaching \(0.5\) without crossing the midpoint.
For a general ordered pair, \(m=(a+b)/2\) and directed gap
\(\delta=b-a\) retain both endpoints through
\(a=m-\delta/2\), \(b=m+\delta/2\). The prior
[midpoint bridge](input_source/MIDPOINT_BRIDGE.md) proves these
identities and the separate completed-L-function reflection.

These coordinate operations are exact. They do not yet specify an
intertwining map from the analytic weights \(a_nJ_2(\alpha n)\)
to the logarithmic height corrections, mixed products, period and
group factor in (13) or (18). In particular, an allowed half-step in
\(\mathbb Q\) does not establish that a half of a given point exists
in \(E(\mathbb Q)\). Duplication and inversion in the rational
elliptic-curve group have their own domains and fibers. This is a
specific missing relation to test, not an attribution of quadratic
cancellation to the user's corrected movement.

The latest whole-unit observation also has a useful typed role.
For a nonnegative real \(x\), retaining only \(\lfloor x\rfloor=0\)
keeps the entire fiber \(0\le x<1\). Retaining the fractional
remainder restores the value. The negative-input rounding rule is
not supplied by that observation. For this identity experiment,
residual and boundary terms must therefore be retained: even a
constant \(V_k=1/2\) has whole-unit readout zero at every stage,
but does not tend to zero. A coarse-zero label for a finite defect
cannot replace (18) or the terminal estimate. A hierarchy of proved
bounds tending to zero could establish exact zero; its continuation
and coverage are the load-bearing facts.

## 6. Bounded replay and result status

```powershell
python -I -B research/bsd-identity-01/work/height_series.py --output research/bsd-identity-01/evidence/height_series.json
```

The new standard-library replay passed. It performs four exact
duplications of \(P,Q,S,O\) and each two-torsion point, retaining
primitive coordinates, gcd valuations, rational \(\rho_j\) and
\(e^{\delta_{R,j}}\). Independent chord-law doubling checks each
result. Without approximating any logarithm, it verifies each finite
telescoping identity by exponentiating it after multiplication by
\(4^k\):

\[
H_0^{4^k}\prod_{j=0}^{k-1}
\left(\frac{H_{j+1}}{H_j^4}\right)^{4^{k-j-1}}=H_k.
\]

It also checks the determinant increment on eleven exact rational
inputs. These are bounded arithmetic replays of the written identities;
they do not prove general soundness of the implementation. The
universal gcd, convergence, error and certificate arguments are
written above, with the standard height and analytic theorems cited.

**Result:** equations (10), (12), (14), (17) and the sufficient
criterion are derived reformulations/proofs at their declared scope.
The E34 comparison identity (4)/(13), any actual potential satisfying
(18) with the terminal boundary, and the remaining total-Sha
identification are OPEN. No prior experiment file was edited, and
no numerical proximity or coarse-zero observation was promoted to
exact equality.
