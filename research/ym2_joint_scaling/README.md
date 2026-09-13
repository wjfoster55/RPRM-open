# YM2 joint and scaling follow-up

[Joint proof, scaling law and geometric explanation](JOINT_AND_SCALING.md).
[Independent review](INDEPENDENT_REVIEW.md).

The closed description is the joint Gram matrix of the homogeneous gauge
fields and electric velocities. It preserves future magnetic energy on the
invariant interacting domain, and has one amplitude/time scaling law for
its entire admitted scale family. It does not establish storage compression,
spatial gluing, a new universal RPRM definition, or a quantum spectral bound.

Replay the 2,312 exact assertions and compare with the saved full rows:

```powershell
python -I -B check_joint.py
```

Python 3.10+, standard library only. `--write-results` explicitly regenerates
`RESULTS.json`; normal replay leaves it unchanged. Original YM2 delivery bytes
remain frozen. The in-conversation visual is a separate explanatory output;
its plotted trajectories are numerical illustrations, not the exact proof.
