# RPRM catch-up synthesis — 17 September 2026

An outside-in reading of RPRM by a synthesis lane, written as a friendly thesis
defence, plus one recommended non-BSD research target.

**Start here:** [`RPRM-understanding-thesis-defense.pdf`](RPRM-understanding-thesis-defense.pdf)
— 58 pages, thirteen numbered chapters, title page and contents. The markdown
source sits beside it.

This directory is a research record, not a publication of new mathematics.
Nothing here upgrades a finite test to a theorem, a written proof to a formal
proof, or a hash to a meaning. Every quantitative statement carries a domain and
an evidence grade.

## Contents

| File | What it is |
|---|---|
| [`RPRM-understanding-thesis-defense.pdf`](RPRM-understanding-thesis-defense.pdf) | The document. 58 pp. Combined first- and third-party account, core contract with fibers computed, lens maturity table, process-honesty chapter, steelman, criticisms, 51 defence questions, the pick, portable briefing appendix |
| `RPRM-understanding-thesis-defense.md` | Markdown source of the above |
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
| Extremal law: for fixed block count `m`, `argmax = (n-m+1, 1, ..., 1)`, `argmin =` balanced | **Conjecture.** Exhaustive search `2 <= n <= 24`, every `m`, every profile: **zero counterexamples** |
| Hostile case: does it survive arity 2? | Run. `n <= 12`, zero disagreements |
| Fragility is **not monotone** in block count | Observed. At `n = 6`, total collapse `(6)` has `F = 0.603`; balanced `(2,2,2)` has `F = 0.981` |
| Applied corollary: uniform binning is the most fragile `m`-block abstraction under unknown dynamics | Derived synthesis, uniform-prior model. At `n = 20, m = 10` the one-big-blob profile survives `1.7 x 10^7` times more often than balanced |

Priority against the wider literature is **OPEN** and must be settled before any
novelty claim. Reproduce with `python -I -B tools/fragility.py`.

**Explicitly not picked**, with reasons given in Chapter 12: BSD (already
committed elsewhere, and on HOLD at an exact contradiction); the enabledness
census (classical, kept as calibration); liar/teacher + Hamming (the right next
*paper*, not the right next *research target* — the backlog itself says to credit
established coding theory); YM2 continuum (the finite covering is proved through
its stated order only); ternary grids and the graded scar cube (graded
*established, not a novelty* by the project's own record).

## Reproduction

```text
python -I -B tools/center_check.py    ternary-grid kernels, withheld-centre determination,
                                      graded cube kernels, weight-<=2 restriction
python -I -B tools/census.py          enabledness census, exposure depths, null control
python -I -B tools/fragility.py       fragility closed form, brute-force confirmation,
                                      extremal search to n = 24, arity-2 hostile case
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
