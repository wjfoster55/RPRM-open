# Exact local multiplier connections for E34

The new relation concerns the actual local conversion factor appearing in
the BSD comparison route. It is a mathematical identity for this curve's
Frobenius roots, with no decimal fitting.

## 1. The two prime paths

Work in K=Q(i), i²=−1. Fresh point counts on E:y²=x³−1156x give

| p | #E(Fp) | ap=p+1−#E(Fp) | πp (positive imaginary representative) |
|---|---:|---:|---|
| 5 | 8 | −2 | −1+2i |
| 13 | 20 | −6 | −3+2i |

The good-reduction Frobenius polynomial is X²−apX+p. The written CM
identification from experiment 02 is retained in `dependencies/`.
The local arithmetic here also directly checks trace and norm.

For π=πp and barπ its conjugate, put

\[
C_p=(1-\pi^{-1})^{-1}(1-\bar\pi^{-1}).
\]

This is the factor in BKS Theorem 6.2 after choosing π to be the allowable
root. Its denominator is nonzero in our cases: neither root is1.
[BKS, Theorem 6.2 and the root convention in §6.1](https://kurihara.math.keio.ac.jp/bks4.pdf#page=40).

Our own exact algebra, using π·barπ=p, gives

\[
C_p=\frac{\pi(\bar\pi-1)}{\bar\pi(\pi-1)}
    =\frac{p-\pi}{p-\bar\pi},\qquad
C_p\bar C_p=1.
\tag{1}
\]

The shared prime is visible before taking any quotient:

\[
\pi_{13}-1=-2i\bar\pi_5,\qquad
\bar\pi_{13}-1=2i\pi_5.
\tag{2}
\]

Thus the Frobenius-minus-one factor at 13 contains precisely a Gaussian
prime over 5, with the displayed unit and orientation. Substitution yields

\[
\boxed{C_5=\frac{4-3i}{5},\quad
C_{13}=\frac{63-16i}{65},\quad
C_{13}=C_5\frac{12+5i}{13}.}
\tag{3}
\]

The familiar triples arise exactly: 4²+3²=5², 12²+5²=13², and
63²+16²=65². The cross terms also matter:
(4−3i)(12+5i)=63−16i. These triples describe rational coordinates on
the norm-one circle. They do not by themselves identify an earlier
informal coordinate transformation or the global BSD multiplier.

An equivalent shared-factor chart is
A=(2+i)/(2−i), B=(3−2i)/(3+2i): C5=−iA and C13=AB.
Retaining one original factor makes the quotient reversible. Keeping only
the ratio leaves the common factor undetermined.

## 2. What is happening at 5 inside prime 13

Choose the embedding i≡2 mod5. Then π5 is a unit and barπ5 has valuation 1.
At the same embedding, π13≡1 and barπ13≡3. Hence (2) gives

\[
v_5(C_5)=-1,\quad v_5(C_{13})=-1,\quad
v_5(C_{13}/C_5)=0.
\]

This is a cancellation in a fixed local field. The curve supplies a
second description: its Frobenius polynomial at 13 is
X²+6X+13≡(X−1)(X−3) mod5. The nonzero order-five points on E(F13),
recomputed with the group law, are (4,4), (4,9), (9,6), (9,7).
Thus the divisibility by 5 has an actual torsion interpretation.

For the own-prime refinement at 13 choose i≡5 mod13. Then π13 is the
unit root and v13(C13)=−1. The independent readback derives the factors
from the original expression, enumerates the points, Hensel-lifts both
specified embeddings, and checks all precision levels through p^8.
It retains denominator valuations and extra digits needed for absolute
precision. It never inverts a multiple of p modulo p^k.

Conjugating sends C to C^−1 and reverses the own-prime valuation. At good
ordinary p, the conjugate root has valuation 1 and fails the allowable-root
condition. Therefore the identity C·barC=1 is not a second ordinary
comparison theorem using the same pairing. No p=13 height or Sha theorem
has been admitted in this experiment.

## 3. General local formula and an oriented factor-removal rule

Write π=a+bi, p=a²+b², d=p−a. Equation(1) becomes

\[
C_p=\frac{d^2-b^2-2dbi}{d^2+b^2},\qquad
d^2+b^2=p(p+1-2a)=p\,#E(\mathbf F_p).
\tag{4}
\]

Thus the reduced rational coordinate denominators divide p·#E(Fp).
This is a support bound, not a claim that every divisor survives
cancellation. For example π101=1+10i and #E(F101)=100, but
C101=(99−20i)/101 has no remaining5 denominator or oriented5 valuation.

There is an exact way to remove the 5-part of any norm-one z∈Q(i)^×.
Let v=v5(z) at i≡2. Since norm(z)=1, its valuation at the conjugate
prime is−v. C5 has valuations (−1,+1) at these two primes and no
denominator or numerator prime support elsewhere. Consequently

\[
z^\circ=z\,C_5^v
\tag{5}
\]

has valuation 0 at both primes over 5; its reduced rational coordinate
denominators are coprime to 5. The inverse is z=z°C5^(−v).
This elementary factor-removal rule applies to known Gaussian scalars;
it does not claim that the unknown BSD scalar belongs to this carrier.

More precisely, on G={z in Q(i)^×:z·bar(z)=1}, the map
S5(z)=z C5^v5(z) is a multiplicative idempotent retraction onto ker(v5). For any w in
ker(v5), its complete fiber is w C5^Z. Retaining the integer v gives the
exact coordinate pair (S5(z),v); the inverse is (w,v)↦w C5^(−v).

Fresh examples show why the direction must be retained:

| p | #E(Fp) | v5(Cp), i≡2 | exact removal of its 5-part |
|---|---:|---:|---|
| 13 | 20 | −1 | C13/C5=(12+5i)/13 |
| 29 | 40 | +1 | C29·C5=(21−20i)/29 |
| 37 | 40 | −1 | C37/C5=(35+12i)/37 |
| 101 | 100 | 0 | C101=(99−20i)/101 |

There is also a precise joint-shadow relation. For p≠5 let
A=v5(πp−1) and B=v5(barπp−1), both nonnegative integers. Since πp
and barπp are5-adic units, (1) and the norm identity imply

\[
s=v_5(\#E(\mathbf F_p))=A+B,\qquad
d=v_5(C_p)=B-A.
\]

The sum records how much5-torsion the reduction count allows, while the
difference records the orientation of this local multiplier. Together
they recover both branches:

\[
\boxed{A=(s-d)/2,\qquad B=(s+d)/2.}
\tag{6a}
\]

For the abstract pair carrier(A,B)∈N0², this coordinate map has image
exactly s≥|d| with s,d of the same parity; curve-derived pairs occupy a
certified subset, with no claim that every abstract pair is realized. At13
the pair is(s,d)=(1,−1), recovering(A,B)=(1,0); at 29 it is(1,+1),
recovering(0,1); at 101 it is(2,0), recovering(1,1). A zero difference
can therefore conceal equal positive contributions. This is an exact
arithmetic instance of retaining both a sum and a signed difference.
It identifies a local pair of valuations, not a global L-value.

The program proves finite valuations by lifting i until the modulus
exceeds the nonzero integer numerator norm. A vanishing residue at that
precision would force the norm divisible by a larger integer than itself.
All reported valuations therefore stabilize; they are not guessed from
an insufficient zero residue.

For an additional count-based directed graph, connect a good odd prime p
to every prime divisor ell of #E(Fp). E has all four rational2-torsion
points, which reduce distinctly at such p, so 4 divides #E(Fp). For odd
ell, Hasse's bound gives ell≤#E(Fp)/4≤(sqrt(p)+1)²/4<p. The target2
also satisfies2<p. Every edge decreases. Iterating this graph cannot
produce a directed cycle; a bad or non-admitted endpoint needs its own
contract before further expansion. This graph follows torsion norms,
and discards the orientation that distinguished13 from 29.

## 4. Prime/lucky census and a failed quotient

The fresh finite carrier is1..1000. Lucky numbers use positional deletion:
start with odd positive integers, then repeatedly remove every kth
remaining entry, where k is the next unused surviving entry after 1.
The prime predicate is computed separately. Prefix stability under
extending the sieve bound to 2000 is checked; analytically, deletions and
their positions inside an initial prefix depend only on that prefix.
Once the next deletion step exceeds its length, no later step can affect it.

The four pointwise prime/lucky codes have counts
(00,01,10,11)=(722,110,125,43). All addresses are retained in the JSON.
Among79 good ordinary primes,37 have5 dividing the point count; only 7
of those37 are lucky. Lucky 13 has v5(C13)=−1, whereas lucky 613 and
lucky 769 have v5(Cp)=+1; lucky 433 has valuation−2. Thus lucky membership
does not determine even this oriented factor-removal exponent on the
tested carrier. It remains available as a selector, with this failed
readout preserved. Lucky prime 31 is supersingular and lucky 9 is composite;
neither can silently enter the good-ordinary-prime contract.

The old finite ray action is freshly recomputed: the two conjugate
Frobenius5 generators span256 elements, and including the conjugate13
generators spans512. A stronger attempted quotient fails. Attach C5
multiplicatively to each forward π5 step. Modulo68, π5 has order 16,
so the empty word and the 16-step word end at the same residue state.
Their accumulated factors are1 and C5^16, with oriented5 valuations0
and−16. They are unequal, despite both having complex norm1.

This disproves descent of this particular assigned multiplicative readout
to the residue state. It does not assert that this assigned weight is a
Kato transition law. The proposed lift must retain the multiplicative
residual, and an actual Euler-system adapter still requires its own proof.
