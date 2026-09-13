# Independent review of the modulo-125 reciprocity readback

Prepared 2026-09-12. **No formula, sign, multiplier or admitted-precision
defect was found in the reviewed calculation.** The certified normalized
class readout is

\[
\boxed{K_c^{\rm MST}\equiv50P+58Q\pmod{125M}}.
\]

This strengthens the primitive digit \(3Q\bmod5M\). It is the same
period-normalized, MST-oriented class defined in
[DERIVED_CLASS_ROUTE.md](DERIVED_CLASS_ROUTE.md), reconstructed through
the proved BKS formula. It is not a new independent computation of Kato
cochains or a proof of the real scalar comparison.

## Reviewed objects and independent checks

Reviewed [reciprocity.py](../work/reciprocity.py),
[analytic.gp](../work/analytic.gp), the runner, and
[the fresh receipt](../runs/fresh-01/RUN.json),
[analytic log](../runs/fresh-01/logs/analytic.log), and
[arithmetic evidence](../runs/fresh-01/evidence/reciprocity.json).
The recorded source snapshots equal the current source bytes, and their
SHA-256 values match the receipt. The evidence JSON hash also matches.
These checks bind the inspected bytes to the receipt; they do not prove
the mathematics.

Without rerunning the analytic pipeline or calling the producer's
arithmetic functions, a fresh Python `Fraction` calculation read each
recorded \((a,b,d)\), checked
\(b^2=a^3-1156ad^4\), reconstructed \(t=-ad/b\) and \(u=-a/b\), and
independently evaluated the displayed truncated logarithm. It recovered:

| Point | \(u\bmod625\) | \(h_5\bmod125\) | \(\log_\omega/5\bmod125\) |
|---|---:|---:|---:|
| \(P\) | 384 | 92 | 117 |
| \(Q\) | 19 | 4 | 102 |
| \(P+Q\) | 444 | 64 | 94 |

The elliptic curve doubling implementation was inspected: it treats the
identity, inverse pair and torsion doubling separately and checks the
curve equation for every newly constructed affine point. The fresh
readback above verifies the stored coordinate outputs and local formulas;
it does not claim an independently implemented replay of all doublings.

## Arithmetic and analytic normalization

For \(z=u^4-1\bmod625\), the arithmetic script uses

\[
h_5(X)\equiv
\frac{z-z^2/2+z^3/3}{20\cdot64}\pmod{125},\qquad
\frac{\log_\omega(X)}5\equiv\frac{t(8X)}{40}\pmod{125}.
\]

The factor 20 is \(4\cdot5\): Teichmüller removal by the fourth power
and the MST logarithm normalization. The factor 64 is \(8^2\).
The integral coordinate denominator retains its non-5 factors. The
required formal-group condition and nonsingular bad-prime reductions are
checked in the source. Torsion killed by 8 is assigned height and logarithm
zero before any local parameter division.

The independent [sigma audit](SIGMA_AUDIT.md) proves both omitted tails
vanish modulo 125 after the specified divisions. In the scalar logarithm
tail, \(n-v_5(n)\ge4\) for every \(n\ge4\); hence discarding these terms
before division by 5 is valid modulo 625. The elliptic formal logarithm's
tail is evaluated with its valuation bound, not incorrectly treated as a
coefficientwise integral series after a single multiplication by 5.

The analytic script constructs the same exact period-anchored modular
symbol as experiment 05 and uses the quadratic twist discriminant 136.
Its classical level-four error is \(5^5\) in \(D_{\rm raw}\); division
by \(4\log_5(6)^2\) leaves precision \(5^3\). The denominator 4 contains
the factorial and twist-period factors, each equal to 2. The separate
overconvergent integration agrees at this precision. The two integrations
share their classical symbol, as the receipt discloses. Rank-zero period
controls check the scale against the previously established exact anchors.

The new log gives

\[
b_2\equiv51,\quad 5C_5\equiv83,\quad
d=\log_5(6)/5\equiv111\pmod{125}.
\]

Thus \(A:=5C_5b_2d^2\equiv43\). The MST matrix, determinant and
logarithm vector are

\[
G=\begin{pmatrix}66&32\\32&117\end{pmatrix},\quad
R\equiv73,\quad \ell_5=\binom{117}{102}\pmod{125}.
\]

Direct finite calculation gives

\[
\operatorname{adj}(G)\ell_5=\binom{50}{113},\qquad
5\Lambda_c=A/R\equiv16,\qquad
K=16\binom{50}{113}=\binom{50}{58}\pmod{125}.
\]

The independent check enumerated all 15,625 vectors of
\((\mathbf Z/125)^2\). Exactly one solves
\(Gv=A\ell_5=(31,11)^t\), namely \((50,58)^t\). This is a complete
finite ONE fiber. Its complete lift fiber in the original lattice is
\(50P+58Q+125M\); a representative of that coset is not the exact class.

The sign convention remains in the definition of the class, not in a
post-processing choice of its digit. With \(\rho(T)=d\),
\(\rho(\langle-,-\rangle_{\rm BKS})=\epsilon B_{\rm MST}\), and
\(c_\xi=\Omega_c/\Omega_\xi\), the computed object is
\(K=c_\xi^{-1}(\mathrm{id}\otimes\epsilon\rho)\kappa_\infty\).
Consequently the raw \(\rho\)-scalarization is \(\epsilon c_\xi K\).
The arithmetic script correctly does not label its output as that raw
class. The comparison-sign theorem itself remains the attributed earlier
height audit, with the limitation disclosed in DERIVED_CLASS_ROUTE.md.

## Basis invariance: the exact class is stronger than its adjugate vector

The proposed stronger basis statement is valid. Work over
\(V=\mathbf Q_5\otimes E(\mathbf Q)_{\rm tf}\), fix the analytic scalar
\(A=5C_5b_2d^2\), and use column bases \(\mathcal B\) and
\(\mathcal B'=\mathcal B U\), where \(U\in\mathrm{GL}_2(\mathbf Q_5)\).
Then

\[
G'=U^tGU,\qquad \ell_5'=U^t\ell_5.
\]

The reconstructed class in the new coordinates is
\(k'=A(G')^{-1}\ell_5'\). As an actual vector in the old coordinates,

\[
Uk'=A\,U(U^tGU)^{-1}U^t\ell_5
   =AG^{-1}\ell_5=k.
\tag{1}
\]

This proves invariance for every invertible \(\mathbf Q_5\) basis change,
including proper finite-index rational sublattices. No determinant-one
condition is needed for the class reconstruction.

The distinction from the arithmetic adjugate vector is material:

\[
U\operatorname{adj}(G')\ell_5'
 =\det(U)^2\operatorname{adj}(G)\ell_5,\qquad
\frac A{\det G'}=\det(U)^{-2}\frac A{\det G}.
\tag{2}
\]

Thus the \(W/5\) vector scales by the index squared, while the multiplier
\(5\Lambda_c\) scales by its reciprocal. Their product is invariant.
The executed index-two control illustrates this: \(W/5\) changes from
\((50,113)\) to \((75,77)\), which is four times the old vector modulo
125; the reconstructed class pushed to the original basis stays
\((50,58)\).

Equations (1)–(2) use exact field arithmetic. Finite precision has a
separate admission rule. If \(U\in\mathrm{GL}_2(\mathbf Z_5)\), it
preserves \(M\) and its modulo-125 receiver, so the current modular
matrix solver applies. An index prime to 5, such as 2, satisfies this.
If the index is divisible by 5, \(\det G'=\det(U)^2\det G\) is no
longer a unit; inversion in \(\mathbf Z/125\) is unavailable and the
script correctly rejects it. This does not contradict exact equation (1).

For example \(U=\operatorname{diag}(5,1)\) gives exact new coordinates
\((k_P/5,k_Q)\). Knowing only \(k_P=50\bmod125\) determines
\(k_P/5=10\bmod25\), not modulo 125. Also \(125M'\) is a different
lattice from \(125M\). Additional digits, tracked denominators and the
transported lattice are necessary before attaching an equally precise
new-coordinate residue. The theorem survives; the old finite inversion
contract does not silently extend to that basis.

## Review ceiling

The new residue and general basis law are established at the stated
normalization and precision. The reviewed controls cover the sign change,
shear, swap, index-two basis change, torsion, and additional point
combinations; they support the implementation without replacing the
written all-basis identity. No expensive pipeline was reexecuted in this
review. No previous pack or source file was edited. The exact real
comparison, total Sha and full BSD remain OPEN.
