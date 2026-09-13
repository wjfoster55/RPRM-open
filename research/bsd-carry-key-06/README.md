# BSD carry/key experiment 06

William proposed that the ordered digits in the coefficient/modulus pair
426 and 625 might supply an operational key, related to fiving and the
earlier pi construction. We recovered the relevant exact operations,
tested explicit candidates, and independently refined the coefficient.

His later corrections added the compression `2301+3125=5426 -> 566`
and specified that 566 is an intermediate state awaiting a carry or
shadow handoff. [COLUMN_HANDOFF.md](COLUMN_HANDOFF.md) implements that
bounded continuation, including the information needed to keep operating.
The candidate shadow path begins `566 -> 687 -> 808`; a complete
10,000-word audit verifies the retained carry state. The intended BSD
operation and terminal readiness criterion remain open.

The fresh result is

\[
b_2\in2301+3125\mathbf Z_5,
\qquad b_2=1+2\cdot5^2+3\cdot5^3+3\cdot5^4+O(5^5).
\]

The convention is unchanged from experiment 05: minimal E34, connected
real period, trivial Teichmuller branch, and cyclotomic generator with
character 6. A classical measure sum with proved error reproduces the
overconvergent result to all five reported digits. No saved PASS is used
as a computation input.

The exact finite key `reverse_decimal(426)+1=625` survives as a scoped
identity. It also arises from a complete seven-state role chart recovered
from the pi-style midpoint, gap and corner relations. Its extension as
the same reversal rule at every precision is refuted by the complete
five-lift fiber; no possible next lift satisfies it.

The coefficient's multiplication operation supplies a stronger transferable
fact: it retains the lower two base-five digits, while five repetitions
close one coarse level and retain a nonzero finer carry. The 4/6 cue also
gives a lawful change of logarithmic coordinate from 6 to -4. Neither
operation supplies an independently determined BSD comparison scalar.

Read [RETURN_TO_WILLIAM.md](RETURN_TO_WILLIAM.md) for the short explanation,
[OPERATIONAL_PROOF.md](OPERATIONAL_PROOF.md) for domains and derivations,
and [BSD_REBRIEF.md](BSD_REBRIEF.md) for the claim boundaries.

Replay with Python 3.10+ and PARI/GP 2.17.4:

```powershell
python -I -B C:/github/RPRM-open/research/bsd-carry-key-06/work/run_probe.py --output C:/github/RPRM-open/research/bsd-carry-key-06/runs/my_fresh_replay
```

The output directory must be new. The default runtime is the executable
already supplied in sibling experiment 05. When unpacking elsewhere,
pass `--gp /absolute/path/to/gp`. The source archive and license for that
runtime remain in `bsd-coefficient-05/runtime/`; no installation or changes
to another lane are performed by this runner.

Fresh evidence is in `runs/fresh_validation/`: source snapshots, all GP
and translator logs, `evidence/operations.json`, and `RUN.json`.
The copied operational-number translator passed its 114 existing checks;
its scout suggestions remain hypotheses. The finite audit enumerates all
625 multiplication states, all seven proposed chart states, all five next
lifts, and all 1,250 states of the repaired integer display operation.

Historical material is attributed in `dependencies/SOURCES.json` and the
bounded fabric packet under `evidence/`. The dated fabric packet is not a
promise that every historical source locator still exists on disk. Current
local recovery and Lexicon files were read directly. No authority memory,
other research lane, previous experiment or paper was modified.
