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
python -I -B examples/fixed_gap.py --n 2 --s 1 --d 1
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

The default runner registers 20 executable jobs: 13 Python jobs and seven Node
jobs. Supplying `--lean` adds the formal job, giving 21. These are registration
counts; the fresh aggregate receipt records what a particular execution ran
and whether it passed.

Without `--lean`, formal checking is explicitly `NOT_RUN`, including its entry
in `checks`. The optional `--python-only` flag omits all seven Node jobs:
`atlas`, `atlas_view`, `rule_lab_model`, `rule_lab_presentation`,
`lens_lab_model`, `music_lens_model` and `music_lens_audio`. Each omitted
job receives its own `NOT_RUN` entry and reason. The two-path Python job still
runs, as does the fixed-gap checker. This gives 13 requested jobs, or 14 if
`--lean` is also supplied.

The aggregate `requested_checks` list identifies the requested execution scope;
PASS requires every listed job to pass. The top-level `node` status covers all
seven Node jobs, and `node_suites` names them. The compatibility field `atlas`
continues to report the Atlas model job alone; it cannot certify `atlas_view`
or any Rule Lab, Lens Lab or Music Lens job. Formal status remains separate.
Missing Node fails a requested full run before any child suite starts; it never silently becomes
a Python-only success. A successful limited run establishes only the scopes
it actually executed.

## What is checked

| Suite | Independent comparison or obligation | Scope and important limits |
|---|---|---|
| `checks/core.py` | Direct finite relation enumeration, source quotient profiles, explicit atomic-state schedules and hostile controls | 8,257 aperture queries; 256 relation pairs and 4,096 triples; 2,637 deterministic, 20,613 nondeterministic and 8,715 stochastic quotient cases; bounded state schedules and one forced concurrent race |
| `checks/unification.py` | Source term/formula evaluator versus separately evaluated translated syntax; exact embedding and shared-interface fibers | 394 source models and 168,546 formula/assignment cases, 864 embedding-fiber cases, 4,088 interface words through length eight, six mathematical countermodels |
| `checks/futures.py` | Direct word enumeration versus pair-graph search and partition refinement | All 845 binary-observation partial machines in the listed size/alphabet families; 5,912 state pairs and 6,560 word executions; the written finite distinguishing bound justifies the oracle depth |
| `checks/proof_donut.py` | Complete finite certificate families and a separate core quotient implementation | 256 aperture, 256 induction, 512 descent and 4,096 quotient comparisons; named hostile and admission controls |
| `checks/fermat.py` | Integer arithmetic and auxiliary-prime certificate verification | 302 certificates, 1,998 exponents and the finite branches in the [written proof](fermat.md); the checker alone is not its all-exponent reduction |
| `checks/prime_frontier.py` | Square-frontier producer versus complete integer-divisor census; proof-donut aperture/path audits; Fermat auxiliary dependencies | The stages `5 -> 25 -> 625 -> 390625`, full classification and factor witnesses, 302 auxiliary pairs and deliberate certificate failures; the unbounded continuation uses the separate written factor theorem |
| `experimental/*/check.py` | Independent finite reference comparisons for the five original packs | Exact scopes, costs and counterexamples are in the [experimental index](../experimental/README.md) and each pack; no empirical application claim |
| `experimental/two-path-lab/test_model.py` (`experimental_two_path`) | Frozen exact probabilities and independent full-matrix contractions versus the declared rational model and coherence receiver | 31 finite fixture tests, including 48 marker/phase/output entries, nine three-output probabilities, channel and conditional-marginal controls; see the [two-path contract](../experimental/two-path-lab/README.md). No physical experiment or arbitrary slit geometry is tested. |
| `checks/atlas/verify.js` | Exact contract checks and numerical conformance for the extracted mechanism and export code | See the emitted receipt and [atlas documentation](../atlas/README.md); finite numerical tests do not certify physical dynamics |
| `checks/atlas/view-checks.js` | Actual app code with finite DOM/Canvas stubs, import/export payloads and seam controls | Code-level checks only; browser, visual layout and accessibility behavior remain NOT_RUN |
| `experimental/rule-lab/model.test.cjs` (`rule_lab_model`) | Independent string-table rule oracle, finite seed/boundary evolution, transform/readout fibers and trial-division sieve comparisons | The [Rule Lab](../experimental/rule-lab/README.md) states the exact finite model and hostile cases; no unbounded prime classifier or physical model is established. |
| `experimental/rule-lab/presentation.test.cjs` (`rule_lab_presentation`) | Pure seed, block-summary, aperture and camera calculations, plus static JavaScript/HTML wiring checks | Separate presentation-helper coverage; does not execute the actual interface. Browser rendering, interactions, downloads, storage and accessibility remain NOT_RUN_UI. |
| `experimental/lens-lab/verify.cjs` (`lens_lab_model`) | Fresh execution of the adjacent `model.test.js` suite with independent coordinate expectations and canonical renderer values | 16 pure model tests: 648,000 locked transitions for one nonuniform fixture, 3,600 duplicate/wrap signature checks, 5,400 unlocked edits, projection/admission controls and browser/CommonJS export compatibility. The [Lens Lab contract](../experimental/lens-lab/README.md) gives the finite boundary; this does not enumerate all `360^5` tuples or execute the browser interface. |
| `experimental/music-lens/verify.cjs` (`music_lens_model`) | Fresh adjacent model replay with independent absolute-pitch admission and canonical event/tuning expectations | 1,200 states, 734,400 candidate pitch-target checks and 895,298 assertions cover three representative phrases at all 25 roots and 16 phases, inverse/readout fixtures and admission controls. The [Music Lens contract](../experimental/music-lens/README.md) gives the finite boundary; the full source-state product is not enumerated. |
| `experimental/music-lens/verify-audio.cjs` (`music_lens_audio`) | Fresh adjacent transport tests with fake clocks and an audio API fixture | Nine deterministic tests cover admission, visual fallback, loop timing, edit/mute cancellation, pending activation races, permission failure, visibility stopping and stalled scheduling. Browser acoustic output, subjective listening and UI behavior are not tested by this suite. |
| `checks/formal.py` | Fresh Lean elaboration and axiom inventory | The 20 declarations listed in [formal proof scope](formal-proofs.md), using an external trusted Lean toolchain |

Counts describe the implemented census families. They are not separate
theorems and should be recomputed when the source changes. Nonempty fibers,
unchanged observations, safe-looking plots and agreement between two pieces
of code are not substitutes for the stated correctness obligations.

## Hostile cases matter

The [fixed-gap checker](../checks/fixed_gap.py) independently enumerates
every integer in the derived brackets of 252 supplied apertures, compares
the normalized residual exactly, checks the bisection receipts and rejects
invalid types and domains. It retains the nonempty n=2 case and empty
fifth-power example. These finite implementation checks accompany the
written all-height decision proof; they do not establish uniform emptiness
over every n>2 and every gap pair.

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
exact tested versions and manually graded results for their recorded tasks.
They measure the tested questions and agents; they do not establish universal
comprehension. The conceptual chapter and experimental packs retain their
application assumptions locally so that jumping directly to a file does not
remove its scope.

The complete book uses six explanatory figures, including two plots of
supplied two-path probabilities. The [book build](../tools/typesetting/README.md)
documents its Pandoc, Tectonic, Python and font dependencies. Run
`python -I -B tools/build_paper.py` to produce a fresh source-bound output
under `.artifacts/paper/`; the command leaves the distributed PDF unchanged.
Its receipt records the exact selected inputs and generated PDF. Typesetting
dependencies are separate from the Python and Node mathematical checks.

The final PDF's source binding, rendered pages and page-review record must
refer to the same selected version. A layout review is not a mathematical
proof, and a passing model test does not certify a PDF. The Atlas has
code-level DOM/Canvas stub checks; Rule Lab has pure presentation-helper and
static wiring checks. Actual browser interaction, visual layout and
accessibility review remain NOT_RUN for the Atlas and NOT_RUN_UI for Rule Lab.

Lens Lab's aggregate job runs only its 16 pure model tests. Its wrapper
requires a completed test summary with all 16 passing and none failed,
cancelled, skipped or marked TODO before publishing PASS. Manual browser
checks are separate: exercise presets, selection, locked/unlocked edits
including A, pointer drag, keyboard ranges, independent lens controls,
collapse and restore, Reset, and narrow/wide layouts. These checks and any
recorded visual review do not become automatic UI coverage in the aggregate
receipt.

Music Lens has separate aggregate jobs for its model and audio transport.
The model wrapper requires a completed JSON summary with PASS and the exact
declared state, pitch-target and assertion counts. The audio wrapper requires
a completed TAP summary with all nine tests passing and none failed,
cancelled, skipped or marked TODO. Both start fresh processes, replace any
prior receipt with PENDING, and compare tested-source hashes before and after.
The [dated browser review](../experimental/music-lens/REVIEW.md) covers the
tested interactions and desktop/390-pixel layouts. Those observations remain
separate from the aggregate's `NOT_RUN_UI` and acoustic `NOT_RUN` fields;
they do not establish recorded acoustic output or subjective listening quality.
