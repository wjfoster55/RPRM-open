# YM2 operational seam continuation

Start with [RESULT.md](RESULT.md). The mathematical result and exact
assumptions are in [COMBINED_RESULT.md](COMBINED_RESULT.md).

- [BSD donor audit](BSD_DONOR.md)
- [Candidate and carrier record](CANDIDATES.md)
- [Exact coefficient and support proof](CHANNEL_SOURCE.md)
- [Kinetic continuation and all-spin obstruction](SPECTRAL_CHANNEL.md)
- [Independent written review](OPERATIONAL_REVIEW.md)
- [Exact-control receipt](RESULTS.json)
- [Visual](operational_seam.png), [SVG](operational_seam.svg)
- [Attribution](LITERATURE.md)

From an extracted folder, run `python -I -B -X utf8 check_operational.py`.
It uses Python's standard library, writes nothing, and emits the full
deterministic JSON receipt for comparison with RESULTS.json. It recomputes
the new matrix identities with sparse arbitrary-precision integers. The
separate channel_probe.py is the original dense independent check and uses
NumPy; it is retained as evidence, but is unnecessary for portable replay.
Drawing the figure requires Matplotlib. No dependency installation is part
of this deliverable. Final-export evidence is adjacent to the delivered ZIP.

The retained archive and selected source snapshots supply the accepted
dependencies. Historical links within those unchanged snapshots retain
their original targets; only new top-level document links are promised
to resolve inside this packet. New artifact provenance records original
locators, hashes and snapshot status. All prior files remain unchanged.
