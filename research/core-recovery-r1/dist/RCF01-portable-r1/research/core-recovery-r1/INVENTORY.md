# RCF01-R1 inventory

## Present in the first returned ZIP (`core-recovery-01.zip`) but omitted from that upload

The reviewer listed these as reported-but-not-packaged. They exist in the
workspace and are included in the successor portable ZIP:

- `experiments/core_recovery_bridge_01/prestige_envelope.py`
- `experiments/core_recovery_bridge_01/check_envelope.py`
- `experiments/core_recovery_bridge_01/PROOFS.md`
- `experiments/core_recovery_bridge_01/PROTOCOL.json` (actual name; version `RCF01-envelope-1`)
- original FAIL `runs/cursor_rcf01_envelope.json` and PASS `runs/cursor_rcf01_envelope_02.json`
- envelope controls `runs/env_control_*.json`
- donor stdout logs `runs/donor_*.txt` (historical/local; donor trees not packaged)
- `rprm/core.py` and `rprm/__init__.py`
- `CONTENTS.md` RCF01 pointer

## Successor-only (not in the original 22-case freeze)

- `experiments/core_recovery_bridge_01_r1/` protocol `RCF01-envelope-1-r1` (26 cases)
- `research/core-recovery-r1/` notes and export validator
- `run_portable.py` at the export root

## Unavailable / non-replayable in the portable tree

- Original Alpha donor working trees (fiving, Double-Stamp, graded scar, ternary, prestige examples). Logs are historical. Claim: **reported local evidence**, not clean-room replay.
- LawCube/RelationForge full pytest (no install; not in this package).
- Held-out evaluator data: not requested and not included.
