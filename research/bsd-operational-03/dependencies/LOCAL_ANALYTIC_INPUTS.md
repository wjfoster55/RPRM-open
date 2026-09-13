# Exact local and analytic inputs for E_34

Date: 2026-09-12. Scope: the rational elliptic curve

\[
E=E_{34}:y^2=x^3-1156x.
\]

The displayed model is globally minimal. Its conductor is
\(N=18496=2^6\cdot17^2\), its global root number is \(+1\), and its
bad Euler polynomials at both 2 and 17 are 1. These inputs do not use a
database's conductor, rank, analytic rank, or special-value output.

The carrier is generalized integral Weierstrass equations over \(\mathbb Q\),
their localizations at rational primes, and the complex L-function with
central point \(s=1\). Equality of equations is separate from rational
isomorphism. The supplied port is \([a_1,a_2,a_3,a_4,a_6]=[0,0,0,-1156,0]\);
the requested readout is minimality, local reduction, conductor, sign and
coefficient rules. The receiver is the subsequent certified analytic
calculation. Rational coordinate changes retain their inverse; their
reductions modulo a bad prime are not asserted to be invertible.

## Minimality without a guessed change of variables

Direct invariant arithmetic gives

\[
b_2=b_6=c_6=0,\quad b_4=-2312,\quad b_8=-1156^2,
\quad c_4=55488=48\cdot34^2,
\]
\[
\Delta=64\cdot34^6=2^{12}17^6=98867482624.
\]

At 17 the valuation of the discriminant is 6, less than 12, so an integral
model cannot reduce it by a positive multiple of 12. Every other odd prime
has good reduction in this equation. At 2, a putative scaling by 2 would
give \(c'_4=c_4/16=3468\), which is even and congruent to 12 modulo 16.
This is impossible for an integral generalized Weierstrass equation:
\(c_4\equiv a_1^4\pmod2\), so even \(c_4\) forces even \(a_1\);
then \(b_2=a_1^2+4a_2\) is divisible by 4 and
\(b_4=a_1a_3+2a_4\) is even, forcing
\(c_4=b_2^2-24b_4\) to be divisible by 16.
No larger 2-power scale is possible because \(v_2(\Delta)=12\).
The displayed model is therefore globally minimal, with the displayed
discriminant. A translation may assist Tate's algorithm without decreasing
the minimal discriminant.

## Explicit Tate branches

The branch criterion and conductor formulas used here are Tate's algorithm
as presented by its implementer J. E. Cremona, *Algorithms for Modular
Elliptic Curves*, second edition, §3.2, printed pages 66–68. An auxiliary
cubic with three distinct roots yields \(I_0^*\),
\(f_p=v_p(\Delta)-4\). Its double-root branch terminates at \(I_m^*\)
with \(f_p=v_p(\Delta)-m-4\). The split final polynomials give local
index 4 in the cases below. These are imported algorithm theorems; the
following substitutions are the calculation specific to this curve.
[Cremona, chapter 3](https://johncremona.github.io/book/fulltext/chapter3.pdf)

For both primes the singular point is already at the origin and
\(p\mid c_4\), \(p^2\mid a_6\), \(p^3\mid b_8\), and
\(p^3\mid b_6\). Thus the multiplicative, II, III, and IV branches do not
terminate the algorithm. The coefficients already satisfy
\(p\mid a_1,a_2\), \(p^2\mid a_3,a_4\), \(p^3\mid a_6\).

At \(p=17\), the auxiliary cubic is

\[
T^3+(a_2/17)T^2+(a_4/17^2)T+a_6/17^3
=T^3-4T.
\]

Its roots \(0,2,15\) in \(\mathbb F_{17}\) are distinct (the derivative
is nonzero at each). The outcome is \(I_0^*\), additive reduction,
\(f_{17}=6-4=2\), and \(c_{17}=4\).

At \(p=2\), the auxiliary cubic is

\[
T^3-289T\equiv T(T+1)^2\pmod2.
\]

Move its double root by the **unscaled** substitution
\(x=X+2,\ y=Y\), with inverse \(X=x-2,\ Y=y\). This gives

\[
[0,6,0,-1144,-2304].
\]

For the first stage of the double-root branch, \(m=1\) and
\(m_x=m_y=4\). The quantities
\((a_2/2,a_3/m_y,a_4/(2m_x),a_6/(m_xm_y))\) are
\((3,0,-143,-144)\). The first quadratic's discriminant is
\(0^2+4(-144)=-576\), even. The required ordinate translation has
\(t/4\equiv-144\equiv0\pmod2\); take \(t=0\).
Indeed \(8\mid a_3\) and \(32\mid a_6\) already hold.

The next stage has \(m=2\), \(m_x=4\), \(m_y=8\), with tuple
\((3,0,-143,-72)\). Its quadratic is
\(3Z^2-143Z-72\); its discriminant is
\(21313\), odd, and its reduction is \(Z^2+Z\), with distinct roots
0 and 1. The outcome is \(I_2^*\), additive reduction,
\(f_2=12-2-4=6\), and \(c_2=4\).

Consequently

\[
N=2^6 17^2=18496=16\cdot34^2,\qquad\sqrt N=136.
\]

As a separate family-level check, Stein's congruent-number notes specify
\(N=16n^2\) for even positive squarefree \(n\), and \(N=32n^2\) for
odd positive squarefree \(n\). Here \(34=2\cdot17\) meets the even
case. Applying the odd formula here would give the wrong conductor.
[Stein, SIMUW 2006 notes, §5](https://wstein.org/simuw06/notes/notes/node8.html)

## Root number and exact normalization

Elkies states the congruent-number family sign theorem for positive
squarefree \(n\): the functional-equation sign is \(+1\) for residues
1, 2, 3 modulo 8 and \(-1\) for residues 5, 6, 7. His model
\(nv^2=u^3-u\) is isomorphic to ours by
\(x=nu,\ y=n^2v\), with inverse
\(u=x/n,\ v=y/n^2\). Thus the theorem applies to exactly this curve;
\(34\equiv2\pmod8\) gives \(w(E)=+1\).
[Elkies, congruent-number curves, introductory sign statement](https://people.math.harvard.edu/~elkies/cong_r3_7a.html)

In the standard elliptic-curve normalization, the completed function is

\[
\Lambda(E,s)=\left(\frac{136}{2\pi}\right)^s\Gamma(s)L(E,s),
\qquad\Lambda(E,s)=\Lambda(E,2-s).
\]

The plus sign makes the Taylor expansion at the center even. It does not,
by itself, force \(L(E,1)=0\), or determine any rank. This lane imports
the established sign theorem; it does not reprove its epsilon-factor theory.

## Euler factors and coefficients

Write \(L(E,s)=\prod_p P_p(p^{-s})^{-1}=\sum_{m\ge1}a_m m^{-s}\)
initially in its absolute-convergence half-plane. At the two additive
primes, \(P_2(T)=P_{17}(T)=1\), hence \(a_{2^k}=a_{17^k}=0\) for
\(k\ge1\). At every other prime,

\[
P_p(T)=1-a_pT+pT^2,\qquad
a_p=p+1-\#E(\mathbb F_p),
\]
\[
a_{p^0}=1,\quad a_{p^1}=a_p,\quad
a_{p^k}=a_pa_{p^{k-1}}-pa_{p^{k-2}}\quad(k\ge2),
\qquad a_{uv}=a_ua_v\ (\gcd(u,v)=1).
\]

Stein states these coefficient rules explicitly for this family, including
the bad-prime zero rule. The replay constructs good-prime counts directly
from the equation, then applies these rules.
[Stein, coefficient definitions](https://wstein.org/simuw06/notes/notes/node8.html)

Here is an **all-index** bound, separate from the finite computed head.
By Hasse, the roots \(\alpha_p,\beta_p\) of
\(Z^2-a_pZ+p\) have absolute value \(\sqrt p\). Expanding the good
Euler factor gives
\(a_{p^k}=\sum_{j=0}^k\alpha_p^j\beta_p^{k-j}\), whence
\(|a_{p^k}|\le(k+1)p^{k/2}\). This also covers coincident roots.
Multiplicativity and the bad-prime zeros imply

\[
|a_m|\le d(m)\sqrt m\le2m\qquad(m\ge1).
\]

The last inequality pairs each divisor below \(\sqrt m\) with its
complementary divisor, giving \(d(m)\le2\sqrt m\). Thus a certified
analytic tail may use \(2m\) without extrapolating finite point-count
observations. Hasse's theorem is an imported theorem; the extension to
all coefficients above is a written elementary derivation.
[Milne, *Elliptic Curves*, chapter IV, Theorem 9.4 and Aside 9.5](https://www.jmilne.org/math/Books/EC2.pdf)

## Reproduction and evidence boundary

From the repository root:

```powershell
python -I -B research/bsd-rank-two-01/work/local_inputs.py --limit 1000 --output research/bsd-rank-two-01/evidence/local_inputs.json
```

The run passed on 2026-09-12 using Python 3.14.5. It retains exact integer
invariants, Tate branch arithmetic, every prime trace through 1000 and
every coefficient through index 1000. It independently compares direct
point enumeration with Legendre-character sums through prime 101. The
code is a **special-case certificate replay**, not a general implementation
of Tate's algorithm. A finite Hasse consistency check does not prove
Hasse's theorem or the coefficient algorithm's general soundness.

Hostile boundaries: the odd conductor formula fails for this even input;
\(v_2(\Delta)=12\) alone does not license a scale-down; a bad-prime
point count does not license the good Euler polynomial; and root number
\(+1\) allows central nonvanishing. Neither the finite coefficient head nor
this input audit establishes a central zero, a second-derivative enclosure,
or a rank. Those are distinct ports for the parent analytic and descent
arguments. The local-input readout is complete relative to the named
standard theorems, while the larger rank problem is outside this lane.
