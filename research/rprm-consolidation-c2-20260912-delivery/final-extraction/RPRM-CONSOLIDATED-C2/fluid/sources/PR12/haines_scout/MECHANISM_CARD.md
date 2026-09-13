# Haines jumps — mechanism admission card

**Status:** source-grounded scout (literature), not a run  
**Date:** 2026-09-10  
**Ceiling:** Extracted state variables and experimental affordances from published descriptions. No local reproduction yet. No clinical/remediation claim.

## Question (candidate, not established RPRM result)

Which small state description predicts whether the next interface event pauses, crosses one throat, or spans several — and which part of that description belongs to the surrounding apparatus rather than the pore alone?

## Sources inspected (titles / DOIs from plan SOURCES.md)

1. Zhang et al. (2026), *The Impact of System Softness on Haines Jumps and Drainage in Porous Media*, Water Resources Research, DOI [10.1029/2024WR039565](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039565).
2. Multiscale drainage dynamics with Haines jumps monitored by stroboscopic 4D X-ray microscopy, PNAS, DOI [10.1073/pnas.2305890120](https://doi.org/10.1073/pnas.2305890120).
3. OpenPNM invasion tutorial (pressure / connectivity / sequence): https://openpnm.org/examples/tutorials/09_simulating_invasion.html

## Extracted themes (admission, not re-derivation)

| Theme | What sources emphasize | Mapping caution |
|---|---|---|
| System softness / compliance | Apparatus and boundary compliance change jump magnitude, cooperative events, and apparent dynamics | Jump timing is not pure pore geometry |
| Stroboscopic / 4D imaging | Event definitions tied to interface motion across constrictions under continuous recording | One realization ≠ ensemble cycle reconstruction |
| Sequence vs clock | Invasion/drainage sequences give order and capillary pressure steps | Thresholded network invasion ≠ physical millisecond clock |
| OpenPNM drainage examples | Useful for pressure, connectivity, invasion order benchmarks | Do **not** claim timed Haines dynamics without an independently justified dynamic model |

## Smallest reproducible entry (proposed next, not executed here)

- Start from a published single-constriction or pores-in-series model with explicit compliance terms and measured time evolution.
- Prefer reconstructing a published figure/table over downloading large tomography volumes first.
- Compare any predictor against the paper's own physics-based predictor before claiming discovery.

## Admission verdict

| Item | Verdict |
|---|---|
| Can we cite physical-mechanism relevance for buildup/transition/continuation intuition? | **YES** (literature) |
| Can we reproduce timed Haines dynamics from OpenPNM alone? | **NO** without added dynamic/compliance model |
| Is RPRM process-digit mapping established? | **OPEN / speculative** — leave unresolved |
| Should this replace the transport project or consume domain-C holdout? | **NO** |

## Separation from transport build

Transport (`CURSOR_TRANSPORT_START.md`) remains the active computational reconstruction. This card is parked until a bounded single-constriction reproduction is authorized as a separate milestone.
