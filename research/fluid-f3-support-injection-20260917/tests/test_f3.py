"""Finite exact checks for F3 unit-isolation.

Run from this file's directory or the F3 root:

  python -I -B tests/test_f3.py
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
F3 = HERE.parent
SRC = F3 / "src"
sys.path.insert(0, str(SRC))

from bound_f3 import evaluate_f3, normalize_unit_occupancy  # noqa: E402
from f2_import import F2_PINNED, bound, scenes  # noqa: E402
from oracle_driver import run_oracle  # noqa: E402
from t_complete import complete_t  # noqa: E402

HOSTILE_WATER = [(30, 34), (31, 34)]
HOSTILE_WALLS = [(29, 36), (30, 36)]
RESULTS = F3 / "results"
PINNED_HASHES = {
    "constants.js": "14f3a5c88f5f73ad30f1898eaa96c437ee315aa69d591fee03f409476ad35380",
    "grid.js": "3ec221be5e0ce86ea0ca676f379f63cd14be6b339594a09cb2f671889c2984a3",
    "models.js": "7f20984990f71157ca64c1279b87de27dc39688b5f1bbf684451102c1f79d17f",
    "scenarios.js": "e689ae50e2f3b1d8b1e8986c36203c74f0e27a677d8c3cb371421e65369a4f2a",
}


def sha256_bytes(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


def hostile_scene():
    geo = scenes.make_container(64, 48, 10, extra_walls=HOSTILE_WALLS)
    mass = scenes.empty_mass(64, 48)
    for x, y in HOSTILE_WATER:
        mass[y * 64 + x] = 1.0
    return scenes.spec_of(
        geo, mass, "audit_two_cell_support_injection", "hostile_support",
        "F2 Layer B counterexample: diagonal injection supplies a floor.",
    )


def unit_scene(x, y, extra_walls=None, scene_id="unit"):
    geo = scenes.make_container(64, 48, 10, extra_walls=extra_walls)
    mass = scenes.empty_mass(64, 48)
    mass[y * 64 + x] = 1.0
    return scenes.spec_of(
        geo, mass, scene_id, "unit",
        f"single unit cell at ({x},{y})",
    )


def floor_sitting_column(x0, width, V, extra_walls=None, scene_id="floor_col"):
    """Hole-free rectangle sitting on y=floor, filled from the floor up."""
    geo = scenes.make_container(64, 48, 10, extra_walls=extra_walls)
    mass = scenes.empty_mass(64, 48)
    cells = []
    for y in range(geo["floor"], 0, -1):
        for x in range(x0, x0 + width):
            cells.append((y, x))
    scenes.fill_cells(mass, geo["walls"], 64, cells, V)
    return scenes.spec_of(
        geo, mass, scene_id, "packed_yes_probe",
        f"floor-sitting w={width} x0={x0} V={V}",
    )


def hanging_column(x0, width, V, extra_walls=None, scene_id="hang_col"):
    """Hole-free rectangle filled from y=1 down (panel packed-column order)."""
    geo = scenes.make_container(64, 48, 10, extra_walls=extra_walls)
    mass = scenes.empty_mass(64, 48)
    scenes.fill_cells(
        mass, geo["walls"], 64, scenes.column_cells(geo, x0, width), V,
    )
    return scenes.spec_of(
        geo, mass, scene_id, "packed_yes_probe",
        f"hanging w={width} x0={x0} V={V}",
    )


def two_cell_scene(cells, extra_walls=None, scene_id="two"):
    geo = scenes.make_container(64, 48, 10, extra_walls=extra_walls)
    mass = scenes.empty_mass(64, 48)
    for x, y in cells:
        mass[y * 64 + x] = 1.0
    return scenes.spec_of(
        geo, mass, scene_id, "two_cell",
        f"two cells {cells}",
    )


class TestPinnedIdentity(unittest.TestCase):
    def test_pinned_js_hashes(self):
        for name, expected in PINNED_HASHES.items():
            path = F2_PINNED / name
            self.assertEqual(sha256_bytes(path.read_bytes()), expected, name)


class TestHostileCasePreserved(unittest.TestCase):
    def test_frozen_layer_b_still_false_no(self):
        scene = hostile_scene()
        layers = bound.evaluate_layers(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
        )
        old, reason = bound.official_static_verdict(layers)
        self.assertEqual(old, "CERTIFIED_NO")
        self.assertIn("sill_need", reason)
        oracle = run_oracle(scene, "full", snapshot_steps=[0, 1, 2, 3])
        self.assertEqual(oracle["Qdyn"], 1)
        self.assertEqual(oracle["firstBreach"], 3)

    def test_f3_does_not_certify_no(self):
        scene = hostile_scene()
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
            audit_soups=True,
        )
        self.assertEqual(f3["n_water"], 2)
        self.assertEqual(f3["static"], "UNRESOLVED")
        self.assertEqual(
            f3["isolation"]["reason"], "n_ge_2_no_cheap_static_no",
        )
        self.assertTrue(f3["full_soup"]["meets_R_catwalk"])
        self.assertTrue(f3["wall_soup"]["meets_R_catwalk"])
        oracle = run_oracle(scene, "cut_exit")
        self.assertEqual(oracle["Qdyn"], 1)
        self.assertEqual(oracle["firstBreach"], 3)


class TestUnitIsolation(unittest.TestCase):
    def test_gap_adjacent_y1_static_no(self):
        # Frozen panel E_adjcell_y1: unique cell not on R_catwalk, Q=0.
        panel = {s["id"]: s for s in scenes.build_panel()}
        scene = panel["E_adjcell_y1"]
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
        )
        self.assertEqual(f3["n_water"], 1)
        self.assertEqual(f3["static"], "CERTIFIED_NO")
        self.assertEqual(f3["isolation"]["reason"], "unique_cell_not_on_R_catwalk")
        oracle = run_oracle(scene, "yes_exit")
        self.assertEqual(oracle["Qdyn"], 0)

    def test_gap_adjacent_y35_static_no(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        scene = panel["E_adjcell_y35"]
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
        )
        self.assertEqual(f3["static"], "CERTIFIED_NO")
        oracle = run_oracle(scene, "yes_exit")
        self.assertEqual(oracle["Qdyn"], 0)

    def test_gap_y20_not_isolated_no(self):
        # Unique cell ON R_catwalk; splash phase can YES. Must stay UNRESOLVED.
        panel = {s["id"]: s for s in scenes.build_panel()}
        scene = panel["C_gap_y20"]
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
        )
        self.assertEqual(f3["n_water"], 1)
        self.assertEqual(f3["static"], "UNRESOLVED")
        self.assertEqual(f3["isolation"]["reason"], "unique_cell_on_R_catwalk")
        oracle = run_oracle(scene, "cut_exit")
        self.assertEqual(oracle["Qdyn"], 1)

    def test_isolated_shelf_one_cell(self):
        walls = [(x, 12) for x in range(1, 16)]
        scene = unit_scene(5, 11, extra_walls=walls, scene_id="unit_shelf")
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
        )
        self.assertEqual(f3["static"], "CERTIFIED_NO")
        oracle = run_oracle(scene, "yes_exit")
        self.assertEqual(oracle["Qdyn"], 0)

    def test_right_compartment_yes(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        scene = panel["C_right_one"]
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
        )
        self.assertEqual(f3["static"], "CERTIFIED_YES")

    def test_fractional_monitor_normalizes_to_yes(self):
        geo = scenes.make_container(64, 48, 10)
        mass = scenes.empty_mass(64, 48)
        mass[40 * 64 + (geo["dx"] + 3)] = 0.25
        scene = scenes.spec_of(
            geo, mass, "fractional_right_one", "admission",
            "raw mass 0.25 in monitor; oracle unit-normalizes to 1",
        )
        f2_layers = bound.evaluate_layers(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
        )
        # Frozen static path can disagree with the oracle on raw fractional mass.
        self.assertNotEqual(f2_layers["A"]["verdict"], "CERTIFIED_YES")
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
        )
        self.assertEqual(f3["static"], "CERTIFIED_YES")
        oracle = run_oracle(scene, "yes_exit")
        self.assertEqual(oracle["Qdyn"], 1)
        self.assertEqual(oracle["firstBreach"], 0)


class TestFormerBOnlyNotRestored(unittest.TestCase):
    def test_v9_shelf_is_one_high_no_not_layer_b(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        scene = panel["D_shelf_isolated"]
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
        )
        self.assertGreaterEqual(f3["n_water"], 2)
        self.assertEqual(f3["static"], "CERTIFIED_NO")
        self.assertTrue(f3["static_reason"].startswith("1HIGH:"))
        self.assertEqual(f3["B_refuted"]["verdict"], "CERTIFIED_NO")
        self.assertFalse(f3["static_reason"].startswith("B:"))
        oracle = run_oracle(scene, "yes_exit")
        self.assertEqual(oracle["Qdyn"], 0)


class TestPanelStaticSoundness(unittest.TestCase):
    def test_no_false_static_on_frozen_panel(self):
        rows_path = (
            F3.parent
            / "fluid-f2-review-20260912"
            / "input"
            / "fluid_dynamic_frontier_02"
            / "results"
            / "rows.jsonl"
        )
        stored = {}
        for line in rows_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            stored[row["id"]] = int(row["Q_ref"])
        panel = scenes.build_panel()
        self.assertEqual(len(panel), 53)
        false_no = []
        false_yes = []
        iso_no_ids = []
        unresolved_former_b = []
        for scene in panel:
            f3 = evaluate_f3(
                scene["walls"], scene["mass"], scene["monitor"],
                scene["W"], scene["H"], scene["thresh"],
                dx=scene["dx"], crest_y=scene["crest_y"],
            )
            q = stored[scene["id"]]
            if f3["static"] == "CERTIFIED_NO" and q == 1:
                false_no.append(scene["id"])
            if f3["static"] == "CERTIFIED_YES" and q == 0:
                false_yes.append(scene["id"])
            if f3["static_reason"].startswith("ISO:"):
                iso_no_ids.append(scene["id"])
            if (
                f3["B_refuted"]["verdict"] == "CERTIFIED_NO"
                and f3["A"]["verdict"] == "UNRESOLVED"
                and f3["static"] == "UNRESOLVED"
            ):
                unresolved_former_b.append(scene["id"])
        self.assertEqual(false_no, [])
        self.assertEqual(false_yes, [])
        # Isolation should recover the two genuine V=1 B-only panel NOs.
        self.assertIn("E_adjcell_y1", iso_no_ids)
        self.assertIn("E_adjcell_y35", iso_no_ids)
        # Stack/blob former B-only NOs stay unrestored. Isolated shelf is
        # a 1-high catwalk-miss NO, not sill_need.
        for sid in ("E_stack10_adj", "E_blob9_far"):
            self.assertIn(sid, unresolved_former_b)
        self.assertNotIn("D_shelf_isolated", unresolved_former_b)


class TestNoCheapV2StaticNO(unittest.TestCase):
    """Cell-graph soups cannot give a useful sound V>=2 static NO.

    Full soup (water floors allowed) meets R_catwalk on every n>=2
    A-unresolved frozen-panel row, so it never certifies NO.
    Wall-only soup leaves the hostile pair uncertified-NO but false-NOs
    packed-column YES scenes. Official routing therefore keeps n>=2
    UNRESOLVED after Layer A.
    """

    def test_full_soup_never_nos_panel_or_probes(self):
        panel = scenes.build_panel()
        for scene in panel:
            f3 = evaluate_f3(
                scene["walls"], scene["mass"], scene["monitor"],
                scene["W"], scene["H"], scene["thresh"],
                dx=scene["dx"], crest_y=scene["crest_y"],
                audit_soups=True,
            )
            if f3["n_water"] >= 2 and f3["A"]["verdict"] == "UNRESOLVED":
                self.assertIsNotNone(f3["full_soup"], scene["id"])
                self.assertTrue(
                    f3["full_soup"]["meets_R_catwalk"],
                    scene["id"],
                )
                if f3["one_high"]["verdict"] != "CERTIFIED_NO":
                    self.assertEqual(f3["static"], "UNRESOLVED", scene["id"])
        for item in (
            ("hostile", HOSTILE_WATER, HOSTILE_WALLS),
            ("midair", [(30, 34), (31, 34)], None),
            ("shelf2", [(5, 11), (6, 11)], [(x, 12) for x in range(1, 16)]),
        ):
            scene = two_cell_scene(item[1], extra_walls=item[2], scene_id=item[0])
            f3 = evaluate_f3(
                scene["walls"], scene["mass"], scene["monitor"],
                scene["W"], scene["H"], scene["thresh"],
                dx=scene["dx"], crest_y=scene["crest_y"],
                audit_soups=True,
            )
            self.assertTrue(f3["full_soup"]["meets_R_catwalk"], item[0])
            if f3["one_high"]["verdict"] != "CERTIFIED_NO":
                self.assertEqual(f3["static"], "UNRESOLVED", item[0])

    def test_wall_only_false_nos_packed_yes(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        for sid in ("A_w4_x26_V180", "C_adj4_V60"):
            scene = panel[sid]
            f3 = evaluate_f3(
                scene["walls"], scene["mass"], scene["monitor"],
                scene["W"], scene["H"], scene["thresh"],
                dx=scene["dx"], crest_y=scene["crest_y"],
                audit_soups=True,
            )
            self.assertEqual(f3["A"]["verdict"], "UNRESOLVED", sid)
            self.assertFalse(f3["wall_soup"]["meets_R_catwalk"], sid)
            self.assertTrue(f3["full_soup"]["meets_R_catwalk"], sid)
            self.assertEqual(f3["static"], "UNRESOLVED", sid)
            oracle = run_oracle(scene, "yes_exit")
            self.assertEqual(oracle["Qdyn"], 1, sid)

    def test_official_never_uses_refuted_b(self):
        scene = hostile_scene()
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
        )
        self.assertEqual(f3["B_refuted"]["verdict"], "CERTIFIED_NO")
        self.assertFalse(f3["static_reason"].startswith("B:"))


class TestTwoCellTravelFinite(unittest.TestCase):
    """Remaining F2 question: can two cells carry toward a gap by injection?

    Grade: finite test on a declared family. Not a general V=2 bound.
    """

    def test_declared_two_cell_family(self):
        family = [
            {
                "id": "hostile_original",
                "cells": HOSTILE_WATER,
                "extra_walls": HOSTILE_WALLS,
                "expect_Q": 1,
            },
            {
                "id": "midair_near_divider",
                "cells": [(30, 34), (31, 34)],
                "extra_walls": None,
                "expect_Q": None,
            },
            {
                "id": "shelf_two_far",
                "cells": [(5, 11), (6, 11)],
                "extra_walls": [(x, 12) for x in range(1, 16)],
                "expect_Q": 0,
            },
            {
                "id": "ledge_end30_two_at_tip",
                "cells": [(29, 35), (30, 35)],
                "extra_walls": [(x, 36) for x in range(20, 31)],
                "expect_Q": None,
            },
            {
                "id": "ledge_end28_two_at_tip",
                "cells": [(27, 35), (28, 35)],
                "extra_walls": [(x, 36) for x in range(20, 29)],
                "expect_Q": None,
            },
        ]
        rows = []
        for item in family:
            scene = two_cell_scene(
                item["cells"], extra_walls=item["extra_walls"], scene_id=item["id"],
            )
            f3 = evaluate_f3(
                scene["walls"], scene["mass"], scene["monitor"],
                scene["W"], scene["H"], scene["thresh"],
                dx=scene["dx"], crest_y=scene["crest_y"],
            )
            oracle = run_oracle(scene, "full", snapshot_steps=[0, 1, 2, 3, 4, 5])
            row = {
                "id": item["id"],
                "cells": item["cells"],
                "n_water": f3["n_water"],
                "static": f3["static"],
                "static_reason": f3["static_reason"],
                "Qdyn": int(oracle["Qdyn"]),
                "firstBreach": oracle["firstBreach"],
                "maxMonitored": oracle["maxMonitored"],
            }
            rows.append(row)
            if row["Qdyn"] == 1:
                self.assertNotEqual(f3["static"], "CERTIFIED_NO", item["id"])
            elif f3["one_high"]["verdict"] == "CERTIFIED_NO":
                self.assertEqual(f3["static"], "CERTIFIED_NO", item["id"])
            else:
                self.assertEqual(f3["static"], "UNRESOLVED", item["id"])
            if item["expect_Q"] is not None:
                self.assertEqual(row["Qdyn"], item["expect_Q"], item["id"])
        RESULTS.mkdir(parents=True, exist_ok=True)
        out = RESULTS / "two_cell_travel.json"
        out.write_text(json.dumps({"family": rows}, indent=2) + "\n", encoding="utf-8")


class TestTokenAwareOccupancy(unittest.TestCase):
    """Class T: n-token occupancy over-approx. Frozen nulls in NULLS.md.

    Official static routing is unchanged: T is never a Layer-B revival
    and never a free static NO.
    """

    def _t(self, scene):
        return evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
            audit_token_aware=True,
        )

    def test_hostile_meets_not_t_no(self):
        scene = hostile_scene()
        f3 = self._t(scene)
        self.assertEqual(f3["static"], "UNRESOLVED")
        t = f3["token_aware"]
        self.assertTrue(t["meets_R_catwalk"], t)
        self.assertNotEqual(t["verdict"], "CERTIFIED_NO")

    def test_end31_yes_meets(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        f3 = self._t(panel["D_ledge_end31"])
        self.assertEqual(f3["static"], "UNRESOLVED")
        t = f3["token_aware"]
        self.assertTrue(t["meets_R_catwalk"], t)
        self.assertNotEqual(t["verdict"], "CERTIFIED_NO")

    def test_horizon_pay_ledges_no_cheap_t_no(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        rows = []
        for sid in ("D_ledge_end28", "D_ledge_end30", "D_sill_end25"):
            f3 = self._t(panel[sid])
            t = f3["token_aware"]
            rows.append({"id": sid, "token_aware": t, "static": f3["static"]})
            self.assertEqual(f3["static"], "CERTIFIED_NO", sid)
            self.assertTrue(f3["static_reason"].startswith("1HIGH:"), sid)
            self.assertNotEqual(t["verdict"], "CERTIFIED_NO", sid)
            self.assertTrue(
                t["meets_R_catwalk"] or t["budget_hit"] or t["skipped"],
                sid,
            )
        RESULTS.mkdir(parents=True, exist_ok=True)
        (RESULTS / "token_aware_ledges.json").write_text(
            json.dumps({"rows": rows}, indent=2) + "\n", encoding="utf-8",
        )

    def test_packed_yes_not_t_no(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        for sid in ("A_w4_x26_V180", "C_adj4_V60"):
            f3 = self._t(panel[sid])
            t = f3["token_aware"]
            self.assertEqual(f3["static"], "UNRESOLVED", sid)
            self.assertNotEqual(t["verdict"], "CERTIFIED_NO", sid)

    def test_shelf_two_far_t_no(self):
        scene = two_cell_scene(
            [(5, 11), (6, 11)],
            extra_walls=[(x, 12) for x in range(1, 16)],
            scene_id="shelf_two_far",
        )
        f3 = self._t(scene)
        t = f3["token_aware"]
        self.assertTrue(t["exhausted"], t)
        self.assertFalse(t["meets_R_catwalk"], t)
        self.assertEqual(t["verdict"], "CERTIFIED_NO")
        self.assertEqual(f3["static"], "CERTIFIED_NO")
        self.assertTrue(f3["static_reason"].startswith("1HIGH:"))
        oracle = run_oracle(scene, "yes_exit")
        self.assertEqual(oracle["Qdyn"], 0)

    def test_midair_pair_t_no(self):
        scene = two_cell_scene(
            [(30, 34), (31, 34)], extra_walls=None, scene_id="midair",
        )
        f3 = self._t(scene)
        t = f3["token_aware"]
        self.assertTrue(t["exhausted"], t)
        self.assertFalse(t["meets_R_catwalk"], t)
        self.assertEqual(t["verdict"], "CERTIFIED_NO")
        self.assertEqual(f3["static"], "UNRESOLVED")


class TestCycleExact(unittest.TestCase):
    """Class E: token-state cycle exact. Cheaper than H iff stepsRun < 300."""

    def test_hostile_yes_not_cycle_no(self):
        scene = hostile_scene()
        out = run_oracle(scene, "cycle_exit")
        self.assertEqual(out["Qdyn"], 1)
        self.assertEqual(out["firstBreach"], 3)
        self.assertNotEqual(out["stop"], "occ_cycle")

    def test_horizon_pay_ledges_cycle_cheaper_than_h(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        rows = []
        for sid in ("D_ledge_end28", "D_ledge_end30", "D_sill_end25"):
            out = run_oracle(panel[sid], "cycle_exit")
            rows.append({
                "id": sid,
                "Qdyn": int(out["Qdyn"]),
                "firstBreach": out["firstBreach"],
                "stepsRun": out["stepsRun"],
                "stop": out["stop"],
                "cutReason": out["cutReason"],
                "sumActive": out["sumActive"],
                "tokenStatesSeen": out.get("tokenStatesSeen"),
                "wall_ms": out["wall_ms"],
            })
            self.assertEqual(out["Qdyn"], 0, sid)
            self.assertLess(out["stepsRun"], 300, sid)
            self.assertEqual(out["stop"], "occ_cycle", sid)
        RESULTS.mkdir(parents=True, exist_ok=True)
        (RESULTS / "cycle_exact_ledges.json").write_text(
            json.dumps({"rows": rows}, indent=2) + "\n", encoding="utf-8",
        )

    def test_yes_rows_not_cycle_no(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        for sid in ("D_ledge_end31", "A_w4_x26_V180"):
            out = run_oracle(panel[sid], "cycle_exit")
            self.assertEqual(out["Qdyn"], 1, sid)
            self.assertNotEqual(out["stop"], "occ_cycle", sid)
            self.assertGreaterEqual(out["firstBreach"], 0, sid)


class TestCompleteTLedges(unittest.TestCase):
    """Complete T on horizon-pay rows: MEETS (frozen NULLS_COMPLETE_T.md)."""

    def test_complete_t_meets_horizon_ledges(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        jobs = (
            ("D_ledge_end28", 28, 21, 32),
            ("D_ledge_end30", 30, 21, 32),
            ("D_sill_end25", 25, 35, 32),
        )
        rows = []
        for sid, tip, row, gap in jobs:
            scene = panel[sid]
            mass_n = normalize_unit_occupancy(scene["mass"], scene["walls"])
            out = complete_t(
                scene["walls"], mass_n, scene["monitor"],
                scene["W"], scene["H"], tip, row, gap,
            )
            rows.append({
                "id": sid,
                "meets_R_catwalk": out["meets_R_catwalk"],
                "method": out.get("method"),
                "witness_len": out.get("witness_len"),
                "replay_ok": out.get("replay_ok"),
                "path": out.get("path"),
                "static": evaluate_f3(
                    scene["walls"], scene["mass"], scene["monitor"],
                    scene["W"], scene["H"], scene["thresh"],
                    dx=scene["dx"], crest_y=scene["crest_y"],
                )["static"],
            })
            self.assertTrue(out["meets_R_catwalk"], sid)
            self.assertTrue(out.get("replay_ok"), sid)
            self.assertEqual(rows[-1]["static"], "CERTIFIED_NO", sid)
        RESULTS.mkdir(parents=True, exist_ok=True)
        (RESULTS / "complete_t_ledges.json").write_text(
            json.dumps({"rows": rows}, indent=2) + "\n", encoding="utf-8",
        )

    def test_complete_t_hostile_still_meets(self):
        scene = hostile_scene()
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
            audit_token_aware=True,
        )
        self.assertTrue(f3["token_aware"]["meets_R_catwalk"])
        self.assertNotEqual(f3["token_aware"]["verdict"], "CERTIFIED_NO")
        self.assertEqual(f3["static"], "UNRESOLVED")
        self.assertEqual(f3["one_high"]["reason"], "not_all_wall_supported")


class TestCarryLemma(unittest.TestCase):
    """Restricted 1-high carry; cheap scan-order-ignoring class stays empty."""

    def test_horizon_ledges_one_high_no(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        rows = []
        for sid in ("D_ledge_end28", "D_ledge_end30", "D_sill_end25"):
            scene = panel[sid]
            f3 = evaluate_f3(
                scene["walls"], scene["mass"], scene["monitor"],
                scene["W"], scene["H"], scene["thresh"],
                dx=scene["dx"], crest_y=scene["crest_y"],
            )
            rows.append({
                "id": sid,
                "static": f3["static"],
                "static_reason": f3["static_reason"],
                "one_high": f3["one_high"],
            })
            self.assertTrue(f3["one_high"]["all_wall_supported"], sid)
            self.assertFalse(f3["one_high"]["cat_meets_R_catwalk"], sid)
            self.assertEqual(f3["static"], "CERTIFIED_NO", sid)
            self.assertTrue(f3["static_reason"].startswith("1HIGH:"), sid)
            oracle = run_oracle(scene, "yes_exit")
            self.assertEqual(oracle["Qdyn"], 0, sid)
        RESULTS.mkdir(parents=True, exist_ok=True)
        (RESULTS / "carry_lemma.json").write_text(
            json.dumps({"horizon_ledges": rows}, indent=2) + "\n",
            encoding="utf-8",
        )

    def test_one_high_yes_rows_cat_meets(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        for sid in ("D_ledge_end31", "D_sill_end31", "D_ledge_to_gap"):
            scene = panel[sid]
            f3 = evaluate_f3(
                scene["walls"], scene["mass"], scene["monitor"],
                scene["W"], scene["H"], scene["thresh"],
                dx=scene["dx"], crest_y=scene["crest_y"],
            )
            self.assertTrue(f3["one_high"]["all_wall_supported"], sid)
            self.assertTrue(f3["one_high"]["cat_meets_R_catwalk"], sid)
            self.assertNotEqual(f3["static"], "CERTIFIED_NO", sid)
            oracle = run_oracle(scene, "yes_exit")
            self.assertEqual(oracle["Qdyn"], 1, sid)

    def test_packed_yes_outside_one_high(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        for sid in ("A_w4_x26_V180", "C_adj4_V60"):
            scene = panel[sid]
            f3 = evaluate_f3(
                scene["walls"], scene["mass"], scene["monitor"],
                scene["W"], scene["H"], scene["thresh"],
                dx=scene["dx"], crest_y=scene["crest_y"],
                audit_soups=True,
            )
            self.assertFalse(f3["one_high"]["all_wall_supported"], sid)
            self.assertEqual(f3["static"], "UNRESOLVED", sid)
            self.assertFalse(f3["wall_soup"]["meets_R_catwalk"], sid)
            oracle = run_oracle(scene, "yes_exit")
            self.assertEqual(oracle["Qdyn"], 1, sid)

    def test_hostile_outside_one_high(self):
        scene = hostile_scene()
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
        )
        self.assertFalse(f3["one_high"]["all_wall_supported"])
        self.assertEqual(f3["static"], "UNRESOLVED")
        oracle = run_oracle(scene, "cut_exit")
        self.assertEqual(oracle["Qdyn"], 1)
        self.assertEqual(oracle["firstBreach"], 3)


class TestPackedYesY1Y2(unittest.TestCase):
    """Y1/Y2 occupancy YES predicates; both killed (NULLS_PACKED_YES.md)."""

    def _q_ref(self):
        rows_path = (
            F3.parent
            / "fluid-f2-review-20260912"
            / "input"
            / "fluid_dynamic_frontier_02"
            / "results"
            / "rows.jsonl"
        )
        stored = {}
        for line in rows_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            stored[row["id"]] = int(row["Q_ref"])
        return stored

    def test_y1_killed_by_floor_sitting_probe(self):
        scene = floor_sitting_column(26, 4, 60, scene_id="probe_w4_x26_V60")
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"], floor=scene["floor"],
        )
        self.assertTrue(f3["y1_match"], f3["packed_rectangle"])
        self.assertNotEqual(f3["static"], "CERTIFIED_YES")
        out = run_oracle(scene, "yes_exit")
        self.assertEqual(out["Qdyn"], 0)
        RESULTS.mkdir(parents=True, exist_ok=True)
        payload = {
            "y1": "FALSE",
            "probe_w4_x26_V60": {
                "Qdyn": int(out["Qdyn"]),
                "firstBreach": out["firstBreach"],
                "stepsRun": out["stepsRun"],
                "stop": out["stop"],
                "shape": f3["packed_rectangle"],
                "static": f3["static"],
            },
        }
        prior = {}
        dest = RESULTS / "packed_yes.json"
        if dest.exists():
            prior = json.loads(dest.read_text(encoding="utf-8"))
        prior.update(payload)
        dest.write_text(json.dumps(prior, indent=2) + "\n", encoding="utf-8")

    def test_y2_killed_by_hang_probe(self):
        scene = hanging_column(26, 4, 60, scene_id="probe_hang_w4_x26_V60")
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"], floor=scene["floor"],
        )
        self.assertTrue(f3["y2_match"], f3["packed_rectangle"])
        self.assertFalse(f3["y1_match"])
        self.assertNotEqual(f3["static"], "CERTIFIED_YES")
        out = run_oracle(scene, "yes_exit")
        self.assertEqual(out["Qdyn"], 0)
        RESULTS.mkdir(parents=True, exist_ok=True)
        dest = RESULTS / "packed_yes.json"
        prior = {}
        if dest.exists():
            prior = json.loads(dest.read_text(encoding="utf-8"))
        prior["y2"] = "FALSE"
        prior["probe_hang_w4_x26_V60"] = {
            "Qdyn": int(out["Qdyn"]),
            "firstBreach": out["firstBreach"],
            "stepsRun": out["stepsRun"],
            "stop": out["stop"],
            "shape": f3["packed_rectangle"],
            "static": f3["static"],
        }
        dest.write_text(json.dumps(prior, indent=2) + "\n", encoding="utf-8")

    def test_panel_y1_empty_y2_matches_are_q_ref_1(self):
        stored = self._q_ref()
        y1_ids = []
        y2_rows = []
        for scene in scenes.build_panel():
            if scene["W"] != 64 or scene["H"] != 48:
                continue
            f3 = evaluate_f3(
                scene["walls"], scene["mass"], scene["monitor"],
                scene["W"], scene["H"], scene["thresh"],
                dx=scene["dx"], crest_y=scene["crest_y"], floor=scene["floor"],
            )
            if f3["y1_match"]:
                y1_ids.append(scene["id"])
            if f3["y2_match"]:
                y2_rows.append({
                    "id": scene["id"],
                    "Q_ref": stored[scene["id"]],
                    "shape": f3["packed_rectangle"],
                })
                self.assertEqual(stored[scene["id"]], 1, scene["id"])
        self.assertEqual(y1_ids, [])
        self.assertIn("A_w4_x26_V180", [r["id"] for r in y2_rows])
        self.assertIn("C_adj4_V60", [r["id"] for r in y2_rows])
        RESULTS.mkdir(parents=True, exist_ok=True)
        dest = RESULTS / "packed_yes.json"
        prior = {}
        if dest.exists():
            prior = json.loads(dest.read_text(encoding="utf-8"))
        prior["panel_y1_matches"] = y1_ids
        prior["panel_y2_matches"] = y2_rows
        dest.write_text(json.dumps(prior, indent=2) + "\n", encoding="utf-8")

    def test_known_packed_looking_q0_do_not_match(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        for sid in ("C_adj4_V20", "C_adj4_V40", "A_w4_x24_V180"):
            scene = panel[sid]
            f3 = evaluate_f3(
                scene["walls"], scene["mass"], scene["monitor"],
                scene["W"], scene["H"], scene["thresh"],
                dx=scene["dx"], crest_y=scene["crest_y"], floor=scene["floor"],
            )
            self.assertFalse(f3["y1_match"], sid)
            self.assertFalse(f3["y2_match"], sid)

    def test_hostile_not_y1_y2_not_official_yes(self):
        scene = hostile_scene()
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"], floor=scene["floor"],
        )
        self.assertFalse(f3["y1_match"])
        self.assertFalse(f3["y2_match"])
        self.assertNotEqual(f3["static"], "CERTIFIED_YES")
        self.assertEqual(f3["static"], "UNRESOLVED")


if __name__ == "__main__":
    unittest.main()
