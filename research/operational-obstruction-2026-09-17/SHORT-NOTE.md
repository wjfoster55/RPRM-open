# Complete O05 obstruction fibers — short note

17 September 2026. Not the 74-page thesis. Not BSD. Not a first-ness claim.

Replay, from `C:\github\RPRM-open-obstruction`:

```powershell
python -I -B research/operational-obstruction-2026-09-17/verify.py
```

Branch `research/new-project-operational-obstruction`. Typed claim: `research/operational-obstruction-2026-09-17/THEORY.md`.

## What the oracle returns

Given a finite deterministic partial machine and a proposed summary `C`, the
oracle returns the **complete** obstruction of `C` against O05: every merged
pair labelled by its earliest failing clause `observation`, `enabledness`,
or `successor`, or `pass`. Disposition is NONE, ONE, or MANY only after that
enumeration.

This is not core’s first REJECT witness. It is not FIVE.future.

**Evidence.** Written trichotomy (clauses are exclusive and exhaustive on
finite tables). Finite test on every partition of the project’s 845-machine
futures family, plus the four-state one-action and three-state two-action
lift families. Not Lean.

## Ghost folds

A ghost fold is future-sufficient and still not operational: FIVE.future is
NONE on every merged pair, and some pair fails successor. Future answers and
update laws are different receivers.

**Null, frozen before the 845 census:** ghosts are only the Manifesto
three-state picture (`0→0`, `1→2`, `2→2`, merge `{0,1}`) and its
relabelings. **False.** MANY(72).

On that three-state one-action slice a 2×2 names all 72, unclassified none:

| Type | Count |
|---|---:|
| `sink_self` | 12 |
| `sink_partner` | 12 |
| `return_self` | 24 |
| `return_partner` | 24 |

`sink_self` is the Manifesto sink/jump. The leftover 60 are not one type.

**Evidence.** Written listing 3·2·2·3·2=72. Finite census. Shape null “the
60 occupy exactly one leftover name” is **false**.

## The 2×2 does not lift

**Null, frozen before looking:** those four names still classify every ghost
on four-state one-action (10 000 machines) and three-state two-action
(32 768 machines). **False.**

Combined ghosts: **9 360**. The 2×2 keeps **5 424**. The other **3 936**
need five extra types. Unclassified none.

| Type | Combined |
|---|---:|
| 2×2 names | 5 424 |
| `split` | 624 |
| `escape` | 384 |
| `crowd` | 1 152 |
| `multi` | 1 152 |
| `mixed` | 624 |

Those five names are typed definitions (profile first), not leftover
buckets. Match null against the census: **true.** Unique-pair still has
**1 632** split/escape/mixed, so the 2×2 failure is not only crowd/multi.

**Evidence.** Written definitions and exclusions; exhaustive finite census.
Not a theorem about n=4 two-action (6.25 million; OPEN) or unbounded
carriers.

## Tile and Board

One Tile is the oracle on a declared `(machine, C)`. A three-cell Board
runs it on Manifesto `{p,q,r}`, unique-pair `split`, and numeric
`sink_self`, with withheld versus revealed ports.

With the summary withheld: Manifesto is ONE; the split machine is MANY(6)
and still hosts `sink_self`. Type `sink_self` occupies two cells (equal
type is not equal occurrence). Not an eight-Tile Board. Not an Atlas.
Generality OPEN.

**Evidence.** Written uniqueness for Manifesto `{p,q,r}`. Finite test for
all three cells and both apertures.

## O05 witness versus FIVE.future

When `C` is not operational, a nonempty O05 word fiber exists. Observation
uses the empty word. Enabledness and successor use length-1 words.
FIVE.future is a different receiver.

**Null, frozen before looking:** FIVE.future NONE on Manifesto / split /
`sink_self` implies the O05 witness fiber is NONE. **False.** Each cell is
ONE successor word `("a",)`.

On the 845 family, FIVE.future ONE matches the O05 word except **24**
successor pairs (`("a","a")` vs `("a",)`).

**Null, frozen before classifying those 24:** they are successor-class
ghost folds of one 2×2 type. **False.** Obstruction class successor;
ghost-fold type NONE; local name `partial_land`; FIVE delay
`late_enabledness` on all 24.

The five-state O08R hostile is delayed by `late_observation` (both sides
`OK`, different values). That reason is not missing; it is unoccupied on
the 845 family.

**Evidence.** Written existence of the O05 word from the trichotomy. Finite
test on the three cells, the 845 family, and the 24-pair fiber. FIVE.future
does not decide operationality.

## What this does not claim

Not a new minimization theory. Not Lean. Not a first-ness claim about
bisimulation or Moore refinement. O05 is the ordinary operational-fold
test for deterministic partial systems; the work is the complete fiber,
the ghost census, and the separation from FIVE.future.

`KERNEL` complete obstruction remains OPEN. First NONDET-LTS contract: `research/operational-obstruction-2026-09-17/CONTRACT-NONDET.md` (observation / enabledness / `successor_blocks`; deadlock is not disabled; the 845 census does not lift).

## Receipts

`CENSUS.json`, `LIFT_CENSUS.json`, `BOARD.json`, `WITNESS.json`,
`DELAYED.json` under `research/operational-obstruction-2026-09-17/`.
