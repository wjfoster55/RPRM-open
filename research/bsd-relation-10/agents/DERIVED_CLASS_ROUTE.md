# E34: the canonical derived class has a computable primitive digit

Prepared 2026-09-12. This is a new written consequence of the admitted
E34 arithmetic and the proved generalized Rubin formula. It uses no
Generalized Perrin–Riou conjecture, main conjecture, or BSD identity.

After an explicit connected-period normalization and the degree-one
height-sign transport described below, the canonical BKS derived class is
an integral primitive vector and satisfies

\[
\boxed{K_c^{\rm MST}\equiv 3Q\pmod{5M}},\qquad
M=\mathbf Z_5\otimes E(\mathbf Q)_{\rm tf}.
\]

This is a digit of a **specified transport** of the canonical class, not
an unqualified assertion that the raw BKS tensor is the rational point
\(3Q\). Its computation uses the analytic coefficient through a proved
reciprocity formula. Consequently it is not an independently arithmetic
test of the conjectural real scalar comparison.

## Contract and supplied evidence

The curve and ordered full free basis are

\[
E:y^2=x^3-1156x,\quad P=(-2,48),\quad Q=(-16,120),\quad
\omega=dx/(2y),\quad p=5.
\]

The minimal equation, torsion, rank, basis and primary-Sha conclusions are
attributed prior results. Relevant exact sources are
[the full-basis proof](../../bsd-identity-01/input_source/GENERATOR_PROOF.md),
[the 5-primary trace proof](../../bsd-trace-02/TRACE_CALCULATION.md), and
[the BKS height admission](../../bsd-coefficient-05/dependencies/PADIC_HEIGHT_AUDIT.md).
Their original computations were inspected as dependencies, not rerun here.

The target carrier is \(M\otimes\mathbf Q_5\), with its actual integral
lattice retained, and the BKS augmentation lines
\(\mathscr Q^j=\mathbf Q_5\otimes I^j/I^{j+1}\).
Vector equality, reduction modulo \(5M\), and collinearity are different
receivers. The forward class readout is enabled by the theorem hypotheses
and the nondegenerate height. The exact class is canonical, but its full
coordinates are not computed here: that numerical task is OPEN. The
complete preimage of its displayed *reduction* is \(3Q+5M\); this does not
claim that every vector in that coset is a canonical class for this curve.

The supplied arithmetic and analytic residues are

\[
G_{\rm MST}\equiv\begin{pmatrix}1&2\\2&2\end{pmatrix},\quad
R=\det G_{\rm MST}\equiv3,\quad
\frac{\ell}{5}\equiv\binom22\pmod5,
\tag{1}
\]

where \(\ell=(\log_\omega P,\log_\omega Q)^t\), and

\[
b_2\in2301+3125\mathbf Z_5.
\tag{2}
\]

For (1), the earlier exact point calculation gives
\(t(8P)=t(8Q)=5\bmod25\), and the formal logarithm's omitted terms vanish
at the required precision. The height is the MST bilinear convention
\(B(X,Y)=h_5(X)+h_5(Y)-h_5(X+Y)\), with functional
\(\log_5\chi_{\rm cyc}/5\). Thus its matrix is not the half-polarized
matrix. See [the normalization and exact residues](../../bsd-coefficient-05/dependencies/PADIC_HEIGHT_AUDIT.md).

For (2), the source is [experiment 06, §7](../../bsd-carry-key-06/OPERATIONAL_PROOF.md)
and its [analytic log](../../bsd-carry-key-06/runs/fresh_validation/logs/analytic.log).
The log contains classical level-six and overconvergent residues 2301
modulo 3125. The proof supplies the classical error, not agreement alone.
The normalization is the connected real period \(\Omega_c\), the trivial
Teichmüller branch and \(T=\gamma-1\), \(\chi_{\rm cyc}(\gamma)=6\).

## The published bridge and its hypotheses

BKS Theorem 6.2(i) gives the first formula below; Theorem 5.6 gives the
second. These are theorems under Hypothesis 2.2, for the good ordinary
case used here. Their class is the Iwasawa–Darmon derivative of Definition
4.5; their analytic coefficient lies in \(I^2/I^3\), not an ordinary
second derivative. [BKS, §§5.2 and 6.2](https://kurihara.math.keio.ac.jp/bks4.pdf#page=34).

\[
\langle x,\kappa_\infty\rangle_5
 =C_5\log_\omega(x)\mathcal L^{(2)}_{S,5},\qquad
\langle x,R^{\rm Boc}_\omega\rangle_5
 =\log_\omega(x)R_5.
\tag{3}
\]

Here \(S=\{\infty,2,5,17\}\),
\(\alpha^2+2\alpha+5=0\), \(\alpha\equiv3\pmod5\),
\(\beta=5/\alpha\), and
\(C_5=(1-\alpha^{-1})^{-1}(1-\beta^{-1})\).

The hypothesis admission is concrete. The discriminant has prime support
\(\{2,17\}\), and \(\#E(\mathbf F_5)=8\), so 5 is good ordinary.
Frobenius at 3 has polynomial \(X^2+3\), irreducible modulo 5; hence
\(E[5]\) is irreducible. This supplies the Tate-module choice and
freeness in Hypothesis 2.2(i). Rank two and finite 5-primary Sha are the
earlier arithmetic and trace results. Neither residual surjectivity nor
a non-CM assumption is introduced. The full integral basis and (1)
supply the invertible pairing. These are exactly the inputs needed here;
BKS's finite-level large-image theorem is not substituted for (3).

## Period, sign and degree transport

Write \(d=\log_5(6)/5\in\mathbf Z_5^\times\), and let
\(\rho:\mathscr Q^1\to\mathbf Q_5\) send \(T\) to \(d\).
Retain the comparison sign \(\epsilon\in\{1,-1\}\) by writing

\[
\rho(\langle x,y\rangle_5)=\epsilon B_{\rm MST}(x,y).
\]

The ordinary height comparison and its convention boundary are the
attributed [prior audit](../../bsd-coefficient-05/dependencies/PADIC_HEIGHT_AUDIT.md#bks-admission-and-nonvanishing-transport).
The original Nekovář PDF could not be fetched through the web reader in
this audit; its exact signed comparison was not newly re-proved. BKS
Remark 5.2 independently confirms the cited comparison location.

Define \(\rho_{\rm MST}=\epsilon\rho\). This is a declared orientation of
the one-dimensional tensor line, chosen to transport the pairing to the
named MST convention. Its degree-two transport is \(\rho^2\), since
\(\epsilon^2=1\). No sign of the unknown class is selected by looking at
the desired digit.

Set \(c_\xi=\Omega_c/\Omega_\xi\ne0\) and define

\[
K_c^{\rm MST}=c_\xi^{-1}
 (\mathrm{id}\otimes\rho_{\rm MST})(\kappa_\infty).
\tag{4}
\]

The exact analytic normalization identifies
\(\mathcal L^{(2)}_{S,5}=c_\xi b_2T^2\).
Its good-5 Euler factor is already incorporated: one checks
\(C_5^{-1}(8/5)=(1-\alpha^{-1})^2\).
The additive primes 2 and 17 supply no nontrivial local Euler polynomial.
Thus an extra \(8/5\) must not be attached to \(b_2\).
See [the coefficient proof, §§2–5](../../bsd-coefficient-05/COEFFICIENT_PROOF.md)
and [BKS's interpolation convention](https://kurihara.math.keio.ac.jp/bks4.pdf#page=41).

Apply degree-two transport to the first equation of (3), then divide by
\(c_\xi\). The result is the exact scalar equality

\[
B_{\rm MST}(x,K_c^{\rm MST})
 =C_5b_2d^2\log_\omega(x).
\tag{5}
\]

This step explains both why the period disappears from the *normalized*
class and why the height sign cannot simply be suppressed in the raw class.

## Exact reconstruction and its first primitive digit

Let

\[
w=\operatorname{adj}(G_{\rm MST})\ell,\qquad
W=w_1P+w_2Q,\qquad
\Lambda_c=\frac{C_5b_2d^2}{R}.
\]

Since \(G_{\rm MST}\) is invertible, the two equations obtained by using
\(x=P,Q\) in (5) have exactly one vector solution. Thus

\[
\boxed{K_c^{\rm MST}=\Lambda_c W}.
\tag{6}
\]

This is stronger than nonvanishing or collinearity. It gives the actual
multiplier relative to independently defined arithmetic data, as a
5-adic analytic/arithmetic ratio. It does not identify that multiplier
with the archimedean BSD ratio.

The residue of \(5\Lambda_c\) can be verified directly rather than imported:

\[
5C_5=\frac{\alpha(5-\alpha)}{\alpha-1}\equiv3,\qquad
d\equiv1,\quad b_2\equiv1,\quad R\equiv3\pmod5.
\]

Consequently \(s:=5\Lambda_c\) is a unit with \(s\equiv1\pmod5\).
The adjugate calculation from (1) gives

\[
\frac w5\equiv
\begin{pmatrix}2&-2\\-2&1\end{pmatrix}\binom22
=\binom03\pmod5.
\]

Equation (6) is therefore \(K_c^{\rm MST}=s(W/5)\). In particular
\(K_c^{\rm MST}\in M\setminus5M\), and its reduction is \(3Q\).
As a direct two-equation check,
\(\left(\begin{smallmatrix}1&2\\2&2\end{smallmatrix}\right)
\binom03=\binom11\) modulo 5, while the right side of (5) is
\((5C_5)b_2d^2(\ell/5)=3\binom22=\binom11\).

A fresh Python integer check evaluated these displayed modular formulas
and enumerated all 25 vectors in \((\mathbf Z/5)^2\): the complete
solution fiber of \(Gv=(1,1)^t\) was exactly \(\{(0,3)^t\}\).
This checks the finite linear algebra from supplied residues; it is not a
fresh execution of the earlier curve or analytic algorithms.

For the raw scalarization \((\mathrm{id}\otimes\rho)\kappa_\infty\),
the exact answer is \(\epsilon c_\xi K_c^{\rm MST}\). A residue of this
raw object requires the explicit period factor and sign. They are not
claimed to be 1. The normalized vector proof above has no such omitted
port.

## A proved CM simplification for the next height calculation

There is a short exact way to eliminate the potentially troublesome cubic
sigma term. It needs no guess that the Eisenstein constant vanishes.

MST Theorem 1.3 uniquely specifies a pair \((\sigma,c)\), with
\(\sigma\in t\mathbf Z_5[[t]]\) odd and normalized by its linear term,
satisfying \(x+c=-D^2\log\sigma\), where \(D=d/\omega\).
Their equation (1.9) identifies
\(c=(a_1^2+4a_2-E_2(E,\omega))/12\).
[MST, Theorem 1.3 and §1.1](https://wstein.org/papers/pheight/pheight.pdf#page=4).

Choose \(i\in\mathbf Z_5\) with \(i^2=-1\). The automorphism
\([i](x,y)=(-x,iy)\) sends \(t\) to \(it\) and pulls \(\omega\) back
to \(i\omega\). Writing \(\omega=A(t)dt\), this gives
\(A(it)=A(t)\), while \(x(it)=-x(t)\).
Put \(\widetilde\sigma(t)=i^{-1}\sigma(it)\). The chain rule gives

\[
-D^2\log\widetilde\sigma(t)=x(t)-c.
\]

The transformed series is again odd, integral and has linear term \(t\).
Uniqueness therefore forces \(c=-c=0\) and
\(\sigma(it)=i\sigma(t)\). Only powers \(t^{4j+1}\) can occur. In
particular

\[
\boxed{\sigma(t)/t\in1+t^4\mathbf Z_5[[t]],\qquad E_2(E,\omega)=0.}
\tag{7}
\]

This is a written deduction from the published uniqueness theorem and the
explicit automorphism. It is not a numerical E2 recognition. For
\(t(8X)\in5\mathbf Z_5\), the sigma correction contributes only
\(5^3\mathbf Z_5\) to the MST height after division by \(5\cdot8^2\).
Thus rational coordinates alone, with a rigorously truncated logarithm,
now suffice for the height modulo 125.

A concrete next calculation is to compute \(u=t(8X)/d(8X)\bmod625\)
for \(X=P,Q,P+Q\), use
\(\log_5u=\frac14\log_5(u^4)\), and retain the terms through degree
three in \(u^4-1\). All terms from degree four onward have valuation at
least four. Divide by \(5\cdot8^2\) to obtain the height modulo 125.
The denominator includes every rational prime, just as in the previous
height proof. Recompute the Gram determinant and \(\ell/5\) at matching
precision, then evaluate (6) using the already certified analytic digits.
That produces additional class digits without requiring a new central
L-value theorem. The parent relation-10 lane owns any fresh execution of
this calculation; this note does not assert its output in advance.

## Exact obstruction to treating this as a BSD test

The pairing in (5) is invertible. Computing \(K_c^{\rm MST}\) from its
right side and then using the same pairing to recover \(b_2\) is therefore
an exact inverse calculation. It cannot provide an independent equality
between \(\Lambda_c\) and a real quotient: its input already contains
\(b_2\), and it introduces no archimedean data.

BKS Corollary 6.7, with nonzero regulator, makes the real-to-p-adic scalar
identity equivalent to their Generalized Perrin–Riou comparison. That
comparison remains a new obligation; it is not an extra conclusion of
Theorem 6.2. [BKS, Corollary 6.7](https://kurihara.math.keio.ac.jp/bks4.pdf#page=43).

Hostile cases retain the boundary. Using the other Frobenius root changes
the allowed ordinary branch. Using half-polarized heights changes the
matrix and class transport. Dropping \(c_\xi\) or the sign changes the raw
tensor digit. Finally \(3Q+5P\) has the same displayed reduction as \(3Q\)
and generally a different exact direction: one residue does not recover
the full class. Full BSD, total Sha and the exact real identity remain
OPEN. Evidence here consists of cited theorems, attributed earlier finite
certificates, new finite linear algebra, and the written transport and CM deductions, not a
formal proof-assistant verification.
