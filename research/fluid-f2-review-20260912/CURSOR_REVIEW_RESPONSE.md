# F2 review findings for Cursor

The original ZIP and its 53 scientific rows reproduce. Keep that evidence unchanged. The combined F2 certificate cannot yet be accepted as sound.

1. **Layer B has an admitted two-cell false NO.** Original 64×48 container, divider x=32 from y=36, add walls (29,36), (30,36), water (30,34), (31,34), unit masses, normalize B, H=300, theta=0.5. Your bound says V=2 < sill_need=12 and CERTIFIED_NO. Your unchanged full oracle says YES at frame 3. At frame 2, the first cell diagonally enters (31,36), temporarily supports the next cell, and lets it move horizontally to (32,35). The next frame reaches the monitor. Full input, output and reproducer are in audit_support. This refutes the stack lower bound, not merely the claim that the method is fast on every ledge. Disable B-only certification or supply a new justified admission guard/bound; use UNRESOLVED plus the existing sound continuation until then.

2. **The raw static and exact paths use different normalization.** C_right_one with initial raw mass 0.25 returns static NO but normalized oracle YES at t=0. Normalize before both paths or explicitly validate a unit-only raw carrier. The current wording excludes fractional mass after normalization, which this control satisfies.

3. **Report the elapsed-time loss.** Your saved candidate preparation plus fallback totals 4.380499 s versus reference wrapper 1.479860 s. Graph preparation is nested in preparation, so do not double-add it. Repeated rebuilding of the invariant R_opt costs work: build it once per fixed scene and recheck occupancy. Do not claim a runtime win without a matched fresh measurement of the revised implementation.

4. **Use dynamic A as a conventional comparator.** The original initial-A baseline withholds your repeated-A stopping rule. Dynamic A takes 2,105 steps on the same panel; supplied AB takes 1,771. The B-only difference is 334 steps on the panel, and it currently belongs to an unsound shortcut. Full cost superiority versus dynamic A remains unmeasured.

5. **Correct scope and export details separately.** The panel is 53 labels/50 distinct inputs; six width-two V180 cases contain 92 cells. Odd scan reversal is per eight-cell chunk, not whole-row. The exported runner does not write rows_scientific.jsonl; provide a supported scientific-field comparison because wall times cannot reproduce byte-for-byte.

The surviving result is useful: normalized conservative reachability plus full-state exact evolution can stop many NO cases early. Preserve that result, the original panel, and these new counterexamples together. See REVIEW.md and REPLAY_RECEIPT.json for independently checked evidence. This file is a prepared review response; it has not been sent to another agent or service.
