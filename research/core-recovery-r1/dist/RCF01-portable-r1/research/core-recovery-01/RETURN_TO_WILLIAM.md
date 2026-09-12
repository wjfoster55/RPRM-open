# Return to William — RCF01 Cursor run

**11 September 2026. Executed work, not a plan.**
Workspace `C:\github\RPRM-open`, git HEAD `4f5c8145a1d9389f28079ef63a385e406122fd34` (`main`).
No commit, push, paper edit, or RPRM context ticket. Named source: unpacked
`RPRM-CORE-FORMALIZATION-01` plus copied recovery ZIP.

This Cursor run is distinct from the package's assistant development receipts
(`results/assistant_development.json`).

## What was already recovered vs what is new

**Recovered (preserved, not rewritten):** Prestige One as relationship/access
and earned operational use (U00, U10, U23–U25, U33); fiving `d=5h+r` and
strong winding; FIVE_IS_SAFE as type-finding with A5→B6→C7 authored dwell;
cube Möbius/zeta and grade-blindness; AD correction that prestige-as-policy
and F5/Z/6Z are not those meanings. Third prestige species, inverse 5/6/7/8
dictionary, and unrecorded sixing remain **explicit gaps**.

**Newly contracted this round:** an inspectable promoted envelope with three
separate families (rational cube, Boolean cube, Double-Stamp); C2 arithmetic
without reading omitted coefficients; cold-artifact reopen with physical
byte/frame/version checks; coherent vs fixed-receiver transport; fiving
slice adapter; source-declared split/midpoint/contract; `rprm.core`
quotient reuse. Written proofs in `PROOFS.md`. Finite tests PE01–PE22.

**Refuted as implementations, not as concepts:** C2-only reuse under `flip_h`
for arbitrary laws; vertex-count dwell; `count==5` / numeral-5 merger; `+4`
as fiving; two finite fivings as strong identity; accepting a mutated cold
file.

## Concept → definition → operation → counterexample → repair

### Prestige One (RCF-P1)

- **Definition (source):** a completed course may display as one while retaining
  a route into its construction. Visible `one` is not the strong object.
- **Operation:** exact reuse when the retained summary determines the admitted
  question **and** enabledness/successors; otherwise reopen cold content or refuse.
- **Counterexample:** two envelopes labelled `one` with the same C2 and different
  winding history (PE11). C2 pair `h+x+y` vs `h+x+y+hxy` (PE04).
- **Repair:** retain history when it is a question; reopen the omitted site/coeff
  when the operation leaves B2.
- **Fiber:** Boolean C2 summary → **MANY(2)**; with omitted site → **ONE**;
  missing cold + admitted flip → **OPEN**/`REOPEN_REQUIRED`; stale bytes →
  **NONE**/`INVALID_DEPENDENCY`.

### Fiving / FIVE_IS_SAFE (RCF-F1, RCF-F2)

- **Definition:** fiving is the C10 half-turn `+5` (not F5). FIVE_IS_SAFE is
  type-finding for a lawful STATE boundary; dwell is authored.
- **Operation:** adapter `A_r` to cube `h`-flip; Double-Stamp split/midpoint.
- **Counterexample:** `+4` disagrees on all 40 adapter cases (PE14). A5 and B6
  share quotient vertex count 3; only A5 admits dwell (PE12–13).
- **Repair:** keep winding; keep inversion/type; do not implement `count==5`.

### Cube (RCF-C1)

- **Definition:** unique multilinear expansion on `{0,1}^3` over `Q`.
- **Operation:** C2 closed under pointwise `+` and `*` (written proof).
- **Counterexample:** arbitrary-law `flip_h` sends B2 to the omitted vertex.
- **Repair:** keep `ahxy` / site 7, or transport the receiver with the view.
- **Positive simplification:** degree-`≤1` laws stay exact on C2 under `flip_h`
  (PE03/PE20). That is success, not suspicion.

### Checked connections vs OPEN connections

```text
CHECKED
  C2 +/*  <---->  cube Möbius (graded-scar donor, independent submask)
  C2 flip_h  --adapter-->  finite fiving display   (not strong winding)
  C2 flip_h  --separator-->  FIVE.future-style one-step distinction
  envelope reopen/refuse  <---->  prestige exact-reuse obligation
  A5 split B6 midpoint C7  <---->  Double-Stamp donor labels/dwell
  rprm.core.deterministic_quotient(clamp_h_0)=ACCEPT, (flip_h)=REJECT successor

OPEN
  fiving {0,5} splice  =?=  Double-Stamp A5 restart   (hypothesis; PE14 rejects naive merger)
  RCF-P2/P3/N1/PI1 experiments
  LawCube F2 / RelationForge shared I/O
  attaching ternary center-blind witness to the same envelope
  1-to-9 prestige lifecycle and uniform grade-to-grade operation lift
```

## Executed checks (this Cursor run)

Python 3.14.5, Windows-11-10.0.26200. Evidence class: constructed development,
not holdout.

### Starter (`check_bridge.py`, not the assistant receipt)

From `C:\github\RPRM-open\RPRM-CORE-FORMALIZATION-01`:

| Command | Exit | Status |
|---|---|---|
| `python -B check_bridge.py --output runs/cursor_rcf01_starter.json` | 0 | PASS (12 cases) |
| `--control omit` | 2 | FAIL as required |
| `--control duplicate` | 2 | FAIL as required |
| `--control unexpected` | 2 | FAIL as required |
| `--control reorder` | 0 | PASS |

`source_sha256 = 92e1be0ade3db207f16657a8234369097c0cedf755c5286c11b2305556f63466`
(matches package manifest). `protocol_sha256 = 5a559ffe…56cf4504`.
Starter output SHA-256 `6026cb4dcf9a270d130f20140cde4e9a87455392ccedd1b1dc83d7162515fe9c`.

Independent inspection of the starter identities used a **submask-walk** Möbius
and B2-pointwise multiplication in `prestige_envelope.py`, not a call into
`check_bridge.py`.

### Envelope (protocol `RCF01-envelope-1`, frozen before first envelope execution)

`python -B check_envelope.py --output runs/cursor_rcf01_envelope_02.json` → exit 0 PASS, 22 cases.

First file `runs/cursor_rcf01_envelope.json` is a retained development FAIL:
PE19 expected `REOPEN_REQUIRED` for an arithmetic contract that does not admit
`flip_h`. The correct split is `UNSUPPORTED` (outside contract) vs
`REOPEN_REQUIRED` (admitted, insufficient hot summary). That is not a silent
overwrite of the protocol.

Envelope controls: omit/duplicate/unexpected nonzero; reorder PASS.

Concept IDs: `python -B research/core-recovery-01/check_ids.py` → PASS, 13 IDs.

| Case | Fiber / status | Grade |
|---|---|---|
| PE02 C2 `+`/`*` | ONE/EXACT on all 65536 Boolean pairs | finite test of Identity 1 |
| PE04 C2+fiving | MANY + REOPEN_REQUIRED; readouts 2,2 → 3,4 | expected REFUTED |
| PE05 cold repair | ONE/EXACT | finite test |
| PE06 no cold | MANY / REOPEN_REQUIRED, fiber size 2 | finite test |
| PE07 altered/deleted cold | INVALID_DEPENDENCY / UNRESOLVED | physical mutation |
| PE08 coherent transport | ONE/EXACT on 48 cube symmetries | finite test of Identity 2 positive |
| PE10 two fivings | display identity, strong `(0,0,0)→(1,0,0)` | algebra + 70 samples |
| PE12–13 dwell | A5/C7 ONE, B6 NONE; count shortcut rejected | finite test |
| PE14 `+4` | 40/40 disagreements | hostile adapter |
| PE15 composition | A5→B6→C7→A5 with enabledness | finite test |
| PE16 broken composition | local PASS, composed dwell UNSUPPORTED | hostile |
| PE21 `rprm.core` | clamp ACCEPT; flip REJECT successor | existing quotient helper |
| PE20 affine class | C2 reuse succeeds | hostile to “universal compression failure” |

Instrument snapshot (not a benchmark): hot_ops 130, cold_reads 103,
constructions 74, checks 10, storage_bytes 3203, invalidations 2.
No runtime-advantage claim. Full-table, memoization, and C2 arithmetic **agree**
on B2 `+`/`*`; memo is ordinary caching; C2 is not required to “win”.

### Original donors actually rerun

| Donor | Command | Result |
|---|---|---|
| Fiving AB lift | `python -I -B verify_half_decade_fiving_ab_lift.py` | PASS, hashes match recovery packet, `tree_delta=0` |
| Double-Stamp | `python -I -B verify_double_stamp_seam_midpoint.py` | PASS, 26 hostiles, `tree_delta=0` |
| Graded scar cube | `python verify_graded_scar.py` | TOTAL FAILURES 0 |
| Ternary bridge (secondary) | `python verify_ternary_bridge.py` | TOTAL FAILURES 0; n=3 extra blind dim 10 |
| Prestige examples (7 Sep) | `python -I -B verify_examples.py --no-receipt` | PASS 2324+19 |

LawCube/RelationForge are on disk; full LawCube pytest was not rerun (no install;
F2 ANF is a different contract). Details: `DONOR_RECONCILIATION.md`.

## Required examples (one each)

1. **Positive reuse:** seven-coefficient pointwise `+`/`*` on all Boolean pairs (PE02).
2. **Operation-induced insufficiency:** C2 collision, after `flip_h` readouts 3 vs 4 (PE04).
3. **Successful coherent transport:** 48 symmetries, seven observations remain enough (PE08).
4. **State/operation-admission:** A5 dwell EXACT, B6 dwell UNSUPPORTED (PE12).

## Publication-placement note (provisional, after evidence)

Not a mandate to publish one large new paper.

1. **Companion/addendum** for recovered meanings and the source chain — appropriate
   as explanatory material; do not let the envelope example replace Prestige One.
2. **Absolute Distinction** — a short proposed bridge only: inspecting a retained
   distinction, a changed operation, a transported vs fixed receiver, and a repair.
   That is how distinction-inspection changes method. It is **not** a replacement
   AD definition, not unseen AD evidence, and not F5/Five. The AD thread keeps
   ownership.
3. **Separate methods paper** — not justified as novel mathematics (factorization
   and interpolation are inherited). The working title remains a label.
4. **Several destinations, one shared technical source** — **recommended.**
   Shared source: `research/core-recovery-01/` + `experiments/core_recovery_bridge_01/`.
   Cross-link; do not merge fiving with Double-Stamp or prestige-with-AD-policy.

## Open seams (not a new plan dump)

- Fiving splice ↔ Double-Stamp restart commuting adapter: **OPEN**
- RCF-P2, RCF-P3, RCF-N1, RCF-PI1: preserved, **NOT_RUN**
- RCF-C2 witness not yet attached to the envelope
- LawCube/RelationForge typed I/O sharing: **OPEN**
- Prestige 1-to-9 acquisition / uniform operation lift: **OPEN**
- No speed claim; meters exist for a later fair comparison

## Anti-forgetting pointer

`CONTENTS.md` and this folder. IDs must survive later consolidations
(`check_ids.py`). Deferred concepts stay in the register.

## Key absolute paths

- `C:\github\RPRM-open\RPRM-CORE-FORMALIZATION-01\CURSOR_START_HERE.md`
- `C:\github\RPRM-open\research\core-recovery-01\`
- `C:\github\RPRM-open\research\core-recovery-01\sources\RPRM-CONCEPT-RECOVERY.zip`
- `C:\github\RPRM-open\experiments\core_recovery_bridge_01\prestige_envelope.py`
- `C:\github\RPRM-open\experiments\core_recovery_bridge_01\runs\cursor_rcf01_envelope_02.json`
- `C:\github\RPRM-open\RPRM-CORE-FORMALIZATION-01\runs\cursor_rcf01_starter.json`
- `C:\github\RPRM-open\research\core-recovery-01\RETURN_TO_WILLIAM.md`
