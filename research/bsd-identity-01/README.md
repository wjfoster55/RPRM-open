# BSD identity 01

This is a new, isolated continuation of the E34 experiment, authorized by
the user's request to pursue the exact analytic BSD identity and its
remaining arithmetic factors. The identity is still **NOT_ESTABLISHED**.
General BSD remains **OPEN**. No earlier delivery or other lane was edited.

Start with [RETURN_TO_WILLIAM.md](RETURN_TO_WILLIAM.md) for the explanation
and [REBRIEF.md](REBRIEF.md) for the concise result.

## Run from source

Python 3.11 or newer, standard library only. The delivered run used
Python 3.14.5. From this directory:

```powershell
python -I -B work/run_identity.py --output runs/my_fresh_run
```

Choose a new destination. The wrapper refuses an existing directory,
copies source only, executes all seven preceding input stages, then
runs the three new programs. It records logs, exit codes, source and
receipt hashes, and the actual open proof obligations. The odd-prime
checker is expected to report OPEN: its missing trace is not computed.
That is a mathematical stopping point, not a process error to conceal.

The final delivered run is `runs/return_validation/RUN.json`. It
completed in approximately 23 seconds on this machine. Fresh input
evidence is nested under `runs/return_validation/inputs/evidence/`,
and new evidence under `runs/return_validation/evidence/`. Written
theorem arguments remain required; execution does not formally verify
the cited theorems or prove the missing comparison.

## What is included

| Readout | Note | Executable or evidence |
|---|---|---|
| Authorized scope and exact target | `CONTRACT.md` | Fixed E34, no assumption of BSD |
| Actual complex identity theorem bridges | `EXACT_IDENTITY_THEOREMS.md` | Six-search bounded primary review, with hypotheses |
| Height series, regulator increments and a sufficient matching certificate | `EXPLICIT_IDENTITY_TARGET.md` | `work/height_series.py` |
| Exactness, coarse zero, retained carry, denominator gate | `EXACTNESS_AND_LEVELS.md` | `work/identity_gate.py` |
| User's latest correction in their words | `USER_ITERATION.md` | Attributed input; interpretation distinguished |
| One odd-prime attempt, p=5 | `ODD_PRIME_ATTEMPT.md` | `work/odd_prime.py`, actual trace null |
| Final status by claim | `CLAIM_LEDGER.json`, `REBRIEF.md` | Open premises remain explicit |
| Independent reviews and controls | `AUDIT.md` | Fresh run logs and exact receipts |
| Unchanged input source and proof snapshot | `input_source/SNAPSHOT_NOTICE.md` | Original rank-two sources and budget |

The input snapshot contains no old saved receipts. The development
receipts under `evidence/` are also included. `identity_gate.json` is
the initial gate run before adding the explicit congruence hierarchy;
its exact source is `evidence/identity_gate_initial_source.py`.
`identity_gate_final.json` and the final aggregate run use the current
source. No intermediate version is silently presented as the final one.

## Claim ceiling

We proved conditional completion criteria and explicit convergent
reformulations, checked the actual theorem conditions, and admitted
one concrete trace calculation. We did not compute that trace, prove
the quotient's rationality or denominator bound, construct an all-stage
analytic–arithmetic matching rule, establish new odd-primary Sha
vanishing, or prove the exact BSD identity.

In particular, the maximum denominator 10774 is a property of an
interval-isolation criterion. It is not a proved denominator bound on
the actual quotient. Five possible trace residues form the complete
fiber of a known coarse residue; the actual finer residue is unknown.

The work is a reproducible research continuation, not a paper or a
claimed general solution. `MANIFEST.json` checks delivered byte integrity
only; hashes do not prove mathematical contents.
