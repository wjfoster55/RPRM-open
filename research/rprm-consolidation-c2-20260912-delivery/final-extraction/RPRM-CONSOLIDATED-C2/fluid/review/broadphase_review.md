# F1 broadphase source closeout

The saved canonical result supports a larger certification count for P than for the specified local CA+sleeping comparator, with zero **observed** false certifications in that saved suite. It does not establish runtime savings, production-engine superiority, dominance, or universal soundness. One fixed hostile replay in this review demonstrates a false certification by **both** P and CA+sleeping on an input accepted by the supplied simulator.

## Identity and evidence boundary

Repository: `wjfoster55/rprm-fluid-adjacency`; exact PR13 commit: `7e3a6603c8f3c036f9f59f519b069cfc02b7825f`. All `S/` references below expand to this exact local directory:

`C:/github/RPRM-open/research/rprm-consolidation-c2-20260912/fluid/sources/PR13/broadphase_lab/`

The coordinator verified acquisition against Git blobs. This review independently hashed the inspected bytes; hashes are in `review/broadphase_arithmetic.json`, including saved results SHA-256 `7a84024a988fdae62f290761b0fa1453945fdf5448eb040c895b59ae4b44a335`. The source/result files were not edited. The benchmark runner and diagnostic panel were read, never imported or executed. The only fresh dynamics check is the fixed three-disk case below, loaded from hash-checked in-memory copies of `sim.py` and `certificate.py`.

`S/README.md:66–85` attributes the retained summary to seed 7, 1,120 scenes, 160 per family and 25 evaluated steps per scene. The JSON itself omits seed, scene count and runtime metadata; the attribution is the source README's, not a newly regenerated panel. The runner defaults agree (`S/run_broadphase_experiment.py:39–41,135–159`). Only the canonical summary is retained in this broadphase artifact directory. Seeds 23/101/202 remain prose-reported results in `S/README.md:162–170`, not independently audited saved records here.

## Receiver and contract

The carrier is the supplied finite 2D disk `World`: positions, linear/angular velocities, radii, mass/inertia, static-wall configuration, gravity, timestep, restitution and friction (`S/sim.py:35–85`). Equal disk values do not erase body-index identities. A disk-disk island is a connected component at the current receiver band; wall contacts do not join separate disks (`S/certificate.py:48–84`). The supplied ports are the current world, island and contact-pair set; the requested readout is whether the set of pairs incident to those same body identities changes after **one complete simulator step**, including additions to outside bodies (`S/certificate.py:90–99`). This is a forward finite prediction, not an inverse/completion-fiber solution.

Receiver membership is strict surface gap `< 0.03`, with disk-disk labels `(i,j)` and fixed negative wall labels (`S/sim.py:22–29,243–257`). Reference evolution integrates gravity, constructs contacts at the different band `0.05`, performs 12 sequential-impulse iterations, then updates positions and angles (`S/sim.py:152–177`). This is the discrete toy oracle, not independent real-fluid or production-engine ground truth.

## Reconciled claim ledger

Every source path in this table has the PR13 commit identity above.

| Exact claim under review | Receiver and conditions | Source path/lines; evidence type | Observed result and metric/denominator | Corrected wording | Unresolved obligation |
|---|---|---|---|---|---|
| P gives a 1.11× advantage | One-step incident pair-set equality; canonical exposed suite | `S/artifacts/broadphase_results.json:1–44,356–366`; saved summary plus fresh arithmetic; `S/run_broadphase_experiment.py:106–122,214–217` | P `51,742/70,221 = 73.6845103%`; CA+sleep `46,577/70,221 = 66.3291608%`; difference `7.3553495` percentage points; rate ratio `1.1108916418` | P certified more of the saved island-step decisions at these operating points. This is a certification-rate ratio. | No elapsed-time comparison or scaling law follows; the fluid ~14× quantity is not a matched runtime comparator. |
| P saves 77.2% contact work and 73.0% body work | Weighted current contact/body counts over the fully evolved reference records | `S/run_broadphase_experiment.py:44–82,258–272`; source implementation and saved fractions at `S/artifacts/broadphase_results.json:374–386` | P fractions `.7720602518` contacts, `.7296269688` bodies; comparator `.5330837557`, `.5972920696`. Denominators are `sum(n_contacts)` and `sum(n_bodies)` over all records; contact division clamps denominator to at least 1. | These are potential weighted skips, computed after full reference evolution. | Numeric weighted denominators and numerators are absent from the saved summary. No actual skip path, timing, certificate overhead, or end-to-end equivalence was measured. |
| Comparison against the sophisticated production incumbent | Same receiver; same local addition guard | `S/certificate.py:273–307`; executable method definitions; `S/run_broadphase_experiment.py:85–103` | Naive is absolute-speed threshold alone; pure CA adds the guard and requires no existing receiver contacts; CA+sleep requires the guard and either no existing contacts or speed below threshold; P requires the guard and persistence test. | This is a comparison against the repository's local CA+sleeping implementation. | No actual Box2D, Bullet, TGS, or speculative-contact integration was measured. README claims at `S/README.md:3–12,47–55` exceed this evidence. |
| Zero-FP thresholds and ~75% coverage at 0.1% FP | Threshold selection using all exposed canonical records | `S/run_broadphase_experiment.py:125–132,153–163,232–250`; `S/artifacts/broadphase_results.json:4–5,365–366` | Search: 241 thresholds from 0 to 12 in steps of .05. Selected naive threshold 0, CA+sleep 1.6. Sensitivity uses **CA+sleeping**, with reported cert rate `.7473832614`, corresponding to 52,482 certifications. FP rate is `FP/70,221`, not `FP/(FP+TN)` or `FP/certifications`. | On this exposed sweep, local CA+sleeping reaches 74.7383% coverage with at most 0.1% false certifications per all decisions. | Actual FP count and selected sensitivity threshold are not saved. At this denominator the budget permits at most 70 FP; it is not a 0.1% bound conditional on the 838 changed cases. Threshold curves/raw records and prospective validation are absent. README's “plain velocity sleeping” wording at lines 21–22 and 213–217 is wrong. |
| Every disagreement favors P; advantage occurs only in slow_drift/mixed | Canonical pair-set receiver; family labels and the runner's separate speed category | `S/artifacts/broadphase_results.json:356–372`; `S/run_broadphase_experiment.py:205–230,252–255` | 5,754 P-only, all saved correct; 589 CA-only, also saved correct; net +5,165. All P-only are reported speed `> .5`; P-only also includes impact 316 and settled_stack 165. | P has an aggregate advantage and is not dominant. Moving is an observed category, not a family identity. | No row records are saved to audit speed minima or identify every case. Speed `>.5` does not itself prove impossibility for every velocity threshold or every future workload. README lines 154–156 contradict its own lines 107–110 and retained counts. |
| P is sound / fixes provide conservative sufficient conditions | Intended gravity/impulse/persistence bounds, actual discrete solver and arithmetic | `S/certificate.py:135–181,184–267,302–307`; `S/sim.py:152–240`; `S/README.md:172–193`; source inspection plus separate fresh hostile replay | Saved canonical P FP `0/70,221`, with 51,742 certifications and 838 changed cases. The fresh one-case replay falsely certifies with both methods. | Zero observed false certifications survives for the saved suite. Universal soundness over accepted `World` inputs is refuted by the retained hostile case. | A valid restricted-domain theorem would need explicit admission limits and proved bounds on all solver-induced motion; no such proof is supplied in the reviewed broadphase sources. |
| Pair-set equality permits cached manifold reuse and skipped narrowphase/solver state | Pair identities at band .03 only | `S/README.md:34–36,116–117`; `S/certificate.py:3–6`; actual data at `S/sim.py:89–145,152–177,192–234,243–257` | The receiver retains only pair labels. Detection also computes normals, gaps and contact offsets; solver computes impulses and uses band .05. | A valid pair-set certificate could preserve receiver pair membership for its declared one-step continuation. | It does not establish invariant normals, gaps, offsets, impulses, AABBs, velocities, or the solver's wider-band contact list. Those quantities must continue to update unless separately justified. |

The naive zero-FP point certifies no decisions, so dividing by its zero certification rate is undefined as a finite gain. The saved artifact writes nonstandard JSON `Infinity` at line 362; the arithmetic output keeps this as a disclosed artifact property and does not publish an infinite speedup.

## Non-dominance and family arithmetic

The source generates equal **scene** counts, not equal island-step counts (`S/scenes.py:162–180`). Family labels describe generators, not every later island's motion. The `slow_drift` generator itself includes both horizontal rows and free-falling chains (`S/scenes.py:42–72`); the `free_fall` family is a separate base-and-faller construction (`S/scenes.py:133–144`).

| Family | Island-step denominator | P certifications | CA+sleep certifications | P-only | CA-only, derived |
|---|---:|---:|---:|---:|---:|
| free_fall | 7,993 | 7,934 | 7,937 | 0 | 3 |
| impact | 8,617 | 2,721 | 2,422 | 316 | 17 |
| jitter | 12,299 | 2,597 | 2,724 | 0 | 127 |
| mixed | 12,000 | 12,000 | 10,353 | 1,647 | 0 |
| near_miss | 12,382 | 11,876 | 11,878 | 0 | 2 |
| settled_stack | 12,930 | 10,622 | 10,897 | 165 | 440 |
| slow_drift | 4,000 | 3,992 | 366 | 3,626 | 0 |
| Total | 70,221 | 51,742 | 46,577 | 5,754 | 589 |

Source ranges: `S/artifacts/broadphase_results.json:47–90,91–134,135–178,179–222,223–266,267–310,311–355,368–372`. CA-only per family is derived as `P_only - (P_certifications - CA_certifications)`, not read from raw decisions. The families sum exactly, as do their exclusive counts. In particular, impact has a positive P advantage of 299 decisions (about 3.47 percentage points), contradicting the blanket tie/absence-of-advantage wording at `S/README.md:133–138`.

## Soundness boundary and retained hostile case

The evaluated suite uses default `DT=1/60` and gravity 9.8; the runner passes `A_BOUND=9.8` and `SLACK=0`. Persistence accepts relative linear speed at most `.2` (code rejects `> .2`, whereas README says `< .2`). It uses the current normal separation speed and a `v_tan²/dist` term; the shared addition guard uses `speed_i + 2*max_cluster_speed` and a half-acceleration displacement term (`S/certificate.py:135–181,204–220,226–267`). Geometric fallbacks use `1e-12` and a shear denominator floor `1e-6`. Ordinary NumPy floating-point operations are used, with strict band comparisons and no outward-rounded interval proof. `World` permits nondefault gravity/timestep, while method defaults and runner parameters remain the module constants; a sound contract must require equality or explicitly pass matching parameters.

The effective-speed routine does not bound penetration stabilization, masses/inertia or angularly mediated friction impulses. The persistence routine's small present linear relative speed is not a proof of force balance through the next solver pass. `S/README.md:176–189` describes prior failures and fixes; `S/diagnose_fp.py:10–15,23–50` exposes persistence-tolerance exploration on generated panels. These are development/testing records, not an all-input derivation.

The fixed witness uses three radius-.5 disks at `(5,5)`, `(5.1,5)`, `(5,6.028)`, all initial linear and angular velocities zero, density 1, a 20×20 world, no walls, zero restitution/friction and default gravity/timestep. It is accepted by the constructors (`S/sim.py:38–70`). Disk pair `(0,1)` starts deeply overlapped, with gap `-.9`; pair `(0,2)` starts at gap `.028`. All three form one receiver island.

Both P guards return true, and CA+sleeping at 1.6 also returns true. In the actual step, Baumgarte stabilization (`S/sim.py:203–219`) converts the deep overlap into horizontal velocities approximately `-5.37,+5.37,0`. Pair `(0,2)` ends at gap `.03188868101166764`, crossing out of the receiver band. The pair set changes from `{(0,1),(0,2)}` to `{(0,1)}`. This is a finite, moderate-valued accepted input, not a reliance on infinite acceleration. It lies outside the initialized randomized scene mixture; no claim is made that the saved suite contained it.

The one fixed replay is preserved as `review/check_broadphase_hostile.py`, with results in `review/broadphase_hostile_result.json`. It verifies exact SHA-256 hashes of `sim.py` and `certificate.py`, refuses output overwrite, loads source bytes into memory copies and never imports the runner. It was run with Python 3.14.5 and NumPy 2.3.5; the result records executable/platform/dependency details. A fresh export can replay it from the fluid directory with an unused output path:

```powershell
python -I -B review/check_broadphase_hostile.py --output review/broadphase_hostile_replay.json
```

This counterexample limits the universal claims; it does not replace, silently repair, or contaminate the prior zero-FP summary. No additional cases, tuning or campaign are needed for this closeout.

## Reuse boundary

Even an actually unchanged receiver pair set establishes only label membership at band .03. For example, surface gaps .04 and .06 are both absent from this receiver, while only .04 belongs to the solver's band .05. Thus even equality of receiver sets cannot establish equality of solver candidate sets. For pairs that remain present, contact normals and separations depend on current positions, and impulses depend on current relative contact velocity, angular velocity, mass/inertia and accumulated impulses (`S/sim.py:101–114,179–240`). Updating these quantities is necessary to reproduce the supplied evolution. The saved runner performs those updates and never tests a frozen-manifold continuation. The retained moving cases support a contact-topology observation, not an unchanged physical or solver state.

## Scoped publication wording and disposition

In the source-reported canonical 2D disk experiment, P certified unchanged one-step incident contact-pair sets on 51,742 of 70,221 island-step decisions (73.6845%), compared with 46,577 (66.3292%) for the repository's local CA+sleeping comparator at an exposed-suite-selected threshold; neither method had an observed false certification in that saved suite. P-only and comparator-only counts were 5,754 and 589, respectively, so the result is an aggregate certification advantage rather than dominance. The reported weighted contact/body skips are retrospective potential-work measures, not executed runtime savings. A separate fixed three-disk replay demonstrates false certification by both methods when penetration stabilization creates motion from an initially motionless state, ruling out unrestricted soundness for accepted simulator inputs. These results support a bounded engineering observation about the declared pair-set receiver, with restricted-domain soundness, safe manifold reuse and end-to-end performance left unestablished.

**Broadphase disposition:** completed source/result reconciliation, with canonical finite observations retained; universal soundness refuted on the accepted input carrier; narrower soundness, complete-manifold reuse and performance claims unestablished. Dynamic-fluid and witnessed-invalidation dispositions belong to the coordinator's independent review and are not adjudicated here.

Created artifacts: this report; `review/broadphase_arithmetic.json` (saved-summary arithmetic and source identities); `review/check_broadphase_hostile.py` (one-case portable replay); `review/broadphase_hostile_result.json` (fresh observation and runtime). No source edits, installs, full panel replay, remote changes, commit or push were performed.
