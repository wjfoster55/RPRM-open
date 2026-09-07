# Rule Lab

A dependency-free explorer for paired elementary cellular automata, exact relation views, retained block summaries and explicitly addressed finite prime comparisons. The mathematical model, presentation transforms and interface are separate files. All generated cells remain available even when the display shows a summary.

## Launch and controls

Open `index.html` in a modern browser that permits local HTML and JavaScript. On Windows PowerShell, a permitted local launch is:

```powershell
Invoke-Item .\index.html
```

No browser launch was performed during the standalone staging checks. Respect the host's URL policy. Browser behavior remains **NOT_RUN_UI**; the commands below verify pure calculations and static source bindings only.

1. Choose rules A/B, width, seed, retained row count and the spatial boundary. Rule numbers include both 0 and 255. Rule 86 is the left/right mirror of 30; the 30/83 preset is an independent custom comparison.
2. Select the initial seed: single center, center/right pair, centered triplet, echo offsets −21/−7/0/7/21, centered custom bits, exact full-width bits, or reproducible random band. B may use the same, mirrored or complemented seed. Fixed offsets outside the finite width are clipped; invalid or oversized custom strings are rejected. Every exact seed is displayed and exported.
3. Declare the first integer address and which selected relation values predict prime, then choose **Generate & compare**. Pending form changes do not change the displayed experiment or its exported model inputs.
4. Select A, B, XOR, agreement, AND, OR or four states. Changing the relation recalculates its finite comparison under the generated address settings. Palette and camera changes do not affect the counts.
5. Use Fit all, Center, the zoom and pan buttons, or the numeric scale. Drag pans, click selects an exact cell, and Ctrl + wheel zooms around the pointer. Plain wheel scrolls the page. With the drawing focused: arrows pan, +/− zoom, F fits, C centers, G generates, and 0–7 requests a manual level within the finite ceiling.
6. Select a block base of 3, 7 or 9 and a summary. Automatic mode chooses a level from the current scale; manual mode retains the requested admitted level. The selected exact cell determines the block whose full numeric summary table is shown.

The UI admits widths 1–257 and retained row counts 1–512. The pure model has a larger explicit cell-allocation limit; these UI limits are not mathematical limits.

## Exact model contract

The model takes an explicit binary seed, rule in `0..255`, retained row count, and boundary name `zero` or `periodic`. Row zero is the supplied seed; `rows` includes it. An update reads only the preceding row and updates all columns synchronously. For neighborhood `(left,center,right)`, the output is bit `4*left+2*center+right` of the rule. Displayed rule tables run from `111` down to `000`.

The zero boundary fixes every outside spatial input to 0 at every update; this is a finite-window boundary condition. Periodic boundaries wrap within exactly the supplied width. At width one, both neighbors refer to the sole source cell. Neither condition wraps time. The pure model also admits width zero or zero retained rows, preserving an empty grid and appropriate metadata.

Numeric bits must be actual 0 or 1. Strings, booleans, fractions, sparse holes and invalid values are rejected. Seeds may be arrays or `Uint8Array` values. Allocation and sieve limits are both 16,777,216. Returned typed buffers are caller-owned snapshots: wrappers are frozen but typed-array contents are not immutable. Do not mutate a retained base and continue treating it as the original. Functions never mutate supplied seeds or grids.

The three rule transforms are distinct involutions on the 256-rule carrier:

| Transform | New local output | Rule 30 image |
| --- | --- | --- |
| Mirror | `f(right,center,left)` | 86 |
| Output complement | `1−f(left,center,right)` | 225 |
| Black/white conjugation | `1−f(1−left,1−center,1−right)` | 135 |

A transformed trajectory also requires compatible seed and boundary transformations. Conjugation preserves the periodic convention; conjugating a zero exterior would require a one exterior. Complementing each local output does not make all future rows a simple color complement. No inverse for arbitrary time evolution is claimed.

`generatePair` aligns equal-width A and B seeds at the same row/column occurrences. Four-state code `A+2B` has the exact inverse `A=code%2`, `B=floor(code/2)` on codes 0–3. Binary views generally forget information. A/B, XOR and agreement each have two source pairs per admitted output. AND=1 fixes `(1,1)`, while AND=0 has three possible pairs. OR=0 fixes `(0,0)`, while OR=1 has three possible pairs. Retaining the pair preserves those distinctions for reopening.

```javascript
const M = require('./model.js');
const pair = M.generatePair({
  ruleA: 30, ruleB: M.mirrorRule(30),
  seedA: [0,0,1,0,0], seedB: [0,0,1,0,0],
  rows: 6, boundary: 'zero'
});
const view = M.relationView(pair, 'XOR');
const comparison = M.comparePrimes(view, {
  addressMap: 'row-major', start: 0, positiveValues: [1]
});
console.log(comparison.counts);
```

In the browser, `model.js` exposes `RPRMRuleLab`; `presentation.js` exposes `RPRMRuleLabPresentation`. Both also export CommonJS modules for Node.

## Retained summaries and inspection

At level ℓ, origin-aligned blocks have side `base^ℓ`, clipped at the carrier's right and bottom edges. Every level counts original cells directly, not a prior summary. Level 0 draws exact codes. Automatic selection takes the smallest level whose block spans at least 0.9 CSS pixel, stopping when one block covers the carrier. Manual levels have no hidden automatic override. Exact-level cells smaller than one pixel can be visually undersampled; numerical inspection still addresses the retained cells.

| Summary | Binary relation | Four-state relation |
| --- | --- | --- |
| Density | Ones / retained area | Separate A and B densities |
| Uniform closure | All zero or all one; otherwise mixed | One identical code throughout; otherwise mixed |
| Majority | 1 at or above half the area | A and B thresholds separately; ties go to 1 |
| Parity | Count mod 2 | A and B counts mod 2 |
| Count residue | Count mod selected base | A and B counts mod selected base |
| Edge pressure | Differing orthogonal neighbor incidences / `(4*area)` | Same receiver on relation codes |

Edge pressure counts neighbors inside the entire retained window, including neighbors across the selected block's edge. If both endpoints of an unequal edge lie in the block, that edge contributes twice. Exterior and periodic wrap edges are omitted by this summary, independently of the update boundary. These are declared finite scores. Colors blend their values; they do not decode the original cell arrangement. Empty helper blocks have empty readouts and null density/pressure. The exact pair is the retained reopen route.

The inspector always uses the selected relation, even when the drawing shows a prime overlay. Its nine roles include explicit boundary records. Periodic spatial slots can repeat source cells. Fixed exterior slots have A=B=0, so agreement is 1 there; they have no integer address. Rows before the seed or after the retained end are unknown under either spatial boundary.

The separate inspection law is the numeric second difference `u−2v+w`. Four radial checks cross the center: the two diagonals, vertical and horizontal lines. Four lateral checks use the top, bottom, left and right sides. Full check closure requires eight known zero residuals. Counterfeit central closure means all four radial checks pass but some lateral check fails. The synthetic four-state board `[0,1,0;1,1,1;2,1,2]` has radial residuals all zero and lateral residuals −2, +2, 0, 0; this is an admitted code example, not a claim that a chosen automaton generates it. A known nonzero check establishes an open condition; unresolved required slots cannot be counted as passes.

A fully known binary radial pass forces every entry to match its binary center, so that counterfeit case is impossible there. This follows because an opposite binary pair summing to twice the center must have both values equal to it. The CA update table separately shows the previous-row inputs, rule output and observed selected cell. Numeric inspection closure is not the update rule, an inverse for evolution, or a physical law.

## Prime comparison and exports

The conventional sieve classifies the full bounded integer interval, independently of the automata. A composite integer has a least prime divisor no larger than its square root; ascending prime passes mark multiples from `p*p`, retaining the first prime factor. Unmarked integers at least two are prime. Zero and one are nonprime and are not called composite.

The explicit address is `start + row*width + column`; an explicit subset of relation codes supplies predicted positives. No offset, rule, subset or best map is inferred. TP, FP, FN and TN, plus precision, recall, specificity, accuracy, F1 and prevalence, are computed from all exact cells. Undefined denominators return null. The interface also shows always-nonprime accuracy as a class-imbalance baseline. Agreement on a chosen finite map does not establish an unseen prime classifier or a new prime generator. Looking at many settings on the same data is not held-out validation.

Full experiment JSON exports explicit model inputs, both grids, relation values, certified truth, outcomes and metrics. Settings JSON exports complete seeds, model arguments, comparison parameters and current presentation settings. Replay its `modelInput` with `generatePair`, then use `viewMode` and `comparison` with the corresponding model functions. There is no automatic settings importer in this version. The PNG is the current viewport only, including any cropping, aggregation and selection outline; it excludes text tables and mathematical certificates.

The random-band convenience uses a uint32 linear congruential generator: update `word=(1664525*word+1013904223) mod 2^32` for each band column, then compare `word/2^32` to density/100. Exact keys and arrays are exported. This is a reproducibility mechanism, not a random-quality claim.

Working notes are separate from experiment data. Saving uses one browser-storage key; storage can be denied or unreliable for local files. A separate text download makes notes portable. Clipboard and download actions report failure when the browser API reports it. No network transfer is part of the tool.

## Verification status

**NOT_RUN_UI.** Browser rendering, keyboard/pointer behavior, accessibility, clipboard, PNG/file downloads, storage and responsive layout have not been verified. The mathematical and static checks below do not establish those behaviors.

Node.js 18 or newer is required. No package installation is needed. From this directory:

```powershell
node .\model.test.cjs
node .\presentation.test.cjs
```

These commands write fresh `.artifacts/model.json` and `.artifacts/presentation.json`. For aggregate integration, each accepts exactly `--output` followed by an absolute receipt path:

```powershell
$receiptDir = [System.IO.Path]::GetFullPath('.artifacts')
node .\model.test.cjs --output (Join-Path $receiptDir 'model.json')
node .\presentation.test.cjs --output (Join-Path $receiptDir 'presentation.json')
```

The runner writes PENDING before importing the model/checker, runs fresh assertions, checks source stability, then atomically publishes PASS or FAIL. PASS includes hashes of this package's current source files and this run's coverage counts. Exit code 0 means the assertions passed and the PASS receipt was written; 1 means execution or receipt I/O failed; 2 rejects malformed CLI arguments before tests. Relative paths, extra/duplicate arguments, unknown options and package-source destinations are rejected. A receipt publication error never counts as success; inspect the exit code as well as a receipt that may belong to an earlier run. Generated `.artifacts` evidence is not package source and is not a substitute for rerunning checks.

Model tests preserve independent string-table rule evaluation, all 256 rules, all seeds through width five at both boundaries and row counts 0/1/2/6, transform and trajectory symmetries plus a boundary hostile, relation fibers/readouts, trial-division sieve checks, explicit prime contingency cases and invalid-input controls. The classic-script export smoke test uses only a bare Node VM.

Presentation tests independently check deterministic seeds, direct block counts and all six summaries, clipped block partitions, spatial/time boundary slots, all 512 binary apertures, a four-state counterfeit witness, empty and missing-value cases, and camera anchor calculations. Static source checks parse JavaScript, inspect HTML IDs and numeric-input bindings, validate script order and check metric names. They do not execute the interface or a browser.

The tests grade conventional finite calculations and this implementation's stated scope. They provide no compression theorem, performance superiority, physical mechanism, or unbounded prime-prediction result.
