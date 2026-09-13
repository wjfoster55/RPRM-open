# General reconstruction: the condition beyond compatible residues

This is a written elementary argument for a general carrier. It uses standard
finite generation when specialized to an elliptic curve. It is not a claim of
novelty or a proof of the analytic or Sha assertions of BSD.

## Carrier and supplied data

Let G be a finitely generated abelian group, with identity 0. Let
H:G -> R_{≥0} be proper: each set {g:H(g)≤B} is finite. Let positive integers
M_n divide M_(n+1). Supply classes c_n in G/M_nG compatible under reduction.
Equality at level n means equality modulo M_nG, not equality of source points.
The requested readout is the complete fiber of a *single* g with all these
classes. The admitted infinite tower is explicit; the runnable program tests
only its separately stated finite ranges.

For E/Q on any fixed nonsingular rational Weierstrass equation, take G=E(Q).
Its finite generation is the Mordell-Weil theorem. Set H(O)=1; for affine R
with reduced x(R)=a/b, b>0, put H(R)=max(|a|,b). This H is proper directly:
bounded H leaves finitely many rational abscissas, and the quadratic equation
in y has at most two rational roots for each. This works for general
Weierstrass equations, including nonzero a1,a3. O is handled separately.
[Milne, Chapter IV, finite-basis theorem](https://www.jmilne.org/math/Books/ectext6.pdf#page=109).

## Proposition 1: a uniform height bound closes reconstruction

There exists g with all the supplied classes if and only if there is one
finite B such that, for every n, c_n has a representative g_n with H(g_n)≤B.

Proof. A common g supplies B=H(g). Conversely set

    F_n(B) = {g in G : H(g)≤B and [g]_(M_n)=c_n}.

Compatibility makes F_(n+1)(B) a subset of F_n(B). These are nonempty finite
sets by the supplied bound. A descending sequence of nonempty subsets of a
fixed finite set eventually stabilizes at a nonempty set. Each point in that
intersection has every prescribed class. This proves both directions.

If a common representative g exists, the complete unrestricted fiber is

    g + intersection_n M_nG.

Indeed another point has every same class exactly when its difference lies in
every M_nG. Within H≤B, intersect this coset with the height ball; a naive
height bound need not be invariant under torsion translation.

For M_n=n!, this intersection is {0}. In G=Z^r ⊕ T, the free coordinates
divisible by every n! are zero; for n large enough the exponent of finite T
divides n!, so n!T=0. Hence the complete reconstruction fiber is ONE(g).

For M_n=p^n with p prime, the intersection is T_(p'), the subgroup of torsion
of order prime to p. The free coordinates again vanish; the p-primary torsion
is eventually killed, while multiplication by p^n is an automorphism of
T_(p'). The full fiber is g+T_(p'), with |T_(p')| members. Thus a single-prime
tower need not even distinguish all actual rational points.

Without a supplied B or another proof of existence, an unfinished bounded
search stays OPEN. Empty F_n(B) excludes only this B, not all heights.

## Proposition 2: finite compatibility alone does not close reconstruction

In Z, put c_n=3^(-1) mod 2^n. The inverse exists since 3 is odd. It is unique
modulo 2^n, and its reductions are compatible. Every individual class has an
integer representative. If one integer m represented all of them, then
2^n would divide 3m-1 for every n. This forces 3m-1=0, impossible for m in Z.
So the complete source fiber is NONE, although every finite prefix has
integer witnesses. Its inverse-limit value is the 2-adic integer 1/3;
being in Z_2 does not make it an ordinary integer.

This is also an actual E5 example using the previously proved
E5(Q)=ZP ⊕ (Z/2)^2, P=(-4,6). Set c_n=[k_nP] mod 2^nE5(Q), with
k_n=3^(-1) mod 2^n. All classes are rationally realized and compatible.
A single R=mP+T representing them would require m=1/3, impossible.
This obstruction exists even though E5's Sha is trivial. It is an obstruction
to recovering a rational point from completion data, not a new Sha element.

For the abstract Z carrier and H(m)=|m|, this tower has no representatives in
[-B,B] once 2^n>3B+1: the nonzero integer 3m-1 has absolute value at most
3B+1 and cannot be divisible by 2^n. That gives a finite exact separator for
each fixed B. It also proves the height premise of Proposition 1 cannot be
silently supplied by compatibility.

## A finite readback threshold with a supplied integral basis

Suppose an integral basis P1,...,Pr of G/T is already proved and the torsion
coordinate is retained separately. Write q for the full x canonical height
and define A_ij=(q(P_i+P_j)-q(P_i)-q(P_j))/2. Thus the diagonal is q(P_i).
Suppose this Gram matrix satisfies A ≥ lambda I for a certified lambda>0. Then

    hhat(sum m_i P_i + T) = m^t A m ≥ lambda sum m_i^2.

A proved bound hhat(R)≤Bhat therefore gives |m_i|≤C for
C=floor(sqrt(Bhat/lambda)). Any modulus M>2C uniquely recovers each integer
m_i from its residue and this bound: two such integers differ by less than
M. The full torsion coordinate then recovers R. At rank zero there is no
Gram matrix to invert; retain the finite torsion point directly.

This is a conditional finite readback procedure, not a basis-finding
algorithm. Independent points spanning a subgroup of finite index do not
supply integral coordinates for all G/T. The Gram eigenvalue and height
bound must be independently certified. Decimal determinants are insufficient.
[Milne, canonical height and quadratic pairing, IV §4](https://www.jmilne.org/math/Books/ectext6.pdf#page=128).

The threshold is strict: +P and -P collide at modulus 2 with coefficient
bound C=1. A determinant alone cannot supply lambda: the positive definite
matrices [[1,N],[N,N^2+1]] have determinant 1 and arbitrarily small least
eigenvalue. If exact torsion is not retained, its finite-level fiber is
t_0+MT. A modulus divisible by the torsion exponent removes that ambiguity;
large magnitude alone does not guarantee divisibility.

## What this contributes to the general argument

It isolates a necessary and sufficient condition for recovering one rational
point from compatible rational-point quotients, and specifies the torsion
ambiguity. A bounded representation can close this step if it proves a
uniform source-height bound. A bound on labels or carries alone is not such
a bound unless a proved map controls the source height.

It supplies no procedure that decides the bound for every tower, no reason
all locally soluble coverings have rational points, and no identity relating
rank to an L-function. General Sha may be nontrivial; a proposed universal
argument must retain it rather than force every Selmer class to be rational.
