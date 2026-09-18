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

from bound_f3 import evaluate_f3  # noqa: E402
from f2_import import F2_PINNED, bound, scenes  # noqa: E402
from oracle_driver import run_oracle  # noqa: E402

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
    def test_v9_shelf_is_unresolved(self):
        panel = {s["id"]: s for s in scenes.build_panel()}
        scene = panel["D_shelf_isolated"]
        f3 = evaluate_f3(
            scene["walls"], scene["mass"], scene["monitor"],
            scene["W"], scene["H"], scene["thresh"],
            dx=scene["dx"], crest_y=scene["crest_y"],
        )
        self.assertGreaterEqual(f3["n_water"], 2)
        self.assertEqual(f3["static"], "UNRESOLVED")
        self.assertEqual(f3["B_refuted"]["verdict"], "CERTIFIED_NO")
        oracle = run_oracle(scene, "cut_exit")
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
        # Multi-cell former B-only NOs must not be restored as official static NO.
        for sid in ("D_shelf_isolated", "E_stack10_adj", "E_blob9_far"):
            self.assertIn(sid, unresolved_former_b)


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
            self.assertEqual(f3["static"], "UNRESOLVED", item["id"])
            if item["expect_Q"] is not None:
                self.assertEqual(row["Qdyn"], item["expect_Q"], item["id"])
            # Isolation must never false-NO a two-cell YES.
            if row["Qdyn"] == 1:
                self.assertNotEqual(f3["static"], "CERTIFIED_NO", item["id"])
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
            self.assertEqual(f3["static"], "UNRESOLVED", sid)
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
        self.assertEqual(f3["static"], "UNRESOLVED")
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


if __name__ == "__main__":
    unittest.main()
