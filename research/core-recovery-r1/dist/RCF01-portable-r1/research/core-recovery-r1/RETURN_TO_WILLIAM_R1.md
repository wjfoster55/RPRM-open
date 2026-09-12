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
- `check_ids.py` is ID coverage only: records-only export check PASSes on the
  live register; an ID-only mutation is required to fail the new validator.
- Envelope protocol filename is `PROTOCOL.json`, version `RCF01-envelope-1`.
- PE01–PE22 were already on disk (`cursor_rcf01_envelope_02.json`, 22/22 PASS).
  The review could not replay them because they were not in the first ZIP.

Refuted as “missing because never executed”: the experiment, proofs, 22-case
protocol, FAIL+PASS receipts, and `rprm.core` import all exist in this workspace.

## 3. What was repaired

Successor directory, original freeze untouched:

- Frozen original envelope SHA-256 `0e93e04d6aaa47419712110f69216dcd5bbf8ae98f0c5b5d2f22a6ad3999a1c3`
- Frozen original 22-case protocol `381ff518623ae6c4ee95db287787c444bf8ded57a5b2e48fe60d27ae1c040c56`
- Frozen PASS receipt `c9246334d99eb2dabd7e325a46be69d577b3670793057a1b844980d5df2306e7`
- Frozen FAIL receipt `ee44d1d0e734e89196b3d34a1e1e345647b9630f50450d24e29d3822fdf66323` (PE19 status split; not overwritten)

Genuine implementation defect (not in the original 22 cases): `add_units` /
`multiply_units` dropped backing, so `(h*x)*y` could not reopen the **composed**
table even when units had cold artifacts. Successor API keeps an in-memory
composition recipe, meters recipe work as `constructions` not extra silent hot
reads, and reopens the composed table rather than an operand or a zero fill.

Documentation: `STATUS_CORRECTIONS.md`. Finite fiving is named as **this round's
finite model**, not the whole source concept.

Composition regression: **not present** as an executable public-API chain in
PE01–PE22 (PE15 is stamp composition + add-then-clamp; PE02 is pairwise C2
arithmetic). **Newly added** as PE23–PE26. First successor run FAIL retained
(`runs/envelope_r1.json`, PE24 distinguisher typo). Corrected suite PASS
`runs/envelope_r1_02.json` (26/26).

## 4. Executed results

Python 3.14.5, Windows-11-10.0.26200. Evidence class: constructed development,
not holdout.

| Command | Exit | Result |
|---|---|---|
| `python -B check_ids.py` | 0 | PASS, 13 IDs |
| `check_export.py --layout records` | 0 | PASS |
| R1 `check_envelope.py --output runs/envelope_r1.json` | 2 | FAIL retained (PE24) |
| R1 `check_envelope.py --output runs/envelope_r1_02.json` | 0 | PASS 26/26 |
| `--control omit` | 2 | FAIL, missing PE26 |
| `--control duplicate` | 2 | FAIL, duplicate IDs |
| `--control unexpected` | 2 | FAIL, UNDECLARED vs PE26 |
| `--control reorder` | 0 | PASS |

Successor source SHA-256 `0edf6572fd2c0319d443250caa342e091593fe919dca1c0d66416bcfb3d2d720`
checker `22c44904ad180bcbb81de506e020b9ae14d5104f2d28652918143f38bec9323c`
protocol `e7b9f81fbf1e55db9960cf4b22b305927bfad231019c950d8bf10e6e3910950d`

Fibers / grades for the new cases:

| Case | Fiber / status | Grade |
|---|---|---|
| PE23 `(h*x)*y` hot C2 | ONE/EXACT zero 7-tuple; degree 1→2→3; cold_reads_delta 0 | finite test of Identity 6 hot half |
| PE24 arith flip | NONE/UNSUPPORTED | finite test |
| PE24 admitted, no backing | MANY/REOPEN_REQUIRED; no fabricated table | finite test |
| PE24 backed recipe flip | ONE/EXACT; readout (0,1,1)=1 vs zero law 0 | finite test |
| PE25 corrupt/deleted operand | INVALID_DEPENDENCY / UNRESOLVED; not an empty law family | physical mutation |
| PE26 `h+h` | ONE/EXACT C2; family `rational_cube`; site h = 2 | finite test |
| PE26 hot `0+hxy` | ONE/EXACT unique C2; mathematical full sums MANY(3) **outside API** | documented, not candidate propagation |
| Boolean C2 of zero | MANY(2) via `boolean_fiber_for_compact` | existing helper |

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
- Clean-room replay receipt is recorded after ZIP extraction (below or in
  `CLEANROOM_REPLAY.json` if this paragraph is the in-ZIP freeze)

## 7. Key absolute paths

- `C:\github\RPRM-open\research\core-recovery-r1\RETURN_TO_WILLIAM_R1.md`
- `C:\github\RPRM-open\research\core-recovery-r1\STATUS_CORRECTIONS.md`
- `C:\github\RPRM-open\research\core-recovery-r1\INVENTORY.md`
- `C:\github\RPRM-open\experiments\core_recovery_bridge_01_r1\`
- `C:\github\RPRM-open\experiments\core_recovery_bridge_01_r1\runs\envelope_r1_02.json`
- `C:\github\RPRM-open\experiments\core_recovery_bridge_01\runs\cursor_rcf01_envelope_02.json`
- Portable ZIP: `C:\github\RPRM-open\research\core-recovery-r1\dist\RCF01-portable-r1.zip`
