# Source ledger for this handoff

## Supplied arithmetic and analytic sources

Byte-preserved copies are under `inputs/`; origin ZIP members and hashes are in
`SOURCE_BINDINGS.json`.

1. `inputs/descent/E5_DESCENT_NOTE.md`: full 2-descent, candidate support, rational
   witnesses, local exclusions, compatible quotient tower, and readback algorithm.
   These are conversation-derived classical calculations to inspect, not an
   authority that replaces an independent proof check.
2. `inputs/analytic/ANALYTIC_NOTE.md`: conductor/sign specialization, Mellin identity,
   exact rational nonvanishing bound, cube representation, and claim limits.
3. `context/CURRENT_STATE.md`, `context/BSD_CHAT_UPDATE.md`, and selected C1/AD1
   documents: accepted framework meanings and closed-task/ownership boundaries.

## Primary mathematical references

The following locators are retained from the supplied notes unless explicitly
marked as checked during packaging. Locate the relevant statement and preserve
its hypotheses; do not report a reference as read if it was not opened.

- J. S. Milne, *Elliptic Curves* (2006), Chapter IV, §3, Remark 3.7; §5.
  Kummer squareclass map, exceptional points, kernel, and descent.
  https://www.jmilne.org/math/Books/ectext6.pdf
- Michael Stoll, *Descent on Elliptic Curves*, §1.1 (2006).
  Selmer/local-Kummer definition and the rational-point/Sha exact sequence.
  https://arxiv.org/abs/math/0611694
- Boris M. Bekker and Yuri G. Zarhin, *The divisibility by 2 of rational points
  on elliptic curves*, §2, Theorem 2.1 and equations (3)–(6), v2.
  https://arxiv.org/html/1702.02255v2
- Noam D. Elkies, *Curves D y^2=x^3-x of odd analytic rank*, §1.1 and §2.
  The supplied note obtains conductor 32D^2 for odd squarefree D and sign -1 at D=5.
  https://arxiv.org/pdf/math/0208056
- Sage elliptic L-series reference, `deriv_at1` and its input warning.
  Central derivative identity; references Cohen §7.5.3. This official HTML page
  was opened during packaging on 2026-09-12. Its formula is consistent with the
  source note; no installed Sage run occurred during packaging.
  https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/lseries_ell.html
- NIST DLMF §6.2 (exponential-integral definition). Opened during packaging.
  https://dlmf.nist.gov/6.2
- Andrew Sutherland, MIT 18.783, Lecture 7, Hasse bound and Frobenius trace.
  https://math.mit.edu/classes/18.783/2023/LectureNotes7.pdf
- Andrew Wiles, Clay BSD problem description: rank order versus full coefficient.
  https://www.claymath.org/wp-content/uploads/2022/05/birchswin.pdf
- RPRM `docs/proof-donut.md`, source blob cited by the supplied analytic note:
  0d5c948de8dc032fbaddff7283eb0504337efe8f. General proof-certificate discipline,
  not an independent proof of the analytic theorem dependencies.
  https://github.com/wjfoster55/RPRM-open/blob/main/docs/proof-donut.md

No external PDF, proprietary text, font, or database dump is redistributed here.
The analytic branch must not use the arithmetic rank as a numerical input.
