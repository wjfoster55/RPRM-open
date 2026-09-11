# Protein-folding kit

**Question:** What finite lattice geometry is available, and what continuation
facts can a contact-map / energy view lose?

**Carrier / model:** The existing public HP square-lattice pack
(`experimental/protein-folding/`), lengths 1..8.

**This kit does:**
- Link and replay a small minimizer example (`HPPH`).
- Expose the geometry/continuation witness already present in that pack.

**This kit does not:**
- Equate NMR model index with time.
- Treat the circuits kit as molecular validation.
- Execute `research-packs/folding-dynamics/` scientific comparisons.

**Evidence grades:** lattice toy is original public RPRM-open material;
dynamics research remains an unexecuted proposal.

**Run:**

```sh
python -I -B experimental/process-mechanics/protein-folding/example.py
python -I -B experimental/process-mechanics/protein-folding/check.py
```

Requires the adjacent public lattice pack in the same checkout.
