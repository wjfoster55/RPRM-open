# Return to William — RCF01-R1 review repair

**11 September 2026. Executed work, not a plan.**
Workspace `C:\github\RPRM-open`, git HEAD `4f5c8145a1d9389f28079ef63a385e406122fd34` (`main`), uncommitted local RCF01 + this R1 successor.
No commit, push, paper edit, package install, or RPRM context ticket.
Named source `RCF01-REVIEW-01`: `rctx.py reopen` returned `OPEN_SOURCE_MISSING`; this note is the handoff.

Active assignment: `CURSOR_REVIEW_REPAIR.md` in `C:\Users\bkbee\Downloads\RCF01-REVIEW-01.zip`
(SHA-256 `EA6FC79CA7CFC1AEFD12FD321F11811642ACC1B432E18351A4B47B8E74A0454D`).
`REVIEW.md` was supporting material, not a second job list.

## 1. What the assignment asked

Bounded scope: preserve completed RCF01 recovery/experiment work; export the
actual envelope, proofs, protocols, receipts, and `rprm.core`; repair named
status meanings; inspect/add one cube composition regression through the public
API; add a small export/record validator; clean-room replay the successor ZIP.
Do not restart the original project or begin a new research campaign.

## 2. REVIEW.md vs disk

Confirmed:

- First return ZIP was research-notes only (10 regular files). Experiment
  directory was absent from that upload. That is an export gap, not a failed
  experiment.
- Original recovery ZIP `7887e3a0518d8ac849f23305ed0e3a70abfe80ba160b786fc44ae0ad08e516f2`
  and `CONCEPT_REGISTER.source.md` `36f059195564fcc58a6a7f49e24eb5d736607ed85eff38a9a9b6ffda257558e2`
  still match.
- Starter checker `92e1be0ade3db207f16657a8234369097c0cedf755c5286c11b2305556f63466`
  matches the review baseline.
- `check_ids.py` is ID coverage only. The new export validator fails an ID-only
  disposable copy (exit 2) without claiming the live register lost meaning.
- Envelope protocol filename is `PROTOCOL.json`, version `RCF01-envelope-1`.
- PE01–PE22 were already on disk (`cursor_rcf01_envelope_02.json`, 22/22 PASS).

Refuted as “missing because never executed”: the experiment, proofs, 22-case
protocol, FAIL+PASS receipts, and `rprm.core` import all exist in this workspace.

## 3. What was repaired

Successor directory, original freeze untouched.

Frozen original hashes (unchanged):

- envelope `0e93e04d6aaa47419712110f69216dcd5bbf8ae98f0c5b5d2f22a6ad3999a1c3`
- protocol `381ff518623ae6c4ee95db287787c444bf8ded57a5b2e48fe60d27ae1c040c56`
- PASS receipt `c9246334d99eb2dabd7e325a46be69d577b3670793057a1b844980d5df2306e7`
- FAIL receipt `ee44d1d0e734e89196b3d34a1e1e345647b9630f50450d24e29d3822fdf66323`

Genuine implementation defect: `add_units` / `multiply_units` dropped backing,
so `(h*x)*y` could not reopen the composed table. Successor API keeps a composition
recipe, meters recipe work as `constructions`, and reopens the composed table
rather than an operand or a zero fill.

Status meanings: `STATUS_CORRECTIONS.md`. Finite fiving is **this round's finite
model**, not the whole source concept.

Composition regression: **not** an existing public-API case in PE01–PE22.
**Newly added** PE23–PE26. Development FAIL retained as `envelope_r1.json`.
Corrected PASS `envelope_r1_02.json` (26/26).

## 4. Executed results

Python 3.14.5, Windows-11-10.0.26200. Evidence class: constructed development,
not holdout.

### Workspace successor (`experiments/core_recovery_bridge_01_r1`)

| Command | Exit | Result |
|---|---|---|
| `python -B research/core-recovery-01/check_ids.py` | 0 | PASS, 13 IDs |
| `check_export.py --layout records` | 0 | PASS |
| `check_envelope.py --output runs/envelope_r1.json` | 2 | FAIL retained (PE24 distinguisher) |
| `check_envelope.py --output runs/envelope_r1_02.json` | 0 | PASS 26/26 |
| `--control omit` | 2 | FAIL, missing PE26 |
| `--control duplicate` | 2 | FAIL, duplicate IDs |
| `--control unexpected` | 2 | FAIL, UNDECLARED vs PE26 |
| `--control reorder` | 0 | PASS |

Successor source `0edf6572fd2c0319d443250caa342e091593fe919dca1c0d66416bcfb3d2d720`,
checker `22c44904ad180bcbb81de506e020b9ae14d5104f2d28652918143f38bec9323c`,
protocol `e7b9f81fbf1e55db9960cf4b22b305927bfad231019c950d8bf10e6e3910950d`.

| Case | Fiber / status | Grade |
|---|---|---|
| PE23 `(h*x)*y` hot C2 | ONE/EXACT zero 7-tuple; degree 1→2→3; cold_reads_delta 0 | finite test |
| PE24 arith flip | NONE/UNSUPPORTED | finite test |
| PE24 admitted, no backing | MANY/REOPEN_REQUIRED | finite test |
| PE24 backed recipe flip | ONE/EXACT; (0,1,1)=1 vs zero law 0 | finite test |
| PE25 corrupt / deleted operand | INVALID_DEPENDENCY / UNRESOLVED | physical mutation |
| PE26 `h+h` | ONE/EXACT C2; family `rational_cube`; value 2 | finite test |
| PE26 hot `0+hxy` | ONE/EXACT unique C2; full sums MANY(3) outside API | documented |
| Boolean zero-C2 source | MANY(2) | existing helper |

### Clean-room (extracted ZIP, PYTHONPATH empty)

Extracted to `C:\Users\bkbee\Downloads\RCF01-portable-r1_cleanroom`.
`python -B run_portable.py --output-dir runs/cleanroom_01` → overall exit 0.

| Job | Exit | Seconds |
|---|---|---|
| envelope 26/26 | 0 | 23.9 |
| omit | 2 | 23.2 |
| duplicate | 2 | 23.8 |
| unexpected | 2 | 23.4 |
| reorder | 0 | 24.2 |
| check_ids | 0 | 0.07 |
| check_export --layout export | 0 | 0.12 |
| starter 12/12 | 0 | 2.12 |

Packaged hashes in that replay matched the successor sources above.
`rprm.core` `a461bbeccd141caa10f3583b5cdb5c083d7032dbbd6793dd34a849efc69f3f0b`.
Donors: **NOT_REPLAYED**; logs only.

Disposable export mutations (copy of extracted tree):

| Control | Exit | Boundary |
|---|---|---|
| id-only records | 2 | empty required fields |
| missing-source | 2 | `prestige_envelope.py` absent |
| missing-receipt | 2 | `cursor_rcf01_envelope_02.json` absent |

First ZIP `research/core-recovery-r1/dist/RCF01-portable-r1.zip`
SHA-256 `aada35a24c136d323531c1288667b131aa209a3e26b572af9dab6c41577b01e5`
(relative output-dir quirk; replay still used packaged code). Corrected
entrypoint ZIP is `dist_02` after this note.

## 5. Preserved unchanged

- `research/core-recovery-01/` notes, register, source ZIP, `check_ids.py`
- `experiments/core_recovery_bridge_01/` sources, protocol, proofs, all runs
  including `cursor_rcf01_envelope.json` FAIL and `_02.json` PASS
- Deferred IDs RCF-P2, RCF-P3, RCF-N1, RCF-PI1 still NOT_RUN / DEFERRED
- Open seam fiving `{0,5}` splice vs Double-Stamp A5 restart still OPEN
- Publication rec: several destinations, one shared technical source
- No third prestige species, inverse-number dictionary, or forced merger

## 6. Open seams (not a new campaign)

- Fiving splice ↔ Double-Stamp restart commuting adapter: **OPEN**
- RCF-P2, RCF-P3, RCF-N1, RCF-PI1: preserved **NOT_RUN**
- Explicit Q-sum candidate-family propagation: **outside this API**
- Historical donor trees: **non-replayable** in the portable ZIP
- RCF-C2 witness still not attached to the envelope
- LawCube/RelationForge typed I/O sharing: **OPEN**

## 7. Key absolute paths

- `C:\github\RPRM-open\research\core-recovery-r1\RETURN_TO_WILLIAM_R1.md`
- `C:\github\RPRM-open\research\core-recovery-r1\STATUS_CORRECTIONS.md`
- `C:\github\RPRM-open\research\core-recovery-r1\INVENTORY.md`
- `C:\github\RPRM-open\research\core-recovery-r1\dist\RCF01-portable-r1.zip`
- `C:\github\RPRM-open\research\core-recovery-r1\dist_02\RCF01-portable-r1.zip`
- `C:\github\RPRM-open\experiments\core_recovery_bridge_01_r1\runs\envelope_r1_02.json`
- `C:\github\RPRM-open\experiments\core_recovery_bridge_01\runs\cursor_rcf01_envelope_02.json`
- Clean-room extract: `C:\Users\bkbee\Downloads\RCF01-portable-r1_cleanroom`
