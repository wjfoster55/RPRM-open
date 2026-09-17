# RPRM catch-up synthesis — 17 September 2026

An outside-in reading of RPRM by a synthesis lane, written as a friendly thesis
defence, plus one recommended non-BSD research target.

**Start here:** [`RPRM-understanding-thesis-defense.pdf`](RPRM-understanding-thesis-defense.pdf)
— 69 pages, thirteen numbered chapters plus appendices. The markdown source sits
beside it.

**Then read Appendix E**, which records what happened when the hostile cases the
document declared were actually run overnight. Two of them bit, one of them
against the document's own headline claim, and the priority search produced a
better result than either outcome it was hedging against.

**Then read Appendix F**, written later the same night, which proves the
conjecture the rest of the document is careful to call a conjecture — and, in the
same four lines, explains why the classical version of the object does not have
the result at all. The research record is [`FRAGILITY.md`](FRAGILITY.md).

This directory is a research record, not a publication. Nothing here upgrades a
finite test to a theorem, a written proof to a formal proof, or a hash to a
meaning. Where a theorem is claimed, a written proof is given and every step of
it is separately machine-checked in exact arithmetic; that is still a written
proof, not a formal one. Every quantitative statement carries a domain and an
evidence grade, and proving a statement is not the same as establishing that
nobody has proved it before — no novelty is claimed anywhere in this directory.

**The theorem was then attacked twice, and both attacks changed the record.** A
literature review found that the closed form is a corollary of a published
theorem and that the condition already has a name; a hostile audit found three
wrong explanatory claims around a proof it otherwise confirmed. The corrections
are in the documents where the errors were, marked as withdrawals rather than
quietly edited, and each was re-derived here before being accepted. What survived
both is the extremal law — and it survived in better shape than it started, since
the same proof turns out to cover the published total-map monoid.

## Contents

| File | What it is |
|---|---|
| [`RPRM-understanding-thesis-defense.pdf`](RPRM-understanding-thesis-defense.pdf) | The document. 69 pp. Combined first- and third-party account, core contract with fibers computed, lens maturity table, process-honesty chapter, steelman, criticisms, 51 defence questions, the pick, portable briefing appendix, the overnight addendum, and the proof |
| `RPRM-understanding-thesis-defense.md` | Markdown source of the above |
| [`FRAGILITY.md`](FRAGILITY.md) | The research record for the pick: typed claim, five hostile cases, prior-art separation, dispositions, and what is still owed |
| [`05-portable-briefing-for-other-gpts.md`](05-portable-briefing-for-other-gpts.md) | Self-contained briefing to paste into any other model. No prior context assumed |
| [`WILLIAM-WORKING-STYLE.md`](WILLIAM-WORKING-STYLE.md) | Sanitized operating page: standing corrections and the three-role abduction/verification split |
| [`01-first-party-rprm.md`](01-first-party-rprm.md) | Ingest lane 1 — the project's self-account, read from the repository spine |
| [`03-independent-math-reading.md`](03-independent-math-reading.md) | Ingest lane 3 — an independent mathematical reading, run cold, `verify.py` executed |
| [`04-coverage-gaps.md`](04-coverage-gaps.md) | What was searched for, found, and still missing |
| [`notes/extremal-order-TXP.pdf`](notes/extremal-order-TXP.pdf) | **Standalone 10-page mathematical note**, readable by a transformation-monoid audience with no RPRM vocabulary at all: the extremal shape theorem for Sarkar–Singh's `\|T(X,P)\|`, proof, hostile cases, literature position, evidence grades. Source: [`notes/extremal-order-TXP.md`](notes/extremal-order-TXP.md) |
| [`LITERATURE-sigma-E.md`](LITERATURE-sigma-E.md) | The real literature review. Cost us the count and the condition; left the extremal law standing |
| [`EXCHANGE-LEMMA-AUDIT.md`](EXCHANGE-LEMMA-AUDIT.md) | Independent hostile audit of the proof. Verdict THEOREM; three surrounding claims rejected, all three retested and withdrawn here |
| [`tools/`](tools/) | Eleven exact-arithmetic verification scripts and their raw outputs |

Ingest lane 2 (process history) is held outside this repository. It contains
private material. Its usable content is distilled into `WILLIAM-WORKING-STYLE.md`.

## The pick

**Make RPRM's coverage boundary into a computable number: the fragility spectrum
of a quotient under unknown operations.**

RPRM insists an operational quotient is valid only relative to a *declared*
operation set. Every modeller's operation set is incomplete, and nobody has
turned that into an invariant. For a partition `C` of a finite carrier, count the
arity-`a` partial operations that `C` survives in the exact O05 sense (matching
enabledness, matching successor block), and define fragility as the complement
fraction.

| Component | Status |
|---|---|
| Closed form `sigma_1(C) = prod_i ( 1 + sum_j n_j^{n_i} )`, and the arity-`a` generalisation | Derived; confirmed by exhaustive brute force against **every** partial map for `n <= 5` at arity 1 and `n <= 3` at arity 2 |
| Null control: discrete partition survives everything, `F = 0` | Declared before running; holds for `n = 1..8` |
| Extremal law: for fixed block count `m`, `argmax = (n-m+1, 1, ..., 1)`, `argmin =` balanced | **THEOREM**, at every arity, for the uniform prior over partial maps. Found first by exhaustive search (903 cells to `n = 45`, zero counterexamples), then proved. See `FRAGILITY.md` §8d–8e |
| **Exchange lemma** — moving one element from a smaller block to a larger one strictly increases survival; implies the extremal law | **THEOREM.** The profile supplies both the bases inside `f(k) = 1 + sum_j n_j^k` and the exponents at which `f` is evaluated. Separate them: Karamata makes `f` pointwise larger, and `f` is a sum of exponentials hence log-convex, so spreading the two exponents apart at fixed sum cannot decrease their product. Higher arity by convex order |
| Why the classical successor-only monoid has **no** such law | **ONE(separation).** Its factor function is `sum_j (n_j+1)^k - (m-1)` — a sum of exponentials **minus a positive constant**, which is not log-convex. Controlled: hold the bases fixed and drop only the subtraction, and both log-convexity and the exchange lemma come back (`0` vs `66` failures in 42,903 exchanges). Adding a constant is harmless; subtracting one is not |
| `sigma_E(j+1,j-1)/sigma_E(j,j) -> cosh^2(1) = 2.381097845...` | **ONE(constant).** Written derivation, then verified in exact arithmetic to `j = 20,000`. Splitting a balanced pair apart multiplies survival by a fixed factor that does not wash out |
| Extremal law for the **total-map** prior | **THEOREM**, every arity — promoted §8h after audit. Same proof; its factor `sum_j n_j^k` is also a sum of exponentials. At arity 1 this is Sarkar–Singh's published `\|T(X,P)\|` |
| Extremal law for the **idempotent** prior | **OPEN.** 0 failures in 466 exchanges to `n = 13`, but the idempotent count provably does **not** factor over blocks, so there is no factor function for the mechanism to use. A closed form for it is derived and brute-force validated |
| Hostile cases: arity 2, arity 3, total-only, idempotent-only | All run. Survived: `n <= 12`, `n <= 10`, `n <= 18`, `n <= 7`. Zero failures |
| Hostile case: **non-uniform priors** | **Bit.** The `argmin` half fails under injective-partial and permutation priors. The `argmax` half survives every class but one. Six counterexamples retained |
| Fragility is **not monotone** in block count | Observed. At `n = 6`, total collapse `(6)` has `F = 0.603`; balanced `(2,2,2)` has `F = 0.981` |
| Admissible domain sizes of a surviving operation = **subset sums of the profile** | Written proof. `(6)` admits only `{0,6}`; `(3,2,1)` admits all of `0..6` |
| Applied corollary: uniform binning is the most fragile `m`-block abstraction | **Restricted.** Holds under partial, total and idempotent priors — at `n = 20, m = 10` the blob survives `1.7 x 10^7` times more often. **Reverses under bijective priors** |

### Priority, and the result it produced

The classical partition-preserving transformation monoid is Pei's, enumerated for
arbitrary finite partitions by **Sarkar–Singh**, arXiv:2006.04242, and — for the
partial, uniform case — by **Cicalò–Fernandes–Schneider**, arXiv:1210.4775, with
order `(m(n+1)^n - m + 1)^m`. **Its condition is successor agreement only, with no
condition on the domain.** RPRM's enabledness condition cuts out a strictly
smaller submonoid. Deriving the classical count independently reproduces the
published order exactly in all 22 cases checked, which verifies the
identification rather than assuming it.

The ratio is the **enabledness price**: at `n = 8` with balanced four-block
compression, `rho = 83,521/1,185,921` — **93% of the abstractions the classical
monoid admits are rejected by enabledness.**

And then the thing nobody planned. Over the same 231 `(n, m)` cells with
`3 <= n <= 24`, the classical monoid has **no clean extremal shape — 14 argmax
and 41 argmin exceptions** — while the enabledness-enforced submonoid has an
exact one with **zero exceptions in 903 cells to `n = 45`**. Where they disagree
the extremal profiles **invert**, first at `n = 11, m = 9`. *The `sigma_E` half is
now a theorem; what stays OPEN is a characterisation of which cells the classical
monoid fails in.*

Reproduce with `python -I -B tools/fragility.py`,
`tools/fragility_hostile.py`, `tools/fragility_priority.py`.

### The literature review, and what it cost

[`LITERATURE-sigma-E.md`](LITERATURE-sigma-E.md) is the real review that the
single-pass search had left owed. **It went against us on two of four questions,
and that is recorded rather than buried.**

| Question | Verdict |
|---|---|
| Closed form `sigma_E` | **Not new.** A one-line corollary of Sarkar–Singh Thm 6.1: adjoin a sink `*` as a singleton block and `sigma_E(P) = \|T(X+{*}, P+{{*}})\| / (n+1)`. Verified exactly on all 507 profiles to `n = 14` |
| The enabledness condition | **Not new.** It is Fernandes's **P-stability** (1998) — "if a point is in the domain, so is its whole block" — known for injective order-preserving partial maps |
| `sigma_blind`, uniform | **Published**, CFS Thm 1.1(i). Non-uniform: object in print (Pei–Zhou 2009), no cardinality found |
| The **extremal law** | **No published counterpart found.** That literature studies *rank* as a function of shape, never *order*. Not a first-ness claim — a recorded search |

Two corrections it forced: arXiv:1210.4775 is **Cicalò–Fernandes–Schneider**, not
Fernandes–Quinteiro; and Fernandes 1998 is *Semigroup Forum* **56**, not 58.

A second pass chased the three papers the review could not obtain. **Sun 2013 was
obtained in full** and overturns nothing — it fixes a uniform partition, so the
shape question cannot arise. **Pei 1994 was not obtained**, but its zbMATH review
was, and it shows the paper contains no cardinality at all. **Fernandes 1998 was
not obtained**, so the P-stability attribution is now graded as secondary
testimony rather than verified from primary. The condition is certainly in the
literature; that Fernandes 1998 is where it starts is someone else's word.

Worth more than any of the three: almost every paper here *fixes a uniform
partition by hypothesis*, which determines the shape and makes the extremal
question unaskable. The order for an arbitrary shape appears only with
Sarkar–Singh in 2021. The question is three years old in askable form — which
explains the absence of an answer without anyone needing to be first.

And one thing it gained. The proof needs only that the factor function is a sum
of exponentials. Sarkar–Singh's `|T(X,P)| = prod_i sum_j n_j^{n_i}` has factor
`sum_j n_j^k` — also a sum of exponentials. **So the same proof gives the extremal
law for the published total-map monoid**, an object anyone in that literature can
check, rather than only for an RPRM-internal count. Verify with
`python -I -B tools/fragility_literature.py`.

**Explicitly not picked**, with reasons given in Chapter 12: BSD (already
committed elsewhere, and on HOLD at an exact contradiction); the enabledness
census (classical, kept as calibration); liar/teacher + Hamming (the right next
*paper*, not the right next *research target* — the backlog itself says to credit
established coding theory); YM2 continuum (the finite covering is proved through
its stated order only); ternary grids and the graded scar cube (graded
*established, not a novelty* by the project's own record).

## Reproduction

```text
python -I -B tools/center_check.py       ternary-grid kernels, withheld-centre determination,
                                         graded cube kernels, weight-<=2 restriction
python -I -B tools/census.py             enabledness census, exposure depths, null control
python -I -B tools/fragility.py          closed form, brute-force confirmation,
                                         extremal search to n = 24, arity-2 hostile case
python -I -B tools/fragility_hostile.py  all five hostile cases, restricted operation
                                         classes, fixed-domain slices, search to n = 45
python -I -B tools/fragility_priority.py prior-art separation, enabledness price,
                                         two-monoid extremal comparison, subset sums
python -I -B tools/fragility_literature.py  the published reduction: Sarkar-Singh Thm 6.1
                                         against brute force, the adjoin-a-sink identity,
                                         and the exchange lemma on the published T(X,P)
python -I -B tools/fragility_audit_response.py  the three withdrawn claims, each retested:
                                         +1 inessential, tensor majorisation works,
                                         total maps covered, idempotents obstructed
python -I -B tools/fragility_exchange.py the exchange lemma, 5.7M exchanges to n = 40
python -I -B tools/fragility_critical.py targeted attack on the tightest family
python -I -B tools/fragility_limit.py    the cosh^2(1) asymptotic
python -I -B tools/fragility_proof.py 30 every step of the proof, exact integers
python -I -B tools/fragility_arity.py    the general-arity convex-order argument
python -I -B tools/fragility_mechanism.py why the proof fails for the classical monoid
```

Integers and `fractions.Fraction` only. Raw outputs are retained beside the
scripts so a reader can diff a fresh run against the recorded one.

## Corrections this pass made to its own inputs

1. The `rprm-alpha` memory fabric **is** reachable and populated (115 blobs,
   1,932 occurrences, 1,817 relations, **0 claims**). An earlier lane reported it
   unqueryable.
2. The fabric holds an August grading, missed by both other lanes, that the
   ternary-grid and graded-cube constructions are *"established
   finite-dimensional mathematics, not a novelty or physics claim."* Both lanes
   had recommended them as research targets. This pass rejected them on that
   authority.
3. The ternary-grid nullities, the withheld-centre determination table, the
   graded-cube kernels, the weight-`<=2` kernel dimension, and the 845-machine
   census family count were all independently recomputed and all confirmed
   exactly.
4. `MANIFESTO.md`'s Evidence Appendix states the runner requests **seventeen**
   suites. `docs/verification.md` and the actual run report **twenty**. The book
   is stale.
5. `experimental/shadow-lens/` holds a complete 181,447 = 7 x 161^2 scene census
   in seven probe fibers of 25,921, with 11 tests, and is **not** listed in the
   nine-pack index one directory above it. Same for
   `experimental/process-mechanics/`.
