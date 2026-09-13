# Independent bounded review

2026-09-12. Read-only reviewer `/root/joint_scaling_audit`; this record captures
the returned review, formatted by the owner. Reviewer inspected
`JOINT_AND_SCALING.md` and `check_joint.py` and ran the checker.

**PASS within the declared homogeneous rank≥2 domain.**

The reviewer independently derived the closed S,T,U equations, readouts,
Gauss equivalence `GΩG=0`, complete Gram representative fibers, and the
one/two physical-branch distinction at ranks two/three. The proof that any
periodic gauge relating the admitted homogeneous representatives is constant
was checked in all three rank cases, including cross-index `E_j,D_iE_j`.
Joint rank is invariant; rank changes of A alone do not invalidate the proof.

Improper reflection preserves the magnetic-energy receiver while potentially
changing `ΣE_i·B_i`. Positive amplitude scaling, energy normalization and the
normalized horizon `λ_max T` were checked. The local symmetric S,B Riccati
chart is valid only when A is invertible. Storage, performance, spatial gluing,
quantum and novelty limits are appropriately separated. The AD/SAT connection
is explicitly an analogy about proved families and retained interfaces.

The two recurrences use distinct source and joint right-hand sides, with
shared exact matrix utilities disclosed. Coefficients through degree four are
fully determined and do not depend on uncomputed terms. The reviewer ran

`python -I -B research/ym2_joint_scaling/check_joint.py`

and obtained PASS with `RESULTS.json` matching: 2,312 assertions across 34
full state rows. This is independent replay of finite calculations, not a
machine-formal proof of all general statements or arbitrary Gram realization.

Two wording corrections were incorporated after review:

- Spatially constant, gauge-covariant vectors were distinguished from
  *covariantly constant* vectors, which would mean something different.
- Complete fibers were identified as the source fibers of the **Gram map**,
  not a claimed classification of every source sharing the same entire
  magnetic-energy future.

No code or computed result needed correction. The original YM2 files and ZIP
were not edited.
