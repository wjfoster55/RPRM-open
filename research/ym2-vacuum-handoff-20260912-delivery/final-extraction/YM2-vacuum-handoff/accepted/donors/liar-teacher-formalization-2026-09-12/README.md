# Seven/eight, teachers and the P versus NP continuation

12 September 2026. **The historical construction is recovered, several exact models are now proved, and a new parity-message SAT experiment passes.** The stable knowledge-base entrance is [recovered-concepts/README.md](../../recovered-concepts/README.md); its [running paper backlog](../../recovered-concepts/NEXT-PAPER-BACKLOG.md) records this addition for later editorial selection.

## The construction in plain language

Start with three calibrated binary observations `a,b,c` of a three-bit state. They generate seven usable questions:

```text
a, b, c, a XOR b, a XOR c, b XOR c, a XOR b XOR c.
```

Keep `a,b` and replace `c` with `a XOR c`: the old `c` is recovered by XORing the new answer with `a`. This is a justified teacher handoff. Replace `c` with `a XOR b` instead, and the third answer adds nothing: two source states remain possible. Exactly **28 of the 35 three-question panels** recover all eight states; seven do not. All distinct panels of four or more questions separate them. At the smaller four-state level, any two of its three nonzero binary checks suffice.

The source-role version is different but equally exact. Two independent commuting toggles give `I,A,B,AB`. A new independent toggle `C` brings in `C,AC,BC,ABC`, creating eight distinct roles. The quartet `I,A,C,AC` retains two old roles and replaces a related pair. A reference change can make `C` the relative identity, provided the decoding/frame information moves with it. Restricting to a quartet need not preserve every question about the whole eight-role source.

The student is the receiving role for a requested completion. Before completion it may be a vacancy; after a unique completion it can hold the result. Retaining that value for later use is justified only if it preserves the next observation, operation and enabledness. An anchor, a student and an extra silent ninth position need distinct contracts. The historical proposal can be richer than either binary model.

## The Hamming connection is an equation

Let H have the seven nonzero three-bit labels as columns. The full seven-teacher answer vector is `Hᵀx`. Its eight possible words form the **[7,3,4] simplex code**, which is the orthogonal dual of the **[7,4,3] Hamming code** `ker H`. The seven failing teacher triples are exactly the label triples supporting Hamming's weight-three codewords. [THEORY.md, P4–P9a](THEORY.md) proves these statements.

| Count | What is being counted | What the extra coordinate does |
|---|---|---|
| Four → eight source roles | Combinations of independent reversible toggles | Adds one free binary distinction |
| Seven teacher answers / eight possible words | All nonzero linear checks of a three-bit state | Adds redundant checks beyond a basis |
| Hamming seven → extended eight positions | Error-protected codewords, sixteen in either code | Adds a determined parity bit; detects double errors but does not uniquely locate their pair |

This uses established coding theory; the contribution here is the explicit connection to the recovered teacher and handoff model. The original context is [Hamming (1950)](https://onlinelibrary.wiley.com/doi/abs/10.1002/j.1538-7305.1950.tb00463.x).

## What the new SAT test establishes

The imported ChatGPT discussion found that point/partial-assignment messages could not summarize parity economically. The new pilot builds linear-size raw-CNF parity chains, recognizes their equations from the clauses, eliminates private variables and joins exact boundary messages.

**All 24 finite cases passed**, including renamed/complemented versions. An independent raw-clause oracle enumerated **87,360 complete local assignments** and checked the complete projected relations and joins. Each local message is **one parity equation instead of 2^(b−1) boundary points**. The test also passed 276 recognizer truth tables, 38 small projection systems and two non-affine hostile joins. Eight larger algebra-only runs are recorded separately without an exhaustive oracle.

The same parity recognizer was supplied to conventional whole-system Gaussian elimination. It also avoids point enumeration. Some panel operation counts were lower for the chosen ordering; the report shows equal and worse cases too. The result establishes an exact compact message for this affine family, with no new decision capability beyond Gaussian elimination. Affine SAT and SAT/parity combinations are established topics: [Schaefer (1978)](https://www.khoury.northeastern.edu/home/lieber/courses/csg260/f06/materials/papers/max-sat/p216-schaefer.pdf), [Laitinen, Junttila and Niemelä (2012)](https://arxiv.org/abs/1207.0988).

The next mathematical step is explicit in **THEORY P11**: a clause can be retained exactly as a small union of affine pieces, and projection/join remain exact. Repeated joins can multiply the number of pieces. Replacing that union with its affine hull can produce a false SAT answer; OR3 and exactly-one controls demonstrate the loss. A uniformly affordable representation for arbitrary CNF, including construction and intermediate costs, remains open. This gives a concrete next target for the P versus NP investigation.

## Read, reproduce and reopen

| File | Purpose |
|---|---|
| [THEORY.md](THEORY.md) | Explicit carriers, written proofs, handoffs, moving reference, Hamming duality, affine projection and exact non-affine extension |
| [CONTINUATION.md](CONTINUATION.md) | Imported discussion, decision-only SAT target, reported prior results and next open obligation |
| [REVIEW-MISSING-CONCEPTS-SOURCE.json](REVIEW-MISSING-CONCEPTS-SOURCE.json) | Latest eight source turns with IDs and a disclosed older-history boundary |
| [SAT-PILOT.md](SAT-PILOT.md) · [SAT-RESULTS.json](SAT-RESULTS.json) | Frozen experiment, actual results, counterexamples, fair baseline and costs |
| [PANEL-RESULTS.json](PANEL-RESULTS.json) | **13,665 passing assertions** on the declared finite carriers; counts do not mean independent proofs |
| [RELATED-RESEARCH.md](RELATED-RESEARCH.md) | Read-only BSD/Yang–Mills inspection and transferable reference/joint-witness/future-readout lessons |
| [Historical recovery](../liar-teacher-recovery-2026-09-12/RECOVERY.md) · [Original user turns](../liar-teacher-recovery-2026-09-12/SELECTED-PASSAGES.md) | Original August–September sources, richer operational intent and the previous experiment |
| [VERIFICATION.json](VERIFICATION.json) | Final source hashes, execution and local-link checks |

From `C:\github\RPRM-open`, with ordinary Python 3.10+ and its standard library:

```powershell
python -I -B research/liar-teacher-formalization-2026-09-12/verify_panels.py
python -I -B research/liar-teacher-formalization-2026-09-12/sat_pilot.py
```

The panel command prints JSON; the SAT command writes its adjacent receipt. Assertions must remain enabled. Independent review checked the panel mathematics and SAT projection implementation; review-driven additions tested degenerate quartet newcomers, the extended parity-bit error and rank-zero/one/repeated-row systems. Written proofs, finite implementation tests, old reported results and open research claims remain separate evidence grades. No published paper or neighboring BSD/Yang–Mills/SAT02 implementation was changed.
