# E5: finite proof of a simple central zero, and a cube coordinate system for descent

**Date:** 12 September 2026. **Scope:** continuation of BSD arithmetic in this conversation.
This is a calculation using established elliptic-curve/modularity theorems, not a
new BSD theorem, a paper draft, an agent dispatch, or a reopening of the frozen
Lind–Reichardt/AD work.

## 1. Question and outcome

For E: y^2=x^3-25x, the preceding E5_DESCENT_NOTE.md established arithmetic rank 1
by an exact 2-descent. The new question is whether the first central Taylor
coefficient of L(E,s) is nonzero, independently of that rank calculation.

Using the standard functional equation and a rapidly convergent central-derivative
formula, we prove

    L(E,1)=0,       L'(E,1)>65/100.

Consequently ord_(s=1) L(E,s)=1, and the rank equality in BSD holds for this
particular curve when combined with the previous descent. The nonvanishing proof
does not input a database rank, the BSD conjecture, a Sha prediction, or a forced
zero from an arithmetic-rank label.

The full leading-coefficient formula, the odd-index saturation of P=(-4,6), and
the universal BSD claim are not established by this calculation. These are
limits of this work, not statements that those particular-curve facts are absent
from the mathematical literature.

## 2. Imported standard mathematics and source identity

**Curve identification, conductor, sign.** Put x=5u, y=25v. The equation becomes
5v^2=u^3-u. It is the D=5 member of Elkies's congruent-number family. His §1.1
states the functional-equation sign; §2 (printed p.4) states N=32 D^2 for odd
squarefree D. Therefore N=800 and epsilon=-1. These are cited standard inputs,
not outputs of our finite point counts. No rank statement in that paper is used.

**Modularity and completed L-function.** For an elliptic curve over Q, modularity
gives an entire L-function with completed function

    Lambda(s) = (sqrt(N)/(2*pi))^s Gamma(s) L(E,s),
    Lambda(s) = epsilon Lambda(2-s).

The factor multiplying L is analytic and nonzero near s=1. The sign -1 gives
Lambda(1)=0 and hence L(E,1)=0 exactly. It is Lambda(1+t), not necessarily the raw
L(E,1+t), that is odd in t.

**Euler coefficients.** Write L(E,s)=sum a_n/n^s in its convergence half-plane.
For a good prime, a_p=p+1-#E(F_p). The coefficients are multiplicative on coprime
integers and

    a_(p^0)=1, a_(p^1)=a_p,
    a_(p^k)=a_p*a_(p^(k-1))-p*a_(p^(k-2)).

The displayed model is minimal at each prime: its discriminant has valuations
6 at 2 and 5 and 0 elsewhere, all below 12, so it cannot be decreased by 12
while remaining integral. Its singular reductions at 2 and 5 are cuspidal
(additive), so their local L-factors are 1 and a_n=0 whenever 2 or 5 divides n.
Counting projective points of the singular models gives a_2=a_5=0 as a check;
this is not described as counting points of a nonsingular reduced elliptic curve.

For p=2, first put X=x+1, giving y^2=X^3+X^2, then put Z=y+X.
The equation becomes Z^2=X^3. At 5 it is already y^2=x^3. This makes
the cusp classification explicit.

## 3. Derivative formula, with its analytic dependency visible

Set alpha=2*pi/sqrt(800)=pi/(10*sqrt(2)), and define

    E1(x)=integral from x to infinity of exp(-t)/t dt   (x>0).

The standard sign-minus-one central-derivative identity is

    L'(E,1) = 2 sum_(n>=1) (a_n/n) E1(alpha*n).         (A)

This is the formula documented for Sage's deriv_at1, citing Cohen §7.5.3. We
implement its finite arithmetic and give a separate conservative tail estimate;
we do not run Sage or rely on its returned numerical error estimate.

For the normalization check, let f(z)=sum a_n exp(2*pi*i*n*z) be the corresponding
weight-two modular form and g(u)=f(i*u/sqrt(N)). Mellin transformation gives

    Lambda(s)=integral_0^infinity g(u)*u^(s-1) du.

The modular transformation gives g(1/u)=epsilon*u^2*g(u). Splitting at 1 yields

    Lambda(s)=integral_1^infinity g(u)*(u^(s-1)+epsilon*u^(1-s)) du.

With epsilon=-1,

    Lambda'(1)=2 integral_1^infinity g(u)*log(u) du.

Termwise integration is justified by exponential decay. Integration by parts
shows that integral_1^infinity exp(-alpha*n*u)log(u)du=E1(alpha*n)/(alpha*n).
Since L(E,1)=0, Lambda'(1)=L'(E,1)/alpha, proving (A).

This uses a globally valid analytically continued representation. It is NOT
substitution of s=1 into a finite Euler product and NOT termwise differentiation
of a Dirichlet series outside its stated convergence domain.

## 4. Exact finite arithmetic: only four nonzero terms through 20

Two separately structured elementary point counts (pair enumeration and a
square-root multiplicity table) agree at each prime through 20:

| p | model's projective point count | a_p | local status |
|---|---:|---:|---|
| 2 | 3 | 0 | additive |
| 3 | 4 | 0 | good |
| 5 | 6 | 0 | additive |
| 7 | 8 | 0 | good |
| 11 | 12 | 0 | good |
| 13 | 20 | -6 | good |
| 17 | 20 | -2 | good |
| 19 | 20 | 0 | good |

The Euler recurrences and multiplicativity therefore give only

    a_1=1, a_9=-3, a_13=-6, a_17=-2

as nonzero coefficients with 1<=n<=20. In particular a_9=a_3^2-3=-3.
These a_n are the Euler/Fourier coefficients, NOT the central Taylor coefficients
c_j in L(E,1+t)=sum c_j t^j. The coefficient being bounded is c_1=L'(E,1).

## 5. Bound every omitted term, not just sampled terms

At good primes the two Euler roots have absolute value sqrt(p), by Hasse's bound.
Thus |a_(p^k)|<=(k+1)p^(k/2). Multiplicativity gives

    |a_n| <= d(n)*sqrt(n) <= 2n,

where d(n) counts positive divisors; d(n)<=2 sqrt(n) follows by pairing divisors
on opposite sides of sqrt(n). The additive bad-prime coefficients are zero and
satisfy the same bound.

For x>0,

    0<E1(x)<=exp(-x)/x.

We have 1/5<alpha<1/4. The checker certifies this using rational bounds for pi
from Machin's identity and the alternating arctan series, together with
7/5<sqrt(2)<3/2. Since exp(alpha)>1+alpha>6/5,

    exp(-alpha)<q=5/6.

For n>=21, the absolute tail in (A) is at most

    4 sum_(n>=21) E1(alpha*n)
      < (20/21) sum_(n>=21) q^n
      = (120/21) q^21
      = 2384185791015625 / 19194831810330624
      < 0.125.                                        (B)

The bound covers all n>=21. It does not assume their actual signs or an observed
pattern of zero coefficients.

## 6. A positive lower bound without numerical special functions

The leading contribution satisfies

    2E1(alpha) > 2 integral_(1/4)^1 exp(-t)/t dt
               > (2/3) log(4)
               > 8/9.                                (C)

Here e<3 follows from its factorial series, and log2>2/3 follows from
log2=2*atanh(1/3)=2[1/3+(1/3)^3/3+...]. Neither inequality requires an uncertified
floating approximation to e, pi, or a logarithm.

The three known negative contributions have total magnitude below

    Bneg = 10[(3/9^2)q^9 + (6/13^2)q^13 + (2/17^2)q^17]
         = 22338243056640625 / 206678743485087744
         < 0.109.                                     (D)

Combining (B)-(D):

    L'(E,1) > 8/9 - Bneg - (120/21)q^21
            = 615556405007957768183 / 937494780448358006784
            > 0.65.

All arithmetic in this displayed sign certificate is rational. A decimal display
of the lower bound is approximately 0.6565971543, but rounding that display is
not part of the proof. Even the looser rounded upper estimates 0.109 and 0.125
retain a lower bound greater than 0.65.

Thus L(E,1)=0 and L'(E,1)>0. A holomorphic function with zero constant term and
nonzero linear term has vanishing order exactly one.

An OPTIONAL, noncertified-roundoff numerical illustration evaluates (A) through
n=100 at 60-digit mpmath precision and gives about 2.2273703795441462. The analytic
tail bound at 100 is about 1.62e-10 when evaluated numerically. The exact proof of
positivity does not depend on those decimal digits or on mpmath being installed.

## 7. The user's eight / four / wrapper question: an exact cube adapter

Retain the previous descent's squareclass subgroup H generated by

    p=delta(P)=(-1,-1,1),
    t0=delta(T0)=(-1,-5,5),
    tplus=delta(Tplus)=(5,2,10).

Every class is uniquely p^a t0^b tplus^c with a,b,c in {0,1}. Thus H has 2^3=8
classes, INCLUDING the identity. A wrapper describing H and its operation law is
an object at another interface, not an extra member of H.

The previous 32-element candidate group V has four H-cosets with representatives
1, A=(2,2,1), B=(1,2,2), AB=(2,1,2). The map

    (a,b,c,u,v) -> p^a t0^b tplus^c A^u B^v

is an exact bijection from a five-bit cube to V. The first three bits label one
of eight positions inside a block; the final two select one of four blocks.
The accepted arithmetic exclusions say that a class is realized exactly when
u=v=0. In these coordinates the indicator is (1-u)(1-v).

The checker verifies the bijection, the block sizes, and the indicator on all
32 vertices. The cube RECODES the previously proved local exclusions; it does
not derive those exclusions from a shape or from the numerals 8, 4, or 9. It is
also not the assertion that naturally embedded low-degree representatives of C1
are closed under full multiplication.

There is a concrete inverse distinction: [P]=[-P] in G/2G, because their difference
is 2P. They are distinct in G/4G because the preceding descent proved 2P is not in
4G. This is one specified quotient/inverse phenomenon, not a definition of every
use of the RPRM word 'shadow'.

## 8. Proof-donut use and boundaries

The published proof-donut reference requires an explicit missing question,
compatible constraints, coverage, transport, continuation, and landing. Here:

- Question: is c_1 nonzero, given the already proved exact central zero?
- Analytic identification: modularity/Mellin formula (A).
- Finite inputs: coefficients through 20 computed from E.
- Infinite coverage: Hasse/multiplicativity and the geometric tail bound (B).
- Landing: the exact rational lower bound is positive.

This is a theorem-based certificate using the proof-donut discipline. The finite
`audit_finite_aperture` API was NOT run on an infinite analytic carrier, and no
claim is made that its finite engine alone proves modularity, the functional
equation, or (A). A named scope and sufficient tail estimate close this query
without reconstructing every digit or every coefficient of the source function.

## 9. Source ledger

1. Original attached E5_DESCENT_NOTE.md, sections 2-8: the eight classes, four-coset
   partition, arithmetic rank, 2-primary Sha statement, and odd-index caveat.
   This is inherited source evidence, not analytic input to (A).
2. Original attached CURRENT_STATE.md / BSD_CHAT_UPDATE.md (12 September 2026):
   accepted C1/AD1 scope; original Prestige meanings; closed-task boundaries.
3. Noam D. Elkies, 'Curves D y^2=x^3-x of odd analytic rank', arXiv:math/0208056,
   §1.1 and §2, printed pp.1-4. Curve normalization, root sign, conductor.
   https://arxiv.org/pdf/math/0208056
4. Sage reference, Lseries_ell.deriv_at1: exact derivative formula and input scope;
   original reference Cohen, A Course in Computational Algebraic Number Theory,
   §7.5.3. We derive the normalization and use our own conservative error bound.
   https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/lseries_ell.html
5. Andrew Sutherland, MIT 18.783 Fall 2023 Lecture 7, Theorem 7.3: Hasse bound and
   point-count trace. https://math.mit.edu/classes/18.783/2023/LectureNotes7.pdf
6. Andrew Wiles, Clay BSD problem description, especially modularity and the rank
   comparison. https://www.claymath.org/wp-content/uploads/2022/05/birchswin.pdf
7. NIST DLMF §§6.2, 6.6: definition of E1 and its standard representations.
   https://dlmf.nist.gov/6.2 ; https://dlmf.nist.gov/6.6
8. Published RPRM docs/proof-donut.md, Git blob
   0d5c948de8dc032fbaddff7283eb0504337efe8f, read on 12 September 2026.
   https://github.com/wjfoster55/RPRM-open/blob/main/docs/proof-donut.md

The code runs locally, makes no network calls, and writes only its named receipt.
No external worker or old frozen audit is dispatched.
