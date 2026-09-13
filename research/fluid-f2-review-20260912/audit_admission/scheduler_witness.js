// Bounded documentation witness. Reads pinned files; does not modify them.
// Run: node research/fluid-f2-review-20260912/audit_admission/scheduler_witness.js
const fs = require('fs');
const path = require('path');
const assert = require('assert');

const pinned = path.resolve(__dirname, '../input/fluid_dynamic_frontier_02/pinned');
const source = ['constants.js', 'grid.js', 'models.js']
  .map(name => fs.readFileSync(path.join(pinned, name), 'utf8')).join('\n');
const run = new Function(source + `
  function fixture() {
    const g = new Grid(16, 5);
    for (let x = 0; x < g.w; x++) {
      g.set(x, 0, WALL); g.set(x, 3, WALL); g.set(x, 4, WALL);
    }
    for (let y = 0; y < g.h; y++) {
      g.set(0, y, WALL); g.set(g.w - 1, y, WALL);
    }
    g.set(6, 2, WALL);
    g.set(7, 2, WATER, 1); g.set(8, 2, WATER, 1);
    normalizeForModel(g, 'B'); g.wakeAll();
    return g;
  }
  const actual = fixture();
  actual.beginFrame();
  const order = [];
  actual.forEachActiveRow((x0, x1, y, ltr) => {
    if (y !== 2) return;
    for (let x = ltr ? x0 : x1 - 1; x !== (ltr ? x1 : x0 - 1); x += ltr ? 1 : -1)
      order.push(x);
  });
  actual.stepSand(); stepWater(actual, 'B');
  const control = fixture();
  // Explicit alternative implementing the prose's whole-row scan direction.
  // It is a comparison control, not the pinned model or a proposed repair.
  control.forEachActiveRow = function(cb) {
    const ltr = (this.frame & 1) === 0;
    for (let y = this.h - 1; y >= 0; y--) cb(0, this.w, y, ltr);
  };
  control.beginFrame(); control.stepSand(); stepWater(control, 'B');
  const water = g => Array.from(g.type, (t, i) => t === WATER ? [i % g.w, (i / g.w) | 0] : null).filter(Boolean);
  return {
    evidence_grade: 'finite executable documentation witness',
    scope: 'normalized binary model-B initial state; one frame; no claimed Q_300 counterexample',
    CHUNK, frame: actual.frame, actual_row_scan: order,
    prose_whole_row_scan: Array.from({length: 16}, (_, i) => 15 - i),
    initial_water: [[7, 2], [8, 2]],
    pinned_after_frame_1: water(actual),
    whole_row_control_after_frame_1: water(control)
  };
`);
const result = run();
assert.strictEqual(result.CHUNK, 8);
assert.deepStrictEqual(result.actual_row_scan, [7, 6, 5, 4, 3, 2, 1, 0, 15, 14, 13, 12, 11, 10, 9, 8]);
assert.deepStrictEqual(result.pinned_after_frame_1, [[7, 2], [9, 2]]);
assert.deepStrictEqual(result.whole_row_control_after_frame_1, [[8, 2], [9, 2]]);
fs.writeFileSync(path.join(__dirname, 'scheduler_witness_result.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result, null, 2));
