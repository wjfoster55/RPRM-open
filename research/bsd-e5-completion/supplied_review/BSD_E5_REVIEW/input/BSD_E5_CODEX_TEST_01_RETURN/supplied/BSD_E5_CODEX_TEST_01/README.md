# BSD E5 — Codex test 01

**One active assignment: `CODEX_START_HERE.md`.**

This bundle combines the recent arithmetic descent and analytic nonvanishing
construction for `y^2=x^3-25x`. It preserves their original source bytes and
receipts, then asks for independent verification and one bounded new result:
a rigorous interval of width at most 0.01 for the first central coefficient.

## What the test is trying to establish

1. **Arithmetic:** eight witnessed doubling classes are all the classes, giving
   rank one and the stated 2-primary result—not a total Sha computation.
2. **Analysis:** the central zero is exact, and the derivative is positive through
   a finite sum plus a bound on everything omitted—not a tiny-decimal guess.
3. **Representation:** cube coordinates and retained remainders support exactly
   their declared operations—not a ninth class or a generic compression theorem.
4. **New readout:** a rigorous numerical interval for the derivative, if achieved
   within the explicit finite budget. This does not establish the full BSD formula.

The interval coefficient is the number multiplying t in `L(E,1+t)` near zero.
The mathematical remainder is not assumed to be zero: its possible contribution
must be enclosed.

## Contents

- `CODEX_START_HERE.md`: sole active prompt.
- `TEST_PLAN.json`: fixed tasks and six focused controls.
- `inputs/descent/`: byte-preserved arithmetic note, code, and historical receipt.
- `inputs/analytic/`: byte-preserved analytic note, code, and historical receipt.
- `context/`: selected exact state and accepted C1/AD1 source records.
- `RPRM_CONTEXT.md`: integration boundaries and preserved meanings.
- `SOURCES.md`: actual source locators and which parts were checked for this handoff.
- `INTERVAL_CONSTRUCTION_HINT.md`: one mathematically explicit way to get a rigorous
  interval without treating ordinary high-precision evaluation as proof.
- `SOURCE_BINDINGS.json`: hashes and origin members of the 17 preserved source files.
- `tools/replay_inputs.py`: simple two-program replay; does not claim independent
  verification or automatic theorem validation.
- `preflight/`: assistant-side smoke run only, if present.
- `DELIVERY_INVENTORY.json`: final delivered files, excluding itself.

## First command

From this extracted directory, run:

    python -B tools/replay_inputs.py --output runs/codex_replay

Python 3.10+ and the standard library suffice for the replay. If mpmath happens
to be installed, the original analytic script also prints a noncertified decimal
illustration. That illustration is not used by the exact sign proof.

Read `CODEX_START_HERE.md` for the actual work after this smoke run. An earlier
PASS is not an independent rerun. Existing result fields are exposed development
expectations, not independent or hidden labels.

## Ownership and limits

This is a BSD-only request, in an isolated experiment directory. It does not
reassign or stop Yang–Mills, fluids, or SAT work. Closed Lind–Reichardt and AD
pilot tasks stay closed. No paper drafting, publication, general BSD proof,
performance superiority, or other-lane dispatch is requested.

The original notes' theorem claims remain claims to independently inspect.
The shipped launcher validates the finite replay and binding, not all proofs.
