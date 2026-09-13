# Final export evidence — PASS

Archive: `YM2-global-phase-joint-2026-09-12.zip`  
SHA-256: `c42d6cd9f09a8377af2eaff7b36f07ca69c553fe585cb0a0078c2f87f100062d`  
Archive bytes: 162537; payload files: 26;
uncompressed payload bytes: 459468.

The final archive passed CRC verification and was extracted into a new
directory. All 26 files matched their source bytes; the manifest
covered the other 25 files. All three new checkers ran successfully
from that extraction with isolated Python and bytecode disabled. Each
freshly recomputed and compared its complete saved receipt. All three
exited zero with empty stderr. Neither source nor extracted payload bytes
changed during replay. The archive checksum also remained unchanged.

The exact receipts cover 14 tree phase cases in two gauge representatives
each, six regular bridges, 3,008 invariant checks, and all 128 quantum
edge-support subsets plus exact Pauli and drift calculations. Continuous
and all-spin coverage rests on the written proofs and their stated
established inputs, not finite-test extrapolation.

An execution control additionally confirmed that the assertion-based tree
checker refuses optimized Python instead of reporting success with its
checks disabled. That deliberately rejected invocation is separately
recorded; the three mathematical replays all passed normally.

Nine named accepted source copies and their originals still match the
recorded SHA-256 values. Both earlier frozen YM2 archives retain their
expected hashes. No accepted YM1 or earlier YM2 suite was rerun.

`FINAL_EXPORT_EVIDENCE.json` records commands, paths, interpreter, counts,
hashes and exit codes. Individual stdout/stderr files are beside this
note. This evidence binds bytes and actual execution; it is not a formal
proof of the checkers' soundness, quantum limit construction, or continuum
mass gap. The sidecar is generated after the ZIP is frozen.
