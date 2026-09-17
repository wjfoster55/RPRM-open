# Fragility: the coverage boundary as a computable number

**Opened** 17 September 2026, overnight shift following the catch-up synthesis.
**Lane** typing and testing (wizard). Not abduction. Nulls declared before every
run and printed in every output.
**Status** the central extremal statement is, as of §8d and §8e, a **theorem at
every arity** for the uniform partial-map prior, with a written proof. It remains
a conjecture for the total-map and idempotent classes, and is **false** for the
bijective ones. Priority is **settled for one half and OPEN for the other**.

Reproduce everything here with

```text
python -I -B tools/fragility.py           closed form, brute force, n = 6 spectrum, search to n = 24
python -I -B tools/fragility_hostile.py   five hostile cases, extended search to n = 45
python -I -B tools/fragility_priority.py  prior-art separation, the enabledness price
python -I -B tools/fragility_exchange.py  the exchange lemma, 5.7M exchanges to n = 40
python -I -B tools/fragility_critical.py  targeted attack on the tightest exchange family
python -I -B tools/fragility_limit.py     the cosh^2(1) asymptotic
python -I -B tools/fragility_proof.py 30  every step of the §8d proof, exact
python -I -B tools/fragility_arity.py     the §8e general-arity argument
python -I -B tools/fragility_mechanism.py why the proof fails for sigma_blind
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

## 8b. The exchange lemma — stated, and where it is tightest

> **Section 8b and 8c were written while this was still a conjecture. Section 8d
> proves it. The two sections are kept as written, because where the evidence was
> tightest is what told the proof where it had to work.**

The extremal law is awkward to prove directly because it is a statement about
argmax and argmin over a whole poset. A single stronger statement implies both
halves at once and is a far better thing to hand a combinatorialist.

> **Exchange lemma.** Let `C` have two blocks of sizes `a >= b` with `b >= 2`,
> and let `C'` replace them by `a+1` and `b-1`, keeping `n` and `m` fixed. Then
> `sigma_E(C') > sigma_E(C)` strictly.

**This implies the extremal law**, and it is a local statement about two blocks
rather than a global one about a poset. The implication needs no machinery. If a
profile with `m` blocks is not balanced, some pair has `a >= b + 2`, so the
*reverse* exchange applies to `(a-1, b+1)` and produces a strictly smaller
`sigma_E`; iterating strictly decreases and terminates at the balanced profile,
which is therefore the unique minimum. If a profile is not `(n-m+1, 1, ..., 1)`,
some block has size `>= 2` besides the largest, so a forward exchange applies and
strictly increases; iterating reaches the maximally unequal profile, which is
therefore the unique maximum. (This is the majorisation order on partitions of
`n` into exactly `m` parts, but the argument above does not need that fact.)

**The first step was proved before the rest.** With `S_k = sum_j n_j^k`, the
exchange gives `S'_k >= S_k` for every `k >= 1`, strictly for `k >= 2`:
`(a+1, b-1)` majorises `(a, b)` and `x -> x^k` is convex, so Karamata applies.
Consequently every factor of `sigma_E` indexed by an unchanged block weakly
increases, and the factor for the grown block strictly increases. Checked on all
14,799 exchanges for `n <= 19`: zero violations, as it must be.

**What stayed unproved for most of the night** was that the single shrinking
factor `(1 + S'_{b-1})` cannot lose more than everything else gains. The crude
sandwich of Section 8 is lossy by a factor of `(1+m)^2` here, which was exactly
the gap. Section 8d closes it by not going through the sandwich at all.

**Evidence, gathered before the proof existed.** Every valid exchange in every
profile, `n = 4..40`:

| Quantity | Value |
|---|---:|
| Exchanges tested | **5,686,463** |
| Non-increases | **0** |
| Tightest ratio observed | 1.000678, at `n = 40`, `(26,7,7) -> (26,8,6)` |
| `m = 2` case pushed to `n = 400` | 39,601 exchanges, 0 failures |

**Where it is tightest, and therefore where a proof must work.** The minimising
exchange always has the same shape: a large spectator block, and two *equal*
blocks being split apart.

| n | tightest exchange | ratio |
|---:|---|---:|
| 6 | (2,2,2) → (3,2,1) | 1.768320 |
| 12 | (6,3,3) → (6,4,2) | 1.286139 |
| 18 | (10,4,4) → (10,5,3) | 1.079199 |
| 24 | (14,5,5) → (14,6,4) | 1.023515 |
| 30 | (18,6,6) → (18,7,5) | 1.006507 |

The ratio falls toward 1. That is alarming enough to attack directly rather than
extrapolate, so the family `(K, j, j) -> (K, j+1, j-1)` was stressed far beyond
the general search: `j` up to 200, spectator `K` up to `100,000`, plus the
three-equal-block variant, the all-equal-blocks variant with `m` up to 40, and
the no-spectator variant to `j = 2000`.

**Total refutations across every targeted family: 0.** The ratio approaches 1
from above and does not cross it. Along `(2j, j, j) -> (2j, j+1, j-1)` the excess
`ratio - 1` halves cleanly with each increment of `j`: the successive quotients
run 1.995, 1.920, 1.868, 1.885, ... 1.9975 at `j = 40`, converging to **2**.

*Evidence grade: finite test, complete enumeration for `n <= 40` plus targeted
families far beyond it. Still a conjecture.*

## 8c. An exact asymptotic: splitting a balanced pair multiplies survival by cosh²(1)

The no-spectator exchange out of the balanced two-block profile does **not**
approach 1. It approaches a constant, and the constant is identifiable.

```text
sigma_E(j, j)     = ( 1 + 2 j^j )^2                                  ~ 4 j^{2j}
sigma_E(j+1, j-1) = ( 1 + (j+1)^{j+1} + (j-1)^{j+1} )
                    ( 1 + (j+1)^{j-1} + (j-1)^{j-1} )                ~ (j+1)^{2j} (1 + e^{-2})^2
```

since `((j-1)/(j+1))^{j±1} -> e^{-2}`. Therefore

```text
sigma_E(j+1, j-1) / sigma_E(j, j)  ->  e^2 (1 + e^{-2})^2 / 4
                                    =  ( e + e^{-1} )^2 / 4
                                    =  cosh^2(1)  =  2.381097845541816...
```

The derivation was written before the numbers were printed. Exact-arithmetic
check:

| j | n | ratio | limit − ratio | j · (limit − ratio) |
|---:|---:|---:|---:|---:|
| 10 | 20 | 2.173595361539517 | 2.075e-01 | 2.0750 |
| 100 | 200 | 2.357623065853014 | 2.347e-02 | 2.3475 |
| 1,000 | 2,000 | 2.378720143406846 | 2.378e-03 | 2.3777 |
| 20,000 | 40,000 | 2.380978799147820 | 1.190e-04 | 2.3809 |

So `ratio = cosh^2(1) (1 - 1/j) + O(1/j^2)`, with the `1/j` coefficient itself
converging to `cosh^2(1)`.

**Reading.** The balanced two-block partition is not marginally worse than its
neighbour. It is worse by a fixed factor of about 2.381 that does not wash out as
the carrier grows. *Evidence grade: written derivation plus exact finite test.
Disposition ONE(constant).* It does not prove the exchange lemma — the lemma also
has to survive the spectator families where the ratio tends to 1, and that is
where the open problem lives.

## 8d. Result 6 — the exchange lemma is a theorem, and the extremal law follows

*Written after 8b and 8c, and after the numeric attack on the tight family had
failed to break the lemma. Machine check of every step:*
`python -I -B tools/fragility_proof.py 30`.

The sandwich of Section 8 was the wrong instrument. It tried to bound the
spectator product, which is where it lost `(1+m)^2`. The spectator product does
not need bounding: it is *termwise* larger after the exchange, and the entire
difficulty can be pushed into a statement about one function of one variable.

**Notation.** For a profile `p` write `S_k(p) = sum_j n_j^k` and

```text
f_p(k) = 1 + S_k(p) ,        sigma_E(p) = prod_i f_p(n_i) .
```

Note the two roles `p` plays: it supplies the *bases* inside `f_p`, and it
supplies the *exponents* at which `f_p` is evaluated. The proof separates them.

Let `p` have blocks `a >= b >= 2` and spectators `c_1, ..., c_{m-2}`, and let `q`
be `p` with those two blocks replaced by `a+1` and `b-1`.

> **Step 1 (bases).** For every `k >= 1`, `S_k(q) >= S_k(p)`, strictly for
> `k >= 2`.
>
> *Proof.* `(a+1, b-1)` majorises `(a, b)` and `x -> x^k` is convex on `x > 0`,
> strictly convex for `k >= 2`; the spectators are unchanged. Karamata. For
> `k = 1` both sides equal `n`. ∎

Hence `f_q(k) >= f_p(k)` for all `k >= 1`, strictly for `k >= 2`.

> **Step 2 (exponents).** `f_q` is log-convex, so
> `f_q(a+1) f_q(b-1) >= f_q(a) f_q(b)`.
>
> *Proof.* `f_q(k) = e^{k·0} + sum_j e^{k ln q_j}` is a sum of log-convex
> functions of `k`, hence log-convex; the constant `1` is the `e^{k·0}` term and
> is what makes this work. Write `h = log f_q`, convex. Since `a >= b`, the
> interval `[a, a+1]` lies weakly to the right of `[b-1, b]`, and `h'` is
> nondecreasing, so `h(a+1) - h(a) >= h(b) - h(b-1)`. Exponentiate. ∎

> **Step 3 (combine).**
>
> ```text
> sigma_E(q) = ( prod_c f_q(c) ) · f_q(a+1) · f_q(b-1)
>           >= ( prod_c f_q(c) ) · f_q(a)   · f_q(b)     by Step 2
>           >  ( prod_c f_p(c) ) · f_p(a)   · f_p(b)     by Step 1
>            = sigma_E(p) .
> ```
>
> The last line is strict because `a >= 2`, so `f_q(a) > f_p(a)`, and every
> factor is positive. ∎

**Theorem (exchange).** For `a >= b >= 2`, `sigma_E(q) > sigma_E(p)`.
**Corollary (extremal law, arity 1).** For fixed `n` and `m`, `sigma_E` is
uniquely maximised at `(n-m+1, 1, ..., 1)` and uniquely minimised at the balanced
profile. *Both by the iteration argument in 8b.*

**Disposition ONE(theorem) for arity 1. Evidence grade: written proof.** Every
step machine-checked in exact integer arithmetic on all **128,121** distinct
exchanges over all **28,622** partitions of `n = 4..30`, including the separate
null control that Step 2's log-convexity also holds for the *old* profile — it is
a property of the factor function, not an artifact of the exchange. Zero
failures. In the hostile large-spectator family, Step 2 was checked with spectator
blocks up to `10^30`, where the direct ratio is numerically indistinguishable
from 1; Step 2 holds there because the spectator enters it only through `S_k` and
pushes the ratio toward 1 from above, never through it.

**What §8d leaves open.** Arities `>= 2`, where the exponents are products rather
than single block sizes. Section 8e closes that too.

## 8e. Result 7 — the same proof at every arity, via convex order

At arity `r` the factors are indexed by **products** of block sizes:

```text
sigma_r(p) = prod over ordered r-tuples T of   f_p( prod_{i in T} p_i ) .
```

Step 1 is unchanged. Step 2 needs replacing, because there are now `m^r`
evaluation points rather than two, and what must be shown is that for every
convex `phi`

```text
sum_T phi(e'_T)  >=  sum_T phi(e_T)                                    (*)
```

where `e_T`, `e'_T` are the exponent products before and after the exchange.

**Proof of (*).** Read a uniformly random ordered `r`-tuple as `r` independent
coordinate draws, and condition on which coordinates land in the two changed
blocks — call that set `U`, `|U| = s` — and on the spectator choices for the
remaining `r - s` coordinates, whose product is a constant `P > 0`. Every tuple
falls in exactly one cell. Inside a cell the exponent is `P` times a product of
`s` independent draws, each uniform on `{a, b}` before and on `{a+1, b-1}` after.

1. `{a+1, b-1}` majorises `{a, b}` at equal mean, so for the single draw
   `X <=_cx X'` in the convex order.
2. Convex order is closed under multiplication by an independent nonnegative
   factor: for `y >= 0` the map `x -> phi(xy)` is convex, so conditioning and
   integrating gives `XY <=_cx X'Y <=_cx X'Y'`. Induction on `s` gives
   `prod X_i <=_cx prod X'_i`. All values are positive because `b >= 2`.
3. Scaling by `P >= 0` preserves convex order, same reason.
4. The inequality `sum phi >= sum phi` is **additive over cells**, so summing
   over every `U` and every spectator assignment gives (*). ∎

Note step 4 is why the argument is phrased in convex order rather than
majorisation: majorisation is not additive over disjoint unions, but the
`sum phi` inequality is, and the `sum phi` inequality is all Karamata was ever
being used for.

Then exactly as before, with `phi = log f_q` (convex, since `f_q` is log-convex):

```text
sigma_r(q) = prod_T f_q(e'_T) >= prod_T f_q(e_T) >= prod_T f_p(e_T) = sigma_r(p),
```

strictly, because `a >= 2` makes the factor at the all-`a` tuple — exponent
`a^r >= 2` — strictly larger.

**Theorem (exchange, all arities).** For every `r >= 1` and `a >= b >= 2`,
`sigma_r(q) > sigma_r(p)`.
**Corollary.** The extremal law holds for `sigma_r` at every arity.

*Disposition ONE(theorem). Evidence grade: written proof.* Machine check:
`python -I -B tools/fragility_arity.py`. The cell decomposition of step 4 was
verified to reproduce the brute-force exponent multiset exactly; (*) was tested
against six convex functions the proof never mentions, including `2^x` and two
piecewise-linear hinges; and two concave controls were required to **reverse**
the inequality, which they do. 963 exchanges at arities 2, 3 and 4.

> A note on the null control, because it is the kind of thing worth keeping. The
> first version of this test demanded that *every* concave `phi` reverse the
> inequality **strictly**, and flagged 143 failures. The failures were mine:
> `min(x, 12)` is concave but linear below the kink, so on exchanges whose
> exponents all sit under it both sides are equal, which is correct behaviour.
> The test was wrong, not the claim. Corrected, then rerun.

## 8f. Result 8 — why the same proof cannot work for the classical monoid

This is the mechanism behind Result 4, and it is one line.

The proof rests on exactly one property: `f_p(k) = 1 + sum_j n_j^k` is log-convex
in `k`, because it is a sum of exponentials. The classical successor-only count
has factor function

```text
f_blind,p(k) = 1 + sum_j ( (n_j+1)^k - 1 ) = sum_j (n_j+1)^k - (m - 1) .
```

That is a sum of exponentials **minus a positive constant** whenever `m >= 2`.
Subtracting a constant does not preserve log-convexity. So Step 2 is not merely
harder for `sigma_blind` — **its hypothesis is false.**

Tested on all 913 profiles with `n <= 16`, over all `a >= b >= 1`:

| factor function | instances tested | log-convexity violations | worst ratio |
|---|---:|---:|---:|
| `f_p` — enabledness enforced | 25,702 | **0** | — |
| `f_blind,p` — successor only | 25,702 | **7,488** | 0.1357 |

and the failures live in the same regime as the extremal-law failures: the `-1`
per block is largest relative to the whole factor exactly when blocks are tiny,
which is why `sigma_blind`'s 41 bad `(n, m)` cells are all many-block,
mostly-singleton profiles.

> **Reading.** Enabledness is not decoration. Dropping the domain requirement
> subtracts one unit per block from every factor, and that subtraction is
> precisely what destroys log-convexity of the factor function and with it the
> extremal law. The condition RPRM adds for modelling reasons is the condition
> that makes the count analytically well behaved.

*Evidence grade: written proof for the `sigma_E` direction; finite test for the
`sigma_blind` failures. Reproduce with* `python -I -B tools/fragility_mechanism.py`.

This does **not** say enabledness is the right modelling choice. It says the two
conditions cut out objects of different analytic character, and the difference is
identifiable rather than aesthetic.

## 9. Dispositions

| Statement | Disposition | Grade |
|---|---|---|
| Closed form for `sigma_a(C)`, all arities | **ONE(formula)** | Written proof + complete finite test |
| Null: discrete partition, `F = 0` | **ONE(value)** | Finite test, `n <= 8` |
| `sigma_blind` reproduces the published uniform-partition order | **ONE(identity)** | Finite test, 22 cases, exact |
| Enabledness price `rho(C)` | **ONE(rational)** per profile computed | Exact arithmetic |
| Admissible domain sizes = subset sums of the profile | **ONE(characterisation)** | Written proof |
| **Exchange lemma, arity 1** | **ONE(theorem)** | **Written proof** (§8d); every step machine-checked on 128,121 exchanges to `n = 30` |
| **Exchange lemma, every arity** | **ONE(theorem)** | **Written proof** (§8e, convex order); decomposition and six convex test functions checked, concave controls reverse |
| **Extremal law for `sigma_r`, every arity** | **ONE(theorem)**, corollary of the above | **Written proof** |
| Extremal law under the total-map and idempotent-map classes | **OPEN** — conjecture, 0 counterexamples to `n = 18` / `n = 7`; the proof above does not cover them, since those classes are not the uniform partial-map prior | Finite test |
| Karamata step `S'_k >= S_k`, strict for `k >= 2` | **ONE(inequality)** | Written proof |
| `f_p(k) = 1 + sum_j n_j^k` is log-convex; `f_blind` is not | **ONE(separation)** | Written proof + 25,702-instance finite test |
| `sigma_E(j+1,j-1)/sigma_E(j,j) -> cosh^2(1)` | **ONE(constant)** | Written derivation + exact finite test to `j = 20,000` |
| Extremal law under injective or permutation priors | **refuted for argmin**, 6 explicit counterexamples retained | Finite test |
| Extremal law within a fixed domain size | **refuted**, `(2,2,2)` beats `(4,1,1)` at `n = 6, d = 4` | Finite test |
| `sigma_blind` has no clean extremal law while `sigma_E` does | **ONE(comparison)** on `3 <= n <= 24`; general case **OPEN** | Finite test, complete enumeration |
| Priority of `sigma_blind` | **ONE(citation)** — arXiv:1210.4775, arXiv:2006.04242 | Located |
| Priority of `sigma_E` | **NONE found after a stated single-pass search** | Not a novelty claim |
| Applied corollary "uniform binning is worst" | **restricted**: holds under partial, total and idempotent priors; **fails** under bijective priors | Finite test |

## 10. What is owed next

1. A real literature review for `sigma_E`, beyond one search pass. Until then no
   novelty is claimed.
2. **The total-map and idempotent-map classes.** §8d and §8e prove the law for
   the uniform prior over *partial* maps. The total-map class is a different
   measure and the proof does not transfer: the factor function there is not
   `1 + sum n_j^k`. The conjecture survived to `n = 18` and deserves the same
   treatment — find its factor function and ask whether it is log-convex.
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
not establish novelty — Section 8d proves a statement, which is a different thing
from proving that nobody has proved it before.

The extremal law is now a theorem **for every arity, for the uniform prior over
partial maps, and for nothing else**. The bijective, injective-partial and
fixed-domain-size counterexamples of Section 5.2 are unaffected by the proof and
still stand: they are statements about different operation classes, and in those
classes the law is false. A proof under one prior is not a proof under all
priors, and the applied corollary still carries its regime.
