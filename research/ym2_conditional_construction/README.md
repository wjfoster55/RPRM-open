# YM2 conditional construction continuation

Read [the result and remaining issues](RESULT.md), then
[the combined actual-vacuum and physical-gap theorem](COMBINED_RESULT.md).
The supporting new notes are
[gauge estimates](GAUGE_NORM_GAIN.md),
[local source and correction](LOCAL_VACUUM_ROUTE.md),
[the missing joint obstruction](CONDITIONAL_OBSTRUCTION.md), and
[the exact two-square geometry](TWO_SQUARE_GEOMETRY.md).

The [independent review](CONSTRUCTION_REVIEW.md) records its source-byte
bindings and evidence scope. The [PNG](joint_construction.png),
[SVG](joint_construction.svg), [drawing code](draw_geometry.py), and
[visual checks](VISUAL_CHECKS.md) are included.

Run only the new standard-library checker:

```text
python -I -B -X utf8 check_construction.py
```

It compares the complete computed result to [RESULTS.json](RESULTS.json),
runs no earlier checker, and writes no files. Source snapshots and the
preceding frozen rail ZIP are under `accepted/`. Historical links inside
those byte-preserved snapshots retain their original locations; new
top-level file links resolve within this packet. See
[provenance](SOURCE_PROVENANCE.json) for source paths and hashes.

The manifest excludes only itself. The final-export evidence, archive
hash, stdout and stderr are sidecars beside the frozen ZIP, produced
after fresh extraction and replay. Hashes establish byte identity, not
mathematical truth. This is bounded research with publication on hold.
