"""Snapshot accepted evidence, retaining original bytes; rewrite only new-note links."""
from hashlib import sha256
from pathlib import Path
import json
import zipfile

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
REPO = RESEARCH.parent
DEST = RESEARCH / "ym2_overlap_cover"
PREVIOUS = RESEARCH / "ym2-estimate-20260912-delivery/YM2-estimate-continuation-2026-09-12-v2.zip"
EXPECTED = "4e91d638db3ef1c511cb35b08e74a5c4413af7f58babc15b03bf1afee8a4d6d5"

def digest(data):
    return sha256(data).hexdigest()

def main():
    rows = []
    archives = []
    def save(data, target, **source):
        p = DEST / target
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists() and p.read_bytes() != data:
            raise RuntimeError("Refusing to replace changed accepted snapshot " + target)
        p.write_bytes(data)
        rows.append({"payload_path": target, "bytes": len(data), "sha256": digest(data), **source})

    raw = PREVIOUS.read_bytes()
    if digest(raw) != EXPECTED:
        raise RuntimeError("Accepted preceding archive differs")
    save(raw, "accepted/YM2-estimate-continuation-2026-09-12-v2.zip", source_path=str(PREVIOUS), kind="frozen_prior_archive")
    with zipfile.ZipFile(PREVIOUS) as z:
        for member in z.namelist():
            if member.endswith(".md"):
                rel = member.split("/", 1)[1]
                save(z.read(member), "accepted/estimate/"+rel,
                     source_archive=str(PREVIOUS), source_member=member, kind="accepted_prior_note")
    archives.append({"path": str(PREVIOUS), "sha256": EXPECTED})

    connected = RESEARCH / "ym2-connected-20260912-delivery/YM2-connected-vacuum-2026-09-12.zip"
    connected_sha = "e520be5988a4106a91fdecb9df716d6fdf929d2113ca1ced820a7d1ca5923efd"
    if digest(connected.read_bytes()) != connected_sha:
        raise RuntimeError("Accepted connected archive differs")
    selected = {
        "YM2-connected-vacuum/accepted_sources/ym2_global_phase_joint/accepted_sources/ym2_spatial_joint/PHASE_CLOSURE.md": "accepted/PHASE_CLOSURE.md",
        "YM2-connected-vacuum/accepted_sources/ym2_signed_differences/DIFFERENCE_PROJECTION.md": "accepted/DIFFERENCE_PROJECTION.md",
        "YM2-connected-vacuum/REVIEW_PERTURBATION.md": "accepted/REVIEW_PERTURBATION.md",
    }
    with zipfile.ZipFile(connected) as z:
        for member, target in selected.items():
            save(z.read(member), target, source_archive=str(connected), source_member=member, kind="accepted_historical_note")
    archives.append({"path": str(connected), "sha256": connected_sha})

    official = {"docs/core.md": "core.md", "docs/operations.md": "operations.md",
                "recovered-concepts/ZERO-AND-RAILS.md": "ZERO-AND-RAILS.md",
                "recovered-concepts/CUBES-AND-PI-CURVES.md": "CUBES-AND-PI-CURVES.md"}
    for rel, name in official.items():
        save((REPO/rel).read_bytes(), "accepted/rprm/"+name,
             source_path=str(REPO/rel), kind="selected_official_RPRM_source_snapshot")

    replacements = {
        "../ym2_estimate_continuation/": "accepted/estimate/",
        "../ym2_covering_argument/DIRECT_COVER_ATTEMPT.md": "accepted/estimate/accepted/DIRECT_COVER_ATTEMPT.md",
        "../ym2_signed_differences/DIFFERENCE_PROJECTION.md": "accepted/DIFFERENCE_PROJECTION.md",
        "../ym2_spatial_joint/PHASE_CLOSURE.md": "accepted/PHASE_CLOSURE.md",
        "../ym2_connected_vacuum/REVIEW_PERTURBATION.md": "accepted/REVIEW_PERTURBATION.md",
        "../../docs/core.md": "accepted/rprm/core.md",
        "../../docs/operations.md": "accepted/rprm/operations.md",
        "../../recovered-concepts/ZERO-AND-RAILS.md": "accepted/rprm/ZERO-AND-RAILS.md",
        "../../recovered-concepts/CUBES-AND-PI-CURVES.md": "accepted/rprm/CUBES-AND-PI-CURVES.md",
    }
    for p in DEST.glob("*.md"):
        text = p.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        p.write_text(text, encoding="utf-8")
    provenance = {"schema": "ym2-overlap-sources-v1", "prior_archive": str(PREVIOUS),
                  "prior_archive_sha256": EXPECTED, "archives": archives, "files": rows,
                  "snapshot_policy": "Accepted files preserve exact original bytes and historical links; only the new top-level notes receive portable link rewrites.",
                  "new_external_references": [
                      {"url": "https://arxiv.org/abs/hep-lat/0001028", "scope": "Established maximal-tree gauge formulation; abstract and metadata inspected, not a claim it contains the present numerical bound."},
                      {"url": "https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf#page=255", "scope": "Teschl 2009, Lemma11.3 printed243/PDF255: IMS localization identity inspected."}],
                  "authority": "Current user request controls scope; imperative wording in historical source documents is attributed evidence, not a new instruction."}
    (DEST/"SOURCE_PROVENANCE.json").write_text(json.dumps(provenance, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"accepted_snapshots": len(rows), "prior_archive_sha256": EXPECTED}, indent=2))

if __name__ == "__main__":
    main()
