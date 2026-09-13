# E34: independent audit of the 5-adic height certificate

Prepared 2026-09-12. The proposed residue calculation is valid. The
half-polarized determinant is `2 mod 5`; the **Mazur–Stein–Tate (MST)
bilinear regulator** has determinant `3 mod 5`. Both are nonzero. Combining
this result with the previously established rank and 5-primary Sha result
also establishes nonvanishing of the Bockstein regulator in
Burns–Kurihara–Sano (BKS), Definition 4.10. This audit does not establish
either of their remaining main-conjecture or Generalized Perrin–Riou
inputs.

## Contract and dependencies

The carrier is the fixed rational curve

`E: y^2=x^3-1156x`, `P=(-2,48)`, `Q=(-16,120)`, `p=5`,

with its globally minimal equation and differential `omega=dx/(2y)`.
Point equality is elliptic-curve equality; a point and its occurrence in a
sum remain distinct roles. The target is a scalar 5-adic cyclotomic
regulator and then the nonzero readout of a specified cohomological
regulator. Neither is the real Néron–Tate regulator.

The local-model and Tamagawa dependencies are
[LOCAL_ANALYTIC_INPUTS.md](../bsd-identity-01/input_source/LOCAL_ANALYTIC_INPUTS.md).
The full rank-two basis is an attributed result of
[GENERATOR_PROOF.md](../bsd-identity-01/input_source/GENERATOR_PROOF.md).
The established `Sha(E/Q)[5^infinity]=0` is imported from
[TRACE_CALCULATION.md](../bsd-trace-02/TRACE_CALCULATION.md), with its
[formula and orbit audit](../bsd-trace-02/TRACE_FORMULA_AUDIT.md).
These earlier proofs were read here, not rerun or newly proved by this audit.

The new finite receiver retains residues modulo 5 and a nonzero
determinant. A residue does not recover the exact 5-adic scalar: its
complete scalar preimage is its congruence class. The nonzero readout is
nevertheless constant on a nonzero residue class. A zero residue would
leave nonvanishing OPEN at this precision.

## Formula and normalization

MST use `log_5(5)=0`, the cyclotomic functional
`rho=(1/5)log_5(chi_cyc)`, and

\[
h_5(R)=\frac{1}{5m^2}
 \log_5\!\left(\frac{\sigma(t(mR))}{d(mR)}\right),\qquad t=-x/y.
\]

Here `mR` must lie in the formal group at 5 and in the identity component
at every bad prime; `d` is the positive denominator square root in the
minimal model. Their bilinear pairing is
`B(R,U)=h_5(R)+h_5(U)-h_5(R+U)`, so `B(R,R)=-2h_5(R)`.
[MST, equation (1.1), pp. 586–588, and Algorithm 3.4, p. 600](https://wstein.org/papers/pheight/pheight.pdf#page=3).

The half-polarization used in the proposed calculation is instead

\[
H(R,U)=\frac{h_5(R+U)-h_5(R)-h_5(U)}2,
\qquad B=-2H.
\]

This distinction changes the named residue, not the nonvanishing result.
The factor `1/5` is equally material to the residue: using `log_5` without
this factor multiplies every entry by 5 and the rank-two determinant by
25. Such a regulator is still nonzero over `Q_5`, but is no longer a
5-adic unit in that normalization.

Harvey explicitly uses a quadratic height equal to `2p` times MST's
height. Thus at 5 his quadratic height is `10h_5`, and its
half-polarized pairing is `10H=-5B`.
[Harvey, introduction and equation (3)](https://arxiv.org/pdf/0708.3404#page=2).
No source or software output with that convention may be compared to
`h_5 mod 5` without this conversion.

## Admission and the exact truncation argument

The inherited minimal discriminant is `2^12*17^6`, so 5 is good.
Direct enumeration gives

`E(F_5)={O,(0,0),(1,0),(2,1),(2,4),(3,2),(3,3),(4,0)}`.

Consequently `#E(F_5)=8` and `a_5=-2`, which is nonzero modulo 5;
5 is ordinary. The inherited component orders are `c_2=c_17=4`.
Thus `m=lcm(8,4,4)=8` meets the point-preparation conditions for every
rational point. In particular, `5` does not divide `m`.

MST's sigma theorem supplies integral coefficients and oddness under
elliptic-curve inversion. Harvey clarifies that the general `t^2`
coefficient is `a_1/2`.
[MST, Theorem 1.3](https://wstein.org/papers/pheight/pheight.pdf#page=4),
[Harvey, §4, p. 7](https://arxiv.org/pdf/0708.3404#page=7).
For our equation, `a_1=a_3=0`, so inversion sends `(x,y)` to `(x,-y)`
and sends `t` exactly to `-t`. Therefore

\[
\sigma(t)=t+t^3 A(t^2),\quad A\in\mathbf Z_5[[t]],
\qquad\frac{\sigma(t)}t\in1+t^2\mathbf Z_5[[t]].
\]

This is sufficient; no value of the Eisenstein constant or a higher
sigma coefficient is needed. If `t in 5Z_5`, then
`sigma(t)/t in 1+25Z_5`. Its logarithm lies in `25Z_5`, and division by
`5m^2=320` leaves an error in `5Z_5`. These bounds cover the entire
uncomputed tail, rather than a finite list of coefficients.

Write `8R=(a/d^2,b/d^3)` in reduced form with `d>0`.
Since `t=-ad/b`, the unit in the remaining logarithm is

\[
u=t/d=-a/b\in\mathbf Z_5^\times.
\]

To evaluate it from a residue, use `u^4 in 1+5Z_5` and

\[
\log_5 u=\tfrac14\log_5(u^4)
\equiv\tfrac14(u^4-1)\pmod{25\mathbf Z_5}.
\]

Indeed, the `n`th logarithm term for `n>=2` has valuation at least
`n-v_5(n)>=2`. Hence

\[
\boxed{\quad
h_5(R)\equiv\frac{u^4-1}{20m^2}\pmod{5\mathbf Z_5}.
\quad}
\]

The right side depends only on `u mod 25`: changing the lift by `25k`
changes its fourth power by a multiple of 25, which becomes a multiple
of 5 after division by 5. In executable integer arithmetic, divide
`u^4-1` by 5 and then multiply by the inverses of 4 and `m^2` modulo 5.
Integer division by 20 is not valid for arbitrary representatives.

The positive choice of `d` pins the rational coordinate convention.
Changing a coherent denominator sign merely contributes `log_5(-1)=0`;
arbitrarily changing just one normalized coordinate is not the same
operation. The complete integer `d` includes its factors at all primes.
Keeping only its 5-power part would discard the non-p local contribution
and generally change the height. The identity `t/d=-a/b` retains that
contribution exactly.

## Independent finite arithmetic

An independent Python `Fraction` calculation in this audit used the
short-Weierstrass chord-and-tangent law and three exact doublings per
point. It recovered

`P+Q=(2178/49,65472/343)`

and the following data, with reduced `a,b,d` independently checked against
the rational coordinates and curve equation:

| R | a mod 25 | b mod 25 | d mod 25 | v_5(t(8R)) | u mod 25 | h_5(R) mod 5 |
|---|---:|---:|---:|---:|---:|---:|
| P | 21 | 6 | 20 | 1 | 9 | 2 |
| Q | 16 | 11 | 20 | 1 | 19 | 4 |
| P+Q | 16 | 11 | 15 | 1 | 19 | 4 |

All three denominators have positive 2-adic valuation (`4,4,6`), so
the three points reduce to `O` at 2. At 17 their denominators are units
and their reductions are `(9,7),(4,9),(13,15)`; these are nonsingular
points of `y^2=x^3` because their y-coordinates are nonzero. This is an
additional direct check of the bad-prime point preparation.

The resulting matrices are

\[
H\equiv\begin{pmatrix}2&4\\4&4\end{pmatrix},\quad
\det H\equiv2\pmod5,
\qquad
B\equiv\begin{pmatrix}1&2\\2&2\end{pmatrix},\quad
\det B\equiv3\pmod5.
\]

Thus the scalar cyclotomic pairing is nondegenerate on the rank-two
Mordell–Weil space. The independent calculation confirms the supplied
residues; the parent lane owns the durable executable replay. This file
does not claim that an inline check is an independently implemented
general p-adic height algorithm.

## BKS admission and nonvanishing transport

Set `S={infinity,2,5,17}`, `V=Q_5 tensor T_5(E)` and let
`Gamma=Gal(Q_infinity/Q)` be the cyclotomic `Z_5` extension. BKS use a
modular-quotient lattice `T`, initially not necessarily `T_5(E)`;
irreducibility of `E[5]` permits the Tate-module choice and gives
Hypothesis 2.2(i). Their other hypotheses here are positive rank and
finite 5-primary Sha.
[BKS, §2.1, Hypothesis 2.2 and Remark 2.3](https://kurihara.math.keio.ac.jp/bks4.pdf#page=9).

For completeness, irreducibility has a tiny exact certificate. Modulo 3
the equation is `y^2=x^3-x`, and its points are
`O,(0,0),(1,0),(2,0)`. Thus Frobenius at 3 has characteristic polynomial
`X^2+3` on `E[5]`. It has no root in `F_5`, since `2` is not a square.
A Galois-stable line would in particular be Frobenius-stable and supply
an eigenvalue in `F_5`, a contradiction. This proves irreducibility,
not surjectivity. The CM property does not invalidate this argument.

One can also see the freeness step from `0 -> T --5--> T -> E[5] -> 0`:
the vanishing of `H^0(Q,E[5])` makes multiplication by 5 injective on
`H^1(Z_S,T)`. Its standard finite generation then makes it `Z_5`-free.
The rank and Sha conditions are the attributed dependencies above.
Therefore every part of Hypothesis 2.2 is supplied.

BKS's ordinary height is the Selmer-complex height. The classical
comparison is Nekovář's Theorem 11.3.9, as cited in BKS Remark 5.2;
the norm and cohomological conventions differ by sign.
[BKS, §5.1.1 and Remark 5.2](https://kurihara.math.keio.ac.jp/bks4.pdf#page=29),
[Nekovář, §11.3, especially Theorem 11.3.9, printed p. 370](https://www.numdam.org/item/AST_2006__310__R1_0.pdf).
Here both constructions use the canonical ordinary local condition and
the cyclotomic direction. The Weil pairing provides the self-duality
and orthogonal one-dimensional ordinary filtration. Local invariants
in `V` vanish because local 5-power torsion is finite. The ordinary
quotient has no invariant vector: its unit Frobenius root `alpha` is
not 1, since `1^2-a_5*1+5=8`.

The target line `Q_5 tensor I/I^2` is not literally the scalar `Q_5`.
Use the isomorphism induced by

`Gamma -> Z_5`, `gamma -> log_5(chi_cyc(gamma))/5`.

It is nonzero and invertible after tensoring with `Q_5`. Under this
comparison the canonical ordinary pairings agree up to the overall
duality-sign convention; hence their determinants vanish together.
This audit asserts nonvanishing of the BKS tensor regulator, not a
numerical identity between its untrivialized tensor and the residue 3.

BKS Theorem 5.6 states

\[
\langle x,R^{\mathrm{Boc}}_\omega\rangle_5
 =\log_\omega(x)R_5.
\]

It is used under the §5.2 assumption of Hypothesis 2.2.
[BKS, §5.2 and Theorem 5.6](https://kurihara.math.keio.ac.jp/bks4.pdf#page=33).
Take `x=P`. In the formal group, the invariant differential has integral
power-series coefficients with constant term 1, so
`log_omega(t)=t+sum_(n>=2) b_(n-1)t^n/n`, with `b_j in Z_5`.
At `t=t(8P)` its first term has valuation 1 and every later term has
valuation at least 2. Therefore `log_omega(8P)` and
`log_omega(P)=log_omega(8P)/8` are nonzero. Since `R_5` is nonzero,
the displayed identity forces

\[
\boxed{R^{\mathrm{Boc}}_\omega\ne0
\quad\text{in }(\mathbf Q_5\otimes_{\mathbf Z}E(\mathbf Q))
 \otimes_{\mathbf Z_5} I/I^2.}
\]

This is a theorem-backed implication using the admitted earlier results.
The Bockstein nonvanishing statement is thus stronger than the finite
residue observation, but it is not an independent new computation of
Kato's derived zeta element or of the complex coefficient.

## Hostile cases and evidence ceiling

The sigma truncation would require revision if `a_1` were nonzero, if
`t` were not in `5Z_5`, or if `5` divided `m`: in the last case division
by `m^2` loses additional precision. A nonminimal equation or a point
outside the required bad-prime components also fails the formula's
admission. A matrix with determinant zero modulo 5 cannot be declared
degenerate over `Q_5` from that residue alone.

The new evidence consists of primary-source formula auditing, written
tail and normalization proofs, finite rational arithmetic, and the
written Frobenius irreducibility argument. It is not formal verification.
The main conjecture and the exact rank-two Generalized Perrin–Riou
comparison remain separate obligations. Real BSD equality, total Sha
finiteness and general BSD remain outside this solved receiver.

## Extension: an arithmetic vector and the direction of the derived class

Let `M=Z_5 tensor E(Q)_tf`, let `G` be the exact MST pairing matrix in
the full ordered basis `(P,Q)`, and let
`ell=(log_omega(P),log_omega(Q))^t`. Define the exact arithmetic vector
by its coordinates

\[
w=\operatorname{adj}(G)\ell,\qquad
W_{\mathrm{MST}}=w_1P+w_2Q\in M.
\]

The height and logarithm, not an analytic BSD coefficient, define this
object. Since `det(G)!=0`, it is the unique vector satisfying

\[
B_{\mathrm{MST}}(x,W_{\mathrm{MST}})
 =\log_\omega(x)\det(G)\qquad(x\in\mathbf Q_5\otimes E(\mathbf Q)).
\]

The equality follows from `G adj(G)=det(G) Id`; conversely an invertible
`G` determines all vector coordinates from these two basis equations.
Thus this specific vector-completion fiber is `ONE(W_MST)`, although
the finite computation below determines only its first nonzero digit.

The independent rational doubling calculation additionally gives
`t(8P)=t(8Q)=5 mod 25`. The formal-log tail estimate proved above and
division by 8 give

\[
\ell/5\equiv(2,2)^t\pmod5,
\qquad
\frac w5\equiv
\begin{pmatrix}2&-2\\-2&1\end{pmatrix}
\begin{pmatrix}2\\2\end{pmatrix}
=\begin{pmatrix}0\\3\end{pmatrix}\pmod5.
\]

Therefore `W_MST in 5M`, `W_MST notin 25M`, and

\[
\boxed{W_{\mathrm{MST}}/5\equiv3Q\pmod{5M}.}
\]

This is a residue of a vector in a specified Mordell–Weil lattice. It
does not say `W_MST=15Q` exactly. For example, adding `25P` preserves
the displayed digit while generally changing the exact direction.

For a new full integral basis `(P',Q')=(P,Q)U`, with `U in GL_2(Z)`,
the data become `G'=U^t G U` and `ell'=U^t ell`. The coordinates of
the new vector in the old basis are

\[
U\operatorname{adj}(U^tGU)U^t\ell
 =\det(U)^2\operatorname{adj}(G)\ell
 =\operatorname{adj}(G)\ell.
\]

The first equality follows by writing each adjugate as determinant times
inverse; the second uses `det(U)=+1` or `-1`. Thus the vector is
basis-independent for the full integral lattice. Replacing the basis by
a proper finite-index sublattice multiplies the resulting vector by the
square of that index, so that operation is outside this invariance claim.
Under scaling of the pairing `G -> cG`, the rank-two vector scales as
`W -> cW`. Accordingly, `3Q` is the digit for the declared MST
normalization, not an unqualified digit of the BKS tensor.

There is a further theorem-supported refinement to the proposed
direction test. For the canonical `kappa_infinity` of BKS Definition
4.5, their Theorem 6.2(i) gives, under the already admitted hypotheses,

\[
\langle x,\kappa_\infty\rangle_5
 =C_\alpha\log_\omega(x)\mathcal L^{(2)}_{S,5},\qquad
C_\alpha=(1-\alpha^{-1})^{-1}(1-\beta^{-1}),
\quad\beta=5/\alpha.
\]

Here `alpha` is the unit root of `X^2+2X+5`; the superscript `(2)`
denotes the augmentation-ideal coefficient in `I^2/I^3`, as defined in
their §6.2. It is not an unconverted ordinary second derivative.
[BKS, Definition 4.5 and Theorem 6.2](https://kurihara.math.keio.ac.jp/bks4.pdf#page=42).

Both roots differ from 1 because the polynomial takes value 8 at 1.
After consistently trivializing the tensor lines, compare this formula
with Theorem 5.6. Nondegeneracy cancels the pairing and yields

\[
\kappa_\infty
 =\frac{C_\alpha\mathcal L^{(2)}_{S,5}}{R_5}
 R^{\mathrm{Boc}}_\omega.
\]

The ratio is between elements of the same degree-two tensor line; its
denominator is nonzero. Hence the canonical derived class lies on the
line spanned by the Bockstein vector, and therefore on the line of
`W_MST` after transport. This collinearity is established by the cited
theorems and the new nondegeneracy result. The explicit value and
nonvanishing of the numerator have not been computed here.

For an independently presented candidate `kappa`, the condition
`det(kappa,W_MST)=0` remains a useful necessary direction check after
all carriers and tensor normalizations are matched. It allows every
scalar multiple, including zero; it cannot establish the required scalar.
A determinant that is merely zero modulo a finite power of 5 also does
not establish exact collinearity. For the actual canonical BKS class,
one should not record collinearity itself as OPEN: what remains OPEN
here is an explicit independent class computation and the exact
archimedean scalar comparison. BKS Corollary 6.7, including its converse
when `R_5!=0`, now makes Conjecture 4.8 equivalent to the exact equality

\[
C_\alpha\mathcal L^{(2)}_{S,5}
 =\frac{L_S^*(E,1)}{\Omega_\xi R_\infty}R_5.
\]

The complex-to-5-adic comparison embedding and all period, height,
Euler-factor and augmentation conventions are those in BKS. The
nonzero `R_5` enables this converse; it does not supply the equality.
In particular, the canonical `kappa_infinity=0` possibility is not
excluded by the established direction statement alone.
[BKS, Corollary 6.7](https://kurihara.math.keio.ac.jp/bks4.pdf#page=43).
