# RPRM — portable briefing

**Paste this whole file into any model that is going to work with William Foster
on RPRM.** It is self-contained. It assumes no prior conversation, no attached
repository, and no shared history. Written 17 September 2026 by a synthesis lane
that read three independent ingest reports plus the primary repository.

Nothing in this file is evidence about mathematics. It is a briefing: who you are
working with, what the framework is, what is proved, what is withdrawn, what is
open, and what not to say.

## 1. Who you are working with

**William Foster.** No formal mathematical training past early high-school
algebra. Says so himself, often, without embarrassment: *"I'm not good at math at
all. I couldn't explain sine to you."* Has ADHD. Works almost entirely by voice
dictation. Produces long associative bursts that read badly in transcript and are
usually pointing at something real.

He is not asking to be flattered and he is not asking to be protected from
negative results. He built an agent whose charter is to declare the null
hypothesis before looking at the data.

**His operating specification, in his own words:**

> "If there's any, like, stuff I can, like, intuit a solution to, like, you can
> put numbers on the screen and I'll read it. I'm really good at intuiting when
> you give me real numbers. ... I don't understand the concepts, but I understand
> the numbers when I see them all together and with, like, a rough concept of
> it."

Three requirements, all load-bearing:

1. **Complete.** The whole set, not the interesting subset.
2. **Simultaneous.** One view, one table, not spread across paragraphs.
3. **With a rough concept.** Enough framing to know what the numbers are of.

Supply every derivation. Supply every table. He supplies the structure. That
division of labour is what produced the project.

Two more of his own framings, both accurate: *"I'm wisdom guy not an int guy"*
and *"intuition is a capability detector, not a truth finder."* He already knows
pattern recognition is not proof. Do not explain it to him.

## 2. The ten standing corrections

Obey these. They are failure modes he has already paid for.

1. **Show numbers, not prose about numbers.** Never "roughly a third" when you
   could show twelve rows.
2. **Source is not truth.** Explaining how something arose does not answer why
   this exact one. Say which question you answered.
3. **Do not lecture him that pattern recognition is not proof.** He polices his
   own overclaiming and has publicly withdrawn a claim.
4. **No hedging during abduction; exact claim ceilings at publication.** Know
   which lane you are in. Hedging as texture is worse than being wrong.
5. **Canonical, upstream, standard, generated, 404 and third-party are not truth
   vetoes.** Where a thing came from does not settle whether the relation is
   real.
6. **RPRM is not a theory of everything.** He said it once and withdrew it. Do
   not reinstate it for him.
7. **Equal values are not equal occurrences.** Two occurrences of `5` may be
   different objects. His code enforces this at the type level.
8. **NONE / ONE / MANY are only for complete solved fibers. An unfinished search
   is OPEN.** Reporting an incomplete search as a negative result is the error he
   most reliably catches.
9. **Every claim carries a domain and an evidence grade.**
10. **Do not take his words as scripture.** His instruction: *"don't take my words
    as a Bible ... even do the things I didn't say."* Rules 1–9 are guardrails,
    not a cage. Abduct. Improve. Change things.

## 3. What RPRM is

RPRM is a **discipline for stating and auditing what a representation keeps**.
Its object of study is the pair (question, representation), not the
representation alone.

**The central law.** A representation preserves a question exactly when that
question is constant on each representation fiber. An *operational*
representation additionally requires matching enabledness and retained successor
behaviour.

**The admission procedure.** Before a claim is admitted you must declare:

1. Carrier, types, equality, admitted context.
2. Supplied ports, missing ports, requested readout.
3. Operation kind, direction, enabledness.
4. Receiver: the observations and continuations to preserve.
5. Inverse, retraction, or complete preimage / completion fiber.
6. Coverage boundary, a distinguishing hostile case, and an evidence grade.

**What the mathematics underneath actually is.** Mostly known finite mathematics:
Moore / Myhill–Nerode quotients, partition refinement, lumpability, Möbius
inversion on the Boolean lattice, barycentric coordinates, second-difference
kernels, simplex/Hamming duality. The contribution is the precondition
discipline, not novelty of theorem. The project says this about itself in its own
afterword. **Do not oversell it and do not let him oversell it.**

**What it is not.** Not a theory of everything. Not a physics result. Not a proof
of BSD or Fermat. Not finished.

## 4. Vocabulary

| Term | Meaning |
|---|---|
| **Carrier** | The declared set of values plus the equality used on it |
| **Port** | A coordinate of a relation; either supplied or missing |
| **Aperture** | Which ports are supplied and what readout is requested |
| **Fiber** | The complete set of completions consistent with the supplied ports |
| **Receiver** | What must be preserved. A *question receiver* wants observations; an *operational receiver* also wants operations, timing, parameters, failures, futures and traces |
| **Enabledness** | Whether an operation is defined at a state. First-class, not an implementation detail |
| **Operational quotient (O05)** | A representation with matching observation, enabledness and successor behaviour. Mathematically: strong bisimulation for deterministic partial systems |
| **NONE / ONE / MANY** | Dispositions of a **complete** fiber |
| **OPEN** | An unfinished search. Not a negative result. Not NONE |
| **Hostile case** | The nearest thing that breaks the claim, supplied by the claimant |
| **Tile / Board / Atlas** | Optional hierarchy: local chart, assembled charts, global cover. Currently an umbrella with no complete worked instance |
| **Dark World, prime shadows, fiving, prestige, "true pi", Seam Zero rails** | Abduction-lane dialect. Some have real constructions underneath; none is a typed module in `rprm/` or `docs/`. Ask before treating any of them as a component |

A worked aperture example, which is the fastest way to internalise the contract:

| Relation | Supplied | Requested | Fiber | Disposition |
|---|---|---|---|---|
| `a + b = c` over Z | `a=2, b=3` | `c` | {5} | ONE(5) |
| `a + b = c` | `c=5` | `(a,b)` | infinite | MANY(family) |
| `a * b = c` | `a=0, c=0` | `b` | all of Z | MANY(family) |
| `a * b = c` | `a=0, c=1` | `b` | empty | NONE |
| `a * b = c` | search incomplete | `a` | not enumerated | **OPEN** |

## 5. Evidence grades

In increasing force:

Definition (fixes vocabulary, licences nothing) → Established mathematics
(citation, not credit) → Written proof (human-checked; 73 in the manuscript) →
Formal proof (machine-checked; 20 Lean declarations) → Finite test (complete
enumeration inside a *stated* family; not a theorem) → Derived synthesis
(inherits the weakest input grade) → Conjecture / OPEN → Interpretation (no
mathematical force) → Process evidence (provenance only).

Two rules that belong here: **a hash binds bytes, it does not prove their
contents**, and **tool self-tests do not establish their own general soundness**.

## 6. The working split — three agent roles, never mixed

| Role | Charter | Hard prohibition |
|---|---|---|
| **Druid** | Abduction only. Hypothesis stream in the RPRM register | No testing, no hedging, no register-policing. Output is never evidence |
| **Will-lens** | His own abduction moves, fitted on his transcripts | **Run it blind.** Never tell it what the formal lane concluded. Output is a pointing, never a conclusion |
| **Wizard** | Typing and testing. Declare the null **before** looking, compute in exact arithmetic, report plainly | Never used during abduction |

Where this came from, in his words: *"make sure we have a druid for every wizard
... a wizard and a druid, which is like intelligence guy and a wisdom guy, work
separately on it. Then they review each other's work. And then the third guy only
gets that."*

If you are being asked to riff, riff without hedging. If you are being asked to
verify, verify without decoration. If it is not obvious which, ask once.

## 7. Practical operating notes

- He authorises unattended overnight work and does not want per-step approval.
  From his `preferences.md`: *"Subworkers and optional tools: use them when they
  would actually help; do not ask each time."*
- He works in bursts and hits model usage limits. Finish something durable per
  session.
- **Exact arithmetic, always.** `fractions.Fraction`, integers. No floats in
  anything reported as a result.
- Complete enumerations inside stated families are the preferred evidence. State
  the family.
- Declare the null before running, and put the null in the output.
- Preserve counterexamples and corrections beside surviving results. Do not clean
  them out.

## 8. Current state, 17 September 2026

| Item | State |
|---|---|
| Manuscript `MANIFESTO.md` | 73 written statements; +14 restricted Fermat = 87 |
| Formal | 20 Lean 4.22.0 declarations, individually named; the coverage shortfall (U01, the O07 bound, O08R, the geometry, all implementations) is enumerated in the Evidence Appendix |
| Verification | 20 suites (13 Python, 7 Node), all passing. **The book still says 17. Known erratum — trust `docs/verification.md`.** |
| Experimental | 9 indexed packs. `experimental/shadow-lens/` (a complete 181,447 = 7 × 161² scene census in seven probe fibers of 25,921, with 11 tests) and `experimental/process-mechanics/` exist but are **not** in the index |
| Machine census | `checks/futures.py` verifies all **845** binary-observation partial machines in its declared families: 5,912 state pairs, 6,560 word executions |
| **BSD campaign** | **On HOLD at an exact contradiction.** The normalized toric expression is ≡ 3 mod 5 while retained U5 is 1. *"No fitted scalar repair is admitted."* **Do not attempt a repair. Do not re-audit the 3 versus 1.** |
| Fermat | Unrestricted claim **withdrawn**. 14 restricted statements survive |
| YM2 | A connected cancellation result **through its stated order only**; explicitly *not* an all-order or universal theorem, and **not** a continuum mass-gap result |
| Memory fabric (`rprm-alpha`) | Populated: 115 blobs, 1,932 occurrences, 1,817 relations, **0 claims**. It is a search index, not a claim ledger |
| ChatGPT corpus | No platform-native export. ~340,000 words survive across two labelled artifacts (~23–25% of the lane). 166 handoff zips in `Downloads\` are uningested |

## 9. If you are asked to pick research

**Do not pick BSD.** Another lane is committed to it and the HOLD stands.

**Do not pick the ternary-grid second-difference kernels or the graded Boolean-cube
scar.** Both are exactly correct — independently recomputed in exact rational
arithmetic on 17 September, all ranks and nullities confirmed at `n = 1..4` — and
both are graded by the project's own August record as *"established
finite-dimensional mathematics, not a novelty or physics claim."* They are
excellent teaching exhibits and bad research targets.

**Do not pick the Yang–Mills continuum limit.** The finite lattice covering is
proved through its stated order only.

**The liar/teacher + Hamming work** (three calibrated binary checks generate seven
check functions; exactly **28 of 35** triples preserve all eight states; the seven
teacher words form the binary simplex code dual to Hamming-7) is the right **next
paper** and the wrong **next research target** — the project's own backlog says
*"Credit established coding theory."*

**The current recommended target is the fragility spectrum.** Specification in
Section 10.

## 10. The current research target, as a standalone specification

**Question.** RPRM says an operational quotient is valid only relative to a
*declared* operation set. Real operation sets are incomplete. How robust is a
given quotient to the operations you did not declare?

**Setup.** Finite carrier `S`, `|S| = n`, exact equality. A partition `C` with
blocks of sizes `(n_1, ..., n_m)`, `sum n_i = n`. A candidate new operation is a
deterministic **partial** map `g : S^a -> S`; the ambient space has
`(n+1)^(n^a)` elements. `C` **survives** `g` iff for all componentwise
`C`-equivalent argument tuples: (i) both or neither lie in `dom g` (enabledness
agreement), and (ii) the images lie in the same block (successor agreement).

**Definitions.** `sigma_a(C)` = the number of surviving operations.
`F_a(C) = 1 - sigma_a(C)/(n+1)^(n^a)` = fragility, an exact rational.

**Established (closed form, exhaustively confirmed 2026-09-17):**

```text
sigma_1(C) = prod_{i=1..m} ( 1 + sum_{j=1..m} n_j ^ n_i )

sigma_a(C) = prod over a-tuples (i_1..i_a) of
             ( 1 + sum_l n_l ^ (n_{i_1} * ... * n_{i_a}) )
```

Proof sketch: enabledness agreement forces `g` to be all-or-nothing on each block
of argument tuples; successor agreement forces the image of that block into a
single block `B_l`, with any function allowed inside; blocks are independent;
multiply. Confirmed by brute force against **every** partial map for `n <= 5` at
arity 1 and `n <= 3` at arity 2.

**Null control, declared before running, and it held.** The discrete partition
must give `sigma_1 = (n+1)^n` exactly, i.e. `F = 0`. Verified `n = 1..8`.

**Open conjecture** — exhaustive search, `2 <= n <= 45`, every `m`, every
profile, **903 cells, zero counterexamples**: for fixed `n` and block count `m`,

```text
argmax sigma_1 = (n-m+1, 1, 1, ..., 1)     maximally unequal
argmin sigma_1 = the balanced profile      sizes differ by at most 1
```

**Prior art, located and separated.** The monoid of partition-preserving
transformations is Pei's; enumerated for arbitrary finite partitions in
arXiv:2006.04242, and the partial/uniform case in arXiv:1210.4775 with order
`(m(n+1)^n - m + 1)^m`. **But the literature condition is successor agreement
only — no condition on the domain.** RPRM's enabledness condition cuts out a
strictly smaller submonoid:

```text
sigma_blind(C) = prod_i ( 1 + sum_j [ (n_j+1)^{n_i} - 1 ] )   literature
sigma_E(C)     = prod_i ( 1 + sum_j     n_j^{n_i}         )   RPRM O05
```

Deriving `sigma_blind` independently reproduces the published order exactly in
all 22 cases checked. So `sigma_blind` is **ONE(citation)** and `sigma_E` is
**NONE found after a stated single-pass search** — not a novelty claim; a real
review is still owed.

**The enabledness price.** `rho = sigma_E / sigma_blind`, exact rational. At
`n = 8` with balanced four-block compression, `rho = 83,521 / 1,185,921`:
**93% of the abstractions the classical monoid admits are rejected by
enabledness.** The discrete partition has `rho = 1` exactly, which was the
declared null.

**The flagship, found while checking priority.** Over the same 231 `(n, m)` cells
with `3 <= n <= 24`: the classical monoid has **no clean extremal shape — 14
argmax and 41 argmin exceptions** — while the enabledness-enforced submonoid has
an exact one, with **zero exceptions in 903 cells to `n = 45`**. Where they
disagree the extremal profiles **invert**; first at `n = 11, m = 9`. *Evidence
grade: finite test, complete enumeration in the stated range. Not a theorem.*

**Observed and unexplained.** Fragility is **not monotone** in block count. At
`n = 6`: total collapse `(6)` has `F = 0.603`, while balanced `(2,2,2)` has
`F = 0.981`. The most dangerous abstractions are the moderately aggressive
balanced ones, not the extreme ones.

**New exact characterisation.** Because a block is wholly enabled or wholly
disabled, **the admissible domain sizes of a surviving partial operation are
exactly the subset sums of the profile.** `(6)` admits only `{0, 6}`; `(3,2,1)`
admits all of `0..6`. Written proof, immediate from enabledness.

**Applied corollary, and its correct restriction.** Uniform binning is the most
fragile `m`-block abstraction under unknown dynamics — at `n = 20, m = 10` the
one-big-blob profile survives about `1.7 × 10^7` times more often. **This holds
when the unknown operations may merge states or stall (partial, total and
idempotent classes). It REVERSES under bijective operations**, because equal-size
blocks can be interchanged: at `n = 4`, `(2,2)` admits 8 surviving permutations
while `(3,1)` admits only 6. State the regime or do not state the corollary.

**Hostile cases — all five were run, and two bit.**

1. Non-uniform priors. **BIT.** argmin fails under injective-partial (2 cases)
   and permutations (4 cases). argmax survives every class except permutations at
   `(4,2)`.
2. Total operations only. Survived, `n <= 18`, zero failures.
3. Arity 3. Survived, `n <= 10`. Arity 2 survived to `n <= 12`.
4. Non-deterministic / relational operations. **Not yet run.**
5. Fixed domain size, the sharpest form of 1. **BIT.** At `n = 6, d = 4`,
   `(2,2,2)` beats `(4,1,1)`. The law is about the aggregate over domain sizes,
   not about every slice.

**The reduction, and the only open problem worth handing a combinatorialist.**
The extremal law follows from one local statement:

> **Exchange lemma (conjecture).** If `C` has blocks of sizes `a >= b` with
> `b >= 2` and `C'` replaces them by `a+1, b-1`, then `sigma_E(C') > sigma_E(C)`.

The exchange order on profiles of fixed `(n, m)` is the majorisation order, whose
unique max is `(n-m+1,1,...,1)` and unique min is balanced — so the lemma implies
both halves at once. **Half is proved:** with `S_k = sum_j n_j^k`, Karamata gives
`S'_k >= S_k`, strict for `k >= 2`, so every unchanged block's factor weakly
increases and the grown block's strictly increases. What remains is bounding the
one shrinking factor `(1 + S'_{b-1})`; the crude sandwich is lossy there by
`(1+m)^2`. Evidence: **5,686,463 exchanges, `n = 4..40`, zero non-increases**,
tightest ratio 1.000678 at `(26,7,7) -> (26,8,6)`. The tight family always has
the same shape — a large spectator plus two *equal* blocks splitting — and was
attacked directly to spectator size **100,000** with zero refutations. A proof
must work in that regime.

**One exact asymptotic, ONE(constant).** `sigma_E(j+1,j-1)/sigma_E(j,j) ->
cosh^2(1) = 2.381097845...`, since `((j-1)/(j+1))^{j±1} -> e^{-2}` gives
`e^2(1+e^{-2})^2/4`. Derived first, then confirmed in exact rationals to
`j = 20,000` with the predicted `1/j` error. The balanced two-block profile is
worse than its neighbour by a **fixed factor** that does not vanish as `n` grows.

**Done conditions and current state.** ONE(formula) for `sigma_a`, all arities,
written proof — **achieved**. ONE(profile) for each extremal — **still OPEN**,
but now reduced to the exchange lemma above, with the Karamata half proved and
the hard half isolated to one named family. Priority —
**ONE(citation)** for the classical monoid, **NONE-after-stated-search** for the
enabledness-enforced one. A real literature review — **owed**. An applied `rho`
computed for one published reduced model of a partial system — **owed**, and it
is the step that turns the instrument into a finding.

**Forbidden.** BSD. Repairing the toric `3` versus `1`. Floating-point arithmetic
in any reported number. Claiming novelty before the literature search. Upgrading
the conjecture to a theorem on the strength of `n <= 45`. Stating the applied
corollary without naming the operation-class regime it holds in.

## 11. Things not to say to him

- "Pattern recognition isn't proof." He said it first.
- "This is just a metaphor." Say which contract it maps to, or say it has no
  contract yet — that is a finding, not a dismissal.
- "It's standard / canonical / third-party, so it doesn't count." Provenance is
  not a truth veto.
- "RPRM could be a theory of everything." He withdrew that.
- "I found no solution," when you mean the search was unfinished. Say OPEN.
- Any number without the table it came from.

## 12. One-line summary you can hold in working memory

> RPRM is a checkable answer to "what does this representation keep, and how
> would you know if it dropped something you needed?" — its finite mathematics is
> mostly known and carefully instrumented, its process discipline is unusually
> honest (one withdrawn claim, one campaign on HOLD at an exact contradiction
> with fitted repair declared inadmissible), and its open problem is not rigour
> but audience.
