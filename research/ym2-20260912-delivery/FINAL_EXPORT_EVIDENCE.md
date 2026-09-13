# YM2 final export evidence

**PASS.** Final source was frozen, checked, archived, freshly extracted, and
replayed from the actual exported bytes. Final replay outputs remain outside
the already-hashed payload.

- Archive: [YM2-interacting-SU2-2026-09-12.zip](YM2-interacting-SU2-2026-09-12.zip)
- SHA-256: `167e181c19e6c2a5dfdcb3e9956412251a8dcb9d808c7684e68393e7d86f1f8c`
- Archive bytes: 155781
- Payload files: 39 plus its manifest
- Exact source checks, independent scalar reference and optional small numerical
  illustration: PASS from source and final extraction.
- Packet transfer inventory: PASS, 23 files; accepted YM1 checker NOT_RUN.
- Exported manifest before and after replay: PASS.
- Full fresh result bytes equal packaged final-source result bytes: PASS.
- Archive SHA-256 unchanged after replay: PASS.
- New authored Markdown local links: PASS.

[Machine-readable evidence with commands, outputs and exit codes](FINAL_EXPORT_EVIDENCE.json)
and [fresh full result rows](FINAL_REPLAY_RESULTS.json) are external to the ZIP.
Python: 3.14.5; standard library only.

The mathematical result is exact failure of R3 and its one K refinement in the
declared interacting classical sector. A hash binds bytes; replay checks the
supplied executable calculations. Neither is a quantum mass-gap proof or a
general soundness proof of the checker.
