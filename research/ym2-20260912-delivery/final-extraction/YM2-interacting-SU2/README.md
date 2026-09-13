# YM2 portable research result

Start with [RETURN_TO_WILLIAM.md](RETURN_TO_WILLIAM.md) for the result and
intuition. [MODEL_AND_DERIVATION.md](MODEL_AND_DERIVATION.md) gives the
constraint/gauge/units contract, exact witnesses, bounded repair and complete
conditioned fiber. [PROBLEM_BRIDGE.md](PROBLEM_BRIDGE.md) separates this result
from the quantum ambition. [SOURCES.md](SOURCES.md) separates literature,
accepted YM1 evidence and new derivations.

## Replay without installation

Python 3.10 or newer, standard library only. From this directory:

```powershell
python -I -B verify_manifest.py
python -I -B check_ym2.py --numeric --output ../YM2_REPLAY.json
python -I -B check_scalar_reference.py
python -I -B supplied/CODEX_YM2/verify_packet.py
```

On other systems use the available Python 3 executable with the same arguments.
The first and fourth commands check bytes. The second recomputes all scientific
rows; the third independently prints the six scalar reference series, to compare
with `review/FINAL_MATH_REVIEW.md`. Omitting `--numeric` runs exact calculations only. Omitting `--output`
prints the full result. Write fresh outputs outside the payload to keep the
manifest valid. The supplied YM1 checker is **not** part of this replay.

`RESULTS.json` contains exact rational strings, full state/series/control rows
and numerical diagnostics. `FREEZE.json` identifies the implementation and
assumptions frozen before the final source run. `MANIFEST.json` binds every
payload file except itself. `SOURCE_MANIFEST.json` binds the input provenance.
Hashes attest bytes, not mathematical truth.

The final exported archive is tested from a fresh extraction. Its SHA-256,
actual replay stdout, exit codes, runtime, fresh rows and payload-integrity
checks are external in the sibling delivery folder. They are not inserted
afterward into the archive whose bytes they identify.

No paper or publication is included. This folder is a bounded research record
and runnable counterexample package.
