"""Frozen F2 development panel. Scene identities are declared here.

This file is the protocol's scene generator. Do not add/remove scenes after
the scored execution. Original F1 tall/flat are included as exposed
development regressions, not as a new insufficiency study.

Grid default is the F1 container: W=64, H=48, divider x=32, crest_h=10
(crest_y = floor-crest_h = 36), monitor = right compartment.
"""
from __future__ import annotations

W0, H0 = 64, 48
THETA = 0.5
HORIZON = 300
MODEL = "B"


def make_container(W, H, crest_h, extra_walls=None):
    dx = W // 2
    walls = [0] * (W * H)
    for x in range(W):
        walls[x] = 1
        walls[(H - 1) * W + x] = 1
    for y in range(H):
        walls[y * W] = 1
        walls[y * W + W - 1] = 1
    floor = H - 2
    crest_y = floor - crest_h
    for y in range(crest_y, floor + 1):
        walls[y * W + dx] = 1
    if extra_walls:
        for x, y in extra_walls:
            if 0 < x < W - 1 and 0 < y < H - 1:
                walls[y * W + x] = 1
    monitor = [y * W + x for y in range(1, H - 1) for x in range(dx + 1, W - 1)]
    return {
        "W": W, "H": H, "walls": walls, "dx": dx, "floor": floor,
        "crest_y": crest_y, "crest_h": crest_h, "monitor": monitor,
    }


def empty_mass(W, H):
    return [0.0] * (W * H)


def add_rect(mass, walls, W, H, x0, x1, y0, y1):
    n = 0
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            i = y * W + x
            if 0 <= i < W * H and not walls[i]:
                mass[i] = 1.0
                n += 1
    return n


def fill_cells(mass, walls, W, cells, V):
    n = 0
    for y, x in cells:
        if n >= V:
            break
        i = y * W + x
        if not walls[i] and mass[i] <= 0:
            mass[i] = 1.0
            n += 1
    return n


def column_cells(geo, x0, width):
    cells = []
    for y in range(1, geo["floor"] + 1):
        for x in range(x0, x0 + width):
            cells.append((y, x))
    return cells


def flat_cells(geo):
    cells = []
    for y in range(geo["floor"], 0, -1):
        for x in range(1, geo["dx"]):
            cells.append((y, x))
    return cells


def ramp_cells(geo):
    order = list(range(geo["dx"] - 1, 0, -1))
    cells = []
    for depth in range(1, geo["floor"]):
        for k, x in enumerate(order):
            y = geo["floor"] - depth
            if depth <= (len(order) - k) and y > 0:
                cells.append((y, x))
    return cells


def spec_of(geo, mass, scene_id, family, note):
    V = float(sum(mass))
    return {
        "id": scene_id,
        "family": family,
        "note": note,
        "W": geo["W"],
        "H": geo["H"],
        "walls": list(geo["walls"]),
        "mass": [float(v) for v in mass],
        "monitor": list(geo["monitor"]),
        "dx": geo["dx"],
        "crest_y": geo["crest_y"],
        "crest_h": geo["crest_h"],
        "floor": geo["floor"],
        "V": V,
        "model": MODEL,
        "steps": HORIZON,
        "thresh": THETA,
    }


def build_panel():
    """Declared frozen panel. Order is the official evaluation order."""
    scenes = []

    def add(scene_id, family, geo, mass, note):
        scenes.append(spec_of(geo, mass, scene_id, family, note))

    # --- F1 exposed regressions (crest 10, V=180) ---
    g10 = make_container(W0, H0, 10)
    m = empty_mass(W0, H0)
    fill_cells(m, g10["walls"], W0, column_cells(g10, g10["dx"] - 6, 6), 180)
    add("f1_tall", "f1_regression", g10, m, "F1 tall w6 against divider V=180")
    m = empty_mass(W0, H0)
    fill_cells(m, g10["walls"], W0, flat_cells(g10), 180)
    add("f1_flat", "f1_regression", g10, m, "F1 flat puddle V=180")

    # --- Family A: placement at fixed V=180, crest=10 ---
    for width, x0s in (
        (2, (1, 15, 26, 28, 29, 30)),
        (4, (1, 14, 24, 26, 27, 28)),
        (6, (1, 13, 22, 24, 25, 26)),
    ):
        for x0 in x0s:
            if x0 + width > g10["dx"]:
                continue
            m = empty_mass(W0, H0)
            placed = fill_cells(m, g10["walls"], W0, column_cells(g10, x0, width), 180)
            add(
                f"A_w{width}_x{x0}_V180",
                "placement_V180",
                g10, m,
                f"column w={width} x0={x0} placed={placed}",
            )
    m = empty_mass(W0, H0)
    fill_cells(m, g10["walls"], W0, ramp_cells(g10), 180)
    add("A_ramp_V180", "placement_V180", g10, m, "ramp from floor, taller near divider")
    m = empty_mass(W0, H0)
    fill_cells(m, g10["walls"], W0, column_cells(g10, 1, 3), 90)
    fill_cells(m, g10["walls"], W0, column_cells(g10, g10["dx"] - 3, 3), 90)
    add("A_twocol_V180", "placement_V180", g10, m, "far+adj twin columns")

    # --- Family B: crest and volume on three named arrangements ---
    for crest_h in (8, 12):
        g = make_container(W0, H0, crest_h)
        for name, builder, V in (
            ("flat", lambda geo: flat_cells(geo), 180),
            ("far4", lambda geo: column_cells(geo, 1, 4), 140),
            ("adj4", lambda geo: column_cells(geo, geo["dx"] - 4, 4), 140),
        ):
            m = empty_mass(W0, H0)
            fill_cells(m, g["walls"], W0, builder(g), V)
            add(f"B_c{crest_h}_{name}_V{V}", "crest_volume", g, m, f"crest_h={crest_h} {name} V={V}")

    # --- Family C: threshold, empty, gap cells, small/adj V ---
    m = empty_mass(W0, H0)
    add("C_empty", "threshold", g10, m, "no water")
    m = empty_mass(W0, H0)
    m[40 * W0 + (g10["dx"] + 3)] = 1.0
    add("C_right_one", "threshold", g10, m, "one cell already in monitor")
    for y in (1, 20, 35):
        m = empty_mass(W0, H0)
        m[y * W0 + g10["dx"]] = 1.0
        add(f"C_gap_y{y}", "threshold", g10, m, f"single cell in gap column y={y}")
    for V in (20, 40, 60, 180):
        m = empty_mass(W0, H0)
        fill_cells(m, g10["walls"], W0, column_cells(g10, g10["dx"] - 4, 4), V)
        add(f"C_adj4_V{V}", "threshold", g10, m, f"adj4 V={V}")
    for V in (20, 180):
        m = empty_mass(W0, H0)
        fill_cells(m, g10["walls"], W0, column_cells(g10, 1, 4), V)
        add(f"C_far4_V{V}", "threshold", g10, m, f"far4 V={V}")

    # --- Family D: ledges and sills (declared extra walls) ---
    shelf_walls = [(x, 12) for x in range(1, 16)]
    g_shelf = make_container(W0, H0, 10, extra_walls=shelf_walls)
    m = empty_mass(W0, H0)
    add_rect(m, g_shelf["walls"], W0, H0, 2, 10, 11, 11)
    add("D_shelf_isolated", "ledge", g_shelf, m, "wall shelf y=12 x=1..15, water on it")

    ledgef = [(x, 22) for x in range(5, 33)]
    g_lf = make_container(W0, H0, 10, extra_walls=ledgef)
    m = empty_mass(W0, H0)
    add_rect(m, g_lf["walls"], W0, H0, 6, 20, 21, 21)
    add("D_ledge_to_gap", "ledge", g_lf, m, "ledge floor x=5..32, water x=6..20")

    for end in (28, 30, 31):
        walls = [(x, 22) for x in range(5, end + 1)]
        g = make_container(W0, H0, 10, extra_walls=walls)
        m = empty_mass(W0, H0)
        add_rect(m, g["walls"], W0, H0, 6, min(end, 20), 21, 21)
        add(f"D_ledge_end{end}", "ledge", g, m, f"ledge floor to x={end}")

    for end in (25, 31):
        walls = [(x, g10["crest_y"]) for x in range(1, end + 1)]
        g = make_container(W0, H0, 10, extra_walls=walls)
        m = empty_mass(W0, H0)
        add_rect(m, g["walls"], W0, H0, 1, end, g["crest_y"] - 1, g["crest_y"] - 1)
        add(f"D_sill_end{end}", "ledge", g, m, f"sill at crest-1 to x={end}")

    # --- Family E: unsupported singles / short stacks ---
    for y in (1, 35):
        m = empty_mass(W0, H0)
        m[y * W0 + (g10["dx"] - 1)] = 1.0
        add(f"E_adjcell_y{y}", "small", g10, m, f"single gap-adjacent cell y={y}")
    m = empty_mass(W0, H0)
    add_rect(m, g10["walls"], W0, H0, 31, 31, 26, 35)
    add("E_stack10_adj", "small", g10, m, "10-high unsupported stack against divider")
    m = empty_mass(W0, H0)
    add_rect(m, g10["walls"], W0, H0, 2, 4, 2, 4)
    add("E_blob9_far", "small", g10, m, "9-cell far blob above crest")

    # --- Family F: fill / overfull left basin ---
    m = empty_mass(W0, H0)
    fill_cells(m, g10["walls"], W0, flat_cells(g10), 400)
    add("F_flat_V400", "fill", g10, m, "flat V=400, basin may fill above crest")

    # --- Family G: declared scaling check (same contract, 96x64) ---
    W2, H2 = 96, 64
    gS = make_container(W2, H2, 12)
    m = empty_mass(W2, H2)
    fill_cells(m, gS["walls"], W2, column_cells(gS, 1, 4), 180)
    add("G_scale_far4_V180", "scale", gS, m, "96x64 far column")
    m = empty_mass(W2, H2)
    fill_cells(m, gS["walls"], W2, column_cells(gS, gS["dx"] - 4, 4), 180)
    add("G_scale_adj4_V180", "scale", gS, m, "96x64 adj column")

    # uniqueness
    ids = [s["id"] for s in scenes]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate scene id")
    if len(scenes) > 60:
        raise RuntimeError(f"panel too large: {len(scenes)}")
    return scenes


def scene_to_oracle_spec(scene, mode):
    return {
        "W": scene["W"],
        "H": scene["H"],
        "walls": scene["walls"],
        "mass": scene["mass"],
        "monitor": scene["monitor"],
        "thresh": scene["thresh"],
        "steps": scene["steps"],
        "mode": mode,
        "maxFall": 6,
        "snapshotSteps": [],
    }
