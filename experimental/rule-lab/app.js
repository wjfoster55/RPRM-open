/* Presentation only; the independently checked model and all base buffers remain unchanged. */
"use strict";
(function () {
  const M = globalThis.RPRMRuleLab, P = globalThis.RPRMRuleLabPresentation;
  const $ = id => document.getElementById(id), number = id => $(id).valueAsNumber;
  const outcomes = ["TN: correctly nonprime", "FP: false prime", "FN: missed prime", "TP: matched prime"];
  const comparisonColors = ["#263340", "#ed9c84", "#e5c565", "#86dcb9"];
  const palettes = {
    midnight: ["#121820", "#96e3c1", "#eab181", "#a8baff", "#db92db"],
    paper: ["#f5f2e9", "#12584a", "#aa4717", "#414ea0", "#9c2576"],
    ember: ["#1b1316", "#ffc17b", "#a7c9ff", "#f6e9cf", "#ff819d"],
    neon: ["#121426", "#77f5c4", "#fcba65", "#b2b0ff", "#f78ddb"]
  };
  let state = null, camera = {cx: 0, cy: 0, scale: 6}, pending = false, frame = 0, drag = null;
  const percent = value => value === null ? "undefined (empty denominator)" : (100 * value).toFixed(2) + "%";
  const fmt = value => Number.isInteger(value) ? String(value) : Number(value).toFixed(4);
  const report = text => { $("status").textContent = text; };
  function markPending() {
    pending = true;
    report("Settings changed. Generate to apply them; displayed results and exports retain the generated experiment.");
  }
  function configureSeed() {
    const mode = $("seed-mode").value;
    $("seed").disabled = mode !== "centered" && mode !== "exact";
    $("random-density").disabled = $("random-key").disabled = mode !== "random";
  }
  function ruleB(a) {
    switch ($("transform").value) {
      case "mirror": return M.mirrorRule(a);
      case "same": return a;
      case "complement": return M.outputComplementRule(a);
      case "conjugate": return M.conjugateRule(a);
      default: return number("rule-b");
    }
  }
  function regenerateView(candidate) {
    const view = M.relationView(candidate.pair, candidate.viewMode);
    const comparison = M.comparePrimes(view, {addressMap: "row-major", start: candidate.start, positiveValues: candidate.positiveValues});
    const projection = P.createProjection(candidate.pair, view, candidate.viewMode);
    Object.assign(candidate, {view, comparison, projection});
  }
  function generate() {
    if (!$("setup").reportValidity()) return;
    try {
      const seedRequest = {width: number("width"), mode: $("seed-mode").value, bits: $("seed").value.trim(), density: number("random-density"), randomKey: number("random-key")};
      const seedA = P.makeSeed(seedRequest), relation = $("seed-b").value;
      const seedB = relation === "mirror" ? M.mirrorSeed(seedA) : relation === "complement" ? M.complementSeed(seedA) : seedA;
      const a = number("rule-a"), b = ruleB(a);
      const input = {ruleA: a, ruleB: b, seedA: Array.from(seedA), seedB: Array.from(seedB), rows: number("rows"), boundary: $("boundary").value};
      const positive = $("positive").value;
      const candidate = {pair: M.generatePair(input), input, seedRequest, seedRelation: relation,
        start: number("start"), positiveValues: positive === "nonzero" ? [1, 2, 3] : [Number(positive)], viewMode: $("view").value};
      regenerateView(candidate); // Publish one complete candidate only after every calculation succeeds.
      state = candidate; pending = false;
      $("inspect-row").max = String(input.rows - 1); $("inspect-column").max = String(seedA.length - 1);
      $("inspect-row").value = String(Math.max(0, Math.min(number("inspect-row") || 0, input.rows - 1)));
      $("inspect-column").value = String(Math.max(0, Math.min(number("inspect-column") || 0, seedA.length - 1)));
      $("result-title").textContent = "Rule " + a + " × Rule " + b;
      $("result-meta").textContent = seedA.length + " columns · " + input.rows + " rows · " + input.boundary + " boundary · " + state.view.data.length.toLocaleString() + " exact cells";
      const table = M.ruleTable(a);
      $("rules").textContent = "Neighborhood  " + table.map(x => x.neighborhood).join(" ") + "\nRule A        " + table.map(x => " " + x.output + " ").join(" ") + "\nRule B        " + M.ruleTable(b).map(x => " " + x.output + " ").join(" ") + "\nIndex = 4×left + 2×center + right; output is that bit of the rule.";
      $("exact-seeds").textContent = "Seed A: " + input.seedA.join("") + "\nSeed B: " + input.seedB.join("");
      report("Generated. Results and exports refer to these explicit seeds, rules, boundary and address settings.");
      fit(); render();
    } catch (error) { report(error.message + ". Previous results, if any, remain displayed."); }
  }
  function changeView() {
    if (!state) return;
    try {
      const candidate = {...state, viewMode: $("view").value};
      regenerateView(candidate); state = candidate; render();
    } catch (error) { $("view").value = state.viewMode; report(error.message); }
  }
  function render() {
    if (!state) return;
    const c = state.comparison, counts = c.counts;
    $("predicate").textContent = "View: " + state.viewMode + ". Predict prime when value ∈ {" + state.positiveValues.join(", ") + "}. Address range " + c.metadata.first + "–" + c.metadata.last + ". Counts always use every exact base cell.";
    $("counts").replaceChildren();
    [["TP", "Matched primes", 3], ["FP", "False positives", 1], ["FN", "Missed primes", 2], ["TN", "Correct nonprimes", 0]].forEach(([key, label, color]) => {
      const box = document.createElement("div"), n = document.createElement("strong"), l = document.createElement("span");
      box.className = "stat"; box.style.borderColor = comparisonColors[color]; n.textContent = counts[key].toLocaleString(); l.textContent = label;
      box.append(n, l); $("counts").append(box);
    });
    $("metrics").textContent = "Precision " + percent(c.metrics.precision) + " · Recall " + percent(c.metrics.recall) + " · Specificity " + percent(c.metrics.specificity) + " · F1 " + percent(c.metrics.f1) + " · Accuracy " + percent(c.metrics.accuracy) + " · Always-nonprime baseline " + percent(counts.total ? (counts.TN + counts.FP) / counts.total : null);
    inspect(); scheduleDraw();
  }
  function dimensions() {
    const canvas = $("grid");
    return {width: Math.max(1, canvas.clientWidth), height: Math.max(1, canvas.clientHeight)};
  }
  function fit() {
    if (!state) return;
    const {width, height} = dimensions();
    camera = P.fitCamera(state.pair.width, state.pair.rows, width, height); scheduleDraw();
  }
  function center() { if (state) { camera.cx = state.pair.width / 2; camera.cy = state.pair.rows / 2; scheduleDraw(); } }
  function levelInfo() {
    const base = Number($("block-base").value), max = state ? P.maxLevel(state.pair.width, state.pair.rows, base) : 0;
    $("manual-level").max = String(max);
    const manual = Math.max(0, Math.min(max, Math.trunc(number("manual-level") || 0)));
    $("manual-level").value = String(manual);
    const relation = $("display").value === "relation";
    $("manual-level").disabled = $("auto-level").checked || !relation;
    $("summary").disabled = $("auto-level").disabled = $("block-base").disabled = !relation;
    const level = !state || !relation ? 0 : P.activeLevel(state.pair.width, state.pair.rows, base, camera.scale, $("auto-level").checked, manual);
    return {base, level, size: base ** level, max, relation};
  }
  function mix(a, b, ratio) {
    const bytes = hex => [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16));
    const aa = bytes(a), bb = bytes(b);
    return "rgb(" + aa.map((v, i) => Math.round(v + (bb[i] - v) * ratio)).join(",") + ")";
  }
  function blockColor(block, info, colors) {
    const mode = $("summary").value, four = state.viewMode === "four-state", s = P.summarize(block, mode, four, info.base);
    if (s.kind === "uniform") return colors[s.values[0]];
    if (s.kind === "mixed") return colors[4];
    if (mode === "pressure") return mix(colors[0], colors[4], s.values[0]);
    const values = mode === "residue" ? s.values.map(x => x / (info.base - 1)) : s.values;
    if (!four) return mix(colors[0], colors[1], values[0]);
    // Bilinear palette map: four corner colors recover the exact four-state legend.
    const [a, b] = values;
    const channels = colors.slice(0, 4).map(hex => [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16)));
    return "rgb(" + [0, 1, 2].map(i => Math.round(channels[0][i] * (1 - a) * (1 - b) + channels[1][i] * a * (1 - b) + channels[2][i] * (1 - a) * b + channels[3][i] * a * b)).join(",") + ")";
  }
  function scheduleDraw() { if (!frame) frame = requestAnimationFrame(() => { frame = 0; draw(); }); }
  function draw() {
    if (!state) return;
    const canvas = $("grid"), {width, height} = dimensions(), dpr = Math.min(2, window.devicePixelRatio || 1);
    const w = Math.round(width * dpr), h = Math.round(height * dpr);
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
    const context = canvas.getContext("2d");
    if (!context) { report("Canvas is unavailable. Exact cells and summaries remain available in the textual inspector and exports."); return; }
    context.setTransform(dpr, 0, 0, dpr, 0, 0); context.imageSmoothingEnabled = false;
    context.fillStyle = "#101720"; context.fillRect(0, 0, width, height);
    const info = levelInfo(), colors = palettes[$("palette").value], mode = $("display").value;
    const data = mode === "comparison" ? state.comparison.outcomes : mode === "truth" ? state.comparison.truth : state.view.data;
    const cellColors = mode === "comparison" ? comparisonColors : colors;
    const left = width / 2 - camera.cx * camera.scale, top = height / 2 - camera.cy * camera.scale;
    const paint = (r0, c0, r1, c1, color) => {
      const x = left + c0 * camera.scale, y = top + r0 * camera.scale, bw = (c1 - c0) * camera.scale, bh = (r1 - r0) * camera.scale;
      if (x >= width || y >= height || x + bw <= 0 || y + bh <= 0) return;
      context.fillStyle = color; context.fillRect(x, y, bw, bh);
      if ($("block-lines").checked && Math.min(bw, bh) >= 6) { context.strokeStyle = "#6b7d90"; context.lineWidth = 0.5; context.strokeRect(x, y, bw, bh); }
    };
    if (info.level === 0) {
      const c0 = Math.max(0, Math.floor(-left / camera.scale)), c1 = Math.min(state.pair.width, Math.ceil((width - left) / camera.scale));
      const r0 = Math.max(0, Math.floor(-top / camera.scale)), r1 = Math.min(state.pair.rows, Math.ceil((height - top) / camera.scale));
      for (let r = r0; r < r1; r++) for (let c = c0; c < c1; c++) paint(r, c, r + 1, c + 1, cellColors[data[r * state.pair.width + c]]);
    } else for (const block of state.projection.level(info.base, info.level).blocks) paint(block.row0, block.column0, block.row1, block.column1, blockColor(block, info, colors));
    const r = number("inspect-row"), c = number("inspect-column");
    if (Number.isInteger(r) && Number.isInteger(c)) {
      context.strokeStyle = "#ffffff"; context.lineWidth = 2;
      context.strokeRect(left + c * camera.scale, top + r * camera.scale, Math.max(1, camera.scale), Math.max(1, camera.scale));
    }
    $("scale").value = String(Number(camera.scale.toPrecision(5)));
    $("hierarchy-status").textContent = "Active level " + info.level + "/" + info.max + " · block " + info.size + " × " + info.size + " · " + camera.scale.toFixed(3) + " CSS px/base cell. " + (!info.relation ? "Prime display uses exact cells; relation summaries are paused." : info.level ? "Partial right/bottom blocks use their actual retained area. Exact base cells remain stored." : "Exact cell colors; selected summary begins at level 1.");
    legend(info, colors); inspectBlock(info);
  }
  function legend(info, colors) {
    const mode = $("display").value;
    const labels = mode === "comparison" ? outcomes : mode === "truth" ? ["0: nonprime", "1: prime"]
      : state.viewMode === "four-state" ? ["0: neither", "1: A only", "2: B only", "3: both"] : ["0", "1"];
    $("legend").replaceChildren();
    labels.forEach((label, i) => {
      const swatch = document.createElement("span"); swatch.className = "swatch"; swatch.style.background = mode === "comparison" ? comparisonColors[i] : colors[i]; swatch.setAttribute("aria-hidden", "true");
      $("legend").append(swatch, document.createTextNode(label + " "));
    });
    if (info.level) $("legend").append(document.createTextNode(" · " + $("summary").selectedOptions[0].textContent + ": intermediate colors encode the declared numeric summary, not an exact source code. Mixed closure blocks use the open color."));
  }
  function appendRow(body, values, selected) {
    const tr = document.createElement("tr"); if (selected) tr.className = "selected";
    for (const value of values) { const td = document.createElement("td"); td.textContent = String(value); tr.append(td); } body.append(tr);
  }
  function inspectBlock(info = levelInfo()) {
    if (!state) return;
    const r = number("inspect-row"), c = number("inspect-column");
    if (!Number.isInteger(r) || !Number.isInteger(c) || r < 0 || c < 0 || r >= state.pair.rows || c >= state.pair.width) return;
    const r0 = Math.floor(r / info.size) * info.size, c0 = Math.floor(c / info.size) * info.size;
    const b = state.projection.block(r0, c0, Math.min(state.pair.rows, r0 + info.size), Math.min(state.pair.width, c0 + info.size));
    $("block-description").textContent = "Relation block containing selected exact cell: rows " + b.row0 + "–" + (b.row1 - 1) + ", columns " + b.column0 + "–" + (b.column1 - 1) + "; " + b.area + " retained cells. Occupied " + b.count + "; A ones " + b.countA + "; B ones " + b.countB + "; code histogram [0,1,2,3] = [" + b.histogram.join(", ") + "].";
    $("block-summaries").replaceChildren();
    for (const mode of P.MODES) {
      const summary = P.summarize(b, mode, state.viewMode === "four-state", info.base);
      const value = summary.kind === "mixed" ? "MIXED (not uniform)" : summary.kind === "uniform" ? "UNIFORM code " + summary.values[0] : summary.values.map(fmt).join(" / ");
      appendRow($("block-summaries"), [mode === "residue" ? "count residue mod " + info.base : mode, value], mode === $("summary").value);
    }
  }
  function inspect() {
    if (!state || !$("inspect-form").checkValidity()) return;
    const row = number("inspect-row"), column = number("inspect-column");
    const result = P.inspect(state.pair, state.viewMode, row, column), idx = row * state.pair.width + column;
    $("selection").textContent = "Exact center (" + row + ", " + column + ") · address " + (state.start + idx) + " · " + outcomes[state.comparison.outcomes[idx]] + ". Diagnostics use relation " + state.viewMode + ", regardless of the drawing overlay.";
    $("cells").replaceChildren();
    const directions = ["NW", "N", "NE", "W", "C", "E", "SW", "S", "SE"];
    result.cells.forEach((cell, i) => {
      const hasAddress = cell.kind === "exact" || cell.kind === "periodic";
      const index = hasAddress ? cell.row * state.pair.width + cell.column : null, n = hasAddress ? state.start + index : null;
      const prime = hasAddress ? state.comparison.truth[index] : null;
      const classification = !hasAddress ? "No integer address" : prime ? "Prime" : n < 2 ? "Nonprime (0 or 1)" : "Composite; factor " + state.comparison.certificate.smallestFactor[n];
      appendRow($("cells"), [directions[i], cell.requestedRow + ", " + cell.requestedColumn, cell.kind + (cell.kind === "periodic" ? " → " + cell.row + ", " + cell.column : ""), n ?? "—", cell.A ?? "?", cell.B ?? "?", cell.value ?? "?", classification, hasAddress ? outcomes[state.comparison.outcomes[index]] : "—"], i === 4);
    });
    $("residuals").replaceChildren();
    result.lines.forEach(line => appendRow($("residuals"), [line.name, line.value === null ? "UNKNOWN: unretained time" : (line.value > 0 ? "+" : "") + line.value, line.value === null ? "unknown" : line.value === 0 ? "passes" : "fails"]));
    $("closure-status").textContent = result.status.replaceAll("_", " ") + ". Radial " + result.radial + "; lateral " + result.lateral + ".";
    $("closure-status").className = "diagnostic " + (result.status === "FULL_CHECK_CLOSURE" ? "pass" : "warn");
    const centerCell = result.cells[4], previous = P.sample(state.pair, state.viewMode, row - 1, column);
    $("differences").textContent = "Center relation: " + ["neither", "A only", "B only", "both"][centerCell.A + 2 * centerCell.B] + ". Time changes A/B: " + (previous.A === null ? "unknown before seed" : (centerCell.A - previous.A) + " / " + (centerCell.B - previous.B)) + ". Local XOR: " + result.xorCount + " / " + result.knownSlots + " known aperture slots (wrapped repeats count as separate slots).";
    $("update-check").replaceChildren();
    for (const name of ["A", "B"]) {
      const parents = [-1, 0, 1].map(dc => P.sample(state.pair, state.viewMode, row - 1, column + dc)[name]);
      const observed = centerCell[name], rule = state.input[name === "A" ? "ruleA" : "ruleB"];
      appendRow($("update-check"), [name, rule, parents.includes(null) ? "unretained before seed" : parents.join(""), parents.includes(null) ? "not an update row" : M.ruleOutput(rule, ...parents), observed]);
    }
    inspectBlock(); scheduleDraw();
  }
  function zoom(factor, x, y) {
    const {width, height} = dimensions(); camera = P.zoomCamera(camera, factor, x ?? width / 2, y ?? height / 2, width, height); scheduleDraw();
  }
  function pan(dx, dy) { camera.cx += dx / camera.scale; camera.cy += dy / camera.scale; scheduleDraw(); }
  function selectAt(x, y) {
    if (!state) return;
    const {width, height} = dimensions(), point = P.worldPoint(camera, x, y, width, height);
    const row = Math.floor(point.y), column = Math.floor(point.x);
    if (row < 0 || column < 0 || row >= state.pair.rows || column >= state.pair.width) return;
    $("inspect-row").value = String(row); $("inspect-column").value = String(column); inspect();
  }
  function presentationSettings() {
    const info = levelInfo();
    return {version: P.version, display: $("display").value, palette: $("palette").value, summary: $("summary").value,
      blockBase: info.base, automatic: $("auto-level").checked, manualLevel: number("manual-level"), activeLevel: info.level,
      camera: {...camera}, viewportCSS: dimensions(), gridLines: $("block-lines").checked,
      selected: {row: number("inspect-row"), column: number("inspect-column")},
      summaryContract: "Relation only; origin-aligned clipped base^level squares; direct exact-base counts; ties go to 1; residue modulo block base; pressure uses retained-window orthogonal differing incidences/(4*area); no exterior/wrap edges",
      apertureContract: "Eight arithmetic second differences of relation codes; spatial boundary from model, exterior A=B=0, unretained time unknown; separate from CA update law"};
  }
  function settingsPayload() {
    return {schema: "rprm-rule-lab-settings/v2", modelVersion: M.version, modelInput: state.input,
      seedConstruction: {...state.seedRequest, BRelation: state.seedRelation, randomAlgorithm: "uint32 LCG: word=(1664525*word+1013904223) mod 2^32; sample=word/2^32"},
      viewMode: state.viewMode, comparison: {addressMap: "row-major", start: state.start, positiveValues: state.positiveValues},
      presentation: presentationSettings(), pendingFormChangesExcluded: pending};
  }
  function downloadBlob(blob, filename) {
    try {
      if (!blob) throw new Error("The browser did not create an export blob");
      const url = URL.createObjectURL(blob), link = document.createElement("a"); link.href = url; link.download = filename;
      document.body.append(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 30000);
      $("export-status").textContent = "Download requested: " + filename + ". Browser completion is not observable here.";
    } catch (error) { $("export-status").textContent = "Export unavailable: " + error.message; }
  }
  const downloadJSON = (value, name) => downloadBlob(new Blob([JSON.stringify(value, null, 2) + "\n"], {type: "application/json"}), name);
  $("setup").addEventListener("submit", event => { event.preventDefault(); generate(); });
  $("setup").addEventListener("input", markPending);
  $("seed-mode").addEventListener("change", configureSeed);
  $("transform").addEventListener("change", () => { $("rule-b").disabled = $("transform").value !== "custom"; });
  $("rule-preset").addEventListener("change", () => {
    if (!$("rule-preset").value) return;
    $("rule-a").value = "30"; $("transform").value = $("rule-preset").value === "mirror" ? "mirror" : "custom";
    $("rule-b").value = $("rule-preset").value === "mirror" ? "86" : "83"; $("rule-b").disabled = $("transform").value !== "custom"; markPending();
  });
  $("view").addEventListener("change", changeView);
  for (const id of ["display", "palette", "summary", "block-base", "auto-level", "manual-level", "block-lines"]) $(id).addEventListener("change", scheduleDraw);
  $("scale").addEventListener("change", () => { if ($("scale").reportValidity()) { camera.scale = number("scale"); scheduleDraw(); } });
  $("fit").addEventListener("click", fit); $("center").addEventListener("click", center);
  $("zoom-in").addEventListener("click", () => zoom(1.5)); $("zoom-out").addEventListener("click", () => zoom(1 / 1.5));
  document.querySelectorAll("[data-pan]").forEach(button => button.addEventListener("click", () => pan(...button.dataset.pan.split(",").map(Number))));
  $("inspect-form").addEventListener("submit", event => { event.preventDefault(); inspect(); });
  const canvas = $("grid");
  canvas.addEventListener("wheel", event => {
    if (!event.ctrlKey) return; // Keep ordinary page scrolling and browser magnification elsewhere.
    event.preventDefault(); const rect = canvas.getBoundingClientRect();
    zoom(Math.exp(Math.max(-1, Math.min(1, -event.deltaY * 0.002))), event.clientX - rect.left, event.clientY - rect.top);
  }, {passive: false});
  if ("PointerEvent" in window && "setPointerCapture" in canvas) {
    canvas.addEventListener("pointerdown", event => {
      if (!event.isPrimary || event.button !== 0) return;
      canvas.focus(); drag = {id: event.pointerId, x: event.clientX, y: event.clientY, startX: event.clientX, startY: event.clientY, moved: false}; canvas.setPointerCapture(event.pointerId);
    });
    canvas.addEventListener("pointermove", event => {
      if (!drag || event.pointerId !== drag.id) return;
      if (Math.hypot(event.clientX - drag.startX, event.clientY - drag.startY) > 4) drag.moved = true;
      if (drag.moved) pan(drag.x - event.clientX, drag.y - event.clientY);
      drag.x = event.clientX; drag.y = event.clientY;
    });
    canvas.addEventListener("pointerup", event => {
      if (!drag || event.pointerId !== drag.id) return;
      const moved = drag.moved; drag = null;
      if (canvas.hasPointerCapture(event.pointerId)) canvas.releasePointerCapture(event.pointerId);
      if (!moved) { const rect = canvas.getBoundingClientRect(); selectAt(event.clientX - rect.left, event.clientY - rect.top); }
    });
    for (const name of ["pointercancel", "lostpointercapture"]) canvas.addEventListener(name, () => { drag = null; });
  } else canvas.addEventListener("click", event => { const rect = canvas.getBoundingClientRect(); selectAt(event.clientX - rect.left, event.clientY - rect.top); });
  canvas.addEventListener("keydown", event => {
    if (event.ctrlKey || event.altKey || event.metaKey) return;
    const keys = {ArrowLeft: [-80, 0], ArrowRight: [80, 0], ArrowUp: [0, -80], ArrowDown: [0, 80]};
    if (keys[event.key]) { event.preventDefault(); pan(...keys[event.key]); }
    else if (event.key === "+" || event.key === "=") { event.preventDefault(); zoom(1.5); }
    else if (event.key === "-") { event.preventDefault(); zoom(1 / 1.5); }
    else if (event.key.toLowerCase() === "f") fit();
    else if (event.key.toLowerCase() === "c") center();
    else if (event.key.toLowerCase() === "g") $("setup").requestSubmit();
    else if (/^[0-7]$/.test(event.key)) { $("auto-level").checked = false; $("manual-level").value = event.key; scheduleDraw(); }
  });
  if ("ResizeObserver" in window) new ResizeObserver(scheduleDraw).observe(canvas);
  else window.addEventListener("resize", scheduleDraw);
  $("download").addEventListener("click", () => {
    if (!state) return;
    downloadJSON({...settingsPayload(), schema: "rprm-rule-lab-experiment/v2", pair: state.pair.metadata, width: state.pair.width, rows: state.pair.rows,
      A: Array.from(state.pair.A.data), B: Array.from(state.pair.B.data), view: {mode: state.viewMode, data: Array.from(state.view.data)},
      comparisonCertificate: state.comparison.metadata, counts: state.comparison.counts, metrics: state.comparison.metrics,
      truth: Array.from(state.comparison.truth), outcomes: Array.from(state.comparison.outcomes)}, "rprm-rule-lab-experiment.json");
  });
  $("download-settings").addEventListener("click", () => { if (state) downloadJSON(settingsPayload(), "rprm-rule-lab-settings.json"); });
  $("copy-settings").addEventListener("click", async () => {
    if (!state) return;
    const text = JSON.stringify(settingsPayload(), null, 2); $("settings-text").value = text;
    try {
      if (!navigator.clipboard?.writeText) throw new Error("Clipboard API unavailable");
      await navigator.clipboard.writeText(text); $("export-status").textContent = "Generated settings copied.";
    } catch (_) { $("settings-text").focus(); $("settings-text").select(); $("export-status").textContent = "Settings are selected below. Use your browser's Copy command; clipboard access was unavailable."; }
  });
  $("download-png").addEventListener("click", () => {
    if (!state) return;
    try {
      draw();
      if (!canvas.getContext("2d") || typeof canvas.toBlob !== "function") throw new Error("PNG export is unavailable");
      canvas.toBlob(blob => downloadBlob(blob, "rprm-rule-lab-viewport.png"), "image/png");
    } catch (error) { $("export-status").textContent = error.message; }
  });
  const notesKey = "rprm-rule-lab-presentation-v2-notes";
  try { $("notes").value = localStorage.getItem(notesKey) || ""; }
  catch (_) { $("notes-status").textContent = "Local storage unavailable. Notes stay in this page; download a copy before closing."; }
  $("notes").addEventListener("input", () => { $("notes-status").textContent = "Unsaved notes. Save locally or download a copy."; });
  $("save-notes").addEventListener("click", () => {
    try { localStorage.setItem(notesKey, $("notes").value); $("notes-status").textContent = "Saved in this browser context. Local-file persistence can vary; download a portable copy if needed."; }
    catch (_) { $("notes-status").textContent = "Local storage unavailable. Notes remain in the text field and can be downloaded."; }
  });
  $("download-notes").addEventListener("click", () => downloadBlob(new Blob([$("notes").value], {type: "text/plain;charset=utf-8"}), "rule-lab-notes.txt"));
  configureSeed(); generate();
})();
