# Cursor: BSD / Absolute Distinction 0.1 — review repair, one active task

Continue the existing `rprm-bsd-absolute-distinction` workspace. Do NOT start over or run archived prompts. This is a small correction to the first return, not authorization for a new general Selmer project.

## Context and source binding

The reviewer reproduced all five submitted stages using `MANIFEST.candidate.json`, and every mathematical result payload matched `runs/candidate_001`. The submitted input archive hash is recorded in `REPLAY_COMPARISON.json`. Existing candidate-manifest SHA-256:

`28885f21146065783c06efe9703c85ae818036850c52f87833c8e962e6850b21`

The reviewer also found an actual omitted-case mutation that passes the full runner, a semantic mistranslation in the return, an omitted condition in the dependency map, and a degeneracy in the proposed next study. Read `REVIEW.md`, `REVIEW_CHECKS.json`, and `COVERAGE_GAP_RECEIPT.json` first.

Review scripts should be outside the audited source tree for baseline replay (or in a clearly excluded `runs/review_materials/` directory). Adding Python files anywhere else under the project changes its manifest's source inventory. Do not silently re-freeze the original just to hide this change.

Respect actual workspace instructions, preserve unrelated edits and all receipts, and make no external writes, installations, paid calls, pushes or merges. Use new candidate names and fresh run directories. Do not overwrite `MANIFEST.json` or `MANIFEST.candidate.json`.

## A. Reproduce the baseline and the coverage finding

Run the current candidate with a fresh output path:

```text
python -B run_all.py --manifest MANIFEST.candidate.json --output runs/review_baseline_002
```

Existing directories require a new name, not deletion. Keep assertions enabled.

Run the attached external reviewer scripts on a disposable copy/out-of-tree path, or reproduce the exact findings with an equally inspectable script:

```text
python -B review_checks.py --package <project> --output <fresh-review-json>
python -B reproduce_coverage_gap.py --package <project> --work <new-disposable-directory-outside-project>
```

Before the fix, actual deletion of the AD11 record call produces only ten question audits and nevertheless PASS. The negative control `silently_drop_failed_case` still claims rejection. The reproduction honestly creates a new candidate manifest; it does not defeat the old manifest's integrity check. Do not change that scope in reporting.

## B. Enforce the already-declared obligations on the actual aggregate path

`protocol.json` already declares `audit_cases` AD01-AD11 and `operational_cases` OP01-OP03. Wire those into a real coverage validator before aggregate PASS. Do not derive expected obligations from emitted rows. Avoid a large framework or multiple registries when one existing protocol is enough.

Required behavior:

- Exact required IDs appear once each. Missing, duplicate and unexpected IDs fail explicitly; counts alone are insufficient.
- Required stages produce properly typed results, and their required cases/control outcomes are present and valid before aggregate PASS. An expected mathematical REFUTED verdict is a valid outcome, not a runner failure.
- State the minimal required schema and validate what the runner actually relies on, rather than accepting any callable return because no exception was raised.
- Replace positional lookups such as `audits[6]` with case-ID lookups where they couple controls to specific obligations.
- Keep the byte-integrity manifest distinct from protocol coverage and semantic correctness.
- Update the documented active invocation to name the actual candidate manifest; leave historical instructions/receipts intact and clearly labeled.

Prove the fix with a small set of actual mutations, not only Boolean comparisons that narrate what might fail:

1. Remove AD11 from execution -> required-case failure and aggregate FAIL/nonzero exit.
2. Remove a required OP case -> the same.
3. Replace an expected case ID with an unexpected ID, preserving total count -> failure.
4. Duplicate one case ID while hiding another -> failure.
5. Reorder states and reorder valid result rows -> unchanged mathematical verdict and valid coverage.
6. A required stage returns no valid result record despite returning normally -> failure.

Keep the original finite arithmetic unchanged unless a reproduced arithmetic defect requires a separately explained patch. Reuse the external small-table oracle or an equivalently independent pairwise implementation to verify the core. No claim that this proves arbitrary Python programs correct.

## C. Repair the meanings instead of silently replacing them

Correct `RETURN_TO_WILLIAM.md` and any affected ledger/dependency references:

- 'Prestige/rebirth one' in this conversation is a tentative layered/tiered object idea. Vanishing order was explored as one exact depth model. It is NOT social status or the policy of distrusting authority. Preserve `(r,u)` for `f=t^r*u` with `u(0)!=0` as the exact mathematical example, distinct from package/promote operations, overall complexity and literal arithmetic 1.
- The no-exemption-by-authority policy belongs to Absolute Distinction and is a separate use of 'prestige'.
- Keep F5 versus Z/6Z as a carrier/admission example, not as the recovered formal meaning of the earlier Five/Six operators. The inherited prior prompt/notes identify Five as a counterexample-localization/refinement operator; unsupported Six/fiving/sixing mechanisms stay explicitly unformalized. Do not search for or invent a missing prime-hop algorithm in this task.
- A numeral can occupy value, address, count, coefficient or another specified role. Do not define every numeral as an address.

Retain one short intent -> formalization record with the original intended meaning and the exact narrowed mathematical proposal. Do not claim full formalization of the user's speculative vocabulary.

The consolidated prompt left this ambiguous, so report it as a handoff correction rather than blaming either the user or prior mathematics.

## D. Restore the lifting condition

In the dependency map use `k=e` or explicitly `k>=e` when obtaining
`image(S_(n+k)->S_n)=G_n` from the hypothesis that the ell-primary Sha is killed by ell^e. The unconditioned finite-depth expression leaves the obstruction term `ell^k Sha[ell^(n+k)]`.

For k<e, that exponent bound alone does not establish vanishing; do not claim vanishing is impossible in every special case. Distinguish standard mathematical identities that were not computed from genuinely open universal claims.

## E. Replace the next-study proposal; do not launch it

Explain this known null before proposing more computation:

Confirmed Selmer n-coverings have points everywhere locally. Therefore exact local-solubility Boolean vectors are constant on that admitted set, for any choice of places. If there are both globally realized and obstructed classes, those bits cannot distinguish them. Adding more such bits does not repair the loss.

Important qualifications:

- Before Selmer admission, those local tests can screen a larger candidate family; that is a different question.
- Full covering equations, explicit maps, local witnesses, pairings and higher-descent information are richer data than the Boolean vector.
- Different class IDs alone do not refute a decoder for a Boolean global-realizability question. The witness needs different target answers, independently justified.
- An exhausted finite point-search budget means UNRESOLVED unless accompanied by a valid nonexistence theorem/certificate.
- Zero pairing or finite lifting persistence is not automatically a global-point certificate.

Prepare ONE next-experiment proposal focused on an actual arithmetic certificate, not rank fitting. Preferred target: explicit coverings for one elliptic curve with a rational-point witness and a separately justified obstruction example, or one source-bound case that cleanly distinguishes local evidence from a global certificate.

The proposal must name actual source locations, curve and covering equations, the covering maps or exact availability gap, the relevant local and global proof obligations, an ordinary comparator, and a cost ledger for any additional retained information. State what the candidate method sees versus what only the evaluator may use. Do not use `E.sha().an()` or a database rank label as independent proof. Do not assume a Sage API exposes complete coverings merely because it returns a dimension.

Use primary sources. Stoll, *Descent on elliptic curves*, sections 1.1-1.3, especially printed pages 8-12, gives the covering interpretation and the role of rational-point search/higher descents:
`https://arxiv.org/pdf/math/0611694`
Sage documents which Sha values are conjectural:
`https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/sha_tate.html`

Source inspection to make the proposal concrete is in scope. No new Selmer/L-series execution, large dependency installation, open-ended literature sweep or feature search is in scope. If a needed covering or certificate is genuinely unavailable after a bounded source lookup, retain the exact blocking item instead of fabricating it. Do not recycle the constant-bit null as the central scientific result.

## F. Return and stop

Deliver:

- `RETURN_REVIEW_REPAIR.md`: baseline reproduced, actual pre-fix omission receipt, precise patch, post-fix mutation outcomes, semantic corrections and remaining limits;
- an updated distinction ledger and dependency map, with historical receipts preserved;
- one new manifest and fresh successful full-run receipts, plus expected failing mutation receipts;
- `NEXT_ARITHMETIC_CERTIFICATE_PROPOSAL.md` as the sole proposed next study.

The success criterion is repairing the exact demonstrated gaps while preserving valid compressions and all supported arithmetic. No new broad framework, UI, detector-agent system, proof of BSD or universal research-success claim.
