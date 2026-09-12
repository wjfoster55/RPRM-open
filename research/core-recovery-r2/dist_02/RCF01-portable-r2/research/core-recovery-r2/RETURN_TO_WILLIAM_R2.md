# Return to William — RCF01-R2 guard repair

**12 September 2026. Executed work, not a plan.**
Workspace `C:\github\RPRM-open`, git HEAD `4f5c8145a1d9389f28079ef63a385e406122fd34` (`main`).
No commit, push, paper edit, package install, remote upload, or RPRM context ticket.
Named source `RCF01-R1-REVIEW-02`: `rctx.py reopen` returned `OPEN_SOURCE_MISSING`; this note is the handoff.

Active assignment: `CURSOR_RCF01_R2.md` in `C:\Users\bkbee\Downloads\RCF01-R1-REVIEW-02.zip`
(SHA-256 `9e9db1721d2e255aa697bf58e10c11c6f2f2e66b29507207968b092c446e3a64`).
`REVIEW.md` was supporting material, not a second job list.

## 1. What CURSOR_RCF01_R2.md asked

Bounded successor of reviewed R1. Preserve RCF01 and R1. Do not restart
original recovery or the R1 campaign. Repair only:

1. Full-output family rule for Q-addition versus Boolean multiplication.
2. Generic-map admission and degree metadata.
3. Aggregate runner verdict (JSON, printed status, exit code).

Then replay from a portable ZIP. No third prestige species, inverse-number
dictionary, or fiving↔Double-Stamp merger.

## 2. REVIEW.md versus disk

Confirmed on this workspace:

- Official R1 ZIP `research/core-recovery-r1/dist_02/RCF01-portable-r1.zip`
  SHA-256 `53d1e8761aeca98d26cb3732150af7a31ed109aad4e1c9187b3e4dc192315cea`.
- Reviewed envelope SHA-256 `0edf6572fd2c0319d443250caa342e091593fe919dca1c0d66416bcfb3d2d720`.
- Original envelope `0e93e04d…99a1c3`, protocol `RCF01-envelope-1`.
- Original FAIL `ee44d1d0…f66323`, PASS `c9246334…2306e7`.
- Concept register JSON `8843b2a0…015be0`; source.md `36f05919…7558e2`.
- Direct R1 API replay of the hidden sum: `s.family == boolean_cube` while
  omitted = 2. Named `flip_h` on `ARITH_CONTRACT` is `UNSUPPORTED`; generic
  map still proceeds. Mapping `(0,0,0,1,0,0,0,1)` on `h` advertises
  `degree_bound=1`.
- Review runner controls: starter exit 7 → overall PASS; export exit 2 with
  JSON status PASS; crash exit 1 counted as expected rejection.

The review's 26/26 envelope, 12/12 starter, 768-value oracle, and composition
recipe are accepted and were not rebuilt. `review_runner_controls.py` is a
fixture harness, not mathematical evidence.

## 3. What was repaired

Fresh successor only. Frozen RCF01 and R1 bytes were not overwritten.

| Repair | Disposition | Files |
|---|---|---|
| A. Family | Boolean sums lift to `rational_cube`. Boolean×Boolean stays Boolean. Mixed cube operands coerce to `rational_cube`. Invalid `boolean_cube` promotions are rejected. Hot add/mul still do zero cold reads. | `experiments/core_recovery_bridge_01_r2/prestige_envelope.py` SHA-256 `bebf2c25d26f2ecf92e3366082aaf38f4d379e18ac06ea0f1d9294ecc64ee3a8` |
| B. Maps | Certified generic maps are named coordinate maps with the same contract gate as `apply_input_map`. `apply_raw_site_map` is an unchecked helper: `degree_bound=None`, contract reduced to `read_admitted`. | same file |
| C. Runner | One verdict from every required job, including starter unless `--skip-starter`. Coverage rejection requires a FAIL receipt with `Coverage mismatch` or duplicate-ID coverage error. Crashes/missing/malformed outputs fail the aggregate. | `research/core-recovery-r2/run_portable.py` SHA-256 `46ef570e0cef28b41fd735985e5aa72cf6a41af42e93913118c686551e9239da` |

Protocol `RCF01-envelope-1-r2`: original 22 + R1 PE23–PE26 + PE27–PE28 (28).
Checker SHA-256 `635e28f19db32a74bc9689a8f92783904a0ab21aa171c5f75dcaadc8b1b417f9`.
Protocol SHA-256 `33ea582ebd832869c204cac061360899c8e9b7b39b5c668adb1ea2f7b61d8508`.

## 4. Executed results

Python 3.14.5, Windows-11-10.0.26200. Evidence class: constructed development,
not holdout. NONE/ONE/MANY only where the fiber is complete.

### Workspace successor (`experiments/core_recovery_bridge_01_r2`)

| Command | Exit | Result |
|---|---|---|
| `check_envelope.py --output runs/envelope_r2.json` | 0 | PASS 28/28 |
| `check_envelope.py --output runs/envelope_r2_02.json` | 0 | PASS 28/28 |
| `--control omit` | 2 | FAIL, missing PE28, coverage receipt |
| `--control duplicate` | 2 | FAIL, duplicate IDs |
| `--control unexpected` | 2 | FAIL, UNDECLARED vs PE28 |
| `--control reorder` | 0 | PASS 28 |
| `research/core-recovery-01/check_ids.py` | 0 | PASS, 13 IDs |

| Case | Fiber / status | Grade |
|---|---|---|
| PE26 `h+h` | ONE/EXACT C2; family `rational_cube`; value 2 | finite test (kept) |
| PE27 hot `hxy+hxy` | ONE/EXACT zero C2; family `rational_cube`; omitted `REOPEN_REQUIRED` | finite test |
| PE27 backed `hxy+hxy` | ONE/EXACT; omitted 2; flip `(0,1,1)=2`; family `rational_cube`; cold_reads_delta 0 | finite test |
| PE27 Boolean×Boolean | stays `boolean_cube` | finite test |
| PE27 mixed Boolean+rational add | ONE/EXACT; family `rational_cube` | finite test |
| PE27 invalid Boolean claim | rejected (`AdmissionError`) | finite test |
| PE27 unique C2 vs Boolean sources | C2 ONE; Boolean helper MANY; Q-sum candidates OUTSIDE_THIS_API | finite test |
| PE28 named and generic `flip_h` on ARITH | both UNSUPPORTED | finite test |
| PE28 non-coordinate map certified | UNSUPPORTED | finite test |
| PE28 raw helper | EXACT values; `degree_bound` unset; `certified=false` | finite test |
| PE28 clamp named/generic | EXACT; coherent hot identity EXACT without omitted value | finite test |

### Runner harness (fixtures; not mathematics)

`check_runner.py` against the extracted package, exit 0, PASS:

| Injected condition | Exit | JSON status | Printed status |
|---|---|---|---|
| Good fixture run | 0 | PASS | PASS |
| Starter exit 7 | 2 | FAIL | FAIL |
| Export fixture FAIL | 2 | FAIL | FAIL |
| Negative-control crash (exit 1, no receipt) | 2 | FAIL | FAIL |
| `--skip-starter` | 0 | PASS | narrower scope |

`check_export.py` does not hash-pin checker bytes, so fixture substitution still
reaches the aggregation boundary.

## 5. Portable replay

**Active ZIP:** `C:\github\RPRM-open\research\core-recovery-r2\dist_02\RCF01-portable-r2.zip`
(sidecar digest `RCF01-portable-r2.sha256` next to it after packaging).

Historical first packaging, not active:
`research/core-recovery-r2/dist/RCF01-portable-r2.zip`
SHA-256 `a06247f926b4e5834b1bf7a5ff995b65207399d31b294e359350ed33ef7d6487`.

Clean-room extract of that first ZIP to
`C:\Users\bkbee\Downloads\RCF01-portable-r2_cleanroom` with `PYTHONPATH` unset:

```text
python -B run_portable.py --output-dir C:\Users\bkbee\Downloads\RCF01-portable-r2_cleanroom_out
```

Overall exit 0, JSON/printed status PASS.

| Job | Exit | Seconds |
|---|---|---|
| envelope 28/28 | 0 | 17.16 |
| omit | 2 | 16.72 |
| duplicate | 2 | 16.65 |
| unexpected | 2 | 16.70 |
| reorder | 0 | 16.73 |
| check_ids | 0 | 0.06 |
| check_export --layout export | 0 | 0.11 |
| starter 12/12 | 0 | 1.96 |

Disposable export mutations on the extract: id-only, missing-source, missing-receipt
all exit 2.

Packaged hashes in that replay: envelope `bebf2c25…4ee3a8`, protocol
`33ea582e…1d8508`, inherited R1 protocol `e7b9f81f…10950d`, original protocol
`381ff518…040c56`, `rprm.core` `a461bbec…9f3f0b`.
Donors: **NOT_REPLAYED**; logs only.

## 6. What was preserved unchanged

- `research/core-recovery-01/` recovery archive and original concept register.
- `experiments/core_recovery_bridge_01/` including FAIL `cursor_rcf01_envelope.json`
  and PASS `cursor_rcf01_envelope_02.json` (22/22).
- `experiments/core_recovery_bridge_01_r1/` including FAIL `envelope_r1.json` and
  PASS `envelope_r1_02.json` (26/26). Composition recipe for `(h*x)*y` kept.
- Official R1 ZIP `research/core-recovery-r1/dist_02/RCF01-portable-r1.zip`.
- First R1 ZIP `research/core-recovery-r1/dist/RCF01-portable-r1.zip`.
- 13 concept IDs, meanings, anchors, unformalized remainder, deferred concepts.
- Named status meanings from R1 `STATUS_CORRECTIONS.md`.
- Original research-folder README still has only the R1 successor pointer;
  this R2 home is a new directory. Do not claim literally every old research
  byte is unchanged: that README already had the R1 pointer.

## 7. Open seams remaining (not a campaign)

- Fiving `{0,5}` splice commuting with Double-Stamp A5 restart
- RCF-P2, RCF-P3, RCF-N1, RCF-PI1 `NOT_RUN`
- Q-sum candidate-family propagation outside API
- RCF-C2 witness not on envelope
- Donor trees not replayable from ZIP
- LawCube/RelationForge typed I/O
- Coherent transport still reopens backing when present (correct values; not a
  speed claim)

## 8. Absolute paths

- Assignment: `C:\github\RPRM-open\research\core-recovery-r2\review\RCF01-R1-REVIEW-02\CURSOR_RCF01_R2.md`
- Successor experiment: `C:\github\RPRM-open\experiments\core_recovery_bridge_01_r2\`
- Official PASS: `C:\github\RPRM-open\experiments\core_recovery_bridge_01_r2\runs\envelope_r2_02.json`
- This note: `C:\github\RPRM-open\research\core-recovery-r2\RETURN_TO_WILLIAM_R2.md`
- Active ZIP: `C:\github\RPRM-open\research\core-recovery-r2\dist_02\RCF01-portable-r2.zip`

This bounded guard repair is finished. No further research assignment is issued.
