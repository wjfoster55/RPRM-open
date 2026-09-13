# Toolchain pin

Recorded after local install on 2026-09-10 (Windows win64).

| Component | Version / id | Notes |
|---|---|---|
| Python | 3.14.5 | Local pythoncore |
| FloPy | 3.11.0 | `pip` |
| MODFLOW-ORG/executables | release **30.0** | `get-modflow --repo executables` |
| mf6.exe | 6.7.0 (02/05/2026) | SHA-256 `B0B70E1C4CDE6183932496B644563FD98867C520026321FD22A8FC796084FA1C` |
| mf2005.exe | 1.12.00 | Same release bundle |
| mt3dms.exe | 5.3.0 | Same release bundle |
| Plan zip docs | see root `manifest.json` | SHA-256 verified match on copy-in |

Binaries live under `bin/` (gitignored). Re-run `get-modflow` to restore.
