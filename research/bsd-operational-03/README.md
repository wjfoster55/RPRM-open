# BSD operational continuation03

Read [RETURN_TO_WILLIAM.md](RETURN_TO_WILLIAM.md) for the result and
[BSD_REBRIEF.md](BSD_REBRIEF.md) for the concise frontier. This successor
recovers operational value, implements an invertible two-shadow adapter,
and proves nonvanishing of E34's cyclotomic5-adic regulator. Full BSD is OPEN.

From this directory:

```text
python -I -B work/run_operational.py --output runs/my_fresh_run
```

Requires Python3.10+, assertions enabled (no `-O`), no packages or network.
The output directory must be new. The runner snapshots `work/*.py` and
`input_source/*.py`, then generates every calculation witness afresh.
Its four stages take about30 seconds on the recorded machine. Any failure
retains its output and an OPEN status. Earlier result directories remain
unchanged. The included final run is `runs/return_validation/RUN.json`.

| File | Responsibility |
|---|---|
| `work/rational_ec.py` | Exact rational point arithmetic |
| `work/padic_height.py` | Exact5-adic height residues with theorem-backed tail bound |
| `work/padic_height_readback.py` | Separate duplication formulas, local checks and Frobenius irreducibility |
| `work/operational_shadow.py` | Complete finite quotient, inverse and rational mixed-height witness |
| `work/bockstein_readout.py` | Cofactor vector's first digit and determinant covariance |
| `work/run_operational.py` | Isolated fresh execution and source binding |

`input_source/` contains unchanged finite-field arithmetic from trace02;
no old numerical receipt is used as its input. `dependencies/` holds
unchanged earlier written proofs, with original source paths and hashes.
Their relative links refer to the original directories. The new scripts
do not read those proofs or old PASS records to obtain their answers.

[CONTRACT.md](CONTRACT.md) fixes carriers and receivers.
[OPERATIONAL_BRIDGE.md](OPERATIONAL_BRIDGE.md) explains the implementation.
[THIRD_RELATION_AUDIT.md](THIRD_RELATION_AUDIT.md) proves the comparison
criteria; [PADIC_HEIGHT_AUDIT.md](PADIC_HEIGHT_AUDIT.md) checks the external
theorems. [OPERATIONAL_VALUE_RECOVERY.md](OPERATIONAL_VALUE_RECOVERY.md)
and its evidence retain the original meaning and corrections.

`evidence/bockstein_readout.json` is the initial arithmetic run, with its
then-pending direction metadata. Its exact initial source is preserved in
`evidence/bockstein_readout_initial_source.py`. The subsequent theorem
audit closes canonical collinearity; the final fresh run contains the
corrected metadata and unchanged numerical result.

No formal proof assistant, universal operational solver, paper, publication,
or change to another research lane is claimed. A manifest binds bytes;
it does not prove mathematics.
