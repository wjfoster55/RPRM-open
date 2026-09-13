"""Bind and package this starting investigation; hashes certify bytes only."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT.parent / "BSD_GENERAL_01_START_RETURN.zip"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if DESTINATION.exists():
        raise FileExistsError("Archive exists; no existing delivery is overwritten")
    receipt = json.loads((ROOT / "evidence/general_checks_release.json").read_text())
    assert receipt["source_sha256"] == digest(ROOT / "work/check_general.py")
    assert receipt["checks"]["mellin_tail_controls"]["source_sha256"] == digest(ROOT / "work/mellin_tail.py")
    ledger = json.loads((ROOT / "CLAIM_LEDGER.json").read_text())
    for claim in ledger["claims"]:
        assert (ROOT / claim["source"]).is_file(), claim["id"]
    dependencies = [
        ROOT.parent / "bsd-e5-completion/GENERATOR_PROOF.md",
        ROOT.parent / "bsd-e5-completion/COORDINATE_NOTE.md",
        ROOT.parent / "bsd-e5-completion/BSD_SHA_THEOREMS.md",
        ROOT.parent / "bsd-e5-test-01/ANALYTIC_THEOREMS.md",
        ROOT.parent / "bsd-e5-test-01/INTERVAL_DERIVATION.md",
    ]
    files = sorted(p for p in ROOT.rglob("*") if p.is_file()
                   and "__pycache__" not in p.parts and p.name != "DELIVERY_INVENTORY.json")
    inventory = {
        "purpose": "Byte identity, not proof of contents",
        "files": [{"path": p.relative_to(ROOT).as_posix(), "sha256": digest(p),
                   "bytes": p.stat().st_size} for p in files],
        "reused_proof_dependencies_not_bundled": [
            {"path": str(p), "sha256": digest(p)} for p in dependencies
        ],
        "general_BSD": "OPEN",
    }
    manifest = ROOT / "DELIVERY_INVENTORY.json"
    if manifest.exists():
        raise FileExistsError("Manifest exists; preserve prior delivery")
    manifest.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    files.append(manifest)
    with zipfile.ZipFile(DESTINATION, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, ROOT.name + "/" + path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(DESTINATION) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(files)
        for path in files:
            archived = archive.read(ROOT.name + "/" + path.relative_to(ROOT).as_posix())
            assert archived == path.read_bytes()
    sha = digest(DESTINATION)
    DESTINATION.with_suffix(".zip.sha256").write_text(
        sha + "  " + DESTINATION.name + "\n", encoding="ascii")
    print(json.dumps({"status": "BYTES_VERIFIED", "archive": str(DESTINATION),
                      "members": len(files), "sha256": sha,
                      "general_BSD": "OPEN"}, indent=2))


if __name__ == "__main__":
    main()
