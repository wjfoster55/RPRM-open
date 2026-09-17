# Complete O05 obstruction fibers

Research note, 17 September 2026. Evidence grades below are **definition**,
**written proof**, and **finite test**. Not Lean. Not a Manifesto theorem
number. Not last night's `T(X,P)` count.

## 1. Task record

1. **Carrier, types, equality, admitted context.** Finite deterministic
   partial machines as in `rprm.futures.Machine`: state tuple of exact atoms,
   named actions, total observation table, per-action partial maps. Equality
   is the declared state equality. Bool/float atoms are admission errors.
   A proposed summary `C` is a total map from states to exact atoms.
2. **Supplied ports, missing ports, requested readout.** Supplied: the
   machine and `C`. Missing: the obstruction of `C` against O05. Readout:
   each unordered merged pair labeled by its *earliest* failing clause
   `observation`, `enabledness`, or `successor`, or `pass`.
3. **Operation kind, direction, enabledness.** `PARTIAL`. Direction is
   diagnostic: we do not execute a preferred input/output split of the
   original relation; we inspect merged pairs. Enabledness is membership in
   each action's domain, and is a first-class clause.
4. **Receiver.** Observation, enabledness, and retained successor summaries
   as in O05. A second receiver, FIVE.future, is the tagged-word observation
   language including `FAIL`. These receivers are not interchangeable.
5. **Inverse / complete fiber.** The obstruction fiber is the complete set of
   merged pairs whose earliest clause is not `pass`. Disposition is NONE,
   ONE(pair), or MANY(family) only after that enumeration. The ghost-fold
   subfiber is the complete set of merged pairs with FIVE.future NONE and
   clause `successor`. The O09 repair is the unique coarsest operational
   fold refining `C`; it is not a fitted scalar.
6. **Coverage, hostile case, evidence grade.** Coverage: written trichotomy
   for every finite deterministic partial machine; exhaustive census of every
   set-partition of every machine in the `checks/futures.py` 845-machine
   family. Hostile cases in §4. Grade: written proof of the pair trichotomy
   and of FIVE-visibility of the first two clauses; finite test for the
   census and for O09 kernel agreement. Unbounded carriers, `NONDET`, and
   `KERNEL` remain OPEN.

## 2. Closed claim

**Definition.** For states `x ≠ y` with `C(x) = C(y)`, the *earliest O05
clause* is:

1. `observation` if `O(x) ≠ O(y)`;
2. else `enabledness` if some action is defined at exactly one of `x, y`;
3. else `successor` if some enabled action sends them to different `C`-blocks;
4. else `pass`.

**Proposition (trichotomy).** These four labels partition the merged-pair
carrier. Proof: the clauses are checked in order; each is a decidable
equality on a finite table; exactly one label is returned.

**Proposition (FIVE-visibility of the first two clauses).** If the clause is
`observation`, the empty word distinguishes the pair. If it is
`enabledness`, the one-letter word of a mismatched action distinguishes them
by `FAIL` versus `OK`. Proof: that is the tagged observation used by
`observe_word`.

**Corollary (ghost pairs are successor failures).** A merged pair with
FIVE.future NONE cannot have clause `observation` or `enabledness`. If it
fails the one-step check, the clause is `successor`. A one-step `pass` pair
need not be future-equivalent: later disagreement can live in a successor
block that `C` has not split yet. If *every* merged pair is `pass`, then `C`
is an operational fold and every merged pair is future-equivalent.

**Proposition (one-block and two-state controls).** If `C` has a single
block, successor agreement is automatic, so a ghost pair is impossible. If
there are at most two states, the only merged partition is indiscrete, hence
again no ghost pair. Proof: one block gives a unique successor label; the
n=2 indiscrete case is that one-block case.

**Proposition (empty obstruction iff O09 does not split).** On a finite
deterministic partial machine, `C` is an operational fold iff every merged
pair is `pass` iff the least stable refinement of `C` has the same kernel as
`C`. Proof: O05 is the conjunction of the three clauses on merged pairs;
O09 terminates at the coarsest stable refinement of `(C, O)` (written O09).
If `C` is already stable it is not split; if some clause fails, refinement
splits that class.

**O08R (recorded, not new).** The minimum tag alphabet repairing a question
`Q` relative to `C` is `max_K |Q[K]|` over `C`-fibers, or `0` on the empty
carrier. Proof: `docs/operations.md` O08R. Hostile: that minimum can be `1`
(question already descends) while the O05 obstruction is nonempty.

NONE/ONE/MANY are used only for complete fibers of merged pairs. An
unfinished search is not this module.

## 3. Null, declared before the census

The following sentence was frozen before enumerating the 845-machine family
and its partitions:

> In the `checks/futures.py` 845-machine family, every partition that is
> future-sufficient on its merged pairs is an operational fold, except the
> Manifesto three-state example (constant observation, `a: 0→0, 1→2, 2→2`)
> and its state relabelings.

The Manifesto example is already known to be a ghost fold; the null says it
and its relabelings exhaust the family. The census may confirm or refute
that. The named hostiles in §4 were checked before the census ran.

## 4. Hostile cases

| Name | What it must expose |
|---|---|
| Manifesto `{p,q,r}` | FIVE.future NONE, obstruction ONE(successor), O09 discrete, future quotient indiscrete |
| Two observation failures | Complete fiber MANY(2); `deterministic_quotient` returns one witness contained in that fiber |
| n=2 enabledness | Obstruction ONE(enabledness), ghost NONE, FIVE.future ONE |
| One-block cycle | Ghost NONE; indiscrete total constant-obs map is operational |
| Five-state O08R | Min tag alphabet 1 for `O` after pairing `O` with `O∘T`, O05 successor MANY, FIVE.future ONE(`aa`) |
| Empty machine | O08R = 0, obstruction NONE |
| Kernel equal support | Three states, merged pair, equal support `{0,2}` but masses `(1/2,1/2)` vs `(1/4,3/4)` into the two blocks; `stochastic_quotient` REJECT `pushforward_mass`. Out of this PARTIAL fiber. One-block kernels cannot witness the distinction. |
| Bool atom | Admission error |

## 5. Census readout

The null of §3 was declared before enumeration. It is **false**.

| Quantity | Value | Disposition |
|---|---:|---|
| Machines in the futures family | 845 | complete declared family |
| Machine–partition cases | 3217 | Bell partitions of each state set |
| Operational folds (obstruction NONE) | 1239 | complete |
| Ghost folds | 72 | MANY(72), listed in [CENSUS.json](CENSUS.json) |
| Manifesto self-loop/jump relabelings | 12 | 3 singleton choices × 2 jump choices × 2 observation labels |
| Remaining ghost folds | 60 | not that pattern |
| Ghost successor pairs | 72 | one merged pair each |
| FIVE-visible successor pairs | 120 | successor failure with a distinguishing word |
| Observation-failing pairs | 1698 | FIVE-visible |
| Enabledness-failing pairs | 688 | FIVE-visible |
| `null_holds` | false | §3 refuted on this family |

Shape of the 72, all of which lie in the three-state one-action slice:

| Shape | Count |
|---|---:|
| Total maps | 72 |
| Constant observation | 72 |
| Singleton is a fixed point | 24 |
| Some merged state is a self-loop | 36 |
| Both (the Manifesto sink/jump pattern) | 12 |

Invariant checks, independent of the null and all passed: no one-block ghost; no n≤2 ghost; every observation/enabledness failure has FIVE.future ONE; every operational fold has FIVE.future NONE on merged pairs and matches the O09 kernel; every ghost fold in this family is a total constant-observation map.

The scientific yield is the negative: treating the Manifesto `{p,q,r}` picture as the only future-sufficient-but-not-updateable compression is false already on the project's own 845-machine family. The complete unexpected family is retained, not repaired.

## 6. OPEN

- `NONDET` complete obstruction (successor *sets* of blocks; deadlock is not
  a separate enabledness port). Overnight's relational/unknown-map count was
  not run; it stays OPEN.
- `KERNEL` complete obstruction (pushforward mass, not support).
- Applied `rho` of last night's count on one published reduced model of a
  partial system.
- Characterisation of the cells where the classical successor-only monoid
  fails last night's extremal law.
- Lean of the pair trichotomy (the 20 declarations are not enlarged here).
- One Tile/Board instance that uses this oracle as a Tile without
  preinstalling the center.
- Families with two or more actions at n=3: the futures census uses one
  action there, so this ghost count does not cover that slice.

## 7. Named types for the 72

The 60 leftover maps are not a new vocabulary problem. On this family's
ghost-fold slice the dynamics are forced, and four ordinary names suffice.

**Definition (2×2 shape).** Let `C` be a ghost fold of a one-action total
map on three states with block profile `(2,1)`. Write `M` for the merged
pair and `s` for the singleton. Successor disagreement forces exactly one
*stayer* `t∈M` with `T(t)∈M` and one *jumper* `j∈M` with `T(j)=s`. The
stayer is `self` if `T(t)=t` and `partner` if `T(t)` is the other point of
`M`. The singleton is `sink` if `T(s)=s` and `return` if `T(s)∈M`. The four
labels are `sink_self`, `sink_partner`, `return_self`, `return_partner`.
Anything else is `unclassified`.

**Proposition (exhaustion on this slice).** Every such ghost fold receives
exactly one of the four labels. Proof: `T` is total on a three-point
carrier, so `T(s)` is `s` or a point of `M`. The stayer's image is itself
or its partner. Those are the two binary choices.

**Proposition (listing).** Choose the singleton (3), the jumper (2), the
stayer kind (2), the image of `s` (3), and the constant observation bit
(2). That product is `3·2·2·3·2=72`. Each such configuration is
future-sufficient (total map, constant observation) and not operational
(one jumper, one stayer). Cell sizes: `T(s)=s` and `self` gives 12;
`T(s)=s` and `partner` gives 12; `T(s)∈M` and `self` gives 24;
`T(s)∈M` and `partner` gives 24. So the listing is
`(sink_self, sink_partner, return_self, return_partner) = (12, 12, 24, 24)`,
with `unclassified=0`. `sink_self` is exactly the Manifesto sink/jump
relabeling.

**Shape null, declared before the shape census:**

> After removing `sink_self`, the remaining ghost folds occupy exactly one
> of the leftover named types `sink_partner`, `return_self`, `return_partner`.

The listing is a written count, not a hope that the 60 are one type. The
null asks the one-type question. Hostiles for the three leftover labels are
the definitional maps in `verify.py`, built before the shape census, not
sampled from `CENSUS.json`.

**Readout.** The shape null is **false**. The listing holds. Unclassified
is NONE.

| Type | Count | What the singleton and the stayer do |
|---|---:|---|
| `sink_self` | 12 | Singleton stays; stayer is a self-loop (Manifesto) |
| `sink_partner` | 12 | Singleton stays; stayer maps to its partner |
| `return_self` | 24 | Singleton returns into the merged pair; stayer self-loops |
| `return_partner` | 24 | Singleton returns into the merged pair; stayer maps to its partner |
| unclassified | 0 | — |

The 60 are MANY(3 leftover types), not one type and not a mess:
`12+24+24`. `sink_self` agreed with the Manifesto-relabeling predicate on
every row. Three leftover occupied types.

## 8. Disposition of the closed fiber

On the declared 845-machine family, the obstruction fiber of every
partition is completely solved (NONE, ONE, or MANY). The ghost-fold
subfiber is completely solved: MANY(72). Those 72 are completely typed by
the 2×2 of §7 (unclassified NONE on this slice). The null of §3 is **false**.
The shape null of §7 is recorded in the census boolean; it is not a theorem
about other families.
