# YM2 rail closure — bounded research continuation

Start with [the result and intuitive explanation](RESULT.md), then
[the conditional-law/vacuum derivation](CONDITIONAL_RAIL.md) and
[chain estimates and separating witnesses](CHAIN_ESTIMATES.md).
The source recovery is split between [vault/FLICK](VAULT_RECOVERY.md)
and [pi/rail/FullZip](RAIL_RECOVERY.md). Their broader RPRM meanings
remain explicit; the YM realization has its own stated carrier.

The [figure](rail_closure.png), [SVG](rail_closure.svg), and
[drawing source](draw_rail.py) are included. The checker uses only the
Python standard library:

```text
python -I -B -X utf8 check_rail.py
```

It recomputes and compares the complete saved [receipt](RESULTS.json).
It runs no old checker and writes no output files. The earlier frozen
vacuum-handoff archive and selected accepted notes are retained under
`accepted/`; source bytes remain unchanged. Historical links inside
those snapshots may require their original roots. New top-level file
links are made portable in this packet.

[Provenance](SOURCE_PROVENANCE.json) records source paths and hashes.
[Independent review](INDEPENDENT_REVIEW.md) distinguishes written proofs
from finite controls. [Visual checks](VISUAL_CHECKS.md) record figure QA.
The SHA-256 manifest excludes only itself. Final-export evidence lives
beside the frozen ZIP because it is generated after fresh extraction
and replay; the ZIP does not purport to contain its own final hash.

The new work establishes conditional reconstruction, exact chart/error
accounting, a weighted response criterion, and exact hostile cases.
It does not establish a new actual YM coupling window, a continuum gap,
or a cryptographic security guarantee. Publication remains on hold.
