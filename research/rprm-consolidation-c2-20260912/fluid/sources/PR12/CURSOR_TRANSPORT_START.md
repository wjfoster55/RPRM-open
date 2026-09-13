# Cursor launch — RPRM Transport, discovery/reconstruction stage

## Task and limits

Create a new local project, provisionally `rprm-transport`, separate from the existing water, protein, cancer, and public RPRM repositories. Do not modify, push, or overwrite any of those projects. Begin with a source-grounded numerical study, not a UI, a large 3D field campaign, or a new physical-force claim.

**Scientific question:** Can a present outlet reading hide stored tracer that changes subsequent release, and can a limited, time-respecting observation account retain the information needed to predict that release?

**Method question:** Does the RPRM Process Mechanics template improve a declared prediction/observation task over competent conventional baselines, rather than merely restating the known fact that hidden storage matters?

All experiments are simulated conservative-tracer studies. No field release, remediation operation, patient experiment, or biological intervention is requested.

## 1. Admit the numerical source before the research claim

Inspect the official MODFLOW 6 groundwater-transport documentation, immobile-domain storage/exchange package, FloPy documentation, and the official one-dimensional dual-domain examples listed in SOURCES.md.

Record precisely what the chosen source supports: governing equations, mobile and immobile volumes, exchange law, units, boundary conditions, timing, mass balance, outputs, executable versions, licensing, and reproducible installation/run commands. FloPy is the Python interface; do not presume it supplies every required external executable without checking.

First reproduce one documented numerical verification example under its own assumptions. The official MT3D supplementary problem 6.3.2 examples include production and optional sorption; reproducing that example is a verification step, not the proposed passive experiment. Any removal of production/reaction/sorption belongs to a separately specified new model. Do not call a modified case an unchanged reference reproduction.

If toolchain access fails, produce a precise admission report and bounded fallback proposal. Do not silently substitute an undisclosed toy and label it a MODFLOW result.

## 2. Start small and physically legible

Use a one-dimensional column with a mobile transport region and a slow-exchange immobile region. The first scientific model uses a nonreacting tracer: no biological response, decay, chemical production, or unnecessary reactive complexity. Define concentration and stored mass separately and respect the volumes needed to convert between them.

Prepare different model histories using explicitly specified inlet/flow histories. Use a tracer pulse and subsequent tracer-free flow; a flow pause/restart can be a separate declared perturbation. Inputs after a comparison checkpoint must be identical when the question concerns different stored histories, not different future forcing.

Run no-exchange/no-immobile and rapid-equilibration controls. Check conservation and time/space refinement. A small numerical mass residual is not by itself evidence that transition timing, boundary conditions, or inference are right.

A retrospective search for same-summary/different-future examples is allowed during discovery. Mark those examples as selected. Do not use them as the confirmatory cohort.

## 3. Specify the receiver before scoring

Choose one primary question before the first held-out outputs. A suitable candidate is whether outlet tracer concentration exceeds a predeclared analytical threshold in a specified future interval under a known continuation input. This threshold is a model-study endpoint, not a health or safety standard.

Possible secondary endpoint: cumulative tracer mass released during that interval. Keep threshold classification, concentration-path error, integrated mass, and timing separate. A correct threshold answer need not determine the full internal inventory; an equal current reading does not determine the future.

Define how unresolved possibilities, no compatible history, and false unique answers are represented. Do not silently return a chosen candidate when the correct output is ambiguous.

## 4. Separate observer information from evaluator information

The observer may see only declared acquired records: for example outlet concentration, known flow, and any explicitly costed additional sampling position. The simulator's immobile inventory, exact hidden parameters, complete clean trajectory, and future target observations are evaluator-only unless a separate oracle diagnostic is named.

If retained histories are available on demand, declare acquisition, storage, and retrieval separately. If a sensor becomes active now, it cannot produce past records that were never acquired. Interpolated values from coarse data are predictions, not genuine new measurements.

Retain actual timestamps, units, sensor identity, candidate-history identity, and shared-error structure. Keep numerical solver timesteps distinct from observation schedules and from the times at which a controller changes input.

Test that changing evaluator truth cannot change policy actions. Test that changing future target data cannot change past outputs. Test that changing an unpurchased observation cannot affect the choice to purchase it. Dense evaluator recording does not demonstrate physical removal of a measuring interaction.

## 5. Compare against competent alternatives

Include an inexpensive current-reading/history baseline and a conventional physics-informed or system-identification baseline with the same allowed input pool and calibration budget. A proposed RPRM account must not win merely because it receives hidden storage while its comparator receives one scalar.

Possible components to investigate, each separately labeled:

- A richer observation or retained history that distinguishes otherwise merged futures.
- A prospective complementary-observation gate based on the admitted candidates' predictions.
- A bounded continuation/look-away prediction evaluated on withheld subsequent observations.
- An exact certificate cache replacing repeated calculations under an unchanged decision rule.

Keep policy quality separate from kernel speed. First establish exact output equivalence for a computational replacement; measure setup, memory, runtime, storage and retrieval separately.

Record both the cases improved by refinement and cases where tighter constraints falsely exclude an off-catalogue truth. Catalogue counts are not probabilities without a declared probabilistic model.

## 6. Discovery then confirmation

Use initial cases to understand which relationships matter and what current summaries miss. It is legitimate for that stage to change the proposed representation.

Then freeze a short protocol with the model family, candidate construction, calibration inputs, policies, thresholds, error process, observation budget, numerical requirements and primary endpoints. Generate independent preparation/parameter histories for confirmation. Do not split neighboring frames from a single preparation into supposedly independent trials.

Pair all policies on the same physical episode and physical-time error realization. Report all generated eligible cases, failed solves, absent witnesses, NONE/MANY/false ONE, missed events, latency, coverage and cost. If accuracy/coverage differs, do not present a lower total observation count as a free efficiency win. Compute latency only on declared matched sets and report unresolved/censored outcomes alongside it.

Do not claim RPRM discovered slow exchange merely because slow exchange was included in the simulator. The target is whether the template identifies and uses the right distinguishing information efficiently and transfers beyond the selected examples.

## 7. Deliver a compact report

Produce readable FINDINGS.md, source/assumption manifest, machine-readable protocol, per-case outcomes, hypothesis/evidence distinction, regression tests and replay commands. Store dense arrays locally with hashes; export only small required witnesses and selected traces for review. Do not build huge movies or export whole 3D volumes as the first milestone.

End the first report with: the smallest useful retained description found, where it fails, how it compares with conventional methods at equal information cost, and which rule is ready to freeze for a later domain. Mark model results separately from physical observations and any cancer/protein analogy.

No fixed RPRM numbered-stage sequence is required to pass. Provisional nested stages may be annotated only when grounded in distinct operations or events, with unresolved mappings left open.
