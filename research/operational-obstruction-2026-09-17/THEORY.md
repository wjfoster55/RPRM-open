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
   family, plus the four-state one-action and three-state two-action lift
   families of §9. Hostile cases in §4 and the lift hostiles of §9. Grade:
   written proof of the pair trichotomy and of FIVE-visibility of the first
   two clauses; finite test for the censuses and for O09 kernel agreement.
   Unbounded carriers, `NONDET`, `KERNEL`, and n=4 two-action remain OPEN.

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
- Four-state two-action machines with the same constructor: 2^4·5^8 =
  6 250 000 machines, too large for this cut.
- n≥5 one-action, and n=4 with a larger action alphabet.

The n=3 two-action slice named as OPEN in the first cut is closed as a
finite test in §9.

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
about other families. The 2×2 does **not** lift to the four-state one-action
or three-state two-action families of §9. Those families are exhausted by
the a priori lift vocabulary (unclassified NONE), not by the four names.

## 9. Hostile cut: does the 2×2 lift?

The 2×2 of §7 is a three-state one-action fact. The next hostile is whether
those four names remain a complete typing after one extra state or one extra
action. Same constructor as `checks/futures.py`: binary observations, all
partial maps, all set-partitions.

1. **Carrier.** Four-state one-action machines: 2^4·5^4 = 10_000. Three-state
   two-action machines: 2^3·4^6 = 32_768. Partitions: Bell(4)=15 and
   Bell(3)=5, hence 150_000 and 163_840 machine–partition cases.
2. **Ports.** Supplied: those two families. Missing: the occupancy of each
   a priori lift name on the ghost-fold subfiber. Readout: NONE/ONE/MANY is
   not used per machine; the solved fiber is the complete occupancy table.
3. **Operation.** `PARTIAL`, diagnostic, same O05 clauses as §1.
4. **Receiver.** Same O05 / FIVE.future split. The 2×2 names are a receiver
   on unique size-2 stay-jump-to-singleton blocks. Residues are named from
   the failure modes of that picture, before occupancy is read.
5. **Fiber.** Every ghost fold in the two families is classified. Disposition
   of unclassified is NONE or MANY only after that enumeration.
6. **Coverage, hostile, grade.** Coverage: exhaustive on the two declared
   families. Hostiles in `verify.py` (idle n=4 `sink_self`, split, escape,
   crowd, multi, mixed, and FIVE-visible `partial_land`) were built from the
   definitions, not sampled from the census. Grade: written propositions for
   which residues can occur on which slice, and for the 2 880 = 72·40
   embedding of the old 2×2 into n=4; finite test for occupancy.

**Definition (lift vocabulary).** For a known ghost fold:

- a block of size ≥3 is `crowd`;
- two or more size-2 blocks is `multi`;
- otherwise, on the unique size-2 block, each successor-witnessing action is
  typed as in §7, or `split` if both points leave to different blocks, or
  `escape` if the jumper's singleton leaves to a third class, or
  `partial_land` if that singleton is not in the action's domain, or
  `wide_landing` if the landing class is not a singleton;
- distinct witnessing names across actions are `mixed`;
- anything else is `unclassified`.

Occupancy is a census readout, not a premise.

**Proposition (n=3 forbids split, escape, crowd-ghosts, and multi).** On three
states the only merged profiles that can be ghost folds are `(2,1)`. Proof:
`(3)` is one-block, so successor agreement is automatic; discrete has no
merged pair. On `(2,1)` there is one outside point, so both merged states
cannot jump to *different* blocks (`split`), and the singleton's image is
itself or a point of the merged pair (`escape` is impossible). `multi`
needs two pairs. `crowd` as a ghost needs a size-≥3 block that is not the
whole carrier.

**Proposition (`mixed` needs two actions).** One action supplies at most one
witnessing name.

**Proposition (`partial_land` is FIVE-visible).** If the unique merged pair
has a stayer and a jumper whose landing is undefined, then a one-letter
continuation is `OK` from the stayer and `FAIL` from the jumper. So
`partial_land` cannot be a ghost fold. Grade: written.

**Proposition (`wide_landing` is unreachable after profile-first).** Unique
size-2 plus no larger class forces every other class to be a singleton, so
the landing class has size 1. A larger landing class is already `crowd` or
`multi`. Grade: written.

**Proposition (n=4 one-action 2×2 count).** Each of the 72 three-state
ghost folds, together with a choice of which of four labeled states is the
extra singleton, an extra observation bit, and an extra image in
`{-1,0,1,2,3}`, yields 72·4·2·5 = 2 880 distinct n=4 ghosts of 2×2 type.
The complementary three-set is invariant under the old map (the jumper
lands on the old singleton, which sinks or returns into the merged pair),
so the merged pair never sees the extra state; the restriction is exactly
a §7 ghost. Conversely every n=4 2×2 ghost has profile `(2,1,1)` and
restricts to one of the 72. Grade: written listing; finite test agrees.

Three nulls, frozen before the lift enumeration:

> On the four-state one-action family and the three-state two-action family,
> every ghost fold still receives one of the four names `sink_self`,
> `sink_partner`, `return_self`, `return_partner`.

> On those families, every ghost fold whose block profile has exactly one
> size-2 class and no larger class still receives one of those four names.

> On those families, every ghost fold receives a name in the a priori lift
> vocabulary; unclassified is NONE.

**Readout.** The first two nulls are **false**. The exhaustion null is
**true**. Unclassified is NONE. The 2×2 is a special case of a unique
size-2 stay-jump-land, not a complete typing of the larger families.

| Family | Machines | Cases | Operational folds | Ghost folds |
|---|---:|---:|---:|---:|
| Four-state one-action | 10 000 | 150 000 | 22 206 | 6 192 |
| Three-state two-action | 32 768 | 163 840 | 41 248 | 3 168 |
| Combined | 42 768 | 313 840 | 63 454 | 9 360 |

Four-state one-action occupancy:

| Type | Count | Profile |
|---|---:|---|
| `sink_self` | 480 | `(2,1,1)`; 72·40 embedding |
| `sink_partner` | 480 | `(2,1,1)` |
| `return_self` | 960 | `(2,1,1)` |
| `return_partner` | 960 | `(2,1,1)` |
| `split` | 624 | `(2,1,1)`; both leave to different classes |
| `escape` | 384 | `(2,1,1)`; landing leaves to a third class |
| `crowd` | 1 152 | `(3,1)`; 864 one jumper, 288 two jumpers |
| `multi` | 1 152 | `(2,2)`; 768 one witnessing pair, 384 both |
| `mixed` | 0 | one action |
| `partial_land` | 0 | FIVE-visible |
| `wide_landing` | 0 | unreachable |
| unclassified | 0 | — |

`(2,1,1)` unique-pair ghosts: 3 888 = 2 880 + 624 + 384. The local 2×2
does not exhaust even that slice.

Three-state two-action occupancy, all profile `(2,1)`:

| Type | Count |
|---|---:|
| `sink_self` | 408 |
| `sink_partner` | 408 |
| `return_self` | 864 |
| `return_partner` | 864 |
| `mixed` | 624 |
| split, escape, crowd, multi | 0 |
| `partial_land`, `wide_landing`, unclassified | 0 |

2×2 names occupy 2 544 of 3 168. The leftover 624 are `mixed`: two actions
witness different stay-jump-land names, and FIVE.future still NONE.

Combined 9 360 = 5 424 of type 2×2 + 3 936 residues
(`split`+`escape`+`crowd`+`multi`+`mixed` = 624+384+1 152+1 152+624).

The replacement of the 2×2 is this lift vocabulary, not a fifth binary
bit. Evidence grade: finite test on the two families; not a theorem about
n=4 two-action machines (OPEN: 6.25 million machines) or unbounded
carriers. Frozen receipt: [LIFT_CENSUS.json](LIFT_CENSUS.json).
