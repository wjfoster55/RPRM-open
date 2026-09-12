# core_recovery_bridge_01_r2

Successor of the frozen R1 envelope (`../core_recovery_bridge_01_r1/`).
Protocol `RCF01-envelope-1-r2`: original 22 cases, R1 PE23–PE26, plus PE27–PE28.

```text
python -B check_envelope.py --output runs/fresh_name.json
```

Inherited R1 protocol copy: `PROTOCOL.inherited.json`.
Frozen original and R1 receipts stay in their experiment directories.
This directory does not overwrite `cursor_rcf01_envelope.json` or `envelope_r1_02.json`.

Finite fiving here is **this round's finite model** (`d=5h+r` on C10), not
the whole source fiving concept.
