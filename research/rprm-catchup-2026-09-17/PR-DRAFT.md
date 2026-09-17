# Pull request draft

The branch is pushed. The PR could not be opened from here: `gh pr create` fails
with

```text
GraphQL: wjfoster55 does not have the correct permissions to execute
`CreatePullRequest` (createPullRequest)
```

`gh auth status` reports scopes `gist, read:org, repo, workflow`, which are
sufficient for PR creation, so this is an account- or app-level restriction on
the OAuth app rather than a missing scope. The GitHub MCP tool fails identically.
Fixing it means changing authentication, which was out of scope for an overnight
run, so nothing was touched.

**Open it with one click:**
https://github.com/wjfoster55/RPRM-open/compare/main...research/catchup-thesis-defense-2026-09-17?expand=1

Title and body below are ready to paste.

---

## Title

```text
Catch-up synthesis, a non-BSD research pick, and a proof of its central conjecture
```

## Body

```markdown
Adds `research/rprm-catchup-2026-09-17/`: an outside-in reading of RPRM written
as a friendly thesis defence, a recommended non-BSD research target, and the
overnight work on that target.

### What is here

- **`RPRM-understanding-thesis-defense.pdf`** — 69 pages. Combined first- and
  third-party account of the framework, the core contract with fibers actually
  computed, a lens maturity table, a process-honesty chapter, a steelman, the
  criticisms, 51 answerable defence questions, and the pick. Appendices E and F
  record what happened overnight, including where the document's own first pass
  was wrong.
- **`FRAGILITY.md`** — the research record for the pick: typed claim, domain,
  missing ports, readout, hostile cases, dispositions, and what is still owed.
- **`05-portable-briefing-for-other-gpts.md`** — self-contained briefing that
  assumes no prior context.
- **`tools/`** — nine verification scripts. Integers and `fractions.Fraction`
  only; no floating point is used to decide anything.
- Ingest reports 01 and 03, the coverage-gap record, and a sanitized working-style
  page. Ingest lane 2 (process history) is deliberately **not** in the repo.

### The pick, and what landed

**The fragility spectrum of operational quotients.** For a partition `C` of an
`n`-element carrier, count the partial operations that survive it as an
operational quotient under the full O05 contract — successor agreement *and*
matching enabledness:

```text
sigma_a(C) = prod over (i1..ia) of ( 1 + sum_l  n_l^(n_i1 · ... · n_ia) )
```

Closed form, all arities, written proof plus complete finite verification.

**Priority is separated, not claimed.** Prior art exists for a *different*
monoid — the literature condition is successor agreement only, with no condition
on the domain. That count was re-derived from scratch here and reproduces the
published uniform-partition order exactly in all 22 computed cases. RPRM's
enabledness condition cuts out a strictly smaller submonoid. For a balanced
four-block reduction of an eight-state system it rejects 93% of the abstractions
the classical monoid admits.

**The extremal law is a theorem.** For fixed `n` and block count `m`, survival is
uniquely maximised by the maximally unequal profile and uniquely minimised by the
balanced one. Found first by exhaustive search (903 cells to `n = 45`, zero
counterexamples), then proved: the profile supplies both the bases inside
`f(k) = 1 + sum_j n_j^k` and the exponents at which `f` is evaluated, and the
proof is to stop conflating them. Karamata makes `f` pointwise larger; `f` is a
sum of exponentials hence log-convex, so spreading two exponents apart at fixed
sum cannot decrease their product. Higher arity follows by convex order.

**And the same argument explains the negative result.** The classical factor
function is `sum_j (n_j+1)^k - (m-1)` — a sum of exponentials *minus a positive
constant*, which is not log-convex. So the classical monoid has no clean extremal
shape (55 exceptions in 231 cells) while the enabledness-enforced one does.
Enabledness removes the `-1` per block, and the `-1` per block was what broke it.

### Coverage boundary, stated

This is a theorem about the **uniform prior over partial maps** and nothing else.
Under bijective priors the argmin half is **false**; within a fixed domain size it
is **false**; the total-map and idempotent classes remain conjectures the proof
does not reach. Those counterexamples are kept in the record rather than removed.

No novelty is claimed. Proving a statement and establishing that nobody has
proved it are different acts, and only the first happened. A real literature
review is still owed, as is an applied computation on one published reduced model.

### Not included, on purpose

No raw conversation extracts, no bulk sweep artifacts, no credentials, and not
the full process-history ingest report. No BSD material is touched.
```
