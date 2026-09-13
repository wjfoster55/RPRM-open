# YM2 — does energy-transfer closure survive interacting SU(2) dynamics?

**New research assignment to Codex. Paper on hold. One question; complete a mathematical attempt and executable evidence, not just a roadmap.**

Read CURRENT_STATE.md and the accepted YM1 sources first. Preserve YM1 and C1 as completed work; do not run their entire audit again. Follow the actual workspace AGENTS.md. Check only the relevant local task/return records to avoid duplicating a YM2 result or sharing a live worktree. Work in a fresh `research/ym2_interacting_energy_transfer/` (or a new suffix). One writer owns this work.

## Research question

YM1 proved that separate electric and magnetic energies are insufficient for future magnetic energy in a fixed Maxwell mode, and that a signed-transfer term repairs the declared time evolution. Now determine whether the corresponding retained description

    R(x) = (U_E(x), U_B(x), J(x)),  J = dU_B/dt under the declared dynamics,

is sufficient for the magnetic-energy trajectory in one genuinely interacting classical SU(2) setting. Do not import the Maxwell one-mode identity z²=4be or its k-normalization into the new model. Derive units and normalization for J. The question is not whether total conserved energy determines itself.

A strong outcome is either (a) an exact closure theorem for a stated interacting class, or (b) an exact equal-summary/different-future witness together with an identified missing interaction and a checked, limited refinement. Both are useful. A small negative result should expose the mechanism, not end at “nonlinearity is hard.”

## 1. Choose and derive an actual interacting sector

Default first route: a spatially homogeneous, temporal-gauge, pure SU(2) classical sector in a finite periodic box, with noncommuting color/spatial components and the Gauss constraint retained. Homogeneous Yang–Mills mechanics is established prior work, not invented here. Derive the reduction from a stated Yang–Mills action; confirm whether it is an exact invariant ansatz or a declared truncation. A comparably small Hamiltonian-lattice route is acceptable only if this default is unsuitable for a stated mathematical reason. Do not survey many models or silently select the easiest special symmetric orbit after seeing the desired answer.

State the gauge fields, canonical momenta, color convention, coupling, volume normalization, gauge transformations/quotient, constraints, admissible domain, dynamics, and observable. Account for residual/global gauge transformations and any periodic-holonomy issue. Show that the starting states satisfy Gauss and the flow preserves it. Positive magnetic self-interaction/nonzero commutators must actually occur; merely renaming an Abelian oscillator SU(2) is not this task.

Use PRIMARY_SOURCE_LEADS.md for starting references. Read the actual equations needed before borrowing them. Distinguish exact reduction from strong-coupling approximation and quantum mechanics from this classical question. No invented potential, seam-energy charge, mass term, Higgs field, or fitted physics is authorized. Recovered terminology should guide the question without selecting the dynamical answer.

## 2. Test the proposed summary analytically before large computation

Compute the time derivatives/Poisson brackets of U_E, U_B, and J. Test whether they factor through R on the admitted constraint surface. Finite samples alone cannot prove global closure. One admissible exact pair with equal R and a different derivative of the requested future observable can refute it: derive the first unequal derivative and the smoothness argument that yields different sufficiently nearby future values. Do not mistake a numerical near-collision for exact equality.

Prefer a small symbolic or rational/algebraic witness. Include the full source states, constraints, parameters, equal-summary identities, differing derivative, and physical interpretation. Check that it is not just gauge relabeling, a different coupling/volume, or a changed question. Numeric trajectories can illustrate the result with explicit tolerances; they are not its proof.

If closure holds only after additional assumptions, name those assumptions and retain an outside-assumption test. If it fails, identify which commutator/orientation/correlation controls the failure.

## 3. Follow one repair far enough to be substantive

Try one justified refinement suggested by the actual unequal term, for example a specified higher transfer derivative or gauge-invariant interaction contraction. State whether it merely resolves the exhibited pair or genuinely supports all admitted future updates. Differentiate the added quantity and inspect the next obligation instead of announcing closure from one repaired example. Stop after this bounded extension if a new independent quantity appears; supply a precise unresolved condition or another exact witness. Do not grow an unlimited moment hierarchy or call storage of the full source a compressed discovery.

A constructive description with a proven update and clear source fibers is a positive result, even if it is not smaller than the conventional state. Report representation size, supplied assumptions, and any reopening cost honestly. A known conventional reduction may already solve the proposed subproblem; show that and identify exactly what, if anything, this derivation adds.

## 4. Controls and relation to the mass-gap ambition

- Independently derive at least one identity or evaluate witnesses by a separate direct method, not two functions calling the same code.
- Verify Gauss and energy conservation at the analytical level; check them in any numeric illustration with stated errors.
- Transport a genuine gauge relabeling consistently; distinguish coordinate/gauge choices from physically different states.
- Include a commuting/vanishing-interaction or other justified simpler control. It need not recreate the fixed nonzero-frequency Maxwell mode; explain differences in sector and parameters.
- Separate physical source ambiguity from the retained answer and from unavailable evidence.
- Keep the accepted 1/L finite-box lesson. If any spectral or “positive minimum” statement is introduced, identify the quantum theory and the volume/cutoff limit actually involved. Do not infer a quantum gap from bounded classical trajectories, a finite matrix spectrum, or a homogeneous restriction.

End with a short PROBLEM_BRIDGE.md: what the new derivation says about interacting observable preservation; whether it supplies any nontrivial spectral bound (normally not part of this task); and the ONE precise bridge still missing to the broader quantum question. Do not sell a classical closure failure as proving or disproving a mass gap. Equally, do not refuse the concrete derivation merely because the broader problem is open.

## 5. Research and delivery discipline

Preserve source meanings; separate inherited theory, newly derived-in-this-run statements, finite checks, conjectures, and literature novelty. No requirement to force a new theorem, favorable result, or publication. Use the installed local environment; no package installation, paid compute, remote write, commit/push/merge, paper changes, or worker in another project. Read-only primary research is allowed. If a library is missing, use exact elementary calculations or the available environment and report the limit rather than stop at a plan.

Deliver a concise RETURN_TO_WILLIAM.md, MODEL_AND_DERIVATION.md, the closure theorem OR exact witness plus bounded repair result, PROBLEM_BRIDGE.md, source citations with exact locations, runnable checker(s), full result rows, and a source/delivery manifest. Add or supply one local rebrief pointer. Freeze the claimed implementation/assumptions before final checks; exploratory corrections stay labelled as such. Test the actual exported ZIP from a fresh extraction; put final replay evidence outside its already-hashed payload. Return the ZIP and SHA-256. Close YM2 at its stated result, not by reopening C1/YM1 or launching a next campaign.
