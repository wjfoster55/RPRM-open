# Literature review: partition-preserving transformation monoids, and where `sigma_E` sits

**Date** 17 September 2026, overnight shift.
**Purpose** settle the priority question that `FRAGILITY.md` had been carrying as
`NONE-after-a-stated-single-pass-search`. One search pass is not a review. This
is the review.
**Verdict in one line** the count is **not new** — it is a corollary of a
published theorem — the domain condition is **not new** and already has a name,
and the extremal law is the only part for which a serious search found no
published counterpart. **No first-ness is claimed anywhere in this file.**

Reproduce the arithmetic with `python -I -B tools/fragility_literature.py`.

---

## 0. What was being asked about

Fix a finite set `X`, `|X| = n`, and a partition `C` into `m` blocks of sizes
`n_1, ..., n_m`. For **partial** maps `t : X -> X` two conditions were in play:

**Condition A — successor agreement only.** For `x, y` in the same block and
*both* in `dom(t)`, `t(x)` and `t(y)` lie in a common block. No constraint on
where `t` is defined.

```text
sigma_blind(C) = prod_i ( 1 + sum_j [ (n_j + 1)^{n_i} - 1 ] )
```

**Condition B — Condition A plus enabledness (RPRM's O05).** Additionally, each
block is either wholly inside `dom(t)` or wholly outside it.

```text
sigma_E(C) = prod_i ( 1 + sum_j n_j^{n_i} )
```

---

## 1. Source table

| Source | Object counted | Total / partial | Domain condition | Formula | How verified |
|---|---|---|---|---|---|
| Pei 1994, *Semigroup Forum* 49, 49–58 | introduces `T(X,P)` | total | n/a | none (structure) | **UNVERIFIED** — paywalled; attribution from three secondary reference lists |
| Pei 2005, *Comm. Algebra* 33(1) | `T_E(X)`, regularity, Green's | total | n/a | none | abstract only |
| Araújo–Schneider, arXiv:0807.1214 | rank of `T(X,P)`, uniform | total | n/a | rank only | PDF read |
| Araújo–Bentz–Mitchell–Schneider, arXiv:1404.1598 | rank of `T(X,P)`, **arbitrary** partition | total | n/a | rank only | PDF read |
| **Cicalò–Fernandes–Schneider, arXiv:1210.4775** | partial maps preserving a **uniform** equivalence | **partial** | **none** = Condition A | `(m(n+1)^n − m + 1)^m` | **PDF read** |
| **Sarkar–Singh, arXiv:2006.04242**, *Comm. Algebra* 49(1) 2021, 331–342 | `T(X,P)`, **arbitrary** finite partition | **total** | n/a | `prod_i ( sum_j m_j n_j^{n_i} )^{m_i}` | **PDF read** |
| Pei–Zhou 2009, *Adv. Math. (China)* | `P_E(X)`, arbitrary `E` | **partial** | **none** = Condition A | **no count** — Green's, regularity, abundance | abstract only (CNKI) |
| Fernandes 1998, *Semigroup Forum* **56**, 418–433, DOI 10.1007/PL00005955 | introduces **P-stable** partial permutations | partial, injective | **union of blocks** | not seen | **NOT OBTAINED** — no preprint; author's own publication page lists the citation with no file. Definition read only as restated in arXiv:1905.11489. **Attribution not verified from primary** |
| Caneco–Fernandes–Quinteiro, arXiv:1905.11489 | `POI_{k×m}`, P-stable *and* P-order-preserving partial permutations | partial, injective | **union of blocks** | `sum_t C(k,t)^2 (m!)^t` | PDF read |
| Sarkar–Singh, *Semigroup Forum* 2021 | `Γ(X,P)`, blocks map **onto** blocks | total | n/a | yes | publisher text read |
| Sarkar–Singh, arXiv:2310.19414 | `T_{S(I)}(X,P)`, character in a prescribed `S(I)` | total | n/a | **no cardinality** | abstract read |

A methodological note that belongs in the record: during this review a search
engine's auto-generated summary produced **incorrect formulas twice** — once
inserting Stirling numbers into Sarkar–Singh's theorem, once asserting that
uniform partitions *maximise* the count, which is the opposite of the truth.
Every row marked "PDF read" comes from source text.

---

## 2. A correction to our own citation

`FRAGILITY.md` and the thesis-defence document both attributed arXiv:1210.4775 to
**Fernandes and Quinteiro**. That is wrong. It is **Cicalò, Fernandes and
Schneider**, *Partial transformation monoids preserving a uniform partition*. The
Fernandes–Quinteiro paper is a different one — *The cardinal of various monoids
of transformations that preserve a uniform partition*, BMMS 35(4) 2012 — and it
concerns **total** maps with order and orientation constraints. Both earlier
documents are corrected.

The CFS definition, verbatim from Section 2:

> "Given an equivalence relation E on Ω we say that a partial transformation α
> **preserves** E if for all i, j ∈ Dom α such that (i, j) ∈ E we have that
> (iα, jα) ∈ E."

That is Condition A exactly: the quantifier ranges over `Dom α` and nothing
constrains the domain. Their Theorem 1.1(i) gives `|PT_E| = (m(n+1)^n − m + 1)^m`
for a **uniform** equivalence with `n, m >= 2`. Our `sigma_blind` reproduces it in
every case computed, which is what our earlier 22-case check was checking.

**For non-uniform partitions no published count of Condition A was found.** The
object exists in print for arbitrary equivalences — Pei–Zhou's `P_E(X)` — but
that work is about Green's relations, regularity and abundance, not cardinality.

---

## 3. The finding that downgrades us: `sigma_E` is a corollary

Sarkar–Singh Theorem 6.1 counts **total** partition-preserving maps for an
arbitrary finite partition. Regrouped over individual blocks rather than size
classes it reads

```text
|T(X,P)| = prod_i sum_j n_j^{n_i}
```

which is `sigma_E` **with the `1 +` deleted from each factor**. The `1 +` is not
decoration — it is the sink.

> **Adjoin-a-sink.** Let `*` be a new point and `P' = P + {{*}}` a new singleton
> block on `X + {*}`. The standard bijection "undefined ↦ `*`" carries
> Condition-B partial maps on `(X, P)` exactly onto the total maps in
> `T(X + {*}, P')` that fix `*`. A block either maps into a block of `P`, or is
> sent wholesale to `*` — and `{*}` is itself a block, which is precisely what
> enabledness buys. The block `{*}` has `n+1` possible images, one of which fixes
> `*`, so
>
> ```text
> sigma_E(P) = |T(X + {*}, P + {{*}})| / (n + 1).
> ```

**Verified here, not taken on trust.** The size-class and per-block forms of
Theorem 6.1 agree on all 914 profiles with `n <= 16`; `|T(X,P)|` agrees with
brute-force enumeration of all total maps on every profile with `n <= 6`; and the
adjoin-a-sink identity holds exactly on all 507 profiles with `n <= 14`. Worked
example: `sigma_E(3,3) = 3025`, `|T(X+*, (3,3,1))| = 21175`, and `21175 / 7 = 3025`.

> **Disposition: the closed form `sigma_E` is a corollary of published work.**
> Not a new enumeration. The honest description is "apparently unwritten, but
> immediate from Sarkar–Singh Theorem 6.1", and the right citation practice is to
> cite Sarkar–Singh for the count and Fernandes for the condition.

The same trick does **not** rescue Condition A. There a block maps into
`B_j ∪ {*}`, which is not a block of `P'`, so `sigma_blind` is a genuinely
separate computation — which is where its inclusion–exclusion shape comes from.

---

## 4. The condition is not new either: it is "P-stability"

Fernandes (1998) introduced exactly the domain requirement, for partial
permutations. From Caneco–Fernandes–Quinteiro, verbatim:

> "α is **P-stable** if X_{i_x} ⊆ Dom(α) and X_{i_x}α = X_{i_xα}, for all
> x ∈ Dom(α); and **P-order preserving** if i_x ≤ i_y implies i_{xα} ≤ i_{yα},
> for all x, y ∈ Dom(α)"

The first clause is "if a point is in the domain, so is its whole block" — our
enabledness condition, under a name that has been in print for 25 years. These
monoids matter there because they generate the pseudovariety `NO` of normally
ordered finite inverse semigroups.

The difference in scope is real but narrow: P-stability appears **only for
injective, order-preserving** partial maps, and always bundled with `onto`-a-block
rather than `into`-a-block. For general non-injective partial maps with saturated
domain, the search found nothing.

Searches that returned nothing relevant: "saturated domain", "block-saturated",
"P-saturated" partial transformation; "domain is a union of blocks/classes" with
transformation semigroup; partial + partition-preserving + non-uniform. The arXiv
abstract search `"uniform partition" AND cat:math.GR` returns exactly five
papers, only one about partial maps. Citation lists of both key papers contain no
partial or non-uniform follow-up — every descendant of Sarkar–Singh is a
total-map variant.

**OEIS: no hits.** Searched `81,3025,263169`; `2197,3025,46657`;
`2197,3025,3885,5733,5929`; `1548,600,1728,3126`; and CFS's own published table
`289,16129,1560001`. All empty. The only relevant hit is **A014566** (`n^n + 1`),
the degenerate one-block case. CFS's published order is not indexed either, which
suggests this corner is simply not in OEIS rather than that our object is exotic.

**Structural observation, ours, not from a source.** Condition B is closed under
composition (if `s` maps block `B` into `B'`, then `B'` is wholly in or wholly
out of `dom(t)`, so `B` survives or dies as a unit), its idempotent partial
identities are the `id_D` for `D` a union of blocks, and these form a semilattice
isomorphic to the Boolean lattice `2^m`. That makes it a **left restriction
submonoid of `PT_X`**. No paper was found identifying it this way.

---

## 5. Extremal results: none found, and this is where our work actually sits

**No extremal or majorisation result was found for any of these monoids.** The
extremal literature surfacing on these terms — Hwang–Rothblum and
Chang–Chen–Guo–Hwang–Rothblum on Schur-convex bounded-shape partitions,
Anily–Federgruen on structured partitioning — is about partitioning *numbers*
into parts, not about counting partition-preserving maps. The partition-semigroup
literature studies **rank** as a function of shape (Araújo–Bentz–Mitchell–Schneider
give the exact rank of `T(X,P)` for arbitrary `P`); it does not appear to study
**order** as a function of shape at all.

**And our proof covers the published object, not only ours.** The proof in
`FRAGILITY.md` §8d–8e needs exactly one property: the factor function is a sum of
exponentials, hence log-convex. Compare:

| monoid | factor function | sum of exponentials? | exchange lemma |
|---|---|---|---|
| `T(X,P)` — Sarkar–Singh, **published** | `sum_j n_j^k` | yes | **holds**, 0 failures in 42,903 exchanges |
| `sigma_E` — enabledness | `1 + sum_j n_j^k` | yes | **holds**, 0 failures |
| `sigma_blind` — successor only | `sum_j (n_j+1)^k − (m−1)` | **no**, minus a constant | **fails**, 66 failures |

So the extremal law, with the same four-line proof, is a statement about
**Sarkar–Singh's `T(X,P)`** — an object that is in the literature, is counted
there, and for which this review found no published extremal result. That is a
considerably better position than a statement about an RPRM-internal count, and
it costs nothing: the proof is unchanged.

An independent computation run during the review agrees with ours in every
respect, including the failure: it found `sigma_blind`'s smallest counterexample
at `n = 11, m = 9`, where `(2,2,1,1,1,1,1,1,1)` gives `38^2 · 12^7 = 51,741,130,752`
against `(3,1,1,1,1,1,1,1,1)`'s `120 · 12^8 = 51,597,803,520`. That is the same
cell our own priority run reported as the first disagreement, reached by a
different route.

---

## 6. Verdicts, graded

| Question | Verdict | Grade |
|---|---|---|
| Is Condition A's count published? | **KNOWN**, for uniform partitions — CFS Theorem 1.1(i). **Not found** for non-uniform | Located, PDF read |
| Is Condition B's count published? | **VARIANT / not new.** Not found stated anywhere, but it is a one-line corollary of Sarkar–Singh Theorem 6.1 via adjoin-a-sink, verified here | Written derivation + exact finite test |
| Is the enabledness condition new? | **KNOWN.** The condition is in the literature as *P-stability*, for injective order-preserving partial maps; not found for general partial maps. Its attribution to Fernandes 1998 is **secondary testimony only** | Definition quoted from Caneco–Fernandes–Quinteiro; Fernandes 1998 **not obtained** |
| Is the extremal law published? | **NONE FOUND after a real search**, for any of these monoids. This is not a novelty claim | Search recorded above |
| Is the extremal law true? | **ONE(theorem)** for `sigma_E` and for `T(X,P)`, uniform partial-map prior, every arity. **False** under bijective priors | Written proof, §8d–8e |

**What would overturn the "none found" rows.** The Chinese-journal literature
here — *Advances in Mathematics (China)*, *J. Guizhou Normal Univ.*, *Xinyang
Normal Univ. J.* — is poorly indexed and was largely inaccessible; a counting
result could be hiding there.

### Second pass on the three unobtained papers (same night)

The three papers flagged as "not obtained" were chased again. The outcomes
differ, and two of them change what this file may assert.

| Paper | Outcome | Effect |
|---|---|---|
| **Sun**, BMMS **36**(1) 2013, 179–192 | **OBTAINED IN FULL**, open access via EMIS | Counts `OP_E(X)`, `O_E(X)` and their idempotents — Fibonacci `F_{2n}` appears in the idempotent formulas — for a **uniform** partition only. No shape dependence, no extremal statement. **Does not overturn anything** |
| **Pei**, *Semigroup Forum* **49** 1994, 49–58, DOI 10.1007/BF02573470 | **NOT OBTAINED** — Springer paywalled, the EuDML copy at `eudml.org/doc/135333` timed out repeatedly. **zbMATH review obtained in full** (Zbl 0804.20046) | The review quotes the definition verbatim — `T_E(X) = {f ∈ T_X : (f(a),f(b)) ∈ E ∀(a,b) ∈ E}` — and summarises the contents as lattices of `T`-equivalences and α-congruences, with a result on exactly six α-congruences. **No cardinality of any kind.** Overturn risk now low, and for a stated reason rather than by assumption |
| **Fernandes**, *Semigroup Forum* **56** 1998, 418–433, DOI 10.1007/PL00005955 | **NOT OBTAINED.** No preprint anywhere; the author's own publication page lists the citation with no file | **The P-stability attribution is downgraded to "not verified from primary".** It rests entirely on the restatement in Caneco–Fernandes–Quinteiro, arXiv:1905.11489. The *condition* is certainly in the literature — that paper defines and uses it — but that Fernandes 1998 is where it originates is secondary testimony |

**A bibliographic correction.** This file previously gave Fernandes 1998 as
*Semigroup Forum* **58**. It is **volume 56**. Both the author's publication page
and the DOI record agree. Corrected above and in the note.

**A structural observation that explains the absence, without appealing to
novelty.** Almost every paper in this area *fixes a uniform partition by
hypothesis* — Cicalò–Fernandes–Schneider, Araújo–Schneider,
Caneco–Fernandes–Quinteiro, Fernandes–Quinteiro and Sun all assume `m` blocks of
size `n`. Under that hypothesis the shape is determined by `(m,n)` and the
extremal question **cannot be posed at all**. The order for an arbitrary shape
appears to become available only with Sarkar–Singh in 2021. So "no published
extremal result" is less surprising than it first looks: the question is only
three years old in askable form. That is an explanation, not a priority claim.

---

## 7. Papers to read next, in priority order

1. **Pei & Zhou**, *Semigroups of Partial Transformations Preserving an
   Equivalence Relation*, Adv. Math. (China) 2009 — Condition A for arbitrary
   `E`. The one paper most likely to already contain a count we did not find.
2. **Fernandes**, *Normally ordered inverse semigroups*, Semigroup Forum 58
   (1998), 418–433 — where P-stability originates. Needed to cite the condition
   correctly rather than via a restatement.
3. **Araújo, Bentz, Mitchell & Schneider**, arXiv:1404.1598 — rank of `T(X,P)`
   for arbitrary `P`; the model for how shape-dependence is handled in this
   literature, and it ends with open problems.
4. **Sarkar & Singh**, arXiv:2006.04242 — already read, but the source to cite.
5. **Caneco, Fernandes & Quinteiro**, arXiv:1905.11489 — the accessible
   P-stability source.
6. **L. Sun**, *Combinatorial results for certain semigroups of transformations
   preserving orientation and a uniform partition*, BMMS 36(1) 2013 — not
   obtained; the title suggests counting results that could overlap.
7. **Dolinka & East**, arXiv:1407.3312, and **Dolinka, East & Mitchell**,
   arXiv:1504.02520 — idempotent enumeration in `T(X,P)`.

---

## 8. What this changes in the other documents

- The closed form is **a corollary of published work**, not a new count. Stated
  in `FRAGILITY.md` §4 and in the README.
- The enabledness condition is **P-stability**, named in 1998. Cited.
- arXiv:1210.4775 is **Cicalò–Fernandes–Schneider**, not Fernandes–Quinteiro.
  Corrected everywhere.
- The extremal law is restated as a result about **`T(X,P)` as well as
  `sigma_E`**, because that is where it is checkable against the literature.
- Nothing here is claimed as first. The strongest admissible phrasing remains
  *no published counterpart found after the search recorded in this file*.
