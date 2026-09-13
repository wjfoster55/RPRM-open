# Bounded admission and Layer A review

Input is the immutable `../input/fluid_dynamic_frontier_02` tree. This note is a code review plus the one-frame executable scheduler witness; it does not report a new panel campaign.

## Layer A survives on normalized binary water

Carrier: finite rectangular grid with Boolean wall occupancy, unit mass on each water cell, no sand or inflow, pinned model B initialized and normalized as declared, horizon 300 and strict threshold 0.5. Monitor entries refer to grid cells. The requested receiver is the breach bit over frames 0 through 300.

Every actual relocation is included in `src/bound.py:65`'s optimistic graph: vertical down 1 through 6 with wall-clear intermediate cells, or one horizontal/down-diagonal step to a non-wall destination. Compare `pinned/models.js:84` through `:109` and `:115` through `:121`. Boundaries are consistently blocked by `pinned/models.js:26` and `src/bound.py:42`; sleeping and stamps can remove moves but cannot add an omitted edge. A water cell starting outside reverse reachability cannot enter it, since any predecessor of a reachable vertex is itself reachable. Thus no water in that set remains no water in it. At theta 0.5, `water_in_R_opt <= theta` is exactly the zero-water condition because water mass is integral. Current monitor mass above theta is an exact t=0 YES.

Duplicate valid monitor indices are summed in both static and oracle readouts (`src/bound.py:143`, `src/oracle.js:91`). The graph deduplicates them, but at normalized unit mass and theta 0.5 duplication cannot change either the breach bit or the zero-water condition. No duplicate-index refutation applies to this frozen receiver. Larger thresholds or fractional mass remaining after normalization would require another contract.

Evidence grade: written argument grounded in the pinned code, not a formal proof or an exhaustive arbitrary-input test. No Layer A refutation found under this carrier.

## Raw initial mass has an undocumented stronger static precondition

`MODEL_CONTRACT.md:19` normalizes before t=0; `:25` includes initial mass fields in scene identity; `:52` excludes fractional mass *remaining after normalize*. It does not expressly require raw initial positive masses to equal one. The oracle converts every positive non-wall raw mass to WATER (`src/oracle.js:83` through `:88`) and normalization sets that mass to one (`pinned/models.js:957` through `:962`). Static evaluation instead directly sums raw masses (`src/bound.py:139`, `:143`, `:238`, `:261`, `:268`), and `src/run_f2.py:98` passes the raw scene array.

The cost review's saved witness `../audit_cost/audit_cost_results.json` changes C_right_one's single mass from 1 to 0.25: static A/AB returns NO; the normalized reference returns YES at t=0. This is a real API/domain mismatch under the literal pre-normalization receiver contract. It does not refute the binary frozen panel. Either static input must be normalized identically or its stronger binary precondition must be expressly admitted and enforced. This review did not rerun that witness.

## Scheduler prose differs from the pinned scheduler

`MODEL_CONTRACT.md:36` says odd frames scan right to left. `pinned/grid.js:146` always visits chunk columns in increasing order, and `pinned/models.js:78` through `:81` reverse cell order only within a chunk. `pinned/constants.js:13` sets CHUNK=8. Thus an odd 16-cell row scans 7..0,15..8, not 15..0.

Executed `node research/fluid-f2-review-20260912/audit_admission/scheduler_witness.js` successfully. The script reads the pinned files without editing them. For two normalized cells at (7,2),(8,2) on a wall-supported row, the actual frame-1 state is (7,2),(9,2); an explicit whole-row scan control produces (8,2),(9,2). See `scheduler_witness_result.json`. This demonstrates consequential state-transition ambiguity in the prose. It is not a Q_300 counterexample and does not impair Layer A's graph inclusion argument.

## Scope and non-findings

The scored runner constructs its own frozen scenes and exposes no arbitrary scene input CLI. Static and oracle functions lack explicit schema/domain admission checks, but malformed indices, dimensions, mass values, alternate thresholds, or a changed model are not evidence against the frozen panel. No such robustness test was promoted to a within-contract refutation here.

Separately, `src/scenes.py:134` describes placement Family A as fixed V=180, but the six width-2 columns generated at `:136` and `:144` hold only 2*(48-2)=92 cells; their IDs retain V180. The note records the actual placed count and result V is calculated from actual mass, so this is a family/ID description error rather than a wrong numerical readout.
