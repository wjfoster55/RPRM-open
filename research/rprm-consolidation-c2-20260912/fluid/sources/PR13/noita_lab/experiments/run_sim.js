// Headless driver: runs the REAL browser physics (js/*.js) under node so the
// measured experiments and the interactive demo share one implementation.
//
// Usage:
//   node run_sim.js <scenario> <model> <steps> <W> <H> <frameEvery> <out.json>
//
// Emits JSON: { meta, steps:[{m,a,mv}], frames:[{s,t,m}] }
//   m = total water mass, a = active cells, mv = cells changed
//   frames: t = type string (len W*H), m = per-cell mass (rounded)

const fs = require('fs');
const path = require('path');

const jsdir = path.join(__dirname, '..', 'js');
const src = ['constants.js', 'grid.js', 'scenarios.js', 'models.js']
  .map(f => fs.readFileSync(path.join(jsdir, f), 'utf8'))
  .join('\n');

const [scenario, model, stepsS, wS, hS, feS, out, overridesS] = process.argv.slice(2);
const steps = +stepsS, W = +wS, H = +hS, frameEvery = +feS;
const overrides = overridesS ? JSON.parse(overridesS) : {}; // e.g. {"C":{"MaxCompress":0.25}}

const driver = `
  const grid = new Grid(${W}, ${H});
  const __ov = ${JSON.stringify(overrides)};
  if (__ov.C) Object.assign(C, __ov.C);
  if (__ov.B) Object.assign(B, __ov.B);
  if (__ov.D) Object.assign(D, __ov.D);
  SCENARIOS[${JSON.stringify(scenario)}](grid);
  const perStep = [];
  const frames = [];
  function snapshot(s) {
    let t = '';
    const m = new Array(grid.type.length);
    for (let i = 0; i < grid.type.length; i++) { t += grid.type[i]; m[i] = Math.round(grid.mass[i] * 100) / 100; }
    frames.push({ s, t, m });
  }
  snapshot(0);
  for (let s = 1; s <= ${steps}; s++) {
    const __t0 = process.hrtime.bigint();
    grid.beginFrame();
    grid.stepSand();
    stepWater(grid, ${JSON.stringify(model)});
    const __dtus = Number(process.hrtime.bigint() - __t0) / 1000; // microseconds
    perStep.push({ m: grid.totalWaterMass(), a: grid.activeCells, mv: grid.movedCells,
                   lc: grid.labelCells || 0, lp: grid.labelPasses || 0,
                   rc: grid.relaxCells || 0,
                   bt: grid.bodiesTotal || 0, brf: grid.bodiesReflooded || 0,
                   bcs: grid.bodiesCertSkipped || 0, bss: grid.bodiesSettledSkipped || 0,
                   rt: grid.bodiesRefloodTimer || 0, sr: grid.bodiesSettledReverify || 0,
                   rw: grid.bodiesRefloodWitnessed || 0, ru: grid.bodiesRefloodUnwitnessed || 0,
                   dt: __dtus });
    // Dense early sampling (fast action happens first) + sparse later. The very
    // dense first-80 window lets model D's fast level equalization be visible.
    if (s % ${frameEvery} === 0 || (s <= 80 && s % 4 === 0) || (s <= 800 && s % 25 === 0) || s === ${steps}) snapshot(s);
  }
  const result = { meta: { scenario: ${JSON.stringify(scenario)}, model: ${JSON.stringify(model)}, W: ${W}, H: ${H}, steps: ${steps}, frameEvery: ${frameEvery},
                           invalidation: (typeof D !== 'undefined' ? D.Invalidation : null),
                           refloodDefects: (grid._refloodDefects || []).slice(0, 40),
                           refloodDefectCount: (grid._refloodDefects || []).length },
                   steps: perStep, frames };
  __emit(JSON.stringify(result));
`;

const full = src + '\n' + driver;
const fn = new Function('__emit', full);
fn((json) => fs.writeFileSync(out, json));
console.error(`[run_sim] ${scenario}/${model} ${W}x${H} x${steps} -> ${out}`);
