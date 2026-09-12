# Recalled-concept coverage audit of the public RPRM repository

Audit date: 2026-09-11 (machine date). Repository: `C:\github\RPRM-open`. Audited HEAD: `4f5c8145a1d9389f28079ef63a385e406122fd34`; initial tracked working tree was clean. This paper-audit phase created this report; a later delegated historical recovery produced separate neighboring artifacts. No existing source, paper, or publication was changed.

## Scope and method

Read `AGENTS.md`, `README.md`, and `AGENT_HANDBOOK.md`. First inspected both papers' section maps and focused passages, then searched the wider public repository. Canonical paper text is `MANIFESTO.md` and the combination of `papers/process-mechanics/MANUSCRIPT.md`, `APPENDICES.md`, and `BIBLIOGRAPHY.md`.

The first pass used all four canonical texts, with headings and focused context for centered coordinates, abduction, formula transport, vacancy, continuation, curves, and evidence. The second pass searched public text, including `docs`, `rprm`, `examples`, `checks`, `atlas`, and `experimental`, followed by `git grep -I` across tracked files for distinctive recalled names. A scoped inventory counted 213 discoverable text/code files in `.md`, `.py`, `.js`, `.json`, `.lean`, `.html`, `.csv`, and `.tex` (excluding dependency lock files and vendor/dependency trees). Negative findings mean **not located in current public tracked text under the stated searches**, not a claim about private history or every possible paraphrase.

Classification used below:

- **Direct:** the recalled mathematical construction is actually described, regardless of typographic numeral style.
- **Related substrate:** a precise operation or example survives, but no evidence establishes that it is the recalled concept.
- **Absent name / unlocated construction:** distinctive terminology or the full proposed construction was not found.
- **Generic overlap:** a word or general principle occurs but is insufficient to identify the recalled idea.

No new mathematical theorem was derived. Numerical examples not present in the sources were not silently filled in. In particular, a general affine chart capable of expressing a shifted pair is not evidence that the shifted-pair research made it into the paper.

## Canonical source/PDF verification

All six relevant SHA-256 checks matched the recorded manifests. Consequently no PDF rendering was needed to resolve a source/build mismatch. This verifies byte bindings to the recorded builds, not mathematical correctness or a new visual-layout review.

| File | SHA-256 verified against manifest | Result |
|---|---|---|
| `MANIFESTO.md` | `1970db936f6b448c869e563559955e3199fdf688fceb9962fe2d47466510922e` | MATCH |
| `RPRM-Manifesto.pdf` | `a9d0c83456281ffa59fbf0c90394d18399bdca98dbc90d337df3ec8f1226e958` | MATCH |
| `papers/process-mechanics/MANUSCRIPT.md` | `c4a60a79a1ed23690f61df6a0e35c705ce141e7187452de09bffb11952b9270e` | MATCH |
| `papers/process-mechanics/APPENDICES.md` | `4d3596a2a8b43061baa34a79712ad4ad29493e09d49042aef5fca09e0d9e7e94` | MATCH |
| `papers/process-mechanics/BIBLIOGRAPHY.md` | `8c225dceacbd28aab6507d735a5e6a5c87f2e08474daf132b7420a9f8c938897` | MATCH |
| `papers/process-mechanics/The-Right-Answer-Is-Not-Enough.pdf` | `97de1e6e688fab05a83aef981fb39a97e0f381447ff90b5b2e08d240135eac62` | MATCH |

Manifest locators: `DOCUMENT_BUILD.json:4` (source), `:5` (PDF), `:8` (source hash), `:9` (PDF hash); `papers/process-mechanics/DOCUMENT_BUILD.json:27`–`:29` (three source hashes), `:35`–`:36` (PDF and hash). Recorded sizes are 140 pages and 41 pages, respectively. The Process Mechanics bibliography identifies the first paper separately at `papers/process-mechanics/BIBLIOGRAPHY.md:4`; this audit does not mix their DOIs.

## Coverage matrix

### 1. Prestige, reincarnated, or ascended ones; possibly three types

**Both papers:** No distinctive names or three-type account of these “ones” located. Ordinary source identity, repeated occurrences, encodings, and carry are not enough to identify them.

**Wider public repo:** No `prestig*`, `reincarn*`, or ascended-one naming located. Two explicitly different promotion contracts do survive:

- `docs/operations.md:300`–`:314`: `PROMOTE.capability` maps a closed compound to a higher-level carrier under interface preservation equations; `PROMOTE.state` accepts a candidate into a state store through FLICK.
- `docs/glossary.md:1429`–`:1455`: these two meanings are distinguished. Neither defines a third type or names prestige/reincarnation/ascension.
- `MANIFESTO.md:276` begins value/role/occurrence distinctions; `MANIFESTO.md:1104` and `:1150` distinguish numeral width, carry, and lifted state. These are possible neighboring ideas, not recovered identities.

**Disposition:** absent names; full recalled three-type taxonomy OPEN for recovery from an earlier source. Do not rename PROMOTE's two contracts as the remembered three types.

### 2. Centered −0.5/+0.5; shifted −0.6/+0.4; residual −0.2; math rail vs physics rail

**Manifesto — direct centered half construction:**

- `MANIFESTO.md:1199`–`:1215`: `c(x)=x−1/2` maps the binary axis `{0,1}` bijectively to `{−1/2,+1/2}`; `c(1−x)=−c(x)` transports complement to negation. Two coordinate occurrences remain a pair until a sum is requested.
- `MANIFESTO.md:1217`–`:1232`: a separately supplied unit-total carrier `(S,R)` has difference `δ=S−R`; zero difference forces `(1/2,1/2)`, and `δ=2c(S)`. For k equal unit-total lanes, each is `1/k`.
- `MANIFESTO.md:333` introduces the general affine chart, but that is not a recorded −0.6/+0.4 example.

**Process Mechanics:** It discusses added coordinates and preserving scientific measurement context (`MANUSCRIPT.md:120`–`:122`, `:443`, `:469`), not this centered/shifted lane calculation. Decimal probabilities 0.6 or 0.5 in its statistical examples are unrelated occurrences.

**Wider public repo:** `docs/core.md:594`–`:628` and `docs/glossary.md:831`–`:837` retain residual, half, balance, separate coordinate occurrences, and alternative views. `docs/origins.md:54`–`:78` discusses zero/balance and physical interpretation. No exact shifted −0.6/+0.4, residual −0.2 sequence or named math/physics-rail contract was located.

**Disposition:** ±0.5 is directly covered. The shift/residual/dual-rail relationship is unlocated, not silently supplied by the affine definitions. The general separation of mathematics from physical interpretation is present (`MANIFESTO.md:238`–`:256`) but is only a generic overlap with the remembered rails.

### 3. Formula translation cube: center vacancy, abduction, dimensional lift, self-check

**Manifesto — several concrete pieces survive, but not as a named cube:**

- `MANIFESTO.md:169`–`:210` and `:908`–`:1013`: four-lane abduction, joint source fiber, and inference at an unvisited center. The supplied grammar is the multiaffine square `f(x,y)=a+bx+cy+dxy`, not a general 3D formula cube. Four corners determine the function; the whole boundary fails to determine the center after enlarging the grammar.
- `MANIFESTO.md:216`–`:236`, with the expanded argument beginning `:546`: truth-preserving translation of supplied many-sorted first-order structures. It encodes sorts, graphs of functions, predicates, and image-guarded quantifiers. This is formula translation, but no cube interface or universal formula-discovery engine is claimed.
- `MANIFESTO.md:1234`–`:1248`: vacancy is an explicit occupancy state, distinct from zero payload or an unassigned port. Its concrete carrier is **four labeled sites in a line**, not a center-vacancy cube.
- `MANIFESTO.md:467`: a lift/retraction pair recovers the source on its image. This supplies a part of the general transport substrate, not a dimensional-cube implementation.
- `MANIFESTO.md:1092`–`:1100` and `:3919`–`:3925`: certificates expose checking conditions; finite self-application can expose inconsistencies, with the checker's general soundness kept as a separate obligation.

**Process Mechanics:** The task diagram and three operational conditions (`MANUSCRIPT.md:43`–`:67`, `:124`–`:154`), joint-source compatibility (`:173`–`:237`), and soundness/trust boundaries (`:360`–`:380`) are related formal scaffolding. The paper does not describe a formula cube, center vacancy, or dimensional traversal. `APPENDICES.md:5`–`:81` proves target-resolution/composition claims, not a cube reconstruction theorem.

**Wider public repo — more explicit construction vocabulary:**

- `docs/core.md:530`–`:592` and `docs/operations.md:282`–`:298`: dimensional promotion and `LIFT–SPIN–LAND`. The richer operation's landing must be proved; a retraction alone does not prove the desired operation.
- `docs/glossary.md:114`–`:154`: optional eight-Boards-plus-withheld-capability Atlas and eight-Tiles-plus-withheld-capability Board arrangements. `docs/glossary.md:1867`–`:1875`: a Tile has its own hypothesis carrier, withheld role, experiments, and interface.
- `docs/operations.md:310`: even a completed Tile with four corners, law, and proof does not automatically inhabit an ordinary component-value port.
- `docs/glossary.md:278`–`:288`: a 3x3 layout or square boundary does not by itself specify an interior law.
- `docs/proof-donut.md:44`–`:46` uses “cube completion” only for factoring an arithmetic cube `a=w^3`; this is not the recalled translation cube.

**Disposition:** abduction and unvisited center are direct; formula transport, vacancy, lift, hierarchy, and checking are individually substantive. Their integration into the remembered cube, its exact dimensional rules, and any executable traversal/self-check loop remain unlocated. Do not present this collection of pieces as proof that the complete cube made it into either paper.

### 4. “True pi” / curve

**Both papers:** No “true pi” or alternate π construction located. The Manifesto has conventional trigonometric/mechanism curves, winding, normalization, and branch-aware inverse examples (`MANIFESTO.md:1506`–`:1740`). Process Mechanics' fitted biological curves and units problem (`MANUSCRIPT.md:382`–`:405`) are a different topic.

**Wider public repo:**

- `atlas/README.md:70`–`:91`: IEEE-754/standard-library trigonometry, finite-difference slopes, schematic drawings, and an explicit statement that separate polygon, curve, and topology constructions are not runtime dependencies.
- `experimental/lens-lab/README.md:95`–`:108`: ordinary phase-wave sine and circle renderers; the curve is explicitly a new phase-wave renderer, not a moving-frame curve-reconstruction result (`:103`).

**Disposition:** curve examples are present, but the distinctive “true pi” idea is unlocated. Conventional π use does not recover it. The Lens Lab wording is a useful historical search lead for a possibly separate moving-frame curve project, not evidence for what that project proves.

### 5. “5ing”

**Both papers:** No `5ing` name. The Manifesto contains shortest distinguishing-future search (`MANIFESTO.md:862`–`:870`) but does not name it FIVE. It also contains generic lifted carry (`:1150`–`:1197`).

**Wider public repo:**

- `docs/glossary.md:711`–`:725`, `docs/core.md:441`–`:453`, and `docs/operations.md:198`–`:210`: `FIVE` / `FIVE.future` means a distinguishing-future search, returning merged source states plus a continuation that separates their admitted observations.
- `docs/glossary.md:1845`–`:1853`: a **separate** oriented ten-cycle half-turn writes `d=5h+r` and adds five modulo ten, preserving r while toggling h. The source explicitly distinguishes this from distinguishing-future search.
- `atlas/kernel.js:347`, `:448`–`:452`: a cyclic half-turn component applies `D(d)=d+n mod 2n` on a retained finite carrier.

**Disposition:** a strong naming lead plus an exact arithmetic operation survive, but their relation to the user's “5ing” must be recovered, not assumed. In particular, FIVE.future, +5 mod10, and generic inverse search are three different things in the current public text.

### 6. “Doing 3 with 2/4”

**Both papers:** No named operation located. The Manifesto's three-plus-one parity example (`MANIFESTO.md:153`–`:159`, `:1250`–`:1293`) and overlapping arithmetic triples (`:1015`–`:1037`) have explicit different laws; neither alone identifies this phrase.

**Wider public repo — specific local-chart fragment:**

- `atlas/kernel.js:354`–`:356`: a retained path address x in 1..9; charts centered at 2,4,6,8 with `h_c(x)=x−c` on the triple `[c−1,c,c+1]`; handoff ports at x=3,5,7 read +1 on the left and −1 on the right.
- `atlas/kernel.js:466`–`:473`: the implementation of chart admission and paired handoff receipts.

**Disposition:** this directly supplies x=3 represented relative to chart centers 2 and 4, making it a precise reconstruction lead. It is not labeled “doing 3,” and the historical identity remains unconfirmed.

### 7. Inverse 5/6/7/8

**Both papers and wider repo:** No four named number-specific inverse operations located. General converse/inverse/fiber machinery is extensive (`MANIFESTO.md:292`–`:415`; `docs/core.md:315`–`:353`; `docs/glossary.md:981`–`:989`). The local chart centers 6/8 and half-turn above are not evidence of a 5/6/7/8 inverse taxonomy.

**Disposition:** absent names; unlocated operation family. Need the earlier rule table or source examples to decide whether these were different operations, ports, phases, or states.

### 8. “Every 3 is a 9”

**Both papers:** No matching assertion or defined 3→9 law located. Parity's three supplied roles and a fourth, or arithmetic cubes modulo nine in the separate Fermat material, are not equivalent claims.

**Wider public repo:** optional 3x3/eight-plus-center construction vocabulary survives at `docs/glossary.md:118`, `:148`, `:282`, but no general “every three is nine” result is stated. The path 1..9 with overlapping triples is a separate finite coordinate construction (`atlas/kernel.js:354`–`:356`).

**Disposition:** hierarchy/arrangement substrate only. The recalled quantified statement and its intended domain are unlocated.

### 9. “Waiting on 1,3,5,7”

**Both papers:** No named waiting rule located.

**Wider public repo:** the chart handoffs at **3,5,7**, within path **1..9**, survive (`atlas/kernel.js:354`–`:356`, `:466`–`:473`). No corresponding handoff at 1 is registered there, and no waiting mechanism is described by those components. Thread barriers and UI waits are irrelevant literal matches.

**Disposition:** concrete odd-handoff fragment, with an important mismatch: it does not supply the recalled four-item sequence or its “waiting” operation.

## Other visible coverage differences

These are differences between the public papers and public companion, not new claims about everything omitted from private research:

1. **Tile → Board → Atlas capability hierarchy** is more explicit in the public glossary than either paper. The Manifesto's “Mechanical Motion Atlas” is an application name, not a demonstration of that hierarchy. The capability family's optional arity and withheld role survive as definitions, not a complete executed dimension ladder (`docs/glossary.md:114`, `:146`, `:1867`; `docs/operations.md:300`).
2. **FIVE, TRACEBACK, PROMOTE, SEAL, INHERIT, FLICK** remain named operation contracts in `docs/operations.md:198`, `:300`, `:316`. Some of their mathematics appears in the papers under ordinary descriptions; the names and family taxonomy are not all carried into the connected paper argument. This matters when searching only the PDFs.
3. **Local coordinate handoffs and cyclic half-turns** survive in the Atlas code, while the Manifesto chapter proves three selected ideal mechanism laws and refers to the larger Atlas only collectively (`MANIFESTO.md:1738`, `:3841`). A paper-only search can miss exact implemented numeric fragments.
4. **C-shaped return/depth** is actually retained, not an omission: `MANIFESTO.md:2588`–`:2685` develops complementary-side continuing returns, depth, projected address, return receipt, and separate clocks. It explicitly stops short of claiming the C-shaped geometric embedding has been supplied (`:2590`). This is worth including if a broader concept inventory is later assembled.
5. **Constructor/width/carry and three-plus-one** are also retained directly: `MANIFESTO.md:1104`–`:1197`, `:1250`–`:1293`. Their stated carriers distinguish operation count, numeral width, and geometric dimension. Whether that is a faithful narrowing of an older richer concept requires the older source; this audit cannot settle that from the public text alone.

## Strongest supported answer and remaining work

The papers demonstrably retain centered halves, joint abduction, an unvisited center under a supplied interpolation law, faithful formula transport, occurrence distinctions, zero/vacancy distinctions, and explicit checking conditions. The public companion retains additional exact fragments: FIVE.future, the ten-cycle half-turn, Tile/Board/Atlas capability families, lift–spin–land, and charts at 2/4/6/8 with 3/5/7 handoffs.

The distinctive remembered terminology and several full constructions are not located in the public text: prestige/reincarnated/ascended ones, the shifted-pair/residual/dual-rail account, the integrated formula translation cube, true pi, the numbered inverse family, every-3-is-9, and the waiting-on-1/3/5/7 rule. The next useful step is historical-source recovery with these fragments as search leads. Related mathematics should not be treated as a recovered identity without that source link.
