# RCF01-R1 independent review — composition verified; narrow guards remain

**11 September 2026 · Review of the uploaded `core-recovery-r1.zip`.**

## Verdict

Accept the recovery/export repair and the demonstrated composition-reopening result. The actual portable implementation is now present and replays. Do not yet treat all output-family claims, the generic-map entry point, or the portable runner's aggregate PASS as a finished guardrail.

This review found one output-family defect, one generic-map interface/metadata defect family, and one aggregate-runner defect family. None refutes the cube restriction theorem or the successful composed-product calculation. Complete one bounded repair, not another recovery campaign.

## Source selected and preservation

The outer submission includes both `dist` and `dist_02`. This review selected the explicitly corrected `dist_02/RCF01-portable-r1.zip`, SHA-256:

`53d1e8761aeca98d26cb3732150af7a31ed109aad4e1c9187b3e4dc192315cea`.

It contains 68 regular files. All **67 manifest-listed files** match their stated byte lengths and SHA-256 values; `MANIFEST.json` is the remaining file. The outer and selected inner ZIP CRC checks pass. Extraction rejected unsafe paths and symlinks.

The original recovery archive and original concept-register bytes are unchanged. Nine of the ten files in the prior research-only ZIP are byte-identical; its README has one added relative pointer to the R1 successor. That is an explicit navigation addition, not a loss of historical meaning. Do not say literally every old research file is unchanged.

The original 22-case implementation/protocol, original FAIL and PASS receipts, R1's 26-case implementation/protocol, its development FAIL and corrected PASS receipts, and the imported `rprm.core` source are now included. Historical donor logs are included, but the donor source trees are not: **the original donor experiments were not independently replayed in this review**.

Evidence: `results/input_inventory.json`, `results/preservation_checks.json`, `results/README_export_change.diff`, and `results/independent_review.json`.

## Actual unmodified replay

Extracted the selected inner ZIP to a fresh local tree. Used packaged dependencies with `PYTHONPATH` unset and fresh output/work directories outside that source tree. Runtime: Python 3.13.5 on Linux, versus the producer's reported Python 3.14.5 on Windows. No installation, remote repository action, or original source modification.

Command:

```text
python -B <fresh-extract>/run_portable.py --output-dir <fresh-review-output>
```

| Job | Observed result |
|---|---|
| Current envelope | PASS, 26/26 named cases |
| Omit required case | exit 2, FAIL; missing PE26 |
| Duplicate required case | exit 2, FAIL; duplicate IDs |
| Substitute unexpected case | exit 2, FAIL; UNDECLARED replacing PE26 |
| Reorder cases | exit 0, PASS, 26 cases |
| Concept ID check | exit 0, 13 IDs |
| Export/record validation | exit 0, PASS |
| Inherited starter | exit 0, PASS, 12 cases |

The entire invocation returned exit 0. The individual child receipts were inspected rather than trusting that aggregate status alone. The envelope's 65,536 ordered-law-pair arithmetic checks are deterministic checks on its declared Boolean-valued inputs, not independent physical trials or proof of the complete API.

The new export checker also rejected actual disposable mutations: ID-only records, removed implementation source, and removed historical PASS receipt all exited 2. This closes the specific ID-only/export omissions from the earlier review.

Evidence: `results/replay/portable_summary.json`, the accompanying case receipts and stdout/stderr, `results/review_replay_context.json`, and `results/export_mutations.json`.

## Substantive success: composition now retains a route to its result

The producer reports a real defect in the original API: addition/multiplication discarded backing, so a composed result could not reopen. The current implementation stores a composition recipe instead.

The reviewer exercised the production API:

```text
p = multiply(multiply(unit(h), unit(x)), unit(y)) = hxy
```

The hot representation is the zero seven-coefficient tuple. The two backed multiplications made **zero cold reads** and created two recipe nodes. The degree bounds became 1, 2, 3 as required. After an admitted fixed-receiver h-flip, the reconstructed result was `xy - hxy`, reading 1 at `(0,1,1)` and 0 at the omitted `(1,1,1)` site. It was not an operand's old table or a zero fill.

Physically altering and deleting a required operand's backing file produced `INVALID_DEPENDENCY` and `UNRESOLVED`, respectively, with no exact result fabricated.

A separate seeded construction used 12 rational-valued starting laws and **96 arithmetic/map steps**. At each step, seven hot values plus the reopened omitted value matched an independently computed direct-table reference: **768 exact value comparisons**. The reference used direct Fraction arithmetic and direct input indexing, not the envelope's coefficient product/pullback helpers. This is finite exposed development verification, not a universal program-correctness proof.

This is a concrete realization of one recovered Prestige One requirement: a compact, operationally useful result retains a route to the construction it summarizes. It does not settle all prestige/reincarnation/approximate-grouping meanings.

## Required repair A — Boolean output-class escape hidden outside the current view

**Source:** `prestige_envelope.py`, `_family_after_arith`, lines 494–500; its use in `add_units`, lines 536–556.

The R1 PE26 test checks `h+h`. Because value 2 occurs at a retained site, the implementation correctly changes that output to `rational_cube`. It does not test the same class escape at the omitted site.

A counterexample uses only legitimate public constructors and operations:

```text
h, x, y = boolean-valued coordinate units with backing
p = multiply(multiply(h, x), y)
s = add(p, p)
```

All inputs are genuinely Boolean-valued. But `s = 2hxy`, not a Boolean-valued law.

Observed:

```text
s.retained                    = (0,0,0,0,0,0,0)
s.family                      = "boolean_cube"    # wrong full-output class
inspect_omitted(s).value       = 2                 # numerically correct
apply_input_map(s,"flip_h")    = EXACT
flipped readout at (0,1,1)     = 2
flipped.family                = "boolean_cube"    # still wrong
```

The numerical calculation is correct; the promised family excludes the actual full output. Passing its all-zero C2 to the Boolean-fiber helper yields `{0,hxy}`, neither of which is `2hxy`. This is how an incorrect metadata claim can erase the actual possibility without corrupting the visible arithmetic.

**Minimal safe direction:** distinguish the type rules for addition and multiplication. Pointwise multiplication of Boolean-valued laws stays Boolean. Ordinary addition over Q does not, absent an explicit global nonoverlap guarantee. Default such sums to a containing rational family, or retain a sufficiently justified stronger type. Do not infer a full-output class from B2 values alone. Do not read the omitted value silently just to keep a narrow label.

Keep input-family admission honest as well. The requested fix is not full candidate-set propagation; that remains outside this API.

Evidence: `results/independent_review.json`, check `hidden_boolean_addition_class_escape`.

## Required repair B — define the generic map's boundary and preserve metadata

**Source:** `prestige_envelope.py`, `apply_fixed_receiver_map`, lines 672–706.

Two directly exercised facts:

1. For a backed unit with `ARITH_CONTRACT`, the named call `apply_input_map(env,"flip_h")` returns `UNSUPPORTED`. The generic call with the same map returns `EXACT`. The generic entry point does not check that operation's admission.
2. The generic helper accepts an eight-site map that sends a site to input address 1 exactly when h and x are both on, and to 0 otherwise:

```text
mapping = (0,0,0,1,0,0,0,1)
```

Applying this to the coordinate law h gives hx. All map images lie in B2, so its hot calculation is valid, but the helper retains `degree_bound=1`. The actual result has degree 2.

The second issue is an incorrect advertised bound, not a wrong value. Coordinate flips/clamps do not establish a degree rule for every arbitrary site map.

**Bounded choices:** route supported public operations through a single admission/metadata path; admit arbitrary maps only through an explicit contract with appropriate bounds; or fence this function as an unchecked/reference helper that cannot supply a certified public envelope. Do not destroy the useful distinction between coherent coordinate/question transport and a changed fixed-receiver task.

Evidence: `generic_map_contract_gate` and `generic_map_degree_bound` in the independent result.

## Required repair C — aggregate status must reflect all required jobs

**Source:** exported `run_portable.py`, summary status construction and final `ok` expression.

The unmodified mathematical replay really passed. Separately, a **runner-only fault-injection harness** copied the package and substituted explicitly labelled fast fixtures for the expensive mathematical subjobs. It ran the actual unchanged portable entrypoint. These harness runs are not mathematical replays or additional theorem tests.

| Injected condition | Actual runner behavior |
|---|---|
| Starter exits 7 | Overall exit 0 and reported PASS |
| Required receipt removed; export checker exits 2 | Overall exit 2, but reported PASS |
| Negative-control subjobs crash with an unrelated exception (exit 1, no rejection receipt) | Overall exit 0 and reported PASS |

Causes: the JSON summary status uses only the first envelope job; starter success is absent from the aggregate expression; any nonzero negative-control exit counts as the intended rejection.

Compute one final verdict from all declared required jobs and use it consistently for JSON, stdout, and exit status. Required starter execution must count unless deliberately skipped under an explicitly narrower invocation. Require a structured expected coverage-rejection result from negative controls, not an arbitrary crash or absent output. A new registry framework is unnecessary.

Evidence: `results/runner_controls/runner_controls.json`, per-case stdout/stderr and portable summaries. The fixture substitutions are documented in `review_runner_controls.py`.

## Nonblocking scope/cost observations

`coherent_transport` reopens backing when it exists before falling back to the already sufficient hot values. A coherent transported receiver can be answered from the seven retained observations; the current backed branch incurs an avoidable read. This does not make its answer wrong and is not a blocker for the mathematical result. Do not describe that branch as avoiding cold work yet.

The affine-class positive checks are algebraic demonstrations, not a implemented general class-aware fallback in the main API. Candidate propagation for Q-sums remains outside scope. The finite fiving splice/Double-Stamp restart adapter, full Tile/Board/Atlas composition, and deferred broader recovered concepts remain open/preserved. No universal speedup, physical-safety result, or proof-assistant verification follows from these tests.

## Reviewer execution hygiene

The initial independent reviewer script completed its mathematical assertions but failed serializing a frozenset in the Boolean-fiber diagnostic. The serializer was corrected and the entire script was rerun into a fresh directory. That was a reviewer-output bug, not a submitted implementation failure. An initial local path assumption about the inner ZIP having a wrapper folder was also corrected before execution; it extracts directly at its root.

No uploaded source was patched. All mutations were confined to disposable review copies. This package supplies findings and reproducible checks, not a silently modified replacement implementation.

## Next decision

Keep the successful recovery and composition results. Complete the three narrow guard repairs under `CURSOR_RCF01_R2.md`, replay the existing suite plus direct regressions, and then stop this repair round. Paper placement and broader scientific applications remain separate decisions.
