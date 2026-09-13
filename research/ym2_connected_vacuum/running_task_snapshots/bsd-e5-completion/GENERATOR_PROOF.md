# Complete primitive-generator proof for E5

**Result:** for `E/Q: y²=x³−25x` and `P=(−4,6)`,

    E(Q) = Z·P ⊕ {O,(0,0),(5,0),(−5,0)}.

In particular, the free index of P is **ONE(1)**. This closes the odd-index
question left open by the earlier experiment; it does not reinterpret that
earlier result as having already established saturation.

## Contract and dependencies

The carrier is the exact rational group E(Q), including the projective
identity O, with ordinary group equality. Supplied ports are the curve, P,
and the accepted facts that the rank is one, the torsion subgroup is exactly
`K=E[2](Q)`, and P has odd nonzero index in `E(Q)/K`. The missing port is
that positive index. The receiver must preserve generation over Z, not merely
surjectivity onto every quotient modulo a power of two. The operation is
rational group multiplication; multiplication by an odd integer is not
silently treated as rational division.

The rank and oddness inputs are in
`supplied_review/BSD_E5_REVIEW/input/BSD_E5_CODEX_TEST_01_RETURN/ARITHMETIC_PROOF.md`,
A01–A02 (preserved from the prior experiment). The full torsion input is in
`supplied_review/BSD_E5_REVIEW/TORSION_COROLLARY.md`. That corollary correctly
applies good reduction at 3: the discriminant is 1,000,000 and `#E(F_3)=4`.
Milne's stated torsion injection at an odd good prime was independently
checked in [Chapter II, Corollary 5.7, printed p.66](https://www.jmilne.org/math/Books/ectext6.pdf#page=74).
None of those inputs alone excludes an odd index greater than one.

One new standard theorem dependency is used: the logarithmic x-height has
a canonical limit which is a quadratic form. We use the exact normalization

    H(R)=max(|a|,b),  h_x(R)=log H(R),
    x(R)=a/b, gcd(a,b)=1, b>0;
    H(O)=1, h_x(O)=0;
    Hhat_x(R)=lim_(n→∞) 4^(−n) h_x(2^n R).

This is the normalization in [Milne, *Elliptic Curves* (2006), Chapter IV
§4, printed pp.120–124](https://www.jmilne.org/math/Books/ectext6.pdf#page=128):
the height definition, Lemma 4.6, Theorem 4.7, Proposition 4.9 and Lemma 4.11.
The named passages were opened and inspected on 12 September 2026. The
curve is a nonsingular rational Weierstrass model, so their hypotheses hold.
Quadraticity implies `Hhat_x(mR)=m² Hhat_x(R)`; the associated real bilinear
form vanishes against torsion, so `Hhat_x(R+T)=Hhat_x(R)` for torsion T.
This `Hhat_x` is twice the alternative canonical height defined with a
factor 1/2 before the limit. No regulator convention is needed for this proof.

The universal argument below is a written proof with that cited dependency.
`work/generator_check.py` supplies an exact, bounded finite certificate using
Python's standard library. Its self-checks do not formally prove the height
theorem or the preceding descent.

## An explicit height comparison

For primitive projective x-coordinates `(a:b)`, the duplication formula is

    x(2R) = (F(a,b):G(a,b)),
    F(a,b)=(a²+25b²)²,
    G(a,b)=4ab(a²−25b²).

Here an affine x=a/b has b>0, and O is represented by (1:0). The formula
also handles the three rational 2-torsion abscissas: G=0 but F is nonzero,
giving the point at infinity. Thus no zero denominator is passed through as
an affine rational division.

Let `d=gcd(F,G)>0`. For every primitive pair,

    d ≤ 2²·5⁴ = 2500.                                    (1)

To prove (1), a prime dividing both F and G must divide
`a²+25b²` and one of `4,a,b,a²−25b²`. Coprimality shows that a prime other
than 2 or 5 cannot do so: in the last case subtraction gives divisibility
of 50b². At 2, if a,b have opposite parity, F is odd; if both are odd,
`a²+25b² ≡ 2 (mod 8)`, so `v_2(F)=2`. At 5, if 5 does not divide a,
F is a unit. If a=0 or `v_5(a)≥2`, coprimality makes b a unit and
`v_5(F)=4`. Finally, if `a=5c` with c,b units, then

    F=5⁴(c²+b²)²,   G=4·5³ cb(c²−b²).

If 5 does not divide `c²+b²`, F has valuation 4. If it does, then
`c²−b² ≡ −2b² (mod 5)` is a unit, and G has valuation 3. In all cases
the common 5-adic valuation is at most 4. The primitive case b=0 is
`a=±1`, giving d=1, and is covered separately without valuation ambiguity.

For `H=max(|a|,|b|)`, elementary real inequalities give

    H⁴ ≤ F ≤ 676 H⁴,
    |G| ≤ 104 H⁴ ≤ 676 H⁴.

After cancelling d, therefore,

    H(R)⁴/2500 ≤ H(2R) ≤ 676 H(R)⁴,
    −log2500 ≤ h_x(2R)−4h_x(R) ≤ log676.                 (2)

These estimates include O and the 2-torsion points. Telescoping (2), with
weights `4^(−j−1)` for j≥0 whose sum is 1/3, proves

    h_x(R)−(log2500)/3 ≤ Hhat_x(R)
                       ≤ h_x(R)+(log676)/3.             (3)

This elementary comparison is deliberately coarse. It suffices to close
the index question, so it does not require a numerical canonical-height
algorithm, a regulator value, a database generator, or any BSD assumption.

## Every possible proper odd divisor is covered

Choose a primitive free generator Q of E(Q)/K. By the known rank and
torsion results, there are an integer k≠0 and T∈K such that
`P=kQ+T`, and the known mod-2 result makes k odd. If `|k|>1`, then
`|k|≥3`, so quadraticity and (3), using H(P)=4, imply

    Hhat_x(Q)=Hhat_x(P)/k²
              ≤ (log4+(log676)/3)/9,

    h_x(Q) ≤ (log4)/9+(log676)/27+(log2500)/3.

Multiply the last inequality by 27 and exponentiate:

    H(Q)^27 ≤ 4³·676·2500⁹ < 21²⁷.                     (4)

The final comparison in (4) is checked as an exact integer inequality, not
by rounded logarithms. H(Q) is a positive integer, so **H(Q)≤20**. This
covers every possible proper odd index at once, including unbounded odd
primes. No finite list of trial saturation primes is being assumed complete.

## Complete rational-point enumeration at H≤20

Every affine rational x of height at most 20 has exactly one reduced form
`a/b` with `−20≤a≤20`, `1≤b≤20`, and gcd(a,b)=1. There are 511 such
abscissas. Define the integer

    N = ab(a²−25b²).

The curve equation is equivalent to `(b²y)²=N`. A rational number whose
square is an integer is an integer (reduce its numerator and denominator),
so an ordinate exists precisely when N is a nonnegative integer square.
For N>0 both ordinates are `±sqrt(N)/b²`; for N=0 there is one. Testing
all 511 integers N therefore exhausts the finite fiber, with no assumption
about square denominators and no bounded ordinate search.

The complete result, including O separately, is

| Point(s) | Exact group identification |
|---|---|
| O, (0,0), (5,0), (−5,0) | K |
| (−4,±6) | ±P |
| (−5/9,±100/27) | ±(P+(5,0)) |

The chord law gives `P+(5,0)=(−5/9,−100/27)`; both signs are included.
Every nontorsion point in this complete list has free class ±P. Thus the
putative Q forced into this list by (4) satisfies `[Q]=±[P]` in E(Q)/K.
Combining this with `[P]=k[Q]` gives k=±1 since [Q] has infinite order,
contradicting `|k|≥3`. Consequently the index is exactly one. Directness
and uniqueness of `R=mP+T` follow from P having infinite order and K being
the torsion subgroup. This is the complete infinite group family, rather
than just an assertion about the finitely enumerated subset.

## Certificate, hostile cases, and limits

From this directory run:

    python -I -B work/generator_check.py --output evidence/generator.json

The receipt contains all 511 abscissa rows, the exact integer cutoff,
every resulting point and its group identification, and independent
x-duplication/chord-law comparisons, including all exceptional points.

Three controls preserve important distinctions. The curve point (45,−300)
attains gcd(F,G)=2500, rejecting an unjustified smaller cancellation bound.
Multiplication by 3 is a bijection modulo 2^n (checked for n=1,…,8, with
the general fact given by gcd(3,2^n)=1), so binary quotient coverage alone
does not imply primitivity; after the present proof, 3P is an actual
index-three example on this same curve. The off-curve pair (0,1) is rejected
by the group-operation admission check.

The work changes no prior arithmetic proof or supplied review. The new
conclusion concerns this single rational curve. It supplies the generator
ingredient for a BSD coefficient calculation but does not itself determine
Sha, periods, local Tamagawa numbers, or a leading-coefficient identity.
