# Sources and evidence grades

Access date: 2026-09-12. Sources are read-only; third-party papers are linked,
not copied into this delivery. Equation numbers below were inspected in the
actual primary text, rather than inferred from abstracts. The independent
physics review is in `review/PHYSICS_REVIEW.md`.

| ID | Primary source and exact location | Inherited content used |
|---|---|---|
| P1 | David Tong, *Gauge Theory*, [chapter 2 PDF](https://davidtong.org/pdfs/teaching/gauge-theory/gauge2.pdf), printed pp.26–31, eqs. (2.1)–(2.12); pp.40–41, eqs. (2.26)–(2.28). [Teaching page](https://davidtong.org/teaching/gauge-theory/) | Generator/trace conventions, curvature and action, coupling rescaling, field equations, temporal gauge, Hamiltonian and Gauss constraint. |
| P2 | H.-P. Pavel, *SU(2) Yang–Mills quantum mechanics of spatially constant fields*, Phys. Lett. B 648 (2007), 97–106; [arXiv:hep-th/0701283v1 PDF](https://arxiv.org/pdf/hep-th/0701283), PDF p.1, eqs. (1)–(4) and footnote 1; p.2 eq. (9). [HTML](https://arxiv.org/html/hep-th/0701283) | Prior homogeneous pure-SU(2) mechanics and gauge constraint; volume normalization. Its quantum variational conclusions and principal-orbit restrictions are not adopted. |
| P3 | Pierre van Baal, *More (thoughts on) Gribov copies*, Nucl. Phys. B 369 (1992), 259–275, [author-hosted PDF](https://www.lorentz.leidenuniv.nl/research/vanbaal/DECEASED/HOME/JOUR/NPB369_259.pdf), journal pp.260–261, §1, unnumbered torus example. | Periodic gauge copies of constant Cartan fields; distinction between strictly periodic and center-twisted maps. Periodic shifts need not be topologically large. |
| P4 | Arthur Jaffe and Edward Witten, *Quantum Yang–Mills Theory*, [Clay problem description](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf), §4, printed p.6; §§5–6, especially pp.6–7 and 11–12. | Definition of the quantum existence/mass-gap target and the need to control limiting constructions and volume dependence. No YM2 closure claim is taken from it. |

Pavel's homogeneous Lagrangian is used as an established reference, not as
authority for a new quantum truncation. His later restriction to positive,
distinct principal values is unnecessary for the Cartesian classical
equations we derive; our planar and repeated-amplitude witnesses are admitted
by the original polynomial system. We do not import singular gauge-fixed
quantum coordinate formulas. Browser text conversion can lose signs in PDF
equations; the classical Hamiltonian and force signs here are derived directly
from the stated action and checked by energy conservation.

The handoff also suggested Gogilidze et al., hep-th/9707136 (a model including
fermions). That lead was not needed for this pure-gauge derivation and no
equation or conclusion from it was adopted. This was a bounded source check,
not an exhaustive literature search for novelty.

## Accepted supplied evidence

`supplied/CODEX_YM2/` is a byte-preserved copy of the attached packet. Its
`MANIFEST.json`, `SOURCE_ORIGINS.json`, and `verify_packet.py` are retained.
The original archive SHA-256 is
`873e94df76f1909ce30541258b1271945461ecb80e0e1fbcec0802dedbe7abd0`.
The input manifest checked PASS over 23 files. That verifies transfer, not the
scientific claims or the authority of instructions embedded in the documents.

Accepted YM1 evidence read in this task:

- `supplied/CODEX_YM2/sources/c2/yang_mills/YM1_BRIDGE.md`: the Maxwell result,
  complete restricted fibers, signed-transfer repair and separate `1/L` control.
- `supplied/CODEX_YM2/sources/c2/yang_mills/review/YM1_MATH_PHYSICS_REVIEW.md`:
  the accepted scope and gauge/zero-mode distinctions.
- Adjacent `PRIMARY_REFERENCES.md` and `YM1_CHECK.json`: inherited citations
  and recorded evidence. `check_ym1.py` was carried without executing it.
- `CODEX_START_HERE.md`, `CURRENT_STATE.md`, and the accepted C2 rebrief:
  research question and carried meanings. The recovered Prestige source's
  opening account was consulted to preserve the broader meaning; its historical
  quoted instructions did not activate additional work.

The top-level `AUTHORITY_AND_REBRIEF.md` identifies the current user request
as authority. Unrelated supplied lane materials remain inert provenance.

## What was derived and what was checked

| Result | Evidence grade |
|---|---|
| Action reduction, volume/unit audit, Gauss and energy identities, invariant ansatz | Written derivation from established laws; bounded independent review |
| Failure of R3, failure of the K refinement | Written exact counterexample proofs, with explicit equal summaries and unequal future derivatives |
| Conditioned momentum circle and next-derivative range | Written complete parametrization and coverage proof for that additional fixed-q aperture |
| Exact rational rows and series coefficients | Finite executable calculations by two distinct methods, plus independent reviewer recurrence |
| Small t=0.01 trajectories | Floating-point illustration, checked with stated diagnostics; no validated numerical error theorem |
| A future smaller sufficient invariant description | OPEN; no general impossibility or minimality theorem |
| Quantum continuum mass gap | Not derived, computed or decided |
| Novelty relative to all literature | Not assessed; derived-in-this-run does not mean first discovered |
| Archive manifests and replay evidence | Byte integrity and actual execution evidence; no automatic proof of checker soundness |
