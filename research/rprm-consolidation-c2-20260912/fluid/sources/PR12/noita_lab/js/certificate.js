// RPRM sufficiency certificate P for model D's hydrostatic read-off.
//
// Receiver question R_static: "what is the resting free-surface level of this
// connected water body?" Model D answers it instantaneously from the summary
//   C_body = (body water volume V, containing-cavity geometry)
// by filling the cavity bottom-up with V (see models.js `relaxLevels`).
//
// P(body) is a cheaply-checkable predicate that certifies C_body is a SUFFICIENT
// statistic for R_static right now, i.e. that D's instantaneous read-off equals
// the true resting level. It is derived from the two factorization theorems of
// RPRM's Process Mechanics paper (MANUSCRIPT.md §3.1 Prop 1, §3.2 Prop 2). See
// design/SUFFICIENCY_TEST.md for the derivation. This module ONLY inspects the
// grid; it never mutates it, so it can be run as an oracle in the harness.
//
// It reproduces D's exact body+cavity flood + bottom-up fill (relaxLevels) so the
// certificate is judging D's real computation, then evaluates the conditions:
//   C1 (Prop 1, single equipotential): the read-off wetted region is ONE
//       4-connected component under a single free surface.
//   C2 (Prop 2, descent stability):    no water is perched strictly above the
//       read-off surface (body top row == read-off surface row), so the cavity
//       the fill used is invariant as the surface settles.
//   C3 (Prop 2, partition congruence): the body's cavity contains no water from
//       a different body and is not shared/first-claimed by another body (no
//       pending merge / no shared-cavity mis-allocation).
// P = C1 && C2 && C3 is the headline certificate; the harness also measures the
// weaker variants (C1&&C3 etc.) to find what actually drives false positives to 0.

function computeReadoffAndCertificate(grid) {
  const W = grid.w, H = grid.h, type = grid.type, mass = grid.mass;
  const N = W * H;
  const isWater = (i) => type[i] === WATER && mass[i] > C.MinMass;
  const isSolid = (i) => type[i] === WALL || type[i] === SAND;

  const label = new Int32Array(N).fill(-1);   // body id per water cell
  const claim = new Int32Array(N).fill(-1);   // which body first-claimed a cavity cell
  const pred = new Float32Array(N);           // D's predicted resting mass per cell
  const bodies = [];
  let sharedCavityAny = false;

  const stack = [];
  for (let start = 0; start < N; start++) {
    if (!isWater(start) || label[start] !== -1) continue;
    const id = bodies.length;

    // 1. Flood the connected water body (4-connectivity through water).
    const body = [];
    let top = H;
    stack.length = 0; stack.push(start); label[start] = id;
    while (stack.length) {
      const c = stack.pop();
      body.push(c);
      const cy = (c / W) | 0, cx = c - cy * W;
      if (cy < top) top = cy;
      if (cx > 0)     { const n = c - 1; if (label[n] === -1 && isWater(n)) { label[n] = id; stack.push(n); } }
      if (cx < W - 1) { const n = c + 1; if (label[n] === -1 && isWater(n)) { label[n] = id; stack.push(n); } }
      if (cy > 0)     { const n = c - W; if (label[n] === -1 && isWater(n)) { label[n] = id; stack.push(n); } }
      if (cy < H - 1) { const n = c + W; if (label[n] === -1 && isWater(n)) { label[n] = id; stack.push(n); } }
    }

    // 2. Flood the containing cavity (air+water, walls block), bounded above by
    //    `top` — EXACTLY as D does in relaxLevels, INCLUDING first-claim: cells
    //    already claimed by an earlier body's cavity are NOT re-entered (this is
    //    the source of D's shared-cavity mis-allocation, PROBLEMS #1* mode 3). We
    //    replicate it faithfully so `pred` conserves mass and matches D's output.
    const cavity = [];
    let V = 0;
    let foreignWater = false;         // cavity touches another body's water (C3)
    let truncated = false;            // cavity flood blocked by another body's claim (C3)
    stack.length = 0;
    for (let k = 0; k < body.length; k++) {
      const c = body[k];
      if (claim[c] === -1) { claim[c] = id; stack.push(c); }
      else if (claim[c] !== id) { truncated = true; }   // our own water pre-claimed
    }
    while (stack.length) {
      const c = stack.pop();
      cavity.push(c);
      const cy = (c / W) | 0, cx = c - cy * W;
      if (type[c] === WATER) V += mass[c];
      if (isWater(c) && label[c] !== -1 && label[c] !== id) foreignWater = true;
      const pushN = (n, okRow) => {
        if (!okRow || isSolid(n)) return;
        if (claim[n] === -1) { claim[n] = id; stack.push(n); }
        else if (claim[n] !== id) { truncated = true; }
      };
      if (cx > 0)     pushN(c - 1, cy >= top);
      if (cx < W - 1) pushN(c + 1, cy >= top);
      if (cy > 0)     pushN(c - W, cy - 1 >= top);
      if (cy < H - 1) pushN(c + W, true);
    }

    // 3. Read the target level straight off: fill the cavity bottom-up with V.
    cavity.sort((a, b) => b - a);
    const n = cavity.length;
    const tgt = new Float32Array(n);
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
      for (let q = k; q < j; q++) { tgt[q] = per; pred[cavity[q]] += per; }
      surfRow = yRow;   // last (highest) filled row
      k = j;
    }

    // ---- Certificate conditions -------------------------------------------
    // C1 (Prop 1): the filled region (tgt>0) is a single 4-connected component.
    const filled = [];
    const filledSet = new Set();
    for (let q = 0; q < n; q++) if (tgt[q] > 0) { filled.push(cavity[q]); filledSet.add(cavity[q]); }
    let C1 = true;
    if (filled.length > 0) {
      const seen2 = new Set();
      const st = [filled[0]]; seen2.add(filled[0]);
      while (st.length) {
        const c = st.pop();
        const cy = (c / W) | 0, cx = c - cy * W;
        const tryN = (nn) => { if (filledSet.has(nn) && !seen2.has(nn)) { seen2.add(nn); st.push(nn); } };
        if (cx > 0) tryN(c - 1);
        if (cx < W - 1) tryN(c + 1);
        if (cy > 0) tryN(c - W);
        if (cy < H - 1) tryN(c + W);
      }
      C1 = (seen2.size === filled.length);
    }

    // C2 (Prop 2): no water perched above the read-off surface (top == surfRow).
    // If top is strictly above surfRow, the cavity was flooded with an inflated
    // upper bound, so its sideways extent (hence footprint) may not be invariant
    // as the surface settles — the summary can change under the settling op.
    const C2 = (surfRow === -1) ? true : (top >= surfRow);
    // (top is the min row index of body; surfRow is the highest filled row index;
    //  top <= surfRow always. top === surfRow means no perched water.)
    const C2strict = (surfRow === -1) ? true : (top === surfRow);

    // C3 (Prop 2): cavity holds no foreign water and was not truncated by another
    // body's claim (first-claim conflict => shared cavity / pending merge).
    const C3 = !foreignWater && !truncated;
    if (truncated || foreignWater) sharedCavityAny = true;

    // C4 (Prop 2, drainage congruence): every currently-wet cell of the body can
    // reach the read-off wetted region F by a monotone downhill/level path. If
    // some water is trapped above a lip (a local basin the global bottom-up fill
    // would wrongly drain), reject. This is the cheap catch for the trapped-
    // pocket / spill failure that C1 and C3 cannot see. BFS from F to higher-or-
    // equal cavity cells (a cell can drain to F iff it is reached this way).
    let C4 = true;
    {
      const cavSet = new Set(cavity);
      const drain = new Set();
      const q = [];
      for (const c of filled) { drain.add(c); q.push(c); }
      let head = 0;
      while (head < q.length) {
        const d = q[head++];
        const dy = (d / W) | 0, dx = d - dy * W;
        const tryN = (nn, ny) => {
          if (!cavSet.has(nn) || drain.has(nn)) return;
          if (ny <= dy) { drain.add(nn); q.push(nn); }   // nn higher-or-equal -> drains into d
        };
        if (dx > 0) tryN(d - 1, dy);
        if (dx < W - 1) tryN(d + 1, dy);
        if (dy > 0) tryN(d - W, dy - 1);
        if (dy < H - 1) tryN(d + W, dy + 1);
      }
      for (const c of body) { if (!drain.has(c)) { C4 = false; break; } }
    }

    // continuous read-off surface height (cells from the grid bottom).
    let surfHeight = 0;
    if (surfRow !== -1) {
      // fraction of the partial (top) row that is filled
      let partial = 1.0;
      for (let q = 0; q < n; q++) if (((cavity[q] / W) | 0) === surfRow) { partial = tgt[q] / C.MaxMass; break; }
      surfHeight = (H - surfRow - 1) + partial;
    }

    bodies.push({
      id, V, top, surfRow, surfHeight,
      nCells: body.length, nCavity: n, nFilled: filled.length,
      C1, C2, C2strict, C3, C4,
      bodyCells: body, cavityCells: cavity.slice(),
    });
  }

  return { bodies, pred, sharedCavityAny, W, H };
}

// A single local-advection probe step (model D's incompressible down+spread) used
// ONLY to measure the naive baselines (how much water would move next step, and
// the max local flow magnitude). It runs on a scratch copy so it does not mutate
// the real grid. Returns { movedMass, maxFlow, activeWaterCells } scene-wide and
// per body (indexed by the label grid we recompute here).
function localActivityProbe(grid) {
  const W = grid.w, H = grid.h, type = grid.type, mass = grid.mass;
  const N = W * H;
  const isSolid = (x, y) => {
    if (x < 0 || x >= W || y < 0 || y >= H) return true;
    const t = type[y * W + x];
    return t === WALL || t === SAND;
  };
  let movedMass = 0, maxFlow = 0, activeWaterCells = 0;
  // per-cell activity so the harness can aggregate per body if it wants.
  const cellActive = new Uint8Array(N);
  const nm = new Float32Array(N);
  for (let i = 0; i < N; i++) nm[i] = mass[i];
  for (let y = H - 1; y >= 0; y--) {
    for (let x = 0; x < W; x++) {
      const i = y * W + x;
      if (type[i] === WALL || type[i] === SAND) continue;
      let remaining = mass[i];
      if (remaining <= 0) continue;
      let flow;
      if (!isSolid(x, y + 1)) {
        const j = (y + 1) * W + x;
        flow = Math.max(0, Math.min(C.MaxMass - mass[j], Math.min(D.MaxSpeed, remaining)));
        if (flow >= C.MinFlowCutoff) { movedMass += flow; if (flow > maxFlow) maxFlow = flow; if (flow > C.MinFlowCutoff) { cellActive[i] = 1; } remaining -= flow; }
      }
      if (remaining > 0 && !isSolid(x - 1, y)) {
        const j = y * W + (x - 1);
        flow = (mass[i] - mass[j]) * D.SideFlow;
        if (flow > C.MinFlowCutoff) { movedMass += flow; if (flow > maxFlow) maxFlow = flow; cellActive[i] = 1; remaining -= flow; }
      }
      if (remaining > 0 && !isSolid(x + 1, y)) {
        const j = y * W + (x + 1);
        flow = (mass[i] - mass[j]) * D.SideFlow;
        if (flow > C.MinFlowCutoff) { movedMass += flow; if (flow > maxFlow) maxFlow = flow; cellActive[i] = 1; remaining -= flow; }
      }
    }
  }
  for (let i = 0; i < N; i++) if (cellActive[i]) activeWaterCells++;
  return { movedMass, maxFlow, activeWaterCells, cellActive };
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { computeReadoffAndCertificate, localActivityProbe };
}
