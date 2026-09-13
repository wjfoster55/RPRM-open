# E34: bounded full-BSD and Sha-finiteness applicability audit

**Result: NOT_ESTABLISHED.** This bounded primary-source review did not
identify an applicable theorem that proves either finiteness of the full
`Sha(E/Q)` or the exact complex BSD leading-coefficient formula for

\[
E=E_{34}:y^2=x^3-1156x.
\]

This is the outcome of the sources and hypotheses checked below, not a
universal assertion that no such theorem exists. Four targeted searches and
direct primary-text reads were completed on **12 September 2026**. No curve
database rank, predicted Sha order, or additional curve computation was used.
Earlier interval-audit files were left unchanged.

## Contract and retained inputs

The carrier is this fixed elliptic curve over Q, its actual cohomologically
defined Sha, and its complex Hasse–Weil L-function. The supplied investigation
establishes conductor `18496`, analytic and algebraic ranks two, CM by
`Z[i]`, torsion `(Z/2)^2`, and `Sha[2^infinity]=0`. Its leading coefficient
`c_2=L''(E,1)/2` is enclosed by `6.38511803..6.38518585`. The proof that the
selected two points form a full free basis is now complete in
`GENERATOR_PROOF.md`; that result does not resolve the theorem
applicability below. `FACTOR_COMPARISON.md` adds the rigorous comparison.

Requested readouts are full Sha finiteness and the exact complex BSD
identity. Forward theorem application is enabled only after all of that
theorem's hypotheses are supplied. A partial primary-group result preserves
only that primary readout. This note neither recovers a complete group fiber
nor returns NONE from an unfinished literature search. The evidence grade is
primary-source theorem inspection and written applicability analysis, with
the new 2026 source explicitly retained as a preprint.

## The old E5 theorem fails two separate hypotheses

Creutz–Miller, *Second Isogeny Descents and the Birch and Swinnerton-Dyer
Conjectural Formula*, Theorem 1.1, proves full BSD when the conductor is
below 5000 **and** analytic rank is at most one. Its conclusion includes
finite Sha and the full leading-coefficient identity. For E34,
`18496<5000` is false and `2<=1` is false. Either failure prevents the
application; repairing only one would not suffice. CM, a saturated basis,
or trivial two-primary Sha is not an alternative hypothesis in this theorem.
[Authors' theorem, printed p.2](https://arxiv.org/pdf/1105.4018v2#page=2).

## Other low-rank CM theorems checked

Rubin's CM exposition states its initial BSD theorem over an imaginary
quadratic CM field with the explicit hypothesis `L(E/K,1)!=0`, and its
primewise conclusion is stated for good primes above `p>7`. E34's central
vanishing cannot supply that hypothesis. In particular, merely passing to
the CM field does not turn its positive rank into the finite Mordell–Weil
group required by that theorem's conclusion. The cited main-conjecture
machinery is not, on its own, a full-BSD theorem for every CM rank.
[Rubin, opening theorem](https://swc-math.github.io/aws/1999/99RubinCM.pdf#page=1).

Li–Liu–Tian's Theorem 1.1(i) assumes a **simple** central zero and then
gives finite Sha and the stated ordinary prime part of BSD; E34 has order
two. Their full-BSD family in Theorem 1.2 requires positive squarefree
`n=5 mod 8`, all prime factors `1 mod 4`, and no ideal class of order four
in `Q(sqrt(-n))`. For `n=34`, the first condition fails (`34=2 mod 8`) and
the prime-factor condition fails at 2. No class-group calculation can repair
those failed conditions. The theorem's family has rank one.
[Li–Liu–Tian, Theorems 1.1–1.2](https://arxiv.org/pdf/1605.01481#page=1).

## Genuine rank-two results have a smaller conclusion

Coates–Liang–Sujatha give a usable CM criterion: for good `p=1 mod 4`,
their critical Hecke value
`c_p^+(E)=(Omega_infinity^+)^(-p)L(bar(psi_E)^p,p)` satisfies a valuation
bound. At rank two, valuation exactly 2 implies `Sha[p^infinity]=0`;
valuation at most 3 implies that this primary group is finite. The missing
input here is a certified valuation of that Hecke value for the chosen p.
The real number `L''(E,1)/2` is a different readout.
[Coates–Liang–Sujatha II, section 4, printed p.19](https://arxiv.org/pdf/1005.4206#page=19).

Their Theorem 1.3 executes primewise results below 30,000 for the five
curves `y^2=x^3-Dx` with `D=-14,17,-33,-34,-39`; our `D=1156` is absent.
In particular their `D=-34` means `y^2=x^3+34x`. A matching numeral or
j-invariant does not transfer the computation. Even for their listed
curves, the theorem covers a bounded range of good ordinary primes, not
the full Sha group. Their general Theorem 1.1 only bounds primary coranks
by a quantity growing with p; it does not make those coranks zero.
[Theorems 1.1 and 1.3, printed pp.1–2](https://arxiv.org/pdf/1005.4206#page=1).

Stein–Wuthrich's large rank-at-least-two calculation, Theorem 1.1, is for
**non-CM** curves, good ordinary `5<=p<1000`, and surjective mod-p
representation. Its non-CM hypothesis already excludes E34. Their
Theorem 6.1 instead describes a general structural bridge: the algebraic
p-adic characteristic series has order equal to the Mordell–Weil rank
exactly when the p-adic height pairing is nondegenerate and the p-primary
Sha is finite. A real regulator, or a real complex-L coefficient, supplies
neither the needed p-adic order nor this conjunction. Applying the bridge
would require further compatible p-adic evidence.
[Stein–Wuthrich, Theorem 1.1](https://wstein.org/papers/shark/shark.pdf#page=2),
[Theorem 6.1](https://wstein.org/papers/shark/shark.pdf#page=20).

## A recent rank-two preprint also needs new inputs

Banwait's **8 September 2026 preprint** states a criterion directly for
rank-two CM curves with `L(E,1)=0` and sign +1. Theorem A requires a good
split prime `p>=5`, exclusion from its set `S_E`, and a normalized second
coefficient of the **p-adic** L-function that is a p-adic unit. It then gives
`Sha[p^infinity]=0`. Theorem B relates that unit condition to a unit p-adic
regulator together with trivial primary Sha, or a specified critical-value
combination of valuation two. E34's real interval proves no such unit
condition.

Equation (8) excludes primes arising from bad/local factors, anomalous
reduction, reducible residual representation, comparison constants, and
the relevant ray class group. Those admissions have not been checked here.
The announced `p=577` completion concerns `y^2=x^3+34x`, again a different
curve. The source remains a newly posted preprint; this review checked its
stated hypotheses and conclusion, not its proof or formalization. Even an
admitted successful prime would establish only that primary conclusion.
[Banwait, Theorems A–B](https://arxiv.org/pdf/2609.08431#page=3),
[excluded set (8)](https://arxiv.org/pdf/2609.08431#page=17).

## The exact remaining obligations

For the full Sha finiteness readout, primewise work must eventually supply
both a finite exceptional set and a proof that `Sha[p]=0` for every prime
outside it, plus finiteness of each primary group inside it. This statement
follows directly from primary decomposition of a torsion abelian group.
Checking any fixed number of odd primes does not supply the first
quantifier. Even proving every individual primary group finite would not
alone rule out infinitely many nonzero primary groups.

As an elementary distinguishing case, the abstract group
`direct_sum_(odd p) (Z/p)^2` has trivial two-primary part and every primary
group finite, yet is infinite. This is a logical control, not an assertion
that this group is realized as Sha of a curve. The finite group `(Z/3)^2`
likewise shows that a trivial two-primary group does not force an entire
finite group to be trivial.

For the complex leading-coefficient readout, the supplied Tamagawa numbers
at 2 and 17 are both 4 and the torsion order is 4. With the full minimal
real period and a proved full free basis, the BSD identity would therefore
read

\[
c_2=\Omega_E\operatorname{Reg}_E\#\Sha(E/\mathbf Q).
\]

An independently rigorous factor interval could enclose
`c_2/(Omega_E Reg_E)` near an integer. Without an applicable exact identity,
that quotient has not been identified with the order of the actual Sha;
an interval around 1 also contains nonintegers. Saturation fixes the
regulator's meaning and normalization, but does not prove this connecting
identity. The real formula and full finiteness thus remain separate,
substantial obligations, not routine numerical cleanup.

The existing arithmetic and analytic rank certificates remain intact.
This review establishes no new odd-primary Sha result and no full-BSD
promotion for E34. Reopen the frontier only with an applicable theorem and
its missing primewise or global hypotheses explicitly discharged.
