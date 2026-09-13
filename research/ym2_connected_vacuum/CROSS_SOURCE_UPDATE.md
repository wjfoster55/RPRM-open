# Update while the other tasks were running

The source-selection metadata is in [THREAD_SNAPSHOTS.json](THREAD_SNAPSHOTS.json).
The exact source-copy receipt is [SOURCE_PROVENANCE.json](SOURCE_PROVENANCE.json).
These are snapshots, not an assertion that either other task has finished.
Neither source task was edited, messaged, or rerun by this YM continuation.

[CROSS_PNP.md](CROSS_PNP.md) records the earlier snapshot, when the SAT pilot
specification had no execution results. At the later capture, completed
12 September 2026 at 18:42:14 UTC, that file had changed. The bundled
[updated SAT pilot](running_task_snapshots/liar-teacher-formalization-2026-09-12/SAT-PILOT.md)
reports the following source-task results:

- 24 exhaustive parity cases passed, together with two non-affine controls,
  276 recognizer truth tables, 38 projection systems and eight algebra-only
  cases. The reported exhaustive oracle examined 87,360 local assignments.
- Each local chain projected to one parity equation while preserving its
  complete boundary relation. The non-affine examples were explicitly
  declined by the affine recognizer instead of being replaced by a larger
  affine relation.
- Equal-capability Gaussian elimination already avoids point enumeration.
  The panel order sometimes reduces measured work but is not uniformly
  cheaper, even within the reported operation counters. The larger cases
  have no independent exhaustive oracle. The source leaves P versus NP open.

These are **read source claims**, not newly rerun or independently audited
SAT results. The useful YM transfer remains operation-preserving message
design and explicit coverage/cost boundaries. A compact parity equation
does not establish a compact all-order quantum vacuum construction.

The earlier [BSD audit](CROSS_BSD.md) used the exact source revisions
preserved in the bundled BSD files. Its generator and Sha claims remain
attributed to that running task. We import its complete-coverage and
remainder-ledger methods, not an elliptic-curve theorem as a physical premise.

The first capture script contained a transcription error in the expected
hash for BSD's INTERVAL_DERIVATION.md. Comparing the original audit table
with the actual copied bytes resolved it: the correct hash ends
`755bcb6600206`, and the bytes had not changed. The script and provenance
record were corrected before export. SAT-PILOT.md is the only captured file
that actually changed relative to its audit snapshot.

The audits are retained with their original retrieval times. This update
explains the later evidence instead of silently rewriting the history of
what was available when the transfers were first selected.
