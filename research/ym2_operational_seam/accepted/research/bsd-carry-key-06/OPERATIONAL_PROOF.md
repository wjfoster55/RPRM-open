# Ordered keys, carries and the coefficient

## 1. What the two numbers supply

The source observation is the reduction of a fixed 5-adic analytic
coefficient: b2 lies in 426+625 Z5. The modulus is 625=5^4. The glyphs
426 are its canonical integer representative at that precision. The
ordinary fraction 426/625 is not the source object.

The finite reduction map Z5 -> Z/625 has a complete residue fiber. At
one additional digit, that fiber has exactly five canonical representatives:

\[
426,\ 1051,\ 1676,\ 2301,\ 2926\pmod{3125}.
\]

Their distinct occurrences share their old reduction. Operations on a
printed word can be studied while retaining its base, width, chosen
representative, and the direction of every map.

## 2. The exact reversal and complete carry

There is an exact mixed-representation operation:

\[
426_{10}\xrightarrow{\text{decimal reversal}}624_{10}
=4444_5\xrightarrow{+1}10000_5=625_{10}.
\]

The second step carries through all four base-five positions. The first
step is decimal reversal; it is not reversal in base five. Indeed
426=3201_5, whose base-five reversal is 1023_5=138.

Freeze the proposed stronger rule rev10(r_N)+1=5^N on canonical residues
0<=r_N<5^N. At N=5 it requires rev10(r_5)=3124, hence r_5=4213,
outside the carrier. In particular none of the five possible lifts works.
The finite key at N=4 remains true; this particular precision-compatible
extension is refuted. A different scale-dependent operation needs its
transition rule supplied explicitly.

## 3. Two exact role charts

One recovered interpretation uses endpoint-gap-endpoint records
(A,2,B), with B=A+2 and A=0,...,7. Its midpoint is (A+B)/2.
The endpoint reflection

\[
J(A,2,B)=(9-B,2,9-A)
\]

is an involution on this eight-state carrier. It gives 426 <-> 325.
Here 426 has endpoints 4 and 6, midpoint 5; 325 has endpoints 3 and 5,
midpoint 4. The gap remains its own port. Complementing all three digits
would instead give M(426)=573.

The historical pi legend names endpoint span 325 and its midpoint/gap/
corner identities. A second role assignment is a new candidate inspired
by those identities. Let m=1,...,7, g=2, A=m-1, B=m+1, c=m+2.
Encode the same record by alpha=(m,2,c) or beta=(c,2,B):

| m | alpha | beta |
|---:|---:|---:|
| 1 | 123 | 322 |
| 2 | 224 | 423 |
| 3 | 325 | 524 |
| 4 | 426 | 625 |
| 5 | 527 | 726 |
| 6 | 628 | 827 |
| 7 | 729 | 928 |

The map H(m,2,c)=(c,2,m+1) has inverse
H^-1(c,2,B)=(c-2,2,c), enabled when B=c-1 and c=3,...,9.
Both encodings are injective. Gap alone has MANY(7) records; the full
output 625 has ONE(426) as its input under this declared chart.
Every row satisfies rev10(alpha)+1=beta, with no carry in its final
decimal digit. Only beta=625 is a power of five, so the intersection of
this seven-state chart with positive powers of five is exactly one row.

This explains the ordered 4,2,6 -> 6,2,5 observation within a complete
finite family. The role of 4 differs between the two interpretations:
it is an endpoint in J and a midpoint in H. Neither interpretation was
derived from the curve as a requirement on its analytic coefficient.
At m=8 the outer value is 10 and leaves H's three-digit carrier.

Sources: the copied [pi legend](dependencies/PI_CLOSURE_LEGEND.md),
especially its midpoint, gap and corner definitions and its span record
325; the [scope audit](dependencies/operational_numbers/PI_CLOSURE_LEGEND_AUDIT.md).
The legend supplies useful roles; the H encoding above is newly proposed.

## 4. Multiplication retains a lower layer and moves its fiber

Now use the coefficient as an actual multiplication operation on Z/625.
Its old residue is b=426=1+25*17. Every x has a unique expression
x=a+25t with 0<=a,t<25. Since 25^2=625,

\[
bx\equiv a+25(t+17a)\pmod{625}.
\]

Thus the lower two base-five digits a remain fixed, while t is translated
modulo 25. The inverse multiplier is 1-425=201 modulo 625. The complete
cycle census is 25 fixed points, 20 cycles of length 5, and 20 cycles
of length 25. For unit x, 17a is a unit modulo 25, so its entire
25-element fiber is one orbit. The finite program checks all 625 states.

The power formula b^k=1+425k modulo 625 gives

\[
b^5\equiv251\pmod{625},\qquad b^5\equiv1\pmod{125}.
\]

Five repetitions return the coarser state and still retain a finer
remainder 250=2*125. With the newly computed lift, b^25=1251 mod 3125:
twenty-five repetitions close modulo 625 while retaining a finer carry.

There is also a written statement about the exact admitted coefficient.
The known residue implies b2=1+25u with u a 5-adic unit. If z has
v5(z)=k>=2, the term 5z in (1+z)^5-1 has valuation k+1; every other
binomial term has strictly greater valuation. Induction proves

\[
v_5(b_2^{5^j}-1)=2+j\qquad(j\ge0).
\]

Every five-fold iteration advances this carry by one precision level.
No such finite iteration equals 1 in Z5 itself. This is an exact
retained-carry mechanism. It holds for every unit in 1+25 Z5 whose
difference from 1 has valuation 2, so its coarse cycle signature cannot
select which of the five possible next coefficient digits is correct.

## 5. Fiving and its missing integer bit

The recovered half-decade contract writes n=10w+5h+r, h in {0,1},
r in {0,...,4}. The strong operation n->n+5 changes
(w,h,r)->(w+h,1-h,r). It descends to addition by 5 modulo 625.

Holding the decade w fixed gives a different operation
f(n)=n+5(1-2h). It does not descend to Z/625:

\[
426\equiv1051\pmod{625},\qquad
f(426)=421,\quad f(1051)=1056\equiv431\pmod{625}.
\]

Since adding 625 toggles h, every one of the 625 paired representatives
fails this proposed descent. Retaining the integer modulo 1250 repairs
it. Equivalently retain the modulo-625 value and its parity bit: the
Chinese remainder compatibility condition mod gcd(625,2)=1 imposes no
restriction. All 1,250 states were checked, including the involution.
Parity is additional integer information; it is not supplied by a
5-adic coefficient. This repair explicitly changes the carrier.

A canonical representative can define a new operation, but does not
restore the claimed involution: 620 -> 0 -> 5 is a counterexample.

The historical source is
[PRESTIGE-AND-NUMBER-OPERATIONS.md](../../recovered-concepts/PRESTIGE-AND-NUMBER-OPERATIONS.md),
the section "Finite fiving donor and its exact inverse". Its retained
winding principle transfers to the multiplication example in section 4;
its literal decimal half-turn is not identified with that multiplication.

## 6. A 4/6 operation on the actual analytic coordinate

The coordinate already used in the analytic calculation has character
6=1+5. The opposite nearby principal unit is -4=1-5. Their product is
1-25, giving the exact identity

\[
\log_5(4)+\log_5(6)=\log_5(1-25).
\]

Here log5(4)=log5(-4), because log5(-1)=0. The sum has valuation 2;
the difference has valuation 1 by their convergent power series.
Both logarithms have valuation 1. Therefore
u=log5(-4)/log5(6) is a unit, u=-1 mod 5.

PARI uses the branch with log5(5)=0; the computations use genuine
5-adic arguments, not real logarithms.
[Official logarithm documentation](https://pari.math.u-bordeaux.fr/dochtml/html-stable/Transcendental_functions.html#log).

Replacing gamma by gamma^u changes its character from 6 to -4 and
T'=gamma^u-1=uT+O(T^2). For a series of exact order two, rewriting in
T' multiplies its quadratic coefficient by u^-2. The matching
rank-two scalar height determinant is multiplied by the same u^-2,
so their quotient is unchanged.

The fresh finite calculation gives u=1544 mod 3125 and the transported
coefficient 1091 mod 3125. Multiplying back by u^2 recovers 2301 mod 3125.
This is a dependent coordinate readback, not a second source of analytic
information or a proof of the BSD quotient.

## 7. Fresh refinement and the actual next missing operation

The exact normalization, quadratic twist factor, and classical measure
are those proved in the copied [coefficient proof](dependencies/COEFFICIENT_PROOF_05.md).
The current classical residue-ball sum extends from level 5 to level 6.
Its uniform squared-log error is O(5^7); division by
4*log5(6)^2 loses exactly two digits. The fresh results are:

| Classical level | Raw second derivative | Coefficient |
|---:|---|---|
| 4 | 2725 mod 3125 | 51 mod 125 |
| 5 | 2725 mod 15625 | 426 mod 625 |
| 6 | 65225 mod 78125 | 2301 mod 3125 |

The exact-symbol overconvergent computation also returns 2301 mod 3125.
Its agreement is a cross-check; the written error bound establishes the
classical precision. Both use the same normalized classical symbol.
The lower-order vanishing still uses the admitted algebraic rank and
theorem conditions documented in experiment 05.

For a concrete route to an independent digit prediction, retain the
previously defined component comparison

\[
S=5\Lambda_c=Ub_2/R,\quad
U=5C_5[\log_5(6)/5]^2,\quad R=R_{\rm MST}.
\]

U and R are 5-adic units. If an independently justified comparison
supplies the target s and supplies U,R,s modulo 3125, define
H(b)=Ub-sR. Provided H(426)=0 mod 625, exactly one lift digit satisfies

\[
j=-\frac{H(426)}{625}U^{-1}\pmod5.
\]

This follows by substituting b=426+625j and reducing modulo 3125.
It is a genuine complete ONE digit fiber under those supplied ports.
The current arithmetic regulator certificate provides only its residue
modulo 5, and the exact target s is not established. Setting a target to
the desired BSD value would assume the missing identity.

The new operations therefore sharpen a possible proof task: derive a
law from the arithmetic data that forces the required scalar or all its
compatible lifts, with the period and height conversions retained.
An infinite compatible identity with an argument covering every level
would be stronger than finitely many matching digits. The present work
proves finite maps and the stated carry law; full BSD and total Sha stay
OPEN. No claim of a new general number-theory theorem or proof-assistant
verification is made.
