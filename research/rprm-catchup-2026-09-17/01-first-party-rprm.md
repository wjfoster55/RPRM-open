# First-party RPRM: how the project understands itself

**Prepared:** 16–17 September 2026  
**Workspace read:** `C:\github\RPRM-open` (git `main`, locally ahead of `origin/main` by autosync commits; working tree also contains untracked Paper 3 and live BSD/cross-closure debris)  
**Stance:** take the project's own papers, docs, and declared contracts as primary. Chat logs and assistant process notes are process evidence, not theorems. William Foster is the named author. Benefit of the doubt on experimental work; no rubber-stamping. Every claim below has a domain and an evidence grade. Chats, Codex tickets, and Memory Fabric packets are cited only as recovery locators, never as mathematical authority.

**Reading edition of the public book:** Manifesto v1.0.3, DOI [10.5281/zenodo.22650748](https://doi.org/10.5281/zenodo.22650748), source `MANIFESTO.md`, PDF `RPRM-Manifesto.pdf` (140 pages). Byte binding in `DOCUMENT_BUILD.json`: source SHA-256 `1970db936f6b448c869e563559955e3199fdf688fceb9962fe2d47466510922e`, PDF SHA-256 `a9d0c83456281ffa59fbf0c90394d18399bdca98dbc90d337df3ec8f1226e958`, status `SOURCE_MATCHING_LAYOUT_REVIEWED`.

**Companion working paper:** *The Right Answer Is Not Enough*, Process Mechanics 0.3, 11 September 2026, DOI [10.5281/zenodo.22709682](https://doi.org/10.5281/zenodo.22709682). Canonical sources: `papers/process-mechanics/{MANUSCRIPT.md,APPENDICES.md,BIBLIOGRAPHY.md}`. This DOI is **not** the Manifesto DOI.

**Paper 3 (private draft, not released):** *Absolute Distinction: Revising Task Distinctions and Retaining Access in RPRM*, draft 0.1, 16 September 2026, untracked at `papers/absolute-distinction/`. Explicitly not a publication.

**What this report is:** a first-party map of live contracts, live mathematics, research debris, recovered concepts, and open non-BSD paper candidates.  
**What this report is not:** a next-target picker, a BSD deep dive, a novelty verdict, or a PDF.

---

## 0. How to read this document

Evidence grades used here follow `docs/core.md` §16, `docs/glossary.md` “Evidence grade”, and `AGENTS.md`:

| Grade | Meaning in this corpus |
|---|---|
| **Definition** | A named object or convention. Not a theorem. |
| **Established mathematics** | Standard result, attributed (factorization through kernels, Moore refinement, Hamming codes, Newton interpolation, strong lumpability, etc.). |
| **Written proof** | Argument in the Manifesto, `docs/*.md`, or a research note, with stated hypotheses. Not Lean unless listed. |
| **Formal proof** | One of the exact 20 Lean declarations in `lean/Relations.lean` and `lean/Carrier.lean`. |
| **Finite test** | Exhaustive or bounded census on a declared family. Scope is the family. |
| **Derived synthesis** | Composition of stated results; contribution is the connection, not a new primitive. |
| **Conjecture / OPEN** | Unproved, unfinished search, or missing contract. |
| **Interpretation** | Physical, biological, historical, or authorial reading. Not a proof premise. |
| **Process evidence** | Chats, recovery packets, agent assessments, layout reviews, hashes. A hash binds bytes; it does not prove contents. |

Dispositions for complete solved fibers, from `AGENT_HANDBOOK.md` §3 and `docs/core.md` §5:

- **NONE** — complete admitted fiber empty.  
- **ONE(value)** — unique member.  
- **MANY(family)** — several members, represented completely.  
- **OPEN** — unfinished search or unresolved obligation. Not NONE.  
- **OPEN_NEW_CARRIER** — a new type/operation/receiver is required.  
- **REJECT** — a well-formed certificate fails.  
- **Admission error** — malformed or out-of-carrier input.

NONE/ONE/MANY are used **only** for a complete solved fiber. An unfinished search that found two witnesses has found at least two witnesses; it has not returned MANY.

---

## 1. What RPRM claims to be

### 1.1 The project's own one-line claim

From `README.md` and `MANIFESTO.md`:

> **RPRM stands for Relational Pressure Retention Model.** The name comes from the motivating physics proposal about underlying relations, pressure and retention. It remains the name of the whole framework.

> RPRM is a **relational framework for mathematical unification**. It describes mathematical problems through their carriers, relations, operations, observations, and missing information. Its purpose is to connect existing mathematics while preserving what each source system means.

Domain: the stated source class of each preservation theorem.  
Grade: **definition of the program**, not a theorem that every mathematical problem has been unified.

`docs/core.md` §1 is more precise about what “unifies” would require:

> “Unifies all human mathematics” would require a specified class of source mathematics, an interpretation for each member and a preservation result of the requested strength. This version states a broad relational-presentation result and separately scoped application bridges; it does not infer universal coverage from the ability to write a tuple.

The Manifesto’s unifying claim (`MANIFESTO.md` opening):

> Its unifying claim concerns a common relational presentation of specified mathematical structures. Physical and biological applications retain their stated models and open experimental obligations.

### 1.2 Two tasks that must not be collapsed

`docs/relational-layer.md` and `MANIFESTO.md` Part I §7 separate:

1. **Mathematical unification.** Encode a *supplied* structure as typed relations and prove that its statements and (when claimed) operations survive. This is U01–U05 in `docs/unification.md`. Grade: written proof; selected identities formalized.  
2. **Physical identification.** Ask whether observable objects, forces, and geometry arise from an underlying organization of relations and lawful continuations. “Underlying” names explanatory dependence, not an extra spatial dimension or a demonstrated substance. Grade: **interpretation / open modeling**. Closure of a description does not prove that a hidden coordinate exists, nor that it is forever inaccessible.

The afterword (`MANIFESTO.md` “Author afterword”) is authorial interpretation: William states that his mathematics education never went beyond algebra, that the work was developed through conversations with ChatGPT and Claude, that Codex assisted with drafting/implementation, and that he wants the work freely reusable without claiming personal credit for the ideas. That is process and intention evidence, not a mathematical result. The licenses match that intention: original software 0BSD, original prose CC0 (`README.md`, `LICENSING.md`). `CONTRIBUTING.md` promises no maintenance.

### 1.3 What the name does *not* establish

`docs/core.md` §15 and `docs/glossary.md`:

- **Pressure** has no universal scalar. A model may use constraint count, residual norm, live-fiber cardinality, resource deficit, etc. `log₂|F|` on a finite nonempty fiber is an information-capacity measure, not Shannon entropy without a probability law.  
- **Retention** has an exact information reading through `ker C`. Storage size, access cost, and persistence are extra.  
- **Zero, half, balance, vacancy, missing assignment** are different typed roles. Missing assignment is never numerical zero without a declared map.

The handbook (`AGENT_HANDBOOK.md` §1):

> Do not assume a concept is new because its RPRM name is new. Give ordinary mathematical names and attribution where applicable.

`docs/references.md` credits Codd (relational model), Plotkin (operational semantics), Moore-style minimization, Fritz (Markov kernels), Lean’s quotient axioms. Ancestry of the Manifesto’s opening theorems is explicit: [Q] quotients, [M] Moore refinement, [I] bilinear Lagrange, [L]/[S] many-sorted logic and function graphs.

### 1.4 The motivating example the project always starts with

`README.md` / `MANIFESTO.md` Part I §1, law `a+b=c` on `{0,1,2,3,4}`, ordinary addition, no wrap:

| Supplied ports | Missing ports | Complete answer |
|---|---|---|
| `a=1,b=2` | `c` | ONE: `3` |
| `a=1,c=3` | `b` | ONE: `2` |
| `c=3` | `(a,b)` | MANY: `(0,3),(1,2),(2,1),(3,0)` |
| `a=4,c=0` | `b` | NONE in this carrier |

The last answer changes if negative integers are admitted. The third answer is a **correlated set of pairs**, not two independent lists. Grade: elementary exhaustive fiber on a finite carrier; used as the contract’s teaching example, not as a new theorem.

### 1.5 Version and publication identity

| Object | Identity | Evidence |
|---|---|---|
| Manifesto edition | v1.0.3 “independent research scope correction” | `MANIFESTO.md`, `CITATION.cff`, GitHub release 2026-09-07 |
| Manifesto DOI | 10.5281/zenodo.22650748 | `CITATION.cff`, README |
| Process Mechanics | working paper 0.3, 11 Sep 2026 | `papers/process-mechanics/README.md` |
| Process Mechanics DOI | 10.5281/zenodo.22709682 | same; “does not inherit the Manifesto DOI” |
| GitHub | https://github.com/wjfoster55/RPRM-open | public; created 2026-09-07 |
| GitHub issues | **disabled** | `gh issue list` |
| GitHub PRs | none visible | `gh pr list` empty |
| GitHub releases | v1.0.0, v1.0.1, v1.0.2, v1.0.3, all 7 Sep 2026 | `gh release list` |
| Local tags | v1.0.0, v1.0.1, v1.0.2 | `git tag` — **local tags stop before the reading edition’s v1.0.3 tag**; Paper 3’s plan already notes this |
| Fermat history | v1.0.1 withdrew theorem-inheritance closure; v1.0.2 restored independent scope; v1.0.3 keeps the bounded study in `docs/fermat-study.md` | git log `3b4fcdc`, `a748367`, `79c78fa`; `docs/fermat-study.md` |

---

## 2. Core ontology

This section is the live contract. Primary sources: `AGENTS.md`, `AGENT_HANDBOOK.md` §§2–6, `docs/core.md`, `docs/operations.md`, `docs/glossary.md`.

### 2.1 Carrier, sorts, types, equality, context

**Carrier** (`docs/glossary.md`, `docs/core.md` §2): a supplied set of typed values or states, optionally with extra structure (order, topology, metric, algebra, units, probability, encoding). Empty carriers are allowed unless a theorem says otherwise. Finite cardinality, finite description, spatial boundedness, and finite execution horizon are **four different conditions** (`docs/core.md` §13).

**Sort / type:** a named carrier plus equality. Distinct sort names remain different types even if underlying numerals coincide. A typed value is the pair `(τ, x)`. Well-typed ≠ admitted ≠ solvable.

**Context `Θ`:** a versioned specification containing signature, carriers, equality, admission, operations, observations, failure contract, and parameters. The identifier is a pointer; it supplies none of the content. Changing a fixed field creates a new context version. A later timestamp is not a compatibility proof.

**Equality profiles** (`docs/core.md` §4) that must not be silently substituted:

| Equality | Required data |
|---|---|
| Same occurrence | Equality in the occurrence-ID carrier |
| Same value | Equality in a declared value sort |
| Same expression | Syntax under a stated equivalence |
| Same denotation | Interpreted values/relations/functions |
| Same receiver behavior | Declared observations/futures |
| Same artifact bytes | Byte strings or a hash under its assumptions |

`AGENTS.md`: “Keep equal values distinct from equal occurrences.” Two independently stored zeros are not interchangeable for an ancestry receiver. `1+1` and `2` may be equal as values while traces differ.

**Occurrence carrier:** identifiers, `type: Id → Sort`, `val(i) ∈ |type(i)|`, optional incidence/ancestry/position/source maps. Identifiers do not prove ownership or authenticity.

**Address:** a coordinate in a supplied scheme. Equal printed addresses from different schemes do not establish a conversion map.

**Hostile case (decimal digits):** the symbols `0…9`, the cyclic group `Z/10Z`, and a digit-with-carry are three different signatures (`docs/core.md` §3). Linear successor fails at 9; cyclic successor sends 9→0; positional increment sends 9→ digit 0 and carry 1.

### 2.2 Ports, missing ports, environments, readout, apertures

**Role:** a named position in a relation. **Port:** a role plus type plus interface behavior. For finite port set `I`, assignments live in `Asn(I) = ∏_{i∈I} |τ_i|`.

**Relation:** `R ⊆ Asn(I)`. The relation itself has **no inherent input/output split**. Direction is an aperture choice.

**Environment `η`:** a partial typed assignment to `K ⊆ I`. Missing assignment is not zero, empty-set, or error.

**Completion fiber** (`docs/core.md` §5):

```text
Fib(R, K, η) = { r|_A : r ∈ R, r|_K = η },  A = I \ K
```

Joint correlation is load-bearing. For `R = {(0,0),(1,1)}`, the two-port fiber has two members; the product of unary projections has four, two of them false.

**Readout `ρ`:** a map on the missing-assignment carrier. The identity readout returns full completions. A lossy readout can make the *display* unique while the source fiber remains MANY.

**Aperture profiles** (`docs/core.md` §6) share a name, not an encoding:

1. **Relation aperture** — `(Θ, R, I, K, η, A, ρ)`. Rotation changes which ports are vacant; it changes the question, not the law.  
2. **Observation/query aperture** — probe family `Q_p`, selected probe, source or source fiber. Passive vs state-replacing observations differ. A **window** is a footprint + coordinate map + readout.  
3. **Hypothesis/rule aperture** — family `H`, experiments, evaluation `ev`, evidence. ONE means unique in that family. If the true rule is outside `H`, a singleton survivor need not be true of the world.  
4. **Construction boundary / moving vacancy / zipper** — attachment sites, occupancy vacancy, sequential frontier. Family definitions; no universal cube or gap-drawing theorem.

`AGENTS.md`: “Keep correlated missing ports joint.”

### 2.3 Operation kind, direction, enabledness

Semantic kinds (`docs/operations.md` §1): `REL`, `PARTIAL`, `NONDET`, `KERNEL`. A total map is PARTIAL with full domain.

| Kind | Composition | Identity | What it is not |
|---|---|---|---|
| REL | existential middle witness | diagonal | a selected output |
| PARTIAL | sequential on joint domain | `id` | automatically decidable domain |
| NONDET | union of successor sets | `{x}` | probability, fairness, scheduler |
| KERNEL | sum of products of masses | point mass | a realized sample; a zero row is not a law |

**Direction** selects the requested leg. **Inverse, converse, retraction, negation, complement, reversal** are different operations (`docs/core.md` §7, glossary).

**Enabledness** is membership in the operation’s domain. An exact operational quotient must give the same enabledness answer for all sources it merges. Comparing only jointly legal runs can conceal enabledness loss.

**Witness-aware composition:** retain `(x,y,z)`. Endpoint projection can be ONE while the middle fiber is MANY.

### 2.4 Receiver, representation, decoder, CAR / FOLD / ADAPTER

**Question receiver:** family `(Q_p : X → B_p)`. Equality = agreement on every admitted probe.

**Operational receiver:** plus operations, timing, failure, future language/horizon, traces/effects.

**Representation `C : X → Z`:** the retained data. **Observation:** one readout. **Decoder:** map from reached image to requested answer. These roles are not interchangeable even when a small example uses one map twice.

**Central factorization** (Manifesto Theorem 1, `docs/core.md` §8, Lean `factorization_iff`):

```text
∃ g : C(X) → B  with  Q = g ∘ C
  ⇔  C(x)=C(y) ⇒ Q(x)=Q(y)
```

`AGENTS.md`: “A representation preserves a question exactly when that question is constant on each representation fiber.” Decoder unique on the reached image. This is exact sufficiency, not computability, speed, or physical accessibility.

**CAR:** bijection from source to admitted image, inverse specified. Injectivity onto the reached image; not surjectivity onto unused ambient values.

**FOLD:** sufficient for a named receiver. Inclusive: may be injective. **Strict FOLD:** additionally merges at least two sources.

**Operational FOLD** (Manifesto Theorem 2, O05): whenever `C(x)=C(y)`,

1. `O(x)=O(y)`  
2. each `T_a` enabled at both or neither  
3. when enabled, `C(T_a(x))=C(T_a(y))`

An operational quotient also needs matching enabledness and retained successor behavior (`AGENTS.md`). Future-answer sufficiency is weaker than exact updating of an arbitrarily detailed summary. Canonical counterexample (`docs/operations.md` §5): states `{p,q,r}`, all observations 0, `p→p`, `q→r`, `r→r`, `C(p)=C(q)=0`, `C(r)=1`. Every future observation is 0, but summary 0 cannot update uniquely.

**ADAPTER:** typed translation with a named preservation contract. Correct types alone do not prove the contract.

CAR, FOLD, and ADAPTER **overlap**; they are not mutually exclusive species.

### 2.5 Inverse, retraction, preimage / completion fiber

| Construction | Contract |
|---|---|
| Map inverse | undoes a bijection on its image |
| Relation converse | swaps roles; fibers may be MANY |
| Retraction / section | `P ∘ L = id` on source; `P` may be lossy off the image |
| TRACEBACK.preimage | complete predecessor/trace fiber for a declared route |
| TRACEBACK.loss | earliest supported lost distinction on a declared diagnostic order |
| FIVE.future | separating future word for merged states; shortestness needs coverage |
| Lift–spin–land | `T = P ∘ H ∘ L` on the exact composite domain; prove the requested equation with `H` included |

Hostile landing (`docs/core.md` §14): `X={0,1}`, `Y={0,1,2}`, inclusion `L`, `P(2)=0`, `H` swaps 1 and 2. `P∘L=id` and `H` involutive, but the landed map sends both sources to 0.

### 2.6 Coverage boundary, hostile case, evidence grade

Every mathematical task record (`AGENT_HANDBOOK.md` §2 and §14) must state:

1. Carrier, types, equality, admitted context  
2. Supplied ports, missing ports, requested readout  
3. Operation kind, direction, enabledness  
4. Receiver (observations and continuations to preserve)  
5. Inverse, retraction, or complete preimage/completion fiber  
6. Coverage boundary, distinguishing hostile case, evidence grade  

Then: complete fiber or unresolved seam; strongest supported conclusion and next test.

**Coverage senses** (`docs/core.md` §12) that must not be conflated: transition closure, search completeness, invariant closure, receiver closure, boundary completion, topological closure, workflow closure. A **frontier** is a typed set of unvisited nodes, open sites, unresolved obligations, or exit states — not a metaphor.

**Hostile case** (`docs/glossary.md`): an input, mutation, or counterexample designed to expose a missing assumption. An out-of-carrier control tests rejection; it is not automatically a counterexample to an in-carrier theorem.

**Certificate vs receipt vs seal:** a certificate has a verification predicate and a separately stated soundness implication. A receipt records what was executed. A seal binds bytes and versions. Hash equality is byte identity, not mathematical truth, authorship, or permission (`docs/core.md` §16). Tool self-tests do not establish their own general soundness (`AGENTS.md`).

### 2.7 Named operators (minimum certified surface)

From `docs/operations.md` §12. Using the strongest tag requires at least:

| Name | Minimum result |
|---|---|
| SOLVE | complete admitted fiber |
| ATTACH | retained compatible source/boundary/ticket |
| CAR | two-sided inverse on admitted image |
| ADAPTER | typed preservation equation |
| FOLD.question | answer constant on every retained fiber |
| FOLD.operational | observation, enabledness, retained-successor descent |
| FIVE.future | a separating future; shortest/none only with coverage |
| TRACEBACK.loss / .preimage | earliest supported loss, or complete predecessor fiber |
| REFINE.question / .stable | old summary plus new distinction; or stable operational refinement |
| COMPILE.endpoint / .trace | same domain/final answer, or full trace semantics |
| LIFT–SPIN–LAND | typed composite and proved landing target |
| PROMOTE.capability / .state | closed-compound adapter, or FLICK installation |
| SEAL / INHERIT / FLICK | bound evidence; exact reuse cone; atomic parent-bound install |

O-numbered written theorems: O01 composition; O02 finite solving; O03 associative attachment (fixed-seam); O04 question descent; O05 operational descent; O05F minimal future quotient; O06 matched folds compose; O07 finite distinguishing bound ≤ n−1; O07L bounded loss localization; O08 least question refinement; O08R minimum finite repair alphabet = max Q-values in a C-fiber; O09 least stable refinement; O10 endpoint compilation; O11 correct lift–operate–land; O12 conditional promotion; O13 selective exact reuse (complete masks); O14 conditional single-successor installation (ABA-safe versions).

Lean coverage of this list is **narrow**: relation identities + deterministic operational fold + finite-word transport. Shortest-witness bound, min repair, unification translation, and implementation correctness are **not** formalized (`docs/formal-proofs.md`).

---

## 3. The actual mathematical lenses and constructions (with locations)

“Lens” is itself a glossary term (`docs/glossary.md`): package carrier, operation, receiver, retained/lost structure, inverse/fiber, boundary, and evidence as one view. Shared numerals do not make lenses identical.

Below, **live/canonical** means it is in the Manifesto, `docs/`, `rprm/`, or a declared executable pack. **Recovered/historical** means `recovered-concepts/` or Alpha/QR donors, not automatically in the published papers. **Research-lane** means `research/` with its own claim ceiling.

### 3.1 Live core constructions

| Construction | Where it lives | What it actually is | Grade |
|---|---|---|---|
| Complete relation fibers / SOLVE | `docs/core.md` §5, `rprm/core.py`, `checks/core.py` | Exhaustive joint completions on finite tables | written + finite (8,257 aperture queries in core checker) |
| Question factorization / FOLD.question | Manifesto Thm 1, `docs/core.md` §8, Lean `factorization_iff` | Q constant on C-fibers | established + written + formal (selected) |
| Operational fold / future quotient | Manifesto Thm 2, II.4, O05/O05F, Lean `operational_fold_iff` etc. | observation + enabledness + successor; coarsest future classes | established Moore ancestry; written partial-op adaptation; 9 Lean decls; finite machine census (`checks/futures.py`: 845 machines) |
| Least repair and min tag alphabet | Manifesto II.2, O08/O08R | `C'=(C,Q)`; min tags = max Q-values in a fiber | written; not Lean |
| Faithful relational presentation U01 | `docs/unification.md`, Manifesto II.3 | many-sorted finitary FO structures → exact graphs + image-guarded quantifiers | written; Lean has graph/fiber lemmas only; finite unification checker 394 models / 168,546 formula cases |
| Fiber transport U02, operation transport U03, shared interface U04, common records U05 | `docs/unification.md` | exact image encodings; middle-image guards required | written; hostile extra-middle-element counterexample |
| Affine four-port chart / clamp | `docs/core.md` §19, Manifesto II.1.2 | `x=(1-u)L+uR`; all four single-port fibers including collapsed endpoints | established elementary algebra + written |
| Four-corner / four-lane abduction | Manifesto Thm 3, II.5, `docs/proof-donut.md` | multiaffine `f=a+bx+cy+dxy` on `[-1,1]²`; corners determine all, including unvisited center | established Q1 Lagrange; hostile: two opposite corners insufficient; full boundary insufficient if grammar enlarges |
| Proof donut | `docs/proof-donut.md`, `rprm/proof_donut.py`, `checks/proof_donut.py` | certificate method around an unresolved port; independent of core implementation | finite certificates; **does not prove its own soundness** |
| Centered half | Manifesto II.6 ~lines 1199–1232, `docs/core.md` §15, `docs/origins.md` | `{0,1} → {−1/2,+1/2}`; separate unit-total lanes `S+R=1`, balance at `(1/2,1/2)`; k lanes → `1/k` | written identities; **two −1/2 occurrences are not their sum** |
| Vacancy swap (four sites) | `docs/core.md` §17 | 32 states, adjacent swaps, count+vacancy operational fold | written connected example + finite conformance |
| Carry / winding vs cyclic wrap vs real `0.999…=1` | Manifesto II.6, glossary “Carry” | different output types | definitions + written distinctions |
| Ten-cycle half-turn (“fiving” arithmetic) | glossary “Ten-cycle half-turn”; Atlas `atlas/kernel.js` cyclic half-turn | `d=5h+r`, +5 mod 10 toggles h, preserves r | family definition + implemented mechanism; **distinct from FIVE.future** |
| Local 1..9 charts at 2/4/6/8, handoffs 3/5/7 | `atlas/kernel.js` | “doing 3 with 2/4” reconstruction lead | implemented fragment; historical identity not fully confirmed (`PAPER-COVERAGE-AUDIT.md`) |
| Stochastic lumpability | Handbook §11, Manifesto IV.1 | equal block-mass ⇒ common reduced Markov kernel | written elementary criterion; Geiger–Temmel cited as context, not premise |
| Finite reconstruction of scores | Handbook §11 | min worst absolute decoder error = half largest score range in a C-fiber | written |
| Approximate TV bound | Handbook §11 | `TV ≤ min(1, t·ε)` for single-time marginals | written; not path statistics or infinite horizon |
| Fixed-gap Fermat decision | `docs/fermat-study.md`, `rprm/fixed_gap.py` | for each `n≥2,s>0,d>0`, complete NONE/ONE fiber for `a^n+(a+s)^n=(a+s+d)^n` | written all-height per aperture; finite checks; **not uniform FLT** |
| Bounded-side Fermat | `docs/fermat-study.md` Thm III.2.1 | `min(a,b)≤4000 ⇒ a^n+b^n ≠ c^n` for n>2 | written + 302 auxiliary-prime certificates; unrestricted independent goal **OPEN** |
| Prime square-frontier | Manifesto III.1, `experimental/primes/square-frontier.md`, `checks/prime_frontier.py` | primes ≤ B classify through B²; stages `5→25→625→390625` checked | written factor theorem + finite census |
| Two-path coherence receiver | Manifesto III.9, `experimental/two-path-lab/` | `χ` minimal for declared phase family; reduced-state fiber MANY inside disk | written under supplied QM model; 31 exact tests; **no physical experiment** |
| Radial gravity receiver | Manifesto III.10, `docs/relational-layer.md` | `(r,u,j)` forgets orientation | written for supplied Newtonian pair; physical source bridge OPEN |
| Return depth / black holes | Manifesto III.8 | continuation vs observation vs causal escape distinguished | written on supplied Schwarzschild; physical identification OPEN |
| Mechanical Motion Atlas | `atlas/` | 20 mechanism laws, 38 builder types | written proofs for 3 selected ideal laws; numerical IEEE-754 implementation; **not physical dynamics** |
| Rule Lab | `experimental/rule-lab/` | 256 CA rules, transforms, finite prime comparisons | finite model; no unbounded prime classifier |
| Lens Lab | `experimental/lens-lab/` | five ordered phases; lock vs edit | 16 model tests; displays are not source inverses |
| Music Lens | `experimental/music-lens/` | six-note phrase, 3 views, optional sound | 1,200 states / 895,298 assertions; no perceptual claim |
| Shadow Lens | `experimental/shadow-lens/` | inverse cutout from target shadow; 181,447 sources in the finite model | **not listed among the nine packs in `experimental/README.md`**; live playground + Node tests |
| Process Mechanics kits | `experimental/process-mechanics/`, `rprm/process_mechanics/` | circuits, intervals, water, cancer-model nulls | scoped claims in CLAIM_ID_MANIFEST; teaching demos ≠ historical panels |
| Tile / Board / Atlas hierarchy | glossary, `docs/operations.md` O12 | optional 8+center construction; Tile(X) is a new type | **definitions**; no executed universal ladder in the papers |
| Concept Sudoku / minimax query | glossary, handbook §13 | one-step minimax on supplied finite H×E | family definition; catalogue identification only |

### 3.2 Recovered / historical lenses (not automatically in the papers)

Primary index: `recovered-concepts/README.md`. Original passages: `recovered-concepts/ORIGINAL-CONVERSATION-PASSAGES.md` and concept files. Grade of the *user passages*: **authorial process evidence**. Grade of later formalizations: as each note states.

| Lens / name | Recovered meaning (compressed) | Formal home | Paper status | Open seam |
|---|---|---|---|---|
| **Prestige One** | After a 1-to-9 course, a “new-game-plus 1” that retains a *relationship/route* into the previous course, not necessarily the payload (U00, **U10 correction**) | `recovered-concepts/PRESTIGE-AND-NUMBER-OPERATIONS.md`; RCF01 `RPRM-CORE-FORMALIZATION-01/` | absent names in Manifesto/PM; two PROMOTE contracts nearby but **not** the three-type taxonomy | Third type (ascended/rebirth/…) **OPEN** (U33 itself asks) |
| **Reincarnation / tier** | Fold prestiges back; weak relationships; lower computation before next outer move (U15–U16) | same; historical 9×9 reflected board in Alpha notes | deferred in Paper 3 register | no invented third type |
| **Approximate prestige grouping** | Rough outline of a chaotic process, then refine (U34–U38) | RCF-P3 deferred | not in papers | needs approximation relation + cost; do not restart Fluid as a substitute |
| **Fiving / FIVE_IS_SAFE** | Several distinct uses: 0/5 weave; A/B one level up; 5→7 immediate with 6 as mid-seam; clamp key; A5→B6→C7 Double-Stamp | prestige file; glossary ten-cycle; FIVE.future separately | papers have shortest-future search unnamed as FIVE; Atlas has +5 mod 10 | **do not collapse** FIVE.future, +5 mod 10, Double-Stamp, and “inverse 5” |
| **Doing 3 with 2/4** | Different routes to the same landing; route can still matter (U25) | Atlas local charts; curve-frame historical audit | fragment in Atlas code, not labeled in papers | not a complete definition of the phrase |
| **Every 3 is a 9** | Direct user: every 3 is inside a 9; every 9 has three 3s; 7 most complete before carry | prestige file | unlocated as a quantified law in papers | grouping ≠ historical origin |
| **Inverse 5/6/7/8** | Recalled operator family | unlocated as one table | absent | **OPEN** |
| **Waiting on 1/3/5/7** | Recalled waiting/holding | Atlas handoffs at 3,5,7 only; no waiting mechanism, no handoff at 1 | absent | **OPEN**; mismatch with recalled four-item sequence |
| **Seam Zero 6\|4; −0.6/+0.4; residual −0.2** | Oriented translator `τ(x)=(6-x)/2`; +0.4 and −0.6 same phase mod 1, different covering positions; −0.2 a *contrast* | `recovered-concepts/ZERO-AND-RAILS.md`; Audit105 movable cut in foam-dev | ±1/2 is in Manifesto; this shifted family is **not** | “math rail vs physics rail” phrase not located |
| **Formula / graded scar cube** | Binary Möbius/zeta on `{0,1}^n`; inverse `f(S)=∑_{T⊆S} r_T`; grade-k receiver kernel; general finite-product Newton (Thm C.3) | QR `RPRM_GRADED_SCAR_CUBE_02/NOTE.md` via `CUBES-AND-PI-CURVES.md`; LawCube/RelationForge at `C:\github` | four-corner square is in Manifesto, **not** the n-cube | integrated cube-with-vacant-center not assembled in public papers |
| **Ternary checking cube** | Full-line vs center-only second-difference kernels; n=3 nullity 4 vs 14 | same recovery | deferred in Paper 3 (RCF-C2) | don’t call a central ray panel complete |
| **Full Zip / dimensional ladder** | Q0–Q4 by prior-artifact byte handoff | QR Full-Zip; glossary capability grade | deferred | Tile(X) ↛ X without adapter |
| **Circle Compiler / “true pi”** | Equation for curves, not a number; metric-addressed circles, phase+winding | `CUBES-AND-PI-CURVES.md`; later `PI_CLOSURES.md` in BSD67 foundations import | conventional trig in Atlas/Lens Lab only | not an alternate Euclidean π; conversation ID of Circle Compiler still missing |
| **Flexible Bishop-frame curve** | Two bend functions + initial frame; nonzero constant planar bend → circle | same; user export lines cited in Paper 3 plan | theorem deferred | distinct from Circle Compiler |
| **Dark World** | William’s non-mystical term for a declared reflected/negative carrier at 0, −1/2, and below | **not in live public docs**; only in consolidation *source snapshots* of an Aug 13 Alpha context guide (`research/ym2_rail_closure/accepted/sources/…MASTER_ASSISTANT_CONTEXT_GUIDE…`) | not in papers | name does not choose negation vs reciprocal vs complement vs order dual |
| **Prime / shadow five** | User speech U12: “shadow five — shadow prime five … to the super seven … super nine … Prestige 1” | process evidence in prestige file | not a live module | do not treat as a number-theory theorem |
| **Liar → teacher; 7/8; Hamming** | Movable vacant student; three calibrated checks generate seven; 28/35 triples separate F₂³ | `research/liar-teacher-formalization-2026-09-12/THEORY.md` P1–P11 | **priority next-paper candidate**; existing 3+1 parity is nearby but not this | general SAT/cost OPEN |
| **Expand/compress/expand; −3/5 stack** | Growing-carrier operational descent; Audit99 gcd split factors 2,3,2; −0.6/+0.4 additive stack | `research/expansion-compression-2026-09-12/` | substrate already published; connected application is candidate | uniform resource-controlled recurrence OPEN |

### 3.3 Executable Python/Lean kernel (what code actually implements)

`CONTENTS.md` is honest: a glossary name is not an implemented solver.

| Module | Path | Boundary |
|---|---|---|
| Finite core | `rprm/core.py` | nominal sorts, finite relations, fibers, converse, composition with middle witnesses, occurrence attachment, det/nondet/rational-stochastic quotient checks, refinement, lift–land, vacancy swaps, in-process FLICK. Atoms: int/str/None/tuple/frozenset — **not bool/float** |
| Futures | `rprm/futures.py` | shortlex least separating word, canonical future quotient, least stable refinement. Finite deterministic partial machines |
| Proof donut | `rprm/proof_donut.py` | independent finite certificates; no import of core PASS flags |
| Fixed-gap | `rprm/fixed_gap.py` | per-aperture integer decision |
| Process-mechanics adapters | `rprm/process_mechanics/{context,candidates,intervals,measurement}.py` | Paper 2 companion contracts |
| Lean | `lean/Relations.lean`, `lean/Carrier.lean` | 11 + 9 declarations; Lean 4.22.0; only `Init`; axioms among `propext`, `Quot.sound`, `Classical.choice` |
| Unification checker | `checks/unification.py` | bounded executable of U01, not the general Lean theorem |
| Root runner | `verify.py` | 13 Python + 7 Node jobs default; `--lean` adds formal; `--python-only` omits Node. Receipts in `.artifacts/` are not source |

### 3.4 Dark World, inverse ops, prime shadows, ternary grids, dimensional ladders — first-party status

These were named in the catch-up brief because they appear in skills and Alpha memory. In **this** repository:

- **Inverse ops:** live and precise as converse / inverse / retraction / TRACEBACK.preimage / aperture rotation. There is **no** unified “Dark World inverse” operator in `docs/` or the Manifesto. The Alpha guide (snapshot only) warns that “Dark World” does not choose among additive negation, inverse navigation, reciprocal, complement, divisor shadow, or order dual.  
- **Prime shadows:** user metaphor in U12; square-frontier and Fermat auxiliaries are the live prime mathematics; no `prime_shadow` module.  
- **Ternary grids:** recovered as `{-1,0,1}` instance of Newton interpolation and as ternary checking kernels; LawCube F2/F3 tables are external private tooling (`C:\github\LawCube`). Not in Manifesto as a cube product.  
- **Dimensional ladders:** glossary capability grade + Full Zip historical constructor + PROMOTE.capability. Papers do not execute Tile→Board→Atlas.  
- **BSD-related work:** exists in bulk under `research/bsd-*` (campaigns numbered into the 90s as of this workspace). **Noted, not deep-dived.** Some BSD packets export reusable *foundation* lemmas (e.g. graded division / precision Theorem G in `research/bsd-operational-closure-67/`, imported into Paper 3 as AD-R9 with explicit non-BSD-arithmetic attribution).

---

## 4. Proven vs tested vs conjectured vs interpretive

### 4.1 Counted evidence (different counts, different objects)

From `README.md`, `docs/formal-proofs.md`, Manifesto evidence appendix:

| Count | What it is | What it is not |
|---|---|---|
| 73 | written theorem/proposition/lemma/corollary statements in `MANIFESTO.md` | 73 new theorems; 4 are restated opening statements |
| +14 | supplementary Fermat study | does not restore unrestricted independent FLT |
| 87 | 73+14 including restatements | not 87 Lean theorems |
| 20 | Lean declarations | not coverage of U01, O07 bound, O08R, geometry, or implementations |
| 9 | executable experimental packs in `experimental/README.md` | not including Shadow Lens, process-mechanics kits, or RCF01 |
| 3 | unexecuted research-packs (folding dynamics, BRCA1, immune) | not extra executable packs; no biological result |
| Handbook F 24/24, E 16/16, D 79/80 | bounded comprehension assessments of specified handbook versions | not controlled improvement or universal comprehension |

### 4.2 Written-proof core (should be treated as the project’s mathematical spine)

- Question factorization and operational factorization (Theorems 1–2). Ancestry: quotients and Moore refinement; the project’s contribution is the connected organization around apertures, enabledness, failure tags, and receivers.  
- U01 faithfulness for supplied many-sorted finitary first-order structures. **Does not** formalize all of mathematics, higher-order semantics, or unknown source truths.  
- U02–U04 transport, with listed hostile failures (non-injective encodings, unguarded target quantifiers, extra middle witnesses, merged enabled/disabled states, equal support ≠ equal kernels).  
- Finite future quotient, n−1 distinguishing bound, least stable refinement — written; Lean has the operational-fold characterization and word transport, not the bound.  
- Four-corner interpolation and its two hostile grammar/coverage failures.  
- Affine aperture chart including collapsed endpoints.  
- Square-frontier sieve continuation (established sieve reasoning, RPRM-packaged).  
- Bounded Fermat III.2.1 and per-tuple fixed-gap decision.  
- Selected ideal mechanism inverse-fiber arguments (III.3); ray slab + INHERIT-style reuse (III.4); symbolic music fibers (III.5); finite learning/shape search (III.6); CA periodicity vs prime indicator obstruction (III.7).  
- Two-path χ receiver and marker-channel facts **as consequences of the supplied quantum model**, not new QM.  
- Radial Newtonian receiver; Schwarzschild horizon as causal, not as a discarded coordinate.

### 4.3 Formal (Lean) — exact list

`docs/formal-proofs.md`: Relations — identity L/R, compose assoc, converse involutive, converse compose, graph identity/compose, graph converse inverse, retraction_section_injective, aperture_backward_forward, aperture_forward_backward. Carrier — factorization_iff, decoder_unique, toReachable_onto, option_map_eq_iff, operational_fold_iff, run_commutes, run_defined_iff, future_preserved, fiber_conditions_preserve_all_futures.

Replay: `python -I -B checks/formal.py --lean /path/to/lean`. Without `--lean`, aggregate receipt records `NOT_RUN`.

### 4.4 Finite tests (representative, not a theorem dump)

`docs/verification.md` is the live table. Hostile cases the checks actually exercise: lost middle-witness identity, independent marginals misread as joint, quantification outside encoded image, present-preserving but future-changing representation, failed vs successful partial execution, stale candidate (ABA), malformed/aliased carriers, mutable string subclasses in action tables.

Independent dual implementation: proof-donut quotient vs core quotient. Agreement is implementation evidence, not circular soundness.

Browser/UI for Atlas, Rule Lab, Lens Lab, Music Lens: model tests exist; **actual browser interaction remains NOT_RUN / NOT_RUN_UI** except a dated Music Lens review that still does not enter the aggregate as UI coverage.

### 4.5 Research-lane written proofs that are *not* the public book

Treat these as scoped research, often with independent agent review, **not** as Manifesto theorems and **not** as continuum/physical closures:

- **YM2 covering argument** (`research/ym2_covering_argument/`): for admitted finite open SU(2) lattice graphs, d=2 or 3, all spins, actual interacting vacuum, `m=2(d−1)`, `r=β/(αℏ²)`, `0≤r≤1/(48m)` ⇒ `gap_physical ≥ αℏ²/2`. Bound independent of cell count. Written proof + audits + bounded corroboration. **Not** a continuum Yang–Mills mass-gap solution; publication on hold.  
- **YM2 connected vacuum:** two-cell actual vacuum is not a function of two separate plaquette traces on a stated r-interval; signed witness for missing joint orientation. Continuum mass gap OPEN.  
- **YM2 operational seam, rail closure, signed differences, etc.:** a family of 12 Sep 2026 packets with deliveries under `research/ym2-*-20260912-delivery/`.  
- **Liar/teacher THEORY.md P1–P11:** written proofs + complete three-bit census + Hamming dual identification (simplex [7,3,4] dual to Hamming [7,4,3]). Affine projection P10 polynomial for *explicit affine* blocks; P11 non-affine OR3/exactly-one hostile cases. P=NP **OPEN**.  
- **Expansion-compression:** operational descent on growing carriers is O05 applied to a stage family (not new); −3/5 stack and Audit99 2-3-2 splits are exact small models; 34,936 assertions claimed in the backlog note (finite). Uniform scaling OPEN.  
- **RCF01 cube/fiving bridge:** development connection; 12 named checks covering all 256 Boolean 3-cubes and 65,536 ordered pairs for specified arithmetic; historical donors not rerun. Quotient-algebra vs subalgebra correction retained in R1/R2.  
- **AD1 (C2):** 30 named cases + 126 aggregate bags; **conventional tie**; no protocol-benefit claim (`research/rprm-consolidation-c2-20260912/ad/AD1_RESULT.md`).  
- **Fluid F1:** tall/flat placement refutes volume+geometry summary for a 300-frame breach bit — **useful scoped result**.  
- **Fluid F2 Layer B:** **refuted** by a two-cell support-injection hostile scene (`research/fluid-f2-review-20260912/REVIEW.md`). Replay of 53 original rows still matches; general NO certificate is false. Preserve counterexample beside surviving Layer A.  
- **Paper 3 AD-R3 etc.:** written proofs in an unreleased 13-page draft; `check_examples.py` 75,445 assertion *calls* (not 75,445 experiments). Reviewer accepted written arguments within hypotheses; not Lean.

### 4.6 Conjectures, OPEN goals, interpretations

| Item | Grade |
|---|---|
| Unrestricted independent Fermat | OPEN (established FLT is comparison, not a premise that completes the independent goal) |
| Physical relational layer exists in nature | interpretation / open experiment |
| Return-depth = black hole | OPEN physical bridge (`docs/origins.md`) |
| Gravity source `Psi` independently yielding radial `Phi` | encoding vs derivation distinguished; latter OPEN |
| Folding dynamics / BRCA1 / immune packs | unexecuted proposals |
| General SAT compression / P vs NP | OPEN; affine island exact; mixed residual not polynomially bounded here |
| Prestige three-type taxonomy | OPEN naming/definition |
| Inverse 5/6/7/8 and waiting 1/3/5/7 | OPEN |
| Universal Tile–Board–Atlas ladder | not claimed; family definition only |
| YM continuum mass gap | OPEN (lattice covering is a different theorem) |
| Full BSD | OPEN (explicitly; E5 curve-specific work is a different, BSD-lane claim — not expanded here) |
| “RPRM protects you from numerology” (U35) | authorial hope; the actual method is: freeze carrier/receiver and demand a preservation equation. Interpretation, not a theorem that every pattern is safe to follow |

### 4.7 Process Mechanics claims (Paper 2)

Ten retained claims in `papers/process-mechanics/CLAIM_ID_MANIFEST.json`, statuses mostly `ACCEPTED_SCOPED`. Lanes: circuits (continuation, estimation, sufficient state), intervals, partial measurement / cancer-figure reconstruction. Evidence includes sufficient-state and hard-decision **nulls**, model-conditional successes, and a **partial** reconstruction. Teaching demos in `experimental/process-mechanics/` are not the historical 220-origin noiseless panel. Protein-folding and BRCA1 remain unexecuted prospects (Sections 8.1–8.2 of that paper).

---

## 5. Map of the repository

### 5.1 Live canonical core (treat as the public project)

```text
README.md, MANIFESTO.md, RPRM-Manifesto.pdf, DOCUMENT_BUILD.json, CITATION.cff
AGENT_HANDBOOK.md, AGENTS.md, LAYPERSON_GUIDE.md, CONTENTS.md, CONTRIBUTING.md
LICENSING.md, LICENSE, LICENSES/, THIRD_PARTY_NOTICES.md
docs/{core,operations,glossary,unification,formal-proofs,verification,
      relational-layer,concepts,origins,proof-donut,fermat,fermat-study,references}.md
rprm/{core,futures,fixed_gap,proof_donut}.py  + process_mechanics/
lean/{Relations,Carrier}.lean, lean-toolchain
checks/  examples/  verify.py
atlas/   figures/   tools/typesetting/
experimental/{primes,ray-tracing,music,protein-folding,context-communication,
              two-path-lab,rule-lab,lens-lab,music-lens}/ + README.md
experimental/process-mechanics/     # Paper 2 companion; extra to the “nine”
research-packs/{folding-dynamics,brca1-function,immune-mechanisms}/
agent-tests/                        # handbook assessments A–F
papers/process-mechanics/           # Paper 2 canonical
recovered-concepts/                 # stable KB entrance + backlog
```

This is what `README.md`’s “Read and use” table points at. Forks are expected to start here (`CONTRIBUTING.md`).

### 5.2 Live but easy to miss (canonical-adjacent)

| Path | Why it is easy to miss |
|---|---|
| `experimental/shadow-lens/` | Full inverse-shadow playground with MODEL.md and Node tests; **omitted from the nine-pack index** |
| `rprm/process_mechanics/` | Paper 2 adapters; CONTENTS mentions them, experimental README’s nine-pack table does not |
| `docs/fermat-study.md` | Was in the book; now supplement after v1.0.1/1.0.2 scope correction |
| Atlas 2/4/6/8 charts | Implemented in JS, only collectively referenced in Manifesto III.3 |
| Operator names FIVE/TRACEBACK/PROMOTE/SEAL/INHERIT/FLICK | Live in `docs/operations.md`; papers often use ordinary English |

### 5.3 Recovered-concepts (stable memory, not a second Manifesto)

`recovered-concepts/` is the **declared** entrance for recalled concepts (`AGENTS.md` lines 9–11). Files:

- `README.md` — routing table  
- `NEXT-PAPER-BACKLOG.md` — **live** candidate additions; does not authorize publishing  
- `PAPER-COVERAGE-AUDIT.md` — **frozen 11 Sep 2026** snapshot at HEAD `4f5c814`  
- `PRESTIGE-AND-NUMBER-OPERATIONS.md`, `ZERO-AND-RAILS.md`, `CUBES-AND-PI-CURVES.md`, `SPINE-CARRY-AND-CHECKING-RECORDS.md`  
- `RPRM-CONCEPT-RECOVERY.md`, `ORIGINAL-CONVERSATION-PASSAGES.md`

Historical language is kept distinct from later reconstruction. “Not in paper” ≠ “no related mathematics was published.”

### 5.4 Core-recovery formalization (RCF01) — live research home, not a paper edit

```text
RPRM-CORE-FORMALIZATION-01/          # assignment package, concept register, bridge note
research/core-recovery-01/           # anti-forgetting home
research/core-recovery-r1/           # portable export + composition audit
research/core-recovery-r2/           # family/map-interface/aggregate-runner guards
experiments/core_recovery_bridge_01[_r1|_r2]/
```

README and CONTENTS: **not** a tenth executable pack; **not** a change to the published paper. Concept IDs must not disappear in later consolidations.

### 5.5 Consolidation dumps (C2, YM2 deliveries, BSD catchup)

These are **research debris with provenance**, often ZIP+extraction twins. Do not treat nested `source_snapshots/MANIFESTO.md` as a newer Manifesto.

| Cluster | Role |
|---|---|
| `research/rprm-consolidation-c2-20260912/` (+ `-input`, `-delivery`, `.zip`) | 12 Sep F1/AD1/YM1 return; `PAPER_ROUTING_NOTE.md` forbids manuscript edits |
| `research/ym2_*` and `research/ym2-*-20260912-delivery/` | Yang–Mills lattice packets; covering argument is the headline non-BSD science candidate |
| `research/fluid-f2-review-20260912/` | Independent evaluation; Layer B refutation |
| `research/nks-rprm-deep-dive-21/` | NKS as construction catalogue; derived finite examples; not a Wolfram-endorsement of RPRM |
| `research/liar-teacher-*` | recovery + formalization + SAT pilot |
| `research/expansion-compression-2026-09-12/` | connected note across Audit99/116, YM log-density, BSD E5 coverage *as analogy of obligation* |
| `research/bsd-*` (dozens, through ~92 plus catchup extracts) | **BSD campaign archive**; verification-extracts even copy `docs/` — ignore those copies as live docs |
| `research/closure-{master-07,bridge-08,seam-09}/` | earlier closure packets (BSD-adjacent numbering) |
| `research/cross-closure-01/` | **untracked as of this catch-up**; P-vs-NP-related parallel pilot handoff; “does not change the live BSD mission” |
| `research/bsd-public-catchup-*` | snapshots of the public repo used to catch BSD threads up — **duplicates of canonical docs** |

`PAPER_ROUTING_NOTE.md` (C2): F1 belongs with the fluid study; AD1 is a methods specimen (conventional tie); YM1 is a bounded Maxwell-mode note, **not** a mass-gap claim. “No assumption is made that these three lanes belong in one paper.”

### 5.6 Paper 3 worktree (untracked)

`papers/absolute-distinction/` — private manuscript, `manuscript.tex`, reading PDF, concept register, recovered_seeds copies. Explicitly: no released paper, BSD result, solver pilot, Spark job, or registry was changed. Next step is an **author-facing** pass, not more recovery.

### 5.7 Git history: what was started, corrected, abandoned

Important **public** commits (oldest last among the meaningful ones):

| Commit | What it did |
|---|---|
| `04195a3` | Assemble Manifesto and finite reference tools |
| `32944af` | Expand review book and companion package |
| `9705d95` | Clarify physical proposal; focused research comparisons |
| `54b8c8c` | Author afterword; layout |
| `b68b177` | First edition / publication links → v1.0.0 |
| `e15213e` / `aaa3dcf` | Lens Lab; Music Lens |
| `3b4fcdc` | **Failed Fermat move:** close application by crediting established FLT |
| `a748367` / `79c78fa` | **Correction:** restore independent Fermat scope; move detailed study to supplement (v1.0.1–1.0.3 story) |
| `4f5c814` | Publish Process Mechanics 0.3 |
| `9b5e132`…`5190182` | daily `autosync` snapshots (research dumps landing on main) |

**Branches:** `main` (active); leftover `codex/fermat-closure` and `codex/fermat-independent-correction` (the Fermat episode). No other feature branches on the remote listing.

**Abandoned / withdrawn in public:** using established FLT as a closure of the *independent* research goal. The bounded theorem and certificates were kept. This is a model of how the project wants to be judged: it withdrew an overclaim rather than laundering it.

**Not in this git as first-class projects, but referenced as donors:** `C:\github\RPRM-foam-development` (Foam/Alpha implementation head), `C:\github\RPRM Alpha` (skill says this is **not** the OneDrive research head), `C:\github\LawCube`, `C:\github\RelationForge`, `C:\github\RPRMLexicon` (operational number translator), OneDrive Quantum Research tree. Skills `rprm-math-lenses` and `rprm-workbench` still describe Alpha (`knowledge/lenses.json`, `atlas/CLAIM_LEDGER.md`) — those files are **not** the RPRM-open layout. Using them inside RPRM-open without checking for `math-discoveries/` / `knowledge/lenses.json` is a newcomer trap.

### 5.8 GitHub and sibling repos (authenticated `gh`)

RPRM-open: public, issues disabled, no visible PRs, four Manifesto releases in one day (7 Sep 2026). Description: “Typed mathematical relations, executable examples, proof checks, and mechanical motion atlases.”

Related **private** William repos visible to this account (names only; contents not poured here): `RPRM-Alpha`, `rprm-context`, `rprm-fluid-adjacency`, `rprm-protein-folding`, `rprm-cancer-research`, `rprm-water`, `rprm-orc-fortress`, plus NARI/NariTalk/NariOS family. Process Mechanics kits in RPRM-open look like public, scoped extracts of some of that private scientific work.

### 5.9 What is *not* a theorem because it lives in a dump

Nested copies of `docs/core.md` under `research/bsd-public-catchup-*` and `research/ym2-*-delivery/**/source_snapshots/` are **frozen extracts**. Canonical is repo-root `docs/`. The Aug 13 Alpha context guide (Dark World, Flick-as-runtime, scaling recurrence) is historical workspace instruction, not the public AGENTS.md.

---

## 6. Forgotten or unfinished work that still looks useful

“Forgotten” here means: live enough to reopen, under-indexed by README, or deferred with a concrete reopen trigger. Not a recommendation of the next campaign.

### 6.1 High-value, already typed, mostly unused by the papers

1. **Liar/teacher seven/eight + Hamming dual + movable vacancy** — `research/liar-teacher-formalization-2026-09-12/THEORY.md` + `SAT-PILOT.md`. Written proofs, complete census, hostile “any three” failures (7 dependent triples), distinction between adding a free toggle and adding Hamming parity. Backlog already marks this as **priority paper addition**. Domain: binary linear carriers as specified. Grade: written + finite. Missing: general SAT.  
2. **Graded scar cube / finite-product Newton** — recovered in `CUBES-AND-PI-CURVES.md` from QR 19 Aug note. Actual all-finite-n inverse, grade-blindness, hostile basis change that creates fake grades. Strongest “formula in any dimensionality” donor. Not in Manifesto beyond the 2D multiaffine square.  
3. **Seam Zero / movable cut / −0.6/+0.4 stack** — `ZERO-AND-RAILS.md` + expansion-compression §2. Exact translators; Audit105 111,100 relocalizations (historical receipt, not rerun here). Papers have ±1/2 only.  
4. **Shadow Lens** — inverse geometry with complete finite source count 181,447 and a second-light height separator. Better teaching of MANY fibers than several Manifesto pictures, and it is already executable. Index gap.  
5. **Atlas local charts 2/4/6/8 and ten-cycle half-turn** — the only implemented numeric fragments of “doing 3 with 2/4” and arithmetic fiving. Paper-only readers miss them (`PAPER-COVERAGE-AUDIT.md` item 3).  
6. **NKS deep-dive derived examples** — `research/nks-rprm-deep-dive-21/REPORT.md`: ring constraint fiber MANY(4) iff 4|N else NONE; Rule 184 flux conservation. Ready-made hostile `N=6` (local windows sat, global NONE). Candidate: local-constraint compiler as Tile-style completion.  
7. **Expansion/compression commuting equation** — already O05 on a stage family; the missing paper-sized piece is teaching *semantic closure ≠ resource bound*, with the 2,3,2 Audit99 example and the −3/5 stack.  
8. **RCF01 envelope vs glyph vs full state** — prestige as acquired access, tested as whether a promoted envelope supports changing operation sets. Implementation NOT_RUN for full envelope; R2 added guards. Paper 3 models a restricted DAG/recipe version (AD-D3/R5).  
9. **Proof-donut as a reusable certificate language** — implemented and mutually checked; still under-used as the way to land recovered constructions.  
10. **Process Mechanics interval composition (76 law-partition comparisons) and hard-decision nulls** — already in Paper 2; still the cleanest “right Boolean answer, wrong scientific object” exhibit.

### 6.2 Unfinished with a stated reopen trigger

| Seam | Reopen when | Path |
|---|---|---|
| Third prestige/rebirth name | a specific original taxonomy or tier law is supplied — **do not invent** | prestige file U33; Paper 3 register RCF-P2 |
| Inverse 5/6/7/8; waiting 1/3/5/7 | an operation table or distinguishing question | backlog; Paper 3 RCF-N1 |
| Circle Compiler conversation ID; metric/measure theorems | primary source or deferred constructions enter a manuscript | CUBES-AND-PI-CURVES; Paper 3 PI1a |
| Bishop/moving-frame theorem | primary proof/gauge comparison | Paper 3 PI1b |
| FIVE_IS_SAFE Double-Stamp graph | typed restart/splice adapter, not a new graph rewrite | RCF-F2 |
| Mixed SAT residual / piece-union blow-up | economic exact representation of non-affine pieces; fair CNF/XOR baseline | THEORY P11; SAT-PILOT; cross-closure-01 |
| YM remainder summability / continuum | a new lens that preserves the covering certificate’s geometric margin | `ym2_covering_argument/NEXT_OBLIGATION.md` |
| Fluid Layer B | a bound that survives support-injection; until then B-only NO is UNRESOLVED | F2 REVIEW.md |
| Independent unrestricted Fermat | an invariant covering remaining tuples or a same-target integer descent | `docs/fermat-study.md` |
| Physical origins / return-depth bridge | variables, map, source equations, distinguishing measurement | `docs/origins.md` |
| Tile–Board–Atlas executed instance | one reproducible Board including a failed landing | glossary; backlog |
| Handbook assessments as learning evidence | new held-out questions; isolation actually enforced | `agent-tests/README.md` |

### 6.3 Abandoned or correctly stopped

- Fermat-by-inheritance (v1.0.1 withdrawn).  
- Presenting PROMOTE.capability + PROMOTE.state as the remembered three types of “ones” (`PAPER-COVERAGE-AUDIT.md`).  
- Treating Lens Lab’s phase-wave sine as the moving-frame curve theorem (the pack itself denies this).  
- C2’s instruction not to merge F1, AD1, YM1 into one paper.  
- Spatial-display prototype omitted from the Atlas candidate (`CONTENTS.md`): scalar/vector output and discontinuity propagation lacked a consistent contract.  
- Centered translator hub / cube-sphere experiment folders in QR: prefreeze designs only (`CUBES-AND-PI-CURVES.md` item 7). Rotated-face abduction atlas combined bench **not executed**. Component theorems still stand.

---

## 7. How the project wants to be judged

### 7.1 Explicit non-claims (the refusal list)

Collected from README, Manifesto evidence appendix, core §1, unification closing, experimental README, origins, relational-layer:

- Not a claim that every mathematical problem has been solved.  
- Not a theory of everything, new force law, or cosmic-origin mechanism.  
- Not a reconstruction of logic or set theory from an untyped primitive.  
- Not a decision procedure for every theorem or a faster solver for every instance.  
- Expressibility in RPRM notation does not solve a question or prove a cheaper algorithm.  
- A new name for a familiar construction is not a new theorem.  
- Example observations are not unbounded theorems, new physical laws, or evidence of unstated relations between unrelated systems (`AGENTS.md`).  
- Finite PASS does not enumerate every physical possibility.  
- Hash / receipt / layout review / handbook score ≠ proof.  
- Cancer relevance ≠ assay score ≠ tumor/treatment/individual risk.  
- Symbolic music correctness ≠ perception. Atlas traces ≠ load-bearing machines. Rule Lab color match ≠ primality.  
- Closure of a description ≠ hidden variable exists ≠ forever inaccessible.  
- Prestige / Dark World / “true pi” names ≠ cryptography, mysticism, or a new value of π.

### 7.2 Hostile cases the project considers load-bearing

These are the *style* of test it wants, not an exhaustive list:

| Hostile pattern | Canonical exhibit |
|---|---|
| Independent marginals ≠ joint fiber | `{(0,0),(1,1)}` vs `{0,1}×{0,1}` |
| Extra middle witness invents a path | U03 empty source relations + extra `u` |
| Unguarded target quantifiers | U01 image guards; “every x equals a” |
| Merge enabled with disabled | operational fold condition 2 |
| Future-sufficient but not updatable | `{p,q,r}` example |
| Two opposite corners / enlarged grammar | four-lane interpolation |
| Shared-source “liars” | three copies of one wrong report |
| `2^11−1 = 2047 = 23·89` | compact description ≠ cheap/true primality |
| n=2,s=1,d=1 Pythagorean ONE vs fifth-power NONE | fixed-gap is a decision, not uniform emptiness |
| Support-injection in fluids | F2 Layer B refutation |
| Affine hull of OR3 | SAT P11 false solutions |
| Dependent check triple `{a,b,a+b}` | 7/35 Hamming/simplex failures |
| Retract then permute off-image | lift–spin–land identity failure |
| ABA / stale parent | FLICK / O14 |
| Incomplete INHERIT masks | node reads `(a,b)` but declares only `a` |
| Equal support, unequal kernel rows | `(1/2,1/2)` vs `(1/4,3/4)` |
| Endpoint compiler vs trace | `a` vs `aa` on a singleton state |

`CONTRIBUTING.md`: when extending a claim, include a worked example **and** a hostile case; keep written proof, machine-checked proof, and finite computation distinct.

### 7.3 Fermat as a judgment exhibit

The project *tried* to close an independent FLT-style goal by inheriting the established theorem, then **withdrew** that framing within hours (releases v1.0.1–v1.0.3 on 7 Sep 2026). What remains is a bounded written theorem, a per-gap decision procedure, and an honest OPEN. That sequence is first-party evidence of the intended epistemic standard, more informative than any slogan about numerology.

### 7.4 Author afterword vs mathematical contracts

The afterword hopes RPRM helps distinguish numerology from testable relationships and that more people can contribute to mathematics. The contracts that actually implement that hope are: freeze the hypothesis family before looking; declare the receiver; return OPEN rather than NONE on timeout; preserve counterexamples; do not promote scout prose (`rprm-math-lenses` claim ceiling). Those are auditable. The hope is not.

---

## 8. Open problems and paper backlog besides BSD

BSD is noted as an active, bulky research lane (`research/bsd-*`, currently through projection-bridge-92 in the working tree). It is **not** developed here. Non-BSD candidates already named by the project:

### 8.1 Declared next-paper backlog (`recovered-concepts/NEXT-PAPER-BACKLOG.md`)

**Priority:** liar/teacher growth, handoff, Hamming.

| Claim-sized addition | Evidence now | How the backlog says to write it |
|---|---|---|
| Teacher panel preserves Q iff Q constant on panel fibers; futures need P3 | THEORY P1–P3 | application of existing quotient math, not a new theorem |
| 28/35 triples preserve all eight states | P4–P6 complete census | include a successful swap **and** a failing swap |
| 4→8 by independent toggle; paired-quartet replacement; moving anchor | P7, P9b | candidate realization of history; not exhaustive of original meaning |
| Seven teacher-answer words = simplex code, dual to Hamming-7; Hamming-8 vs free toggle | P9–P9a | credit coding theory |
| Compact affine boundary messages | SAT-PILOT, P10 | restricted affine result; general SAT OPEN |

**Other backlog rows:** prestige taxonomy linked to current PROMOTE without fake third type; shifted −0.6/+0.4 with units (not implied by affine chart alone); select a proved cube construction rather than the remembered integration; “true pi”/Circle Compiler at precise domain; fiving terminology map; inverse/waiting dictionary; one failed-landing Tile/Board/Atlas instance.

Already in papers, do not relist as missing: C-shaped return/depth, constructor/width/carry, centered halves, basic three-plus-one.

### 8.2 Paper 3 deferred list (editorial, 16 Sep 2026)

From `papers/absolute-distinction/CONCEPT_REGISTER.md` and `REVIEW_NEXT_STEPS.md`:

Deferred: full ternary-cube exposition; teacher/Hamming panel (supported candidate to *replace* a precision example if it teaches task revision better); moving-frame theorem; metric Circle Compiler; approximate Prestige; missing third prestige category; complete inverse/waiting dictionary; integrated Tile/Board/Atlas; cross-domain experimental advantage.

Included already in the draft: AD policy; prestige as retained-access DAG; occurrence vs value; Boolean cube + fiving adapter; finite future budgets; winding/precision including recovered Theorem G (AD-R9, **no BSD arithmetic**); own-one/calibration.

Next revision the draft itself asks for: author-facing meaning pass; decide **one** additional pre-BSD example (teacher/Hamming **or** ternary cube); then release-candidate discipline. “Do not expand recovery indefinitely.”

### 8.3 Other non-BSD scientific/math candidates noticed in-tree

| Candidate | Path | Claim ceiling already on the folder |
|---|---|---|
| YM2 covering gap bound on finite open SU(2) lattices | `research/ym2_covering_argument/` | not continuum mass gap; publication on hold |
| YM2 connected vacuum / operational seam / rail / signed differences | `research/ym2_*` | model-conditional; remainder control often OPEN |
| C2 YM1 Maxwell-mode energy transfer | `research/rprm-consolidation-c2-20260912/yang_mills/` | not YM mass gap; not cube-arithmetic Hamiltonian |
| Fluid F1 dynamic summary refutation | C2 `fluid/F1_CLOSEOUT.md` | placement ≠ volume; no velocity-only repair theorem |
| NKS local-constraint compiler / flux invariants | `research/nks-rprm-deep-dive-21/` | derived examples finite; book’s physical hypotheses remain Wolfram’s |
| Cross-closure SAT compression pilot | `research/cross-closure-01/` | P vs NP is motivation, not deliverable; untracked handoff |
| Independent Fermat unrestricted | `docs/fermat-study.md` | OPEN |
| Unexecuted molecular packs | `research-packs/` | still unexecuted; Paper 2 already points at them |
| Spatial-display Atlas successor | `CONTENTS.md` | needs a consistent contract first |
| Operational-number translator / nines-flip Klein four | skill points at `C:\github\RPRMLexicon` | **outside this repo**; do not reconstruct from memory |

C2 routing is explicit that F1, AD1, YM1 need not share a paper.

---

## 9. Where a newcomer still gets lost

This section is observational, from the shape of the corpus itself.

### 9.1 Two (soon three) papers, one name, several DOIs

RPRM names a framework, a physics motivation, a 140-page book, a 41-page methods paper, an unreleased distinction paper, nine packs, Atlas, Lean, and a BSD/YM research mill. Newcomers who read only the PDF miss FIVE/TRACEBACK/FLICK names, Atlas numeric fragments, recovered cubes, and Shadow Lens. Newcomers who read only `research/` will think RPRM *is* BSD.

### 9.2 “Pressure” and “Dark World” vs the actual math

The acronym invites a physics theory. The live math is typed relations, fibers, and operational quotients. Pressure is model-dependent. Dark World is an Alpha dialect for typed negative/reflected carriers, almost absent from the public book. Skills still speak Alpha (`knowledge/lenses.json`). In RPRM-open the registry is `recovered-concepts/` + `docs/glossary.md`.

### 9.3 Equal numerals, many carriers

Centered half, unit-total `(1/2,1/2)`, Seam Zero’s raw 5 vs normalized 1/2 vs locator `ONE(6)`, prestige 1 vs ordinary 1, Hamming 8 vs free-toggle 8 vs simplex 8, FIVE.future vs +5 mod 10 — the project’s whole point is that these are different, and it is also the main way readers (and agents) collapse them.

### 9.4 NONE vs OPEN vs REJECT vs admission error

Unfinished search looking like failure is the most common contract violation the handbook warns about. Empty fiber about a source not known to be in H is not a fact about the world.

### 9.5 Evidence-count theater

73 / 87 / 20 / 24/24 / 75,445 / 34,936 / 181,447 are different kinds of numbers. The project says this repeatedly and still invites miscounting. Formal 20 ≠ written 73. Assertion calls ≠ experiments. Handbook scores ≠ theorems.

### 9.6 Live docs vs nested snapshots

`research/bsd-public-catchup-*/verification-extract/repo/docs/core.md` looks like core.md. It is a dated extract. Same for Manifesto copies under YM2 deliveries.

### 9.7 Index holes

Shadow Lens not in the nine-pack table. Paper 3 untracked. `cross-closure-01` untracked. Local git tags missing v1.0.3 while GitHub and CITATION.cff use 1.0.3. Manifesto evidence appendix still says the default runner requests **seventeen** suites (13 Python + 4 Node); `docs/verification.md` now says **20** jobs (13 Python + 7 Node, including Lens Lab and Music Lens). The book appendix lagged the runner. Trust `docs/verification.md` for current jobs.

### 9.8 Recovery language vs contracts

William’s speech (prestige, reincarnation, shadow five, waiting on odds) is preserved verbatim and is often exploratory, self-correcting, and explicitly uncertain (U10, U16, U25, U33). Assistants repeatedly over-identified these with the nearest existing operator. The first-party rule is: keep user meaning, historical model, and draft model in separate columns (Paper 3 concept register does this well). ChatGPT/Codex claims in JSONL are **process evidence**.

### 9.9 Skills that point off-repo

`rprm-math-lenses` and `rprm-workbench` assume Alpha/Foam paths, NariParlor JSON bridges, and sometimes `C:\github\RPRMLexicon`. Those are real William tooling, but they are not the RPRM-open public contract. `AGENTS.md` in this repo is the small starting contract. If `math-discoveries/` is absent, that is expected here.

### 9.10 The unification theorem’s quiet scope

U01 is the only result that looks like “unifies mathematics.” Its scope is finitary many-sorted first-order *supplied* structures, semantic preservation, not a proof theory, not higher-order, not a solver. Readers who skip the “What this establishes / does not” subsections in `docs/unification.md` will overclaim. The project already wrote the correction; it is easy to skip.

### 9.11 Experimental packs that look like science

Nine packs + three research-packs + Process Mechanics kits + YM/fluid/BSD folders. Only the first class is executable-and-indexed; the second is unexecuted-on-purpose; the third is companion-to-Paper-2; the fourth is research debris. A newcomer opening `experimental/protein-folding` or `research-packs/brca1-function` can think a biomedical result exists. Every README screams otherwise; the directory graph still misleads.

### 9.12 Author-education afterword vs the written proofs

The afterword states limited formal training and heavy AI assistance. The spine proofs are elementary-to-standard mathematics with attributions. The correct judgment is neither “therefore crankery” nor “therefore a new foundation.” It is: check each claim’s domain and grade, as the project asks.

---

## 10. Source index (key files, one line each)

### 10.1 Start here

| File | Why it matters |
|---|---|
| `AGENTS.md` | Six-point task record; NONE/ONE/MANY/OPEN; evidence-grade rule |
| `README.md` | Public map, licenses, nine packs, three proposals, verification commands |
| `MANIFESTO.md` | Canonical book source, 73 written statements, afterword |
| `RPRM-Manifesto.pdf` | 140-page reading edition; layout-reviewed |
| `DOCUMENT_BUILD.json` | Source/PDF hashes and toolchain pins |
| `CITATION.cff` | v1.0.3 and Manifesto DOI |
| `AGENT_HANDBOOK.md` | v6 self-contained reasoning contract; assessment F’s text |
| `LAYPERSON_GUIDE.md` | Same core without operator taxonomy |
| `CONTENTS.md` | Honest inventory of what is implemented vs named |
| `CONTRIBUTING.md` | Fork-first; no maintenance promise; hostile-case rule |

### 10.2 Core mathematics

| File | Why it matters |
|---|---|
| `docs/core.md` | Definitions: fibers, apertures, CAR/FOLD, lift-land, half/pressure, affine chart |
| `docs/operations.md` | O01–O14 written proofs and counterexamples |
| `docs/unification.md` | U01–U05 and the hostile-bridge table |
| `docs/glossary.md` | Working vocabulary including Tile/Board/Atlas, FIVE vs ten-cycle, clamp |
| `docs/proof-donut.md` | Certificate method + executable APIs |
| `docs/formal-proofs.md` | Exact 20 Lean declarations |
| `docs/verification.md` | **Current** runner jobs, counts, hostile controls, trust boundary |
| `docs/relational-layer.md` | Physical proposal and observation-limit theorem’s use |
| `docs/concepts.md` | Number descriptions, 3+1, teachers, paired strands |
| `docs/origins.md` | Initial states; physical origin aperture OPEN |
| `docs/references.md` | Codd, Plotkin, Moore, Fritz, Lean axioms |
| `docs/fermat-study.md` | Bounded-side theorem + fixed-gap; unrestricted OPEN |
| `docs/fermat.md` | Runnable fixed-gap pointer |

### 10.3 Code and checks

| File | Why it matters |
|---|---|
| `rprm/core.py` | Finite reference semantics |
| `rprm/futures.py` | Distinguishing words and stable refinement |
| `rprm/proof_donut.py` | Independent certificates |
| `rprm/fixed_gap.py` | Per-aperture Fermat-gap decision |
| `rprm/process_mechanics/` | Paper 2 typed adapters |
| `lean/Relations.lean` | 11 relation identities |
| `lean/Carrier.lean` | 9 observation/continuation identities |
| `verify.py` | Fresh aggregate runner |
| `checks/core.py` | Large finite core census + hostiles |
| `checks/unification.py` | FO translation vs independent evaluator |
| `checks/futures.py` | Machine census vs pair-graph vs refinement |
| `examples/quickstart.py` | Aperture demo |
| `atlas/index.html` + `atlas/kernel.js` | 20 laws; charts/handoffs/half-turn live here |

### 10.4 Papers

| File | Why it matters |
|---|---|
| `papers/process-mechanics/README.md` | Paper 2 identity and DOI |
| `papers/process-mechanics/MANUSCRIPT.md` | Canonical PM argument |
| `papers/process-mechanics/CLAIM_ID_MANIFEST.json` | Ten scoped claims |
| `papers/process-mechanics/CORRECTIONS.md` | Explanatory corrections without changing numerical evidence |
| `papers/absolute-distinction/PAPER_PLAN.md` | Paper 3 baselines, source map, deferred list |
| `papers/absolute-distinction/CONCEPT_REGISTER.md` | Best compact map of recovered vs draft vs user meaning |
| `papers/absolute-distinction/REVIEW_NEXT_STEPS.md` | Draft 0.1 review outcome and next author pass |
| `experimental/process-mechanics/README.md` | Public companion kits |

### 10.5 Recovered concepts and RCF

| File | Why it matters |
|---|---|
| `recovered-concepts/README.md` | KB entrance |
| `recovered-concepts/NEXT-PAPER-BACKLOG.md` | Live non-BSD paper candidates |
| `recovered-concepts/PAPER-COVERAGE-AUDIT.md` | Frozen 11 Sep what-is-in-the-papers |
| `recovered-concepts/PRESTIGE-AND-NUMBER-OPERATIONS.md` | Verbatim prestige/fiving/3-9 passages |
| `recovered-concepts/ZERO-AND-RAILS.md` | Seam Zero and shifted halves |
| `recovered-concepts/CUBES-AND-PI-CURVES.md` | Cube/Newton/pi-curve recovery |
| `recovered-concepts/SPINE-CARRY-AND-CHECKING-RECORDS.md` | Checking records; points at BSD45 without being a BSD paper |
| `RPRM-CORE-FORMALIZATION-01/CONCEPT_REGISTER.md` | Prestige/fiving/cube IDs that must not vanish |
| `RPRM-CORE-FORMALIZATION-01/FORMAL_BRIDGE_NOTE.md` | First cube–fiving–reuse synthesis |
| `research/core-recovery-r2/README.md` | Current guarded implementation successor |

### 10.6 Experimental packs and research-packs

| File | Why it matters |
|---|---|
| `experimental/README.md` | Nine-pack index and non-claims |
| `experimental/primes/` | Square-frontier + Lucas–Lehmer cap; no record primes |
| `experimental/two-path-lab/` | Rational QM fixtures |
| `experimental/lens-lab/` | Locked five-point relationship |
| `experimental/music-lens/` | Phrase transport |
| `experimental/shadow-lens/` | Inverse shadows; missing from the nine-pack table |
| `experimental/rule-lab/` | CA + finite primes |
| `research-packs/README.md` | Three unexecuted scientific comparisons |

### 10.7 Non-BSD research that is more than debris

| File | Why it matters |
|---|---|
| `research/liar-teacher-formalization-2026-09-12/THEORY.md` | P1–P11 written proofs |
| `research/liar-teacher-formalization-2026-09-12/SAT-PILOT.md` | Frozen-before-run affine CNF pilot |
| `research/expansion-compression-2026-09-12/README.md` | Growth/compression contract |
| `research/ym2_covering_argument/README.md` | Lattice covering gap bound |
| `research/ym2_connected_vacuum/README.md` | Joint vacuum witness |
| `research/nks-rprm-deep-dive-21/REPORT.md` | NKS → finite RPRM examples |
| `research/fluid-f2-review-20260912/REVIEW.md` | Layer B refutation preserved |
| `research/rprm-consolidation-c2-20260912/PAPER_ROUTING_NOTE.md` | F1/AD1/YM1 must not be blended |
| `research/rprm-consolidation-c2-20260912/ad/AD1_RESULT.md` | Conventional-tie methods specimen |
| `research/cross-closure-01/input/START_PARALLEL_THREAD.md` | SAT-compression parallel thread (untracked) |

### 10.8 Assessments and figures

| File | Why it matters |
|---|---|
| `agent-tests/README.md` | A–F scores and how *not* to over-read them |
| `figures/README.md` | Six book figures; two two-path plots |

### 10.9 Off-repo donors the first-party texts themselves name

These are not RPRM-open files; the project’s own recovery notes depend on them:

| Locator | Role |
|---|---|
| `C:\github\RPRM-foam-development` | Foam implementation; Audit99/105/116; CLAIM_LEDGER |
| OneDrive Quantum Research `…/ChatGPT/Quantum Research` | Graded Scar Cube, centered-half scout, historical experiments |
| `C:\github\LawCube`, `C:\github\RelationForge` | F2/F3 formula compiler; finite relation rotation |
| `C:\github\RPRMLexicon\operational_numbers\` | Number translator / nines-flip (skill; not this repo) |
| Private GitHub `RPRM-Alpha`, `rprm-fluid-adjacency`, `rprm-protein-folding`, `rprm-cancer-research`, `rprm-water` | Sibling research heads |

---

## 11. Working-tree caveat for this catch-up (16 Sep 2026)

Observed via `git status` while reading, not interpreted as a release:

- `main` is **ahead of `origin/main` by 2** autosync commits.  
- Dirty/untracked mass under `research/bsd-full-source-projection-bridge-92/` (live BSD, out of scope here).  
- Untracked `papers/absolute-distinction/` (Paper 3 draft 0.1).  
- Untracked `research/cross-closure-01/` (SAT-compression handoff).  
- Local tags: v1.0.0–v1.0.2; GitHub also has v1.0.3.

Canonical published bytes remain the Manifesto v1.0.3 binding and Process Mechanics 0.3 binding recorded in their `DOCUMENT_BUILD.json` files. Paper 3 and BSD92 are **not** those editions.

---

## 12. One-page spine for later reuse

RPRM, as this repository understands itself, is a **relational presentation and preservation discipline** for supplied mathematics, named after a still-open physical hypothesis. The operational unit of work is an aperture on a typed relation: freeze carrier and equality, name supplied and missing ports jointly, name the receiver, compute or describe the complete fiber, and refuse to upgrade OPEN to NONE or a finite test to an unbounded theorem. A representation answers a question iff the question is constant on fibers; an operational representation also preserves enabledness and successors. The public book proves that discipline for factorization, finite futures, a finitary first-order encoding, and a list of applied models, then stops. Recovered William-concepts (prestige, fiving, cubes, shifted halves, 7/8 teachers) are real research objects with mixed evidence grades; some already have written proofs and tests that the papers have not absorbed. BSD is a large side mill; it is not the definition of RPRM. The project’s own standard of judgment is the hostile case and the withdrawn Fermat overclaim.

---

*End of first-party corpus report. No next research target is selected. Non-BSD candidates are listed in §8.*
