// Headless smoke test for the browser demo: stubs a minimal DOM/canvas so we
// can load ALL demo scripts (including renderer.js + main.js) under node and
// run several frames across every model/scenario, catching runtime errors.
const fs = require('fs');
const path = require('path');

function fakeEl() {
  return new Proxy({
    style: {}, dataset: {}, classList: { add() {}, remove() {}, toggle() {} },
    checked: false, value: '1', textContent: '', innerHTML: '',
    addEventListener() {}, appendChild() {},
    getBoundingClientRect: () => ({ left: 0, top: 0, width: 400, height: 250 }),
    getContext: () => ({
      createImageData: (w, h) => ({ data: new Uint8ClampedArray(w * h * 4), width: w, height: h }),
      putImageData() {},
    }),
  }, { get: (t, k) => (k in t ? t[k] : undefined), set: (t, k, v) => (t[k] = v, true) });
}

let rafCount = 0;
const stubs = {
  document: {
    getElementById: () => fakeEl(),
    querySelectorAll: () => [],
    createElement: () => fakeEl(),
  },
  window: { addEventListener() {} },
  performance: { now: () => Date.now() },
  requestAnimationFrame: (cb) => { if (rafCount++ < 3) setImmediate(() => cb(performance.now())); },
  console,
};

const jsdir = path.join(__dirname, '..', 'js');
const files = ['constants.js', 'grid.js', 'scenarios.js', 'models.js', 'renderer.js', 'main.js'];
const src = files.map(f => fs.readFileSync(path.join(jsdir, f), 'utf8')).join('\n');

// Exercise every model on every scenario for a handful of steps, then draw.
const test = `
  const scs = { basin: scenarioBasin, utube: scenarioUTube, dam: scenarioDamBreak, stress: scenarioStress };
  for (const m of ['A','B','C','D','E','F']) {
    setModel(m);
    for (const [name, fn] of Object.entries(scs)) {
      fn();
      for (let s = 0; s < 40; s++) { grid.beginFrame(); grid.stepSand(); stepWater(grid, m); }
      renderer.draw();
      const mass = grid.totalWaterMass();
      if (!isFinite(mass)) throw new Error('non-finite mass ' + m + '/' + name);
      console.log('  ok', m, name, 'mass', mass.toFixed(0), 'active', grid.activeCells);
    }
  }
  console.log('SMOKE OK');
`;

const fn = new Function(...Object.keys(stubs), src + '\n' + test);
fn(...Object.values(stubs));
