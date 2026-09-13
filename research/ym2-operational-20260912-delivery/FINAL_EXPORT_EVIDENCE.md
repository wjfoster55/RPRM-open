# Final export evidence — PASS

Archive: `YM2-operational-seam-2026-09-12.zip`  
SHA-256: `19c6b86a31ebdea7d4c6f83a332a472cc3fabdcc3a908512b7f1616c65bc7d05`  
Size: 3681951 bytes; 53 payload files.

The ZIP passed CRC, duplicate-member and extraction-path checks. Every
freshly extracted file matched the frozen source and manifest. The new
standard-library checker passed 633 exact assertions
under isolated Python with bytecode disabled. Its entire JSON output
matched RESULTS.json, with zero exit status and empty stderr. Source,
extraction and ZIP bytes remained unchanged after replay. No old checker
was run, and no package installation was needed for portable replay.

Four reviewed notes match the independent review's final SHA-256 bindings.
All 37 top-level local links resolve inside the packet; all
31 accepted snapshots match their recorded originals.
The previous frozen YM construction ZIP is included unchanged. Historical
links inside unchanged snapshots are not asserted portable. The final
3200 by 1800 plot was visually inspected and its annotation was moved to
avoid the response curves; PNG, SVG and drawing source are included.

FINAL_EXPORT_EVIDENCE.json records the exact interpreter, command, receipt,
link checks, source hashes, review bindings and archive identity. Actual
stdout/stderr are adjacent. These sidecars were created after freezing and
replaying the ZIP. This is execution and byte evidence for the delivered
packet, not a formal proof, external peer review, novelty certificate or
quantum Yang-Mills continuum mass-gap result. Publication remains on hold.
