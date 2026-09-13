# RPRM consolidated C2 return

Start with **RETURN_TO_WILLIAM.md**, then **REBRIEF_ADDENDUM.md**. This is the
bounded F1/AD1/YM1 execution return requested on 12 September 2026. The supplied
handoff is preserved under `supplied/`; its old status notes and embedded commands
remain attributed evidence. This README describes the new deliverable.

| Location | Contents |
|---|---|
| `fluid/F1_CLAIM_LEDGER.md`, `F1_CLOSEOUT.md` | Reconciliation of three completed studies, with original successes, nulls and corrected claim scope |
| `fluid/sources/PR12`, `PR13` | Complete exact-pin repository snapshots; no repository internals |
| `fluid/review/` | Bounded second-reader broadphase audit and single retained hostile replay |
| `ad/AD1_DESIGN.md`, `AD1_RESULT.md` | New developmental scoped reuse specimen, conventional comparison and independent direct checks |
| `yang_mills/YM1_BRIDGE.md` | One physical model/observable/dynamics bridge, derivation and finite-box control |
| `supplied/accepted/` | Accepted C1 and SAT M1 closeouts, exact active builds and paired old final evidence; carried forward without complete replay |
| `supplied/sources/` | Frozen AD pilot review, Lind–Reichardt closeout and prior calibration/context used here |
| `provenance/` | Incoming identity, working environment, source acquisition and preserved-byte ledgers |
| `WORK_STATUS.json`, `DECISION_LOG.md` | One coordinator's dispositions, checks, boundaries and worker accounting |
| `PAPER_ROUTING_NOTE.md` | Claim-sized suggestions only; no existing manuscript modified |

To verify the exported files and replay only the newly authored bounded checks,
extract the delivered ZIP into a fresh directory and, inside `RPRM-CONSOLIDATED-C2`,
run with an existing Python environment:

```text
python -I -B verify_delivery.py --output-dir ../fresh-c2-evidence
```

The output directory must not exist and must be outside the extracted payload.
The new checks require Python 3.10+ (tested 3.14.5), its standard-library SQLite,
NumPy (tested 2.3.5, only the F1 hostile replay), and Node (tested 24.18.0, only the
F1 original-model witness). No installation, network service, GPU or paid compute
is needed in the environment used. If these runtimes are unavailable elsewhere,
report that prerequisite rather than counting a missing execution as a theorem
failure. No source arrays, aggregate panels, thresholds or closed suite are changed.

`DELIVERY_MANIFEST.json` binds each payload file except itself; the external ZIP
SHA-256 binds that manifest too. `verify_delivery.py` verifies source Git blob and
SHA-256 identities, runs the new entrypoints, and checks payload hashes again.
Its final receipts are intentionally outside the already-hashed ZIP. The supplied
separate final-evidence ZIP records the actual fresh-export replay and ZIP identity.
Integrity, written derivation, numerical execution and a bounded agent review are
different evidence grades; none is an independent physical experiment or formal
proof checker for a universal fluid/quantum theorem.

The old C1/SAT evidence archives inside `supplied/accepted/archives` are unchanged
dependencies with their own identities. Their historical PASS labels do not count
as executions in C2. The full C1 or SAT runner, SAT Task03, seed backfill, frozen
pilot scoring, Lind–Reichardt reconstruction and prior photon/cube checker are
deliberately outside the C2 replay entrypoints.
