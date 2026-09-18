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
   families of §9. Hostile cases in §4 and the lift hostiles of §9–§10. Grade:
   written proof of the pair trichotomy and of FIVE-visibility of the first
   two clauses; finite test for the censuses, for O09 kernel agreement, and
   for agreement of the §9 occupancy with the §10 typed residue definitions.
   Unbounded carriers, `NONDET`, `KERNEL`, n=4 two-action, and eight-Tile
   Board/Atlas remain OPEN. The three-cell Board of §11 is a finite test.
   The dual O05 witness fiber of §12 is a finite test on those cells and
   the 845 family; it is not FIVE.future.

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

- `NONDET` complete obstruction on a declared family. §14 is a first probe
  (new carrier, handful of hostiles). Overnight's relational/unknown-map
  count was not run; it stays OPEN.
- `KERNEL` complete obstruction (pushforward mass, not support).
- Applied `rho` of last night's count on one published reduced model of a
  partial system.
- Characterisation of the cells where the classical successor-only monoid
  fails last night's extremal law.
- Lean of the pair trichotomy (the 20 declarations are not enlarged here).
- An eight-Tile Board or Atlas that uses this oracle as a Tile. The
  three-cell instance of §11 is a finite test, not that construction.
- `NONDET`/`KERNEL` distinguishing-witness fibers. The §12 instrument is
  `PARTIAL` only.
- Four-state two-action machines with the same constructor: 2^4·5^8 =
  6 250 000 machines, too large for this cut.
- n≥5 one-action, and n=4 with a larger action alphabet. Occupancy is OPEN.
  The §10 types already partition every finite profile, so n=5 does not
  force a new name.

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
The five occupied residue names are typed in §10: the §9 census occupancy
matches those definitions, rather than the names being fitted after
browsing. The three-cell Board of §11 uses this oracle as a Tile; it is
not an Atlas. The dual O05 witness fiber of §12 is closed on those
cells and on the 845 family; FIVE.future NONE is not that fiber. The 24
delayed FIVE pairs of §13 are successor `partial_land`, not a 2×2 ghost.

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

Occupancy is a census readout, not a premise. The five occupied names are
typed in §10; jumper-count splits of `crowd` and one-vs-both splits of
`multi` are occupancy readouts, not further names.

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
carriers. Frozen receipt: [LIFT_CENSUS.json](LIFT_CENSUS.json). The five
occupied residue names are typed in §10 against a match null.

## 10. Typed residue definitions

The five names `split`, `escape`, `crowd`, `multi`, `mixed` are types of
ghost fold, not leftover buckets from browsing the §9 census. Profile is a
first-class port. The 2×2 of §7 is the unique-pair stay-jump-land case of
the same lattice.

1. **Carrier.** Ghost folds of finite deterministic partial machines, as in
   §1. Equality of states is the declared state equality. A ghost fold is a
   pair `(machine, C)`.
2. **Ports.** Supplied: that pair. Missing: which residue type, if any.
   Readout: one of the five names, or a §7 2×2 name, or `unclassified`.
3. **Operation.** `PARTIAL`, diagnostic. Residue types live only on
   successor ghosts; observation and enabledness failures are FIVE-visible.
4. **Receiver.** O05 successor disagreement on merged pairs, the block-size
   profile of `C`, and the set of local witnessing names of actions on a
   unique size-2 block.
5. **Fiber.** Each type is the complete preimage of that name. Inverse: the
   flags are pairwise exclusive, so a named ghost determines a unique type.
   NONE/ONE/MANY is not used per machine; the solved fiber is occupancy.
6. **Coverage, hostile, grade.** Coverage: the two lift families of §9.
   Hostile: the unique-pair slice still occupies 1632 `split`/`escape`/`mixed`
   ghosts. Grade: written definitions and exclusion; finite test that the
   §9 occupancy equals those fibers. n=5 occupancy is OPEN; it is not a
   missing name.

**Definition (profile kind).** Let `π` be the sorted block-size tuple of `C`.

- `crowd` if some part has size ≥3;
- else `multi` if at least two parts have size 2;
- else `unique_pair` if exactly one part has size 2;
- else `other`.

These four labels partition every finite partition.

**Definition (local witnessing name).** For a size-2 block `M={x,y}` and an
action `a`: if `a` is not enabled at both points, `not_successor`; if
`C(T_a x)=C(T_a y)`, `agree`; else `a` is a *witness*. A witness with both
images outside `M` is `split`. A witness with exactly one stayer in `M` and
one jumper landing on a size-1 class `s` is: `partial_land` if `a` is
undefined at `s`; `sink_*` / `return_*` as in §7 if `T_a s` is `s` or in
`M`; `escape` if `T_a s` is defined and in a third class; `wide_landing` if
the landing class is not size 1. Anything else is `unclassified`.

**Definition (crowd).** A ghost fold whose profile kind is `crowd`.

**Definition (multi).** A ghost fold whose profile kind is `multi`.

**Definition (split).** A ghost fold of unique-pair profile whose set of
witnessing names is exactly `{split}`.

**Definition (escape).** A ghost fold of unique-pair profile whose set of
witnessing names is exactly `{escape}`.

**Definition (mixed).** A ghost fold of unique-pair profile whose set of
witnessing names has cardinality at least 2.

The four 2×2 names are the unique-pair ghosts whose witnessing set is a
singleton in `{sink_self, sink_partner, return_self, return_partner}`.

**Proposition (pairwise exclusive).** Profile kinds are exclusive, so
crowd, multi, and unique-pair types are exclusive. On unique-pair, mixed
is a witnessing set of size ≥2 and is exclusive from every singleton
label, including split, escape, and the 2×2. Grade: written.

**Proposition (unique-pair ghost has a witness).** A unique-pair ghost has
exactly one merged pair, which fails successor, so some action is a
witness. Grade: written.

**Proposition (crowd jumpers on n=4 one-action).** Profile `(4)` is
one-block, hence not a ghost. The only crowd profile on four states is
`(3,1)`. All-stay and all-jump into the unique outside class give successor
agreement, hence are not ghosts. So every n=4 one-action crowd ghost has
jumper count 1 or 2. Grade: written; finite test. This is a corollary, not
a new name.

**Proposition (no definitional hole at n=5).** Every finite profile is
crowd, multi, unique-pair, or other. A ghost needs a merged pair, so a
block of size ≥2. Size ≥3 is crowd; several size-2 and no larger is multi;
one size-2 and no larger is unique-pair. So n=5 occupancy is OPEN but not a
missing name. Grade: written.

**Match null, frozen against the §9 census:**

> On the four-state one-action family and the three-state two-action
> family, every ghost fold named `split`, `escape`, `crowd`, `multi`, or
> `mixed` satisfies the typed definition of that name, and every ghost fold
> satisfying one of those five definitions receives that name. The five
> definitions are pairwise exclusive. Unclassified is NONE.

**Readout.** The match null is **true**. Occupancy is unchanged from §9:
`(split, escape, crowd, multi, mixed) = (624, 384, 1152, 1152, 624)`.
Unique-pair hostile: 7056 unique-pair ghosts, of which 1632 are
`split`/`escape`/`mixed` (624+384+624). The 2×2 failure is not only
crowd/multi. Hostiles for two-jumper crowd and both-pair multi were built
from the definitions: both remain crowd and multi, not split or mixed.
Do not subtype `mixed` by browsing. Frozen receipt:
[LIFT_CENSUS.json](LIFT_CENSUS.json).

## 11. The oracle as a Tile, on a three-cell Board

This is the smallest honest Board that uses the §1 oracle as a Tile. It is
not an eight-Tile Board and not an Atlas. The withheld question is not a
preinstalled eighth cell.

1. **Carrier, types, equality, admitted context.** One Tile is a pair
   `(machine, C)` as in §1, together with the oracle readouts of §1 and
   §10. Equality of states is the declared state equality. A Board cell is
   a named such pair. This Board has three cells: Manifesto `{p,q,r}`,
   unique-pair `split`, and the numeric 2×2 `sink_self`.
2. **Ports.** Tile ports: machine, summary, obstruction fiber, ghost
   fiber, lift type, profile kind, FIVE.future on merged pairs, O05
   distinguishing-witness fiber, O09 kernel agreement. Board apertures:
   (a) machine and summary revealed, diagnosis withheld; (b) machine
   revealed, summary withheld among set-partitions; (c) lift type revealed,
   cell identity withheld among the three closed Tiles. Correlated missing
   ports stay joint: `split` is a fact of `(machine, C)`, not of the
   machine alone.
3. **Operation.** `PARTIAL`, diagnostic. Same O05 clauses. Enabledness is
   unchanged from §1.
4. **Receiver.** The Tile receiver is the classified obstruction. The
   Board receiver is whether that diagnosis is determined by a proper
   subset of the Tile ports. Future answers and operational updates remain
   distinct, as in O05F versus O05.
5. **Fiber.** Closed Tile: the oracle is a function of `(machine, C)`, so
   aperture (a) is always ONE on a declared pair. Withheld-summary fiber:
   complete set of set-partitions that are ghost folds. Type-among-cells
   fiber: complete preimage of a lift type in the three-cell carrier.
   NONE/ONE/MANY only after that enumeration.
6. **Coverage, hostile, grade.** Coverage: these three machines and every
   set-partition of each (Bell(3)=5, Bell(3)=5, Bell(4)=15). Hostile: the
   unique-pair `split` machine has MANY(6) ghost summaries, including two
   `sink_self`, so unique-pair plus ghost does not force a 2×2 name even
   on one machine. Grade: written uniqueness for Manifesto `{p,q,r}`;
   finite test for all three cells and both apertures. Generality OPEN.

**Definition (Obstruction Tile).** For a declared finite deterministic
partial machine and summary `C`, the closed Tile fills every readout port
from `obstruction_fiber`, `ghost_fiber`, `lifted_ghost_type`,
`distinguishing_witness_fiber`, `shortest_witness` on merged pairs, and
`stable_refinement`. The vacancy is those readouts. The commuting receipt
is that substituting the filled ports reproduces the oracle. FIVE.future
`shortest_witness` is a second receiver and does not fill the O05 witness
port.

**Definition (three-cell Board).** Cells, as closed Tiles:

| Cell | Machine | Declared `C` | Type |
|---|---|---|---|
| `manifesto_pqr` | `{p,q,r}`, `p→p`, `q→r`, `r→r`, constant observation 0 | `C(p)=C(q)≠C(r)` | `sink_self` |
| `unique_pair_split` | `{0,1,2,3}`, `0→2`, `1→3`, `2→2`, `3→3`, constant 0 | `C(0)=C(1)`, `2` and `3` singleton | `split` |
| `sink_self_2x2` | `{0,1,2}`, `0→0`, `1→2`, `2→2`, constant 0 | `C(0)=C(1)≠C(2)` | `sink_self` |

The two `sink_self` cells have equal type and unequal pair names. Equal
value is not equal occurrence.

**Proposition (Manifesto machine determines its ghost summary).** On the
Manifesto `{p,q,r}` machine, among the five set-partitions, exactly one is
a ghost fold. Proof: discrete has no merged pair. Indiscrete is one-block,
so successor agreement is automatic; constant observation and a total map
make it operational. Merge `{p,r}` with singleton `q`: both `p` and `r`
stay in the pair, so successor agrees. Merge `{q,r}` with singleton `p`:
both stay. Merge `{p,q}` with singleton `r`: `p` stays, `q` jumps to `r`,
`r` sinks, observations agree, enabledness agrees, FIVE.future NONE. That
one partition is `sink_self`. Grade: written. The numeric 2×2 cell is the
same argument on `{0,1,2}`.

**Proposition (Tile commuting).** Filling the withheld-summary vacancy of
either three-state cell recovers exactly the declared closed Tile. Grade:
written from the previous proposition; finite test.

**Readout, finite test.** Aperture (a): each declared cell is ONE
successor ghost, O09 discrete, future quotient indiscrete, FIVE.future
NONE. Aperture (b): Manifesto `{p,q,r}` and numeric `sink_self` are ONE
(`sink_self`); the split machine is MANY(6) with occupancy
`(crowd, split, multi, sink_self) = (2, 1, 1, 2)`. On that machine the
summaries named `split` are still ONE, namely the declared cell. Aperture
(c): type `sink_self` is MANY(2 cells); type `split` is ONE. Unique-pair
does not force 2×2: the declared split cell is unique-pair `split`, and
the same machine also hosts two `sink_self` ghost summaries.

This Board does not close an Atlas and does not promote `Tile(X)` to `X`.
Frozen receipt: [BOARD.json](BOARD.json).

## 12. Shortest O05 distinguishing witnesses

This is the dual of the §1 pair fiber: an enabled word, or finite set of
words, that must exist when `C` is not operational. It is not FIVE.future.

1. **Carrier, types, equality, admitted context.** Same machines and
   summaries as §1. A word is a finite tuple of admitted actions. The empty
   word is admitted and is the identity. Equality of words is tuple
   equality. Bool/float atoms remain admission errors.
2. **Supplied ports, missing ports, requested readout.** Supplied: the
   machine and `C`. Missing: the complete O05 witness fiber. Readout: for
   each failing merged pair, the earliest clause and the complete set of
   shortest words that exhibit that clause. FIVE.future's word is a second,
   non-interchangeable readout attached to the same pair.
3. **Operation kind, direction, enabledness.** `PARTIAL`, diagnostic. A
   word is enabled at a state when every prefix stays in the corresponding
   action domain. Observation uses the empty word, which is always enabled.
   Enabledness and successor use length-1 words: enabledness words are
   enabled at exactly one of the pair; successor words are enabled at both.
4. **Receiver.** O05 clauses, not tagged future observations. A successor
   word exhibits `C(T_a x) ≠ C(T_a y)` even if every tagged future
   observation agrees. FIVE.future is attached and must not replace the
   O05 words.
5. **Inverse / complete fiber.** The witness fiber is the complete set of
   failing pairs with their shortest clause-witness words. NONE iff `C` is
   operational. ONE/MANY after that enumeration. A FIVE.future NONE on a
   successor pair is not this fiber being NONE. Per-pair word families may
   themselves be ONE or MANY.
6. **Coverage, hostile, grade.** Coverage: written existence from the §2
   trichotomy; finite test on the three Board cells and every failing pair
   in the 845 family. Hostile: ghost pair, FIVE.future NONE, update still
   fails; also the five-state O08R example, where FIVE.future is
   `("a","a")` and the O05 word is `("a",)`. Grade: written existence;
   finite test for the cells and for non-coincidence with FIVE.future.
   `NONDET`/`KERNEL` witness fibers remain OPEN.

**Definition (clause-witness words).** For a merged pair with earliest
clause `κ`:

- if `κ = observation`, the unique shortest word is the empty word;
- if `κ = enabledness`, the shortest words are the length-1 words `(a)`
  where `a` is enabled at exactly one of the pair, in declared action
  order;
- if `κ = successor`, the shortest words are the length-1 words `(a)`
  where `a` is enabled at both and `C(T_a x) ≠ C(T_a y)`, in declared
  action order;
- if `κ = pass`, the set is empty.

**Definition (distinguishing-witness fiber of `C`).** The complete set of
failing merged pairs together with those word sets. Status NONE/ONE/MANY
follows the pair count, as in §1. The shortlex-least word of a pair is a
derived readout and does not replace the set.

**Proposition (existence).** The witness fiber is empty iff the
obstruction fiber is empty iff `C` is an operational fold. Proof: each
non-`pass` clause names a nonempty set of length-0 or length-1 words by
the same checks as §2. Grade: written.

**Proposition (FIVE.future is a different fiber).** Observation and
enabledness clause-witnesses are FIVE.future ONE, and the shortlex-least
words coincide. A successor clause-witness may have FIVE.future NONE
(ghost) or FIVE.future ONE of a possibly longer word. Returning
FIVE.future NONE as the distinguishing witness of a ghost pair, or
returning a longer FIVE.future word as the O05 successor witness, is an
error: those are a different receiver. Grade: written for the first two
clauses (same as §2); finite test for successor.

**Null, frozen before looking at the three cells' witness fibers:**

> On Manifesto `{p,q,r}`, unique-pair split, and numeric `sink_self`,
> FIVE.future is NONE on the declared merged pair, therefore the O05
> distinguishing-witness fiber of each declared `C` is also NONE.

**Readout.** The null is **false**. Each declared cell is ONE, clause
`successor`, word family ONE(`("a",)`), FIVE.future NONE. The word
`("a",)` exhibits the update failure and is not a FIVE.future word.

**Second null, frozen before the 845 witness comparison:**

> On the `checks/futures.py` 845-machine family, for every failing merged
> pair with FIVE.future ONE, the FIVE.future word equals the shortlex-least
> O05 clause-witness.

**Readout.** The second null is **false**. On the 845 family there are
2578 failing pairs, each with a nonempty O05 word set. FIVE.future ONE
coincides with the O05 word on 2482 pairs (all 1698 observation, all 688
enabledness, and 96 successor). It differs on 24 successor pairs: all
are three-state one-action, and the FIVE.future word is `("a","a")`
while the O05 witness is `("a",)`. The remaining 72 failing successor
pairs are the ghosts: FIVE.future NONE, O05 word still `("a",)`.
Returning the longer FIVE.future word, or NONE, as the O05 witness is
the same error on two sides of successor.

## 13. The 24 delayed FIVE successor pairs

The 24 pairs of §12 are a complete fiber. They are not a leftover bucket
and they are not ghost folds.

1. **Carrier.** Delayed FIVE successor pairs on the 845-machine family: a
   merged pair whose earliest O05 clause is successor, FIVE.future is ONE,
   and the FIVE.future word is not among the O05 clause-witness words.
2. **Ports.** Supplied: those 24 pairs. Missing: obstruction class,
   ghost-fold type, unique-pair local name, and FIVE delay reason.
3. **Operation.** `PARTIAL`, diagnostic. Same O05 clauses as §1.
4. **Receiver.** O05 successor versus FIVE.future. A delay reason records
   why the future word is longer, not a new O05 clause.
5. **Fiber.** Complete occupancy of the a priori names below. NONE/ONE/MANY
   is used only for the solved occupancy of each name.
6. **Coverage, hostile, grade.** Coverage: the 845 family. Hostile: the
   named `partial_land` machine is delayed and not a ghost; Manifesto
   `{p,q,r}` is a ghost and not delayed; the five-state O08R pair is
   delayed by `late_observation`, so that reason is not missing, only
   unoccupied on this family. Grade: written exclusion of ghost/2×2;
   finite test for occupancy.

**Definition (late enabledness).** After the first letter of the FIVE.future
word the tagged observations still agree, and the next letter distinguishes
by `FAIL` versus `OK`.

**Definition (late observation).** After that first letter the tagged
observations still agree, and the next letter distinguishes by two
successful observations.

**Proposition (delayed pairs are not ghosts).** A delayed FIVE successor
pair has FIVE.future ONE, so it is not a ghost pair and `(machine, C)` is
not a ghost fold. The 2×2 names of §7 apply only to ghost folds, so the
ghost-fold type is unclassified. Grade: written.

**Null, frozen before classifying the 24:**

> The 24 FIVE.future/O05 disagreements on the 845-machine family are all
> successor-class ghost folds of one 2×2 type `sink_self`, `sink_partner`,
> `return_self`, or `return_partner`.

**Readout.** The null is **false**. Obstruction class is successor on all
24. Ghost-fold type is NONE: 0 ghosts, 2×2 names occupy 0, unclassified
24. They are the already typed unique-pair name `partial_land`, and the
FIVE delay is `late_enabledness` on all 24.

**Match null, frozen against that occupancy:**

> On the 845-machine family, every delayed FIVE successor pair has
> obstruction class successor, is not a ghost fold, has unique-pair local
> name `partial_land`, and has FIVE delay `late_enabledness`. Unclassified
> delay is NONE.

**Readout.** The match null is **true**. Occupancy
`(partial_land, late_enabledness) = (24, 24)`. `late_observation` occupies
0 on this family and is occupied by the five-state hostile. Frozen receipt:
[DELAYED.json](DELAYED.json).

This Board Tile now carries the witness port. Frozen receipts:
[WITNESS.json](WITNESS.json) and the `o05_witness` field of
[BOARD.json](BOARD.json).

## 14. First NONDET probe

The §1 oracle's domain is `rprm.futures.Machine`: deterministic partial
maps. A successor-set table is a new required type. That is
`OPEN_NEW_CARRIER`, not a stretch of the PARTIAL trichotomy. FIVE.future
is not defined on that carrier and does not decide set-valued descent.

1. **Carrier.** Finite total nondeterministic machines: every state has a
   successor set, possibly empty. Equality of states is the declared state
   equality. A proposed summary `C` is as in §1.
2. **Ports.** Supplied: the nondet machine and `C`. Missing: the complete
   obstruction against set-valued O05. Readout: observation or
   `successor_blocks`, or `pass`. There is no enabledness clause.
3. **Operation.** `NONDET`, diagnostic. Deadlock is the empty successor
   set, not a missing domain.
4. **Receiver.** Observation and successor *sets of C-blocks*, as in
   `docs/operations.md`. Not tagged-word FIVE.future.
5. **Fiber.** Complete set of failing merged pairs. NONE/ONE/MANY after
   that enumeration. This cut enumerates only named hostiles, not a family.
6. **Coverage, hostile, grade.** Coverage: written admission boundary of
   the PARTIAL oracle, plus eight named hostiles. Hostile: Manifesto as
   singleton-valued nondet is ONE(`successor_blocks`) while FIVE.future
   cannot run; deadlock versus a singleton is `successor_blocks`, not
   enabledness. Grade: written `OPEN_NEW_CARRIER` for the old domain;
   finite test for the hostiles. A complete family census remains OPEN.

**Definition (NondetMachine).** States, actions, total observation, and a
total table of frozensets. Empty set admitted. Branching admitted.

**Definition (NONDET earliest clause).** Observation if present answers
differ. Else `successor_blocks` if some action has `C[N_a(x)] ≠ C[N_a(y)]`.
Else `pass`.

**Proposition (PARTIAL oracle does not admit this carrier).**
`obstruction_fiber` requires `type is Machine`. `Machine` requires
transition targets to be admitted states, not successor sets.
`shortest_witness` requires `Machine`. Grade: written from the constructors.

**Null, frozen before the hostiles:**

> The existing PARTIAL obstruction oracle already classifies finite
> nondeterministic machines: empty successor sets are enabledness, and
> FIVE.future decides every `successor_blocks` failure.

**Readout.** The null is **false**. The PARTIAL oracle rejects
`NondetMachine` (`OPEN_NEW_CARRIER`). Deadlock is `successor_blocks`.
FIVE.future is `OPEN_NEW_CARRIER` on this carrier. Manifesto-as-nondet is
ONE(`successor_blocks`). Oracle: [nondet.py](nondet.py).
