# Original donor reconciliation — RCF01

Targeted interface comparison, not an archive rerun. Historical PASS files were
not treated as this run. Donors were executed from their own directories with
their own verifiers.

Workspace: `C:\github\RPRM-open` HEAD `4f5c8145a1d9389f28079ef63a385e406122fd34`.

## 1. Half-decade fiving AB lift

- Path: `C:\Users\bkbee\OneDrive\DOCUME~1-DESKTOP-06BJRV0-219031\ChatGPT\Quantum Research\experiments\RPRM_HALF_DECADE_FIVING_AB_LIFT_01`
- Command: `python -I -B verify_half_decade_fiving_ab_lift.py`
- Result: **PASS**, `tree_delta=0`
- `normal_sha256 = 47CF8322678D83D9E7254320A97D05A94079E4E82CBFA699E0EE80F80CC5B8AF`
- `mutation_sha256 = D3850D2F94E2C6838436DDF06E2E1FCF7951BE7D1C89E80A451B025AC32528ED`
- These match the hashes recorded in the recovery packet.
- Carrier: `C10` with `d=5h+r`; strong lift `n=10w+5h+r`; involution on the finite display; two fivings increment winding.
- Envelope adapter: `A_r(h,x,y)=(5h+r,x,y)` is a **new authored map** onto one cube bit. It is not the donor's full graph/fold verifier and is **not** strong-state equivalence.

## 2. Double-Stamp A5/B6/C7

- Path: `C:\Users\bkbee\OneDrive\DOCUME~1-DESKTOP-06BJRV0-219031\ChatGPT\Quantum Research\experiments\RPRM_DOUBLE_STAMP_SEAM_MIDPOINT_01`
- Command: `python -I -B verify_double_stamp_seam_midpoint.py`
- Result: **PASS**, `tree_delta=0`, 26 mutation rejections
- `normal_sha256 = 06550D157CF083507E2F6F87D115DF7614FA4344AD4E098EA602BFAE59C73082`
- Carrier: labelled graphs with fixtures `a0,a1,b0,b1,c,c0,c1,z`. Stage types: A5/C7 STATE dwell allowed; B6 EVENT dwell forbidden.
- Envelope implements those labels, quotient counts `(3,2,0)/(3,3,1)/(4,3,0)`, and the declared split/midpoint/contract transitions.
- The envelope graph check is a structural reconstruction plus authored permissions. It is **not** a substitute for the donor's two-implementation byte receipts.

## 3. Cube transform / checking theorem

- Path: `C:\Users\bkbee\OneDrive\DOCUME~1-DESKTOP-06BJRV0-219031\ChatGPT\Quantum Research\experiments\RPRM_GRADED_SCAR_CUBE_02`
- Command: `python verify_graded_scar.py` (numpy present; `-I` would hide it)
- Result: **TOTAL FAILURES: 0**; n=1..12 exact rational round-trip; n=3 grades `1+3+3+1=8`; k=2 kernel dimension 1
- Secondary: `python verify_ternary_bridge.py` **TOTAL FAILURES: 0**; n=3 headline 27 cells, 49 lines, rank 23, affine nullity 4, extra center-blind dims **10** reproduced
- `seal.py` was **not** run (would rewrite frozen `RESULTS.json`)
- Envelope Möbius is an independent submask walk on n=3 over `Q`, same formulas as Part A, different code from the donor and from `check_bridge.py`
- Address convention here: mask bit0=`h`. LawCube uses `LEX_X2_FASTEST` over **F2**, index `4*x0+2*x1+x2`. Those are different carriers.

## 4. Prestige / promotion / 7 September drafts

- Foam note: `C:\github\RPRM-foam-development\experiments\RPRM_CTHULHU_ZERO_PATH_MOTOR_AUDIT_08\POST_FREEZE_PRESTIGE_ONE.md`
- Self-promotion: `...\RPRM_CTHULHU_ZERO_X_FRAME_SEAM_AUDIT_12\POST_FREEZE_SELF_PROMOTION.md`
- September 7 drafts: `C:\Users\bkbee\OneDrive\DOCUME~1-DESKTOP-06BJRV0-219031\ChatGPT\RPRM Alpha\research\prestige-one-2026-09-07`
- Command: `python -I -B verify_examples.py --no-receipt`
- Result: **PASS**, 2324 positive checks, 19 mutation rejections (receipt not rewritten)
- Envelope implements the **exact-reuse / cold-reopen** obligation from “Prestige as acquired usable knowledge”, not the 1-to-9 cycle artifact, reflected board, or grade-64 DAG.

## 5. LawCube / RelationForge

- Present at `C:\github\LawCube` and `C:\github\RelationForge`
- Full LawCube pytest (2469) was **not** rerun: no package installation authorized; F2 ANF is not this envelope's Q-interpolation
- Schema compared from source: F2 Möbius `M_2=[[1,0],[1,1]]` mod 2 versus integer/rational subset Möbius used here
- Status: available, **not claimed as this experiment's verifier**

## Fiving ↔ Double-Stamp bridge (hypothesis, not forced)

Proposed maps, still **OPEN** as a commuting adapter:

| | Fiving splice | Double-Stamp restart |
|---|---|---|
| Carrier | `C10` / strong `(w,h,r)` | labelled graphs A5/B6/C7 |
| Boundary | `{0,5}` residual `r=0` | A5 (and C7) STATE |
| Operation | `+5` toggles `h`, retains `r`/`w` | split then midpoint |
| Enabledness | weaving designation at 0/5 | dwell at A5/C7, not B6 |
| Failure | `+4`; lost winding; treating two fivings as identity | vertex-count shortcut; dwell at B6 |

Equal numeral `5` does not share an operation set (PE14). Inability to make one bridge commute does not delete either concept.

Receipts: `experiments/core_recovery_bridge_01/runs/donor_*.txt`
