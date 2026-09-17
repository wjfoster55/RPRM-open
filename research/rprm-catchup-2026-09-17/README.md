# RPRM catch-up synthesis — 17 September 2026

An outside-in reading of RPRM by a synthesis lane, written as a friendly thesis
defence, plus one recommended non-BSD research target.

**Start here:** [`RPRM-understanding-thesis-defense.pdf`](RPRM-understanding-thesis-defense.pdf)
— 65 pages, thirteen numbered chapters plus appendices. The markdown source sits
beside it.

**Then read Appendix E**, which records what happened when the hostile cases the
document declared were actually run overnight. Two of them bit, one of them
against the document's own headline claim, and the priority search produced a
better result than either outcome it was hedging against. The research record is
[`FRAGILITY.md`](FRAGILITY.md).

This directory is a research record, not a publication of new mathematics.
Nothing here upgrades a finite test to a theorem, a written proof to a formal
proof, or a hash to a meaning. Every quantitative statement carries a domain and
an evidence grade.

## Contents

| File | What it is |
|---|---|
| [`RPRM-understanding-thesis-defense.pdf`](RPRM-understanding-thesis-defense.pdf) | The document. 65 pp. Combined first- and third-party account, core contract with fibers computed, lens maturity table, process-honesty chapter, steelman, criticisms, 51 defence questions, the pick, portable briefing appendix, and the overnight addendum |
| `RPRM-understanding-thesis-defense.md` | Markdown source of the above |
| [`FRAGILITY.md`](FRAGILITY.md) | The research record for the pick: typed claim, five hostile cases, prior-art separation, dispositions, and what is still owed |
| [`05-portable-briefing-for-other-gpts.md`](05-portable-briefing-for-other-gpts.md) | Self-contained briefing to paste into any other model. No prior context assumed |
| [`WILLIAM-WORKING-STYLE.md`](WILLIAM-WORKING-STYLE.md) | Sanitized operating page: standing corrections and the three-role abduction/verification split |
| [`01-first-party-rprm.md`](01-first-party-rprm.md) | Ingest lane 1 — the project's self-account, read from the repository spine |
| [`03-independent-math-reading.md`](03-independent-math-reading.md) | Ingest lane 3 — an independent mathematical reading, run cold, `verify.py` executed |
| [`04-coverage-gaps.md`](04-coverage-gaps.md) | What was searched for, found, and still missing |
| [`tools/`](tools/) | Three exact-arithmetic verification scripts and their raw outputs |

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
| Extremal law: for fixed block count `m`, `argmax = (n-m+1, 1, ..., 1)`, `argmin =` balanced | **Conjecture.** Exhaustive search `2 <= n <= 45`, every `m`, every profile — **903 cells, zero counterexamples** |
| **Exchange lemma** — moving one element from a smaller block to a larger one strictly increases survival. Implies the extremal law, and is local rather than global | **Conjecture, and the open problem worth solving.** **5,686,463** exchanges to `n = 40`, zero non-increases, plus a targeted attack on the tightest family with spectator blocks up to 100,000. The Karamata step `S'_k >= S_k` is proved |
| `sigma_E(j+1,j-1)/sigma_E(j,j) -> cosh^2(1) = 2.381097845...` | **ONE(constant).** Written derivation, then verified in exact arithmetic to `j = 20,000`. Splitting a balanced pair apart multiplies survival by a fixed factor that does not wash out |
| Hostile cases: arity 2, arity 3, total-only, idempotent-only | All run. Survived: `n <= 12`, `n <= 10`, `n <= 18`, `n <= 7`. Zero failures |
| Hostile case: **non-uniform priors** | **Bit.** The `argmin` half fails under injective-partial and permutation priors. The `argmax` half survives every class but one. Six counterexamples retained |
| Fragility is **not monotone** in block count | Observed. At `n = 6`, total collapse `(6)` has `F = 0.603`; balanced `(2,2,2)` has `F = 0.981` |
| Admissible domain sizes of a surviving operation = **subset sums of the profile** | Written proof. `(6)` admits only `{0,6}`; `(3,2,1)` admits all of `0..6` |
| Applied corollary: uniform binning is the most fragile `m`-block abstraction | **Restricted.** Holds under partial, total and idempotent priors — at `n = 20, m = 10` the blob survives `1.7 x 10^7` times more often. **Reverses under bijective priors** |

### Priority, and the result it produced

The classical partition-preserving transformation monoid is Pei's, enumerated in
arXiv:2006.04242 and — for the partial, uniform case — arXiv:1210.4775 with order
`(m(n+1)^n - m + 1)^m`. **Its condition is successor agreement only, with no
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
the extremal profiles **invert**, first at `n = 11, m = 9`. *Finite test,
complete enumeration in the stated range. Not a theorem; the general case is
OPEN both ways.*

`sigma_blind` priority: **ONE(citation)**. `sigma_E` priority: **NONE found after
a stated single-pass search** — an admission of what was searched, not a novelty
claim. A real review is still owed.

Reproduce with `python -I -B tools/fragility.py`,
`tools/fragility_hostile.py`, `tools/fragility_priority.py`.

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
python -I -B tools/fragility_exchange.py the exchange lemma, 5.7M exchanges to n = 40
python -I -B tools/fragility_critical.py targeted attack on the tightest family
python -I -B tools/fragility_limit.py    the cosh^2(1) asymptotic
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
