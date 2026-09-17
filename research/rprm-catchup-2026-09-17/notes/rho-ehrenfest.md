# `rho` on a published reduced model: the Ehrenfest lumping

*A bounded calculation, and a conjecture it produced and then destroyed.
17 September 2026.*

> **Reading order.** §1–2 are a bounded calculation on a textbook lumping and
> stand. §3 records a conjecture this file previously advanced and now
> **refutes**, with the minimal counterexample. Nothing here is a law about
> `rho`; the only proved monotonicity in this project is the one in
> `extremal-order-TXP.md`, and it is about `sigma_E`, not about `rho`.

---

## Why this model

`rho = sigma_E / sigma_blind` is the fraction of successor-compatible operations
on a partition that also satisfy the block-saturated domain condition — in RPRM
terms, the fraction of literature-admissible reductions that enabledness keeps.
Computing it on a shape invented for the purpose would prove nothing, so it is
computed here on a partition nobody chose to make a point.

The **Ehrenfest urn chain** on the hypercube `{0,1}^d` is strongly lumpable by
Hamming weight. This is textbook (Kemeny–Snell) and long predates anything here.
The lumping is a real published state-space reduction, and its block shape is
binomial — `C(d,0), ..., C(d,d)` — hence strongly non-uniform, which is the regime
where shape matters at all.

**What this computes:** a property of that partition's *shape*, under the uniform
prior over compatible operations.

**What this does not compute:** anything about Ehrenfest dynamics. The Ehrenfest
chain is one operation. `rho` describes the space it sits in. Nothing below says
the model is fragile, robust, well-chosen or badly chosen.

---

## 1. `rho` on the lumping

| `d` | states `n` | blocks `m` | shape | `rho` |
|---:|---:|---:|---|---:|
| 2 | 4 | 3 | (2,1,1) | 0.4667 |
| 3 | 8 | 4 | (3,3,1,1) | 0.1634 |
| 4 | 16 | 5 | (6,4,4,1,1) | 0.08919 |
| 5 | 32 | 6 | (10,10,5,5,1,1) | 0.05529 |
| 6 | 64 | 7 | (20,15,15,6,6,1,1) | 0.04531 |

At `d = 6`, **about 4.5%** of the successor-only operations on that partition also
satisfy the domain condition. The condition is not a mild extra hypothesis on this
shape; it discards roughly nineteen operations in twenty, and the discarded
fraction grows with `d`.

That is the whole content of `rho` as a number, and it is worth being blunt about
its size: the gap between the two counts is not a technicality that a reader can
mentally round away. Two papers counting "the partition-preserving partial maps"
with and without the domain condition are counting objects that differ by more
than an order of magnitude by `d = 6`.

## 2. How much the shape is worth

All shapes of `n` into `m` parts, with the published binomial shape located among
them by `|T(X,P)|`:

| `d` | `n` | `m` | # shapes | rank of binomial (1 = max) | `tau(binom)/tau(min)` | `tau(max)/tau(min)` |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 4 | 3 | 1 | 1 | 1 | 1 |
| 3 | 8 | 4 | 5 | 3 | 3.06 | 24.4 |
| 4 | 16 | 5 | 37 | 22 | 90.6 | 1.15 × 10⁶ |

The binomial shape sits in the middle, not at either extreme — as it should,
being neither balanced nor maximally unequal.

Three shapes in the same cell, all with **32 states and 6 blocks**, differing only
in shape:

| shape | provenance | `\|T(X,P)\|` | `rho` |
|---|---|---:|---:|
| (27,1,1,1,1,1) | dominance maximum | 1.49 × 10⁴⁶ | 0.3746 |
| **(10,10,5,5,1,1)** | **the published Ehrenfest lumping** | 1.75 × 10³⁴ | 0.05529 |
| (6,6,5,5,5,5) | dominance minimum | 1.50 × 10²⁸ | 0.004816 |

A factor of **10¹⁸** in the order of the monoid, from shape alone, at fixed state
count and fixed block count. Whatever else the extremal theorem is, it is not a
statement about a marginal effect.

## 3. A conjecture that lived four minutes, and its counterexample

An earlier revision of this file recorded an observation: `rho` appeared to be
strictly increasing along the dominance order in every case computed — 1,084
exchanges over all shapes with `n <= 15`, zero failures. It was filed as a
conjecture at finite-test grade, with the note that it does **not** follow from
the extremal theorem, since the theorem gives monotonicity of the numerator while
the denominator is precisely the quantity shown to be non-monotone.

**It is false.** The search range was too small by two.

### The counterexample

At `n = 17`, `m = 3`, the exchange `(9,4,4) -> (9,5,3)` moves *up* the dominance
order and moves `rho` *down*:

| | `(9,4,4)` | `(9,5,3)` |
|---|---:|---:|
| `sigma_E` | 19,413,329,297,612,328 | 21,437,143,071,365,448 |
| `sigma_blind` | 127,011,712,746,964,992 | 140,481,534,821,857,272 |
| `rho` | **0.152846764111** | **0.152597585857** |

Exactly,

```
rho(9,5,3) - rho(9,4,4) = -858504691969960082028925 / 3445343558652498113608593664
```

which is negative. This is the **smallest** counterexample: an exhaustive sweep
of every shape and every dominance-increasing exchange finds none at `n <= 16`,
and exactly one at `n = 17`.

Both closed forms were re-derived by brute-force enumeration of the two monoids
on small shapes before being trusted at this size.

### Why it was missed, and why it is not a fluke

The margin is tiny. Across this exchange `sigma_blind` grows by a factor
1.106052 and `sigma_E` by 1.104249 — the numerator does rise, exactly as the
theorem requires, and the denominator simply rises about **0.16% faster**. A
near-miss that narrow needs room to develop, which is why nothing appears below
`n = 17`.

It is not an isolated accident. Failures proliferate with size:

| `n` | 17 | 18 | 19 | 20 | 21 | 22 |
|---|---:|---:|---:|---:|---:|---:|
| failing exchanges | 1 | 5 | 18 | 35 | 58 | 94 |

Restricted to `m = 3` and pushed to `n <= 40`, **18.0%** of all upward exchanges
lower `rho` (791 of 4,388). This is endemic, not marginal.

### The failures have a shape

Every one of the 211 failures in the `n <= 22` sweep — 211 of 211, none
otherwise — has a **block strictly larger than both exchanged parts**. A big
block sits out the exchange while two middling blocks trade. Consistently:

```
(9,4,4) -> (9,5,3)     (13,3,3) -> (13,4,2)     (11,3,3,1) -> (11,4,2,1)
(10,4,4) -> (10,5,3)   (12,4,3) -> (12,5,2)     (8,4,4,1,1) -> (8,5,3,1,1)
```

This predicts that `m = 2`, where no spectator block can exist, never fails —
and it does not, over all two-block shapes to **`n = 160`** (6,241 exchanges,
zero failures). Balanced shapes, which have no large spectator either, also
survive the whole sweep.

The mechanism guess that motivated the search was wrong too, and cleanly so. It
proposed that `rho = prod_i g(n_i)` with `g = f_E/f_B` would inherit the main
theorem's two-step proof if `f_B` were log-**concave** — the mirror of the
log-convexity that drives `sigma_E`. `f_B` is not log-concave (first failure at
`(2,1)`, `k = 4`), `g` is not log-convex, and the pointwise base comparison fails
as well. All three legs were tested and all three broke, which is why the
conjecture was attacked rather than written up.

### It fails at higher arity too

At arity 2 the same thing happens, with the same signature: `(5,3,3) -> (5,4,2)`
is an upward exchange that lowers `rho`. So this is not an artefact of arity 1.

### And it fails next door to the model in §1

Three of the Ehrenfest shapes above have upward exchanges that *lower* `rho`:

| `d` | shape | an upward exchange that lowers `rho` | `Δrho` |
|---:|---|---|---:|
| 5 | (10,10,5,5,1,1) | (10,10,6,4,1,1) | −3.04 × 10⁻⁴ |
| 6 | (20,15,15,6,6,1,1) | (20,16,15,6,5,1,1) | −2.49 × 10⁻⁴ |
| 7 | (35,35,21,21,7,7,1,1) | (35,35,22,21,7,6,1,1) | −6.42 × 10⁻⁵ |

The three-row table in §2 is still correct as arithmetic, and still shows `rho`
falling down the dominance order at `d = 5`. It simply is not evidence of a law;
the immediate neighbourhood of that very shape contains a violation.

### One prediction that did hold

The 32 exchanges in range where `sigma_blind` *decreases* — the classical count's
own non-monotonicity — **all** have `rho` increase, without exception. That was
forced: a falling denominator under a provably rising numerator can only raise
the ratio. The hostile region was always the opposite one, where the denominator
rises faster than the numerator by a fraction of a percent, and that is exactly
where the conjecture died.

### Status

| Statement | Grade |
|---|---|
| `rho` strictly increasing along dominance, general shapes | **FALSE.** Counterexample `(9,4,4) -> (9,5,3)`, exact arithmetic, minimal in `n` |
| `rho` strictly increasing when `m = 2` | **Conjecture**, finite test only: all two-block shapes, `n <= 160`, zero failures. Exactly the spectator-free case. No proof offered |
| `rho` strictly increasing on balanced shapes (`max - min <= 1`) | **Conjecture**, finite test only, `n <= 22` |
| Every failure has a block strictly larger than both exchanged parts | **Finite observation**, 211 of 211, `n <= 22`. Not proved, and not known to be more than a description of this range |
| Failure at arity 2 | **Exact counterexample**, `(5,3,3) -> (5,4,2)` |

Reproduction: `tools/rho_mechanism.py`, `tools/rho_counterexample.py`,
`tools/rho_boundary.py`. Exact integer and rational arithmetic throughout; the
comparison is done by cross-multiplying integers, never by evaluating a float.

---

## Reproduction

`tools/rho_ehrenfest.py`, exact integer and rational arithmetic throughout.

## References

J. G. Kemeny and J. L. Snell, *Finite Markov Chains*, Van Nostrand 1960 — strong
lumpability and the Ehrenfest example.

M. Sarkar and S. N. Singh, *On certain semigroups of transformations that preserve
a partition*, Comm. Algebra **49** (2021), 331–342, for `|T(X,P)|`.

S. Cicalò, V. H. Fernandes and C. Schneider, arXiv:1210.4775, for the
domain-free partial monoid that `sigma_blind` generalises to arbitrary shape.
