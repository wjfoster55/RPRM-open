# RPRM corpus map + grounding audit

**For William. An honest reconciliation of the RPRM we *used* in the fluid project against
your actual development corpus and your running formalization.**

*Scope and privacy.* This document maps a private RPRM development corpus that William
shared (extracted locally, not in this repo) and reconciles it with the RPRM concepts this
fluid project leaned on (`RPRM_FLUIDS.md`, `SUFFICIENCY_TEST.md`, `PERF.md`). Per the brief,
**no raw corpus files, zips, or large verbatim excerpts are committed** — only short cited
phrases and summaries. Private filesystem locators in the corpus (personal `C:\…` / OneDrive
paths, session JSONL ids) are deliberately **not** reproduced here; artifacts are cited by
name only. The point of the exercise is intellectual honesty ("RPRM must not be BS"), so
where we mislabeled or over-claimed I say so plainly.

*What I read.* The whole `RPRM-CORE-FORMALIZATION-01/` package (the WIP formal core ChatGPT
is building), the six recovered-concept reports, the three `absolute-distinction/` files, and
targeted greps of the ~4.9 MB `will-corpus/` Claude/Codex dialogues for the terms the brief
named. I ran `check_bridge.py` and all four controls (§6). Confidence is stated per claim; it
is highest on the CORE-FORMALIZATION (small, exact, executable) and lower on the recovered
natural-language concepts (real but WIP, by their own labels).

---

## 1. Corpus map

### 1.1 `RPRM-CORE-FORMALIZATION-01/` — the current formal core (most important)

This is the live "connect the recovered concepts with explicit math + executable tests"
package (assignment tag **RCF01**, dated 11 Sep 2026). It is explicitly **development
evidence, not holdout** and does **not** rerun the historical donor code.

| File | What it contains / why it matters |
|---|---|
| `CURSOR_START_HERE.md` | The active assignment: formalize Prestige One, fiving/FIVE_IS_SAFE, and the cube/abduction work, and build one *operation-aware promoted envelope* prototype. Hard semantic constraints (e.g. "Prestige One is not social prestige… not merely a hash"; "the finite fiving model is not F5 arithmetic"). Reads as a careful anti-self-deception spec. |
| `README.md` | Orientation; declares the evidence class and the exact starter command. |
| `CONCEPT_REGISTER.md` | The anti-forgetting ledger: 16 concept IDs (RCF-P1 prestige, F1/F2/F3 fiving, C1/C2 cube/abduction, R1 rails, PI1 pi, AD1 absolute-distinction…), each with intent / source / recovered formal piece / evidence status / "do-not-conflate" list. This is where "meaning" is preserved separately from "evidence." |
| `FORMAL_BRIDGE_NOTE.md` | **The mathematical heart.** Proposes one explicit bridge and states the formal objects/claims we care about (see §1.2). Contains Prop-1/Prop-2 in William's own words and the general retained-site closure proposition our fluid certificate turns out to instantiate. |
| `check_bridge.py` | The executable check (stdlib only, exact `Fraction`/int arithmetic). 12 named cases CB01–CB12 + a coverage validator + 4 controls (see §1.3). |
| `PROTOCOL.json` | The frozen list of required case IDs and the declared control outcomes (`omit/duplicate/unexpected` → nonzero FAIL; `reorder` → PASS). The *contract* the coverage validator enforces. |
| `results/assistant_development.json` | The active 12-check receipt (all PASS). `aggregate_controls.json` records the four control subprocess runs and that all matched expectation. `aggregate_{omit,duplicate,unexpected}.json` are **expected failing** controls, not broken runs. |
| `provenance/build_00` | The earlier 11-check build (before the coherent-transport control CB12 was added). Kept, not overwritten — the register's "supersede, don't delete" rule in action. |
| `sources/*` | Copies of the six recovered-concept reports + the AD files + the unchanged recovery zip. Inert source material, explicitly **not** re-activatable jobs. |

### 1.2 What `check_bridge.py` actually tests (formal objects and claims)

The carrier is deliberately tiny: all rational/Boolean functions on the 3-cube `{0,1}^3`,
coordinates `(h,x,y)`, with the multilinear representation
`f = a0 + a_h h + … + a_hxy hxy`. The retained summary **C2** keeps the 7 coefficients of
degree ≤ 2 (equivalently the values at the 7 sites where ≤2 coords are 1) and **omits the
one three-way term `a_hxy`**. The checks establish, exactly and by exhaustion where finite:

- **CB01/CB02** — the coeff↔value transform round-trips on all 256 Boolean tables + 32
  rational tables; the 128 summary fibers each have exactly 2 members differing only in the
  omitted site. *(The summary's "blind spot" is exactly one degree of freedom.)*
- **CB03** — C2 is **closed under pointwise + and ×** (all 65,536 ordered law pairs): a
  degree-≤2 summary supports these operations without ever reading the omitted term. *A
  partial representation can be genuinely, exactly reusable.*
- **CB04/CB05** — the finite fiving map `F(d)=d+5 mod 10`, `d=5h+r`, toggles `h`, preserves
  `r`; adapter `A_r(h,x,y)=(5h+r,x,y)` commutes with the cube's `h`-flip. The **strong lift**
  `n=10w+5h+r` retains winding: two fivings return the finite display but land at `w+1` — so
  *finite return ≠ strong return*.
- **CB06** — the key refutation: two laws with the **same C2 summary** (`h+x+y` vs
  `h+x+y+hxy`) read identically now (both 2 at site 110) but **differ after the flip** (3 vs
  4), because `hxy → xy−hxy` moves the hidden term into the retained view. **C2-only reuse is
  REFUTED under this added operation** — and this expected refutation is a *successful* test.
- **CB07/CB08/CB09** — the general criterion: for an input map `H` acting by pullback,
  the summary `C_S` (retain sites `S`) supports `H` with the **same** `S` **iff `H(S) ⊆ S`**
  (forward-closure). Full-coefficient repair works for all 4,096 law/map pairs; the **minimal**
  forward-closed superset over all 256 site subsets is unique (here: all 8 sites once the flip
  is admitted). *This is a clean minimality theorem in the retained-site family.*
- **CB10/CB12** — a redundant re-probe adds no distinction, but a justified new probe does;
  and **coherent transport** of both view and receiver (`S_new = H⁻¹(S_old)`), tested over all
  48 cube symmetries, creates **no** information loss — distinguishing a lawful
  re-coordinatization from a genuinely new question.
- **CB11** — the Double-Stamp graphs A5/B6/C7: their quotient counts under the row-swap
  involution are `(3,2,0)/(3,3,1)/(4,3,0)`. A5 and B6 share vertex-count 3 but have different
  **declared dwell permissions** — so *count alone cannot decide enabledness*; retaining edge
  inversion/type can. Dwell is authored process semantics, **not** an inferred physical-safety
  claim.

### 1.3 What the omit/reorder/duplicate/unexpected controls establish

Crucially, the controls are **not** about the mathematics — they test the **coverage
validator** (that the harness itself cannot silently drop a required obligation):

- `omit` (drop the last row), `duplicate` (repeat a row), `unexpected` (emit an undeclared
  case id) → all **FAIL with nonzero exit**: the validator compares emitted ids against the
  frozen `required_case_ids` and rejects missing / duplicate / extra ids by set identity, not
  by count.
- `reorder` (reverse the rows) → **PASS**: order is not semantically meaningful.

This is the same **process-integrity pattern** that recurs across William's audits — e.g.
`absolute-distinction/CURSOR_REVIEW_REPAIR.md` §A/§B, where deleting the `AD11` record still
returned PASS until a real coverage validator was wired in ("Do not derive expected
obligations from emitted rows"), and the campaign audit note in the will-corpus flagging
"coverage gaps across campaign task-card directories." **Takeaway: "coverage" in the corpus
means *obligation coverage of an audit* (did every required check actually run), a
meta-integrity property — not the "fraction of scenes certified" sense we used the word in
`SUFFICIENCY_TEST.md` (see §3.4).**

### 1.4 Recovered-concept reports (natural-language → partial formalization)

| File | Contains | Status signal |
|---|---|---|
| `RPRM-CONCEPT-RECOVERY.md` | Compact entrance: which remembered concepts survive in the two papers vs only in conversations. | Recovery, not revision. Careful "Direct / related-substrate / absent" grading. |
| `PRESTIGE-AND-NUMBER-OPERATIONS.md` | Prestige One / reincarnation, fiving, FIVE_IS_SAFE/Double-Stamp, "every 3 is a 9", inverse-number vocabulary — verbatim William turns + existing assistant formalizations. | Third "one" name and full 1–9 waiting/inverse table **OPEN**. |
| `CUBES-AND-PI-CURVES.md` | Multilinear formula cube, ternary checking cube + **abduction space** `Counterfeit_n = ker(D_center)/ker(D_full)`, dim `(3^n−1)/2 − n` (=10 at n=3), LawCube/RelationForge software, Circle Compiler / "true pi". | Individual donors completed at declared scope; integrated cube **OPEN**. |
| `ZERO-AND-RAILS.md` | Centered halves, Seam Zero `SZ-6\|4->0\|1` translator, `+0.4/−0.6/−0.2` contrast, movable-cut / lens-lock (winding-preserving relocalization). | Coordinate identities solid; "math-rail vs physics-rail" physical necessity **unlocated**. |
| `PAPER-COVERAGE-AUDIT.md` | Byte-verified audit of the public `RPRM-open` repo: what's in the *Manifesto* + *The Right Answer Is Not Enough* vs only in the companion. | 6/6 SHA-256 matches; clear Direct/Absent dispositions. |
| `SOURCE-INDEX.json`, `ORIGINAL-CONVERSATION-*`, `VERIFICATION.json`, `PRESTIGE-SOURCE-RECEIPTS.json` | Reopenable source locators, hashes, and raw passages kept as evidence rather than definitions. | Provenance layer. |

### 1.5 `will-corpus/*.txt` (raw dialogues; grepped, not read end-to-end)

The greps confirm the corpus is not marketing — it is working development with an honest
falsification culture. Concretely: William's canonical acronym is **"Relational
Pressure–Retention Model"** (`RPRM_AGENT_CONTEXT_COMPACT.md`); his CITATION.cff titles the work
**"RPRM: receiver-relative closure"**; and there is a running kernel (`RPRMZipperLab`,
`NariZoo`) that implements the operational-factorization test directly — "one-step successor
congruence then established all-finite-word equivalence," emitting a `successor_defect` when the
active domain leaks, with `bisimulation certificate` witnesses. A separate pi-digit study
reports a **clean null** ("no local law in pi's first 300,000 digits at any order up to 6,"
max |z|=1.37, while lawful controls light up at hundreds of sigma) — a decisive falsification
run *against their own hoped-for structure*. That practice is the strongest evidence that the
"not BS" demand is real and enforced.

---

## 2. Grounding audit — did we ground RPRM correctly?

**Overall verdict: yes, the four concepts we leaned on are grounded correctly and named
close-to-canonically.** The corpus *confirms* Props 1–2 and receiver-relative sufficiency
almost verbatim, *extends* the certificate idea with the exact general theorem our `P_geo`
only approximated, and exposes a couple of *non-canonical namings* worth fixing. Details, with
short quotes:

### 2.1 Prop 1 — question factorization → **CONFIRM** (high confidence)

We used: decoder `Q=h∘C` exists iff `C(x)=C(y) ⇒ Q(x)=Q(y)`.
`FORMAL_BRIDGE_NOTE.md` §2 states it identically: *"A decoder from C to Q exists on the reached
image exactly when C(x)=C(y) ⟹ Q(x)=Q(y)."* The corpus also volunteers the honest caveat we
were careful to include: this is *"the ordinary factorization … core already present in
William's work, not a new theorem."* Our `SUFFICIENCY_TEST.md` C1 (single-equipotential) is a
faithful Prop-1 instance. **Nothing to correct.**

### 2.2 Prop 2 — operational congruence / lumpability → **CONFIRM + EXTEND** (high confidence)

We used: to reuse `C` as a *state*, need for `C(x)=C(y)`: same observation, same enabledness,
and `C(T(x))=C(T(y))`. `FORMAL_BRIDGE_NOTE.md` §2 states exactly this ("T is enabled on x iff
… ; when enabled, C(T(x)) = C(T(y))"). The strongest confirmation is not a paper but **William's
running kernel**: `RPRMZipperLab/fold.py` computes the one-step successor-congruence refinement
and raises `successor_defect` when a class fails it — the exact condition we called Prop 2's
clause (3). So our claim that model `C_body` "fails Prop 2 under dynamics" is grounded in code
William actually runs.

*Extension we didn't use:* the kernel carries a **bounded-horizon** structure — "grade-k
receiver" (observes only continuations of depth ≤ k) and a **reopening theorem**: *only bounded
folds reopen under a longer future; the minimal fold is a congruent fixpoint.* We used only the
binary "exact-forever vs must-refine" split; the corpus offers a *graded* dial (exact for k
steps) that we left on the table (see §4.2).

*Naming nuance:* we labeled Prop 2 "strong lumpability / bisimulation." That matches the
*Process Mechanics* §7 cross-walk and the kernel's own `bisimulation certificate` — but note
the word **"lumpability" never appears in the will-corpus**; it is the paper's translation into
standard vocabulary, not William's native term. Fine to keep, but attribute it as *our/the
paper's* standard-name mapping, not William's word.

### 2.3 Receiver-relative sufficiency → **CONFIRM** (high confidence), canonical

"Sufficiency is always relative to a stated receiver" is not a peripheral RPRM idea — it is the
*title concept*: the CITATION.cff calls the whole model **"receiver-relative closure,"** and the
corpus uses "grade-k receiver" / "receiver width" as first-class objects. Our decision to *name
the receiver first* (`R_static`) and make every representation choice relative to it is exactly
right and exactly canonical. **Nothing to correct**; if anything we under-used the *graded*
receiver family.

### 2.4 Certificate / coverage-vs-soundness → **EXTEND, with one naming CORRECTION** (med-high)

Two findings:

1. **Our `P_geo` is a special case of a general theorem the corpus already proves.** We
   presented `P_geo = C1∧C3∧C4` as a hand-built geometric predicate. `FORMAL_BRIDGE_NOTE.md` §6
   gives the general form: a retained-site summary `C_S` supports a future input-view `H` **iff
   `H(S) ⊆ S`** (forward-closure), with the exact minimal repair = the least forward-closed
   superset `S*`. That *is* the sufficiency certificate, in closed form, plus the precise
   "least extra state to add back" — which is our `C' = (C_body, velocity)` repair
   (`RPRM_FLUIDS.md` §3.3) as an instance. **We got the structure right; the corpus supplies the
   general certificate + minimal-repair we only stated informally.** "Certificate" is a
   canonical RPRM word (`bisimulation certificate`, `RPRM_SEAM_CERTIFICATE_01`, "local adjacency
   certificate"), so our usage is on-brand.

2. **Naming correction — "coverage."** In `SUFFICIENCY_TEST.md`/`PERF.md` we used **coverage** to
   mean "fraction of scenes the certificate certifies," and **soundness** to mean "false-positive
   rate." In the corpus, **"coverage" is a reserved audit term meaning *obligation coverage*** —
   did every *required check* actually execute (the omit/duplicate/unexpected validator; the
   AD11-deletion bug). Using "coverage" for "scenes certified" collides with William's meaning
   and could read as BS to him. **Recommendation:** rename our axis to something like *certified
   fraction* / *certification rate*, and reserve "coverage" for obligation-coverage. ("Soundness"
   for FP-rate is fine and does not collide — that word doesn't appear in the will-corpus.)

**Top corrections/extensions (ranked):**
1. *Adopt the general §6 forward-closure certificate + minimal-repair* as the real theorem
   behind `P_geo` (upgrade from a bespoke predicate to a cited instance).
2. *Rename our "coverage" axis* — it clashes with the corpus's obligation-coverage meaning.
3. *Attribute "lumpability/bisimulation" as the standard-name mapping*, and note Prop-2 has a
   graded-horizon extension we didn't use.

---

## 3. High-value corpus concepts we haven't used (ranked by promise)

### 3.1 The Fold → FutureTest → Five → Refold loop + `successor_defect` witness — **highest**

The will-corpus describes the kernel's operating cycle: *"begins with Fold: it assumes somebody
supplied a candidate key/equivalence/representation. It can then FutureTest that proposal, find
a counterexample, Five the failure backward, and Refine/Refold."* Mapped to fluids:

- **Fold** = our `C_body` summary. **FutureTest** = our Prop-2 refinement check. **Refold** =
  our re-flood. We already reinvented three of the four stages *ad hoc*.
- What we're missing is the **witness discipline**: the kernel emits a *minimal reopening
  witness* (the shortest future that breaks a bounded fold — e.g. `('go','go','go')`, length 3)
  and **`five.five`** *backward-localizes* which coordinate the summary failed to read
  ("the distinction needed 3 more steps to become observable; implicated=('credits',)").
- **Payoff for us:** replace `PERF.md`'s heuristic guardrails (TTL=128, volume-drift threshold)
  with a *witnessed* trigger: when a cached body would go wrong, emit a `successor_defect` naming
  the exact cell/quantity (velocity? a specific interface cell?) that forces the re-flood. That
  turns model E's "we think the cache is stale" into "here is the minimal witness that it is."
  This is a *general mechanism*, it is William's actual running formalization, and it directly
  hardens our cheapest, most heuristic component.

### 3.2 Bounded-horizon / grade-k receivers + reopening theorem — **high**

"Only bounded folds reopen under a longer future; the minimal fold is a congruent fixpoint."
For fluids this is a **principled accuracy dial**: instead of the binary static/dynamic split,
certify a body as *exact for the next k frames* even when it is not exact forever. This is
exactly what `CacheTTL` gropes at with a magic constant — the corpus gives it a proof obligation
(fold at horizon k) and tells you when a longer horizon must reopen. Promising for perf *and*
for stating H2 (`RPRM_FLUIDS.md` §5) as a graded, not binary, boundary.

### 3.3 Cube abduction space `Counterfeit_n = ker(D_center)/ker(D_full)` — **high**

`CUBES-AND-PI-CURVES.md` defines, exactly, "the real many-dimensional abduction space": the
family of completions a partial check *cannot* decide (dim `(3^n−1)/2−n`; 10 for the 3-cube).
This is the precise theory of **grade-blindness / center-blindness** — "precisely characterize
what a partial view cannot see, including complete missing-function families." For fluids it is
the rigorous version of "what can `C_body` *not* distinguish" (our fiber), and the companion
**7→8 abductive lift** ("one additional probe resolves the missing direction") is the theory
behind observation economy (`RPRM_FLUIDS.md` §1.7) and our "which one observation to add back."
It connects directly to `check_bridge.py`'s own fiber/minimal-repair objects (CB02/CB09).

### 3.4 Prestige One as a hot-summary + retained-cold-reopen envelope — **medium**

`PRESTIGE-AND-NUMBER-OPERATIONS.md` (U00, U10) + `CONCEPT_REGISTER.md` RCF-P1: a completed
construction "appears as one while retaining a relationship/route to its construction… once the
lower relations are understood, the completed unit can become ordinary to use," with a
*reopening record* and *versioned scope*. William's own gloss (U10): *"it doesn't contain pi,
but a total relationship to pi … another path to the thing."* **This is precisely our model
D_fast cache**: a body displays a cheap cached level (hot summary) while retaining the route to
re-flood the full construction (cold reopen), invalidated by volume-drift/TTL (versioned scope).
Our `stepE` is arguably a *worked instance* of the "operation-aware promoted envelope" the RCF01
assignment §4 asks someone to build. Mostly an organizing/naming win — but it would let us frame
D_fast in William's own vocabulary and satisfy an open assignment target. (Guard against the
register's "do-not-conflate" list: this is the *reuse-capability* sense of prestige, **not** the
Absolute-Distinction authority-inspection sense.)

*Lower promise for fluids but worth naming:* **Absolute Distinction** (the no-exemption
inspection policy: "no step is exempt because it is familiar, prestigious, or RPRM-branded") —
our `RPRM_FLUIDS.md` §6 rename-audit is literally an act of Absolute Distinction, so we could
cite it as method. **Zero-and-rails** (relational/winding coordinates, lens-lock) reinforces our
relational body/level choice but adds little new. **True pi / Circle Compiler** is out of scope
for fluids.

---

## 4. Honest status — solid vs WIP, and where the formalization still has gaps

**Solid / proved (exact, finite, and I re-ran it):** everything in `check_bridge.py`. The
multilinear transform round-trip (256+32 tables), C2's closure under +/× (65,536 pairs), the
fiving adapter identity, the strong-lift winding retention, the **general retained-site
forward-closure proposition** and its **unique minimal repair** (a clean, correct little
theorem), the coherent-transport no-loss result (48 symmetries), and the Double-Stamp
enabledness collision. The coverage validator behaves exactly as its protocol declares. These
are genuinely solid — but **small**: a fixed `{0,1}^3` (and `Z/10`) carrier, and *by the
package's own repeated insistence* exposed development checks, **not** holdout, with the
historical donor code **not** rerun.

**WIP / asserted (the package says so itself, via NOT_RUN / OPEN labels):**
- Prestige One's full lifecycle — the operation-aware promoted envelope is **NOT_RUN** (that is
  the assignment's next build, not a done result).
- The third "one" name (ascended/rebirth/…) — **OPEN**; the register forbids inventing it.
- The full "waiting on 1/3/5/7" rule and the inverse-5/6/7/8 table — **OPEN / unlocated**.
- "Every 3 is a 9" as a quantified law, and "true pi" — **unlocated** in the public text
  (`PAPER-COVERAGE-AUDIT.md`); real as intent, not as a stated theorem.
- The bridge from the fiving splice to the Double-Stamp restart — explicitly **a hypothesis**,
  no commuting adapter proved.

**Where the running formalization still has gaps:**
1. *Carrier scale.* All exact results live on one 8-site cube; nothing yet shows the criteria
   scale to a realistic state space (this is honestly disclaimed as "not a universal claim").
2. *Integration.* The concepts are connected pairwise (fiving↔cube via one adapter) but the
   single integrated device William remembers is not reconstructed; donors remain separate.
3. *Independence.* The checks are self-authored and exposed; there is no holdout / independent
   re-derivation of the mathematics beyond the twin transform/coefficient branches.
4. *Semantics vs structure.* CB11 is candid that dwell permissions are *authored*, not derived —
   the Double-Stamp "safety" is process semantics awaiting a dynamics that would justify it.

Net: the CORE-FORMALIZATION is **honest and internally rigorous at a deliberately small scope**,
with its own limits loudly labeled — which is exactly the "not BS" posture. The recovered
natural-language concepts are **real but genuinely unfinished**, and the package is scrupulous
about not letting a neat finite example silently become the whole meaning.

---

## 5. Did we ground RPRM correctly? (bottom line)

Yes. `RPRM_FLUIDS.md` and `SUFFICIENCY_TEST.md` use Prop 1, Prop 2, receiver-relative
sufficiency, and a decidable certificate in a way the corpus **confirms almost verbatim** — and
our own honesty guardrails (Pressure is not a physics primitive; most ingredients are standard
methods renamed; the certificate wins on certified-fraction, not soundness) match the corpus's
own culture. The three things to fix are modest: (1) cite the general §6 forward-closure
certificate + minimal-repair as the real theorem behind `P_geo`; (2) rename our "coverage" axis,
which collides with the corpus's reserved *obligation-coverage* meaning; (3) mark
"lumpability/bisimulation" as the standard-name mapping and note the unused graded-horizon
extension. The highest-value unused ideas are the **Fold→FutureTest→Five→Refold loop with
`successor_defect` witnesses** (upgrades our heuristic cache triggers to witnessed, minimal
ones), **bounded grade-k receivers** (a principled accuracy/TTL dial), and the **cube abduction
space** (the exact theory of what a cheap summary cannot see). None of these change the physics;
they sharpen the *representation-sufficiency-certificate* machinery we already bet on.

---

## 6. `check_bridge.py` — run result

Run with `/workspace/.venv/bin/python -B check_bridge.py` (Python 3.12.3), fresh output paths:

| invocation | reported status | exit | matches PROTOCOL? |
|---|---|---|---|
| `--control none` (starter) | `PASS`, 12 emitted cases | 0 | yes |
| `--control omit` | `FAIL` — `missing={CB12_TRANSPORTED_RECEIVER}` | 2 | yes (expected FAIL) |
| `--control duplicate` | `FAIL` — `Duplicate emitted case IDs` | 2 | yes (expected FAIL) |
| `--control unexpected` | `FAIL` — `missing CB12 / extra UNDECLARED` | 2 | yes (expected FAIL) |
| `--control reorder` | `PASS`, 12 emitted cases | 0 | yes (expected PASS) |

All 12 cases CB01–CB12 PASS on the clean run; the three integrity controls fail with nonzero
exit and `reorder` passes — exactly as `PROTOCOL.json`/`results/aggregate_controls.json` declare.
**What it establishes:** the finite/exact mathematical claims of §1.2 hold on this carrier, *and*
the harness's coverage validator genuinely rejects a silently-dropped or spoofed required
obligation. It explicitly does **not** establish holdout confirmation, a runtime benchmark, a
universal RPRM mechanism, or any replay of the historical donor code.
