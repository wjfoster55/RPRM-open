# Exact analytic coefficient and its normalization

Let E1:y²=x³−x and E34:y²=x³−1156x. Write Omega_c for the period
of the connected real component and Omega_all=2Omega_c for these curves.
The differential is the minimal Néron differential dx/(2y).

## 1. An exact initial scale

The positive period of E1 is

\[
\Omega_{1,c}=\int_1^\infty\frac{dx}{\sqrt{x^3-x}}.
\]

Tunnell's unconditional Theorem 3 gives L(E1,1)/Omega_(1,c)=1/4.
Its base coefficient is exactly 1: the two ternary representation counts
at 1 are both 2, so their prescribed difference is 2−2/2=1. BSD is not
assumed in that theorem. The runtime independently enumerates those
representations; positivity of the quadratic terms bounds every coordinate
by 1, so this enumeration is complete.
[Tunnell, printed pp.328–329, PDF pp.7–8](https://sites.math.rutgers.edu/~zeilberg/EM22/JT1983.pdf#page=7).

A second exact derivation is L(f32,1)=B(1/2,1/4)/8 for
f32=eta(4z)^2 eta(8z)^2. Substitution in the period integral gives
Omega_(1,c)=B(1/4,1/2)/2, again giving 1/4.
[Li–Long–Tu, Lemma 3.1](https://sigma-journal.com/2018/090/sigma18-090.pdf#page=15).

The curve E1 has conductor 32. The space S2(Gamma0(32)) has dimension 1:
the index is 48, there are 8 cusps and no elliptic fixed points, giving
genus 1. Its unique normalized newform is f32. The exact plus-symbol line
is therefore one-dimensional. We construct it with `msinit` and
`mscuspidal`, then set

\[
\phi=\frac{v}{4\,v([\infty,0])}.
\tag{1}
\]

The denominator is nonzero. Any nonzero rational rescaling of v cancels
exactly in (1), including a sign change. The program checks all symbol
relations and the Hecke eigenvalues at 2,3,5,7; coprime Hecke
multiplicativity and the U2 power relations cover the indices through
the weight-two Sturm bound 8. It also checks the
dimension and the exact normalizing path. Its generator values are

\[
(1/4,-1/2,1/4,0,-1/2,1/4,1/2,0,-1/4).
\]

In particular, phi on any rational cusp path lies in (1/4)Z: the chosen
paths generate the degree-zero divisor module over Gamma0(32), and the
weight-two target has trivial coefficient action. This supplies the
integrality needed in the independent error proof below.

PARI's convenient `msfromell` takes a different route: its
`msfromell_scale` reconstructs a rational from numerical L-values and
periods. That branch was inspected and bypassed entirely in the accepted
program. The initial exploratory call using it is retained with an explicit
lower evidence grade. Formula (1) uses the exact cuspidal subspace directly.
The relevant official source files are included under `dependencies/pari/`.

## 2. Twisting and the factor 2

The primitive quadratic character psi has fundamental discriminant 136,
because136=4·34 with 34 squarefree and congruent to2 modulo 4. Its Gauss
sum is tau(psi)=sqrt(136)=2sqrt(34), and psi(5)=1. Let

\[
\lambda_D(r)=\sum_{b\bmod136}\psi(b)\phi([\infty,r+b/136]).
\tag{2}
\]

The usual finite Gauss-sum identity follows by expanding the Fourier
series under these translations; each coefficient acquires
sum_b psi(b)e^(2pi i nb/136)=tau(psi)psi(n). It remains valid for
coefficients with nonunit n, when both character sides vanish. Thus (2)
is tau(psi) times the twisted cusp integral divided by Omega_(1,c).

The map x=34X, y=34sqrt(34)Y scales dx/(2y) by 1/sqrt(34), so
Omega_(34,c)=Omega_(1,c)/sqrt(34). Therefore

\[
\lambda_D(r)=2\,[\infty,r]_{E34,\Omega_c}.
\tag{3}
\]

The GP minimal-model computation separately checks that twisting E1 by 136
and minimizing gives precisely E34, of conductor 18496. Since psi(5)=1,
the 5-adic unit root is unchanged: alpha²+2alpha+5=0, alpha=3 mod 5.
No extra8/5 Euler factor belongs in the twist-period conversion.

The extra rank-zero control D=8 checks the same factor 2: after removing
its ordinary interpolation factor, the computation returns 1+O(5^7).
The exact raw value 1 and minimal E2 connected-period value 1/2 follow
from the Gauss-sum conversion and the even case of Tunnell's theorem,
with first coefficient 1. The finite computation checks those exact
identities to its reported precision; it does not establish them by
agreement. This is a calibration against an exact analytic identity.

## 3. Two analytic computations

The overconvergent calculation starts with the exact symbol (1), computes
twisted moments at levels6,8,10, then evaluates its logarithmic second
derivative and its T² coefficient separately. The ordinary control theorem
and filtration bounds justify the reported precision; increasing precision
agreement is a consistency check, not that error theorem.
[Belabas–Perrin-Riou, §§2–4](https://arxiv.org/pdf/2101.06960).

The second algorithm uses only classical symbols. For n≥1 and 5 not
dividing a, define

\[
\mu(a+5^n\mathbf Z_5)
=\alpha^{-n}\left(\lambda_D(a/5^n)
-\alpha^{-1}\lambda_D(a/5^{n-1})\right).
\tag{4}
\]

The T5 eigenrelation implies finite additivity of(4). In the sum over
five children, the identity a5−5/alpha=alpha reduces their total to the
parent. Every value is 5-integral because lambda_D belongs to(1/4)Z and
alpha is a unit. Thus (4) defines a bounded Z5-valued measure on Z5 units.
It is the ordinary stabilized measure of the twisted symbol. This
algorithm calls no overconvergent-moment or p-adic-L evaluation function.

Let Draw=integral log5(x)^2 dmu. On a residue ball a+5^n Z5,
log5(x)−log5(a) belongs to5^n Z5, while log5(a) belongs to5Z5.
Expanding the square shows that their squared-log difference lies in
5^(n+1)Z5. Boundedness of the measure then gives the uniform bound

\[
D_{\rm raw}-
\sum_{a\in (\mathbf Z/5^n)^\times}
\log_5(a)^2\mu(a+5^n\mathbf Z_5)
\in5^{n+1}\mathbf Z_5.
\tag{5}
\]

All residue units and all character terms are enumerated. Arithmetic uses
20-digit 5-adic roots/logarithms, well beyond the precision claimed in (5).
No archimedean approximation is involved. The resulting certificates are

| n | Draw residue | Proven modulus |
|---|---:|---:|
| 2 | 100 | 125 |
| 3 | 225 | 625 |
| 4 | 2725 | 3125 |
| 5 | 2725 | 15625 |

Both analytic algorithms use the same exact classical symbol. Their
integration algorithms and error justifications are different.

## 4. Derivative, degree and period conversions

Set T=gamma−1, with the cyclotomic character of gamma equal to6, and
ell=log5(6). Let F34(T)=b2 T²+O(T³) in the connected-period convention.
The lower coefficients vanish exactly by the previously established
[algebraic rank 2](dependencies/ARITHMETIC_PROOF.md) and
[BKS Proposition 6.1](https://kurihara.math.keio.ac.jp/bks4.pdf#page=41),
not because their finite residues were zero. The
[Hypothesis 2.2 audit](dependencies/PADIC_HEIGHT_AUDIT.md#bks-admission-and-nonvanishing-transport)
supplies the admitted rank, irreducibility, freeness and finite 5-primary
Sha conditions. These are attributed earlier proofs, not fresh results
of this coefficient computation.

Under T(s)=exp(ell s)−1, the second derivative at s=0 is 2ell²b2.
Together with the twist factor 2 in (3), this gives

\[
\boxed{b_2=\frac{D_{\rm raw}}{4\log_5(6)^2}.}
\tag{6}
\]

The denominator4 records two different operations: derivative factorial 2
and twist-period 2. Since v5(log5(6))=1, converting(5) costs two digits.
The final independently checked enclosure is therefore

\[
\boxed{b_2\in426+625\mathbf Z_5,\qquad
 b_2=1+2\cdot5^2+3\cdot5^3+O(5^4).}
\tag{7}
\]

Equation (7) specifies a ball containing the exact coefficient, not exact
equality with the integer426. The all-real-components normalization would
give b2/2, whose residue is 213 modulo 625; this is a different declared
normalization. Omitting the twist correction gives227 modulo 625 instead.
The runtime preserves both as distinguishing controls.

## 5. Consequences and remaining comparison

In the BKS convention, A_xi=(Omega_(34,c)/Omega_xi)b2. Its S-truncated
interpolation already absorbs the good5 Euler factor: with beta=5/alpha,
C5^(-1)·(8/5)=(1−alpha^(-1))². Hence no further8/5 multiplies b2
when identifying A_xi. The period ratio is explicit, not silently set to1.
[BKS, §§2.1 and 6.1](https://kurihara.math.keio.ac.jp/bks4.pdf#page=40).

The new coefficient is a unit, so the p-adic analytic order is exactly 2.
It also makes A_xi nonzero. Theorem 6.2 then pairs the canonical derived
class against a point with nonzero formal logarithm to give a nonzero
value; therefore that class is nonzero under the previously checked
hypotheses. The exact real/p-adic scalar identity is still a separate
obligation in Corollary 6.7.
[BKS, Proposition 6.1, Theorem 6.2 and Corollary 6.7](https://kurihara.math.keio.ac.jp/bks4.pdf#page=41).

The fresh rational-point calculation again gives R_MST=3 mod 5. Under
the admitted MST scalarization log5/5, a rank-two regulator changes by
the square of the logarithmic coordinate factor. Define the component
comparison scalar explicitly by

\[
\Lambda_c=\frac{C_5D_{\rm raw}}{100R_{\rm MST}},\qquad
5\Lambda_c=1\pmod5.
\tag{8}
\]

Here100=2·2·25: twist, factorial, and the rank-two MST log factor.
The BKS scalar is (Omega_(34,c)/Omega_xi)Lambda_c. This computation
has determined its component-normalized first digit, not its equality
with a real BSD quotient. Total Sha and the full/general BSD identity
remain OPEN.
