// Cache-invalidation mutation tests: model F (D_fast) vs model D (no cache).
//
// Finding #4 of the trust audit: the cross-frame body cache in D_fast skips a
// SETTLED body entirely, so an external edit (brush paint/erase, a scripted
// mutation) that neither produces an advection touch nor borders a tracked cell
// could leave the body's cached (V, cavity, target) stale forever -- the
// "<=CacheTTL refresh" backstop only applied to ACTIVE records.
//
// Contract under test: after ANY edit via grid.set(), model F must converge to
// the SAME hydrostatic equilibrium as model D (which has no cache and is the
// oracle here). We drive both models through the real js/ physics, apply the
// IDENTICAL mutation to both, let both settle, and compare per-column water mass
// (the hydrostatic observable) and total mass.
//
// Usage:  node experiments/test_cache_invalidation.js
//   exit 0 if every mutation converges (F matches D within TOL), else 1.

const fs = require('fs');
const path = require('path');

const jsdir = path.join(__dirname, '..', 'js');
const src = ['constants.js', 'grid.js', 'scenarios.js', 'models.js']
  .map(f => fs.readFileSync(path.join(jsdir, f), 'utf8'))
  .join('\n');

const W = 48, H = 32;
const SETTLE = 900;      // steps to reach equilibrium before and after a mutation
const TOL_COL = 0.75;    // max allowed per-column water-mass mismatch F vs D (the
                         // hydrostatic observable; this is the real contract)
const TOL_MASS = 0.1;    // total-mass mismatch F vs D. F and D reach slightly
                         // different microstates (F is not frame-identical), so a
                         // few sub-MinMass cells evaporate differently -> a tiny
                         // (<0.05%) total-mass delta that is physics noise, not a
                         // stale-cache error (which would strand whole cells).

// Optional CLI arg 'heuristic' restricts to the old policy; default runs both.
const MODES = process.argv.slice(2).includes('heuristic') ? ['heuristic'] : ['heuristic', 'witnessed'];

const driver = `
  const W = ${W}, H = ${H}, SETTLE = ${SETTLE};
  const wall = (g, x0, y0, x1, y1) => { for (let y=y0;y<=y1;y++) for (let x=x0;x<=x1;x++) g.set(x,y,WALL); };
  const water = (g, x0, y0, x1, y1) => { for (let y=y0;y<=y1;y++) for (let x=x0;x<=x1;x++) g.set(x,y,WATER,C.MaxMass); };
  const erase = (g, x0, y0, x1, y1) => { for (let y=y0;y<=y1;y++) for (let x=x0;x<=x1;x++) g.set(x,y,EMPTY); };

  function box(g) {
    wall(g, 0, H-1, W-1, H-1);        // floor
    wall(g, 0, 0, 0, H-1);            // left wall
    wall(g, W-1, 0, W-1, H-1);        // right wall
  }

  const TESTS = {
    // 1. Paint a blob of water on top of a settled pool -> level must rise.
    paint_into_settled: {
      build(g){ box(g); water(g, 2, H-8, W-3, H-2); },
      mutate(g){ water(g, 4, H-16, 12, H-13); },
    },
    // 2. Drop a full-height wall through a settled pool, splitting it into two
    //    basins with DIFFERENT floor widths -> two DIFFERENT levels. A stale
    //    single-body cache would hold one wrong level.
    split_wall: {
      build(g){ box(g); water(g, 2, H-10, W-3, H-2); },
      mutate(g){ wall(g, 20, 2, 21, H-2); },
    },
    // 3. Two settled pools at different levels separated by a wall; erase the
    //    wall so they MERGE -> a single new equilibrium level.
    merge_pools: {
      build(g){ box(g);
        wall(g, 24, H-14, 24, H-2);
        water(g, 2, H-12, 23, H-2);
        water(g, 25, H-6, W-3, H-2);
      },
      mutate(g){ erase(g, 24, H-14, 24, H-2); },
    },
    // 4. Mass-preserving geometry change of a SETTLED body: scoop water from the
    //    right end and place the SAME amount high on the left. New equilibrium.
    mass_preserving_move: {
      build(g){ box(g); water(g, 2, H-7, W-3, H-2); },
      mutate(g){ erase(g, W-9, H-7, W-3, H-2); water(g, 3, H-20, 8, H-16); },
    },
  };

  function settle(g, model, n){ for (let s=0;s<n;s++){ g.beginFrame(); g.stepSand(); stepWater(g, model); } }
  function colMass(g){
    const c = new Float64Array(W);
    for (let y=0;y<H;y++) for (let x=0;x<W;x++){ const i=y*W+x; if (g.type[i]===WATER) c[x]+=g.mass[i]; }
    return Array.from(c);
  }
  function totalMass(g){ let m=0; for (let i=0;i<g.type.length;i++) if (g.type[i]===WATER) m+=g.mass[i]; return m; }

  // Run every mutation under BOTH F cache-invalidation policies (the heuristic
  // CacheTTL+volume-drift guards, and the witnessed successor_defect guards) so we
  // prove the witnessed policy invalidates just as correctly as the heuristic.
  const MODES = ${JSON.stringify(MODES)};
  const out = {};
  for (const mode of MODES) {
    D.Invalidation = mode;
    for (const name of Object.keys(TESTS)) {
      const t = TESTS[name];
      const gd = new Grid(W,H), gf = new Grid(W,H);
      t.build(gd); t.build(gf);
      settle(gd, 'D', SETTLE); settle(gf, 'F', SETTLE);
      t.mutate(gd); t.mutate(gf);
      settle(gd, 'D', SETTLE); settle(gf, 'F', SETTLE);
      const cd = colMass(gd), cf = colMass(gf);
      let maxCol = 0, argx = -1;
      for (let x=0;x<W;x++){ const d=Math.abs(cd[x]-cf[x]); if (d>maxCol){ maxCol=d; argx=x; } }
      out[mode + '/' + name] = { maxCol, argx, massD: totalMass(gd), massF: totalMass(gf) };
    }
  }
  __emit(JSON.stringify(out));
`;

const fn = new Function('__emit', src + '\n' + driver);
let result;
fn((json) => { result = JSON.parse(json); });

let allPass = true;
console.log(`Cache-invalidation mutation tests  (grid ${W}x${H}, settle ${SETTLE} steps; modes: ${MODES.join(', ')})`);
console.log('mode/mutation                     | max per-col |F-D| | @col | massD    | massF    | mass |F-D|');
console.log('-'.repeat(102));
for (const name of Object.keys(result)) {
  const r = result[name];
  const dmass = Math.abs(r.massD - r.massF);
  const pass = r.maxCol <= TOL_COL && dmass <= TOL_MASS;
  allPass = allPass && pass;
  console.log(
    `${name.padEnd(33)} | ${r.maxCol.toFixed(4).padStart(17)} | ${String(r.argx).padStart(4)} | ` +
    `${r.massD.toFixed(3).padStart(8)} | ${r.massF.toFixed(3).padStart(8)} | ${dmass.toExponential(2).padStart(9)}  ${pass ? 'PASS' : 'FAIL'}`);
}
console.log('-'.repeat(92));
console.log(allPass
  ? 'All mutations converge: F matches D after every edit (cache invalidated correctly).'
  : 'FAIL: F diverges from D after a mutation -- stale cache not invalidated.');
process.exit(allPass ? 0 : 1);
