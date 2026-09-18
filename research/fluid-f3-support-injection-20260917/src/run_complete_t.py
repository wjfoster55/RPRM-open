"""Run complete-T witness hunt. Nulls already frozen in NULLS_COMPLETE_T.md."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "src"
sys.path.insert(0, str(SRC))

from bound_f3 import evaluate_f3, normalize_unit_occupancy  # noqa: E402
from f2_import import scenes  # noqa: E402
from t_complete import complete_t  # noqa: E402

HOSTILE_WATER = [(30, 34), (31, 34)]
HOSTILE_WALLS = [(29, 36), (30, 36)]


def hostile_scene():
    geo = scenes.make_container(64, 48, 10, extra_walls=HOSTILE_WALLS)
    mass = scenes.empty_mass(64, 48)
    for x, y in HOSTILE_WATER:
        mass[y * 64 + x] = 1.0
    return scenes.spec_of(
        geo, mass, "audit_two_cell_support_injection", "hostile_support",
        "hostile",
    )


def main():
    panel = {s["id"]: s for s in scenes.build_panel()}
    jobs = [
        ("D_ledge_end28", 28, 21, 32),
        ("D_ledge_end30", 30, 21, 32),
        ("D_sill_end25", 25, 35, 32),
    ]
    rows = []
    for sid, tip, row, gap in jobs:
        scene = panel[sid]
        mass_n = normalize_unit_occupancy(scene["mass"], scene["walls"])
        out = complete_t(
            scene["walls"], mass_n, scene["monitor"],
            scene["W"], scene["H"], tip, row, gap,
        )
        slim = {
            "id": sid,
            "meets_R_catwalk": out.get("meets_R_catwalk"),
            "exhausted": out.get("exhausted"),
            "method": out.get("method"),
            "witness_len": out.get("witness_len"),
            "witness_depth": out.get("witness_depth"),
            "states_expanded": out.get("states_expanded"),
            "states_seen": out.get("states_seen"),
            "error": out.get("error"),
            "replay_ok": out.get("replay_ok"),
            "replay_meets": (
                out.get("replay_detail") or {}
            ).get("final_meets") if isinstance(out.get("replay_detail"), dict) else None,
            "path": out.get("path"),
        }
        rows.append(slim)
        print(json.dumps(slim))
    scene = hostile_scene()
    f3 = evaluate_f3(
        scene["walls"], scene["mass"], scene["monitor"],
        scene["W"], scene["H"], scene["thresh"],
        dx=scene["dx"], crest_y=scene["crest_y"],
        audit_token_aware=True,
    )
    h = f3["token_aware"]
    print(json.dumps({
        "id": "hostile",
        "meets_R_catwalk": h["meets_R_catwalk"],
        "verdict": h["verdict"],
        "reason": h["reason"],
    }))
    outp = HERE.parent / "results" / "complete_t_ledges.json"
    outp.write_text(
        json.dumps({"rows": rows, "hostile": {
            "meets_R_catwalk": h["meets_R_catwalk"],
            "verdict": h["verdict"],
        }}, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
