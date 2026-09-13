// Grid: cell storage + the active-cell / dirty-rectangle scheme + sand physics.
// Water physics lives in models.js so the three liquid models can be swapped.

class Grid {
  constructor(w, h) {
    this.w = w;
    this.h = h;
    this.type = new Uint8Array(w * h);      // element id per cell
    this.mass = new Float32Array(w * h);     // water amount (model C); 0/1 for A/B
    this.newMass = new Float32Array(w * h);  // double buffer for model C
    this.vx = new Float32Array(w * h);       // model B velocity
    this.vy = new Float32Array(w * h);
    this.stamp = new Int32Array(w * h).fill(-1); // "already moved this frame" marker

    // Chunk grid for dirty rectangles.
    this.cw = Math.ceil(w / CHUNK);
    this.ch = Math.ceil(h / CHUNK);
    this.dirty = new Uint8Array(this.cw * this.ch);      // awake this frame
    this.dirtyNext = new Uint8Array(this.cw * this.ch);  // awake next frame
    this.halo = new Uint8Array(this.cw * this.ch);       // dirty + neighbours

    // Per-frame bookkeeping surfaced in the UI.
    this.activeCells = 0;   // cells actually visited this frame
    this.movedCells = 0;    // cells that changed this frame

    // Alternate horizontal scan direction each frame to cancel L/R bias.
    this.frame = 0;
  }

  idx(x, y) { return y * this.w + x; }
  inBounds(x, y) { return x >= 0 && x < this.w && y >= 0 && y < this.h; }

  // Wake the chunk containing (x,y) and its 8 neighbours so cross-boundary
  // interactions propagate. Cheap: just sets bytes.
  wake(x, y) {
    const cx = (x / CHUNK) | 0;
    const cy = (y / CHUNK) | 0;
    for (let j = cy - 1; j <= cy + 1; j++) {
      if (j < 0 || j >= this.ch) continue;
      for (let i = cx - 1; i <= cx + 1; i++) {
        if (i < 0 || i >= this.cw) continue;
        this.dirtyNext[j * this.cw + i] = 1;
      }
    }
  }

  wakeAll() { this.dirtyNext.fill(1); this.dirty.fill(1); }

  set(x, y, t, mass) {
    if (!this.inBounds(x, y)) return;
    const i = this.idx(x, y);
    this.type[i] = t;
    if (t === WATER) this.mass[i] = (mass == null ? C.MaxMass : mass);
    else this.mass[i] = 0;
    if (t !== WATER) { this.vx[i] = 0; this.vy[i] = 0; }
    this.wake(x, y);
    // Cross-frame body cache (model F / D_fast): an external edit here (brush
    // paint/erase, scripted mutation) can change a cached body's volume or shape
    // WITHOUT producing an advection touch, so waking the chunk alone is not
    // enough — a settled body would be skipped and keep its stale target. Record
    // the edited cell so the level solve can invalidate the owning/adjacent body
    // cache and re-flood it. (No-op for the model-agnostic models that never build
    // the cache.)
    if (this._editList) this._editList.push(i);
    else if (this._bodyId) this._editList = [i];
  }

  clear() {
    this.type.fill(EMPTY);
    this.mass.fill(0);
    this.newMass.fill(0);
    this.vx.fill(0);
    this.vy.fill(0);
    this.dirty.fill(0);
    this.dirtyNext.fill(0);
  }

  totalWaterMass() {
    let s = 0;
    for (let i = 0; i < this.mass.length; i++) if (this.type[i] === WATER) s += this.mass[i];
    return s;
  }

  // Begin a frame: promote dirtyNext -> dirty, reset counters, and count the
  // cells that are eligible for simulation this step (awake-chunk area). This
  // is the honest cost proxy: idle regions sleep and contribute ~0.
  beginFrame() {
    const tmp = this.dirty;
    this.dirty = this.dirtyNext;
    this.dirtyNext = tmp;
    this.dirtyNext.fill(0);
    this.movedCells = 0;
    this.frame++;
    let active = 0;
    for (let cy = 0; cy < this.ch; cy++) {
      const rows = Math.min(CHUNK, this.h - cy * CHUNK);
      for (let cx = 0; cx < this.cw; cx++) {
        if (!this.dirty[cy * this.cw + cx]) continue;
        active += rows * Math.min(CHUNK, this.w - cx * CHUNK);
      }
    }
    this.activeCells = active;
  }

  // Chunk-level dilation of `dirty` into `halo`. Used by the mass model so that
  // cells RECEIVING flow from an active cell (always within one chunk) are also
  // copied/committed — otherwise flow into a sleeping neighbour would be lost.
  computeHalo() {
    this.halo.fill(0);
    for (let cy = 0; cy < this.ch; cy++)
      for (let cx = 0; cx < this.cw; cx++) {
        if (!this.dirty[cy * this.cw + cx]) continue;
        for (let j = cy - 1; j <= cy + 1; j++) {
          if (j < 0 || j >= this.ch) continue;
          for (let i = cx - 1; i <= cx + 1; i++) {
            if (i < 0 || i >= this.cw) continue;
            this.halo[j * this.cw + i] = 1;
          }
        }
      }
  }

  // Iterate the halo (dirty + neighbour chunks), bottom-to-top.
  forEachHaloRow(cb) {
    for (let cy = this.ch - 1; cy >= 0; cy--) {
      const y0 = cy * CHUNK;
      const y1 = Math.min(y0 + CHUNK, this.h);
      for (let y = y1 - 1; y >= y0; y--) {
        for (let cx = 0; cx < this.cw; cx++) {
          if (!this.halo[cy * this.cw + cx]) continue;
          const x0 = cx * CHUNK;
          cb(x0, Math.min(x0 + CHUNK, this.w), y);
        }
      }
    }
  }

  // Iterate awake chunks bottom-to-top (gravity friendly), yielding cell ranges.
  // cb(x0,x1,y) is called per awake row span. leftToRight alternates per frame.
  forEachActiveRow(cb) {
    const leftToRight = (this.frame & 1) === 0;
    for (let cy = this.ch - 1; cy >= 0; cy--) {
      const y0 = cy * CHUNK;
      const y1 = Math.min(y0 + CHUNK, this.h);
      for (let y = y1 - 1; y >= y0; y--) {
        for (let cx = 0; cx < this.cw; cx++) {
          if (!this.dirty[cy * this.cw + cx]) continue;
          const x0 = cx * CHUNK;
          const x1 = Math.min(x0 + CHUNK, this.w);
          cb(x0, x1, y, leftToRight);
        }
      }
    }
  }

  // --- Sand physics (secondary element). Sand falls and piles at ~45 deg,
  // and sinks through water (denser), giving simple buoyancy. ---
  stepSand() {
    const dir = (this.frame & 1) === 0 ? 1 : -1;
    this.forEachActiveRow((x0, x1, y) => {
      const xs = dir === 1 ? x0 : x1 - 1;
      const xe = dir === 1 ? x1 : x0 - 1;
      for (let x = xs; x !== xe; x += dir) {
        const i = this.idx(x, y);
        if (this.type[i] !== SAND) continue;
        if (y + 1 >= this.h) continue;
        // down (into empty or water -> swap: sand sinks)
        if (this.trySandMove(x, y, x, y + 1)) continue;
        // down-diagonals, order depends on scan dir to reduce bias
        const first = dir === 1 ? x - 1 : x + 1;
        const second = dir === 1 ? x + 1 : x - 1;
        if (this.trySandMove(x, y, first, y + 1)) continue;
        if (this.trySandMove(x, y, second, y + 1)) continue;
      }
    });
  }

  trySandMove(x, y, nx, ny) {
    if (!this.inBounds(nx, ny)) return false;
    const i = this.idx(x, y);
    const j = this.idx(nx, ny);
    const tj = this.type[j];
    if (tj === EMPTY) {
      this.type[j] = SAND; this.type[i] = EMPTY;
      this.wake(x, y); this.wake(nx, ny); this.movedCells++;
      return true;
    }
    if (tj === WATER) {
      // swap: sand sinks, water rises
      this.type[j] = SAND;
      this.type[i] = WATER;
      this.mass[i] = this.mass[j] > 0 ? this.mass[j] : C.MaxMass;
      this.mass[j] = 0;
      this.vx[i] = 0; this.vy[i] = 0;
      this.wake(x, y); this.wake(nx, ny); this.movedCells++;
      return true;
    }
    return false;
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { Grid };
}
