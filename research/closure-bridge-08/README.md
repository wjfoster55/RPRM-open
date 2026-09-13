# Bridge 08 — approach the handoff from both sides

**The RPRM-first approach produced an exact new constraint on our BSD bridge.** Working backward from the receiving formula shows that a potential made only by adding independent single-height contributions cannot work on the admitted refinement grid. The curve's actual first point updates give a strictly nonzero interaction. We derived the pair products required to repair that candidate form.

This is a scoped obstruction and repair to the candidate grammar, not a new BSD identity. Its value is that the source data now discriminate a proposed bridge before we spend time refining more digits.

## The connected picture

The corpus recovery found William's earlier correction: **seven is the most complete state pre-carry**. That separates local completion from completing a receiving handoff. The eight/nine assignments in that historical experiment remain provisional. We have not replaced the process meaning with a count of seven Fourier slots, seven tests, or a claim that a conjecture is almost solved.

The current construction has three parts:

1. **Forward:** derive what the source can actually produce, retaining carry, occurrence, scale and interaction data needed by the next operation.
2. **Backward:** derive what an accepted receiving state would require, through the same explicit laws.
3. **Meeting:** require the same complete intermediate state, and distinguish one compatible witness from a conclusion forced for the actual source or every admitted source.

A simple example makes the difference visible. Starting at 7 and allowing five increments, a target of 12 works. At the split after two steps, both directions reach 9. A target of 2 does not work: the forward side reaches 9 while the backward side reaches -1. Both display digit 9, but their carry rows differ.

Your paired rise/fall idea has an exact implementation: reflection of the whole carry state converts increment into decrement. In base ten,

\[
(7,2)\to(8,1)\to(9,0)\to(10,-1)\to(11,-2)\to(12,-3).
\]

Each pair sums to nine. Conservation alone permits this to continue. A stopping argument also needs a justified lower bound or budget and enough progress at each unresolved step. A finite budget with ever-smaller expenditure can last forever; a replenished budget must retain its incoming contribution.

## What changed in the actual BSD calculation

Write the rank-two regulator readout as

\[
R(p,q,s)=pq-\frac{(s-p-q)^2}{4}.
\]

If one source refinement changes p by u and another changes q by v, their interaction is exactly `uv/2`. For the E34 points `P=(-2,48)` and `Q=(-16,120)`, fresh exact duplication gives

\[
u=\tfrac14\log(21025/16)>0,\qquad
v=\tfrac14\log(124609/65536)>0.
\]

Thus the mixed change in the comparison defect is

\[
-\frac{\Omega\sigma}{32}\log(21025/16)\log(124609/65536)<0
\]

for the actual positive period and a candidate positive integer sigma. An additively separable potential gives zero and fails. A candidate must include the corresponding joint interaction; separate storage of the heights is fine if its operations can form those products. This does not refute every possible potential or a rule confined to one locked sequence of refinements.

The exact unresolved question is now sharper: **what source-derived relation connects the analytic contributions to these coupled height contributions, with compatible initial and vanishing limiting boundaries?** Matching every local update still leaves an additive constant; choosing it to force one boundary can move the unknown defect into the other. The [BSD proof](agents/BSD_SEAM.md) makes that obstruction explicit.

## Files and fresh evidence

- [Forward/backward mathematical explanation](BIDIRECTIONAL_BRIDGE.md): reflected carry law, complete meeting fiber, existence/readout distinction, and paired-budget conditions.
- [Actual BSD seam](agents/BSD_SEAM.md): necessary interaction, exact point data, projective/gcd exceptions, asynchronous and locked-path scopes, and backward tail constraints.
- [Corpus recovery](agents/CORPUS_MAP.md): 36 checked source links, earlier user corrections, available lenses and remaining unassigned meanings.
- [Candidate freeze](PREFREEZE.md), [evidence provenance](PROVENANCE.md), [independent review](agents/REVIEW.md).
- [Bridge checks](evidence/bridge.json): 270 carry states, 261 enabled edges, and 69,120 seam comparisons over all 512 three-state relations.
- [Budget checks](evidence/budget.json): 44 finite cases, plus shrinking-cost and replenishment controls.
- [BSD checks](evidence/bsd_seam.json): seven actual/projective point controls and six exact formal rectangle identities.

From this directory with Python 3.10 or newer, choose unused output paths:

```powershell
python -I -B work/check_bridge.py --output evidence/bridge_replay.json
python -I -B work/check_budget.py --output evidence/budget_replay.json
python -I -B work/check_bsd_seam.py --output evidence/bsd_seam_replay.json
```

All three mathematical scripts are standalone standard-library source. The first two reject an existing output path; the BSD script writes the requested path. No saved PASS file, database rank or matching decimal approximation generates these results. Source and evidence hashes are recorded separately; a hash is not mathematical proof.

The next candidate should be tested against the exact mixed interaction and the two boundary conditions. The numeral scout is retained only as a map of possible operations, not as the selector of their meaning. General BSD and the other open Millennium targets remain OPEN. This completed pass leaves the next reasoning step for the ongoing user/assistant iteration; it does not launch unattended background work.
