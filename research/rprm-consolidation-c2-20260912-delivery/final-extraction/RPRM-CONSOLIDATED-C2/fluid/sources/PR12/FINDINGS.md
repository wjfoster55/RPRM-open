# FINDINGS — RPRM fluid-adjacency / transport (first milestone)

**Date:** 2026-09-10  
**Repo:** `rprm-fluid-adjacency`  
**Stage:** discovery / reconstruction (not confirmation freeze; not domain-C transfer)

## Smallest useful retained description (so far)

For the declared outlet-exceedance receiver, a single current (or mean) outlet concentration is **not** a sufficient summary when mobile↔immobile exchange and immobile volume vary. Retaining **candidate histories** that carry distinct stored-immobile inventories (or equivalent exchange parameters) preserves distinctions that matter for the future interval. When those candidates disagree on the threshold question, the correct Process Mechanics output is **MANY**, not a forced ONE.

## Where it fails / remains open

- Confirmation protocol is **not** frozen; discovery examples were selected retrospectively (`results/discovery/`).
- Equal-budget conventional system-identification baseline is only sketched (current/history baselines + candidate gate); a full physics-informed calibrator with matched budgets is still ahead.
- Mass “residual” in passive summaries is a coarse final/peak aqueous-mass proxy, **not** a closed MF6 budget audit.
- Domain-C shallow-water transfer is reserved and untouched (`FROZEN_TRANSFER_PROTOCOL.md`).
- Haines scout is literature-only (`haines_scout/MECHANISM_CARD.md`); no timed reproduction.

## Verification (model software, not the scientific claim)

Official MT3DMS Supplemental Guide Problem **6.3.2** (production ± sorption, dual-domain) reproduced with local `mf6` 6.7.0 vs `mt3dms` 5.3.0:

| Scenario | max |C_MF6 − C_MT3D|/|C_MT3D| (time-aligned) |
|---|---|
| 632a | ~6.7e-5 |
| 632b | ~4.1e-5 |
| 632c | ~4.0e-5 |

Replay: `python scripts/run_verification_mt3dsupp632.py`

This verifies dual-domain IST capability under published assumptions. It does **not** establish the passive-tracer scientific model.

## Passive scientific successor (separately specified)

Nonreacting tracer; no production; no sorption. Controls: `dual_slow`, `no_immobile`, `rapid_equilibration`.

Replay: `python scripts/run_passive_dual_domain.py`

Discovery grid found **8** checkpoint-similar / future-disagreeing pairs (15 runs). Best pair (`z0.001_p0.1` vs `z0.02_p0.02`) yields candidate-gate status **MANY**.

Replay: `python scripts/run_discovery_search.py`

## Comparison at equal information (preliminary)

| Policy | Info used | Behavior on discovery best pair |
|---|---|---|
| current_reading | last outlet c | Forces ONE; ignores storage ambiguity |
| history_mean | mean outlet c | Forces ONE; can disagree with truth for other reasons |
| candidate_gate | admitted future predictions from candidates | Reports **MANY** when futures disagree — correct unresolved output |

Hypothesis (“present outlet can hide stored tracer that changes later release”) is supported at **simulated_model_episode** grade only. Slow exchange was **included** in the simulator; this does **not** claim RPRM discovered exchange.

## What is ready to freeze later (not yet frozen)

Candidate for a later freeze, after confirmation design:

1. Receiver: threshold exceedance on a predeclared future interval + NONE/ONE/MANY/OPEN/FALSE_ONE vocabulary.
2. Observer/evaluator split with policy-blindness tests.
3. Candidate-history gate that refuses to collapse MANY.
4. Requirement that baselines receive the same allowed input pool.

Domain-C adapter remains outcome-blind and not started.

## Hypothesis vs evidence labels

| Statement | Label |
|---|---|
| MF6 GWT+IST matches MT3DMS on official 6.3.2 obs curves here | **Evidence** (numerical verification) |
| Passive dual-domain column runs and controls execute | **Evidence** (local simulation) |
| Same checkpoint outlet / different future exceedance exists in this grid | **Evidence** (selected discovery) |
| Candidate gate is the right observation-purchase rule to freeze | **Hypothesis** (needs confirmation cohort) |
| Workflow will transfer to shallow-water domain C | **Open** (protocol only) |
| Haines jumps map to RPRM process digits | **Speculative / OPEN** |

## Machine-readable artifacts

- `admission/SOURCE_ADMISSION.md`, `admission/TOOLCHAIN.md`
- `protocol/passive_v0.json`
- `results/verification_mt3dsupp632/summary.json`
- `results/passive_dual_domain/summary.json` (+ witnesses)
- `results/discovery/same_summary_different_future.json`
- Unit tests: `pytest -q` (protocol/hash/blindness)
