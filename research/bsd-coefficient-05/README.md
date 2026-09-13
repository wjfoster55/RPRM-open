# BSD coefficient experiment05

The independently normalized analytic coefficient has now been computed:

\[
b_2=426\pmod{625}
 =1+2\cdot5^2+3\cdot5^3+O(5^4).
\]

This uses E34:y²=x³−1156x, its minimal Néron differential dx/(2y),
the period of one real component, the trivial Teichmüller branch, and
T=gamma−1 with the cyclotomic character of gamma equal to6. It is a
5-adic coefficient, not a real decimal estimate or the full BSD ratio.

`RETURN_TO_WILLIAM.md` explains the result and next gap.
`TWO_SCALES.md` displays the quantities being compared.
`COEFFICIENT_PROOF.md` gives the exact normalization and independent
Riemann-sum error proof. `PRIME_FAMILIES.md` recovers the earlier atlas.
`BSD_REBRIEF.md` records the resulting status changes.

On Windows, run with Python 3.10+:

```powershell
python -I -B C:/github/RPRM-open/research/bsd-coefficient-05/work/run_coefficient.py --output C:/github/RPRM-open/research/bsd-coefficient-05/runs/my_fresh_replay
```

After unpacking elsewhere, change the path. The output directory must be
new. The portable official PARI/GP 2.17.4 executable is included with its
complete official source archive and license. Linux/macOS users can use
their own GP 2.17.4 with `--gp /absolute/path/to/gp`.

The runner snapshots executable scripts and records all logs and hashes.
It rejects GP's interactive error output even when GP exits with code 0.
The accepted path uses no `msfromell`, numerical real-period matching,
`bestappr`, `ellpadicbsd`, database labels or saved PASS as an input.

The two analytic algorithms share the exact classical modular symbol;
one uses an overconvergent lift, the other an explicitly bounded ordinary
measure sum. Their agreement is checked, and each error claim is justified
separately. The arithmetic height is freshly replayed from rational points.
The old real interval is displayed as prior evidence, not re-certified here.

The exact 5-adic analytic order is 2 by the cited order theorem
and the nonzero coefficient. The canonical derived class is nonzero under
the [previously admitted BKS hypotheses](dependencies/PADIC_HEIGHT_AUDIT.md#bks-admission-and-nonvanishing-transport).
The exact real BSD identity and
total Sha remain OPEN.
