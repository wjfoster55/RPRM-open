# `rho` on a published reduced model: the Ehrenfest lumping

*A bounded calculation. Two pages. 17 September 2026.*

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

## 3. An observation that is not a consequence of the theorem

`rho` is *also* strictly increasing along the dominance order in every case
computed — 1,084 exchanges over all shapes with `n <= 15`, zero failures.

This does **not** follow from the extremal theorem. The theorem gives
monotonicity of the numerator `sigma_E`. The denominator `sigma_blind` is *not*
monotone — that is the content of the negative result, which exhibits cells where
it moves the wrong way. A ratio of a monotone quantity to a non-monotone one has
no reason to be monotone, so the observation above is genuinely unexplained
rather than a corollary waiting to be written down.

**Grade: conjecture, finite test only.** Range `n <= 15`, exact integer
arithmetic, 1,084 exchanges. No proof is offered and no mechanism is proposed.
If it survives a wider search it is the more interesting statement of the two,
because it would say the domain condition's *selectivity* — not just the raw
count — is governed by partition shape.

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
