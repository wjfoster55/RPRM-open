# Fragility: the coverage boundary as a computable number

**Opened** 17 September 2026, overnight shift following the catch-up synthesis.
**Lane** typing and testing (wizard). Not abduction. Nulls declared before every
run and printed in every output.
**Status** partial results closed; the central extremal statement is a
**conjecture** with exhaustive finite evidence; priority is **settled for one
half and OPEN for the other**.

Reproduce everything here with

```text
python -I -B tools/fragility.py           closed form, brute force, n = 6 spectrum, search to n = 24
python -I -B tools/fragility_hostile.py   five hostile cases, extended search to n = 45
python -I -B tools/fragility_priority.py  prior-art separation, the enabledness price
```

Integers and `fractions.Fraction` only. No floating point appears in any value
used to decide anything; decimals in the tables are display approximations of
exact rationals that are also printed.

## 1. The question

RPRM's contract says an operational quotient is valid only relative to a
**declared** operation set. Every real operation set is incomplete. The framework
states that as a caution. This record turns it into a number.

## 2. The typed record

**Carrier.** A finite set `S`, `|S| = n`. Elements distinguishable, equality
exact, occurrences distinct from values.

**Object.** A partition `C` of `S` into `m` blocks with sizes
`(n_1, ..., n_m)`, `sum n_i = n`. Only the multiset of block sizes — the
**profile** — is supplied.

**Operation.** A deterministic **partial** map `g : S^a -> S` of arity `a`. The
ambient class has `(n+1)^(n^a)` elements: each of the `n^a` argument tuples maps
to one of `n` targets or is undefined.

**Admitted context.** One new operation at a time, drawn from a declared class.
The existing alphabet, the observations and the transition structure of any
underlying system are **missing ports** and are not used.

**Correlated missing ports kept joint.** The block sizes are jointly constrained
by `sum n_i = n`. Marginalising them destroys the object; every statement below
is about how the mass is distributed across blocks, not about any block alone.

**Operation kind, direction, enabledness.** Forward application. Enabledness is
the content: a surviving operation must be defined on a whole block or on none of
it.

**Receiver.** The partition itself, as an operational receiver: it must retain
which block a state is in, whether an operation is available, and which block the
successor lands in.

**Survival (the O05 test applied to one new operation).** `C` survives `g` when
for every pair of componentwise `C`-equivalent argument tuples,

1. both lie in `dom g` or neither does — **enabledness agreement**;
2. their images lie in the same block — **successor agreement**.

Observation agreement is inherited from `C` and is not re-tested.

**Requested readout.** `sigma_a(C)` = the exact integer count of surviving
operations, and the fragility `F_a(C) = 1 - sigma_a(C)/(n+1)^(n^a)` as an exact
rational.

**Inverse / retraction / fiber.** None is claimed. `sigma` is a counting
functional on profiles; the map from profile to count is not injective and no
retraction is asserted.

## 3. Result 1 — the closed form. Disposition ONE(formula).

```text
sigma_1(C) = prod_{i=1..m} ( 1 + sum_{j=1..m} n_j ^ n_i )

sigma_a(C) = prod over a-tuples (i_1..i_a) of
             ( 1 + sum_{l=1..m} n_l ^ ( n_{i_1} * ... * n_{i_a} ) )
```

**Written proof.** Fix the block of argument tuples
`B_{i_1} x ... x B_{i_a}`, of size `k = n_{i_1} * ... * n_{i_a}`. All its members
are componentwise `C`-equivalent, so enabledness agreement forces `g` to be
either undefined on the whole block or defined on the whole block, and successor
agreement forces the image of the whole block to lie inside a single block `B_l`.
Within that constraint `g` may be an arbitrary function from a `k`-element set
into `B_l`, of which there are `n_l^k`. Distinct tuple-blocks impose no
constraints on one another. Hence the choices for that block number
`1 + sum_l n_l^k`, and the total is the product. Nothing in the argument depends
on `a`.

**Evidence grade: written proof, plus finite test by complete enumeration.**
Confirmed against brute force over **every** map in the ambient class:

| Arity | n | Set partitions checked | Maps tested per partition | Result |
|---:|---:|---:|---:|---|
| 1 | 1–5 | 1, 2, 5, 15, 52 | up to 7,776 | all agree |
| 2 | 1–3 | 1, 2, 5 | up to 262,144 | all agree |

**Null declared before the run.** The discrete partition must survive every
operation, `sigma_1 = (n+1)^n`, `F = 0`. Held for `n = 1..8`: 2, 9, 64, 625,
7776, 117649, 2097152, 43046721.

## 4. Result 2 — priority. Disposition: ONE(citation) for half, NONE-after-search for the other half.

This is the part that changed overnight, and it changed in the project's favour.

### 4.1 What the literature already has

The monoid of **total** transformations preserving a partition,
`T(X,P) = { f : for every block C_i there is a block C_j with C_i f ⊆ C_j }`,
was introduced by H. Pei and its cardinality for finite `X` and **arbitrary**
partition is computed in *On certain Semigroups of Transformations that preserve
a partition*, arXiv:2006.04242. The **partial** analogue for a **uniform**
partition (`m` blocks of size `n`) is studied by Fernandes and Quinteiro,
*Partial transformation monoids preserving a uniform partition*,
arXiv:1210.4775, with published order

```text
( m (n+1)^n - m + 1 )^m
```

**These are prior art and they must be cited.** Disposition: **ONE(citation)**.

### 4.2 What the literature condition actually is

The literature imposes **successor agreement only**. Wherever `f` happens to be
defined on a block, the images must stay inside one block. It places **no
condition on the domain**: a map may be defined on part of a block and undefined
on the rest.

RPRM's O05 adds **enabledness agreement**. That is strictly stronger, so it cuts
out a submonoid. The two counts are different objects:

```text
sigma_blind(C) = prod_i ( 1 + sum_j [ (n_j + 1)^{n_i} - 1 ] )      literature
sigma_E(C)     = prod_i ( 1 + sum_j    n_j^{n_i}            )      RPRM O05
```

**Check that this identification is right, not merely plausible.** On a uniform
profile `(n, n, ..., n)` with `m` blocks, the first formula must collapse to the
published order. It does, exactly, in all 22 cases computed — including
`m = 5, n = 3`, where both give `3,150,905,752,576`. Both formulas also match
exhaustive brute force over every partial map for `n <= 6`, every profile, zero
mismatches.

So: the enabledness-blind count is published; **the enabledness-enforced count
`sigma_E` was not located in this search.** Disposition for `sigma_E` priority:
**NONE found after a stated search** — one web search of the transformation-
semigroup literature on 2026-09-17, following the four results it returned. That
is an admission of what was searched, **not** a novelty claim. A proper
literature review is still owed.

### 4.3 The enabledness price, exactly

`rho(C) = sigma_E(C) / sigma_blind(C)`. Then `1 - rho` is the exact fraction of
literature-admissible reductions that RPRM's enabledness condition rejects.

| n | profile | `sigma_E` | `sigma_blind` | `rho` | rejected |
|---:|---|---:|---:|---:|---:|
| 6 | (6) | 46,657 | 117,649 | 0.39658 | 60.3% |
| 6 | (5,1) | 21,889 | 54,649 | 0.40054 | 59.9% |
| 6 | (4,2) | 5,733 | 23,265 | 0.24642 | 75.4% |
| 6 | (3,3) | 3,025 | 16,129 | 0.18755 | 81.2% |
| 6 | (2,2,2) | 2,197 | 15,625 | 0.14061 | **85.9%** |
| 6 | (1,1,1,1,1,1) | 117,649 | 117,649 | 1.00000 | 0.0% |
| 8 | (4,4) | 263,169 | 1,560,001 | 0.16870 | 83.1% |
| 8 | (3,3,2) | 91,287 | 912,951 | 0.09999 | 90.0% |
| 8 | (2,2,2,2) | 83,521 | 1,185,921 | 0.07043 | **92.96%** |
| 8 | (1,…,1) | 43,046,721 | 43,046,721 | 1.00000 | 0.0% |

`sigma_E <= sigma_blind` in every profile computed, with equality exactly on the
discrete partition. That is the declared null and it held.

**Reading.** For a balanced four-block reduction of an eight-state system,
**93% of the abstractions the classical partition-preserving monoid admits are
rejected by the enabledness condition.** That number is the coverage boundary,
made numeric, on one concrete family.

## 5. Result 3 — the extremal law, and what the hostile cases did to it

**Conjectured before any search was run.** For fixed `n` and block count `m`:

```text
argmax sigma_E = (n-m+1, 1, 1, ..., 1)     maximally unequal
argmin sigma_E = the balanced profile      sizes differ by at most 1
```

### 5.1 Where it survived

| Test | Range | Counterexamples |
|---|---|---:|
| Arity 1, all partial maps | `2 <= n <= 45`, every `m`, every profile — **903 cells** | **0** |
| Arity 2 | `n <= 12` | 0 |
| Arity 3 | `n <= 10` | 0 |
| Total maps only (partiality dropped) | `n <= 18` | 0 |
| Idempotent total maps | `n <= 7` | 0 |

### 5.2 Where it broke — and this is the useful half

**H1, non-uniform priors.** The uniform prior over all partial maps was the
declared weakest assumption, so it was attacked first.

| Operation class | argmax failures | argmin failures |
|---|---:|---:|
| Injective partial maps, `n <= 7` | 0 | **2** — at `(n,m) = (6,2)` and `(6,3)` |
| Permutations, `n <= 7` | **1** — at `(4,2)` | **4** |
| Idempotent total maps, `n <= 7` | 0 | 0 |

**The minimum side is prior-dependent. The maximum side is nearly prior-free.**

The mechanism is completely explicable and worth stating because it turns a
failure into structure. Under permutations, `C` survives `g` exactly when `g`
permutes the blocks bijectively. Blocks of **equal size can be interchanged**, so
balanced profiles gain symmetry: for `n = 4`, the profile `(2,2)` admits
`2 x 2! x 2! = 8` surviving permutations while `(3,1)` admits only
`3! x 1! = 6`, because unequal blocks cannot swap. Under general partial maps the
opposite force dominates: a large blob absorbs arbitrary images. The two effects
compete, and which wins depends on the prior.

**H1b, fixed domain size.** The sharpest form of the objection — it removes the
"mostly-undefined maps dominate the count" explanation. At `n = 6`, counting only
partial maps with exactly `d` defined points:

| d | \|class\| | (5,1) | (4,2) | (3,3) | (4,1,1) | (3,2,1) | (2,2,2) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 36 | 6 | 0 | 0 | 12 | 6 | 0 |
| 2 | 540 | 0 | 20 | 0 | 36 | 14 | 36 |
| 3 | 4,320 | 0 | 0 | 108 | 0 | 120 | 0 |
| 4 | 19,440 | 0 | 272 | 0 | 258 | 216 | **432** |
| 5 | 46,656 | 3,126 | 0 | 0 | 3,096 | 504 | 0 |
| 6 | 46,656 | **18,756** | 5,440 | 2,916 | **9,288** | 3,024 | 1,728 |

At `d = 6` the law holds in both groups. At `d = 4` it **inverts** for `m = 3`:
`(2,2,2)` beats `(4,1,1)`. So the law is a statement about the *aggregate* over
domain sizes, not about every slice. Stating it without that qualifier would be
an overclaim.

The zeros are not noise. They are the next result.

### 5.3 The mechanism: admissible domain sizes are subset sums

Because a block is wholly enabled or wholly disabled, **the domain size of any
surviving partial operation is a subset sum of the profile.** Under the
literature condition every domain size `0..n` is reachable.

| profile | admissible domain sizes under O05 | count | of `n+1` |
|---|---|---:|---:|
| (6) | 0, 6 | 2 | 7 |
| (3,3) | 0, 3, 6 | 3 | 7 |
| (5,1) | 0, 1, 5, 6 | 4 | 7 |
| (4,2) | 0, 2, 4, 6 | 4 | 7 |
| (2,2,2) | 0, 2, 4, 6 | 4 | 7 |
| (4,1,1) | 0, 1, 2, 4, 5, 6 | 6 | 7 |
| (3,2,1) | 0, 1, 2, 3, 4, 5, 6 | 7 | 7 |
| (1,1,1,1,1,1) | 0, 1, 2, 3, 4, 5, 6 | 7 | 7 |

*Evidence grade: definition plus written proof. Immediate from the enabledness
condition.* It explains every zero in the `d`-slice table and it is the reason a
blob profile concentrates its surviving operations at a few very large domain
sizes where the counts are enormous.

## 6. Result 4 — the flagship. Enabledness restores an extremal law the classical monoid does not have.

This was not conjectured in advance. It came out of running the priority
separation, and it is the strongest thing in this record.

Run both monoids side by side over the same 231 `(n, m)` cells, `3 <= n <= 24`:

| Monoid | argmax law holds? | argmin law holds? |
|---|---|---|
| `sigma_E` — enabledness enforced (RPRM O05) | **yes, 0 failures in 903 cells to `n = 45`** | **yes, 0 failures** |
| `sigma_blind` — successor only (Pei / Fernandes–Quinteiro) | **no, 14 failures in 231 cells** | **no, 41 failures** |

And where they disagree, they do not merely differ — they **invert**. The first
disagreement is at `n = 11, m = 9`:

```text
sigma_E     argmax (3,1,1,1,1,1,1,1,1)    argmin (2,2,1,1,1,1,1,1,1)
sigma_blind argmax (2,2,1,1,1,1,1,1,1)    argmin (3,1,1,1,1,1,1,1,1)
```

The most robust profile under one condition is the least robust under the other.

**Claim, stated at its exact ceiling.** On the finite family of profiles with
`3 <= n <= 24`, the classical partition-preserving partial transformation monoid
has no clean extremal shape — the maximiser and minimiser wander, with 55
exceptions in 231 cells — while the submonoid cut out by adding RPRM's
enabledness condition has an exact and apparently universal one, with zero
exceptions in 903 cells up to `n = 45`.

*Evidence grade: finite test, complete enumeration inside the stated ranges.*
Not a theorem. The general statement is **OPEN** in both directions: it is open
whether `sigma_E`'s law holds for all `n`, and open whether `sigma_blind`'s
failures have their own characterisation.

This is the argument that RPRM's extra condition is mathematically load-bearing
rather than merely fastidious. It is not an argument that the condition is
*correct* — that is a modelling question — but it does mean the condition picks
out a structurally better-behaved object, which is a reason to take it seriously
that does not depend on agreeing with the framework's philosophy.

## 7. Result 5 — fragility is not monotone in compression

The most fragile profile at each `n`, against the fully collapsed one-block
profile:

| n | most fragile profile | F | F of the single block `(n)` | is total collapse the worst? |
|---:|---|---:|---:|---|
| 4 | (2,2) | 0.870400 | 0.588800 | no |
| 6 | (2,2,2) | 0.981326 | 0.603422 | no |
| 8 | (2,2,2,2) | 0.998060 | 0.610256 | no |
| 10 | (3,3,2,2) | 0.999858 | 0.614457 | no |
| 12 | (3,3,3,3) | 0.999994 | 0.617303 | no |

The maximiser of fragility is always a balanced profile of small blocks, never
either extreme. Collapsing everything into one block is markedly *safer* than
moderately aggressive balanced binning, because a single block is preserved by
any total map and by the empty map alike. **Compression ratio is not a proxy for
robustness.**

## 8. The asymptotic sandwich

Let `M = max_i n_i`. Since `S_k = sum_j n_j^k` lies in `[M^k, m M^k]` and
`M^k >= 1`, every factor satisfies `M^{n_i} <= 1 + S_{n_i} <= (1+m) M^{n_i}`.
Multiplying over the `m` blocks and using `sum n_i = n`:

```text
M^n  <=  sigma_1(C)  <=  (1+m)^m * M^n
```

so `log sigma_1 = n log M + O(m log m)`. The leading term is monotone in `M`, the
unequal profile maximises `M` and the balanced profile minimises it, which is the
shape of the conjecture. Verified numerically for every profile, `n = 2..15`: the
sandwich holds in all 682 profiles, and `min sigma/M^n` converges to 1 fast
(1.2500 at `n = 2`, 1.000021 at `n = 6`, 1.000000 to six places from `n = 8`).

**This is not yet a proof.** For fixed `m` and large `n` the `(1+m)^m` slack
exceeds the gap between competing values of `M^n`, so the sandwich alone does not
separate `(n-m+1, 1, ..., 1)` from `(n-m, 2, 1, ..., 1)`. A proof needs either a
sharper upper bound or a direct exchange lemma: that moving one element from a
smaller block to a larger one strictly increases `sigma_1`. The exhaustive search
to `n = 45` is consistent with that lemma and does not establish it.

## 9. Dispositions

| Statement | Disposition | Grade |
|---|---|---|
| Closed form for `sigma_a(C)`, all arities | **ONE(formula)** | Written proof + complete finite test |
| Null: discrete partition, `F = 0` | **ONE(value)** | Finite test, `n <= 8` |
| `sigma_blind` reproduces the published uniform-partition order | **ONE(identity)** | Finite test, 22 cases, exact |
| Enabledness price `rho(C)` | **ONE(rational)** per profile computed | Exact arithmetic |
| Admissible domain sizes = subset sums of the profile | **ONE(characterisation)** | Written proof |
| Extremal law for `sigma_E`, arities 1–3, total and idempotent classes | **OPEN** — conjecture, 0 counterexamples in 903 cells to `n = 45` | Finite test |
| Extremal law under injective or permutation priors | **refuted for argmin**, 6 explicit counterexamples retained | Finite test |
| Extremal law within a fixed domain size | **refuted**, `(2,2,2)` beats `(4,1,1)` at `n = 6, d = 4` | Finite test |
| `sigma_blind` has no clean extremal law while `sigma_E` does | **ONE(comparison)** on `3 <= n <= 24`; general case **OPEN** | Finite test, complete enumeration |
| Priority of `sigma_blind` | **ONE(citation)** — arXiv:1210.4775, arXiv:2006.04242 | Located |
| Priority of `sigma_E` | **NONE found after a stated single-pass search** | Not a novelty claim |
| Applied corollary "uniform binning is worst" | **restricted**: holds under partial, total and idempotent priors; **fails** under bijective priors | Finite test |

## 10. What is owed next

1. A real literature review for `sigma_E`, beyond one search pass. Until then no
   novelty is claimed.
2. The exchange lemma, which would convert the extremal conjecture into a
   theorem. Start at `m = 2`, where `sigma_E = (1 + a^a + b^a)(1 + a^b + b^b)`
   with `a + b = n`.
3. A characterisation of `sigma_blind`'s 55 extremal exceptions. They are
   concentrated at large `m` with mostly-singleton profiles, which suggests a
   clean description exists.
4. Arity-3 and total-map hostile cases pushed further than `n = 10` and `n = 18`.
5. The applied lane: take a published finite reduced model of a partial system
   and compute its `rho`. That converts the instrument into a finding.

## 11. What this record does not establish

It does not establish that any abstraction in any real system is wrong. It does
not establish that the uniform prior over operations is the right measure for any
application; Section 5.2 shows the answer depends on the prior, and identifying
the right prior is a modelling obligation that has not been discharged. It does
not establish novelty. It does not make the extremal conjecture a theorem, and
`n <= 45` is not "all `n`".
