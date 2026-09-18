// F3 token-state cycle exact (class E). Frozen F2 oracle.js is not edited.
// Loads the same pinned JS bytes as oracle.js.
// Usage:
//   node oracle_cycle.js <spec.json> <out.json>
// spec: { W,H, walls, mass, monitor, thresh, steps, mode?,
//         snapshotSteps?, maxFall? }
// mode: "cycle_exit" (default) | "full"
//
// cycle_exit stops on monitor YES, R_opt empty, exact token-state
// repeat (occupancy + milli vx,vy + frame parity + dirtyNext), or H.
const fs = require('fs');
const path = require('path');

const f2root = path.join(
  __dirname, '..', '..', 'fluid-f2-review-20260912',
  'input', 'fluid_dynamic_frontier_02',
);
const jsdir = path.join(f2root, 'pinned');
const src = ['constants.js', 'grid.js', 'scenarios.js', 'models.js']
  .map(f => fs.readFileSync(path.join(jsdir, f), 'utf8'))
  .join('\n');

const [specPath, outPath] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));

const driver = `
  const spec = ${JSON.stringify(spec)};
  const W = spec.W, H = spec.H;
  const walls = spec.walls;
  const monitor = spec.monitor;
  const thresh = spec.thresh;
  const steps = spec.steps;
  const mode = spec.mode || 'cycle_exit';
  const maxFall = spec.maxFall || 6;
  const snapSet = new Set(spec.snapshotSteps || []);

  function isWallXY(x, y) {
    if (x < 0 || x >= W || y < 0 || y >= H) return true;
    return !!walls[y * W + x];
  }
  function fallClear(x, y, k) {
    const ny = y + k;
    if (ny < 0 || ny >= H || isWallXY(x, ny)) return false;
    for (let s = 1; s < k; s++) if (isWallXY(x, y + s)) return false;
    return true;
  }
  function reverseROpt() {
    const pred = Array.from({ length: W * H }, () => []);
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        if (isWallXY(x, y)) continue;
        const i = y * W + x;
        for (let k = 1; k <= maxFall; k++) {
          if (!fallClear(x, y, k)) break;
          pred[(y + k) * W + x].push(i);
        }
        const dirs = [[-1,1],[1,1],[-1,0],[1,0]];
        for (const [dx, dy] of dirs) {
          const nx = x + dx, ny = y + dy;
          if (nx < 0 || nx >= W || ny < 0 || ny >= H) continue;
          if (isWallXY(nx, ny)) continue;
          pred[ny * W + nx].push(i);
        }
      }
    }
    const seen = new Uint8Array(W * H);
    const q = [];
    for (const m of monitor) {
      const x = m % W, y = (m / W) | 0;
      if (x < 0 || x >= W || y < 0 || y >= H) continue;
      if (isWallXY(x, y)) continue;
      if (!seen[m]) { seen[m] = 1; q.push(m); }
    }
    let qi = 0;
    while (qi < q.length) {
      const i = q[qi++];
      const ps = pred[i];
      for (let j = 0; j < ps.length; j++) {
        const p = ps[j];
        if (!seen[p]) { seen[p] = 1; q.push(p); }
      }
    }
    return seen;
  }

  function tokenStateKey(g) {
    const parts = [];
    for (let i = 0; i < W * H; i++) {
      if (g.type[i] === WATER) {
        parts.push(
          i + ':' + Math.round(g.vx[i] * 1000) + ':' + Math.round(g.vy[i] * 1000),
        );
      }
    }
    let dirty = '';
    for (let i = 0; i < g.dirtyNext.length; i++) {
      if (g.dirtyNext[i]) dirty += i + ',';
    }
    return (g.frame & 1) + '|' + parts.join(',') + '|' + dirty;
  }

  const grid = new Grid(W, H);
  for (let i = 0; i < W * H; i++) {
    if (walls[i]) { grid.type[i] = WALL; grid.mass[i] = 0; }
    else if (spec.mass[i] > 0) { grid.type[i] = WATER; grid.mass[i] = spec.mass[i]; }
    else { grid.type[i] = EMPTY; grid.mass[i] = 0; }
  }
  normalizeForModel(grid, 'B');
  grid.wakeAll();

  const monMass = (g) => {
    let s = 0;
    for (const c of monitor) if (g.type[c] === WATER) s += g.mass[c];
    return s;
  };
  const waterInROpt = (g, seen) => {
    let s = 0;
    for (let i = 0; i < W * H; i++) {
      if (g.type[i] === WATER && seen[i]) s += g.mass[i];
    }
    return s;
  };

  const t0 = Date.now();
  const series = [];
  const snapshots = [];
  let firstBreach = -1, maxMon = 0, stepsRun = 0, sumActive = 0, sumMoved = 0;
  let graphEvals = 0;
  let stop = 'horizon';
  let cutReason = null;
  const seenKeys = new Set();

  const snap = (s) => {
    const m = new Array(W * H);
    for (let i = 0; i < W * H; i++) {
      m[i] = grid.type[i] === WALL ? -1 : (grid.type[i] === WATER ? Math.round(grid.mass[i] * 1000) / 1000 : 0);
    }
    snapshots.push({ s, m });
  };

  const consider = (s) => {
    const mm = monMass(grid);
    series.push(Math.round(mm * 1000) / 1000);
    if (mm > maxMon) maxMon = mm;
    if (firstBreach < 0 && mm > thresh) firstBreach = s;
    if (snapSet.has(s)) snap(s);
    if (firstBreach >= 0) {
      stop = s === 0 ? 'yes0' : 'yes';
      return true;
    }
    graphEvals += 1;
    const seenR = reverseROpt();
    const w = waterInROpt(grid, seenR);
    if (w <= thresh) {
      stop = s === 0 ? 'no0' : 'no_trapped';
      cutReason = 'R_opt_empty';
      return true;
    }
    if (mode === 'cycle_exit') {
      const k = tokenStateKey(grid);
      if (seenKeys.has(k)) {
        stop = 'occ_cycle';
        cutReason = 'token_state_repeat';
        return true;
      }
      seenKeys.add(k);
    }
    return false;
  };

  if (consider(0)) {
    // decided at t=0
  } else {
    for (let s = 1; s <= steps; s++) {
      grid.beginFrame();
      grid.stepSand();
      stepWater(grid, 'B');
      stepsRun += 1;
      sumActive += grid.activeCells;
      sumMoved += grid.movedCells;
      if (consider(s)) break;
    }
  }

  const result = {
    W, H, model: 'B', mode, steps, thresh, stepsRun,
    Qdyn: firstBreach >= 0 ? 1 : 0,
    firstBreach,
    maxMonitored: Math.round(maxMon * 1000) / 1000,
    finalMonitored: series.length ? series[series.length - 1] : 0,
    totalMass: grid.totalWaterMass(),
    sumActive, sumMoved, graphEvals, stop, cutReason,
    wall_ms: Date.now() - t0,
    tokenStatesSeen: seenKeys.size,
    series: mode === 'full' ? series : undefined,
    snapshots,
  };
  __emit(JSON.stringify(result));
`;

const fn = new Function('__emit', src + '\n' + driver);
fn((json) => fs.writeFileSync(outPath, json));
