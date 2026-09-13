# Exact arithmetic admission for E34

For the curve E: y²=x(x−34)(x+34), the fresh calculation proves

    rank E(Q)=2,
    E(Q)_tors = {O,(0,0),(34,0),(−34,0)} ≅ (Z/2Z)²,
    Sel_2(E/Q) = delta(E(Q)), with 16 elements,
    Sha(E/Q)[2^n]=0 for every n≥1.

The independently found points P=(−2,48) and Q=(−16,120) are independent
and generate a subgroup of finite odd index in the free quotient. This file
does not determine that odd index. In particular, these arithmetic results
do not supply a saturated integral basis, an analytic order of vanishing,
the odd-primary part or total order of Sha, or a BSD leading-term identity.

The executable is `work/arithmetic.py`; its fresh output and execution log
are `evidence/arithmetic.json` and `evidence/arithmetic_execution.log`.

## Contract and theorem boundary

The carrier is G=E(Q), including the point O at projective infinity, with
exact rational/projective equality and the elliptic-curve group law. The
model has a-invariants (0,0,0,−1156,0), distinct roots (0,34,−34), and
discriminant 64·34⁶=98,867,482,624≠0. These facts admit E as an elliptic
curve over the number field Q. The root order is fixed throughout.

For descent, the supplied ports are E and a multiplicative squareclass
triple; the missing port is a realizing point, and the requested readout
is membership in the image of the doubling quotient. Squareclass equality
means equality in Q*/Q*², not equality of rational values or point
occurrences. The complete solved finite carrier is G/2G and its Selmer
envelope, not an enumeration of G. Multiplication by two is a total
operation on G; rational halving is its preimage relation. The finite
integer-abscissa search below only finds witnesses and does not close the
unbounded rational-point search.

The dependencies are standard mathematical theorems, used under the
checked hypotheses above. They were opened and inspected during this run:

* **S_KUMMER:** the split two-torsion Kummer homomorphism, its exceptional
  values and kernel 2G; [Milne, *Elliptic Curves*, IV §3, Remark 3.7,
  printed p.113 / PDF page 121](https://www.jmilne.org/math/Books/ectext6.pdf#page=121).
  The preceding identification gives the product-square triple carrier.
* **S_MW:** finite generation over a number field; [Milne, IV opening,
  printed p.101 / PDF page 109](https://www.jmilne.org/math/Books/ectext6.pdf#page=109).
* **S_SELMER:** the all-place local-image definition and exact sequence
  0→G/nG→Sel_n→Sha[n]→0; [Stoll, *Descent on Elliptic Curves*, §1.1,
  pp.2–3](https://arxiv.org/pdf/math/0611694#page=2), with n=2^k>1.
* **S_TORSION_REDUCTION:** injectivity of rational torsion reduction at
  good odd primes; [Milne, II §5, Corollary 5.7, printed p.66 / PDF page
  74](https://www.jmilne.org/math/Books/ectext6.pdf#page=74). Primes 3 and 5
  are good because they do not divide the displayed discriminant.
* **S_HENSEL:** lifting a simple residue root; [Milne, I §2, Theorem
  2.12, printed p.24 / PDF page 32](https://www.jmilne.org/math/Books/ectext6.pdf#page=32). For z²−2 modulo 17,
  z=6 is a root and its derivative 12 is a unit.

The general conclusions below are written deductions from these theorems
and the explicit calculations. The program certifies finite integer and
rational data. Its PASS field and source hash are execution evidence,
not a formal proof or a proof of the cited theorems.

## The squareclass carrier and all-prime support

For x away from the three roots, put

    delta((x,y)) = ([x],[x−34],[x+34]).

Set delta(O)=(1,1,1). At a root e_i, replace its zero factor by
(e_i−e_j)(e_i−e_k), while retaining the other two factors. Thus, for
T0=(0,0), Tplus=(34,0), and Tminus=(−34,0),

    delta(T0)    = (−1,−34,34),
    delta(Tplus) = (34,2,17),
    delta(Tminus)= (−34,−17,2).

The product is a square in all cases. Zero is never treated as an element
of Q*/Q*². By S_KUMMER the map is a homomorphism with kernel 2G; the same
construction restricts to the local Kummer maps over the completions.

Let a Selmer class restrict at a prime q∉{2,17} to a local point. For
an ordinary affine point with v_q(x)<0, all three factors x,x−34,x+34
have the same valuation m. Their square product forces 3m even, hence m
even. If v_q(x)≥0, all factors are integral, and their nonzero pairwise
differences 34 or 68 are q-units. At most one factor can have positive
valuation, and the square product forces that valuation even. O and the
three exceptional signatures satisfy the same support condition directly.
Thus every rational coordinate squareclass in Sel_2 has even valuation
outside {2,17}.

Every such class has exactly one representative in

    D={−34,−17,−2,−1,1,2,17,34}.

The product-square condition determines d3=[d1d2], so D gives exactly 64
triples. Over R an affine point has x∈[−34,0] or x∈[34,∞). Its sign
triple, including the exceptional conventions, is (--+) or (+++).
Consequently every Selmer class lies in the 32-element subgroup

    V={(d1,d2,d3): di∈D, [d1d2d3]=1, d1d2>0, d3>0}.

This is an all-prime support proof followed by a real necessary condition;
it does not infer global solubility from checks at finitely many primes.

## Sixteen rational witnesses

The exact search tests every integer x from −34 through 10,000 and checks
whether x³−1156x has a rational square root. It finds the nonnegative-y
points (−34,0),(−16,120),(−2,48),(0,0),(34,0),(162,2016), and
(578,13872). The choice Q=(−16,120) is the first point whose Kummer class
is outside the eight classes from {O,P}+G[2].

Write a representative as epsilon·P+eta·Q+T, with epsilon,eta∈{0,1}
and T∈K={O,T0,Tplus,Tminus}. Exact chord-and-tangent arithmetic yields:

| epsilon,eta,T | Point | Signature |
|---|---|---|
| 0,0,O | O | (1,1,1) |
| 0,0,T0 | (0,0) | (−1,−34,34) |
| 0,0,Tplus | (34,0) | (34,2,17) |
| 0,0,Tminus | (−34,0) | (−34,−17,2) |
| 0,1,O | (−16,120) | (−1,−2,2) |
| 0,1,T0 | (289/4,4335/8) | (1,17,17) |
| 0,1,Tplus | (−306/25,−13872/125) | (−34,−1,34) |
| 0,1,Tminus | (850/9,−23120/27) | (34,34,1) |
| 1,0,O | (−2,48) | (−2,−1,2) |
| 1,0,T0 | (578,13872) | (2,34,17) |
| 1,0,Tplus | (−272/9,−2312/27) | (−17,−2,34) |
| 1,0,Tminus | (153/4,−867/8) | (17,17,1) |
| 1,1,O | (2178/49,65472/343) | (2,2,1) |
| 1,1,T0 | (−28322/1089,4013632/35937) | (−2,−17,34) |
| 1,1,Tplus | (16337/64,−2069529/512) | (17,1,17) |
| 1,1,Tminus | (−4352/961,−2136288/29791) | (−17,−34,2) |

The sixteen distinct signatures form a subgroup H of V. Every one is
globally witnessed, so H⊆delta(G)⊆Sel_2. The program recomputes each
point, checks its curve equation, identifies each squareclass using exact
rational-square tests, and stores an integer witness of the covering
equations below. It also checks the Kummer homomorphism on all 256 pairs
of displayed points. That finite check supplements S_KUMMER, rather than
replacing its general assertion.

One can verify independence of the four class generators directly. Use
coordinates (negative-sign bit of d1, v2(d1),v17(d1),v2(d2),v17(d2)), all
modulo two. The generators P,Q,T0,Tplus are respectively

    (1,1,0,0,0), (1,0,0,1,0), (1,0,0,1,1), (0,1,1,1,0).

In a vanishing linear combination, the third coordinate first kills the
Tplus coefficient, the fifth kills T0, the second kills P, and the fourth
kills Q. Hence their span has dimension four. The class A=(1,2,2) has
coordinates (0,0,0,1,0) and is outside that span: the same eliminations
would force Q alone, which has negative-sign bit one. Therefore

    V = H disjoint-union A·H.

This argument gives complete coset coverage without relying on the
point-search bounds or treating an observed table shape as a theorem.

## Local obstruction and completion

For a supported triple d define the homogeneous equations

    d1 u1² − d2 u2² = 34t²,
    d3 u3² − d1 u1² = 34t².                 (1)

A local Kummer realization gives a nonzero projective solution of (1).
For an ordinary point use (x−e_i)=d_i(u_i/t)². At a root, its zero factor
allows the corresponding u_i=0, and the exceptional signature ensures
the other two coordinates exist. For O the locally trivial triple gives
a solution with t=0 after taking local square roots of the d_i.

Conversely, if t≠0, equations (1) give the three factors of the curve by
x=d1(u1/t)²; their product is a square because d1d2d3 is a square. A
zero factor recovers the corresponding exceptional Kummer value using
that product-square condition. If t=0, the three d_i u_i² have a common
nonzero value. The common local squareclass has cube equal to one and
therefore is trivial. Hence all d_i are locally squares, recovering the
O class. This is a statement in the completion, not an inference that
locally square rational numbers must be rational squares.

A nonzero Q_p projective solution can be rescaled so that its four
coordinates are p-adic integers and at least one is a unit. Its reduction
modulo p^k is a primitive solution. Thus absence of a primitive residue
solution proves local impossibility. Mere existence of residues is only
a necessary test.

For p=2 the checker independently enumerates every quadruple modulo
2,4,8, retaining precisely those with an odd coordinate satisfying (1).
The signature-survivor counts are 32,28,16. The last set equals H exactly.
All primitive counts and first witnesses for all 32 real-supported
triples are retained in the JSON. These are full finite enumerations,
not randomized tests.

There is a short separate exclusion proof. For A=(1,2,2), equations (1)
are u1²−2u2²=34t² and 2u3²−u1²=34t². Modulo two, u1 is even. Modulo
four, u2,u3,t have the same parity. If t is even, every coordinate is
even, contradicting primitivity. If t is odd, u2 and u3 are odd; the
first equation modulo eight forces u1²≡4, while the second forces
u1²≡0. This is impossible. Therefore A is not Q_2-admissible.

The inverse image in V of the Q_2 Kummer image is a subgroup containing
H. If any A·h with h∈H were admissible, multiplication by the locally
admissible h would make A admissible. Thus the whole complementary coset
is excluded. Together with the rational witnesses this proves

    H ⊆ delta(G) ⊆ Sel_2 ⊆ H.

The place 17 imposes no further restriction on V. In fact, 6²≡2 (mod
17) and 12 is nonzero modulo 17, so S_HENSEL makes 2 a square in Q_17.
Consequently A=(1,2,2) is locally the identity; both cosets H and A·H
are in the Q_17 image. The fresh mod-17 enumeration retains all 32
triples, consistent with this argument. All other local conditions for
the retained sixteen classes, including the real one, are supplied by
their rational points. We have not promoted finite residue survival to
global solubility.

## Rank, torsion, independence and 2-primary Sha

The previous equality and S_KUMMER give |G/2G|=16. By S_MW, write
G≅Z^r⊕T with T finite. Kernel/image counting for multiplication by two
on the finite group T gives |T/2T|=|T[2]|=4: the displayed roots exhaust
the rational two-torsion. Hence

    16 = 2^r · 4,

and rank G=2. This rank argument does not presuppose the full torsion
subgroup or independence of P,Q as integral points.

For the full torsion, direct enumeration gives E(F3)={O,(0,0),(1,0),
(2,0)}, of order four, and |E(F5)|=8. S_TORSION_REDUCTION already bounds
the rational torsion by four using the good odd prime 3. Alternatively,
using only prime-to-p injectivity at 3 and 5 excludes every odd-primary
component and bounds the 2-primary component by four. Since K supplies
four rational torsion points, T=K. The three nonzero Kummer signatures
of K additionally show no nonzero two-torsion point is a rational double,
so rational order-four torsion is impossible.

Modulo the image of K, the displayed P and Q classes give a basis of
(G/K)/2(G/K)≅F2². Choose any integral basis of G/K≅Z². The two column
vectors of P,Q give an integer matrix whose reduction modulo two is
invertible. Its determinant is therefore odd and nonzero. This proves
P,Q are independent and their free subgroup has finite odd index. It
does not prove that the determinant has absolute value one. Full
integral generator saturation at odd primes remains unperformed.

S_SELMER and Sel_2=delta(G) give Sha[2]=0. If a nonzero element were
killed by 2^n, it would have exact order 2^j for some j≥1; multiplying by
2^(j−1) would give a nonzero member of Sha[2], a contradiction. Therefore
Sha[2^n]=0 for every n≥1 and the full 2-primary torsion subgroup is zero.
No finiteness assumption on the whole Sha is needed.

An immediate abstract continuation is

    Sel_(2^n) ≅ G/2^nG ≅ (Z/2^nZ)² × (Z/2Z)²,
    |Sel_(2^n)| = 2^(2n+2).

The classes of P,Q and K give these coordinates, since their free
determinant is odd. The natural transition retains the same rational
point and reduces the two free coordinates modulo 2^n; its complete
fiber has four members. This abstract all-n statement follows from the
group argument and the exact sequence; this arithmetic program does
not implement a rational halving or higher-level decoder.

## Hostile cases, evidence and reproduction

The executable rejects (0,1) and the altered point (−16,121) as off-curve
admission errors. Repeating P in both nominal free directions produces
only eight signatures rather than sixteen. The class A has 16 primitive
solutions modulo four and none modulo eight, preserving an explicit
counterexample to treating one shallow residue success as local proof.

From this experiment directory run:

    python -I -B work/arithmetic.py --output evidence/arithmetic.json

The program uses Python's standard library, exact integer/Fraction
arithmetic, and the fixed E34 inputs. It reads no saved PASS, rank label,
curve database, archived result or old checker. Reading the E5 proof and
its checker informed the split-descent method only; all constants,
points, residue counts, witness signatures and conclusions here are
recomputed for E34. The execution log records the actual run. The
all-prime support, coset obstruction, rank and Sha arguments are written
proofs with cited dependencies; no Lean/formal proof is claimed.
