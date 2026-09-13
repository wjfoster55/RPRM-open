# Final export evidence — PASS

Archive: `YM2-covering-argument-2026-09-12.zip`  
SHA-256: `02ceeb8207b862eb5034a9c24cff9e05566ed4636972e95146b6b673d0f6f5c5`  
ZIP bytes: 715218; payload files: 54;
uncompressed payload bytes: 1368236.

The final archive passed ZIP CRC and duplicate/path checks. It was freshly
extracted into a new directory. Every file matched the frozen source bytes;
MANIFEST.json binds all 53 other files.

The extracted verify_portable.py checked the complete manifest and executed
only check_covering.py and check_conditional_cover.py, with isolated Python,
UTF-8 and bytecode disabled. Both recomputed and matched their full saved
deterministic receipts. The verifier exited zero with empty stderr. Source,
extracted and ZIP bytes remained unchanged after replay.

The covering checker passed 22812 finite exact assertions,
including all 4,224 edge subsets of its two named fixtures and the hostile
cube boundary omission. The conditional checker verifies its rational tail,
head matching and complete bounded oscillation/support fixtures; its full
receipt is copied into FINAL_EXPORT_EVIDENCE.json. These are bounded controls,
not empirical certificates of the unrestricted analytic arguments.

All 30 top-level local file links resolve within the portable payload.
The 3200 by 1500 figure was visually inspected; SVG and drawing source are
included. The figure depicts analytic bounds, not a simulated spectrum.

The 13 accepted YM source files are byte-identical to entries in the earlier
frozen archive. The 18 official/current source snapshots match the bytes
observed in the official-docs audit. No old checker or other-lane task was
executed or changed. The earlier archive remains at SHA-256
`e520be5988a4106a91fdecb9df716d6fdf929d2113ca1ced820a7d1ca5923efd`.

Exact commands, interpreter, paths, stdout hash, complete conditional receipt
and link records are in FINAL_EXPORT_EVIDENCE.json. Actual stdout/stderr
files are adjacent. This sidecar was generated after freezing the ZIP;
it establishes execution and byte integrity, not a continuum theorem.
