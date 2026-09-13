// Headless bridge: takes a geometry+fill spec (produced by the Python harness),
// builds the REAL js/ Grid, and reports model D's instantaneous hydrostatic
// read-off, the RPRM sufficiency certificate P (js/certificate.js), and the
// naive baseline activity probes — all WITHOUT mutating/settling the scene.
//
// Usage:  node certify_sim.js <spec.json> <out.json>
//   spec.json: { W, H, walls:[0/1 len W*H], mass:[float len W*H] }
//   out.json:  { W,H, bodies:[...], pred:[...], mass:[...], baseline:{...} }

const fs = require('fs');
const path = require('path');

const jsdir = path.join(__dirname, '..', 'js');
const src = ['constants.js', 'grid.js', 'scenarios.js', 'models.js', 'certificate.js']
  .map(f => fs.readFileSync(path.join(jsdir, f), 'utf8'))
  .join('\n');

const [specPath, outPath] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));

const driver = `
  const spec = ${JSON.stringify(spec)};
  const W = spec.W, H = spec.H;
  const grid = new Grid(W, H);
  for (let i = 0; i < W * H; i++) {
    if (spec.walls[i]) { grid.type[i] = WALL; grid.mass[i] = 0; }
    else if (spec.mass[i] > 0) { grid.type[i] = WATER; grid.mass[i] = spec.mass[i]; }
    else { grid.type[i] = EMPTY; grid.mass[i] = 0; }
  }
  grid.wakeAll();

  const { bodies, pred, sharedCavityAny } = computeReadoffAndCertificate(grid);
  const probe = localActivityProbe(grid);

  // Trim per-body payload: keep summary + cavity/body cell index lists (needed
  // for per-body pred-vs-truth comparison in Python).
  const outBodies = bodies.map(b => ({
    id: b.id, V: b.V, top: b.top, surfRow: b.surfRow, surfHeight: b.surfHeight,
    nCells: b.nCells, nCavity: b.nCavity, nFilled: b.nFilled,
    C1: b.C1, C2: b.C2, C2strict: b.C2strict, C3: b.C3, C4: b.C4,
    bodyCells: b.bodyCells, cavityCells: b.cavityCells,
  }));

  const result = {
    W, H,
    totalMass: grid.totalWaterMass(),
    sharedCavityAny,
    bodies: outBodies,
    pred: Array.from(pred).map(v => Math.round(v * 1e5) / 1e5),
    mass: Array.from(grid.mass).map(v => Math.round(v * 1e5) / 1e5),
    walls: Array.from(grid.type).map(t => (t === WALL || t === SAND) ? 1 : 0),
    baseline: { movedMass: probe.movedMass, maxFlow: probe.maxFlow, activeWaterCells: probe.activeWaterCells },
  };
  __emit(JSON.stringify(result));
`;

const full = src + '\n' + driver;
const fn = new Function('__emit', full);
fn((json) => fs.writeFileSync(outPath, json));
