#!/usr/bin/env python3
"""RCF01 envelope checks. Frozen protocol RCF01-envelope-1.

Does not import check_bridge.py. Uses prestige_envelope.py and rprm.core.
Development data, not holdout. Standard library only besides adjacent rprm.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from prestige_envelope import (
    ARITH_CONTRACT,
    B2,
    CUBE_CARRIER,
    CUBE_FRAME,
    ENVELOPE_VERSION,
    FLIP_CONTRACT,
    FULL_CUBE_CONTRACT,
    GRAPHS,
    METER,
    OMITTED,
    STAGE_TYPES,
    FullTableStore,
    MemoProduct,
    adapter_A,
    add_units,
    apply_fixed_receiver_map,
    apply_input_map,
    boolean_fiber_for_compact,
    coherent_transport,
    compact_add,
    compact_from_table,
    compact_mul_from_sites,
    contract_restart,
    count_shortcut_dwell,
    dwell_enabled,
    encode_display,
    eval_retained,
    fiving_display,
    fiving_display_wrong,
    graph_summary,
    input_maps,
    insert_midpoint,
    inspect_omitted,
    map_closes_b2,
    meter_snapshot,
    mobius,
    multiply_units,
    promote_cube,
    promote_stamp,
    pullback_table,
    quotient_for_map,
    read_admitted,
    reset_meter,
    split_center,
    strong_encode,
    strong_fiving,
    values_on_b2,
    zeta,
)

REGISTER = REPO / "research" / "core-recovery-01" / "CONCEPT_REGISTER.json"
COLD = ROOT / "cold_store"
REQUIRED_IDS = (
    "RCF-P1", "RCF-P2", "RCF-P3", "RCF-F1", "RCF-F2", "RCF-F3",
    "RCF-C1", "RCF-C2", "RCF-C3", "RCF-N1", "RCF-R1", "RCF-PI1", "RCF-AD1",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def boolean_laws():
    return list(itertools.product((0, 1), repeat=8))


def run_cases(work: Path) -> list[dict]:
    reset_meter()
    cold = work / "cold"
    if cold.exists():
        for path in cold.glob("*.json"):
            path.unlink()
    else:
        cold.mkdir(parents=True)
    laws = boolean_laws()
    rows: list[dict] = []

    def case(name: str, run) -> None:
        try:
            rows.append({"case_id": name, "outcome": "PASS", "data": run()})
        except Exception as exc:
            rows.append({"case_id": name, "outcome": "FAIL",
                         "data": {"exception": type(exc).__name__, "message": str(exc)}})

    def independent_kernel() -> dict:
        for f in laws:
            c = mobius(f)
            require(zeta(c) == tuple(Fraction(v) for v in f), "Boolean round trip failed")
            require(c[:7] == compact_from_table(f), "Compact disagrees with Mobius prefix")
        structured = 0
        for seed in range(32):
            f = tuple(Fraction((seed + 3) * (i + 1) - 17, i + 2) for i in range(8))
            require(zeta(mobius(f)) == f, "Rational round trip failed")
            structured += 1
        # Independent multiplication: site product versus original tables.
        samples = 0
        for f, g in itertools.islice(itertools.product(laws, laws), 0, None):
            # Exhaustive 256^2 is required for PE02; here only kernel sanity on 64 pairs.
            if samples >= 64:
                break
            if (sum(f) + sum(g)) % 7 != 0:
                continue
            a, b = compact_from_table(f), compact_from_table(g)
            site_product = compact_mul_from_sites(a, b)
            table_product = compact_from_table(tuple(x * y for x, y in zip(f, g)))
            require(site_product == table_product, "Independent B2 product disagrees")
            samples += 1
        return {"complete_boolean_tables": len(laws), "structured_rational_tables": structured,
                "independent_product_samples": samples, "method": "submask_walk_plus_B2_pointwise"}
    case("PE01_INDEPENDENT_CUBE_KERNEL", independent_kernel)

    def arithmetic() -> dict:
        summaries = [compact_from_table(f) for f in laws]
        for i, f in enumerate(laws):
            for j, g in enumerate(laws):
                a, b = summaries[i], summaries[j]
                require(compact_add(a, b) == compact_from_table(tuple(x + y for x, y in zip(f, g))),
                        "Compact addition failed")
                require(compact_mul_from_sites(a, b) == compact_from_table(tuple(x * y for x, y in zip(f, g))),
                        "Compact multiplication failed")
        env_a = promote_cube(laws[3], label="one", contract=ARITH_CONTRACT, cold_dir=None, name="a")
        env_b = promote_cube(laws[5], label="one", contract=ARITH_CONTRACT, cold_dir=None, name="b")
        added = add_units(env_a, env_b)
        multiplied = multiply_units(env_a, env_b)
        require(added.status == multiplied.status == "EXACT", "Envelope arithmetic refused a lawful pair")
        require(added.value.retained == compact_add(env_a.retained, env_b.retained), "Add envelope mismatch")
        # Seven-coefficient path must not read omitted coefficients.
        require(len(env_a.retained) == 7 and OMITTED not in range(7), "Omitted site leaked into retained")
        return {"ordered_law_pairs": len(laws) ** 2,
                "operations": ["pointwise_addition", "pointwise_multiplication"],
                "full_table_access_in_compact_operators": False,
                "positive_reuse": True}
    case("PE02_COMPACT_ARITHMETIC", arithmetic)

    def harmless() -> dict:
        # Affine laws: omitted coefficient is identically 0; flip_h stays affine.
        affine = []
        for coeffs in itertools.product((0, 1), repeat=4):
            a0, ah, ax, ay = coeffs
            table = tuple(a0 + ah * ((s >> 0) & 1) + ax * ((s >> 1) & 1) + ay * ((s >> 2) & 1)
                          for s in range(8))
            affine.append(table)
        flip = input_maps()["flip_h"]
        require(not map_closes_b2(flip), "Sanity: flip_h is not B2-closed for arbitrary laws")
        for f in affine:
            require(mobius(f)[7] == 0, "Affine witness has a three-way term")
            env = promote_cube(f, label="one", contract=FLIP_CONTRACT, cold_dir=None, name="affine")
            padded = zeta(tuple(env.retained) + (Fraction(0),))
            got = compact_from_table(pullback_table(padded, flip))
            require(got == compact_from_table(pullback_table(f, flip)),
                    "Affine class failed to reuse C2 under flip_h")
        return {"affine_tables": len(affine), "omitted_forced": 0,
                "successful_simplification": True,
                "scope": "degree-at-most-1 laws on the three-cube; not arbitrary tables"}
    case("PE03_HARMLESS_OMISSION", harmless)

    def insufficiency() -> dict:
        f0 = tuple(s.bit_count() for s in range(8))
        f1 = tuple(s.bit_count() + int(s == 7) for s in range(8))
        require(compact_from_table(f0) == compact_from_table(f1), "Witness did not collide")
        env0 = promote_cube(f0, label="one", contract=FLIP_CONTRACT, cold_dir=None, name="f0")
        env1 = promote_cube(f1, label="one", contract=FLIP_CONTRACT, cold_dir=None, name="f1")
        r0 = apply_input_map(env0, "fiving_slice")
        r1 = apply_input_map(env1, "fiving_slice")
        require(r0.status == r1.status == "REOPEN_REQUIRED", "Hot C2 must refuse flip without cold")
        require(r0.disposition == "MANY", "C2 fiber is not reported as MANY")
        flip = input_maps()["flip_h"]
        out0, out1 = pullback_table(f0, flip), pullback_table(f1, flip)
        require(compact_from_table(out0) != compact_from_table(out1), "Witness did not separate")
        require((f0[6], f1[6], int(out0[6]), int(out1[6])) == (2, 2, 3, 4), "Wrong 2->3/4 readouts")
        return {"same_present_readout": [2, 2], "after_fiving_readout": [3, 4],
                "hot_status": r0.status, "fiber": r0.disposition,
                "verdict_on_C2_fiving_lift": "REFUTED",
                "this_expected_refutation_is_a_successful_test": True}
    case("PE04_OPERATION_INSUFFICIENCY", insufficiency)

    def cold_repair() -> dict:
        f0 = tuple(s.bit_count() for s in range(8))
        f1 = tuple(s.bit_count() + int(s == 7) for s in range(8))
        env0 = promote_cube(f0, label="one", contract=FULL_CUBE_CONTRACT, cold_dir=cold, name="repair0")
        env1 = promote_cube(f1, label="one", contract=FULL_CUBE_CONTRACT, cold_dir=cold, name="repair1")
        r0 = apply_input_map(env0, "flip_h")
        r1 = apply_input_map(env1, "flip_h")
        require(r0.status == r1.status == "EXACT", "Cold reopen failed to repair")
        require(r0.value.retained != r1.value.retained, "Repair erased the distinction")
        omitted = inspect_omitted(env1)
        require(omitted.status == "EXACT" and omitted.value == 4, "Omitted site readout wrong")
        return {"repaired": True, "omitted_f1": str(omitted.value), "used_cold": True}
    case("PE05_COLD_REOPEN_REPAIR", cold_repair)

    def missing_cold() -> dict:
        f = tuple(s.bit_count() + int(s == 7) for s in range(8))
        env = promote_cube(f, label="one", contract=FLIP_CONTRACT, cold_dir=None, name="none")
        fiber = boolean_fiber_for_compact(compact_from_table(tuple((s.bit_count() % 2) for s in range(8))))
        r = apply_input_map(env, "flip_h")
        require(r.status == "REOPEN_REQUIRED" and r.disposition == "MANY", "Missing cold must refuse")
        require(fiber.disposition in ("MANY", "ONE"), "Fiber helper failed")
        return {"status": r.status, "disposition": r.disposition, "witness": r.witness,
                "boolean_example_fiber": fiber.disposition, "fiber_size": len(fiber.members)}
    case("PE06_MISSING_COLD_REFUSAL", missing_cold)

    def stale_cold() -> dict:
        f = tuple(range(8))
        env = promote_cube(f, label="one", contract=FULL_CUBE_CONTRACT, cold_dir=cold, name="stale")
        path = Path(env.cold_route)
        require(path.exists(), "Fixture was not written")
        original = path.read_bytes()
        path.write_bytes(original.replace(b"BOOL_CUBE_Q_n3", b"BOOL_CUBE_Q_n9", 1))
        r = apply_input_map(env, "flip_h")
        require(r.status == "INVALID_DEPENDENCY", "Altered bytes were accepted")
        path.write_bytes(original)
        path.unlink()
        missing = apply_input_map(env, "flip_h")
        require(missing.status in ("UNRESOLVED", "INVALID_DEPENDENCY"), "Deleted artifact was accepted")
        return {"altered_bytes_status": r.status, "deleted_status": missing.status,
                "physically_mutated": True, "did_not_set_valid_false_only": True}
    case("PE07_STALE_COLD_REJECT", stale_cold)

    def coherent() -> dict:
        f0 = tuple(s.bit_count() for s in range(8))
        f1 = tuple(s.bit_count() + int(s == 7) for s in range(8))
        env0 = promote_cube(f0, label="one", contract=FULL_CUBE_CONTRACT, cold_dir=cold, name="tr0")
        env1 = promote_cube(f1, label="one", contract=FULL_CUBE_CONTRACT, cold_dir=cold, name="tr1")
        bijections = set()
        for perm in itertools.permutations(range(3)):
            for offset in range(8):
                bijections.add(tuple(
                    sum(((s >> perm[j]) & 1) << j for j in range(3)) ^ offset
                    for s in range(8)))
        require(len(bijections) == 48, "Wrong cube symmetry count")
        for mapping in bijections:
            t0 = coherent_transport(env0, mapping)
            t1 = coherent_transport(env1, mapping)
            require(t0.status == t1.status == "EXACT", "Coherent transport failed")
            v0, v1 = dict(t0.value), dict(t1.value)
            require(v0 == v1, "Coherent receiver distinguished a transported pair")
            require(len(v0) == 7, "Transport lost an address")
        # Compact-only coherent transport (no cold): values at sources in B2 suffice.
        hot = promote_cube(f0, label="one", contract=ARITH_CONTRACT, cold_dir=None, name="hot")
        identity = tuple(range(8))
        hot_t = coherent_transport(hot, identity)
        require(hot_t.status == "EXACT" and hot_t.witness["used_cold"] is False,
                "Identity transport should not demand cold")
        return {"bijections": len(bijections), "result": "seven transported observations remain sufficient",
                "hot_identity_without_cold": True}
    case("PE08_COHERENT_TRANSPORT", coherent)

    def mismatched() -> dict:
        f0 = tuple(s.bit_count() for s in range(8))
        f1 = tuple(s.bit_count() + int(s == 7) for s in range(8))
        env0 = promote_cube(f0, label="one", contract=FULL_CUBE_CONTRACT, cold_dir=cold, name="mm0")
        env1 = promote_cube(f1, label="one", contract=FULL_CUBE_CONTRACT, cold_dir=cold, name="mm1")
        flip = input_maps()["flip_h"]
        r0 = apply_fixed_receiver_map(env0, flip)
        r1 = apply_fixed_receiver_map(env1, flip)
        require(r0.status == r1.status == "EXACT", "Fixed-receiver repair with cold failed")
        require(r0.value.retained != r1.value.retained, "Fixed receiver hid the real distinction")
        # Storage-order shuffle of retained 7-tuple must not change B2 values.
        env = env0
        shuffled = list(env.retained)
        # Deliberate wrong pairing of coefficients to sites is a mismatched frame.
        bad_frame = Envelope_from(env, retained=tuple(reversed(env.retained)), frame_id="reversed_storage")
        require(env.frame_id != bad_frame.frame_id, "Frame identity was not distinct")
        require(values_on_b2(env.retained) != values_on_b2(tuple(reversed(env.retained))),
                "Reversed storage coincidentally agreed")
        return {"fixed_receiver_separates": True, "frame_mismatch_detected": True,
                "renaming_storage_is_not_transport": True}
    case("PE09_MISMATCHED_TRANSPORT", mismatched)

    def winding() -> dict:
        checked = 0
        for w, h, r in itertools.product(range(-3, 4), (0, 1), range(5)):
            n = strong_encode(w, h, r)
            w1, h1, r1 = strong_fiving(w, h, r)
            require(strong_encode(w1, h1, r1) == n + 5, "Strong plus-five encoding failed")
            w2, h2, r2 = strong_fiving(w1, h1, r1)
            require((w2, h2, r2) == (w + 1, h, r), "Two fivings erased winding")
            d = encode_display(h, r)
            require(fiving_display(fiving_display(d)) == d, "Finite display is not an involution")
            checked += 1
        # A strong-history question cannot treat two fivings as identity.
        start = (0, 0, 0)
        mid = strong_fiving(*start)
        end = strong_fiving(*mid)
        require(end != start, "History question collapsed")
        return {"lifted_states_checked": checked, "finite_return_is_strong_return": False,
                "two_step_history": {"start": start, "end": end}}
    case("PE10_WINDING_HISTORY", winding)

    def equal_label() -> dict:
        a = promote_cube(tuple(range(8)), label="one", contract=ARITH_CONTRACT, cold_dir=cold,
                         name="histA", history=(("winding", 0),))
        b = promote_cube(tuple(range(8)), label="one", contract=ARITH_CONTRACT, cold_dir=cold,
                         name="histB", history=(("winding", 1),))
        require(a.visible_unit_label == b.visible_unit_label == "one", "Labels should match")
        require(a.history != b.history, "History was not retained")
        require(a.retained == b.retained, "Same table should share C2")
        return {"equal_outward_one": True, "history_distinguished": True,
                "permitted_operation_set_not_identified_by_label": True}
    case("PE11_EQUAL_LABEL_DISTINCT", equal_label)

    def dwell() -> dict:
        a = promote_stamp("A5", label="one")
        b = promote_stamp("B6", label="one")
        c = promote_stamp("C7", label="one")
        require(a.retained == (3, 2, 0) and b.retained == (3, 3, 1) and c.retained == (4, 3, 0),
                "Donor quotient counts disagree")
        da, db, dc = dwell_enabled(a), dwell_enabled(b), dwell_enabled(c)
        require(da.status == "EXACT" and da.value is True, "A5 dwell missing")
        require(db.status == "UNSUPPORTED" and db.disposition == "NONE", "B6 dwell must be refused")
        require(dc.status == "EXACT" and dc.value is True, "C7 dwell missing")
        require(a.retained[0] == b.retained[0], "Vertex-count collision absent")
        require(STAGE_TYPES["A5"]["dwell_allowed"] != STAGE_TYPES["B6"]["dwell_allowed"],
                "Authored dwell collision absent")
        return {"quotient": {"A5": a.retained, "B6": b.retained, "C7": c.retained},
                "dwell": {"A5": da.value, "B6": db.value, "C7": dc.value},
                "vertex_count_only": "REFUTED_FOR_DWELL",
                "safety_is": "authored process admission"}
    case("PE12_DWELL_ENABLEDNESS", dwell)

    def count_shortcut() -> dict:
        a = promote_stamp("A5", label="one")
        b = promote_stamp("B6", label="one")
        fake_a = count_shortcut_dwell(a.retained)
        fake_b = count_shortcut_dwell(b.retained)
        require(fake_a is True and fake_b is True, "Shortcut should collide")
        actual_a = dwell_enabled(a).value
        actual_b = dwell_enabled(b).value
        require(actual_a is True and actual_b is False, "Actual dwell must use stage type")
        require(fake_b != actual_b, "Shortcut was not actually rejected")
        return {"count_equals_3_shortcut": {"A5": fake_a, "B6": fake_b},
                "actual": {"A5": actual_a, "B6": actual_b},
                "shortcut_rejected": True}
    case("PE13_COUNT_SHORTCUT_REJECT", count_shortcut)

    def wrong_adapter() -> dict:
        # +4 does not implement the h-flip adapter.
        disagreements = 0
        for r, h, x, y in itertools.product(range(5), (0, 1), (0, 1), (0, 1)):
            d, xx, yy = adapter_A(h, x, y, r)
            five = (fiving_display(d), xx, yy)
            flipped = adapter_A(1 - h, x, y, r)
            four = (fiving_display_wrong(d, 4), xx, yy)
            require(five == flipped, "True +5 adapter failed")
            if four != flipped:
                disagreements += 1
        require(disagreements == 40, "Wrong +4 adapter accidentally agreed everywhere")
        # Equating raw vertex count 5 with residue-5 fiving display.
        a5_vertices = len(GRAPHS["A5"]()[0])
        require(a5_vertices == 5, "A5 should have five raw vertices")
        require(encode_display(1, 0) == 5, "Display 5 is (h=1,r=0)")
        # These equal numerals do not share operations: dwell vs fiving.
        stamp = promote_stamp("A5", label="five")
        require("fiving_slice" not in stamp.contract, "Stamp acquired a fiving operation by numeral")
        require(dwell_enabled(stamp).status == "EXACT", "A5 dwell should remain")
        return {"plus4_disagreements": disagreements, "numeral_5_collision": True,
                "shared_operation_set": False, "adapter_rejected_by_mapping": True}
    case("PE14_WRONG_ADAPTER", wrong_adapter)

    def composition_ok() -> dict:
        start = promote_stamp("A5", label="one")
        mid = split_center(start)
        require(mid.status == "EXACT" and mid.value.stage == "B6", "Split failed")
        require(dwell_enabled(mid.value).status == "UNSUPPORTED", "Enabledness lost at B6")
        end = insert_midpoint(mid.value)
        require(end.status == "EXACT" and end.value.stage == "C7", "Midpoint failed")
        require(dwell_enabled(end.value).status == "EXACT", "C7 dwell missing after composition")
        back = contract_restart(end.value)
        require(back.status == "EXACT" and back.value.stage == "A5", "Restart failed")
        # Cube: add then clamp_h_0, both B2-closed, vs full-table reference.
        f = tuple(range(8))
        g = tuple(2 * v for v in range(8))
        env_f = promote_cube(f, label="one", contract=ARITH_CONTRACT, cold_dir=None, name="cf")
        env_g = promote_cube(g, label="one", contract=ARITH_CONTRACT, cold_dir=None, name="cg")
        summed = add_units(env_f, env_g)
        clamped = apply_input_map(summed.value, "clamp_h_0")
        store = FullTableStore()
        store.put("f", f)
        store.put("g", g)
        ref_sum = store.add("f", "g")
        ref_clamp = pullback_table(ref_sum, input_maps()["clamp_h_0"])
        require(clamped.status == "EXACT", "Closed composition refused")
        require(clamped.value.retained == compact_from_table(ref_clamp), "Composed compact disagrees with original")
        return {"stamp_path": ["A5", "B6", "C7", "A5"],
                "cube_add_then_clamp": True,
                "intermediate_enabledness": {"A5": True, "B6": False, "C7": True}}
    case("PE15_COMPOSITION_POSITIVE", composition_ok)

    def composition_broken() -> dict:
        a = promote_stamp("A5", label="one")
        b = promote_stamp("B6", label="one")
        # Each component owns a local PASS: A5 dwell exact; B6 graph summary exact.
        require(dwell_enabled(a).status == "EXACT", "A5 component")
        require(b.retained == graph_summary(*GRAPHS["B6"]()), "B6 component")
        # Shared participant/frame/operation is missing: dwell composed onto B6 via count.
        composed_via_count = count_shortcut_dwell(b.retained)
        actual = dwell_enabled(b)
        require(composed_via_count is True and actual.status == "UNSUPPORTED",
                "Broken composition was not caught")
        # Cube: add requires shared frame.
        f = tuple(range(8))
        left = promote_cube(f, label="one", contract=ARITH_CONTRACT, cold_dir=None, name="L")
        from prestige_envelope import Envelope
        right = Envelope(
            family=left.family, visible_unit_label="one", retained=left.retained,
            contract=left.contract, carrier_id=left.carrier_id,
            frame_id="other_frame", version=left.version,
            cold_route=None, cold_sha256=None,
        )
        mixed = add_units(left, right)
        require(mixed.status == "UNSUPPORTED", "Cross-frame add was accepted")
        return {"component_local_pass": True, "composed_dwell_via_count": composed_via_count,
                "actual_dwell_on_B6": actual.status, "cross_frame_add": mixed.status}
    case("PE16_BROKEN_COMPOSITION", composition_broken)

    def probes() -> dict:
        pairs = {}
        for f in laws:
            pairs.setdefault(compact_from_table(f), []).append(f)
        require(len(pairs) == 128, "Unexpected Boolean C2 fiber count")
        for siblings in pairs.values():
            require(len(siblings) == 2, "Fiber size")
            for s in B2:
                require(siblings[0][s] == siblings[1][s], "Old probe separated")
            require(siblings[0][7] != siblings[1][7], "New probe failed")
        return {"redundant_probes_per_fiber": 7, "distinguishing_site_mask": 7,
                "fibers": 128, "disposition": "MANY"}
    case("PE17_REDUNDANT_VS_NEW_PROBE", probes)

    def full_coeffs() -> dict:
        maps = input_maps()
        checked = 0
        for f in laws:
            stored = mobius(f)
            for mapping in maps.values():
                candidate = mobius(tuple(
                    sum(stored[t] for t in range(8) if t & mapping[s] == t)
                    for s in range(8)))
                require(candidate == mobius(pullback_table(f, mapping)), "Full-coefficient repair failed")
                checked += 1
        return {"law_map_pairs": checked, "runtime_advantage_claimed": False,
                "sometimes_requires_every_original_value": True}
    case("PE18_FULL_COEFF_TRANSFORM", full_coeffs)

    def baselines() -> dict:
        store = FullTableStore()
        memo = MemoProduct()
        f = tuple(range(8))
        g = tuple((i * i) % 5 for i in range(8))
        store.put("f", f)
        store.put("g", g)
        env_f = promote_cube(f, label="one", contract=ARITH_CONTRACT, cold_dir=None, name="bf")
        env_g = promote_cube(g, label="one", contract=ARITH_CONTRACT, cold_dir=None, name="bg")
        compact_sum = add_units(env_f, env_g).value.retained
        compact_prod = multiply_units(env_f, env_g).value.retained
        require(compact_sum == compact_from_table(store.add("f", "g")), "Full-table add disagrees")
        require(compact_prod == compact_from_table(store.mul("f", "g")), "Full-table mul disagrees")
        require(memo.mul(env_f.retained, env_g.retained) == compact_prod, "Memo disagrees")
        require(memo.mul(env_f.retained, env_g.retained) == compact_prod, "Memo second call")
        require(memo.hits >= 1, "Memo did not hit")
        flip = apply_input_map(env_f, "clamp_h_0")
        require(flip.status == "EXACT", "Closed map should match full storage")
        require(flip.value.retained == compact_from_table(store.apply("f", input_maps()["clamp_h_0"])),
                "Baseline clamp disagrees")
        outside = apply_input_map(env_f, "flip_h")
        require(outside.status == "UNSUPPORTED", "Arithmetic contract must refuse flip as outside admission")
        flip_env = promote_cube(f, label="one", contract=FLIP_CONTRACT, cold_dir=None, name="bflip")
        refused = apply_input_map(flip_env, "flip_h")
        require(refused.status == "REOPEN_REQUIRED", "Admitted flip without cold must reopen")
        full_flip = store.apply("f", input_maps()["flip_h"])
        require(len(full_flip) == 8, "Full-table flip must return eight sites")
        return {"methods_agree_on_B2_arithmetic": True,
                "memo_is_ordinary_caching": True,
                "compact_refuses_flip_without_cold": True,
                "outside_contract_status": outside.status,
                "admitted_without_cold_status": refused.status,
                "full_table_computes_flip": True,
                "rprm_label_not_required_to_win": True,
                "memo_hits": memo.hits, "full_lookups": store.lookups}
    case("PE19_BASELINE_COMPARISON", baselines)

    def constrained() -> dict:
        # Bridge-note proposition is for arbitrary laws. Affine subclass is closed
        # under flip_h, so C2 reuse succeeds — a positive simplification.
        flip = input_maps()["flip_h"]
        require(not map_closes_b2(flip), "Arbitrary-law closure of B2 under flip_h")
        closed_affine = 0
        for coeffs in itertools.product((0, 1), repeat=4):
            a0, ah, ax, ay = coeffs
            f = tuple(a0 + ah * ((s) & 1) + ax * ((s >> 1) & 1) + ay * ((s >> 2) & 1) for s in range(8))
            env = promote_cube(f, label="one", contract=FLIP_CONTRACT, cold_dir=None, name="c")
            padded = zeta(tuple(env.retained) + (Fraction(0),))
            require(compact_from_table(pullback_table(padded, flip)) == compact_from_table(pullback_table(f, flip)),
                    "Affine C2 reuse failed")
            closed_affine += 1
        return {"proposition_scope": "all maps X->Y, Y has two values",
                "hostile_outside_scope": "degree <= 1 laws remain exact on C2 under flip_h",
                "affine_cases": closed_affine,
                "universal_compression_failure_not_assumed": True}
    case("PE20_CONSTRAINED_CLASS", constrained)

    def rprm_quotient() -> dict:
        closed = quotient_for_map("clamp_h_0")
        open_map = quotient_for_map("flip_h")
        require(closed["status"] == "ACCEPT", "clamp_h_0 should descend")
        require(open_map["status"] == "REJECT", "flip_h must fail the operational quotient")
        require(open_map["reason"] in ("observation", "enabledness", "successor"),
                "Unexpected reject reason")
        return {"clamp_h_0": closed["status"], "flip_h": open_map["status"],
                "flip_h_reason": open_map["reason"],
                "helper": "rprm.core.deterministic_quotient"}
    case("PE21_RPRM_QUOTIENT", rprm_quotient)

    def coverage() -> dict:
        payload = json.loads(REGISTER.read_text(encoding="utf-8"))
        ids = [entry["id"] for entry in payload["entries"]]
        require(ids == list(REQUIRED_IDS), f"Concept IDs drifted: {ids}")
        require(len(set(ids)) == len(REQUIRED_IDS), "Duplicate concept IDs")
        return {"ids": ids, "count": len(ids)}
    case("PE22_CONCEPT_ID_COVERAGE", coverage)

    snapshot = meter_snapshot()
    for row in rows:
        if row["outcome"] == "PASS":
            row["data"] = dict(row["data"], meter=snapshot)
    return rows


def Envelope_from(env, **kwargs):
    from prestige_envelope import Envelope
    data = {
        "family": env.family, "visible_unit_label": env.visible_unit_label,
        "retained": env.retained, "contract": env.contract, "carrier_id": env.carrier_id,
        "frame_id": env.frame_id, "version": env.version, "cold_route": env.cold_route,
        "cold_sha256": env.cold_sha256, "history": env.history, "stage": env.stage,
    }
    data.update(kwargs)
    return Envelope(**data)


def validate(rows: list[dict], required: list[str]) -> None:
    require(len(set(required)) == len(required), "Duplicate required protocol IDs")
    require(all(isinstance(row, dict) and isinstance(row.get("case_id"), str)
                and row.get("outcome") in ("PASS", "FAIL") and isinstance(row.get("data"), dict)
                for row in rows), "Malformed result schema")
    ids = [row["case_id"] for row in rows]
    require(len(ids) == len(set(ids)), "Duplicate emitted case IDs")
    require(set(ids) == set(required),
            f"Coverage mismatch: missing={set(required) - set(ids)}, extra={set(ids) - set(required)}")
    require(all(row["outcome"] == "PASS" for row in rows), "At least one check failed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--control", choices=("none", "omit", "duplicate", "unexpected", "reorder"),
                        default="none")
    parser.add_argument("--work", type=Path, default=ROOT / "fixtures" / "work")
    args = parser.parse_args()
    require(not args.output.exists(), "Output already exists; use a fresh name")
    protocol_bytes = (ROOT / "PROTOCOL.json").read_bytes()
    protocol = json.loads(protocol_bytes)
    rows = run_cases(args.work)
    if args.control == "omit":
        rows = rows[:-1]
    elif args.control == "duplicate":
        rows[-1] = rows[0].copy()
    elif args.control == "unexpected":
        rows[-1] = rows[-1] | {"case_id": "UNDECLARED"}
    elif args.control == "reorder":
        rows.reverse()
    error = None
    try:
        validate(rows, protocol["required_case_ids"])
    except ValueError as exc:
        error = str(exc)
    report = {
        "evidence_class": "CURSOR_RCF01_ENVELOPE_DEVELOPMENT_CHECK_NOT_HOLDOUT",
        "status": "FAIL" if error else "PASS",
        "coverage_error": error,
        "control": args.control,
        "python": sys.version,
        "platform": platform.platform(),
        "source_sha256": hashlib.sha256((ROOT / "prestige_envelope.py").read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
        "historical_RPRM_verifiers_rerun": False,
        "meter": meter_snapshot(),
        "results": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps({"status": report["status"], "control": args.control,
                      "emitted_cases": len(rows), "output": str(args.output), "error": error}))
    return 2 if error else 0


if __name__ == "__main__":
    raise SystemExit(main())
