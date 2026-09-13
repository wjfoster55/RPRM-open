// Scenario builders shared by the browser demo (main.js) and the headless
// harness (experiments/run_sim.js), so the demo and the measured experiments
// use identical setups. Coordinates are relative to grid size.

function scBorder(grid) {
  for (let x = 0; x < grid.w; x++) { grid.set(x, 0, WALL); grid.set(x, grid.h - 1, WALL); }
  for (let y = 0; y < grid.h; y++) { grid.set(0, y, WALL); grid.set(grid.w - 1, y, WALL); }
}

// (i) A tall narrow column of water dropped over a wide flat floor.
function scBasin(grid) {
  grid.clear(); scBorder(grid);
  const cx = (grid.w / 2) | 0;
  const hw = Math.max(3, (grid.w * 0.05) | 0);
  const y0 = (grid.h * 0.06) | 0, y1 = (grid.h * 0.5) | 0;
  for (let y = y0; y < y1; y++)
    for (let x = cx - hw; x < cx + hw; x++) grid.set(x, y, WATER);
  grid.wakeAll();
}

// (ii) Connected vessels (U-tube): two narrow vertical shafts joined only by a
// channel at the bottom, solid rock elsewhere. Only the LEFT shaft is filled;
// a model with real pressure equalizes both shaft heights, a binary one can't.
// Shaft geometry (fractions of grid) is mirrored in the Python harness.
const UT = { xLfrac: 0.18, xRfrac: 0.66, swfrac: 0.12, topfrac: 0.08 };
function utubeCols(w) {
  const sw = Math.max(5, (w * UT.swfrac) | 0);
  return { sw, xL: (w * UT.xLfrac) | 0, xR: (w * UT.xRfrac) | 0 };
}
function scUTube(grid) {
  grid.clear(); scBorder(grid);
  const { sw, xL, xR } = utubeCols(grid.w);
  const top = (grid.h * UT.topfrac) | 0;
  const floor = grid.h - 3;      // shafts reach here
  const chan = grid.h - 2;       // single-row connecting pipe at the very bottom
  // Fill the interior with rock, then carve two shafts + a THIN bottom pipe.
  // The thin pipe holds little water, so equalizing forces water UP the shafts
  // (impossible for binary water) rather than just pooling in a wide channel.
  for (let y = top; y < grid.h - 1; y++)
    for (let x = 1; x < grid.w - 1; x++) grid.set(x, y, WALL);
  for (let y = top; y < floor; y++)
    for (let x = xL; x < xL + sw; x++) grid.set(x, y, EMPTY);
  for (let y = top; y < floor; y++)
    for (let x = xR; x < xR + sw; x++) grid.set(x, y, EMPTY);
  for (let y = floor; y <= chan; y++)
    for (let x = xL; x < xR + sw; x++) grid.set(x, y, EMPTY);
  // Fill the left shaft tall. Equilibrium is ~half this height in BOTH shafts.
  const fillH = Math.min(floor - top - 1, (grid.h * 0.55) | 0);
  for (let y = floor - fillH; y < floor; y++)
    for (let x = xL; x < xL + sw; x++) grid.set(x, y, WATER);
  grid.wakeAll();
}

// (iii) Dam-break: a tall block of water on the left collapses to the right.
function scDam(grid) {
  grid.clear(); scBorder(grid);
  const floor = grid.h - 2;
  const x1 = Math.max(8, (grid.w * 0.42) | 0);
  const y0 = (grid.h * 0.05) | 0;
  for (let y = y0; y < floor; y++)
    for (let x = 2; x < x1; x++) grid.set(x, y, WATER);
  grid.wakeAll();
}

// (iv) Multi-body stress scene: a grid of independent walled cells, most of them
// holding a SETTLED pool (its own body + cavity), plus one tall column dropped
// into a few cells so a handful of bodies are actively equalizing while the rest
// are at rest. This is the scene where D_fast should shine: settled bodies are
// cached/skipped and only the disturbed ones pay the flood, and the per-body gate
// keeps the active splashes from throttling the still pools.
function scStress(grid) {
  grid.clear(); scBorder(grid);
  const W = grid.w, H = grid.h;
  // Partition the interior into a grid of cells separated by 1-cell walls.
  const cols = 6, rows = 3;
  const cw = ((W - 2) / cols) | 0;
  const ch = ((H - 2) / rows) | 0;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const x0 = 1 + c * cw, x1 = (c === cols - 1) ? W - 1 : 1 + (c + 1) * cw;
      const y0 = 1 + r * ch, y1 = (r === rows - 1) ? H - 1 : 1 + (r + 1) * ch;
      // Draw right+bottom walls of the cell (interior partitions).
      if (c < cols - 1) for (let y = y0; y < y1; y++) grid.set(x1 - 1, y, WALL);
      if (r < rows - 1) for (let x = x0; x < x1; x++) grid.set(x, y1 - 1, WALL);
    }
  }
  // Fill most cells with a settled pool (~40% depth); leave a few for splashes.
  let idx = 0;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++, idx++) {
      const x0 = 2 + c * cw, x1 = (c === cols - 1) ? W - 2 : c * cw + cw;
      const y0 = 2 + r * ch, y1 = (r === rows - 1) ? H - 2 : r * ch + ch - 1;
      const floor = y1 - 1;
      const active = (idx % 7 === 3); // a few cells get a tall column instead
      if (active) {
        // tall narrow column on the left of the cell -> will slosh to level.
        const cxw = Math.max(2, ((x1 - x0) * 0.28) | 0);
        for (let y = y0; y < floor; y++)
          for (let x = x0; x < x0 + cxw; x++) grid.set(x, y, WATER);
      } else {
        const depth = Math.max(2, ((y1 - y0) * 0.4) | 0);
        for (let y = floor - depth; y < floor; y++)
          for (let x = x0; x < x1; x++) grid.set(x, y, WATER);
      }
    }
  }
  grid.wakeAll();
}

const SCENARIOS = { basin: scBasin, utube: scUTube, dam: scDam, stress: scStress };

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { SCENARIOS, scBasin, scUTube, scDam, scStress, scBorder };
}
