# RPRM Process Mechanics — fluid-adjacency research plan

**Date:** 2026-09-10  
**Status:** PROPOSAL. No new simulations, package installation, dataset acquisition, or repository changes were performed for this plan.

## Recommendation

Keep the existing water/clocks project running. Open **one** new computational project, provisionally `rprm-transport`, on conservative tracer transport with slow storage/exchange in porous material. Use it to reconstruct the Process Mechanics workflow from a different set of governing equations. Reserve a shallow-water propagation problem as a third-domain, outcome-hidden transfer test after the common procedure is frozen.

Haines jumps are a particularly relevant physical-mechanism lead, but start that as a bounded source/model-admission scout rather than a second large simulation campaign. `HAINES_SCOUT.md` keeps its question separate from the transport build.

## The proposed shared question

When several complete states or histories fit current observations, can we retain the distinctions needed for a specified future question and choose the next observation economically—without reading its outcome first?

Preserve three separate claims:

1. A physical mechanism causes the dynamics in a particular domain.
2. A selection or representation method improves a declared inference/prediction task in tested cases.
3. A computational replacement calculates the same result with identical declared semantics.

A success at one level does not automatically establish the other two.

## Why these domains

| Domain | Scientific role in this program | Main challenge introduced |
|---|---|---|
| Existing pressurized water network | Discovery source; preserve its frozen results | Unknown demand/history and competing network explanations |
| Porous-media tracer transport | Second reconstruction | Latent inventory, exchange rates, extended tails, and memory |
| Shallow-water waves | Reserved transfer destination | Propagation, travel-time uncertainty, and a deadline-sensitive receiver |
| Pore-scale Haines jumps | Physical-mechanism scout | Capillary interfaces, apparatus compliance, abrupt transitions |
| Water hammer | Alternate propagation destination | Wave speed, reflection, rapid valve/pump transients |
| Rainfall/runoff and drainage | Later operational transfer | Forcing history, infiltration, storage, backwater and control |
| Distribution-system water quality | Near-transfer convenience | Transport and tank mixing with substantially shared network assumptions |

This is a selected map, not an exhaustive list of fluid problems or a claim that all of them should become active projects.

## What transfers

Transfer the operational interface: receiver question, coherent candidate histories, observation functional/timestamps, allowed uncertainty, observation-selection rule, dependency certificates, explicit NONE/ONE/MANY, and justified stopping/reopening. Do not transfer water-specific tolerances, stage numbers, observation channels, physical equations, or field-accuracy claims.

The prospective water witness is an example of an observation-purchase rule: a nominated candidate path that would distinguish labels is a possible resolving outcome, not the actual unpurchased outcome and not a probability. The new project may discover that this particular rule is not appropriate. That is a discovery result, not an excuse to alter the existing water freeze.

## Program shape

**Discover in A → reconstruct in B → freeze the common procedure → test on C without outcome access.**

The second domain can be explored freely. The third domain is selected in advance, but its scored target outcomes must not inform the adapter or policy. Independent domain physics and known verification examples are permitted and necessary. See `FROZEN_TRANSFER_PROTOCOL.md` for what is fixed and what can change.

## Files

- `CURSOR_TRANSPORT_START.md`: concrete initial work order for the new project.
- `FROZEN_TRANSFER_PROTOCOL.md`: third-domain transfer design, still a proposal.
- `HAINES_SCOUT.md`: bounded physical-mechanism lead.
- `SOURCES.md`: official documentation and primary research inspected for feasibility. No execution of their software is claimed.
