# core_recovery_bridge_01_r1

Successor of the frozen RCF01 envelope (`../core_recovery_bridge_01/`).
Protocol `RCF01-envelope-1-r1`: original 22 cases plus PE23–PE26.

```text
python -B check_envelope.py --output runs/fresh_name.json
```

Inherited protocol copy: `PROTOCOL.inherited.json`.
Frozen original receipts stay in the parent experiment directory.
This directory does not overwrite `cursor_rcf01_envelope.json`.

Finite fiving here is **this round's finite model** (`d=5h+r` on C10), not
the whole source fiving concept.
