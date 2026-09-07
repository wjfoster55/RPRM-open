# Response E

The answers below use only the supplied handbook and examination data. They are deductions about those supplied models, not reports of solver runs or physical experiments.

## 1. Refinement and distinguishing-word bounds

The carrier initially has eight source states and three distinct present observations. Completing every disabled action with a transition to one absorbing failure state gives **nine states**. The failure observation is tagged separately from every successful observation, so the initial observation partition has **four nonempty blocks**: three success blocks and one failure block.

Let the initial observation partition be round 0. Each refinement comparison retains the old block and splits it according to the successor blocks under every action. A strict refinement increases the block count by at least one. There can be at most nine nonempty blocks, so the number of strict refinement rounds is at most

`9 - 4 = 5`.

To connect this count to words, two states share a block at round 0 exactly when their answers agree for the empty word. Inductively, they share a block after round j+1 exactly when they agreed at round j and, under each first action, their successors agree through all suffixes of length at most j. Thus round j compares precisely the tagged answers for every word of length at most j. The absorbing failure state makes this statement include disabled executions.

If a refinement comparison produces no split, the partition is stable: applying the same successor-block rule again changes nothing, so no longer word can reveal a later distinction. Consequently, **every distinguishable pair of source states has a distinguishing word of length at most 5**. Pairs with different present observations are already distinguished by the empty word, of length 0. Pairs in the final same block have no distinguishing word at any length.

An implementation that performs five strict refinement comparisons can then perform **one final no-split comparison**, for **at most 6 total refinement comparisons**. This counts refinement passes after initialization, not individual state/action comparisons; an implementation may also stop earlier if it can recognize stability without that final pass.

These are upper bounds. The counts alone do **not** assert that five strict rounds occur or that any pair requires a word of length 5. Actual transition tables may stabilize sooner, and some pairs may have no distinguishing word at all. The generic eight-source-state bound of 7 is valid but weaker than the bound of 5 obtained using the supplied three observation values.

## 2. The chain and its shortest separating word

The carrier is `{x0,...,x6}`, the only action is a, and the receiver is the final tagged observation: successful execution returns `OK(9)` and disabled execution returns `FAIL`. For a nonnegative integer k, execution of `a^k` from xi succeeds exactly when

`k <= 6 - i`,

and then ends at `x(i+k)`. Indeed, there are exactly `6-i` enabled moves from xi to x6; the next requested move is disabled.

Therefore the shortest distinguishing word for x1 and x3 is **`a^4 = aaaa`**:

| Start | Execution | Tagged output |
|---|---|---|
| x1 | x1 -> x2 -> x3 -> x4 -> x5 | `OK(9)` |
| x3 | x3 -> x4 -> x5 -> x6 -> failure | `FAIL` |

For every length k from 0 through 3, both executions succeed: their endpoints are respectively `x(1+k)` and `x(3+k)`, and both observations are 9. The empty word is included in this check. Since the alphabet has only a, there is exactly one word of each length. This exhausts all shorter words and proves minimality. There is therefore ONE shortest word, `a^4`.

For this machine, n=7 and r=1. Adding failure gives eight states and two initial observation blocks, hence at most `8-2=6` strict rounds and a distinguishing-word bound of 6. The specified pair requires length 4, which is within that bound; a bound of 6 does not force this pair to attain 6. Separately, this particular machine does attain 6 for x0 and x1: both succeed for lengths at most 5, whereas `a^6` returns `OK(9)` from x0 and `FAIL` from x1.

## 3. Returning payload and stale validation

The candidate was validated against the parent state `(payload A, version 8)`. With one version increment for each accepted update, the intervening states are

`(A,8) -> (B,9) -> (A,10)`.

The current version is therefore **10**. The original candidate **may not install merely because the payload is A again**: its parent version 8 is stale. The parent identity must still match at installation. The failed installation leaves the current state `(A,10)` unchanged; installing a newly validated successor would require validation against the current parent.

An arbitrary nondecreasing version sequence alone does not guarantee detection. For example, it permits

`(A,8) -> (B,8) -> (A,8)`.

The version sequence `8,8,8` is nondecreasing, yet the final payload and version both match the old validation target. A check using only that pair would accept the stale parent as if no intervening update had occurred. Strict increase on every accepted update supplies the distinction that this weaker assumption lacks.

## 4. Vector acceleration versus radial-coordinate acceleration

The supplied instantaneous values are `r=5`, tangential speed `v_t=2`, and outward radial component of vector acceleration `a_r=-4/5`. Using the supplied coordinate identity,

`d²r/dt² = a_r + v_t²/r = -4/5 + 2²/5 = -4/5 + 4/5 = 0`.

Thus **the radial-coordinate second derivative is 0 at the specified instant**.

Moving inward is a statement about the first derivative: `dr/dt < 0`. The direction of vector acceleration describes how velocity changes, not the present sign of `dr/dt`. The supplied values contain no radial velocity, so they do not determine whether the object is then moving inward, outward, or instantaneously at constant radius. Even the computed `d²r/dt²=0` does not determine that first derivative.

The distinction is explicit on rearranging the identity:

`a_r = d²r/dt² - v_t²/r`.

The radial direction changes along tangential motion, giving the `v_t²/r` term. Consequently the vector acceleration can have inward component `-4/5` while the distance coordinate has second derivative 0. Identifying these quantities would discard that geometric term and give the incorrect answer `d²r/dt²=-4/5`. Circular motion is compatible with inward acceleration, but these instantaneous data alone do not prove a sustained circular orbit.

