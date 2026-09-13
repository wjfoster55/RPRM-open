# BSD E5 test 01 — return to William

For the fixed rational curve **E: y²=x³−25x**, the descent, analytic
nonvanishing argument, and cube/readback maps held up. The new result is

\[
\boxed{\frac{556371}{250000}<L'(E,1)<\frac{1114529}{500000}}.
\]

These endpoints are exactly **2.225484 and 2.229058**; the width is
**1787/500000 = 0.003574**, below 1/100. The first permitted attempt,
coefficient cutoff **M=40**, achieved it. No larger cutoff or refinement was
needed. This is a rigorous enclosure using standard theorems and exact rational
inequalities, not agreement with the bundle's exposed decimal illustration.

## What the arithmetic establishes

A doubling class records whether the difference of two rational points is
twice another rational point. It is a quotient of the elliptic-curve group,
not reduction of the point coordinates modulo two.

Away from the identity and the three points with y=0, the Kummer signature is
the triple of rational squareclasses of **x, x−5, x+5**. Zero is not a
multiplicative squareclass: the exceptional entries use the product of the
two root differences, and the identity has signature (1,1,1). The standard
Kummer theorem identifies its kernel with 2E(Q).

The all-place Selmer conditions restrict squareclass support to the sign and
primes 2 and 5. The square-product requirement gives 64 triples; the real
sign condition leaves 32. An independently written binary lifting tree
enumerated every primitive residue solution of the two covering equations:
32 signatures survive modulo 2, 16 modulo 4, and **eight modulo 8**.

Crucially, each of those eight has an actual rational representative:
O and the three rational two-torsion points, together with P=(-4,6) plus
each of those four points. Thus necessary local survival is paired with
global existence. The separate coset proof excludes (2,2,1) and (2,1,2)
modulo 4, and (1,2,2) modulo 8. Local admissibility is a subgroup containing
the witnessed eight-element subgroup, so each excluded representative
excludes its whole coset. This proves completeness.

Consequently **Sel₂=E(Q)/2E(Q) has size eight**. Mordell–Weil finite generation
and the four rational points killed by doubling give 8=2ʳ·4, hence
**rank E(Q)=1**. The Selmer exact sequence gives **Sha[2]=0**. A nonzero
element of any finite 2-power order would yield a nonzero element of order
two, so **Sha[2ⁿ]=0 for every n≥1**. The cited theorems, their hypotheses,
exceptional cases, and written coverage proof are in [ARITHMETIC_PROOF.md](ARITHMETIC_PROOF.md).

## What the analytic proof establishes

The rational substitution x=5u, y=25v identifies E with **5v²=u³−u**.
The checked congruent-number-family formulas give conductor **800** and
functional-equation sign **−1**. Minimality follows from discriminant
2⁶·5⁶; the reductions at 2 and 5 are cusps, so their additive Euler factors
are **1**. The good-prime recurrence must not be used at those two primes.

Modularity and the Mellin split give an entire completed function odd about
s=1. Its normalizing factor is nonzero there, which proves **L(E,1)=0
exactly**. Differentiating the split integral gives

\[
L'(E,1)=2\sum_{n\ge1}\frac{a_n}{n}E_1(\alpha n),\qquad
\alpha=\frac{\pi}{10\sqrt2},\quad
E_1(x)=\int_x^\infty\frac{e^{-t}}t\,dt.
\]

This uses analytic continuation and an absolutely convergent integral
representation, not a center substitution into the original Euler product.
Independent prime counts and Euler recurrences recover only a₁=1, a₉=−3,
a₁₃=−6, a₁₇=−2 as nonzero through 20. Every link of the original bound was
checked, including the infinite tail, reproducing

\[
L'(E,1)>
\frac{615556405007957768183}{937494780448358006784}>
\frac{13}{20}.
\]

Thus the central zero is **simple**, and the arithmetic rank and analytic
zero order independently agree at one. [ANALYTIC_THEOREMS.md](ANALYTIC_THEOREMS.md)
records the opened primary sources, conditions, normalization, and estimates.

## What the new coefficient interval means

A coefficient is the number multiplying a specified power in an expansion.
Here the enclosed number is c₁ in **L(E,1+t)=c₁t+O(t²)**. It is different
from the Euler/Fourier coefficient a₁=1.

The extension computed coefficients through 40 and enclosed each retained E₁
integral using 832 midpoint panels, with a proved second-derivative error bound.
Machin's formula and integer square roots enclosed alpha; alternating exponential
series and outward rounding on an 80-bit dyadic grid enclosed function values.
Negative coefficients reverse interval endpoints. Signed products and sums
were exact rational operations.

A **tail bound** limits the combined effect of every omitted term. Hasse's
theorem, the correct Euler factors, and divisor pairing give |aₙ|≤2n for
all n. With alpha>1/5 and exp(−alpha)<5/6 this yields

\[
|R_{40}|<\frac{120}{41}\left(\frac56\right)^{41}.
\]

The interval's width contains about 0.003318917 from the two-sided infinite
coefficient tail, 0.000254621 from quadrature, and less than 0.000000464
from exporting readable endpoints. The remaining constant and exponential
enclosure contributions are much smaller. These rounded descriptions are
for readability; [DERIVATIVE_INTERVAL.json](DERIVATIVE_INTERVAL.json) contains
the exact rational ledger and every retained term. Its entries sum exactly
to the final width. [INTERVAL_DERIVATION.md](INTERVAL_DERIVATION.md) proves
the inequalities and explains why the endpoints are strict.

## Readback, transport, and controls

The five-bit map is a bijection onto the 32 candidate signatures and transports
all **1,024** XOR pairs to squareclass multiplication. The eight admissible
vertices were obtained from the arithmetic filter before comparing with
(1−u)(1−v). A nontrivial basis change passes when its readout is transported;
retaining the old readout produces an explicit mismatch.

The compatible quotient coordinates are Z/2ⁿ × (Z/2)², with transition
(m,T)↦(m mod 2ⁿ,T). Exact readback retains
**R=mP+T+2ⁿRₙ**. The checker completed 112 selected mP+T cases at levels
1–4 and six spot checks obtained by a separate rational-x search. The maximum
admitted point-coordinate numerator/denominator was 1,053 bits, within the
declared 4,096-bit execution cap; there is no unbounded cost claim.

P and −P merge at level one but separate at level two. Likewise,
Q=2P=(1681/144,−62279/1728) and O both have coarse label (0,O), while their
level-two labels are (2,O) and (0,O). All four rational halves of Q were
checked and none is a double. A retained remainder reconstructs the actual
source; the coarse label alone has two finer lifts and does not choose one.
The old quotient operations remain valid. Eight classes already include
their identity; a wrapper adds no ninth class.

All six requested controls received explicit outcomes: off-curve admission
rejection; changed-model certificate rejection; a₉=0 recurrence mismatch;
an OPEN infinite-sum claim after removing its all-term tail premise; the
lost-remainder collision; and coherent/stale frame transport. These are
actual changed inputs or claims. The no-tail control preserves the missing
proof obligation rather than treating a finite head as a complete proof.

## Evidence and stopping boundary

Both supplied programs ran freshly; all 35 original archive members remain
byte-identical. Independent arithmetic and analytic implementations used no
saved result fields or database ranks. Standard theorems remain explicitly
cited rather than claimed as new formal proofs. Optional numerical backends
were not run. One initial independent-checker syntax error was corrected;
its failed execution log remains alongside the successful run. No failed
baseline mathematical obligation was found.

The complete portable runner then completed all five stages with exit code
zero in `runs/portable_validation/`. Its arithmetic records, constants,
coefficient tables, and interval attempts exactly match the first independent
runs. A separate peer review checked the enclosure code and written derivation,
then independently reassembled all signed terms and the rational error ledger.
These reproductions are distinguished from newly independent mathematics.

This establishes the stated one-curve rank equality and 2-primary result.
It does **not** establish the full BSD leading-coefficient formula, odd-primary
Sha, total Sha order, or that P is a saturated integral generator. P's odd
free index suffices for all the 2-power quotients but does not settle odd
saturation. Those frontiers remain open in this experiment. No other lane
was modified or interrupted. This one experiment is complete and stops here.
