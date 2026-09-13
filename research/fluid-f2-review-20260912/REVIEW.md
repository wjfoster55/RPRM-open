# Independent evaluation of Cursor Fluid F2

**Disposition: reproducible, useful partial result; do not accept the general Layer B certificate or the combined router as sound.** The new wall-supported stack argument has a two-cell counterexample within its stated discrete model and ledge geometry. This is a correctness failure, not merely the acknowledged loss of efficiency on disconnected ledges. Layer A and full-state evolution with repeated Layer A checks retain a defensible, narrower result on normalized unit-mass inputs.

The original ZIP is 70,475 bytes, SHA-256 `45cac52b845b641838a11031f245a2c0a4342a3e69cec42fc17fe0b1320ba5e9`. Its input files are preserved under [input/fluid_dynamic_frontier_02](input/fluid_dynamic_frontier_02/README.md). Attached process instructions were read as the study's original specification, not as authorization to perform a new research campaign, change old results, or publish anything.

## What was verified

All 21 entries in the supplied HASHES.txt match their declared sizes and hashes. A fresh execution from the extracted ZIP reproduces all scientific fields in all 53 rows, all summary fields except elapsed time, and the result table after line-ending normalization. It reproduces 20 YES, 33 NO, zero panel errors, 10,125 reference steps and 1,771 candidate steps. The F1 regression again returns tall/flat 1/0, tall first breach 11 and peaks 22/0.

These are finite replay results. The supplied frozen panel does not contain the new hostile scene below. Therefore the replay and the counterexample are consistent: the original rows are reproducible, and the claimed general rule is false.

[REPLAY_RECEIPT.json](REPLAY_RECEIPT.json) records the checks and timing totals. The supplied runner does not regenerate rows_scientific.jsonl, despite the export prose referring to it; [verify_replay.py](verify_replay.py) explicitly removes the five timing fields and compares every remaining parsed field against both saved row files. Raw wall-clock row hashes are not expected to match a fresh run.

## 1. The new static NO certificate is refuted

The failed step is in [DERIVATION.md](input/fluid_dynamic_frontier_02/proof/DERIVATION.md), lines 104–110: it assumes the mass needed for a full column from a fringe cell down to a wall is a lower bound on the mass needed to create support. [bound.py](input/fluid_dynamic_frontier_02/src/bound.py), lines 281–282, turns that assumption into CERTIFIED_NO whenever V is smaller than sill_need. The official router accepts that NO and skips exact evolution.

Use the original 64×48 container, divider x=32 starting at y=36, the original right-compartment monitor, H=300 and strict threshold 0.5. Add ledge walls at (29,36) and (30,36). Place unit water cells at (30,34) and (31,34). All velocities normalize to zero; there is no sand, inflow or edit during evolution. Extra ledges are expressly part of the model contract.

The unchanged bound returns A=UNRESOLVED, B=CERTIFIED_NO, V=2, sill_need=12 and zero water on R_catwalk. The unchanged full oracle returns **YES at frame 3**, with monitored mass 1 and total water mass 2.

| Frame | Water positions | What happens |
|---|---|---|
| 0 | (30,34), (31,34) | Initial state. |
| 1 | (30,35), (31,35) | Both fall once. |
| 2 | (31,36), (32,35) | The first cell moves diagonally from its ledge and becomes temporary support for the second. The second moves sideways into the divider gap. |
| 3 | (31,37), (33,36) | The gap cell enters the monitor. |

The support need only exist when the second cell is processed. It does not need a permanent column beneath it. Stamping prevents one water occurrence from moving twice in a frame; it does not prevent that moved occurrence from supporting another. The same-row injection that Cursor described as a remaining question already breaks its proposed Layer B proof.

This refutes the general guarantee at the stated carrier; it does not estimate how frequently B fails. The exact reproducer, complete initial fields, 301-frame monitor series and early snapshots are in [audit_support](audit_support/LAYER_B_MATH_AUDIT.md). Run:

```powershell
python -I -B audit_support/check_layer_b_support_injection.py
```

The necessary correction is to treat the present B-only NO branch as UNRESOLVED and use the sound continuation, until a separately stated bound or admission guard has a valid proof. Preserve the five original B-only successes as observations and retain this counterexample beside them.

## 2. Fewer simulation steps did not mean less elapsed time

The saved rows contain the unfavorable timing result, but the return does not report it. Sum static preparation and the whole fallback wrapper for the candidate; compare with the whole reference wrapper. Do not add graph preparation a second time, because it is included in static preparation.

| Execution | Candidate preparation + fallback | Reference wrapper | Candidate/reference |
|---|---:|---:|---:|
| Cursor's saved rows | 4.3805 s | 1.4799 s | 2.96× |
| This review's fresh replay | 10.1643 s | 5.9684 s | 1.70× |

These are individual harness runs with process, I/O and diagnostic overhead, not a robust cross-machine engine benchmark. Both measured pipelines are slower for the candidate. Cursor correctly labels 1,771/10,125 as a step ratio, but a complete return should disclose this elapsed-time loss as well. Its active-cell counter excludes the graph work.

[oracle.js](input/fluid_dynamic_frontier_02/src/oracle.js), lines 130–135, rebuilds R_opt for every check: 1,794 graph evaluations in the scored panel. The graph depends on fixed walls, dimensions, monitor and the movement bound. It can be computed once per scene and reused while counting current water in it. Whether a revised implementation beats a matched reference requires measurement after the change.

## 3. The conventional comparison should include repeated reachability

The reported reachability_A comparator checks A only at the initial state and then waits for YES or the full horizon. The candidate checks that same ordinary reachability condition after every real update. Consequently, the 8,625-to-1,771 comparison combines B's effect with a stronger stopping rule withheld from that baseline.

A straightforward dynamic A comparator uses full-state updates and repeats A after each frame. The candidate already executes exactly that path on its unresolved scenes. Only the five B-only static cases needed additional runs to recover the complete comparator:

| Method | Total model-B steps on the original 53 labels |
|---|---:|
| YES exit only | 10,125 |
| Initial A, then YES exit | 8,625 |
| Dynamic A + YES exit | 2,105 |
| Supplied AB + dynamic A | 1,771 |

Thus B's incremental saving against dynamic A is 334 steps, 15.87%, on this panel. Because B is unsound, this cannot be accepted as a sound method's gain. The 2,105-step dynamic A result is useful surviving evidence; its full elapsed-time comparison is not measured by these reconstructed step totals. [Cost audit and six bounded controls](audit_cost/COST_AND_PROTOCOL_REVIEW.md) provide all accounting and duplicate checks.

## 4. Admission and panel descriptions need correction

The static path sums raw input mass, while the oracle turns each positive raw mass into a WATER cell and normalizes its mass to 1 before frame zero. Change the existing C_right_one input from mass 1 to mass 0.25: static A says NO, while the normalized oracle says YES at t=0. The written contract excludes fractional mass remaining *after* normalization; this example leaves none. A shared normalization map, or an explicit validated restriction of raw input to unit occupancy, is required. This is independent of the two-cell B failure, whose masses are already exactly one.

There are 53 labels but 50 distinct simulator inputs. All six width-two scenes named V180 actually contain 92 water cells because the generator runs out of positions; their result rows correctly record V=92. Preserve those rows and correct the fixed-volume family wording. The declared development panel is not held-out validation, and final hashes alone do not establish freeze chronology.

The model's odd-frame scan is reversed within each eight-cell chunk; chunks still advance left-to-right. The contract's whole-row right-to-left description should be corrected before proving any further injection or ordering lemma. The two-cell witness uses the actual pinned order.

## Mathematical scope of the surviving result

| Required contract | Reviewed meaning |
|---|---|
| Carrier, types, equality | Finite static-wall grids; empty/water/wall types; unit water occupancy after declared normalization; complete dynamic arrays, frame, stamps and chunk scheduler. States compare with all continuation-relevant fields retained. |
| Supplied and missing ports | Initial state, geometry, monitor, pinned updater, H=300 and theta=0.5 supplied; requested port is the future breach bit. |
| Operation and direction | Deterministic forward pinned model-B evolution, with no sand, inflow or edits. Walls remain fixed; particles have no upward move. |
| Receiver | Strict monitored mass >0.5 at any sampled frame 0 through 300. This does not ask for the full trajectory or physical fluid behavior. |
| Fiber and continuation | A fully supplied admitted state determines one trajectory and bit. A partial summary can merge many states; it is useful only when that bit is constant on the merged family. No complete inverse or globally minimal state is established. |
| Coverage, hostile case, evidence | Original panel: finite replay agreement. Layer B: refuted by a concrete admitted unit-mass ledge scene. Normalized Layer A: every real move is contained in the optimistic graph, whose complement cannot send water to the monitor. Full-state continuation preserves incoming influence. |

For normalized unit occupancy, Layer A's reverse reachable set contains every location from which an actual water occurrence could arrive. No inflow or upward/sand move can introduce an omitted occurrence. Checking the current monitored mass gives an actual YES; checking that no sufficient water remains in that set gives NO; otherwise exact evolution can continue to H. Ignoring graph-path time only enlarges the possible set, so a diameter assumption is unnecessary for this NO guarantee. This is an ordinary conservative reachability argument applied to the supplied simulator.

The appropriate closeout is: **F2 produced reproducible partial progress and a useful full-state early-stop route; its proposed additional static certificate is refuted, and this implementation did not demonstrate a runtime improvement.** A bounded correction can preserve that progress without restarting F1, altering its evidence, or extending the work into another physical model.
