# Public evidence bundle (I2 saved-row export)

Compact, rights-checked extracts that support paper-cited headline numbers.
This directory is the public support surface; it does **not** republish private
research repositories wholesale.

## Included

| Path | Role | Evidence grade |
|---|---|---|
| `pc1/LEARNER_ORIGIN_PREDICTIONS.csv.gz` | 15,475 saved learner rows (numeric fields) | SAVED_ROW_EXPORT |
| `pc1/OBSERVER_ORIGIN_RECORDS.csv.gz` | 3,271 observer/error rows | SAVED_ROW_EXPORT |
| `pc1/WITHHELD_PLAN_PAIRS.json` | 60 compact pairs + prior/clipping rule | SOURCE_REPORTED_EXTRACT |
| `pc1/MATCHED_INFO_HEADLINE.json` | Producer headline fields for comparison | SOURCE_REPORTED_EXTRACT |
| `pc1/HARD_DECISION_SUMMARY.json` | Hard-decision counts from public gzip | SAVED_ROW_REAGGREGATION |
| `pc1/reaggregate_tables.py` | Recomputes MSE, hard errors, pair Brier from rows | SAVED_ROW_REAGGREGATION |
| `pc1/SAVED_ROW_EXPORT.json` | Export pins / field allowlist | — |
| `water/PR13_TRUST_EXTRACT.json` | Frozen W-TRUST-01 numbers | SOURCE_REPORTED_EXTRACT |
| `c1/MEASUREMENT_STATUS.json` | C-MEAS-01 PARTIAL status + Liang DOI; **no images** | SOURCE_REPORTED_EXTRACT |
| `CLAIM_SUPPORT_MAP.json` | Per-claim grades, hashes, operation types | — |

Kit teaching receipts (generated separately):

- `../water/expected/demo_receipt.json` — from `water/example.py`
- `../circuits/expected/demo_receipt.json` — from `circuits/example.py`

Those demos illustrate contracts; they are **not** the historical 220/660/2391-origin panels.

## Not included

- Private git history, chat exports, full review archives
- Tokenized URLs, author-request drafts, acquisition caches
- Publisher figure images / overlays (C1)
- Independent PR14 behavioral replay artifacts

## Grades

- **SOURCE_REPORTED_EXTRACT** — frozen producer fields (compared, not treated as independent recomputation by themselves).
- **SAVED_ROW_REAGGREGATION** — arithmetic derived here from public CSV.gz / pair rows (hard errors from `p`/`label`, MSE means from squared-error columns, pair conflicts and mixture Brier from labels/prior/clipping).
- **Illustrative demos** — separate; must not substitute for historical panels.

Copied headline MSE alone is **not** an independently recomputed MSE. The script recomputes from saved rows and fails when a reported headline contradicts those rows (e.g. altered Brier with untouched pairs).

## Boundary

Publishing saved rows supports reaggregation of stated summary statistics. It does **not** regenerate source trajectories or prove upstream predictors used their claimed inputs.

## Public-only table generation

```sh
python -I -B experimental/process-mechanics/public_evidence/pc1/reaggregate_tables.py
```

Requires only files under `public_evidence/`. With `--verify-csv PATH`, a hash mismatch against the pinned source is a hard failure.

The paper navigation is [here](../../../papers/process-mechanics/README.md); the retained claims appear in Table 6 / Appendix C.1. Reaggregation rewrites the three derived files `pc1/CLAIM_TABLE.json`, `pc1/hard_decision_counts.json`, and `pc1/HARD_DECISION_SUMMARY.json`. It leaves the saved source rows, pairs and producer extracts unchanged. An arithmetic `--output` redirects only the claim table.
