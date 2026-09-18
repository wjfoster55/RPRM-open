# F₂⁴ lift — stop

Nulls were frozen in [NULL-F24.md](NULL-F24.md) at `b6f9a58` before
`verify_f24.py` ran.

**Surviving null: `N_rank`.** A 4-set of nonzero linear checks on `F₂⁴`
has injective joint readout iff the four labels span `F₂⁴`. That is the
same statement as HT-28 / THEORY P4, with `k = 4` in place of `k = 3`.
It is not a new theorem.

Derived count, not a claim: `|GL(4,2)|/4! = 840` of the `C(15,4) = 1365`
four-sets are bases. Hostile `{1,2,3,4}` has rank 3; its zero fiber is
`{0,8}`.

`N_any` (all 1365 work) and `N_fano_only` (exactly seven fail) are
**false**. Do not open an HT-24 packet. The next artifact on this branch
is the standalone note
[notes/three-checks-simplex-hamming.md](notes/three-checks-simplex-hamming.md).
