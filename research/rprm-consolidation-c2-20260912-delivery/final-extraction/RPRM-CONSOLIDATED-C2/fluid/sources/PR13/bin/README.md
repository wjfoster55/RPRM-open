# Local MODFLOW executables

Install with FloPy (from repo root):

```powershell
python -m flopy.utils.get_modflow .\bin --repo executables --force
```

Expected programs for this project: `mf6.exe` (6.7.0+), `mf2005.exe`, `mt3dms.exe`.

Binaries are gitignored; pin versions and SHA-256 hashes in `admission/TOOLCHAIN.md` after install.
