// Cheap renderer: one pixel per cell via a single ImageData blit, then scaled
// up by CSS (canvas is grid-sized, style stretches it with nearest-neighbour).

class Renderer {
  constructor(canvas, grid, scale) {
    this.canvas = canvas;
    this.grid = grid;
    this.scale = scale;
    canvas.width = grid.w;
    canvas.height = grid.h;
    canvas.style.width = (grid.w * scale) + 'px';
    canvas.style.height = (grid.h * scale) + 'px';
    canvas.style.imageRendering = 'pixelated';
    this.ctx = canvas.getContext('2d');
    this.img = this.ctx.createImageData(grid.w, grid.h);
    this.data = this.img.data;
    this.showChunks = false;
  }

  draw() {
    const g = this.grid, d = this.data;
    for (let i = 0; i < g.type.length; i++) {
      const t = g.type[i];
      let r, gr, b;
      if (t === EMPTY) { r = 12; gr = 12; b = 18; }
      else if (t === WALL) { r = 90; gr = 92; b = 100; }
      else if (t === SAND) { r = 194; gr = 178; b = 108; }
      else { // water: shade by mass (deeper = darker/bluer)
        const m = Math.max(0.15, Math.min(1.4, g.mass[i]));
        r = Math.floor(40 * (1.4 - m) / 1.4) + 20;
        gr = Math.floor(120 * Math.min(1, m)) + 40;
        b = Math.floor(180 + 55 * Math.min(1, m));
      }
      const p = i * 4;
      d[p] = r; d[p + 1] = gr; d[p + 2] = b; d[p + 3] = 255;
    }

    if (this.showChunks) this._overlayChunks();
    this.ctx.putImageData(this.img, 0, 0);
  }

  _overlayChunks() {
    const g = this.grid, d = this.data;
    for (let cy = 0; cy < g.ch; cy++) {
      for (let cx = 0; cx < g.cw; cx++) {
        if (!g.dirty[cy * g.cw + cx]) continue;
        const x0 = cx * CHUNK, y0 = cy * CHUNK;
        const x1 = Math.min(x0 + CHUNK, g.w), y1 = Math.min(y0 + CHUNK, g.h);
        for (let x = x0; x < x1; x++) { tint(d, g.idx(x, y0)); tint(d, g.idx(x, y1 - 1)); }
        for (let y = y0; y < y1; y++) { tint(d, g.idx(x0, y)); tint(d, g.idx(x1 - 1, y)); }
      }
    }
  }
}

function tint(d, i) { const p = i * 4; d[p] = Math.min(255, d[p] + 60); d[p + 1] = Math.min(255, d[p + 1] + 40); }

if (typeof module !== 'undefined' && module.exports) module.exports = { Renderer };
