# BSD E5 Codex test 01 — reviewer acceptance

**12 September 2026. Verdict: ACCEPT at the stated one-curve scope.**
No blocking mathematical or reproducibility defect was found. This is a
review of the attached E5 return, not the unrelated automatically surfaced
Lind-Reichardt review004 text. Closed lanes and the AD pilot remain closed.

## Accepted Codex result

For E/Q: y^2=x^3-25x,

    556371/250000 < L'(E,1) < 1114529/500000,
    equivalently 2.225484 < L'(E,1) < 2.229058.

Width =1787/500000=0.003574<0.01. The first prescribed M=40,K=32 attempt
succeeded; later refinements were not used. Only six Euler coefficients
through 40 are nonzero; computing the six special-function terms required
832 midpoint quadrature panels in the submitted implementation.

This strengthens the prior sign proof to a two-sided enclosure. The
functional-equation sign gives L(E,1)=0 exactly, so the positive derivative
establishes a simple zero. The independent descent gives rank one and
Sha[2^n]=0 for all n>=1. Combining the two sides establishes BSD's rank
comparison for this classical example. It does not prove general BSD, the
full leading-coefficient formula, odd-primary Sha triviality, or that P is
an integral generator.

## Fresh execution and preservation

- All 108 listed delivery entries match hashes and sizes; the 109th file
  is the inventory itself, explicitly not self-hashed.
- All 35 original archive members match the previously delivered source ZIP.
- Fresh `work/run_all.py` execution completed all five stages with exit 0:
  source replay, arithmetic, model binding, analytic interval, peer ledger.
- Every nonmetadata field of the fresh arithmetic, model-binding, analytic,
  and interval results matches the submitted results. The exact excluded
  environment/timestamp/path fields are listed in the comparison receipt.
- All six requested controls executed with their stated outcomes. This
  review did not launch a new broad mutation campaign.
- Submitted and extracted input bytes were unchanged by review.

Environment: Python 3.13.5 on Linux. Sage, PARI/cypari2, and FLINT were not
available. SymPy and mpmath were present but were NOT used by the fresh
independent review scripts. No proof assistant or different global-L backend
was run. The submitted multiworker chronology remains a report from its
SESSION_SCOPE; the mathematical conclusion does not rely on the number of
workers or their claimed isolation.

## Independently implemented checks

`tools/independent_review.py` imports no submitted implementations. It
performs direct covering residue enumeration, checks rational witness
squareclasses, and verifies the five-bit bijection and 1024 group-law pairs.
It computes prime point counts and all Euler coefficients through 40 anew.

Its independent E1 enclosure uses a different pi identity, positive
exponential-series reciprocals, decimal-grid directed rounding, and
three-point Simpson panels with a conservatively derived fourth-derivative
error bound. Every independent E1 enclosure is contained in the matching
submitted interval. The final independent enclosure is

    2.225705022 < L'(E,1) < 2.229026982,

entirely inside the accepted Codex bounds. The shared Mellin and all-n
coefficient-bound theorems remain explicit inputs; see INDEPENDENT_METHOD.md.
This is not a wholly independent proof of the analytic continuation.

`tools/review_replay.py` checks every recorded 112 selected tower cases
and six rational-search readbacks, reconstructing both the original point
and all 304 trace steps using separately written group arithmetic.

## Error budget

The exact rational ledger reassembles identically to the delivered width.
Approximate width contributions (display only) are:

- all omitted Euler terms: 0.003318916277056738;
- retained-integral quadrature: 0.000254620282490465;
- readable-endpoint outward enlargement: 0.000000463440450967;
- integral cutoff, constant enclosures, and exponential/rounding contributions:
  positive and retained, but much smaller;
- exact signed rational accumulation: no additional rounding.

The first term is about 92.86% of the width. Higher decimal arithmetic alone
would not materially remove that deliberately conservative tail allowance.
Negative Euler weights reverse interval endpoints; no favorable tail-sign
assumption or unexplained numerical convergence enters the certificate.

## Additional arithmetic deduction in this review

The checked #E(F_3)=4, together with good reduction at 3 and the standard
rational-torsion injection theorem, proves that the four displayed
2-torsion points are ALL rational torsion. See TORSION_COROLLARY.md.
This was not imported as a Codex claim or a database label.

## What the RPRM-related checks establish

The cube is an explicit recoding of independently justified arithmetic
classes; it does not prove their local admissibility by its shape. The
lost-remainder control demonstrates two different finer classes merged by
the same coarse label, not an empty class. The no-tail control correctly
leaves the finite head available while declining an infinite-sum claim.
Coherent transport passes; stale readout transport fails. None establishes
an unrestricted Prestige construction or measured superiority over ordinary
correct arithmetic and caching.

## Next arithmetic boundary

There is no need to repair this experiment or chase decimal digits for their
own sake. Remaining E5 questions include odd-index saturation of P and
arithmetic ingredients of the full leading-coefficient formula. The wider
unfinished descent direction is image Sel_4 -> Sel_2 on a curve with
nontrivial obstruction. No new worker dispatch is included in this review.

## Reproduction

Unzip the review package and run from its root:

    python -B input/BSD_E5_CODEX_TEST_01_RETURN/work/run_all.py --output fresh_replay_2
    python -B tools/independent_review.py --root input/BSD_E5_CODEX_TEST_01_RETURN --out new_evidence
    python -B tools/review_replay.py --root input/BSD_E5_CODEX_TEST_01_RETURN --fresh fresh_replay_2 --output new_evidence/replay.json

Use an output path that does not already exist for the supplied runner.
The optional --original path for independent_review.py compares a separate
copy of the original source ZIP, if available; it is not needed for the
mathematics or the present delivery integrity check.
