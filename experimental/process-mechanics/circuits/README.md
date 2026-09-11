# Circuits kit

**Question:** Which retained observations and plan facts suffice for a named
future threshold event or current reconstruction on the stipulated synthetic
RC/RLC models?

**Carrier / model:**
- RC: `R=1000 Ω`, `C=1 µF`
- RLC (optional tier): `R=200 Ω`, `L=1 mH`, `C=1 µF` (overdamped)

**Known vs hidden:**
- Known-plan null: present voltage + full future drive schedule.
- Withheld-plan twins: identical past prefix; future release differs.
- RLC: two noiseless timed voltages + constant drive; singular lag rejected.

**Ordinary comparator:** Exact discrete RC stepping; SciPy `expm` affine map
for RLC when available.

**Null / hostile:**
- Present-state sufficiency under known plan (easy null).
- Unprovided future input → opposite labels with equal past.
- Zero-lag / singular observation map → `SINGULAR_OBSERVATION_MAP`.
- Nonfinite voltages → admission error.

**Evidence grades:** see `KIT.json`. `PC-EST-01` remains `UNMAPPED` here.

**Run:**

```sh
python -I -B experimental/process-mechanics/circuits/example.py
python -I -B experimental/process-mechanics/circuits/check.py
```

Optional: NumPy and SciPy for the RLC section. Missing optional deps yield
`SKIP_OPTIONAL_DEPENDENCY`, not PASS-by-omission of a required check.

**Limitations:** Not a hardware certification or universal noisy observer.
