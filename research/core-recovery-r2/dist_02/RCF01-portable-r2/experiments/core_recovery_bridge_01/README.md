# core_recovery_bridge_01

Operation-aware Prestige envelope for RCF01. Standard library plus adjacent
`rprm.core`. Does not import `check_bridge.py`.

```text
python -B check_envelope.py --output runs/fresh_name.json
```

Active Cursor receipt: `runs/cursor_rcf01_envelope_02.json`.
Protocol: `PROTOCOL.json` (`RCF01-envelope-1`).
Proofs: `PROOFS.md`.
`runs/cursor_rcf01_envelope.json` is the first development FAIL (PE19 expected
the wrong refusal status); it is retained, not overwritten.

Not claimed: novelty, physical safety, universal compression, runtime win,
fiving≡Double-Stamp, or holdout confirmation.
