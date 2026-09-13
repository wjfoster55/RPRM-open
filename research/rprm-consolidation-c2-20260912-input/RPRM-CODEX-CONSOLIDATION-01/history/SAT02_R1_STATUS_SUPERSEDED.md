# SAT02-R1 status after SAT02-R1-CLOSEOUT

**12 September 2026. Overlay only. This file does not rewrite submitted R1 source, hashes, or tests.**

SAT02-R1 is accepted as a **partial research closeout**. It is not a whole-solver certification and not a completed ten-seed benchmark.

The submitted local receipt checker remains limited in two concrete ways:

1. Recovery may overwrite retained boundary variables and still receive `local_relation_checked`.
2. Fifty saved empty-relation receipts are falsely rejected for missing recovery. Those fifty remain mathematically valid in the separate review interpreter; they are not fifty wrong SAT/UNSAT answers.

A hash-pinned one-file candidate exists in `../sat02_r1_closeout_packet/` with disposition **REVIEWER_TESTED_NOT_INTEGRATED**. It was not copied into this tree. Live `sat_group_compiler/receipts.py` remains SHA-256 `ececdfdfa4c074b094810c1b58cfe081086cfd638f7e04f34cfc5997184d0c8d`.

This overlay qualifies the R1 owner-return row that called the receipt checker “repaired.” Group-ID, timer, and fingerprint repairs are unchanged. Missing seeds stay NOT_RUN. No Task03. No commit/push.
