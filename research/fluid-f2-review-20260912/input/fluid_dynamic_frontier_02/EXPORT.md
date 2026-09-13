# Export / replay checklist

1. Work only in `experiments/fluid_dynamic_frontier_02/` plus this ZIP. Frozen F1 sources stay read-only in `CURSOR_FLUID_F2/`.
2. Scored run: `python -I -B src/run_f2.py --output-dir results` (refuses to overwrite `rows.jsonl`).
3. ZIP the experiment directory **excluding** `__pycache__` and `replay_evidence/`. Results from the scored run are part of the payload.
4. SHA-256 the ZIP. Record file hashes in `HASHES.txt`.
5. Replay **from the unzipped ZIP**, not from the original working tree, into a directory **outside** the hashed payload.
6. Compare `rows.jsonl` SHA-256 and `summary.json` numeric fields. Run `check_f1_regression.py`.
7. Save the replay receipt outside the ZIP (`replay_evidence/` in the working tree and `/opt/cursor/artifacts`).
