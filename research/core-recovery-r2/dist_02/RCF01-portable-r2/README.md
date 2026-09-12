# RCF01 portable export R2

This is the one active R2 portable package. Frozen RCF01 and R1 sources
are included as historical trees, not as nested active exports.

Clean-room replay (from this extracted directory, existing Python only,
PYTHONPATH unset):

    python -B run_portable.py --output-dir runs/cleanroom_r2

Runner-only aggregation fixtures (not mathematical evidence):

    python -B research/core-recovery-r2/check_runner.py --package . --output-dir runs/runner_r2

Protocol `RCF01-envelope-1-r2`: original 22 cases, R1 PE23–PE26, plus PE27–PE28.
