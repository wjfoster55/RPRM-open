# F2 experiment — constructive dynamic-breach bound

Pinned model-B study. F1 is closed; this directory does not rewrite F1 panels.

```
python -I -B src/run_f2.py --output-dir results
python -I -B src/check_f1_regression.py --rows results/rows.jsonl
```

Requires standard-library Python 3 and Node. No new packages.

| file | role |
|---|---|
| `MODEL_CONTRACT.md` | receiver, pinned updater facts |
| `PROTOCOL.md` | frozen panel and cost rules |
| `proof/DERIVATION.md` | Layer A/B, failed gap-adjacent, cascade/splash |
| `RETURN_TO_WILLIAM.md` | one-page return |
| `pinned/` | PR12 JS bytes used by the oracle |
| `src/bound.py` | static layers |
| `src/oracle.js` | limited exact / yes-exit / full |
| `src/scenes.py` | frozen 53-scene generator |
| `src/run_f2.py` | scored harness |
| `results/` | complete rows from the scored run |

Do not commit/push. Do not treat `failed_gap_adjacent` as official.
