# Process mechanics — companion kits

Companion to [The Right Answer Is Not Enough](../../papers/process-mechanics/README.md), working paper 0.3 (11 September 2026; DOI 10.5281/zenodo.22709682). Table 6 / Appendix C.1 maps claims to their evidence; Appendix C.3 states the public reproduction route.

Additive public family for reusable process-mechanics examples beside the
existing experimental packs. This is **preparation for RPRM-open**, not a
publication authorization.

| Kit | Path | Evidence posture |
|---|---|---|
| Water | [water/](water/) | Reproduced composition + spoof port; local reuse demo |
| Circuits | [circuits/](circuits/) | RC ports stdlib; RLC optional NumPy/SciPy |
| Protein-folding | [protein-folding/](protein-folding/) | Links existing lattice pack; no new biology |
| Cancer-models | [cancer-models/](cancer-models/) | Synthetic nulls + admission; C1 figure lane closed |
| Playground | [playground/](playground/) | Offline HTML/JS teaching sandbox |
| Extras | [extras/](extras/) | Retry identity; units/calibration |

Shared adapters: `rprm/process_mechanics/` (context, candidates, intervals,
measurement). Prefer these over parallel frameworks.

Existing packs stay intact (paths relative to repository root):
- [experimental/protein-folding/](../protein-folding/)
- [research-packs/](../../research-packs/)
- [experimental/lens-lab/](../lens-lab/)

Public historical extracts and claim maps:
- [public_evidence/](public_evidence/) (reaggregation support; teaching demos are separate)
- [PUBLIC_EVIDENCE_MAP.json](PUBLIC_EVIDENCE_MAP.json)

## Quickstart

From a checkout that contains both this family and the public RPRM-open root:

```sh
# Consolidated verification (kits + adapter regressions + public table reaggregation)
python -I -B experimental/process-mechanics/verify_all.py

# Or individual kit checks:
python -I -B experimental/process-mechanics/water/check.py
python -I -B experimental/process-mechanics/circuits/check.py
python -I -B experimental/process-mechanics/protein-folding/check.py
python -I -B experimental/process-mechanics/cancer-models/check.py
python -I -B experimental/process-mechanics/playground/check.py
python -I -B experimental/process-mechanics/extras/retry-identity/check.py
python -I -B experimental/process-mechanics/extras/units-calibration/check.py
python -I -B experimental/process-mechanics/adapters/check_contract_regressions.py
```

Open [playground/index.html](playground/index.html) locally (`file://` offline; no network).
Optional local static server: `python -m http.server` from the playground directory.

See [AGENT_GUIDE.md](AGENT_GUIDE.md) for contracts an agent needs without private chat context.
