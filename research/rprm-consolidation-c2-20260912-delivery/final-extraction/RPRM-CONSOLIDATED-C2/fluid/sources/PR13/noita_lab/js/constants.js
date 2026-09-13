// Shared constants for the mini-Noita falling-sand / liquid lab.
// Kept in one place so the JS demo and the Python headless harness stay in sync.
// (The Python port in ../experiments mirrors these values.)

// Cell element types (stored in Grid.type as a Uint8).
const EMPTY = 0;
const WALL  = 1; // stone
const SAND  = 2;
const WATER = 3;

// Chunk / dirty-rectangle size. Cells only get simulated if their chunk is
// "awake". A chunk wakes when a cell inside (or next to) it changes.
const CHUNK = 8;

// ---- Model C (mass / level-equalizing water) tuning ----
// Canonical "cellular automaton fluid" constants (down/side/up mass exchange
// with a small compressibility so connected vessels equalize via pressure).
const C = {
  MaxMass: 1.0,       // a normal full cell holds this much water
  MaxCompress: 0.2,   // extra water a cell can hold under pressure from above.
                      // The canonical algorithm uses ~0.02; we found a larger
                      // value equalizes U-tubes far faster AND settles calmer
                      // (see experiments/artifacts/compress_sweep.png).
  MinMass: 1e-5,      // below this a cell is treated as empty (evaporates).
                      // Smaller => less mass lost in violent scenes, but faint
                      // films linger. See the dam-break mass-error in PROBLEMS.
  MinFlow: 0.01,      // flows above this are halved for smoother settling
  MaxSpeed: 1.0,      // cap on mass moved per cell per step (vertical)
  MinFlowCutoff: 5e-3,// deadband: flows below this are zeroed. Kills the
                      // surface limit-cycle jitter so cells can go to sleep,
                      // at the cost of a tiny permanent imbalance (~4x this).
  SleepEps: 3e-3,     // a cell keeps its chunk awake only if its mass moved by
                      // more than this. The retention/economy knob (RPRM tie-in).
};

// ---- Model D (level-aware: mass water + connected-body level field) tuning ----
// D augments C's continuous mass with a NON-LOCAL "change of representation":
// each recompute it labels connected water bodies, reads each body's target
// free-surface level straight off (volume / cavity footprint), and relaxes cells
// toward that target. Level is *read off*, not diffused one cell/frame (the RPRM
// move that fixes PROBLEMS #1). D's local advection is deliberately INCOMPRESSIBLE
// (caps at MaxMass) because the level field — not compressibility — carries pressure.
const D = {
  RelabelEvery: 1,    // recompute the body-level field every k steps. k=1 is exact;
                      // larger amortizes the labeling pass but staleness grows on
                      // fast-moving / splitting / merging bodies (measured in PROBLEMS).
  Relax: 0.5,         // max fraction of each body's mass-to-target gap closed per
                      // relabel step. 1.0 snaps to level instantly (teleporty); <1 flows.
  DisturbScale: 0.02, // disturbance gate: when local advection is actively moving
                      // mass (a dam collapsing / splash), throttle relaxation so
                      // gravity produces the visible motion. Gate = 1/(1+moved*scale).
                      // When local flow stalls (U-tube frozen) the gate -> 1 and the
                      // level field finishes equalizing. This keeps splashes alive.
  LevelEps: 0.5,      // if a body's total |gap| to its target level is below this it
                      // is treated as already level and left asleep (economy knob).
  SideFlow: 0.25,     // local horizontal spread constant (naturalness during splashes)
  MaxSpeed: 1.0,      // cap on mass moved down per cell per step (advection)
  // ---- Model E (D_fast) extra knobs ----
  // D_fast keeps D's exact read-off + relaxation but makes the per-frame cost
  // cheap: it maintains connected-body labels across frames and only re-runs the
  // expensive flood for bodies that were externally disturbed (touched by local
  // advection) or whose RPRM certificate P_geo does NOT hold. A CERTIFIED body
  // that is still moving reuses its cached cavity + target level and just relaxes
  // (no flood) — this is where the sufficiency certificate buys skipped work.
  CacheTTL: 128,      // safety: re-flood a cached body at least this often even if
                      // it looks clean, to bound any drift from a stale cache.
  CertGate: true,     // master switch for the CERTIFICATE-moving-skip. When false,
                      // D_fast degrades to pure dirty-region tracking + quiescence:
                      // a MOVING body is always re-flooded, only settled/undisturbed
                      // bodies are skipped. Used by the harness to isolate exactly
                      // how much the RPRM certificate (the #2->#1 link) actually buys.
  // ---- Cache-invalidation policy for F (D_fast) ----
  // 'heuristic' (default): the original guards -- a fixed CacheTTL timer re-floods
  //   an active certified body every N frames, and settled bodies re-verify their
  //   cavity volume every N frames, whether or not anything changed.
  // 'witnessed': WITNESSED, MINIMAL invalidation grounded in the corpus's
  //   Fold->FutureTest->Five->Refold / successor_defect / backward-localization
  //   (design/RPRM_CORPUS_MAP.md unused-concept #1; RPRM-CORE-FORMALIZATION-01
  //   fold.py successor_defect + five.five). No timer. A certified body's cached
  //   read-off is invariant under its own internal advection, so it is re-flooded
  //   ONLY when a witnessed condition fires -- a named cell/quantity whose change
  //   (external inflow/outflow detected by the O(cavity) volume check, or an edit)
  //   would invalidate it. Every forced re-flood carries the implicated cell (the
  //   successor_defect), and a settled undisturbed body is skipped in O(1) FOREVER
  //   (nothing can change it without touching/editing it, which fires the witness).
  Invalidation: 'heuristic',
};

// ---- Model B (momentum water) tuning ----
const B = {
  gravity: 0.4,       // added to vy each step
  maxV: 6.0,          // terminal velocity (cells/step)
  restitution: 0.25,  // downward speed converted to a splash on impact
  friction: 0.7,      // horizontal velocity decay when it can't move
};

// Given the total water in a vertical bottom+top pair, return how much should
// sit in the BOTTOM cell at equilibrium. This is what lets water build a tiny
// bit of pressure and push connected columns up to the same level.
function stableBottom(total) {
  if (total <= C.MaxMass) return C.MaxMass; // clamped by caller to `total`
  if (total < 2 * C.MaxMass + C.MaxCompress) {
    return (C.MaxMass * C.MaxMass + total * C.MaxCompress) / (C.MaxMass + C.MaxCompress);
  }
  return (total + C.MaxCompress) / 2;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { EMPTY, WALL, SAND, WATER, CHUNK, C, D, B, stableBottom };
}
