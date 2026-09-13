# BSD rank-two experiment 01

Self-contained source and proof notes for E34: y²=x³−1156x. Start with
[RETURN_TO_WILLIAM.md](RETURN_TO_WILLIAM.md) for the explanation and
[BSD_REBRIEF.md](BSD_REBRIEF.md) for concise claims and open obligations.
The follow-up [SHA_ORDER_CRITERION.md](SHA_ORDER_CRITERION.md) explains
exactly what would establish #Sha=1 without assuming BSD.

This continues the user-authorized general-argument investigation after
the E5 test and completion. It does not modify either earlier delivery.
Document instructions were treated as attributed inputs; the current
user request determined the scope. No paper, deployment, automation,
or unrelated research lane was started.

## Replay

Python 3.11 or later, standard library only; the recorded run used
Python 3.14.5 on Windows. From this directory:

```powershell
python -I -B work/run_all.py --output runs/my_fresh_run
```

Use a new directory name. The runner refuses an existing destination,
copies only `work/*.py` and `work/BUDGET.json`, and executes seven
stages in order. It does not copy any existing receipt. It retains
stdout, stderr, exit codes, exact rational evidence, input hashes and
dependency checks. A failed stage or consistency check remains recorded.
It does not prove the cited mathematical theorems or certify the
written proofs automatically.

The delivered fresh run is `runs/final_validation/RUN.json`; all seven
stages completed in about 22 seconds total on the author's machine.
Individual development receipts in `evidence/` remain alongside it.
Run through the wrapper when preserving existing receipts matters;
some individual development scripts write to fixed output locations.

## File map

| Topic | Written explanation | Executable |
|---|---|---|
| Complete descent, rank, torsion, two-primary Sha | `ARITHMETIC_PROOF.md` | `work/arithmetic.py` |
| Full integral basis, all finite indices | `GENERATOR_PROOF.md` | `work/generator.py` |
| Minimal model, bad primes, conductor, coefficients | `LOCAL_ANALYTIC_INPUTS.md` | `work/local_inputs.py` |
| Infinite analytic coefficient interval and exact rank | `ANALYTIC_PROOF.md` | `work/interval.py`, frozen `work/BUDGET.json` |
| Independent formulas, coefficients and interval ledger audit | `INTERVAL_AUDIT.md` | `work/interval_audit.py` |
| Midpoint, directed half-step, reflection and information retention | `MIDPOINT_BRIDGE.md`, `USER_ITERATION.md` | `work/midpoint.py` |
| Period, regulator and scoped BSD quotient | `FACTOR_COMPARISON.md` | `work/factor_frontier.py` |
| Actual theorem failures and remaining full-BSD obligations | `FULL_BSD_FRONTIER.md` | Primary-source applicability review |
| Exact remaining arithmetic criterion for #Sha=1 | `SHA_ORDER_CRITERION.md` | Written exact-sequence deduction; quantified input OPEN |
| Full fresh execution | This file | `work/run_all.py` |

Each stage has a JSON receipt and log under the delivered run's
`evidence/` directory. `CLAIM_LEDGER.json` records the final claim status.
`MANIFEST.json` binds delivered bytes, excluding itself; it is not a
mathematical certificate of those bytes.

## Read the staged conclusions together

The first arithmetic receipt intentionally leaves the basis index as
finite odd and saturation as unperformed. The later generator proof
closes that separate obligation with index 1. Similarly, the generator
receipt does not claim the analytic rank; that is established in the
analytic proof. These are scoped stage results, not conflicting final
answers. The rebrief and claim ledger combine them explicitly.

The factors produce an interval around 1 without asserting integrality
or equality to #Sha. Total Sha finiteness/order and full BSD remain
NOT_ESTABLISHED. General BSD remains OPEN. The rank-two exact lower
zeros use an established low-analytic-rank theorem; we have not replaced
that theorem by a new midpoint argument.

The finite checks include hostile cases; the written arguments supply
their all-prime and all-index coverage. Formal verification was not run.
The independent interval audit does not claim a second evaluation of
every Simpson panel. Primary-source links and theorem conditions are
given in the corresponding notes.
