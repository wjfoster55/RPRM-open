# Source admission — MODFLOW 6 dual-domain transport

**Date:** 2026-09-10  
**Status:** ADMITTED for local numerical study (verification + passive successor)  
**Claim ceiling:** Software documentation and reproduced numerical example support. Not a field claim.

## What was admitted

| Item | Record |
|---|---|
| Flow/transport engine | MODFLOW 6 GWF + GWT, executable `mf6` **6.7.0** (USGS / MODFLOW-ORG executables release 30.0) |
| Immobile storage/exchange | GWT-IST package (`POROSITY`, `VOLFRAC`, `ZETAIM`, optional sorption/decay) |
| Python interface | FloPy **3.11.0** (`pip`); writes MF6 input; does **not** embed the Fortran executable |
| Verification example | Official `ex-gwt-mt3dsupp632` (MT3DMS Supplemental Guide Problem 6.3.2) |
| Comparator engines | MODFLOW-2005 + MT3DMS 5.3.0 (same executables release) |
| License posture | USGS public-domain software family; FloPy BSD-style; local binaries downloaded via FloPy `get-modflow` |

## Governing equations (as documented)

- Steady confined 1-D flow with constant specific discharge into column cell 1 and constant-head exit at last cell.
- Transient solute transport with mobile and immobile aqueous domains.
- First-order mass transfer rate `zetaim` between mobile and immobile concentrations.
- Official problem 6.3.2 includes **zero-order production** and optional **sorption**; reproducing it as published is verification, not the scientific passive experiment.

## Units and volumes

- Length: meters; time: days.
- Mobile porosity and immobile porosity must be interpreted with `volfrac` (immobile volume fraction) as in the official notebook: MST porosity = mobile porosity / (1 − volfrac); IST porosity = immobile porosity / volfrac.
- Concentration and stored mass are distinct; convert with the corresponding aqueous volumes.

## Boundary / timing (verification problem)

- Grid: 1 layer × 1 row × 401 columns; `delr=2.5 m`, `delc=1.0 m`, top=1, botm=0.
- Specific discharge `0.06 m/d`.
- Source pulse concentration = 1 for 1000 d at inlet CNC; then 0 through total time 10000 d.
- Observation at x = 200 m.
- `zetaim = 1e-3 /d`, `volfrac = 0.2`, mobile porosity 0.2, immobile porosity 0.05.

## Outputs used

- GWT observation CSV of mobile concentration at the observation cell.
- Optional IST CIM file for immobile concentration (evaluator-only in later experiments).
- Budget / listing files for mass accounting when needed.

## Installation / run commands (this machine)

```powershell
pip install -r requirements\requirements.txt
python -m flopy.utils.get_modflow .\bin --repo executables --force
$env:PATH = "$(Resolve-Path .\bin);$env:PATH"
python scripts\run_verification_mt3dsupp632.py
python scripts\run_passive_dual_domain.py
pytest -q
```

## Explicit non-claims

- Reproducing 6.3.2 does **not** establish the passive-tracer scientific model.
- A modified no-production / no-sorption case is a **separately specified successor**, not an unchanged reference.
- No field release, remediation, health-threshold, or clinical analogy is claimed.
- Haines-jump scout remains a separate bounded literature admission (`haines_scout/`).
