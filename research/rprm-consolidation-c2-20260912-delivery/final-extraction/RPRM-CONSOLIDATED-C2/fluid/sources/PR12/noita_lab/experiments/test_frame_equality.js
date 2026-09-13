// Frame-by-frame STATE EQUALITY check: model E (E_exact) vs model D.
//
// E_exact is D_fast with relaxation rules identical to D (one scene-wide gate
// applied to every body, reflooded or cached). This test steps a D grid and an E
// grid in lockstep on each scenario and reports the maximum per-cell mass
// deviation over ALL cells and ALL frames. "Results preserved" requires this to
// stay at floating-point noise, not merely similar final metrics.
//
// It also runs model F (the faster-settling behavior variant) to DEMONSTRATE that
// F genuinely diverges from D — i.e. that the exactness claim is specific to E.
//
// Usage:  node experiments/test_frame_equality.js [steps]
//   exit 0 if every scenario's E-vs-D deviation < TOL, else 1.

const fs = require('fs');
const path = require('path');

const jsdir = path.join(__dirname, '..', 'js');
const src = ['constants.js', 'grid.js', 'scenarios.js', 'models.js']
  .map(f => fs.readFileSync(path.join(jsdir, f), 'utf8'))
  .join('\n');

const STEPS = parseInt(process.argv[2] || '1500', 10);
const W = 100, H = 64;
const SCENARIOS = ['basin', 'utube', 'dam', 'stress'];
const TOL = 1e-9;   // E must match D to floating-point noise

const driver = `
  const W = ${W}, H = ${H}, STEPS = ${STEPS};
  const scenarios = ${JSON.stringify(SCENARIOS)};

  function mkGrid(scenario) {
    const g = new Grid(W, H);
    SCENARIOS[scenario](g);
    return g;
  }
  function stepOnce(g, model) {
    g.beginFrame();
    g.stepSand();
    stepWater(g, model);
  }
  function maxDiff(a, b) {
    let m = 0;
    for (let i = 0; i < a.mass.length; i++) {
      const av = a.type[i] === WATER ? a.mass[i] : 0;
      const bv = b.type[i] === WATER ? b.mass[i] : 0;
      const d = Math.abs(av - bv);
      if (d > m) m = d;
    }
    return m;
  }
  function typeDiff(a, b) {  // count cells whose WATER/!WATER classification differs
    let n = 0;
    for (let i = 0; i < a.type.length; i++) {
      const aw = a.type[i] === WATER, bw = b.type[i] === WATER;
      if (aw !== bw) n++;
    }
    return n;
  }

  const out = {};
  for (const sc of scenarios) {
    // E vs D
    let gd = mkGrid(sc), ge = mkGrid(sc), gf = mkGrid(sc);
    let maxE = 0, maxEframe = -1, maxEtype = 0;
    let maxF = 0;
    for (let s = 1; s <= STEPS; s++) {
      stepOnce(gd, 'D');
      stepOnce(ge, 'E');
      stepOnce(gf, 'F');
      const de = maxDiff(gd, ge);
      if (de > maxE) { maxE = de; maxEframe = s; }
      maxEtype = Math.max(maxEtype, typeDiff(gd, ge));
      const df = maxDiff(gd, gf);
      if (df > maxF) maxF = df;
    }
    out[sc] = { maxE, maxEframe, maxEtype, maxF,
                massD: gd.totalWaterMass(), massE: ge.totalWaterMass(), massF: gf.totalWaterMass() };
  }
  __emit(JSON.stringify(out));
`;

const fn = new Function('__emit', src + '\n' + driver);
let result;
fn((json) => { result = JSON.parse(json); });

let allPass = true;
console.log(`Frame-by-frame state equality  (grid ${W}x${H}, ${STEPS} steps, tol ${TOL})`);
console.log('scenario | max |mass_E - mass_D| | worst frame | E type-mismatch cells | max |mass_F - mass_D| (variant)');
console.log('-'.repeat(96));
for (const sc of SCENARIOS) {
  const r = result[sc];
  const pass = r.maxE < TOL && r.maxEtype === 0;
  allPass = allPass && pass;
  console.log(
    `${sc.padEnd(8)} | ${r.maxE.toExponential(3).padStart(20)} | ${String(r.maxEframe).padStart(11)} | ` +
    `${String(r.maxEtype).padStart(21)} | ${r.maxF.toExponential(3).padStart(12)}  ${pass ? 'PASS' : 'FAIL'}`);
}
console.log('-'.repeat(96));
console.log(allPass
  ? 'E_exact is frame-identical to D (deviation at float noise). F diverges, as expected.'
  : 'E_exact DIVERGES from D — see failing scenario above.');
process.exit(allPass ? 0 : 1);
