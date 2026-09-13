# YM2 spatial joint — bounded continuation

Start with [the explanation for William](RETURN_TO_WILLIAM.md).

- [Actual seven-link model, constraints and separating witness](DYNAMICS.md).
- [Closed six-coordinate regular Hamiltonian and singular boundary](PHASE_CLOSURE.md).
- [Static joins, complete fibers, third-factor orientation and recovery](STATIC_JOIN.md).
- [Relational scaling and the next coarse-energy obligation](RELATIONAL_SCALING.md).
- [Named ChatGPT discussions and the concepts used](CHAT_BRIDGE.md).
- [Established sources and evidence grades](SOURCES.md).

This is a finite classical open lattice gauge model. The static algebraic
joint has a proved continuation law; the dynamical six-coordinate joint is
proved on the regular domain for as long as its configurations remain there.
General economical spatial blocking and singular phase coverage remain open.
Earlier YM1 and homogeneous YM2 results are accepted context, not rerun tasks.
This directory is self-contained for the new model, derivations and checks;
neighboring-directory references identify optional earlier research.

From this directory, with Python 3.10+ and no third-party packages:

```powershell
python -I -B check_dynamics.py
python -I -B check_static_join.py
python -I -B check_phase.py
```

Normal runs perform fresh computations without replacing receipts. The export
replay also compares their outputs or internal comparisons to the saved
RESULTS files and verifies every payload hash before and after execution.
Use the respective `--write-results` option only to deliberately regenerate
a receipt during development. Written coverage proofs establish continuous
fibers; finite tests alone do not establish those universal statements.

The portable ZIP's checksum and final extraction/replay evidence are stored
beside the ZIP, so the evidence does not purport to hash its own final bytes.
The earlier frozen YM2 ZIP remains unchanged.
