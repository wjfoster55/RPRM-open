# Concise BSD rebrief

- **Curve:** E34/Q, y²=x³−1156x. This is not E5 and not the curve with
  coefficient+34 from the published examples.
- **Earlier established inputs:** algebraic rank2, analytic rank2, trivial
  2-primary Sha. The actual written proofs are attributed in `dependencies/`.
- **New result:** Sha(E34/Q)[5^infinity]=0. The complete primitive CM orbit
  gives a trace unit multiple100 mod125; the alternative chord trace gives
  ±25 mod125. Thus v5(T)=2, and the checked CLS criterion applies.
- **New finite data:** |G|=512;256 trace values with fiber size2;
  first five monic coefficients modulo125 are0,30,36,57,120.
  Newton sums and independent exact multiplication reproduce100.
- **Meaning of coarse zero:** the same torsion point and trace reduce
  compatibly modulo25, where the trace is0. This retains a nonzero remainder
  at the next precision; it does not prove real-number equality.
- **Useful YM transfer:** preserve the complete family, selected component,
  multiplicities and actual operator/readout. Ambient enlargement can help
  an inequality but can change an exact signed trace.
- **Still OPEN:** all unexamined prime-primary parts; finiteness and total
  order of Sha; the full complex leading-coefficient identity; any general
  BSD proof. A signed exact rational critical value was not requested or
  reconstructed from its residue.
- **Next general obligation:** derive an exact analytic/arithmetic comparison,
  or a valid shared uniqueness equation, or an independently proved spacing
  theorem with sufficient precision. None is supplied merely by the matching
  numerical values or the YM argument.
- **Reproduction:** `python -I -B work/run_trace.py --output runs/my_fresh_run`.
  Requires only Python3.10+ and a new output directory; do not use `-O`.
- **Evidence grade:** written theorem-dependent proof plus exact finite
  computation, with independent checks and their shared dependencies stated.
  No formal proof assistant or general soundness claim for the tools.
