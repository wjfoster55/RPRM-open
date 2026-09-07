/* Pure finite presentation transforms. Never evolve, replace, or mutate the model's base. */
(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.RPRMRuleLabPresentation = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";
  const VIEWS = ["A", "B", "XOR", "equality", "AND", "OR", "four-state"];
  const MODES = ["density", "closure", "majority", "parity", "pressure", "residue"];
  const clamp = (x, lo, hi) => Math.min(hi, Math.max(lo, x));
  function integer(x, name, lo, hi) {
    if (!Number.isSafeInteger(x) || x < lo || x > hi) throw new RangeError(name + " must be an integer in [" + lo + ", " + hi + "]");
    return x;
  }
  function viewValue(a, b, mode) {
    switch (mode) {
      case "A": return a;
      case "B": return b;
      case "XOR": return a ^ b;
      case "equality": return Number(a === b);
      case "AND": return a & b;
      case "OR": return a | b;
      case "four-state": return a + 2 * b;
      default: throw new RangeError("Unknown relation view");
    }
  }
  function makeSeed({width, mode, bits = "", density = 35, randomKey = 1}) {
    integer(width, "width", 1, 257);
    const out = new Uint8Array(width), center = Math.floor(width / 2);
    const put = offset => { if (center + offset >= 0 && center + offset < width) out[center + offset] = 1; };
    if (mode === "single") put(0);
    else if (mode === "pair") [0, 1].forEach(put);
    else if (mode === "triplet") [-1, 0, 1].forEach(put);
    else if (mode === "echo") [-21, -7, 0, 7, 21].forEach(put);
    else if (mode === "random") {
      integer(density, "density", 0, 100); integer(randomKey, "random key", 0, 4294967295);
      let word = randomKey;
      const radius = Math.min(Math.floor(width * 0.38), 700);
      for (let i = center - radius; i <= center + radius; i++) {
        word = (Math.imul(1664525, word) + 1013904223) >>> 0;
        out[i] = Number(word / 4294967296 < density / 100);
      }
    } else if (mode === "centered" || mode === "exact") {
      if (typeof bits !== "string" || !/^[01]+$/.test(bits) || bits.length > width || (mode === "exact" && bits.length !== width)) {
        throw new RangeError(mode === "exact" ? "Exact seed must have one binary digit per column" : "Centered seed must contain 1 to width binary digits");
      }
      const start = mode === "exact" ? 0 : center - Math.floor(bits.length / 2);
      for (let i = 0; i < bits.length; i++) out[start + i] = Number(bits[i]);
    } else throw new RangeError("Unknown seed preset");
    return out;
  }
  function maxLevel(width, rows, base) {
    if (![3, 7, 9].includes(base)) throw new RangeError("Block base must be 3, 7, or 9");
    integer(width, "width", 0, 16777216); integer(rows, "rows", 0, 16777216);
    let level = 0, size = 1;
    while (size < Math.max(width, rows)) { size *= base; level++; }
    return level;
  }
  function activeLevel(width, rows, base, scale, automatic, manual) {
    const max = maxLevel(width, rows, base);
    if (!Number.isFinite(scale) || scale <= 0) throw new RangeError("Scale must be positive");
    integer(manual, "manual level", 0, max);
    if (typeof automatic !== "boolean") throw new TypeError("Automatic must be boolean");
    if (!automatic) return manual; // No hidden safety override of an explicitly requested level.
    let level = 0, block = 1;
    while (level < max && scale * block < 0.9) { level++; block *= base; }
    return level;
  }
  function createProjection(pair, grid, mode) {
    if (!VIEWS.includes(mode)) throw new RangeError("Unknown relation view");
    const {width, rows} = pair;
    integer(width, "width", 0, 16777216); integer(rows, "rows", 0, 16777216);
    integer(width * rows, "cells", 0, 16777216);
    for (const data of [pair.A.data, pair.B.data, grid.data]) if (data.length !== width * rows) throw new RangeError("Grid dimensions disagree");
    for (let i = 0; i < grid.data.length; i++) {
      integer(pair.A.data[i], "A bit", 0, 1); integer(pair.B.data[i], "B bit", 0, 1);
      if (grid.data[i] !== viewValue(pair.A.data[i], pair.B.data[i], mode)) throw new RangeError("Relation view does not agree with retained pair");
    }
    const cache = new Map();
    function block(row0, column0, row1, column1) {
      integer(row0, "first row", 0, rows); integer(row1, "last row exclusive", row0, rows);
      integer(column0, "first column", 0, width); integer(column1, "last column exclusive", column0, width);
      let count = 0, countA = 0, countB = 0, edgeSum = 0;
      const histogram = [0, 0, 0, 0], area = (row1 - row0) * (column1 - column0);
      for (let r = row0; r < row1; r++) for (let c = column0; c < column1; c++) {
        const i = r * width + c, value = grid.data[i];
        count += Number(value !== 0); countA += pair.A.data[i]; countB += pair.B.data[i]; histogram[value]++;
        // Legacy edge-pressure receiver: all retained-window neighbors of each block cell.
        // No exterior or wrap edge; an internal differing pair contributes twice.
        if (c > 0 && grid.data[i - 1] !== value) edgeSum++;
        if (c + 1 < width && grid.data[i + 1] !== value) edgeSum++;
        if (r > 0 && grid.data[i - width] !== value) edgeSum++;
        if (r + 1 < rows && grid.data[i + width] !== value) edgeSum++;
      }
      const uniform = area === 0 ? null : histogram.findIndex(n => n === area);
      return Object.freeze({row0, column0, row1, column1, area, count, countA, countB, edgeSum,
        histogram: Object.freeze(histogram), density: area ? count / area : null,
        densityA: area ? countA / area : null, densityB: area ? countB / area : null,
        uniform: uniform === -1 ? null : uniform, pressure: area ? edgeSum / (4 * area) : null});
    }
    function level(base, number) {
      integer(number, "level", 1, maxLevel(width, rows, base));
      const key = base + ":" + number;
      if (!cache.has(key)) {
        const size = base ** number, columns = Math.ceil(width / size), rowCount = Math.ceil(rows / size), blocks = [];
        for (let r = 0; r < rows; r += size) for (let c = 0; c < width; c += size) blocks.push(block(r, c, Math.min(rows, r + size), Math.min(width, c + size)));
        cache.set(key, Object.freeze({base, level: number, size, columns, rows: rowCount, blocks: Object.freeze(blocks)}));
      }
      return cache.get(key);
    }
    return Object.freeze({pair, grid, mode, block, level});
  }
  function summarize(block, mode, fourState, modulus) {
    if (!MODES.includes(mode)) throw new RangeError("Unknown summary");
    if (![3, 7, 9].includes(modulus)) throw new RangeError("Residue modulus must be a block base");
    if (!block.area) return Object.freeze({kind: "empty", values: []});
    if (mode === "closure") return Object.freeze({kind: block.uniform === null ? "mixed" : "uniform", values: block.uniform === null ? [] : [block.uniform]});
    if (mode === "pressure") return Object.freeze({kind: "pressure", values: [block.pressure]});
    const counts = fourState ? [block.countA, block.countB] : [block.count];
    const values = counts.map(count => mode === "density" ? count / block.area
      : mode === "majority" ? Number(2 * count >= block.area)
      : mode === "parity" ? count % 2 : count % modulus);
    return Object.freeze({kind: mode, values: Object.freeze(values)});
  }
  function sample(pair, mode, row, column) {
    if (!VIEWS.includes(mode)) throw new RangeError("Unknown relation view");
    const requestedRow = row, requestedColumn = column;
    if (row < 0 || row >= pair.rows || pair.width === 0) return Object.freeze({requestedRow, requestedColumn, kind: "unretained-time", row: null, column: null, A: null, B: null, value: null});
    let kind = "exact";
    if (column < 0 || column >= pair.width) {
      if (pair.A.metadata.boundary === "zero") return Object.freeze({requestedRow, requestedColumn, kind: "fixed-exterior", row, column: null, A: 0, B: 0, value: viewValue(0, 0, mode)});
      if (pair.A.metadata.boundary !== "periodic") throw new RangeError("Unknown boundary");
      column = ((column % pair.width) + pair.width) % pair.width; kind = "periodic";
    }
    const i = row * pair.width + column, A = pair.A.data[i], B = pair.B.data[i];
    return Object.freeze({requestedRow, requestedColumn, kind, row, column, A, B, value: viewValue(A, B, mode)});
  }
  const LINES = Object.freeze([
    ["Radial NW–C–SE", 0, 4, 8], ["Radial NE–C–SW", 2, 4, 6],
    ["Radial N–C–S", 1, 4, 7], ["Radial W–C–E", 3, 4, 5],
    ["Lateral top", 0, 1, 2], ["Lateral bottom", 6, 7, 8],
    ["Lateral left", 0, 3, 6], ["Lateral right", 2, 5, 8]
  ].map(Object.freeze));
  function residuals(values) {
    if (values.length !== 9 || Array.from(values).some(v => v !== null && !Number.isFinite(v))) throw new RangeError("Supply nine finite values or nulls");
    const lines = LINES.map(([name, a, b, c]) => Object.freeze({name,
      value: [values[a], values[b], values[c]].includes(null) ? null : values[a] - 2 * values[b] + values[c]}));
    const disposition = list => list.some(x => x.value !== null && x.value !== 0) ? "fails" : list.some(x => x.value === null) ? "unknown" : "passes";
    const radial = disposition(lines.slice(0, 4)), lateral = disposition(lines.slice(4));
    const status = radial === "passes" && lateral === "passes" ? "FULL_CHECK_CLOSURE"
      : radial === "passes" && lateral === "fails" ? "COUNTERFEIT_CENTRAL_CLOSURE"
      : radial === "fails" || lateral === "fails" ? "OPEN" : "INCOMPLETE";
    return Object.freeze({lines: Object.freeze(lines), radial, lateral, status});
  }
  function inspect(pair, mode, row, column) {
    integer(row, "row", 0, pair.rows - 1); integer(column, "column", 0, pair.width - 1);
    const cells = [];
    for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) cells.push(sample(pair, mode, row + dr, column + dc));
    const known = cells.filter(cell => cell.value !== null);
    return Object.freeze({cells: Object.freeze(cells), ...residuals(cells.map(cell => cell.value)),
      xorCount: known.reduce((sum, cell) => sum + (cell.A ^ cell.B), 0), knownSlots: known.length});
  }
  function fitCamera(width, rows, viewportWidth, viewportHeight) {
    return {cx: width / 2, cy: rows / 2, scale: clamp(0.94 * Math.min(viewportWidth / Math.max(1, width), viewportHeight / Math.max(1, rows)), 0.002, 64)};
  }
  function worldPoint(camera, x, y, width, height) {
    return {x: camera.cx + (x - width / 2) / camera.scale, y: camera.cy + (y - height / 2) / camera.scale};
  }
  function zoomCamera(camera, factor, x, y, width, height) {
    if (!Number.isFinite(factor) || factor <= 0) throw new RangeError("Zoom factor must be positive");
    const anchor = worldPoint(camera, x, y, width, height), scale = clamp(camera.scale * factor, 0.002, 64);
    return {cx: anchor.x - (x - width / 2) / scale, cy: anchor.y - (y - height / 2) / scale, scale};
  }
  return Object.freeze({version: "presentation/2", VIEWS: Object.freeze(VIEWS), MODES: Object.freeze(MODES),
    viewValue, makeSeed, maxLevel, activeLevel, createProjection, summarize, sample, residuals, inspect, fitCamera, worldPoint, zoomCamera});
});
