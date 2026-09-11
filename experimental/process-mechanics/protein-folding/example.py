"""Protein-folding process-mechanics kit: lattice link + geometry availability."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_lattice(repo_root: Path):
    model_path = repo_root / "experimental" / "protein-folding" / "model.py"
    if not model_path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("hp_lattice_model", model_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def geometry_availability(model) -> dict:
    """Witness: contact map can preserve energy while losing extension enabledness."""
    straight = ((0, 0), (1, 0), (2, 0))
    bent = ((0, 0), (1, 0), (1, 1))
    return {
        "sequence": "PPP",
        "same_contact_map": model.contact_map(straight) == model.contact_map(bent),
        "same_energy": model.energy("PPP", straight) == model.energy("PPP", bent),
        "straight_extend_W": model.extend(straight, "W"),
        "bent_extend_W": model.extend(bent, "W"),
        "enabledness_differs": model.extend(straight, "W") != model.extend(bent, "W"),
        "note": "Geometry/continuation witness from existing lattice pack; not NMR time",
    }


def run(repo_root: Path | None = None) -> dict:
    root = repo_root or _guess_repo_root()
    model = load_lattice(root)
    if model is None:
        return {
            "kit_id": "process-mechanics/protein-folding",
            "status": "OPEN_MISSING_DEPENDENCY",
            "evidence_grade": "UNEXECUTED",
            "note": "experimental/protein-folding/model.py not found beside this payload",
            "links": {
                "lattice_pack": "experimental/protein-folding/",
                "research_proposal": "research-packs/folding-dynamics/",
            },
        }
    minimizers = model.minimizers("HPPH")
    geo = geometry_availability(model)
    return {
        "kit_id": "process-mechanics/protein-folding",
        "version": "0.1.0",
        "claim_ids": ["UNMAPPED"],
        "evidence_grade": {
            "lattice_toy": "ORIGINAL_ACCEPTED_IN_RPRM_OPEN",
            "geometry_witness": "REPRODUCED_PUBLIC_PORT",
            "molecular_series_pc1": "SEPARATE_CIRCUIT_SCOPE",
            "folding_dynamics_research": "UNEXECUTED_RESEARCH_PROPOSAL",
        },
        "worked_example": {
            "sequence": "HPPH",
            "path_count": len(model.enumerate_paths(4)),
            "minimizer_disposition": minimizers["disposition"],
            "minimizer_count": minimizers["count"],
            "minimum_energy": minimizers["minimum_energy"],
        },
        "geometry_availability": geo,
        "links": {
            "lattice_pack": "experimental/protein-folding/",
            "research_proposal": "research-packs/folding-dynamics/",
            "circuits_kit": "experimental/process-mechanics/circuits/",
        },
        "non_claims": [
            "Not an atomistic folding solution",
            "Circuit study is not molecular validation",
            "NMR model index is not time",
        ],
    }


def _guess_repo_root() -> Path:
    # Prefer an overlay root that already contains experimental/protein-folding.
    for candidate in [HERE.parents[3], HERE.parents[4], Path.cwd()]:
        if (candidate / "experimental" / "protein-folding" / "model.py").is_file():
            return candidate
    return HERE.parents[3]


def main() -> None:
    result = run()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out = HERE / "expected" / "demo_receipt.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text, end="")
    print("sha256", hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()
