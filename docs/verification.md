# Verification and reproduction

The release separates mathematical proofs, formal elaboration, finite
implementation checks and visual inspection. A test receipt is a report of
what was executed. Its hash binds bytes; its status does not make untested
claims true.

## Run from a fresh checkout

Use Python 3.10 or newer and Node.js 18 or newer. The Python code uses only
the standard library. No package installation is needed for the examples or
checks. The browser application has its own local JavaScript sources.

```sh
python -I -B verify.py
python -I -B examples/quickstart.py
python -I -B examples/proof_donut.py
```

The root runner starts every requested checker afresh, requires a successful
exit and a fresh PASS receipt, and records each result under `.artifacts/`.
A failed process cannot reuse the preceding PASS as its result. Each run has
a unique directory under `.artifacts/runs/`; the aggregate pointer is
`.artifacts/verification.json`. Logs are adjacent to receipts. A lock prevents
concurrent aggregate writers. An interrupted process leaves PENDING or a
partially completed run visible; after confirming it has stopped, remove a
leftover `.artifacts/verification.lock` before rerunning. Source hashes are
compared before and after the whole run. This detects persistent source edits
during checking; it is not a sandbox against a hostile process changing bytes
and restoring them between observations. Generated receipts and caches are
excluded from Git.

For formal checks install Lean 4.22.0 separately and supply its executable:

```sh
python -I -B verify.py --lean /path/to/lean
```

Without `--lean`, formal checking is explicitly `NOT_RUN`. The optional
`--python-only` flag requests a limited run without the Node atlas checks.
A successful limited run establishes only the scopes it actually executed.

## What is checked

| Suite | Independent comparison or obligation | Scope and important limits |
|---|---|---|
| `checks/core.py` | Direct finite relation enumeration, source quotient profiles, explicit atomic-state schedules and hostile controls | 8,257 aperture queries; 256 relation pairs and 4,096 triples; 2,637 deterministic, 20,613 nondeterministic and 8,715 stochastic quotient cases; bounded state schedules and one forced concurrent race |
| `checks/unification.py` | Source term/formula evaluator versus separately evaluated translated syntax; exact embedding and shared-interface fibers | 394 source models and 168,546 formula/assignment cases, 864 embedding-fiber cases, 4,088 interface words through length eight, six mathematical countermodels |
| `checks/futures.py` | Direct word enumeration versus pair-graph search and partition refinement | All 845 binary-observation partial machines in the listed size/alphabet families; 5,912 state pairs and 6,560 word executions; the written finite distinguishing bound justifies the oracle depth |
| `checks/proof_donut.py` | Complete finite certificate families and a separate core quotient implementation | 256 aperture, 256 induction, 512 descent and 4,096 quotient comparisons; named hostile and admission controls |
| `checks/fermat.py` | Integer arithmetic and auxiliary-prime certificate verification | 302 certificates, 1,998 exponents and the finite branches in the [written proof](fermat.md); the checker alone is not its all-exponent reduction |
| `checks/prime_frontier.py` | Square-frontier producer versus complete integer-divisor census; proof-donut aperture/path audits; Fermat auxiliary dependencies | The stages `5 -> 25 -> 625 -> 390625`, full classification and factor witnesses, 302 auxiliary pairs and deliberate certificate failures; the unbounded continuation uses the separate written factor theorem |
| `experimental/*/check.py` | Independent finite reference comparisons for all five packs | Exact scopes, costs and counterexamples are in the [experimental index](../experimental/README.md) and each pack; no empirical application claim |
| `checks/atlas/verify.js` | Exact contract checks and numerical conformance for the extracted mechanism and export code | See the emitted receipt and [atlas documentation](../atlas/README.md); finite numerical tests do not certify physical dynamics |
| `checks/atlas/view-checks.js` | Actual app code with finite DOM/Canvas stubs, import/export payloads and seam controls | Code-level checks only; browser, visual layout and accessibility behavior remain NOT_RUN |
| `checks/formal.py` | Fresh Lean elaboration and axiom inventory | The 20 declarations listed in [formal proof scope](formal-proofs.md), using an external trusted Lean toolchain |

Counts describe the implemented census families. They are not separate
theorems and should be recomputed when the source changes. Nonempty fibers,
unchanged observations, safe-looking plots and agreement between two pieces
of code are not substitutes for the stated correctness obligations.

## Hostile cases matter

The checks exercise loss of middle-witness identity, independent marginals
misread as a joint relation, quantification outside an encoded image, a
representation that preserves the present but changes later behavior, failed
versus successful partial execution, a stale candidate state, and malformed
or aliased carrier values. The finite-futures constructor rejects mutable
string subclasses in its action tables and copies admitted table data.

The donut checker does not read a core PASS flag. Its quotient result is
computed from the supplied tables, and the other core checker reaches its
own result. Agreement helps detect implementation errors. The proof of the
quotient criterion still rests on the written mathematical argument and,
where applicable, the explicitly listed formal declarations.

## Trust and coverage

Python, Node, the browser, Lean and their standard libraries are execution
dependencies. The tests are open for inspection and replacement. Runtime
input admission is a mathematical API contract, not a sandbox for executing
hostile programs or an operating-system security boundary.

Written proofs remain necessary for unbounded assertions and for bridges
between a finite model and an intended source. A verified finite table does
not establish that it enumerates every physical or theoretical possibility.
The [unification](unification.md), [proof-donut](proof-donut.md) and
[origins](origins.md) documents state those remaining premises explicitly.

## Reading and visual checks

The [handbook assessments](../agent-tests/README.md) preserve questions, keys,
exact tested versions and manually graded results from three fresh agent tasks.
They measure the tested questions and agents; they do not establish universal
comprehension. The conceptual chapter and experimental packs retain their
application assumptions locally so that jumping directly to a file does not
remove its scope.

The four paper figures show complete small examples and separating failures.
Rebuild them with `python -I -B tools/build_figures.py` (matplotlib), then build
the paper with `python -I -B tools/build_paper.py` (matplotlib, ReportLab, pypdf).
These optional packages are not required by the mathematical checks. The PDF
was rendered and its pages visually inspected; this is layout review, not a
mathematical proof. The Atlas has code-level DOM/Canvas stub checks, but actual
browser interaction, visual layout and accessibility review remain NOT_RUN.
