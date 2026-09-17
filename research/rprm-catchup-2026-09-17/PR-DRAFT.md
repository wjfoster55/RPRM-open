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

**Priority: the review was done, and it went against the count.** Prior art
exists for a *different* monoid — the literature condition is successor agreement
only, with no condition on the domain — and that count was re-derived here,
reproducing the published uniform-partition order exactly in all 22 computed
cases. RPRM's enabledness condition cuts out a strictly smaller submonoid, which
for a balanced four-block reduction of an eight-state system rejects 93% of the
abstractions the classical monoid admits.

But `LITERATURE-sigma-E.md` establishes two things against the project, and they
are stated here rather than in a footnote. **The closed form is not new**: it is
a one-line corollary of Sarkar–Singh, arXiv:2006.04242 Thm 6.1, via adjoining a
sink block, verified exactly on all 507 profiles to `n = 14`. **The enabledness
condition is not new either**: it is Fernandes's *P-stability* (1998). What the
review did not find is any published extremal result for these monoids — that
literature studies *rank* by partition shape, never *order*.

**The extremal law is a theorem.** For fixed `n` and block count `m`, survival is
uniquely maximised by the maximally unequal profile and uniquely minimised by the
balanced one. Found first by exhaustive search (903 cells to `n = 45`, zero
counterexamples), then proved: the profile supplies both the bases inside
`f(k) = 1 + sum_j n_j^k` and the exponents at which `f` is evaluated, and the
proof is to stop conflating them. Karamata makes `f` pointwise larger; `f` is a
sum of exponentials hence log-convex, so spreading two exponents apart at fixed
sum cannot decrease their product. Higher arity follows by tensoring the doubly
stochastic matrix, which majorises the exponent multiset directly.

An independent hostile audit confirmed the theorem and **broke three claims made
around it**, all of which are withdrawn in the record rather than edited away:
the `+1` is not what makes log-convexity work (deleting it leaves another sum of
exponentials); product-multiset majorisation does not fail (it is the shorter
proof); and the total-map class is not outside the proof (it is inside it, and is
promoted to theorem). The first and third were the same error.

**And the same argument explains the negative result.** The classical factor
function is `sum_j (n_j+1)^k - (m-1)` — a sum of exponentials *minus a positive
constant*. Adding a constant preserves log-convexity; subtracting one need not,
and here it does not. So the classical monoid has no clean extremal shape (55
exceptions in 231 cells) while the enabledness-enforced one does. Controlled:
hold the bases fixed and drop only the subtraction, and the law returns.

### Coverage boundary, stated

A theorem about the uniform prior over **partial** and over **total** maps, at
every arity `r >= 1`. At `r = 1` the total-map case is Sarkar–Singh's published
`|T(X,P)|`. Outside that: nullary arity is excluded (the count is
profile-independent); under bijective priors the argmin half is **false**; within
a fixed domain size it is **false**; and idempotents stay **OPEN** — their count
provably does not factor over blocks, so the mechanism has nothing to act on.
Those counterexamples are kept in the record rather than removed.

No novelty is claimed anywhere. Proving a statement and establishing that nobody
has proved it are different acts, and only the first happened. Still owed: the
Chinese-journal literature that the review could not access, and an applied
computation on one published reduced model.

### Not included, on purpose

No raw conversation extracts, no bulk sweep artifacts, no credentials, and not
the full process-history ingest report. No BSD material is touched.
```
