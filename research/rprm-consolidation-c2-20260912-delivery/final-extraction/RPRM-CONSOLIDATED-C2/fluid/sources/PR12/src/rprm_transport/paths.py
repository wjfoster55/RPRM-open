"""Paths and executable discovery for local MODFLOW runs."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BIN = ROOT / "bin"


def exe(name: str) -> str:
    """Return absolute path to a project-local executable."""
    candidates = [BIN / name, BIN / f"{name}.exe"]
    for path in candidates:
        if path.exists():
            return str(path)
    raise FileNotFoundError(
        f"Missing executable {name!r} under {BIN}. "
        "Run: python -m flopy.utils.get_modflow .\\bin --repo executables --force"
    )


def mf6() -> str:
    return exe("mf6")


def mf2005() -> str:
    return exe("mf2005")


def mt3dms() -> str:
    return exe("mt3dms")
