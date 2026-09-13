# rprm-fluid-adjacency

Local computational project for the **RPRM Process Mechanics — fluid-adjacency** research plan.

Provisional transport focus name from the plan: `rprm-transport`. This repository keeps the plan packet and implements the discovery/reconstruction stage for **conservative tracer transport with slow mobile↔immobile exchange**.

## Plan packet (from zip)

| File | Role |
|---|---|
| `README.md` (plan) | Program recommendation and shared question |
| `CURSOR_TRANSPORT_START.md` | Initial work order (this build follows it) |
| `FROZEN_TRANSFER_PROTOCOL.md` | Prospective third-domain (C) transfer template |
| `HAINES_SCOUT.md` | Bounded physical-mechanism scout (separate) |
| `SOURCES.md` | Documentation / paper leads |
| `manifest.json` | SHA-256 pins for the plan docs |

## What this repo implements

1. **Source admission** — `admission/`
2. **Verification** — official MF6/MT3DMS dual-domain problem 6.3.2
3. **Passive successor** — no production/sorption dual-domain column + controls
4. **Receiver / observer split** — `src/rprm_transport/{receiver,observer,baselines}.py`
5. **Protocol draft** — `protocol/passive_v0.json`
6. **Haines scout card** — `haines_scout/MECHANISM_CARD.md` (literature only)
7. **Findings** — `FINDINGS.md`

## Quick start

```powershell
cd C:\Users\bkbee\rprm-fluid-adjacency
pip install -r requirements\requirements.txt
python -m flopy.utils.get_modflow .\bin --repo executables --force
python scripts\run_verification_mt3dsupp632.py
python scripts\run_passive_dual_domain.py
pytest -q
```

## Non-goals (explicit)

- Do not modify existing water/protein/cancer/public RPRM repos from this tree.
- Do not treat verification production/sorption cases as the scientific passive model.
- Do not start domain-C shallow-water scoring or peek at held-out C outcomes.
- Do not claim RPRM “discovered” slow exchange merely because IST was enabled.
