# Finite Selmer certificates and the Sha torsion tower

**Scope and evidence.** Arbitrary elliptic curves over `Q`; written deductions
from standard Kummer theory, Mordell–Weil and finite Selmer groups. No BSD
assumption, novelty claim, formal proof or curve-specific computation is made.
Sources and their hypotheses were checked on 2026-09-12.

## Contract

Let `E/Q` be a nonsingular elliptic curve, `p` any prime and `n >= 1`.
Write `G = E(Q)`, `T = G_tors`, `r = rank G`, and `A = Sha(E/Q)`.
Equality of rational points, quotient classes and cohomology classes belongs
to its respective group; these are different carriers. Put

\[
A[p^n]=\{a\in A:p^na=0\},\qquad A[p^\infty]=\bigcup_{n\ge1}A[p^n].
\]

The supplied ports are `E,p,n`, optionally a certified Selmer bound, torsion
data and independent points. Missing ports include `r`, the Sha contribution
and a full generating set. The receiver asks which of these are determined.
The forward operations are Kummer maps and taking cardinalities. Reversing
them requires the full fibers, not independent choices of the missing data.
An uncertified bound or unfinished point search leaves its conclusion OPEN;
a singular equation is outside this contract. No assumption on reduction at
`p`, rational `p`-torsion or analytic rank is imposed.

## 1. Exact finite-level defect

Use continuous Galois cohomology and all places `v` of `Q`, including infinity.
Define

\[
\operatorname{Sel}_{p^n}(E/\mathbf Q)=
\{c\in H^1(\mathbf Q,E[p^n]):
\operatorname{res}_v(c)\in\delta_{v,n}(E(\mathbf Q_v)/p^nE(\mathbf Q_v))
\text{ for every }v\},
\]
\[
A=\ker\!\left(H^1(\mathbf Q,E)\longrightarrow
\prod_v H^1(\mathbf Q_v,E)\right).
\]

**Proposition 1.** For every admitted `E,p,n`,

\[
0\longrightarrow G/p^nG\xrightarrow{\delta_n}
\operatorname{Sel}_{p^n}(E/\mathbf Q)
\xrightarrow{\beta_n}A[p^n]\longrightarrow0,
\tag{1}
\]
\[
\boxed{\left|\operatorname{Sel}_{p^n}(E/\mathbf Q)\right|
=p^{nr}|T/p^nT|\,|A[p^n]|.}
\tag{2}
\]

**Proof.** Multiplication by `p^n` on `E(overline Q)` is surjective. The
cohomology sequence of its kernel `E[p^n]` gives

\[
0\to G/p^nG\to H^1(\mathbf Q,E[p^n])\to H^1(\mathbf Q,E)[p^n]\to0.
\]

The local sequences have the same form and commute with restriction. A
global lift of an element of `A[p^n]` satisfies each local Kummer condition,
because its image in every `H^1(Q_v,E)` is zero. Conversely every Selmer
class maps to `A[p^n]`. This proves (1), including surjectivity.
Mordell–Weil gives a noncanonical isomorphism `G ≅ Z^r ⊕ T`, with `T` finite.
Consequently `|G/p^nG| = p^(nr)|T/p^nT|`. Finite Selmer groups make all three
groups in (1) finite; multiplying orders proves (2). ∎

These source inputs appear in [Stoll, *Descent on Elliptic Curves*, §1.1,
pp. 2–5](https://arxiv.org/pdf/math/0611694#page=2) and [Milne, *Elliptic
Curves* (2006), Chapter IV, finite-basis theorem, equations (22)–(23),
Theorem 3.1](https://www.jmilne.org/math/Books/ectext6.pdf#page=109).
Stoll §1.3, p. 11 already states the corresponding rank/cardinality identity.

If `T[p^infinity] ≅ ⊕_i Z/p^(a_i)Z`, define the normalized defect

\[
D_n:=\frac{|\operatorname{Sel}_{p^n}|}{p^{nr}|T/p^nT|}=|A[p^n]|,
\qquad
\log_p D_n=\log_p|\operatorname{Sel}_{p^n}|-nr-\sum_i\min(n,a_i).
\tag{3}
\]

The torsion quotient has the same order as `T[p^n]`; they need not be
identified canonically. Formula (3) requires the actual rank. Replacing it
with a point-search lower bound does not isolate Sha.

For the map `G -> Sel_(p^n)`, the complete preimage of `c` is empty when
`beta_n(c) != 0`, and is `P + p^nG` when `c = delta_n([P])`. Its finite
quotient class is unique, while its rational-point representatives need not
be. Cardinalities alone do not produce `P` or decide `beta_n(c)` class by class.

## 2. A useful finite certificate, with the saturation gap retained

**Proposition 2.** Suppose the supplied, verified data comprise:

1. `t = dim_Fp E(Q)[p]`, determined exactly;
2. rational points `P_1,...,P_k` independent modulo torsion, with a proof of
   independence;
3. an unconditional upper bound `dim_Fp Sel_p(E/Q) <= U`, supported by
   complete coverage of the ambient classes and sound local exclusions;
4. the equality `U = k + t`.

Then

\[
r=k,\qquad \dim_{\mathbf F_p}\operatorname{Sel}_p=k+t,
\qquad A[p^\infty]=0.
\tag{4}
\]

**Proof.** Independence gives `r >= k`. At `n=1`, (2) gives
`dim Sel_p = r + t + dim A[p]`. Thus
`k+t <= r+t <= dim Sel_p <= U = k+t`; every inequality is equality.
Hence `r=k` and `A[p]=0`. Any nonzero element of `p`-power order would yield
a nonzero element of order `p` by multiplication, a contradiction. ∎

This is a certificate schema, not a certificate supplied for a particular
curve here. A safe finite set for descent includes infinity, `p`, and every
bad-reduction prime. Stoll Theorems 1.1–1.2 justify a finite unramified
ambient group; §2, p. 18 gives the local-condition computation. His smaller
set includes infinity, divisors of the descent integer, and primes whose
Tamagawa number is not coprime to that integer. A proved overestimate can
suffice in Proposition 2. A sampled list or an unproved class/unit-group
calculation cannot supply the stipulated bound. [Stoll, pp. 4–5,
18](https://arxiv.org/pdf/math/0611694#page=4)

**Saturation blind spot.** Even under (4), `H = T + sum Z P_i` need not equal
`G` or be `p`-saturated. In the free-group case `G/T = Z·P`, the point `pP`
has full rank but generates an index-`p` subgroup and maps to zero modulo
`p`. This is an abstract lattice control, independent of the Sha calculation.

If the actual Kummer images of `H` additionally span `Sel_p`, then (1) gives
`G = H + pG`. Since `G/H` is finite by the rank equality, multiplication by
`p` is surjective, hence bijective, on `G/H`. Therefore `p` does not divide
`[G:H]`: this proves `p`-saturation, still allowing an index prime to `p`.
A full basis requires eliminating that remaining index. Stoll explicitly
separates finding independent points and saturation on p. 3.
[Stoll, §1.1](https://arxiv.org/pdf/math/0611694#page=3)

## 3. What growth, and one genuine plateau, prove

**Proposition 3.** For the fixed prime `p`, the following are equivalent:

- `A[p^infinity]` is finite;
- the integers `D_n = |A[p^n]|` are bounded as `n` varies;
- `D_n = D_(n+1)` for some `n >= 1`.

When the last condition holds, `A[p^infinity] = A[p^n]` and its order is `D_n`.

**Proof.** Finiteness gives an exponent bound and therefore eventual
constancy. Boundedness gives an equal adjacent pair, since the finite groups
`A[p^n]` are nested and their orders are nondecreasing integers. Equality of
orders at adjacent levels gives equality of those subgroups. If an element
had exact order `p^m` with `m > n`, multiplying it by `p^(m-n-1)` would
produce an element in `A[p^(n+1)]` of exact order `p^(n+1)`, which cannot
belong to `A[p^n]`. Thus no such element exists, proving the assertion. ∎

In particular, once rank and torsion are certified, two exact Selmer orders
can certify finiteness of the whole `p`-primary part if their *normalized*
defects agree. An equality of upper estimates is insufficient. The raw
Selmer orders can grow with rank even when Sha is zero. Abstractly
`(Q_p/Z_p)[p^n]` has order `p^n`: finiteness at every level alone does not
give a uniform bound.

There is also a finite-depth rank ambiguity. In the abstract cardinality
model (2), with trivial `T`, the data `(r,A) = (r,(Z/p^K Z)^2)` and
`(r+2,0)` give identical orders `p^(n(r+2))` for every `1 <= n <= K`.
They separate at `n=K+1`. Thus any prescribed finite initial segment can
confound rank and finite primary torsion when no independent rank
certificate is supplied. This is a control on the inference from orders,
not a claim that both models arise from elliptic curves.

For all primes together, Sha is a torsion abelian group ([Milne, Chapter
IV §2, p. 110](https://www.jmilne.org/math/Books/ectext6.pdf#page=118)), so

\[
A=\bigoplus_p A[p^\infty].
\]

To see the decomposition, apply the Chinese remainder identity to the
finite order of each element, producing its unique primary components.
It follows that `A` is finite exactly when each primary part is finite
**and only finitely many are nonzero**. Bounded growth for each individual
prime does not supply this second condition. The abstract torsion group

\[
B=\bigoplus_{p\ \mathrm{prime}}\mathbf Z/p\mathbf Z
\]

is infinite, while `|B[p^n]|=p` for every `n >= 1` and every fixed prime `p`.
This refutes that inference for torsion groups; it is **not** a claim that
`B` is realizable as `Sha(E/Q)`. A finite exceptional-prime set plus verified
primary bounds inside it and vanishing outside it would close this gap.

The results provide conditional finite certificates with explicit inputs.
They do not establish their success for every curve, an analytic-rank
identity, or the BSD leading-coefficient formula. Those conclusions remain
OPEN in this artifact.
