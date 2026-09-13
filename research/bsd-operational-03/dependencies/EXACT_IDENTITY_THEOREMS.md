# E34: theorem routes to an exact complex identity

**Outcome: OPEN.** This review identified a precise, published conditional
bridge to the complex BSD formula, but did not establish its missing
rank-two comparison for E34. Nor did it find an applicable proved theorem
giving the normalized real coefficient a rational denominator bound.
This is a bounded applicability result, not a claim of nonexistence.

The practical issue is exactness: we can enclose the two real quantities
tightly, but we still need a theorem that puts their quotient in a discrete
set. Extra decimal places alone do not supply that theorem.

## Contract and inherited evidence

The fixed curve is `E: y^2=x^3-1156x` over Q, with conductor 18496,
CM by Z[i], algebraic and analytic ranks two, and full free basis
`P=(-2,48), Q=(-16,120)`. The inherited investigation supplies
`Sha[2^infinity]=0`, torsion order 4, and Tamagawa product 16. These are
attributed dependencies, not new results of this note:

- [Previous theorem frontier](input_source/FULL_BSD_FRONTIER.md).
- [Factor conventions and comparison](input_source/FACTOR_COMPARISON.md).
- [Full-basis proof](input_source/GENERATOR_PROOF.md).

Let `Omega=integral_(E(R)) |dx/(2y)|`, including both real components;
let Reg be the determinant for the full x-height pairing of that basis;
and set

\[
Q_E=\frac{L''(E,1)/2}{\Omega\operatorname{Reg}}.
\]

The accepted exact interval implies
`0.999920542 <= Q_E <= 1.000092816`. Requested readouts are an exact
identity `Q_E=1`, a proved rationality/denominator statement sufficient to
force it, and, separately, identification with the actual order of Sha.
An evaluation is enabled only with the stated theorem hypotheses and
normalizations. An interval has no inverse recovering the L-function and
does not give a complete equality fiber. The present literature search is
OPEN, not NONE. Evidence grades are cited theorems, explicit conditional
implications, and the elementary written separation argument below.

## 1. A substantive Iwasawa-to-complex bridge

Burns–Kurihara–Sano, *J. Math. Soc. Japan* 76 (2024), Theorem 7.6, proves
the p-part of **complex** BSD under Hypothesis 2.2 (`H^1` is Z_p-free,
positive rank, finite `Sha[p^infinity]`), their Iwasawa main conjecture,
their infinite-level Generalized Perrin–Riou conjecture, and nonzero
Bockstein regulator. Its conclusion is equality of Z_p-lattices, hence
permits a p-adic unit factor.
[Hypothesis 2.2](https://kurihara.math.keio.ac.jp/bks4.pdf#page=12),
[Theorem 7.6](https://kurihara.math.keio.ac.jp/bks4.pdf#page=56).

Proposition 4.14 makes the conjectural comparison explicit:

\[
\kappa_\infty=
\frac{L_S^*(E,1)}{\Omega_\xi R_\infty}\,R_\omega^{\mathrm{Boc}}. \tag{1}
\]

Here the left side is a derived Kato zeta element, while the Bockstein
regulator is cohomological. At rank two, `L_S^*` is the second Taylor
coefficient with specified Euler factors removed. Their period and height
conventions require an explicit conversion to ours. Equation (1) is
equivalent to Conjecture 4.8, not a theorem proved there. No certificate
here establishes (1), the Bockstein nonvanishing, or the required odd-primary
finiteness. Invoking a main conjecture alone skips essential hypotheses.
[Proposition 4.14](https://kurihara.math.keio.ac.jp/bks4.pdf#page=28).

## 2. Why the proved CM regulator theorems do not supply this coefficient

Kings's *The Tamagawa number conjecture for CM elliptic curves*, Theorem
1.1.5, has precise inputs: a CM elliptic curve over its class-number-one
imaginary quadratic field, `k>=0`, and a prime away from 6 and the Hecke
conductor. It constructs a rank-one O_K-module inside
`H_M^2(E,k+2)` and relates its Deligne regulator to the leading term at
`s=-k`, together with an integral p-adic determinant comparison. Section
1.2 explicitly identifies the corresponding values as `L(psi,k+2)`.
[Theorem 1.1.5](https://arxiv.org/pdf/math/0003113#page=7),
[section 1.2](https://arxiv.org/pdf/math/0003113#page=9).

The critical mismatch is `-k=1`, which would require `k=-1`, outside the
theorem. The regulator of those higher K-theory classes is not the
Mordell–Weil height determinant. Extending the comparison to the central
motivic object is a new theorem obligation; a CM label does not perform
that extension. Valid identities at the admitted integer weights do not
by themselves justify a differentiated identity at an excluded weight.

As a concrete check on more explicit formulas, Ito's hypergeometric CM
Beilinson formulas compare regulators in `H_M^2(E,Q(2))` with `L(E,2)`
or, by the functional equation, `L'(E,0)`, on specified small-conductor
curves. For example, Theorem 3.7 gives such an identity for conductor 64.
Its derivative is at **zero**, and its class and regulator have different
types from our rank-two Mordell–Weil data. It therefore supplies neither
`L''(E34,1)` nor a denominator bound for `Q_E`.
[Ito, Theorems 3.6–3.7](https://arxiv.org/pdf/1605.01145#page=12).

## 3. Two different meanings of a higher Gross–Zagier formula

Yun–Zhang's published higher-derivative formula concerns `F=k(X)` for a
smooth proper curve over a finite field of odd characteristic, an
everywhere-unramified PGL_2 automorphic representation, and its quadratic
base change. It identifies even central derivatives with intersections of
Heegner–Drinfeld cycles on shtuka spaces. Its rank-two derivative is a
genuine theorem, but its base field is a function field and its geometric
receiver is that intersection pairing. No theorem in that result transports
it to `E34/Q` and `Reg(P,Q)`.
[Yun–Zhang, introduction and hypotheses](https://math.mit.edu/~zyun/Taylor_Expansion_published.pdf#page=2).

Chan-Ho Kim's *A higher Gross–Zagier formula and the structure of Selmer
groups* instead compares Kolyvagin-system data and Kurihara numbers. Its
working hypotheses in section 2.1 require a **non-CM** elliptic curve,
`p>=5`, a surjective mod-p representation, and a Manin constant prime to p.
The non-CM hypothesis excludes E34. The paper's higher formula is not a
theorem equating our real second derivative to the full Gram determinant.
[Kim, abstract](https://arxiv.org/pdf/2203.12161#page=1),
[working hypotheses](https://arxiv.org/pdf/2203.12161#page=4).

These distinctions matter for an attempted new proof. One must produce
cycles or derived arithmetic classes in the admitted number-field setting,
prove the exact derivative formula, and then identify its pairing with the
full Mordell–Weil regulator. Importing a formula's name supplies none of
these comparison steps.

## 4. A recent CM theorem with a superficially matching rank

Castella's 2025 CM Tamagawa result, Theorem A, works over a field F where
all CM endomorphisms are defined and `F(E_tors)/K` is abelian. It assumes
the associated Hecke L-function has **simple** central vanishing. There
are also split-prime and conductor conditions. Remark 1.1.1 explains that
the resulting ordinary Z-rank over F is two because the Hasse–Weil
L-function factors into the Hecke character and its conjugate.
[Castella, Theorem A and Remark 1.1.1](https://arxiv.org/pdf/2407.11891#page=2).

That is not E34's rank-two problem over Q. At the CM base field Q(i),
the (-1)-quadratic twist of `y^2=x^3-1156x` is the same equation; hence
quadratic base-change factorization gives
`L(E/Q(i),s)=L(E/Q,s)^2`, of order four. Equivalently, the relevant
Hecke factor has order two rather than the required one. The larger base
field does not repair the simple-zero hypothesis. This check preserves
the distinction between rank over Q, rank over the CM field, and rank as
an O_K-module.

## 5. An exact denominator lemma would already finish the real equality

There is a sharply stated weaker target than all of BSD:

> **E34 bounded-rationality target (UNPROVED here).** The real number
> `Q_E` is rational and, in lowest terms, has positive denominator at most
> 10,000.

**Written implication.** If `Q_E=a/b`, `1<=b<=10000`, and `Q_E!=1`, then
`|Q_E-1|=|a-b|/b>=1/10000`. But the accepted interval lies strictly
between `1-1/10000` and `1+1/10000`. Thus that target would force
`Q_E=1` using the existing interval, without any new approximation.

A theorem supplying another explicit denominator bound would also be
useful: refine the interval until it excludes every other admitted
rational. Rationality with no effective denominator bound does not make
finite numerical isolation valid; `1+1/100000` is a rational noninteger
already inside the present interval. Likewise, ruling out sampled
denominators proves no coverage statement for larger denominators.

No primary theorem checked above establishes this bounded-rationality
target for E34. In particular, algebraicity of a higher critical Hecke
value does not imply rationality of our central derivative quotient.

## 6. The actionable missing comparison

The next theorem-bearing target is the **exact archimedean coefficient
comparison**, represented concretely by (1), specialized to E34 with all
Euler, period, height and local factors matched. It must be proved from
independently constructed arithmetic objects; defining one of those
objects using the desired real quotient and then asserting equality would
be circular. A nonzero p-adic regulator or primary-Sha computation can
discharge useful inputs, but does not prove that exact comparison.

The real-equality route needs a proof that `Q_E` lies in an explicitly
bounded rational set, or a stronger exact identity. The full-BSD route
additionally needs a theorem identifying that real value with the order
of the actual Sha and establishing its finiteness. Even a proof of
`L''(E,1)/2=Omega Reg` would not, by itself, identify the cohomological
group's order.

More generally, one p-adic valuation does not determine a positive
rational number; even finitely many valuations leave untested primes.
Without prior rationality, a real quotient does not even have a canonical
p-adic valuation. The cited conditional theorem works with specified
comparison maps into C_p; this is additional structure, not a license to
apply `v_p` directly to a decimal enclosure.

**Plain-language frontier:** we have proved how closely the numbers
agree. To prove that they are exactly equal, we need an exact arithmetic
reason that the quotient cannot be one of the nearby nonintegers. The
published derived-zeta comparison specifies such a research direction,
but its essential rank-two equality is still an unproved input in this
investigation. Calling it a remaining lemma describes the obligation; it
does not make proving it routine.

## Search boundary

Six targeted searches were used, covering: CM central rationality;
higher Gross–Zagier over number/function fields; CM Tamagawa and
Beilinson regulator theorems; and the generalized Perrin–Riou comparison.
The linked primary full texts, including the published 2024
Burns–Kurihara–Sano theorem, were inspected on 12 September 2026.
The old low-rank exclusions remain in the inherited note and were not
used as a substitute for this stronger bridge analysis. No new curve
calculation, database expected answer, or formal verification was run.
