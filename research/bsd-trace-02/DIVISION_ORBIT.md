# A character-weighted division orbit for the p=5 trace

**Computed result:** the character-weighted trace is 25 modulo 125, up to
its single overall sign. In particular its 5-adic valuation is exactly two.
The fresh execution of `work/division_orbit.py`, recorded in
`evidence/division_orbit.json`, evaluates all 256 conjugates and verifies
their square-root identities. This replaces a degree-256 polynomial
factorization with an explicit torsion-point calculation.

The neighboring full-orbit method gives 100 modulo 125, which is the
negative of this result. The two group laws and orbit derivations are
different; the exact coefficient-ring arithmetic is shared and explicitly
attributed. The computation supplies the previously missing critical-value
valuation. Applying the stated Sha theorem also uses the separately
established local and rank hypotheses.

The carrier is an algebraic closure of K=Q(i), with CM action
i(x,y)=(-x,iy), together with its unramified five-adic realization. Equality
is exact field or finite-ring equality. The supplied model is
E': y²=x³+289x, isogenous over Q and isomorphic over K to
E34: y²=x³−1156x. The requested readout is the trace of 2ρ⁵+289ρ, modulo
125, up to an overall sign. All finite assertions below concern this curve and
this prime. They assert no uniform result over all odd primes.

## Conductor and the two-part decomposition

Put λ=1+i, f=68 and f1=68/λ=34(1−i). Use the odd model D'=-289
in the family y²=x³−Dx. Its conductor is f by
[CLS I, Lemma 3.2, PDF p.13](https://arxiv.org/pdf/0901.3832#page=13).
The same page gives the base curve E0: y²=x³−x conductor λ³.
The problematic even-D substitution retained in the preceding experiment is
not used. Neither is the odd-exponent hypothesis of CLS I, Lemma 3.3 applied
to the square 17².

The ray class field F of modulus f has degree 512 over K. Its subfield H
of modulus f1 has degree 256. If A is a primitive f1-division point, then
K(x(A))=H and the square root ρ used by the CLS formula belongs to H and
generates it. These are
[CLS II, Lemmas 4.1 and 4.4, PDF pp.13–15](https://arxiv.org/pdf/1005.4206#page=13).

Take T=(17,17√34). Direct doubling gives 2T=(0,0). The formula

    x([λ]P) = (x(P)²+289)/(2i x(P))

gives x([λ]T)=-17i, a nonzero point in E'[2]. Thus T has exact
annihilator λ³ as a Z[i]-module element. Let R be a primitive element of
E'[17], meaning [17]R=O and neither [4+i]R nor [4−i]R is O. Then
A=T+2R has exact annihilator f1, since the two annihilator ideals are
coprime. Every point with λ³ component T and primitive 17 component has
this form. Choosing the other sign of T only changes the parametrization
of the same x-coordinate orbit.

## A rational formula for coherent square roots

For two distinct nonopposite points U,V, let b(U,V) be the intercept of
their chord:

    b(U,V) = (y(U)x(V)−y(V)x(U))/(x(V)−x(U)).

Substituting y=mx+b into y²=x³+289x produces a monic cubic with constant
term -b² and roots x(U), x(V), x(U+V). Consequently

    b(U,V)² = x(U)x(V)x(U+V).

Define

    g(T,R) = b(T+R,R)/b(T,R).

Dividing two chord identities proves

    x(T+2R) = 17 g(T,R)².

Thus ρ=√17 g(T,R) is a square root of x(A), with a single coherent
overall sign. Also b(-U,-V)=-b(U,V), so

    g(-T,-R) = g(T,R).

All denominators used here are nonzero. For example x(T)=x(R) would
give T=±R, incompatible with coprime nontrivial torsion orders; and
x(T+R)=x(R) would give T=O or T=-2R. An intercept could vanish only if
one of its three x-coordinates were zero, which would likewise force an
impossible equality between the nontrivial λ-primary and 17-primary
components. The same argument survives good reduction at 5 because all
these torsion orders are prime to 5. Hence the denominators are units in
the unramified ring modulo 125.

## Why the weights are the actual Galois signs

There is exactly one primary representative for each Gaussian ideal:
α≡1 mod λ³. For α=a+bi this means a odd, b even, a+b≡1 mod4.
Because E0 has conductor λ³, its type-one Hecke character satisfies
ψ0((α))=α for every such α. The CM reciprocity action on torsion is
τa(P)=[ψ(a)]P; the action is stated in
[CLS II, equation (64), PDF p.13](https://arxiv.org/pdf/1005.4206#page=13).

E' is the quadratic twist of E0 by d=17i: over K(θ), θ²=d, the map
(x,y)↦(dx,dθy) is an isomorphism. If χ(τ)=τ(θ)/θ, transporting the
torsion action through this explicit map gives

    τ_α(R)=[χ(τ_α)α]R,     τ_α(T)=χ(τ_α)T.

For the second assertion one may directly check that E0[λ³] is rational
over K: the extra order-four x-coordinates are ±i, with y-coordinates
±(1∓i). This avoids the excluded square-D application of Lemma 3.3.

The Weil pairing on E'[17] places the seventeenth roots of unity in its
division field. The quadratic Gauss sum in that cyclotomic field is a
choice of √17, and an automorphism ζ↦ζ^u multiplies that Gauss sum by
the Legendre symbol (u/17). The determinant of the CM action
[χ α] on the two-dimensional F17-module is Norm(α), since χ²=1.
Therefore

    τ_α(√17) = ε(α)√17,    ε(α)=(Norm(α)/17).

Combining these identities with simultaneous-negation invariance gives

    τ_α(ρ)=ε(α)√17 g(T,[α]R).

There are 512 primary ray representatives modulo 68. Reduction modulo
17 has 256 unit values and exactly two representatives above each value.
Both representatives give the same displayed expression: their unknown
quadratic-twist signs have canceled. The 256 x-coordinates are distinct,
since T+2[α]R=±(T+2[β]R) forces α=β in the positive case, while the
negative case would give 2T in E'[17], impossible. Thus the expression
gives all 256 conjugates exactly once, rather than an arbitrarily selected
polynomial factor.

The desired trace is accordingly

    Σ_{α in (Z[i]/17)×} ε(α) [2(√17 g(T,[α]R))⁵
                              +289√17 g(T,[α]R)]
    =289√17 Σ_α ε(α)(2g(T,[α]R)⁵+g(T,[α]R)).

For D'=-289, the corrected CLS trace formula has
A1(X)=12(2X⁵+289X), alpha=1+i and beta=68. Thus

    c5_plus(E') = ±Tr_H/K(2ρ⁵+289ρ)/(2·68⁵).

The real period of E' is twice that of E34, while their Hecke characters
agree under the K-isomorphism. Therefore c5_plus(E34)=32 c5_plus(E'),
so every displayed scaling factor is a 5-adic unit. This records only
the normalization used in
[CLS II, equation (77), PDF p.19](https://arxiv.org/pdf/1005.4206#page=19),
with the explicit model/period comparison proved in the preceding
experiment. It follows that the computed trace valuation is the required
v5(c5_plus(E34))=2.

Replacing R by [β]R multiplies this trace by ε(β), hence at most changes
its sign. The analytic point defining CLS's ρ has its λ³ component among
±T: its [17] multiple is a real quarter-period point on E', with x=17.
Thus arbitrary primitive R is sufficient to determine the requested
valuation. If a transported numerical point initially has T-coordinate
-17, multiplication by i brings it to this convention before evaluation.

## Replay contract and limits

`finite_admission()` checks all 512 primary residues, their two-element
fibers, all 65,536 multiplicativity pairs of ε, and the split-17 tests.
`chord_trace()` uses its own E' affine group operations. It checks exact
torsion orders, primitivity, all 256 chord square identities and sign
identities, and distinct squared conjugates. Numerical finite-ring
arithmetic, if imported from the neighboring trace implementation, is
explicitly attributed in the generated receipt; sharing that arithmetic
does not constitute an independent implementation of it.

The replay uses the finite étale ring

    A=(Z/125Z)[z]/(z¹⁶−2),  i=57.

The replay freshly proves z¹⁶−2 irreducible modulo five by Rabin's
criterion, using its own polynomial remainder calculation: z^(5^16)=z
and gcd(z¹⁶−2,z^(5^8)−z)=1. It reads no saved field certificate.
This makes A the reduction of the unramified
degree-16 extension's integer ring. For an elliptic curve with good
reduction, its prime-to-five torsion is finite étale, so the exact
prime-to-five torsion points checked over A are the reductions of unique
unramified torsion lifts. The rational formulas and CM action commute
with reduction. Consequently summing the checked orbit in A computes
the algebraic trace modulo 125, rather than a merely analogous finite
field statistic.

Only the lifted point's two coordinate arrays are read from the adjacent
receipt. Its status and trace are not used. The replay rechecks the
E34 equation, applies the explicit dual isogeny

    x'=(X−1156/X)/4,
    y'=Y(1+1156/X²)/8,

and checks the E' equation. It obtains T=[17]P' and
R=[9](P'−T), normalizing by i if needed, then independently checks their
orders and split primitivity. A Hensel lift of z⁸ gives √17=111z⁸ in A.
The final trace vector is (25,0,...,0), so it is divisible by 25 and is
nonzero modulo 125. This proves the exact valuation, without estimating
a real number or rounding a decimal.

Reproduce from the repository root after the adjacent trace receipt has
been generated:

    python -I -B research/bsd-trace-02/work/division_orbit.py

The flag `--admission-only` intentionally leaves the numerical trace
OPEN and is not the command used for the delivered numerical receipt.

The distinguishing hostile case is a 17-torsion point lying on one of the
two split-17 eigenlines: it has integer order 17 but is not primitive as a
Z[i]-module element, and would produce an incomplete orbit. Both Gaussian
annihilator checks are mandatory. A second hostile case is omitting ε:
the resulting unweighted sum is not the desired trace because √17 itself
has nontrivial Galois action.

The evidence grade is a written CM/Galois proof plus exact finite
computation when its receipt is present. It is not a formal proof. The
overall BSD identity and all unexamined prime-primary parts remain OPEN.
