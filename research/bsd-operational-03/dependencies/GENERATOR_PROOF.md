# Complete integral-basis proof for E34

For E/Q: y²=x³−1156x, let P=(−2,48), Q=(−16,120), and
K={O,(0,0),(34,0),(−34,0)}. The new conclusion is

    E(Q)=Z·P ⊕ Z·Q ⊕ K.

Thus the free index of P,Q is exactly **ONE(1)**. This closes the
odd-saturation question left open in `ARITHMETIC_PROOF.md` and its
unchanged arithmetic receipt. The proof covers every possible proper
finite index simultaneously; no finite list of saturation primes is
being treated as complete.

The fresh executable is `work/generator.py`; its output and log are
`evidence/generator.json` and `evidence/generator_execution.log`.

## Contract, accepted arithmetic and height theorem

The carrier is the exact rational group G=E(Q). The supplied ports are
E,P,Q and the preceding proven facts that rank G=2, torsion G=K, and P,Q
are independent. The missing port is their positive free index. The
receiver is integral generation with exact point reconstruction. Equality
modulo torsion and equality of points are separate relations. Choosing a
lattice coordinate in R² does not enable rational division of a point in
G; all actual point translations below use integer multiples of P,Q.

The arithmetic inputs and their theorem dependencies are written in
`ARITHMETIC_PROOF.md`. The new height dependency is the canonical limit
and its quadraticity: [Milne, *Elliptic Curves*, IV §4, printed pp.120–124
/ PDF pages 128–132, Lemma 4.6, Theorem 4.7, Proposition 4.9 and Lemma
4.11](https://www.jmilne.org/math/Books/ectext6.pdf#page=128). The passages
were opened and inspected during this run. E is a nonsingular rational
Weierstrass curve, with discriminant 98,867,482,624, so their hypotheses
hold. The height is nonnegative, quadratic, and zero precisely on
torsion; consequently torsion translation leaves it unchanged.

The normalization throughout this file is the **full logarithmic
x-height limit**

    x(R)=a/b, gcd(a,b)=1, b>0,
    H_x(R)=max(|a|,b), h_x(R)=log H_x(R),
    H_x(O)=1, h_x(O)=0,
    q(R)=lim_(j→∞) 4^(−j) h_x(2^jR),
    B(R,S)=(q(R+S)−q(R)−q(S))/2.

Thus B(R,R)=q(R). This q is twice the convention that inserts 1/2 before
the displayed limit. The determinant below uses precisely this full
normalization, without silently changing a regulator convention.

The general statements are written deductions from the accepted
arithmetic and the cited height theorem. The executable verifies their
finite integer/rational data; its self-tests and hashes do not establish
the cited theorem or supply a formal proof.

## Explicit duplication bounds, including the prime two

For primitive projective x-coordinates (a:b), define

    F(a,b)=(a²+34²b²)²,
    G(a,b)=4ab(a²−34²b²).

The duplication formula gives x(2R)=(F:G). It includes O=(1:0), and at
the three two-torsion abscissas G=0 while F≠0. These are projective
values, so no division by a zero affine denominator occurs.

For d=gcd(F,G)>0, the uniform cancellation bound is

    d divides C0=2⁶·17⁴=4·34⁴=5,345,344.                (1)

Here is the complete prime analysis. A prime dividing both F and G
divides a²+34²b² and one of 4,a,b,a²−34²b². Coprimality rules out any
prime other than 2 or 17: in the last case subtraction forces a divisor
of 2·34²b². The cases a=0 or b=0 have primitive representatives (0:1) or
(±1:0), giving d=34⁴ or d=1, respectively, and can be handled separately.

At 17, if 17∤a then F is a unit. If v17(a)≥2, b is a unit and v17(F)=4.
If a=17c with c,b units, then

    F=17⁴(c²+4b²)²,
    G=4·17³ cb(c²−4b²).

If c²+4b² is a unit, v17(F)=4. Otherwise c²−4b²≡−8b² is a unit, so
v17(G)=3. The common exponent is therefore at most four.

At 2, an odd a makes F odd. If a is even then b is odd. If v2(a)≥2,
a²+1156b² has valuation two, giving v2(F)=4. If a=2c with c odd, then

    F=16(c²+289b²)².

Odd squares are one modulo eight and 289≡1 modulo eight. Therefore
c²+289b²≡2 modulo eight and v2(F)=6. This proves the exponent bound six,
including every parity case. In particular, the odd-n bound with only a
factor 2² would be invalid here. At a=34,b=1, G=0 and F=4·34⁴, attaining
C0 exactly.

With H=max(|a|,|b|), elementary inequalities give

    H⁴ ≤ F ≤ (1+34²)² H⁴,
    |G| ≤ 4·34² H⁴ ≤ (1+34²)² H⁴.

Set C1=(1+34²)²=1,338,649. After cancelling d and using (1),

    H_x(R)⁴/C0 ≤ H_x(2R) ≤ C1 H_x(R)⁴,
    −log C0 ≤ h_x(2R)−4h_x(R) ≤ log C1.

The estimates include O and the torsion points. Telescoping with weights
4^(−j−1), whose sum is 1/3, proves the uniform comparison

    h_x(R)−(log C0)/3 ≤ q(R) ≤ h_x(R)+(log C1)/3.       (2)

For any k≥0, the same comparison applied to 2^kR gives the certified
finite-height enclosure

    4^(−k)h_x(2^kR)−(log C0)/(3·4^k) ≤ q(R)
        ≤ 4^(−k)h_x(2^kR)+(log C1)/(3·4^k).             (3)

## Fresh rational height and Gram enclosures

The program performs eight exact projective duplications separately for
P,Q, and P+Q=(2178/49,65472/343), cancelling their actual gcds. The last
primitive x-coordinates are retained in hexadecimal, with the complete
duplication ledgers. It uses (3) and rational logarithm enclosures to get
the following outward-rounded intervals; the JSON contains the exact
dyadic endpoints:

| Quantity | Certified enclosure |
|---|---|
| q(P) | [2.512877833, 2.513028381] |
| q(Q) | [3.018586564, 3.018737112] |
| q(P+Q) | [6.925997042, 6.926147590] |
| B(P,Q) | [0.697115774, 0.697341597] |

The logarithm implementation is an attributed adaptation of the helpers
in `research/bsd-e5-completion/work/bsd_factors.py`, copied into the new
script. It imports no old checker and reads no old receipt. For
1≤r≤2, z=(r−1)/(r+1) lies in [0,1/3], and

    log r = 2 sum_(j≥0) z^(2j+1)/(2j+1).

After 96 terms, the nonnegative remainder is bounded by
2z^193/(193(1−z²)). Integer logarithms are reduced as log n=k log2+
log(n/2^k). Large integer mantissas are enclosed between adjacent
100-bit dyadics before the monotone logarithm evaluation. Every returned
lower endpoint rounds down and every upper endpoint rounds up. The
cutoff decisions use exact Fractions, never floating-point logarithms.

Because the basis will be proved integral below, its Gram determinant is
the regulator in the explicitly declared normalization:

    Reg_full = q(P)q(Q)−B(P,Q)²
             ∈ [7.099053962, 7.100201634].             (4)

The program first checks the B interval is strictly positive, then uses
the interval bounds p_lo q_lo−B_hi² and p_hi q_hi−B_lo². Its lower
bound is positive. With half-height diagonal and pairing conventions,
both Gram entries scale by 1/2 and the rank-two determinant scales by
1/4. No BSD or Sha conclusion is inferred from (4).

## Every missing lattice class has height at most 987

Let L=G/K≅Z² and M=Z[P]+Z[Q]. If M is proper in L, choose u∈L∖M.
Since P,Q are independent, they form a real basis of L⊗R. Write u in
this basis and subtract integer multiples of [P],[Q] to obtain

    v=alpha[P]+beta[Q] ∈ L∖M,
    −1/2≤alpha,beta≤1/2.

This is coordinate reduction of an actual lattice class by integral
translations. It does not assert that alpha·P or beta·Q is an enabled
rational-group operation. Lift v to any actual point R∈G. Quadraticity
and torsion invariance give

    q(R)=alpha² q(P)+2alpha beta B(P,Q)+beta² q(Q)
         ≤ (q(P)+q(Q)+2|B(P,Q)|)/4.

Using the certified Gram endpoints, the last expression is at most the
exact rational `box_q_upper` recorded in the receipt, which is less than
1.731612172. Applying (2) gives

    h_x(R) ≤ box_q_upper+(log C0)/3 ≤ U,

where the exact certified U is

    4370557774463719632189197774495 /
      633825300114114700748351602688
      < 6.895524325.

The rational lower bound on log988 is

    8741316310783500819293012134699 /
      1267650600228229401496703205376
      > 6.895682697.

The program checks U is strictly below that lower bound; the exact gap
is retained in the JSON. Therefore H_x(R)<988. Since H_x(R) is an
integer, every possible missing lattice class has an actual rational
representative with **H_x(R)≤987**. The bound lies below the authorized
height cap 5,000 and raw enumeration cap 1,000,000.

## Complete enumeration and exact memberships

Every affine rational point has a reduced abscissa x=a/c² with c>0 and
gcd(a,c)=1. To verify the square-denominator claim, if a prime has
v_p(x)<0, the monic x³ term has strictly smaller valuation than
−1156x, so v_p(y²)=3v_p(x). Thus every negative valuation of x is even.
This applies also at 2 and 17; integrality of the coefficients suffices.

Height at most 987 means |a|≤987 and c²≤987, hence 1≤c≤31. The curve
equation is

    (c³y)² = a(a²−1156c⁴).                            (5)

A rational number whose square is an integer is an integer. Thus y
exists exactly when the right side of (5) is a nonnegative integer
square, and then y=±sqrt(a(a²−1156c⁴))/c³, with one ordinate when zero.
The program exhausts every such (a,c), with no ordinate-search bound.

There are 61,225 raw pairs and **38,205 reduced abscissas**. They yield
exactly **25 affine points**, or 26 points including O. The complete list
is the torsion group K and both signs of each point in this table:

| One signed point from each pair | Exact group expression |
|---|---|
| (−2,48) | P |
| (−16,120) | Q |
| (162,2016) | Q−P |
| (578,13872) | P+T0 |
| (153/4,−867/8) | P+Tminus |
| (289/4,4335/8) | Q+T0 |
| (−272/9,−2312/27) | P+Tplus |
| (850/9,−23120/27) | Q+Tminus |
| (833/16,−18207/64) | Q−P+Tplus |
| (−306/25,−13872/125) | Q+Tplus |
| (−578/81,64736/729) | Q−P+T0 |

Each equality is checked by exact chord-and-tangent arithmetic. The
JSON stores all 26 points separately with their coefficients and
torsion labels, plus per-denominator enumeration counts. Its digest
binds the deterministically ordered candidate stream; the exhaustive
loops and argument (5) establish coverage, not the digest alone.

Every point in the completed height search lies in ZP+ZQ+K. The R forced
into this list by the previous section would therefore have free class
v∈M, contradicting v∈L∖M. Hence M=L, proving index one and the displayed
complete group decomposition. Only membership witnesses are needed:
the small coefficient search {−1,0,1} is not used as a test for general
nonmembership or as a coefficient-coverage theorem.

## Reproduction, controls and scope

From the experiment directory run:

    python -I -B work/generator.py --output evidence/generator.json

The checker uses the standard library and exact rational/integer
arithmetic. It never reads `evidence/arithmetic.json`, and that earlier
receipt remains unchanged. Its output records a fresh PASS for the
height cutoff and completed point search; the accepted rank/torsion
theorems remain explicitly cited dependencies.

The primitive input x=34 attains gcd C0, rejecting an incorrect bound
2²·17⁴ imported from an odd-n parity argument. The malformed point
(−16,121) is rejected before group arithmetic. For all 26 small points,
the homogeneous x-duplication result is checked against independent
chord-law doubling, including O and every zero-ordinate exception.

This is a standard height and lattice saturation argument specialized
to one curve. It establishes an integral basis and a certified regulator
interval. It does not establish an analytic order of vanishing, a BSD
leading-coefficient identity, or the odd-primary/total order of Sha.
