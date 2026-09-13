# Independent audit of bounded-height tower reconstruction

Audit date: 12 September 2026. Scope: `RECONSTRUCTION.md`, the exact
inverse-of-three counterexample, and the proposed finite readback threshold.
The written arguments below use ordinary finite-set and abelian-group
mathematics. They claim no novelty and no general BSD consequence.

## Contract and verdict

The carrier is the exact group `G=E(Q)` on a supplied nonsingular rational
Weierstrass model, including `O`. The ports are compatible quotient classes
`c_n in G/M_nG`, with positive `M_n | M_(n+1)`, and, when supplied, one
uniform proper-height bound `B`. The missing port is a single rational point
realizing **all** classes. The receiver retains rational-point equality and
the complete reconstruction fiber. A tower in an inverse limit is an
explicit additional carrier; its elements are not thereby rational points.

The propositions in `RECONSTRUCTION.md` are correct. Their strongest precise
form is: uniform bounded representatives are equivalent to a common point;
when a point `R` exists, the complete unrestricted fiber is
`R + K`, where `K=intersection_n M_nG`. The height-restricted fiber is
`(R+K) intersect {H<=B}`. These are distinct fibers.

Existence requires only the finite height ball: the sets
`{R:H(R)<=B, [R]_(M_n)=c_n}` are nonempty and nested. If their intersection
were empty, each element of the first finite set would disappear at some
finite stage; the largest such stage would be empty, a contradiction.
Finite generation is used for the subsequent kernel computation, not this
existence argument. Thus the hypothesis is sufficient but is not an
algorithm for establishing its own uniform bound.

For a fixed rational Weierstrass model, the definition
`H(O)=1`, `H(R)=max(|a|,b)` for reduced `x(R)=a/b`, `b>0`, is proper:
there are finitely many such `a,b` below any fixed bound, and at most two
rational ordinates per abscissa. Absolute real coordinate size alone is not
this height; denominator size is essential.

Writing `G=Z^r direct_sum T`, factorial moduli give `K=0`, while `p^n`
gives `K=T_(p')`. The latter is exactly the prime-to-`p` torsion subgroup.
It need not be trivial. A naive-height restriction can remove some torsion
translates; a canonical-height restriction cannot, because canonical height
is unchanged by torsion translation. The rank-zero case has only the finite
torsion fiber and needs no Gram matrix.

## Exact counterexample and hostile controls

The imported E5 input is
`E5(Q)=ZP direct_sum (Z/2)^2`, with `P=(-4,6)`, as proved in
[the existing generator proof](../bsd-e5-completion/GENERATOR_PROOF.md).
This audit reuses that stated result; it does not re-prove its descent or
saturation dependencies.

For `n>=1`, choose the least nonnegative inverse of three modulo `2^n`:

```text
k_n = (2^n+1)/3       when n is odd;
k_n = (2^(n+1)+1)/3   when n is even.
c_n = [k_n P] in E5(Q)/2^n E5(Q).
```

The classes are compatible because both consecutive coefficients are
inverses of three after reduction modulo `2^n`. A common point `mP+T`
would require `3m-1` divisible by every `2^n`, hence `3m=1`, impossible
for integer `m`. In E5, the torsion coordinate is also forced to zero
at every positive level. This gives the complete fiber **NONE**, by proof,
despite a rational witness for every finite prefix.

More quantitatively, every representative has free coefficient congruent
to `k_n`, so its absolute coefficient is at least

```text
d_n = min(k_n, 2^n-k_n) = (2^n-(-1)^n)/3.
```

For either consistently chosen canonical-height normalization `q`, every
such representative has `q >= d_n^2 q(P)`, and `q(P)>0`. Consequently the
minimum representative canonical height tends to infinity. The bounded
difference between logarithmic naive and full-x canonical height then also
excludes a uniform naive-height bound.

Three controls locate the actual boundary:

- `R_n=(2^n+1)P` has unbounded chosen-representative height but represents
  the constant tower of `P`. Growth of a chosen sequence is insufficient;
  the lower bound must cover **every** representative of each class.
- If `P=3Q` in an alternative input, the inverse-of-three tower is realized
  by `Q`. The primitive free-coordinate input is load-bearing.
- For integers `|m|<=B`, a level with `2^n>3B+1` excludes every candidate,
  since nonzero `3m-1` then has magnitude below the modulus. Excluding one
  height ball never excludes all heights without the general argument.

## Finite readback: normalization and saturation matter

Let `P_1,...,P_r` be a **proved integral basis** of `G/T`, with chosen lifts,
and fix the canonical-height function `q`. Define the matrix explicitly by

```text
A_ij = (q(P_i+P_j)-q(P_i)-q(P_j))/2.
q(sum m_i P_i + T) = m^t A m.
```

This convention avoids a factor-of-two ambiguity: Milne's bilinear `B`
omits the displayed division by two, so `q=m^t Bm/2`. Positive definiteness,
quadraticity, bounded-height finiteness and the height normalization are
standard dependencies in [Milne, *Elliptic Curves*, second edition,
IV, Theorem 4.7, Proposition 4.9 and Theorem 6.1](https://www.jmilne.org/math/Books/EC2.pdf#page=129).

A certified inequality `A >= lambda I`, `lambda>0`, and a proved bound
`q(R)<=Bhat` yield `|m_i|<=C`, where
`C=floor(sqrt(Bhat/lambda))`. Use an exact or safely certified integer
bound, not an unchecked floating-point rounding. A residue modulus `M>2C`
determines each such integer coordinate uniquely. Existence still needs
the supplied height premise or verification of the recovered candidate.
The strict inequality is necessary as a general guarantee: at `C=1,M=2`,
the distinct free points `P` and `-P` collide and have equal height.

Full-rank independent points may span a proper sublattice. For example,
using `2Q` in the rank-one group generated by `Q` makes `Q` have coordinate
`1/2`; integer-vector reconstruction would omit a genuine point. Saturation
or a correctly retained larger coordinate lattice must be supplied.

The regulator determinant alone does not certify the required eigenvalue
bound. The positive definite matrices `[[1,N],[N,N^2+1]]` have determinant
one and smallest eigenvalue tending to zero. Full certified Gram information
or another certified lower bound is needed.

If only the quotient `G/MG` is retained, its unresolved torsion fiber is
`t_0+MT`. Retaining the exact torsion coordinate removes it; alternatively,
choosing `M` divisible by the exponent of `T` makes `MT=0`. A large modulus
by itself does not imply this divisibility.

## Evidence and remaining scope

The proofs above cover all their stated group-theoretic domains. A fresh
Python integer check passed the inverse formulas, compatibility, minimum
absolute coefficients and the realizable-growth control at levels 1--40;
it also passed fixed-box exclusion for integer bounds 0--100 and the
`+1/-1 mod 2` boundary collision. Those finite checks corroborate, but do
not replace, the written proofs. No Lean or other formal proof was run.

Uniform source-height bounds, a certified integral basis, and a positive
Gram bound remain supplied obligations for a general reconstruction task.
Nothing here identifies Selmer classes with rational points, establishes
general Sha vanishing, or proves an analytic BSD identity.
