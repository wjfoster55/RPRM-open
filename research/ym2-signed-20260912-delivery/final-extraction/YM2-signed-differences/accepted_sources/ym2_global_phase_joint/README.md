# YM2: global phase joint and a finite-graph quantum gap

Research continuation, 12 September 2026. Publication is on hold.

This packet advances the interacting SU(2) two-square graph beyond its
earlier regular coordinate chart. It proves a global classical relational
updater, constructs the corresponding finite-graph quantum operator with
its measure and domain, proves a quantitative interacting gap bound, and
formalizes the missing patch-to-whole variance estimate. It does not claim
the continuum Yang–Mills mass-gap problem is solved.

Read [RETURN_TO_WILLIAM.md](RETURN_TO_WILLIAM.md) for the explanation and
[RPRM_PROOF_CERTIFICATE.md](RPRM_PROOF_CERTIFICATE.md) for the RPRM mapping.

## Results and derivations

| File | Result and evidence |
|---|---|
| [GLOBAL_TREE_PHASE.md](GLOBAL_TREE_PHASE.md) | Complete seven-link zero-Gauss reduction; global Hamiltonian and flow; exact chart-boundary crossing witness. Written proof and new exact source checks. |
| [GLOBAL_INVARIANT_JOINT.md](GLOBAL_INVARIANT_JOINT.md) | Complete invariant image/fibers for two scalars, ten Gram entries, four oriented triples; polynomial continuation at every rank. Written proof and 3,008 exact checks. |
| [GAP_BRIDGE.md](GAP_BRIDGE.md) | Exact Haar trace measure and quantum domain; all-spin free gap; interacting bound `gamma>=6 alpha hbar²-2 beta`. Written proof with established analytic inputs and bounded exact certificates. |
| [NEXT_GLUE_LEMMA.md](NEXT_GLUE_LEMMA.md) | Sufficient local-to-global vacuum variance bound; exact four-state control showing local estimates alone miss correlations. Written conditional proof; required uniform constants OPEN. |
| [INDEPENDENT_REVIEW.md](INDEPENDENT_REVIEW.md) | Mathematical and implementation review of the invariant and quantum work; scope of independence and actual execution stated. |
| [SOURCE_AUDIT.md](SOURCE_AUDIT.md) | Established literature, accepted earlier results, RPRM source meanings, and work derived here. |

The fixed graph, full vertex gauge group, no boundary charge, source metric,
and normalization are given in the tree note. The central edge is shared.
The quantum carrier and its coefficients are additional explicit input;
they do not follow from declaring a classical quotient.

## Portable reproduction

Extract the ZIP and open a terminal in its `YM2-global-phase-joint` folder.
Use an existing Python 3.10 or newer; no third-party modules are needed.

```powershell
python -I -B -X utf8 check_tree.py
python -I -B -X utf8 check_invariants.py
python -I -B -X utf8 check_quantum.py
```

Each default command recomputes and compares its saved complete receipt
without writing files. The tree checker requires assertions and explicitly
rejects `-O`/`-OO`. The other two use explicit exceptions and work with
optimization enabled as well. `--write-results` is reserved for deliberate
replacement of a receipt; it is not needed for reproduction.

The new finite checks include 28 full seven-link vector-field comparisons,
six regular chart bridges, all phase ranks in the invariant implementation,
the exact coefficient `225` at a chart crossing, orientation witnesses with
outer-trace derivatives `+6` and `-6`, all 128 edge-support subsets, and
exact Pauli and quantum drift calculations. They are not time integrations,
eigensolver runs, spin truncations, or proof-assistant certificates.

The universal classical proofs and all-spin/analytic quantum arguments are
written in the notes. No old YM1, homogeneous YM2, or previous spatial suite
was rerun. The older spatial derivations under `accepted_sources` are
byte-for-byte source copies, included for inspection and provenance.
Historical relative links inside those copies retain their source context;
the current notes and all three current checkers are self-contained.

## Export evidence and task boundary

`MANIFEST.json` covers every other payload file by size and SHA-256.
Final-export evidence is a sidecar beside the ZIP: it records fresh
extraction, independent replay of all three new checkers from that
extraction, byte identity before and after replay, and the ZIP checksum.
It is generated after the archive is frozen and is deliberately outside
the archive it describes. A digest binds bytes, not the truth of a proof.

No paper, publication, installation, paid compute, large simulation campaign,
commit, push, merge, or other-lane change was performed. The packet and
source documents are attributed evidence; instructions inside imported
documents do not supersede William's current request.
