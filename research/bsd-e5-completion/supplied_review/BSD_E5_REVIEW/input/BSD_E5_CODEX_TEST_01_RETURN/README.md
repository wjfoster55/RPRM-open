# BSD E5 test 01

This is one bounded experiment for the rational curve `y^2 = x^3 - 25x`.
Read `RETURN_TO_WILLIAM.md` for the mathematical result, `BSD_REBRIEF.md` for
the short handoff, and `CLAIM_LEDGER.json` for evidence and limits.

Python 3.10 or newer and its standard library suffice. From this directory:

```text
python -B work/verify_delivery.py
python -B work/run_all.py --output runs/my_fresh_run
```

Choose a new, nonexistent output directory for every run. The first command
checks delivered bytes; the second executes the supplied programs and the
independent finite checkers. The runner does not re-prove the cited standard
theorems or turn finite observations into universal theorems.

The original archive is not required to rerun the mathematics. If it is
available, every original member can additionally be compared:

```text
python -B work/check_original_bytes.py /path/to/BSD_E5_CODEX_TEST_01.zip --output runs/original_bytes.json
```

`supplied/BSD_E5_CODEX_TEST_01/` preserves every original member, including
historical receipts. `evidence/codex_replay/` is a fresh execution of the supplied
implementations. Other evidence and `work/` hold the independently written
checks. Archived PASS fields are used only by the supplied replay comparison;
they are not inputs to the independent checkers.

The new interval has a declared finite refinement budget in `work/INTERVAL_BUDGET.json`
and a term-by-term error ledger in `DERIVATIVE_INTERVAL.json`.
`ARITHMETIC_PROOF.md`, `ANALYTIC_THEOREMS.md`, and `INTERVAL_DERIVATION.md`
give the proofs and source checks. `INDEPENDENT_CHECKS.json` and `CONTROLS.json`
account for every task and control from the supplied `TEST_PLAN.json`.

All task writes are confined to this experiment and its final sibling ZIP.
No other research lane, closed experiment, paper, repository routing,
commit, or publication is part of this work.
