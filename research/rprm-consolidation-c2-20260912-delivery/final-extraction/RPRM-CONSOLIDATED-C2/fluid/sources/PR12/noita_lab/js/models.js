// The three liquid models, swappable at runtime.
//   A: classic binary Noita-style water (down / down-diag / horizontal spread)
//   B: momentum/velocity water (inertia + splashes)
//   C: mass-per-cell level-equalizing water (pressure -> flat surfaces + U-tube)
// Each exposes step(grid). Only cells in awake chunks are visited.

const MODELS = ['A', 'B', 'C', 'D', 'E', 'F'];
const MODEL_NAMES = {
  A: 'A · Binary (classic Noita)',
  B: 'B · Momentum (velocity)',
  C: 'C · Mass / level-equalizing',
  D: 'D · Level-aware (body-level field)',
  E: 'E · D_fast / E_exact (cheap, frame-identical to D)',
  F: 'F · D_fast variant (per-body gate, faster settling)',
};

// Horizontal reach for model A's spread step. Larger => flatter but more
// "teleporty" and more expensive.
const A_FLOW = 4;

function isBlocked(grid, x, y) {
  if (!grid.inBounds(x, y)) return true;
  const t = grid.type[grid.idx(x, y)];
  return t === WALL || t === SAND;
}
function isEmpty(grid, x, y) {
  return grid.inBounds(x, y) && grid.type[grid.idx(x, y)] === EMPTY;
}

// ---------------- Model A: binary water ----------------
function stepA(grid) {
  const f = grid.frame;
  grid.forEachActiveRow((x0, x1, y, ltr) => {
    const dir = ltr ? 1 : -1;
    const xs = ltr ? x0 : x1 - 1;
    const xe = ltr ? x1 : x0 - 1;
    for (let x = xs; x !== xe; x += dir) {
      const i = grid.idx(x, y);
      if (grid.type[i] !== WATER || grid.stamp[i] === f) continue;
      // 1. straight down
      if (isEmpty(grid, x, y + 1)) { moveWater(grid, i, grid.idx(x, y + 1), x, y, x, y + 1); continue; }
      // 2. down diagonals
      const d1 = ltr ? x - 1 : x + 1;
      const d2 = ltr ? x + 1 : x - 1;
      if (isEmpty(grid, d1, y + 1)) { moveWater(grid, i, grid.idx(d1, y + 1), x, y, d1, y + 1); continue; }
      if (isEmpty(grid, d2, y + 1)) { moveWater(grid, i, grid.idx(d2, y + 1), x, y, d2, y + 1); continue; }
      // 3. spread horizontally toward the nearest empty within A_FLOW
      let tx = -1;
      for (let s = 1; s <= A_FLOW; s++) {
        const a = ltr ? x - s : x + s;
        const b = ltr ? x + s : x - s;
        if (isEmpty(grid, a, y) && !wallBetween(grid, x, a, y)) { tx = a; break; }
        if (isEmpty(grid, b, y) && !wallBetween(grid, x, b, y)) { tx = b; break; }
      }
      if (tx >= 0) { moveWater(grid, i, grid.idx(tx, y), x, y, tx, y); }
    }
  });
}

function wallBetween(grid, x0, x1, y) {
  const lo = Math.min(x0, x1), hi = Math.max(x0, x1);
  for (let x = lo + 1; x < hi; x++) if (isBlocked(grid, x, y)) return true;
  return false;
}

function moveWater(grid, i, j, x, y, nx, ny) {
  grid.type[j] = WATER; grid.mass[j] = C.MaxMass; grid.stamp[j] = grid.frame;
  grid.type[i] = EMPTY; grid.mass[i] = 0;
  grid.wake(x, y); grid.wake(nx, ny); grid.movedCells++;
}

// ---------------- Model B: momentum water ----------------
// Each water cell carries a velocity. Gravity accelerates it; on impact,
// downward speed becomes a horizontal splash. Occupancy is still one cell.
function stepB(grid) {
  const f = grid.frame;
  grid.forEachActiveRow((x0, x1, y, ltr) => {
    const dir = ltr ? 1 : -1;
    const xs = ltr ? x0 : x1 - 1;
    const xe = ltr ? x1 : x0 - 1;
    for (let x = xs; x !== xe; x += dir) {
      const i = grid.idx(x, y);
      if (grid.type[i] !== WATER || grid.stamp[i] === f) continue;
      grid.vy[i] = Math.min(grid.vy[i] + B.gravity, B.maxV);

      // Try to fall (possibly several cells based on vy).
      const steps = Math.max(1, Math.round(grid.vy[i]));
      let cx = x, cy = y;
      let fell = false;
      for (let s = 0; s < steps; s++) {
        if (isEmpty(grid, cx, cy + 1)) { cy++; fell = true; }
        else break;
      }
      if (fell) {
        relocate(grid, i, cx, cy, x, y);
        continue;
      }
      // Blocked below: convert fall into a horizontal splash.
      let vx = grid.vx[i];
      if (Math.abs(vx) < 0.1) vx = (grid.vy[i] * B.restitution) * ((f + x) & 1 ? 1 : -1);
      else vx = vx * B.friction + (grid.vy[i] * B.restitution) * Math.sign(vx);
      grid.vy[i] = 0;

      const hdir = vx >= 0 ? 1 : -1;
      // prefer down-diagonal (rolling off), then horizontal
      if (isEmpty(grid, x + hdir, y + 1)) { grid.vx[i] = vx; relocate(grid, i, x + hdir, y + 1, x, y); continue; }
      if (isEmpty(grid, x - hdir, y + 1)) { grid.vx[i] = vx; relocate(grid, i, x - hdir, y + 1, x, y); continue; }
      if (isEmpty(grid, x + hdir, y)) { grid.vx[i] = vx * B.friction; relocate(grid, i, x + hdir, y, x, y); continue; }
      if (isEmpty(grid, x - hdir, y)) { grid.vx[i] = -vx * B.friction; relocate(grid, i, x - hdir, y, x, y); continue; }
      grid.vx[i] = 0; // fully stuck; sleep
    }
  });
}

function relocate(grid, i, nx, ny, ox, oy) {
  const j = grid.idx(nx, ny);
  grid.type[j] = WATER; grid.mass[j] = C.MaxMass;
  grid.vx[j] = grid.vx[i]; grid.vy[j] = grid.vy[i];
  grid.stamp[j] = grid.frame;
  grid.type[i] = EMPTY; grid.mass[i] = 0; grid.vx[i] = 0; grid.vy[i] = 0;
  grid.wake(ox, oy); grid.wake(nx, ny); grid.movedCells++;
}

// ---------------- Model C: mass / level-equalizing water ----------------
// Continuous mass per cell exchanged with down/left/right/up neighbours.
// A tiny compressibility lets connected columns equalize height (U-tube).
function stepC(grid) {
  const mass = grid.mass, nm = grid.newMass, type = grid.type;
  // newMass mirrors mass over the halo (active chunks + neighbours) so cells
  // that only RECEIVE flow are still copied and, below, committed. This keeps
  // the model mass-conserving at active/sleeping chunk boundaries.
  grid.computeHalo();
  grid.forEachHaloRow((x0, x1, y) => {
    for (let x = x0; x < x1; x++) nm[grid.idx(x, y)] = mass[grid.idx(x, y)];
  });

  const solid = (x, y) => {
    if (!grid.inBounds(x, y)) return true;
    const t = type[grid.idx(x, y)];
    return t === WALL || t === SAND;
  };

  grid.forEachActiveRow((x0, x1, y) => {
    for (let x = x0; x < x1; x++) {
      const i = grid.idx(x, y);
      if (type[i] === WALL || type[i] === SAND) continue;
      let remaining = mass[i];
      if (remaining <= 0) continue;
      let flow;

      // DOWN
      if (!solid(x, y + 1)) {
        const j = grid.idx(x, y + 1);
        flow = stableBottom(remaining + mass[j]) - mass[j];
        if (flow > C.MinFlow) flow *= 0.5;
        flow = clamp(flow, 0, Math.min(C.MaxSpeed, remaining));
        if (flow < C.MinFlowCutoff) flow = 0;
        nm[i] -= flow; nm[j] += flow; remaining -= flow;
      }
      // LEFT
      if (remaining > 0 && !solid(x - 1, y)) {
        const j = grid.idx(x - 1, y);
        flow = (mass[i] - mass[j]) / 4;
        if (flow > C.MinFlow) flow *= 0.5;
        flow = clamp(flow, 0, remaining);
        if (flow < C.MinFlowCutoff) flow = 0;
        nm[i] -= flow; nm[j] += flow; remaining -= flow;
      }
      // RIGHT
      if (remaining > 0 && !solid(x + 1, y)) {
        const j = grid.idx(x + 1, y);
        flow = (mass[i] - mass[j]) / 4;
        if (flow > C.MinFlow) flow *= 0.5;
        flow = clamp(flow, 0, remaining);
        if (flow < C.MinFlowCutoff) flow = 0;
        nm[i] -= flow; nm[j] += flow; remaining -= flow;
      }
      // UP (pressure): only pushes when this cell is over-full.
      if (remaining > 0 && !solid(x, y - 1)) {
        const j = grid.idx(x, y - 1);
        flow = remaining - stableBottom(remaining + mass[j]);
        if (flow > C.MinFlow) flow *= 0.5;
        flow = clamp(flow, 0, Math.min(C.MaxSpeed, remaining));
        if (flow < C.MinFlowCutoff) flow = 0;
        nm[i] -= flow; nm[j] += flow; remaining -= flow;
      }
    }
  });

  // Commit newMass -> mass over the halo, update types, decide what stays awake.
  grid.forEachHaloRow((x0, x1, y) => {
    for (let x = x0; x < x1; x++) {
      const i = grid.idx(x, y);
      if (type[i] === WALL || type[i] === SAND) continue;
      const before = mass[i];
      const after = nm[i];
      mass[i] = after;
      if (after > C.MinMass) {
        if (type[i] !== WATER) type[i] = WATER;
      } else {
        if (type[i] === WATER) type[i] = EMPTY;
        mass[i] = 0;
      }
      if (Math.abs(after - before) > C.SleepEps) { grid.wake(x, y); grid.movedCells++; }
    }
  });
}

function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }

// ---------------- Model D: level-aware (body-level field) ----------------
// The RPRM "change of representation" for PROBLEMS #1: a purely local rule can
// never SEE the quantity that decides the answer (a connected body's target
// free-surface level), so we retain that quantity explicitly. Each recompute we
//   1. label contiguous water bodies (flood fill over water cells),
//   2. flood each body's containing cavity (air+water bounded by walls),
//   3. read the target level straight off: fill the cavity bottom-up with the
//      body's volume; deep cells target MaxMass, the surface row a partial fill,
//   4. relax every cell a fraction toward that target via a MASS-CONSERVING
//      matched transfer (drain over-full cells top-down, fill deficit cells
//      bottom-up). Because target and current mass both sum to the body volume,
//      any partial relaxation conserves mass exactly.
// Local advection (down + horizontal spread, incompressible) still runs every
// step so splashes/dam-breaks stay alive; the level field carries the pressure
// that local flow cannot (equalizing a U-tube in O(1) label passes, not O(h)).

function stepD(grid) {
  grid.labelCells = 0;
  grid.labelPasses = 0;
  localAdvectD(grid);
  // Disturbance gate: how much did LOCAL advection (gravity/spread) just move?
  // While a scene is violently in motion this is large, so we throttle the
  // non-local level solve and let gravity produce the natural splash; once local
  // flow stalls the gate opens and the level field equalizes what gravity can't.
  const localMoved = grid.movedCells;
  const gate = 1 / (1 + localMoved * D.DisturbScale);
  if (grid.frame % D.RelabelEvery === 0) relaxLevels(grid, D.Relax * gate);
}

// Local, incompressible mass advection: gravity down-fill + horizontal spread.
// No up-pressure and no compressibility (the level field replaces both).
// When `track` is set, record every cell whose mass materially changed this frame
// (index + |delta|) so D_fast can tell WHICH bodies were externally disturbed and
// by how much — the signal that gates re-flooding and drives the per-body gate.
function localAdvectD(grid, track) {
  const mass = grid.mass, nm = grid.newMass, type = grid.type;
  grid.computeHalo();
  grid.forEachHaloRow((x0, x1, y) => {
    for (let x = x0; x < x1; x++) nm[grid.idx(x, y)] = mass[grid.idx(x, y)];
  });
  const solid = (x, y) => {
    if (!grid.inBounds(x, y)) return true;
    const t = type[grid.idx(x, y)];
    return t === WALL || t === SAND;
  };
  grid.forEachActiveRow((x0, x1, y) => {
    for (let x = x0; x < x1; x++) {
      const i = grid.idx(x, y);
      if (type[i] === WALL || type[i] === SAND) continue;
      let remaining = mass[i];
      if (remaining <= 0) continue;
      let flow;
      // DOWN (incompressible: never exceed MaxMass in the cell below)
      if (!solid(x, y + 1)) {
        const j = grid.idx(x, y + 1);
        flow = clamp(C.MaxMass - mass[j], 0, Math.min(D.MaxSpeed, remaining));
        if (flow < C.MinFlowCutoff) flow = 0;
        nm[i] -= flow; nm[j] += flow; remaining -= flow;
      }
      // LEFT
      if (remaining > 0 && !solid(x - 1, y)) {
        const j = grid.idx(x - 1, y);
        flow = (mass[i] - mass[j]) * D.SideFlow;
        flow = clamp(flow, 0, remaining);
        if (flow < C.MinFlowCutoff) flow = 0;
        nm[i] -= flow; nm[j] += flow; remaining -= flow;
      }
      // RIGHT
      if (remaining > 0 && !solid(x + 1, y)) {
        const j = grid.idx(x + 1, y);
        flow = (mass[i] - mass[j]) * D.SideFlow;
        flow = clamp(flow, 0, remaining);
        if (flow < C.MinFlowCutoff) flow = 0;
        nm[i] -= flow; nm[j] += flow; remaining -= flow;
      }
    }
  });
  const tstamp = track ? grid._touchStamp : null;
  const tgen = track ? grid._touchGen : 0;
  const tdelta = track ? grid._delta : null;
  const tlist = track ? grid._touchList : null;
  grid.forEachHaloRow((x0, x1, y) => {
    for (let x = x0; x < x1; x++) {
      const i = grid.idx(x, y);
      if (type[i] === WALL || type[i] === SAND) continue;
      const before = mass[i];
      const after = nm[i];
      mass[i] = after;
      if (after > C.MinMass) { if (type[i] !== WATER) type[i] = WATER; }
      else { if (type[i] === WATER) type[i] = EMPTY; mass[i] = 0; }
      const d = Math.abs(after - before);
      if (d > C.SleepEps) {
        grid.wake(x, y); grid.movedCells++;
        if (track) {
          if (tstamp[i] !== tgen) { tstamp[i] = tgen; tlist.push(i); tdelta[i] = d; }
          else tdelta[i] += d;
        }
      }
    }
  });
}

// The non-local pressure solve. Labels bodies that touch an awake chunk (settled
// asleep pools cost nothing), reads their target level, and relaxes toward it.
function relaxLevels(grid, relax) {
  if (relax == null) relax = D.Relax;
  const W = grid.w, H = grid.h, type = grid.type, mass = grid.mass;
  if (!grid._seen) {
    grid._seen = new Int32Array(W * H);
    grid._cav = new Int32Array(W * H);
    grid._tgt = new Float32Array(W * H);
    grid._stamp = 0;
    grid._stack = [];
  }
  const seen = grid._seen, cav = grid._cav, tgt = grid._tgt;
  const stack = grid._stack;
  const isWater = (i) => type[i] === WATER && mass[i] > C.MinMass;
  const isSolid = (i) => type[i] === WALL || type[i] === SAND;
  // One stamp for the whole call: `seen`/`cav` marks persist across seeds so a
  // body is processed once and cavity cells are first-claimed (multi-body split).
  grid._stamp++;
  const S = grid._stamp;

  grid.forEachActiveRow((x0, x1, y) => {
    for (let x = x0; x < x1; x++) {
      const start = y * W + x;
      if (!isWater(start)) continue;
      if (seen[start] === S) continue; // already part of a processed body

      // 1. Flood the connected water body (4-connectivity through water).
      const body = [];
      let top = H; // smallest y (highest cell) in the body
      stack.length = 0; stack.push(start); seen[start] = S;
      while (stack.length) {
        const c = stack.pop();
        body.push(c); grid.labelCells++;
        const cy = (c / W) | 0, cx = c - cy * W;
        if (cy < top) top = cy;
        if (cx > 0)     { const n = c - 1; if (seen[n] !== S && isWater(n)) { seen[n] = S; stack.push(n); } }
        if (cx < W - 1) { const n = c + 1; if (seen[n] !== S && isWater(n)) { seen[n] = S; stack.push(n); } }
        if (cy > 0)     { const n = c - W; if (seen[n] !== S && isWater(n)) { seen[n] = S; stack.push(n); } }
        if (cy < H - 1) { const n = c + W; if (seen[n] !== S && isWater(n)) { seen[n] = S; stack.push(n); } }
      }

      // 2. Flood the containing cavity (air+water, walls block). Bounded above
      //    by `top`: equilibrium level can never rise above the body's current
      //    highest water cell, so we never flood the open sky.
      const cavity = [];
      let V = 0;
      stack.length = 0;
      for (let k = 0; k < body.length; k++) { const c = body[k]; if (cav[c] !== S) { cav[c] = S; stack.push(c); } }
      while (stack.length) {
        const c = stack.pop();
        cavity.push(c); grid.labelCells++;
        const cy = (c / W) | 0, cx = c - cy * W;
        if (type[c] === WATER) V += mass[c];
        if (cx > 0)     { const n = c - 1; if (cy >= top && cav[n] !== S && !isSolid(n)) { cav[n] = S; stack.push(n); } }
        if (cx < W - 1) { const n = c + 1; if (cy >= top && cav[n] !== S && !isSolid(n)) { cav[n] = S; stack.push(n); } }
        if (cy > 0)     { const n = c - W; if (cy - 1 >= top && cav[n] !== S && !isSolid(n)) { cav[n] = S; stack.push(n); } }
        if (cy < H - 1) { const n = c + W; if (cav[n] !== S && !isSolid(n)) { cav[n] = S; stack.push(n); } }
      }
      grid.labelPasses++;

      // 3. Read the target level straight off: fill the cavity bottom-up with V.
      //    Sorting by cell index descending groups rows bottom-first (row-major).
      cavity.sort((a, b) => b - a);
      const n = cavity.length;
      let rem = V, k = 0;
      while (k < n && rem > 1e-9) {
        const yRow = (cavity[k] / W) | 0;
        let j = k;
        while (j < n && ((cavity[j] / W) | 0) === yRow) j++;
        const rowCount = j - k;
        const cap = rowCount * C.MaxMass;
        let per;
        if (rem >= cap) { per = C.MaxMass; rem -= cap; }
        else { per = rem / rowCount; rem = 0; }
        for (let q = k; q < j; q++) tgt[cavity[q]] = per;
        k = j;
      }
      for (; k < n; k++) tgt[cavity[k]] = 0; // above the level -> dry

      // 4. Mass-conserving matched relaxation toward target.
      let E = 0;
      for (let q = 0; q < n; q++) { const g = tgt[cavity[q]] - mass[cavity[q]]; if (g > 0) E += g; }
      if (E <= D.LevelEps) continue; // already level -> leave the body asleep

      let toMove = relax * E;
      // fill deficit cells bottom-up (cavity is sorted y-descending)
      let filled = 0;
      for (let q = 0; q < n && toMove > 1e-9; q++) {
        const c = cavity[q];
        const need = tgt[c] - mass[c];
        if (need <= 0) continue;
        const add = need < toMove ? need : toMove;
        mass[c] += add; toMove -= add; filled += add;
        if (type[c] !== WATER && mass[c] > 0) type[c] = WATER;
        grid.wake(c - ((c / W) | 0) * W, (c / W) | 0);
        grid.movedCells++;
      }
      // drain the SAME amount from over-full cells top-down (conserves mass)
      let toDrain = filled;
      for (let q = n - 1; q >= 0 && toDrain > 1e-9; q--) {
        const c = cavity[q];
        const avail = mass[c] - tgt[c];
        if (avail <= 0) continue;
        const sub = avail < toDrain ? avail : toDrain;
        mass[c] -= sub; toDrain -= sub;
        if (mass[c] <= C.MinMass) { mass[c] = 0; if (type[c] === WATER) type[c] = EMPTY; }
        grid.wake(c - ((c / W) | 0) * W, (c / W) | 0);
        grid.movedCells++;
      }
    }
  });
}

// ---------------- Model E: D_fast (cheap, certificate-gated model D) ----------
// Same physics and same read-off as D (identical U-tube Δh→0, mass 0.000%), but
// the expensive per-frame connected-components + cavity flood is AMORTIZED:
//
//   * Connected-body labels (`_bodyId`) and each body's cached summary
//     (cells, cavity, target level, RPRM certificate verdict) PERSIST across
//     frames — the incremental / dirty-region body tracking lever.
//   * Only bodies that were externally disturbed this frame (a cell touched by
//     local advection), or that changed topology (split/merge/new water), are
//     RE-FLOODED. Everything else reuses its cache.
//   * A body whose certificate `P_geo` (C1∧C3∧C4) holds and is still MOVING skips
//     the flood entirely and just relaxes toward its cached target level — this is
//     the certificate acting as a license to skip the recompute (#2→#1). An
//     uncertified moving body cannot be trusted stale, so it is re-flooded.
//   * A settled body (gap ≤ LevelEps) is skipped completely (zero cost).
//   * The disturbance gate is PER BODY (mass its own cells moved), so one splash
//     no longer throttles every other body in the scene.
//
// Worst case (a single body where every cell moves — e.g. a dam-break collapse)
// degenerates to D's full flood: that is the honest built-in "full-flood
// fallback", and it is exactly the uncertifiable violent phase, so the
// certificate saves little THERE. The wins are on settled/multi-body scenes and
// on the certified-but-still-moving U-tube fill.

function ensureFastState(grid) {
  const N = grid.w * grid.h;
  if (!grid._bodyId) {
    grid._bodyId = new Int32Array(N).fill(-1);
    grid._records = new Map();
    grid._nextId = 1;
    grid._fcav = new Int32Array(N);   // cavity first-claim marks (one stamp per frame)
    grid._fclaim = new Int32Array(N);  // which body claimed a cavity cell
    grid._ftgt = new Float32Array(N);  // per-cell target during a body's fill
    grid._fvis = new Int32Array(N);    // scratch visited marks for C1/C4 BFS
    grid._fcavStamp = 0;               // bumped once per relaxLevelsFast call
    grid._fvisStamp = 0;               // bumped per BFS
    grid._touchStamp = new Int32Array(N);
    grid._touchGen = 1;
    grid._delta = new Float32Array(N);
    grid._touchList = [];
    grid._fstack = [];
    grid._editList = [];               // cells edited via grid.set() since last solve
    grid._refloodDefects = [];         // witnessed successor_defect log (mode='witnessed')
  }
}

// Reset all cross-frame caches (call when the world is edited wholesale, e.g. a
// scenario load or a live model switch, so stale labels can't leak in).
function resetFastState(grid) {
  if (!grid._bodyId) return;
  grid._bodyId.fill(-1);
  grid._records.clear();
  grid._nextId = 1;
  grid._touchGen++;
  grid._touchList.length = 0;
  if (grid._editList) grid._editList.length = 0;
  if (grid._refloodDefects) grid._refloodDefects.length = 0;
}

function beginFastStep(grid) {
  ensureFastState(grid);
  grid.labelCells = 0;
  grid.labelPasses = 0;
  grid.bodiesReflooded = 0;
  grid.bodiesCertSkipped = 0;   // certified + moving: flood skipped, relax only
  grid.bodiesSettledSkipped = 0; // settled: skipped entirely
  grid.bodiesTotal = 0;
  grid.relaxCells = 0;          // cavity cells touched by cache-only relaxation
  // Invalidation accounting (surfaced for the witnessed-vs-heuristic comparison).
  grid.bodiesRefloodTimer = 0;      // (heuristic) re-floods forced purely by the CacheTTL timer
  grid.bodiesSettledReverify = 0;   // (heuristic) settled bodies re-verified purely by the TTL clock
  grid.bodiesRefloodWitnessed = 0;  // (witnessed) certified re-floods carrying a NAMED implicated cell
  grid.bodiesRefloodUnwitnessed = 0;// (witnessed) volume drifted but no cavity-cell witness (completeness gap)
  grid.lastDefect = null;           // most recent successor_defect (for the harness/UI)
  // Fresh touch generation for this frame.
  grid._touchGen++;
  grid._touchList.length = 0;
}

// Model E = D_fast (E_exact): the cache/skip optimization with relaxation rules
// IDENTICAL to model D. D throttles the level solve by a SCENE-WIDE moved-cell
// count and applies that one gate to EVERY body; E_exact does the same — it
// captures the scene-wide `movedCells` produced by local advection (before any
// relaxation adds to the counter) and passes that single gate to every body,
// reflooded or cached. This is what earns "accelerates the SAME computation,
// results preserved" — see experiments/test_frame_equality.js.
function stepE(grid) {
  beginFastStep(grid);
  localAdvectD(grid, true);
  const localMoved = grid.movedCells;                 // scene-wide, exactly as stepD
  const gate = 1 / (1 + localMoved * D.DisturbScale);
  if (grid.frame % D.RelabelEvery === 0) relaxLevelsFast(grid, D.Relax, gate, true);
}

// Model F = D_fast behavior variant (per-body faster settling). NOT bit-identical
// to D: reflooded bodies use a PER-BODY moved-mass gate (a still pool next to a
// splash equalizes at full speed) and cached certified-moving bodies relax with
// the full parameter WITHOUT any disturbance gate (settle faster). This is the
// original PR#9 "E" behavior, kept as a deliberately separate, differently-named
// variant so the exactness claim (E) is not conflated with the speed changes (F).
function stepF(grid) {
  beginFastStep(grid);
  localAdvectD(grid, true);
  if (grid.frame % D.RelabelEvery === 0) relaxLevelsFast(grid, D.Relax, null, false);
}

// Bottom-up matched, mass-conserving relaxation of one body toward its target,
// given a cavity sorted by cell index DESCENDING (row-major => bottom rows first)
// and a parallel `tgtVals` array. Identical transfer to D's `relaxLevels` step 4.
// Also maintains `_bodyId` for cells that gain/lose water so tracking stays live.
// Returns { E, Vnow, drift }. When `expectedV` is given, computes the body's
// current volume over the cavity in the SAME pass as the gap sum and, if it has
// drifted (external inflow/outflow), returns drift=true WITHOUT relaxing so the
// caller can re-flood/retarget.
function relaxBodyToTarget(grid, id, cavity, tgtVals, relax, expectedV) {
  const W = grid.w, mass = grid.mass, type = grid.type, bid = grid._bodyId;
  const n = cavity.length;
  let E = 0, Vnow = 0;
  for (let q = 0; q < n; q++) { const m = mass[cavity[q]]; Vnow += m; const g = tgtVals[q] - m; if (g > 0) E += g; }
  if (expectedV != null && Math.abs(Vnow - expectedV) > D.LevelEps) return { E, Vnow, drift: true };
  if (E <= D.LevelEps) return { E, Vnow, drift: false };
  let toMove = relax * E;
  let filled = 0;
  for (let q = 0; q < n && toMove > 1e-9; q++) {
    const c = cavity[q];
    const need = tgtVals[q] - mass[c];
    if (need <= 0) continue;
    const add = need < toMove ? need : toMove;
    mass[c] += add; toMove -= add; filled += add;
    if (type[c] !== WATER && mass[c] > 0) { type[c] = WATER; bid[c] = id; }
    else bid[c] = id;
    grid.wake(c % W, (c / W) | 0);
    grid.movedCells++;
  }
  let toDrain = filled;
  for (let q = n - 1; q >= 0 && toDrain > 1e-9; q--) {
    const c = cavity[q];
    const avail = mass[c] - tgtVals[q];
    if (avail <= 0) continue;
    const sub = avail < toDrain ? avail : toDrain;
    mass[c] -= sub; toDrain -= sub;
    // Keep the cell labelled with this body even when it empties: it is still in
    // the body's cavity, so if local advection later shoves water back into it we
    // recognise the move as INTERNAL (no spurious orphan -> no needless re-flood).
    if (mass[c] <= C.MinMass) { mass[c] = 0; if (type[c] === WATER) { type[c] = EMPTY; } bid[c] = id; }
    grid.wake(c % W, (c / W) | 0);
    grid.movedCells++;
  }
  return { E, Vnow, drift: false };
}

// Flood one connected water body from `seed`, its containing cavity (top-bounded,
// first-claim — EXACTLY as D/certificate do), read off the target level, evaluate
// the geometric certificate P_geo = C1∧C3∧C4, and return a cache record. Absorbs
// any previously-clean body it is 4-connected to (a merge). Increments labelCells.
function floodBodyFast(grid, seed, newId) {
  const W = grid.w, H = grid.h, type = grid.type, mass = grid.mass;
  const bid = grid._bodyId, cav = grid._fcav, claim = grid._fclaim;
  const tgt = grid._ftgt, stack = grid._fstack, records = grid._records, S = grid._fcavStamp;
  const isWater = (i) => type[i] === WATER && mass[i] > C.MinMass;
  const isSolid = (i) => type[i] === WALL || type[i] === SAND;

  // 1. Body flood (absorb any clean body we touch => merge).
  const body = [];
  let top = H;
  let bodyMoved = 0;
  const tstamp = grid._touchStamp, tgen = grid._touchGen, tdelta = grid._delta;
  const claimCell = (c) => {
    const old = bid[c];
    if (old >= 0 && old !== newId && records.has(old)) records.delete(old);
    bid[c] = newId;
  };
  stack.length = 0; claimCell(seed); stack.push(seed);
  while (stack.length) {
    const c = stack.pop();
    body.push(c); grid.labelCells++;
    if (tstamp[c] === tgen) bodyMoved += tdelta[c];
    const cy = (c / W) | 0, cx = c - cy * W;
    if (cy < top) top = cy;
    if (cx > 0)     { const nn = c - 1; if (bid[nn] !== newId && isWater(nn)) { claimCell(nn); stack.push(nn); } }
    if (cx < W - 1) { const nn = c + 1; if (bid[nn] !== newId && isWater(nn)) { claimCell(nn); stack.push(nn); } }
    if (cy > 0)     { const nn = c - W; if (bid[nn] !== newId && isWater(nn)) { claimCell(nn); stack.push(nn); } }
    if (cy < H - 1) { const nn = c + W; if (bid[nn] !== newId && isWater(nn)) { claimCell(nn); stack.push(nn); } }
  }

  // 2. Cavity flood (air+water, walls block), bounded above by `top`, first-claim.
  const cavity = [];
  let V = 0;
  let foreignWater = false, truncated = false;
  stack.length = 0;
  for (let k = 0; k < body.length; k++) { const c = body[k]; if (cav[c] !== S) { cav[c] = S; claim[c] = newId; stack.push(c); } else if (claim[c] !== newId) truncated = true; }
  while (stack.length) {
    const c = stack.pop();
    cavity.push(c); grid.labelCells++;
    const cy = (c / W) | 0, cx = c - cy * W;
    if (type[c] === WATER) V += mass[c];
    if (isWater(c) && bid[c] !== -1 && bid[c] !== newId) foreignWater = true;
    const pushN = (nn, okRow) => {
      if (!okRow || isSolid(nn)) return;
      if (cav[nn] !== S) { cav[nn] = S; claim[nn] = newId; stack.push(nn); }
      else if (claim[nn] !== newId) truncated = true;
    };
    if (cx > 0)     pushN(c - 1, cy >= top);
    if (cx < W - 1) pushN(c + 1, cy >= top);
    if (cy > 0)     pushN(c - W, cy - 1 >= top);
    if (cy < H - 1) pushN(c + W, true);
  }
  grid.labelPasses++;

  // 3. Read the target level off: fill the cavity bottom-up with V.
  cavity.sort((a, b) => b - a);
  const n = cavity.length;
  const tgtVals = new Float32Array(n);
  let rem = V, k = 0, surfRow = -1;
  while (k < n && rem > 1e-9) {
    const yRow = (cavity[k] / W) | 0;
    let j = k;
    while (j < n && ((cavity[j] / W) | 0) === yRow) j++;
    const rowCount = j - k;
    const cap = rowCount * C.MaxMass;
    let per;
    if (rem >= cap) { per = C.MaxMass; rem -= cap; }
    else { per = rem / rowCount; rem = 0; }
    for (let q = k; q < j; q++) { tgtVals[q] = per; tgt[cavity[q]] = per; }
    surfRow = yRow;
    k = j;
  }
  for (; k < n; k++) { tgtVals[k] = 0; tgt[cavity[k]] = 0; }

  // ---- certificate P_geo = C1 ∧ C3 ∧ C4 (mirror of certificate.js) ----
  // C1: filled region (tgt>0) is a single 4-connected component.
  const filled = [];
  for (let q = 0; q < n; q++) if (tgtVals[q] > 0) filled.push(cavity[q]);
  let C1 = true;
  const vis = grid._fvis;
  if (filled.length > 0) {
    const S2 = ++grid._fvisStamp;
    const st = [filled[0]]; vis[filled[0]] = S2;
    let cnt = 1;
    const inFilled = (nn) => cav[nn] === S && tgt[nn] > 0;
    while (st.length) {
      const c = st.pop();
      const cy = (c / W) | 0, cx = c - cy * W;
      const tryN = (nn) => { if (inFilled(nn) && vis[nn] !== S2) { vis[nn] = S2; st.push(nn); cnt++; } };
      if (cx > 0) tryN(c - 1);
      if (cx < W - 1) tryN(c + 1);
      if (cy > 0) tryN(c - W);
      if (cy < H - 1) tryN(c + W);
    }
    C1 = (cnt === filled.length);
  }
  const C3 = !foreignWater && !truncated;
  // C4: every wet body cell can reach the filled region by a monotone
  // downhill/level path through the cavity (Prop-2 drainage congruence).
  let C4 = true;
  {
    const S3 = ++grid._fvisStamp;
    const q = [];
    for (let z = 0; z < filled.length; z++) { vis[filled[z]] = S3; q.push(filled[z]); }
    let head = 0;
    const inCav = (nn) => cav[nn] === S;
    while (head < q.length) {
      const d = q[head++];
      const dy = (d / W) | 0, dx = d - dy * W;
      const tryN = (nn, ny) => { if (inCav(nn) && vis[nn] !== S3 && ny <= dy) { vis[nn] = S3; q.push(nn); } };
      if (dx > 0) tryN(d - 1, dy);
      if (dx < W - 1) tryN(d + 1, dy);
      if (dy > 0) tryN(d - W, dy - 1);
      if (dy < H - 1) tryN(d + W, dy + 1);
    }
    for (let z = 0; z < body.length; z++) { if (vis[body[z]] !== S3) { C4 = false; break; } }
  }
  const certified = C1 && C3 && C4;

  return { id: newId, cells: body, cavity, tgt: tgtVals, V, top, surfRow, certified, bodyMoved, gen: grid.frame, active: false };
}

// Backward-localization (five.five): when a cached certified body's volume has
// drifted (the O(cavity) volume check fired), NAME the exact cell that carries the
// change -- the cavity cell touched this frame with the largest mass delta. That
// named cell is the `successor_defect`: the witness that the cached body-level
// read-off must be re-derived, and *which* quantity forced it. If no touched
// cavity cell is found (drift with no witness), we count it as an honest
// completeness gap rather than pretend the witness set was complete.
function recordSuccessorDefect(grid, rec) {
  const tstamp = grid._touchStamp, tgen = grid._touchGen, tdelta = grid._delta, W = grid.w;
  let witCell = -1, witDelta = 0;
  for (let q = 0; q < rec.cavity.length; q++) {
    const c = rec.cavity[q];
    if (tstamp[c] === tgen && tdelta[c] > witDelta) { witDelta = tdelta[c]; witCell = c; }
  }
  if (witCell >= 0) {
    grid.bodiesRefloodWitnessed++;
    const y = (witCell / W) | 0, x = witCell - y * W;
    const d = { frame: grid.frame, id: rec.id, x, y, quantity: 'volume',
                delta: Math.round(witDelta * 1000) / 1000 };
    grid.lastDefect = d;
    if (grid._refloodDefects.length < 500) grid._refloodDefects.push(d);
  } else {
    grid.bodiesRefloodUnwitnessed++;
    grid.lastDefect = { frame: grid.frame, id: rec.id, x: -1, y: -1, quantity: 'unwitnessed', delta: 0 };
  }
}

// The cheap non-local solve. Instead of D's global flood every frame, only
// re-flood disturbed/uncertified bodies; reuse cached target levels otherwise.
function relaxLevelsFast(grid, relax, sceneGate, exact) {
  if (relax == null) relax = D.Relax;
  // `exact` (model E): apply the SCENE-WIDE gate uniformly to every body, exactly
  // as model D does. `!exact` (model F): reflooded bodies use a per-body gate and
  // cached bodies relax ungated (the faster-settling behavior variant).
  if (exact == null) exact = false;
  const W = grid.w, type = grid.type, mass = grid.mass;
  const bid = grid._bodyId, records = grid._records;
  const isWater = (i) => type[i] === WATER && mass[i] > C.MinMass;
  // E_exact (`exact`) reproduces D exactly: it re-floods EVERY disturbed/moving
  // body from scratch each frame (like D's global relabel) and skips only settled
  // undisturbed bodies. The certificate-moving-skip and orphan-adoption are cache
  // reuses that D does NOT do, so they are OFF in exact mode and live only in the
  // faster-settling variant F.
  const certGate = !exact && (D.CertGate !== false);
  // Witnessed invalidation (F only): drop the CacheTTL timer and re-flood a
  // certified body ONLY when a witnessed change fires (volume drift localized to a
  // named cell, or an edit). See design/WITNESSED_INVALIDATION.md.
  const witnessed = !exact && (D.Invalidation === 'witnessed');
  // One cavity-claim stamp for the whole frame so bodies reflooded together share
  // first-claim (matches D's within-call semantics for simultaneously-labeled
  // bodies). Cached bodies not reflooded this frame do not re-mark their claims.
  grid._fcavStamp++;

  // E_exact: the ONLY way to be frame-for-frame identical to D is to reproduce D's
  // global relabel exactly — re-flood EVERY awake water cell in strict row-major
  // seed order (D's `forEachActiveRow` scan) so that shared-cavity first-claim is
  // resolved in the same order D uses. The incremental certificate-skip / adoption
  // (which reflood only SOME bodies and reuse the rest off cache) necessarily
  // change that first-claim order on fragmenting/multi-body scenes, so they cannot
  // be exact; they live only in variant F. The only work E_exact skips vs D is
  // fully-asleep chunks — which D skips too via forEachActiveRow — so E_exact is a
  // faithful mirror of D, not a speedup. (See design/TRUST_AUDIT.md, Finding #2.)
  if (exact) {
    records.clear();
    if (grid._editList) grid._editList.length = 0; // full relabel covers all edits
    const seeds = [];
    grid.forEachActiveRow((x0, x1, y) => {
      const base = y * W;
      for (let x = x0; x < x1; x++) { const i = base + x; if (isWater(i)) { bid[i] = -1; seeds.push(i); } }
    });
    for (let s = 0; s < seeds.length; s++) {
      const seed = seeds[s];
      if (bid[seed] !== -1 || !isWater(seed)) continue; // claimed by an earlier flood
      const rec = floodBodyFast(grid, seed, grid._nextId++);
      records.set(rec.id, rec);
      const r = relaxBodyToTarget(grid, rec.id, rec.cavity, rec.tgt, relax * sceneGate);
      rec.active = r.E > D.LevelEps;
      grid.bodiesReflooded++;
    }
    grid.bodiesTotal += grid.bodiesReflooded;
    return;
  }

  // 1. Classify cached bodies from this frame's advection touches.
  const touched = grid._touchList;
  const tstamp = grid._touchStamp, tgen = grid._touchGen;
  const candidates = [];       // -1 water cells to (re)flood from
  const invalidate = (rec) => {
    for (let z = 0; z < rec.cells.length; z++) { const c = rec.cells[z]; if (bid[c] === rec.id) { bid[c] = -1; if (isWater(c)) candidates.push(c); } }
    records.delete(rec.id);
  };
  const Wl = W, Hl = grid.h;
  // If an orphan cell is spread into by exactly one certified body, adopt it into
  // that body instead of re-flooding: advection conserves mass, so the body's
  // volume/target is unchanged (the drift check below re-verifies). Returns the
  // certified neighbour id to adopt into, or -1 if it must (re)flood/merge.
  const adoptInto = (i) => {
    const y = (i / Wl) | 0, x = i - y * Wl;
    let nb = -1, multi = false;
    const chk = (n) => { const bn = bid[n]; if (bn >= 0 && records.has(bn)) { if (nb === -1) nb = bn; else if (nb !== bn) multi = true; } };
    if (x > 0) chk(i - 1);
    if (x < Wl - 1) chk(i + 1);
    if (y > 0) chk(i - Wl);
    if (y < Hl - 1) chk(i + Wl);
    if (!multi && nb !== -1 && records.get(nb).certified) return nb;
    return -1;
  };
  const toInvalidate = new Set();
  const dirtyBodies = new Set();   // certified bodies disturbed this frame (touch/adopt)
  for (let z = 0; z < touched.length; z++) {
    const i = touched[z];
    const b = bid[i];
    const rec = b >= 0 ? records.get(b) : undefined;
    if (isWater(i)) {
      if (rec) {
        // A CERTIFIED body's read-off (V, cavity, target) is invariant under its
        // own internal advection, so surface jitter / sloshing within it does NOT
        // require a re-flood — this is the certificate licensing the skip. Only an
        // UNCERTIFIED body must be re-flooded when its cells move. With the gate
        // OFF, every moving body is re-flooded (pure dirty-tracking baseline).
        if (!rec.certified || !certGate) toInvalidate.add(b);
      } else {
        const adopt = certGate ? adoptInto(i) : -1;
        if (adopt !== -1) { bid[i] = adopt; dirtyBodies.add(adopt); } // internal spread into a certified body
        else candidates.push(i);            // new/orphan/foreign water -> (re)flood/merge
      }
      if (rec && rec.certified) dirtyBodies.add(b); // certified body was disturbed
    } else {
      // Cell drained empty. Re-flood only if the body is not certified (a
      // certified single-equipotential body draining toward its own level does
      // not split; the TTL re-flood + volume-drift check are the backstops).
      if (rec) { if (!rec.certified) { toInvalidate.add(b); bid[i] = -1; } /* else keep label */ }
      else if (b >= 0) bid[i] = -1;
    }
  }
  // External edits (brush paint/erase via grid.set) change a cached body's volume
  // or shape WITHOUT an advection touch. Invalidate the body owning each edited
  // cell AND any 4-neighbour body (so a split, a merge, or a mass-preserving shape
  // change of a SETTLED body is re-flooded), and queue freshly painted orphan
  // water for flooding. This is the direct fix for the settled-cache invalidation
  // hole (see design/TRUST_AUDIT.md, Finding #4).
  const editList = grid._editList;
  if (editList && editList.length) {
    const markBody = (c) => { const b = bid[c]; if (b >= 0 && records.has(b)) toInvalidate.add(b); };
    for (let z = 0; z < editList.length; z++) {
      const i = editList[z];
      markBody(i);
      const y = (i / Wl) | 0, x = i - y * Wl;
      if (x > 0) markBody(i - 1);
      if (x < Wl - 1) markBody(i + 1);
      if (y > 0) markBody(i - Wl);
      if (y < Hl - 1) markBody(i + Wl);
      if (bid[i] === -1 && isWater(i)) candidates.push(i);
    }
    editList.length = 0;
  }
  // Uncertified moving bodies must re-flood every frame (their stale cache can't
  // be trusted). Certified MOVING bodies: the HEURISTIC re-floods them at least
  // every CacheTTL frames as a blind drift backstop; the WITNESSED policy drops
  // that timer entirely and lets them fall through to the per-frame O(cavity)
  // volume witness in phase 3 (re-flood only when a named cell actually changes).
  // Settled/undisturbed bodies need neither guard here.
  for (const rec of records.values()) {
    if (!rec.active) continue;
    if (!rec.certified) { toInvalidate.add(rec.id); continue; }
    if (!witnessed && grid.frame - rec.gen >= D.CacheTTL) { toInvalidate.add(rec.id); grid.bodiesRefloodTimer++; }
  }
  for (const id of toInvalidate) { const rec = records.get(id); if (rec) invalidate(rec); }

  // Discover any UNLABELLED water in an awake chunk (fresh scene / wakeAll /
  // water that appeared without a touch record). Cheap: only scans active cells,
  // exactly like D's seed scan, and only picks cells with no live body.
  grid.forEachActiveRow((x0, x1, y) => {
    const base = y * W;
    for (let x = x0; x < x1; x++) { const i = base + x; if (bid[i] === -1 && isWater(i)) candidates.push(i); }
  });

  // 2. Re-flood every disturbed component, evaluate its certificate, relax it.
  //    `cursor` lets us drain `candidates` even as later phases push more onto it.
  let cursor = 0;
  const floodPending = () => {
    for (; cursor < candidates.length; cursor++) {
      const seed = candidates[cursor];
      if (bid[seed] !== -1 || !isWater(seed)) continue; // already claimed by a prior flood
      const rec = floodBodyFast(grid, seed, grid._nextId++);
      records.set(rec.id, rec);
      // E_exact: the scene-wide gate (matches D). F: a PER-BODY disturbance gate.
      const gate = exact ? sceneGate : 1 / (1 + rec.bodyMoved * D.DisturbScale);
      const r = relaxBodyToTarget(grid, rec.id, rec.cavity, rec.tgt, relax * gate);
      rec.active = r.E > D.LevelEps;
      grid.bodiesReflooded++;
    }
  };
  floodPending();

  // 3. Reuse cache for undisturbed bodies. A certified body's (V, cavity, target)
  //    is invariant under its own motion, so we relax it off the cache with NO
  //    flood — the certificate's "safe while moving" license turned into skipped
  //    work. A cheap volume-drift check over the cached cavity catches any
  //    external inflow/outflow (a stream, a merge, a brush) that WOULD change the
  //    target, and forces a single re-flood in that case (the honest fallback).
  for (const rec of [...records.values()]) {
    if (rec.gen === grid.frame) continue; // freshly reflooded above
    const dirty = dirtyBodies.has(rec.id);
    const settledBackstop = !rec.active && !dirty;
    // A SETTLED body that was not disturbed this frame cannot have changed —
    // skip it in O(1) (no cavity scan, no relax). This is what makes the amortized
    // cost collapse once a scene comes to rest. BUT re-verify its cavity volume at
    // least every CacheTTL frames so an external edit we somehow missed (a brush
    // that neither touched nor bordered a tracked cell) is still caught within
    // CacheTTL — the settled-record backstop (TRUST_AUDIT.md, Finding #4).
    // WITNESSED: a settled undisturbed body cannot change without a touch/edit
    // (which would fire a witness), so skip it in O(1) FOREVER -- no periodic
    // re-verify. HEURISTIC: re-verify its cavity volume every CacheTTL frames on a
    // blind timer even though nothing changed.
    if (settledBackstop && (witnessed || grid.frame - rec.gen < D.CacheTTL)) { grid.bodiesTotal++; grid.bodiesSettledSkipped++; continue; }
    if (settledBackstop) grid.bodiesSettledReverify++; // heuristic timer-driven re-verify
    if (rec.active && !certGate) { invalidate(rec); continue; } // baseline: re-flood all movers
    // Otherwise relax off the cache; the same pass verifies the cavity volume
    // (catches adopted external inflow, a merge, or a brush) and forces a re-flood
    // if it drifted, before trusting the cached target.
    grid.bodiesTotal++;
    // E_exact: relax the cached body with the SAME scene-wide gate D would apply
    // to it this frame (D re-floods and relaxes every body with D.Relax*gate). F:
    // relax ungated (the faster-settling variant).
    const cachedRelax = exact ? relax * sceneGate : relax;
    const r = relaxBodyToTarget(grid, rec.id, rec.cavity, rec.tgt, cachedRelax, rec.V);
    grid.relaxCells += rec.cavity.length;
    if (r.drift) {
      // external change -> reflood. In witnessed mode, NAME the cell that forced
      // it (the successor_defect) before invalidating.
      if (witnessed) recordSuccessorDefect(grid, rec);
      invalidate(rec); continue;
    }
    rec.active = r.E > D.LevelEps;
    if (settledBackstop) rec.gen = grid.frame; // reset TTL clock: clean settled recheck
    grid.bodiesCertSkipped++;
  }
  // Re-flood any bodies whose volume drifted (invalidate() queued their cells).
  floodPending();
  grid.bodiesTotal += grid.bodiesReflooded;
}

function stepWater(grid, model) {
  if (model === 'A') stepA(grid);
  else if (model === 'B') stepB(grid);
  else if (model === 'D') stepD(grid);
  else if (model === 'E') stepE(grid);
  else if (model === 'F') stepF(grid);
  else stepC(grid);
}

// When switching models live, reconcile the two water representations.
function normalizeForModel(grid, model) {
  for (let i = 0; i < grid.type.length; i++) {
    if (grid.type[i] === WATER) {
      if (model === 'C' || model === 'D' || model === 'E' || model === 'F') { if (grid.mass[i] <= 0) grid.mass[i] = C.MaxMass; }
      else { grid.mass[i] = C.MaxMass; grid.vx[i] = 0; grid.vy[i] = 0; }
    }
  }
  // D_fast keeps cross-frame body caches; a wholesale change of representation
  // must invalidate them so stale labels can't leak into the new state.
  if (model === 'E' || model === 'F') resetFastState(grid);
  grid.wakeAll();
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { MODELS, MODEL_NAMES, stepWater, normalizeForModel, stepA, stepB, stepC, stepD, stepE, stepF, relaxLevels, relaxLevelsFast, resetFastState };
}
