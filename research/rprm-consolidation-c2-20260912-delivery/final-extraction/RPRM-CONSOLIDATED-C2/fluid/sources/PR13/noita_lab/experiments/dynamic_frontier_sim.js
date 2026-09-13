// Headless dynamic-rollout bridge for the DYNAMIC-FRONTIER experiment.
//
// Takes a fully specified start state (walls + per-cell mass) and rolls it forward
// under the REAL js/ dynamics (any model A/B/C/D/E/F) for `steps` frames WITH NO
// external inflow, monitoring a declared set of cells each step. It reports the
// dynamic receiver Q_dyn:
//   Q_dyn = "does the water at any monitored cell exceed `thresh` at some step
//            t <= steps (a transient overflow / height breach)?"
// plus the full monitored-mass timeseries and a few state snapshots for figures.
//
// This is the ground-truth oracle for Q_dyn: it is an ACTUAL dynamic rollout of
// the sim's own dynamics, not a summary read-off.
//
// Usage:  node dynamic_frontier_sim.js <spec.json> <out.json>
//   spec.json: { W,H, walls:[0/1 len W*H], mass:[float len W*H], model, steps,
//                monitor:[cell indices], thresh, snapshotSteps:[...] }

const fs = require('fs');
const path = require('path');

const jsdir = path.join(__dirname, '..', 'js');
const src = ['constants.js', 'grid.js', 'scenarios.js', 'models.js']
  .map(f => fs.readFileSync(path.join(jsdir, f), 'utf8'))
  .join('\n');

const [specPath, outPath] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));

const driver = `
  const spec = ${JSON.stringify(spec)};
  const W = spec.W, H = spec.H;
  const model = spec.model;
  const steps = spec.steps;
  const monitor = spec.monitor;             // array of flat cell indices
  const thresh = spec.thresh;               // breach threshold (summed monitored mass)
  const snapSet = new Set(spec.snapshotSteps || []);

  const grid = new Grid(W, H);
  for (let i = 0; i < W * H; i++) {
    if (spec.walls[i]) { grid.type[i] = WALL; grid.mass[i] = 0; }
    else if (spec.mass[i] > 0) { grid.type[i] = WATER; grid.mass[i] = spec.mass[i]; }
    else { grid.type[i] = EMPTY; grid.mass[i] = 0; }
  }
  normalizeForModel(grid, model);
  // Optional initial velocity field (model B): lets a witness differ ONLY in
  // in-flight momentum, with an identical mass field. normalizeForModel zeroes
  // velocity for A/B, so apply AFTER it.
  if (spec.vx) for (let i = 0; i < W * H; i++) if (grid.type[i] === WATER) grid.vx[i] = spec.vx[i];
  if (spec.vy) for (let i = 0; i < W * H; i++) if (grid.type[i] === WATER) grid.vy[i] = spec.vy[i];
  grid.wakeAll();

  const monMass = (g) => { let s = 0; for (const c of monitor) if (g.type[c] === WATER) s += g.mass[c]; return s; };

  const series = [];
  const snapshots = [];
  let firstBreach = -1, maxMon = 0;

  const snap = (s) => {
    const m = new Array(W * H);
    for (let i = 0; i < W * H; i++) m[i] = grid.type[i] === WALL ? -1 : (grid.type[i] === WATER ? Math.round(grid.mass[i] * 1000) / 1000 : 0);
    snapshots.push({ s, m });
  };

  // step 0 (initial)
  let mm = monMass(grid);
  series.push(Math.round(mm * 1000) / 1000);
  if (mm > maxMon) maxMon = mm;
  if (firstBreach < 0 && mm > thresh) firstBreach = 0;
  if (snapSet.has(0)) snap(0);

  for (let s = 1; s <= steps; s++) {
    grid.beginFrame();
    grid.stepSand();
    stepWater(grid, model);
    mm = monMass(grid);
    series.push(Math.round(mm * 1000) / 1000);
    if (mm > maxMon) maxMon = mm;
    if (firstBreach < 0 && mm > thresh) firstBreach = s;
    if (snapSet.has(s)) snap(s);
  }

  const result = {
    W, H, model, steps, thresh,
    Qdyn: firstBreach >= 0 ? 1 : 0,
    firstBreach,
    maxMonitored: Math.round(maxMon * 1000) / 1000,
    finalMonitored: Math.round(mm * 1000) / 1000,
    totalMass: grid.totalWaterMass(),
    series,
    snapshots,
  };
  __emit(JSON.stringify(result));
`;

const fn = new Function('__emit', src + '\n' + driver);
fn((json) => fs.writeFileSync(outPath, json));
