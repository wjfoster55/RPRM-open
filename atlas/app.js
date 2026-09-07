/* Local presentation of the admitted mechanism laws. Canvas samples are display
   records, not exact roots, physical parts, or continuous-time certificates. */
(() => {
  "use strict";
  const K = globalThis.MMAKernel;
  const E = globalThis.MMAMathExport;
  const $ = id => document.getElementById(id);
  const TAU = Math.PI * 2;
  const SCHEMA = "rprm-motion-workspace/v1";
  const GRAPH_SCHEMA = "rprm-motion-graph/v1";
  const COLORS = ["#197b68", "#b95a35", "#496ac2", "#987227", "#9c4f87", "#247d92", "#707625", "#915240"];
  const DARK_COLORS = ["#72d9ba", "#ffa87c", "#a6b8ff", "#e8c66b", "#e9a0d3", "#8fd5ea", "#c8d488", "#e6b7a1"];
  const FAMILY = { transport: "Carry phase", ratio: "Gears & ratios", convert: "Convert motion", gate: "Gates & dwells", accumulate: "Accumulate travel" };
  const SPANS = [.5, 1, 2, 4, 8, 16];
  const SHIFTS = [0, .25, .5, .75];
  const PRESETS = { paths: ["chebyshev", "rack", "one-way"], joints: ["cv", "universal"], gears: ["bevel", "gearbox", "worm"], linkages: ["slider", "scotch", "chebyshev"], gates: ["oscillator", "offset", "cam", "intermittent"] };
  const eventChannels = new Set(["oscillator", "one-way", "cam", "offset", "intermittent"]);
  let state, records = [], frameHandle = 0, lastFrame = null, lastReadout = 0;
  const models = K ? K.mechanisms : [];
  const byId = new Map(models.map(m => [m.id, m]));
  const definitions = K ? K.definitions() : [];
  const defs = new Map(definitions.map(d => [d.id, d]));
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  const dark = matchMedia("(prefers-color-scheme: dark)");
  const number = value => typeof value === "number" && Number.isFinite(value);
  const valueText = value => Array.isArray(value) ? "(" + value.map(valueText).join(", ") + ")" : number(value) ? Math.abs(value) < 1e-12 ? "0" : Number(value.toPrecision(7)).toString() : "OPEN";
  const color = id => (dark.matches ? DARK_COLORS : COLORS)[models.findIndex(m => m.id === id) % COLORS.length];
  function element(tag, text, className) { const e = document.createElement(tag); if (text !== undefined) e.textContent = text; if (className) e.className = className; return e; }
  function status(text, error = false) { $("status").textContent = text; $("status").classList.toggle("error", error); }
  function safe(action) { try { return action(); } catch (error) { pause(); status(error.message || String(error), true); return null; } }
  function button(text, action, className) { const b = element("button", text, className); b.type = "button"; b.addEventListener("click", () => safe(action)); return b; }
  function option(value, text) { const o = element("option", text); o.value = value; return o; }
  function layer(id) { return state.layers.find(x => x.id === id); }
  function modelName(id) { return byId.get(id)?.short || byId.get(id)?.name || defs.get(id)?.name || id; }
  function nodeInputs(def) { return def?.inputPorts?.length ? def.inputPorts : def?.inPort ? [{ name: "in", type: def.inPort }] : []; }
  function node(id, componentId, aperture = .45) { return { id, componentId, name: modelName(componentId), aperture }; }
  function freshEdgeId() { const used = new Set(state.graph.edges.map(e => e.id)); let id = 1; while (used.has("e" + id)) id++; return "e" + id; }
  function graphPreset(name) {
    if (name === "carry") return { schema: GRAPH_SCHEMA, intervalTurns: [0, state.span], nodes: [node("n1", "digit-clock"), node("n2", "carry-one"), node("n3", "carry-cell"), node("n4", "carry-digit-fold"), node("n5", "carry-out-fold")], edges: [{ id: "e1", from: "n1", to: "n3", toPort: "digit" }, { id: "e2", from: "n2", to: "n3", toPort: "carry" }, { id: "e3", from: "n3", to: "n4" }, { id: "e4", from: "n3", to: "n5" }], carrierN: 5, point: 5 };
    const kinds = name === "joint" ? ["motor", "universal", "one-way"] : name === "linkage" ? ["motor", "chebyshev"] : ["motor", "bevel", "worm", "rack"];
    return { schema: GRAPH_SCHEMA, intervalTurns: [0, state.span], nodes: kinds.map((kind, i) => node("n" + (i + 1), kind)), edges: kinds.slice(1).map((_, i) => ({ id: "e" + (i + 1), from: "n" + (i + 1), to: "n" + (i + 2) })), carrierN: 5, point: 5 };
  }
  function initialize() {
    if (!K || !E || models.length !== 20) { status("The local mathematical modules did not load. Keep index.html, kernel.js, math-export.js and app.js together.", true); return; }
    state = { layers: models.map(m => ({ id: m.id, enabled: PRESETS.paths.includes(m.id), aperture: .45, offset: 0 })), focus: "chebyshev", view: "trace", receiver: "output", scale: "layer", span: 2, time: 0, speed: .25, playing: false, graph: null };
    state.graph = graphPreset("reduction");
    definitions.forEach(d => $("component").append(option(d.id, modelName(d.id))));
    $("component").value = "bevel";
    bind(); syncControls(); renderLibrary(); rebuild(); renderGraph();
    if (reduced.matches) $("motion-note").textContent = "Reduced motion preference is active. The workspace stays static unless you choose Play; the time slider works while paused.";
    if (typeof ResizeObserver !== "undefined") new ResizeObserver(draw).observe($("plot")); else window.addEventListener("resize", draw);
    dark.addEventListener("change", () => { renderLibrary(); renderLegend(); draw(); });
    reduced.addEventListener("change", () => { if (reduced.matches) { pause(); status("Playback paused for the reduced motion preference."); } });
  }
  function bind() {
    $("search").addEventListener("input", renderLibrary);
    $("preset").addEventListener("change", () => applyPreset($("preset").value));
    $("show-all").addEventListener("click", () => { state.layers.forEach(l => l.enabled = true); renderLibrary(); rebuild(); });
    $("show-none").addEventListener("click", () => { state.layers.forEach(l => l.enabled = false); renderLibrary(); rebuild(); });
    document.querySelectorAll('input[name="view"]').forEach(e => e.addEventListener("change", () => { state.view = e.value; draw(); syncCaption(); }));
    for (const id of ["receiver", "scale"]) $(id).addEventListener("change", () => { state[id] = $(id).value; rebuild(); });
    $("span").addEventListener("change", () => { pause(); state.span = Number($("span").value); state.time = Math.min(state.time, state.span); state.graph.intervalTurns = [0, state.span]; syncControls(); rebuild(); updateGraphResults(); });
    $("time").addEventListener("input", () => { pause(); state.time = Number($("time").value); refreshTime(); });
    $("speed").addEventListener("change", () => state.speed = Number($("speed").value));
    $("play").addEventListener("click", () => state.playing ? pause() : play());
    $("reset").addEventListener("click", () => { pause(); state.time = 0; refreshTime(); });
    $("aperture").addEventListener("input", () => { layer(state.focus).aperture = Number($("aperture").value); rebuild(); });
    $("offset").addEventListener("change", () => { layer(state.focus).offset = Number($("offset").value); rebuild(); });
    $("add-focus").addEventListener("click", () => addComponent(state.focus, layer(state.focus).aperture));
    $("add-component").addEventListener("click", () => addComponent($("component").value));
    $("builder-reset").addEventListener("click", () => { state.graph = { schema: GRAPH_SCHEMA, intervalTurns: [0, state.span], nodes: [node("n1", "motor")], edges: [], carrierN: 5, point: 5 }; renderGraph(); });
    $("builder-preset").addEventListener("change", () => { state.graph = graphPreset($("builder-preset").value); renderGraph(); });
    $("workspace-export").addEventListener("click", () => safe(() => download("motion-workspace.json", JSON.stringify(workspace(), null, 2) + "\n", "application/json")));
    $("workspace-import").addEventListener("click", () => $("import-file").click());
    $("import-file").addEventListener("change", importWorkspace);
    $("graph-export").addEventListener("click", () => safe(() => download("motion-graph.json", JSON.stringify(K.cleanSnapshot(state.graph), null, 2) + "\n", "application/json")));
    $("python-export").addEventListener("click", () => safe(() => download("motion-composition.py", E.python(state.graph), "text/x-python")));
    $("latex-export").addEventListener("click", () => safe(() => download("motion-composition.tex", E.latex(state.graph), "text/x-tex")));
    $("csv-export").addEventListener("click", () => safe(exportCSV));
    $("png-export").addEventListener("click", () => safe(() => { pause(); $("plot").toBlob(blob => safe(() => { if (blob) download("motion-plot.png", blob, "image/png"); else status("PNG export could not be created.", true); })); }));
    document.addEventListener("visibilitychange", () => { if (document.hidden) pause(); });
  }
  function applyPreset(name) { pause(); const ids = name === "all" ? models.map(m => m.id) : PRESETS[name] || PRESETS.paths; state.layers.forEach(l => { l.enabled = ids.includes(l.id); l.offset = 0; l.aperture = .45; }); state.focus = ids[0]; state.time = 0; renderLibrary(); rebuild(); }
  function inspect(id) { state.focus = id; renderLibrary(); renderInspector(); renderLegend(); renderTables(); draw(); }
  function renderLibrary() {
    const query = $("search").value.toLowerCase().trim(), list = $("mechanism-list"); list.replaceChildren(); let matches = 0;
    for (const family of Object.keys(FAMILY)) {
      const group = models.filter(m => m.family === family && [m.id, m.name, m.short, m.formula, m.family].join(" ").toLowerCase().includes(query));
      if (!group.length) continue;
      list.append(element("h3", FAMILY[family], "family-name"));
      for (const m of group) {
        matches++;
        const row = element("div", undefined, "mechanism-row" + (state.focus === m.id ? " inspected" : ""));
        const check = element("input"); check.type = "checkbox"; check.id = "show-" + m.id; check.checked = layer(m.id).enabled; check.setAttribute("aria-label", "Show " + m.name);
        check.addEventListener("change", () => { layer(m.id).enabled = check.checked; rebuild(); });
        const mark = element("span", undefined, "model-mark"); mark.style.background = color(m.id); mark.setAttribute("aria-hidden", "true");
        const b = button(m.name, () => inspect(m.id)); b.setAttribute("aria-pressed", String(state.focus === m.id));
        row.append(check, mark, b); list.append(row);
      }
    }
    $("no-results").hidden = matches > 0; $("layer-count").textContent = state.layers.filter(l => l.enabled).length + " / 20";
  }
  function renderInspector() {
    const m = byId.get(state.focus), l = layer(state.focus);
    $("inspect-name").textContent = m.name; $("inspect-family").textContent = FAMILY[m.family] || m.family;
    $("inspect-formula").textContent = m.formula || "Defined ideal component law";
    $("inspect-fidelity").textContent = m.fidelity || "Ideal mathematical model on the stated finite input interval.";
    $("inspect-fiber").textContent = m.fiber || "The displayed scalar channel can forget full phase or configuration. Forward evaluation does not solve its complete inverse fiber.";
    $("aperture").value = l.aperture; $("aperture-value").textContent = l.aperture.toFixed(2);
    $("parameter-label").textContent = typeof m.parameter === "function" ? m.parameter(l.aperture) : m.parameter || "Dimensionless admitted model setting a ∈ [0,1].";
    $("offset").value = l.offset;
  }
  function syncControls() { $("span").value = state.span; $("time").max = state.span; $("time").value = state.time; $("receiver").value = state.receiver; $("scale").value = state.scale; $("speed").value = state.speed; document.querySelectorAll('input[name="view"]').forEach(e => e.checked = e.value === state.view); }
  function rawSample(id, turns, a) { try { const v = K.sample(id, turns * TAU, a, state.receiver); return number(v) ? v : null; } catch { return null; } }
  function recordFor(l) {
    const end = state.span - l.offset, count = Math.max(129, Math.min(2049, Math.ceil(state.span * 128) + 1));
    if (end < 0) return { id: l.id, layer: l, points: [], seams: new Set(), domain: [-1, 1], rateDomain: [-1, 1] };
    const points = Array.from({ length: count }, (_, i) => { const t = end * i / (count - 1); return { t, input: t + l.offset, raw: rawSample(l.id, t + l.offset, l.aperture), slope: null }; });
    const seams = new Set();
    if (state.receiver === "hidden") for (let i = 1; i < points.length; i++) {
      const p = points[i - 1], q = points[i];
      if (eventChannels.has(l.id) && p.raw !== null && q.raw !== null && Math.abs(p.raw - q.raw) > 1e-9) seams.add(i);
      if (["rack", "worm"].includes(l.id) && (Math.floor(p.input + 1e-12) !== Math.floor(q.input + 1e-12) || p.raw !== null && q.raw !== null && Math.abs(q.raw - p.raw) > 1)) seams.add(i);
    }
    const h = end * TAU / (count - 1);
    for (let i = 0; i < count; i++) {
      const p = points[i]; if (p.raw === null || h === 0) continue;
      const left = i > 0 && !seams.has(i) && points[i - 1].raw !== null;
      const right = i + 1 < count && !seams.has(i + 1) && points[i + 1].raw !== null;
      // At a discontinuity neither adjacent retained sample is assigned a slope.
      if (seams.has(i) || seams.has(i + 1)) continue;
      if (left && right) p.slope = (points[i + 1].raw - points[i - 1].raw) / (2 * h);
      else if (right) p.slope = (points[i + 1].raw - p.raw) / h;
      else if (left) p.slope = (p.raw - points[i - 1].raw) / h;
    }
    return { id: l.id, layer: l, points, seams, domain: extent(points.map(p => p.raw)), rateDomain: extent(points.map(p => p.slope)) };
  }
  function extent(values) { const finite = values.filter(number); if (!finite.length) return [-1, 1]; let lo = Infinity, hi = -Infinity; finite.forEach(x => { lo = Math.min(lo, x); hi = Math.max(hi, x); }); return [lo, hi]; }
  function normalize(v, domain) { return !number(v) ? null : domain[0] === domain[1] ? 0 : (v - domain[0]) / (domain[1] - domain[0]) * 2 - 1; }
  function rebuild() {
    records = state.layers.filter(l => l.enabled).map(recordFor);
    const rawDomain = extent(records.flatMap(r => r.points.map(p => p.raw))), rateDomain = extent(records.flatMap(r => r.points.map(p => p.slope)));
    records.forEach(r => r.points.forEach(p => { p.y = state.scale === "raw" ? p.raw : normalize(p.raw, state.scale === "shared" ? rawDomain : r.domain); p.rate = state.scale === "raw" ? p.slope : normalize(p.slope, state.scale === "shared" ? rateDomain : r.rateDomain); }));
    $("layer-count").textContent = records.length + " / 20";
    renderInspector(); renderLegend(); syncCaption(); refreshTime();
  }
  function syncCaption() {
    $("view-title").textContent = { trace: "Traces", phase: "Phase portrait", mechanism: "Mechanism" }[state.view];
    $("plot-caption").textContent = state.view === "mechanism" ? "The inspected model at the current input. Geometric linkage diagrams use the ideal constraints; other diagrams show input phase and the selected channel, schematically." : state.view === "phase" ? "Channel versus its sampled slope per radian. Different times can occupy the same coordinate; crossings do not establish equivalent mechanisms." : "Channel versus input turns. Shifted displays stop at their retained support. " + (state.scale === "raw" ? "Raw layer coordinates may use different units." : "Normalization forgets original scale and offset; the readout table and CSV retain raw values.");
  }
  function renderLegend() { $("legend").replaceChildren(); records.forEach(r => { const b = button(modelName(r.id) + (r.layer.offset ? " +" + r.layer.offset + "t" : ""), () => inspect(r.id)); const mark = element("span", undefined, "legend-line"); mark.style.background = color(r.id); b.prepend(mark); b.setAttribute("aria-pressed", String(state.focus === r.id)); $("legend").append(b); }); }
  function refreshTime(tables = true) { $("time").value = state.time; $("time-value").textContent = state.time.toFixed(3) + " turns"; draw(); if (tables) { renderTables(); updateGraphResults(); } }
  function pause() { if (!state) return; state.playing = false; $("play").textContent = "Play"; cancelAnimationFrame(frameHandle); lastFrame = null; }
  function play() { if (state.time >= state.span) state.time = 0; state.playing = true; $("play").textContent = "Pause"; lastFrame = null; frameHandle = requestAnimationFrame(animate); }
  function animate(now) { if (!state.playing) return; if (lastFrame !== null) state.time = Math.min(state.span, state.time + Math.min(.1, (now - lastFrame) / 1000) * state.speed); lastFrame = now; const read = now - lastReadout > 150; refreshTime(read); if (read) lastReadout = now; if (state.time >= state.span) { pause(); renderTables(); updateGraphResults(); status("Reached the end of the admitted interval."); } else frameHandle = requestAnimationFrame(animate); }
  function palette() { const style = getComputedStyle(document.documentElement); return { bg: style.getPropertyValue("--soft"), ink: style.getPropertyValue("--ink"), muted: style.getPropertyValue("--muted"), grid: style.getPropertyValue("--line") }; }
  function draw() {
    if (!state) return;
    const canvas = $("plot"), rect = canvas.getBoundingClientRect(), ratio = Math.min(2, devicePixelRatio || 1), w = Math.max(100, rect.width), h = Math.max(100, rect.height);
    if (canvas.width !== Math.round(w * ratio) || canvas.height !== Math.round(h * ratio)) { canvas.width = Math.round(w * ratio); canvas.height = Math.round(h * ratio); }
    const c = canvas.getContext("2d"); if (!c) return; c.setTransform(ratio, 0, 0, ratio, 0, 0); const p = palette(); c.fillStyle = p.bg; c.fillRect(0, 0, w, h);
    if (state.view === "mechanism") { drawMechanism(c, w, h, p); return; }
    const margin = { left: 56, right: 22, top: 22, bottom: 44 }, x0 = margin.left, y0 = margin.top, ww = w - margin.left - margin.right, hh = h - margin.top - margin.bottom;
    let xd = state.view === "trace" ? [0, state.span] : state.scale === "raw" ? extent(records.flatMap(r => r.points.map(v => v.y))) : [-1.12, 1.12];
    let yd = state.scale === "raw" ? extent(records.flatMap(r => r.points.map(v => state.view === "trace" ? v.y : v.rate))) : [-1.12, 1.12];
    function padded(d) { const gap = (d[1] - d[0]) || 2; return [d[0] - gap * .08, d[1] + gap * .08]; }
    if (state.scale === "raw") { yd = padded(yd); if (state.view === "phase") xd = padded(xd); }
    const X = x => x0 + (x - xd[0]) / (xd[1] - xd[0] || 1) * ww, Y = y => y0 + (1 - (y - yd[0]) / (yd[1] - yd[0] || 1)) * hh;
    c.strokeStyle = p.grid; c.lineWidth = .65; c.fillStyle = p.muted; c.font = "11px system-ui";
    for (let i = 0; i <= 4; i++) { const xx = x0 + i * ww / 4, yy = y0 + i * hh / 4; c.beginPath(); c.moveTo(xx, y0); c.lineTo(xx, y0 + hh); c.moveTo(x0, yy); c.lineTo(x0 + ww, yy); c.stroke(); c.textAlign = "center"; c.fillText(valueText(xd[0] + i * (xd[1] - xd[0]) / 4), xx, h - 22); c.textAlign = "right"; c.fillText(valueText(yd[1] - i * (yd[1] - yd[0]) / 4), x0 - 9, yy + 4); }
    c.textAlign = "center"; c.fillText(state.view === "trace" ? "display turns" : "channel coordinate", x0 + ww / 2, h - 6);
    c.save(); c.translate(13, y0 + hh / 2); c.rotate(-Math.PI / 2); c.fillText(state.view === "trace" ? "channel coordinate" : "sampled slope", 0, 0); c.restore();
    c.save(); c.beginPath(); c.rect(x0, y0, ww, hh); c.clip();
    records.forEach((r, index) => {
      c.strokeStyle = color(r.id); c.lineWidth = r.id === state.focus ? 2.5 : 1.7; c.setLineDash(index >= 8 ? [7, 4] : []); c.beginPath(); let open = false;
      r.points.forEach((v, i) => { const x = state.view === "trace" ? v.t : v.y, y = state.view === "trace" ? v.y : v.rate; if (!number(x) || !number(y) || r.seams.has(i)) { open = false; if (!number(x) || !number(y)) return; } if (!open) c.moveTo(X(x), Y(y)); else c.lineTo(X(x), Y(y)); open = true; }); c.stroke(); c.setLineDash([]);
      if (state.time <= state.span - r.layer.offset + 1e-12 && r.points.length) { const v = nearest(r, state.time), x = state.view === "trace" ? v.t : v.y, y = state.view === "trace" ? v.y : v.rate; if (number(x) && number(y)) { c.fillStyle = color(r.id); c.beginPath(); c.arc(X(x), Y(y), r.id === state.focus ? 5 : 3.5, 0, TAU); c.fill(); } }
    });
    if (state.view === "trace") { c.strokeStyle = p.muted; c.setLineDash([3, 5]); c.lineWidth = 1; c.beginPath(); c.moveTo(X(state.time), y0); c.lineTo(X(state.time), y0 + hh); c.stroke(); c.setLineDash([]); }
    c.restore(); if (!records.length) { c.fillStyle = p.muted; c.textAlign = "center"; c.font = "15px system-ui"; c.fillText("Choose a layer from the mechanism library", w / 2, h / 2); }
  }
  function drawMechanism(c, w, h, p) {
    const m = byId.get(state.focus), l = layer(state.focus), t = state.time + l.offset;
    c.textAlign = "center"; c.fillStyle = p.ink; c.font = "600 15px system-ui"; c.fillText(m.name, w / 2, 28);
    if (t > state.span + 1e-12) { c.fillStyle = p.muted; c.font = "14px system-ui"; c.fillText("The shifted layer is outside the admitted interval.", w / 2, h / 2); return; }
    const theta = t * TAU, scale = Math.min(w / 9, h / 6.2), center = [w / 2, h / 2 + 12];
    const P = v => [center[0] + v[0] * scale, center[1] - v[1] * scale];
    const line = (a, b, col = color(m.id), width = 4) => { const A = P(a), B = P(b); c.strokeStyle = col; c.lineWidth = width; c.beginPath(); c.moveTo(...A); c.lineTo(...B); c.stroke(); };
    const dot = (v, fixed = false) => { const a = P(v); c.fillStyle = fixed ? p.ink : p.bg; c.strokeStyle = color(m.id); c.lineWidth = 2; c.beginPath(); c.arc(a[0], a[1], 6, 0, TAU); c.fill(); c.stroke(); };
    const circle = (v, r, col = p.grid) => { const a = P(v); c.strokeStyle = col; c.lineWidth = 1.5; c.beginPath(); c.arc(a[0], a[1], r * scale, 0, TAU); c.stroke(); };
    if (m.id === "chebyshev") {
      center[0] = w / 2 - scale; center[1] = h * .86; const a = [Math.cos(theta), Math.sin(theta)], o = [2, 0], dx = o[0] - a[0], dy = -a[1], d = Math.hypot(dx, dy), height = Math.sqrt(6.25 - d * d / 4), b = [(a[0] + 2) / 2 - dy / d * height, a[1] / 2 + dx / d * height], foot = [2 * b[0] - a[0], 2 * b[1] - a[1]];
      circle([0, 0], 1); line([0, 0], a); line(a, b); line(b, o); line(a, foot, color(m.id), 2); [[0, 0], o].forEach(v => dot(v, true)); [a, b, foot].forEach(v => dot(v)); c.fillStyle = p.muted; c.font = "12px system-ui"; c.fillText("Crank 1 · base 2 · links 2.5 · P = 2B − A", w / 2, h - 10);
    } else if (m.id === "slider" || m.id === "scotch") {
      center[0] = w * .29; const a = [Math.cos(theta), Math.sin(theta)], L = 2.2 + 2.8 * l.aperture, x = m.id === "slider" ? a[0] + Math.sqrt(L * L - a[1] * a[1]) : a[0];
      const localScale = m.id === "slider" ? Math.min(scale, w * .6 / (L + 1)) : scale; const old = scale;
      // Uniform scene transform keeps the admitted slider geometry in the frame.
      c.save(); if (m.id === "slider") { c.translate(center[0], center[1]); c.scale(localScale / old, localScale / old); c.translate(-center[0], -center[1]); }
      circle([0, 0], 1); line([-1.3, 0], [m.id === "slider" ? L + 1.3 : 1.5, 0], p.grid, 2); line([0, 0], a); if (m.id === "slider") line(a, [x, 0]); else line([x, -1.2], [x, 1.2]); dot([0, 0], true); dot(a); dot([x, 0]); c.restore();
      c.fillStyle = p.muted; c.font = "12px system-ui"; c.fillText(m.id === "slider" ? "Positive square-root assembly branch; crank radius = 1" : "Unit-radius geometry; the typed output rescales by its radius", w / 2, h - 10);
    } else {
      const input = [-1.6, 0], output = [1.6, 0], raw = rawSample(m.id, t, l.aperture); circle(input, .92); circle(output, .92); line(input, [input[0] + .85 * Math.cos(theta), .85 * Math.sin(theta)]); dot(input, true);
      let typed; try { typed = K.sample(m.id, theta, l.aperture, "typed"); } catch { typed = raw; }
      const outAngle = number(typed) ? typed : raw || 0; line(output, [output[0] + .85 * Math.cos(outAngle), .85 * Math.sin(outAngle)]); dot(output, true); line([-.45, 0], [.45, 0], p.grid, 2);
      c.fillStyle = p.muted; c.font = "12px system-ui"; c.fillText("Input phase", P(input)[0], P(input)[1] + 1.2 * scale); c.fillText("Typed output readout", P(output)[0], P(output)[1] + 1.2 * scale);
      c.fillText("Pointer angle is a schematic display for non-angular outputs.", w / 2, h - 10);
      c.fillStyle = p.ink; c.font = "13px ui-monospace, monospace"; c.fillText("selected channel = " + valueText(raw), w / 2, 58);
    }
  }
  function nearest(r, time) { const i = Math.max(0, Math.min(r.points.length - 1, Math.round(time / (state.span - r.layer.offset || 1) * (r.points.length - 1)))); return r.points[i]; }
  function cells(row, values) { values.forEach(v => row.append(element("td", String(v)))); return row; }
  function renderTables() {
    $("readout-body").replaceChildren(); records.forEach(r => { const admitted = state.time + r.layer.offset <= state.span + 1e-12, sample = r.points.length ? nearest(r, state.time) : null, raw = admitted ? rawSample(r.id, state.time + r.layer.offset, r.layer.aperture) : null; $("readout-body").append(cells(element("tr"), [modelName(r.id), r.layer.aperture.toFixed(2), admitted ? (state.time + r.layer.offset).toFixed(4) : "Outside interval", valueText(raw), admitted ? valueText(sample?.slope) : "OPEN"])); });
    if (!records.length) { const row = element("tr"), cell = element("td", "No visible layers."); cell.colSpan = 5; row.append(cell); $("readout-body").append(row); }
    const r = records.find(r => r.id === state.focus) || recordFor(layer(state.focus)); $("sample-caption").textContent = modelName(state.focus) + " — sampled raw " + state.receiver + " channel"; $("sample-body").replaceChildren();
    const indices = new Set(Array.from({ length: 21 }, (_, i) => Math.round(i / 20 * (r.points.length - 1)))); indices.forEach(i => { const v = r.points[i]; if (v) $("sample-body").append(cells(element("tr"), [v.t.toFixed(4), v.input.toFixed(4), valueText(v.raw), valueText(v.slope)])); });
  }
  function addComponent(kind, aperture = .45) {
    safe(() => { if (state.graph.nodes.length >= 24) throw new Error("This workspace admits at most 24 graph nodes."); const previous = state.graph.nodes.at(-1), used = new Set(state.graph.nodes.map(n => n.id)); let n = 1; while (used.has("n" + n)) n++; const next = node("n" + n, kind, aperture); state.graph.nodes.push(next); const ports = nodeInputs(defs.get(kind)); if (previous && ports.length) state.graph.edges.push({ id: freshEdgeId(), from: previous.id, to: next.id, toPort: ports[0].name }); renderGraph(); status("Added " + modelName(kind) + ". Inspect its port disposition below."); });
  }
  function renderGraph() {
    $("graph-nodes").replaceChildren(); const description = safe(() => E.describe(state.graph)); if (!description) return;
    state.graph.nodes.forEach((n, index) => {
      const def = defs.get(n.componentId), detail = description.nodes?.find(d => d.id === n.id), card = element("li", undefined, "graph-node"); card.append(element("span", n.id), element("strong", modelName(n.componentId)), element("p", detail?.formula || "OPEN: no registered formula"));
      const label = element("label", "Parameter a"), slider = element("input"); slider.type = "range"; slider.min = 0; slider.max = 1; slider.step = .01; slider.value = n.aperture; slider.id = "node-a-" + index; label.htmlFor = slider.id; slider.addEventListener("input", () => { n.aperture = Number(slider.value); updateGraphResults(); }); card.append(label, slider);
      const inputs = nodeInputs(def), edgePort = edge => edge.toPort == null ? inputs[0]?.name : edge.toPort;
      inputs.forEach(port => {
        const id = "node-port-" + index + "-" + port.name.replace(/[^a-z0-9]/gi, ""), select = element("select"), label = element("label", port.name + ": " + port.type); select.id = id; label.htmlFor = id; select.append(option("", "No supplied input")); state.graph.nodes.filter(x => x.id !== n.id).forEach(x => select.append(option(x.id, x.id + " · " + modelName(x.componentId))));
        const edge = state.graph.edges.find(e => e.to === n.id && edgePort(e) === port.name); select.value = edge?.from || "";
        select.addEventListener("change", () => { state.graph.edges = state.graph.edges.filter(e => !(e.to === n.id && edgePort(e) === port.name)); if (select.value) state.graph.edges.push({ id: freshEdgeId(), from: select.value, to: n.id, toPort: port.name }); renderGraph(); }); card.append(label, select);
        const disposition = description.connections?.find(e => e.to === n.id && (e.targetPort || edgePort(e)) === port.name); const note = element("p", disposition ? disposition.disposition + " · from " + disposition.from : "OPEN · missing input", !disposition || disposition.disposition.includes("OPEN") ? "edge-open" : ""); card.append(note);
      });
      card.append(element("p", "Output: " + (def?.outPort || "OPEN")));
      const actions = element("div", undefined, "button-row"); actions.append(button("Remove " + n.id, () => { state.graph.nodes = state.graph.nodes.filter(x => x.id !== n.id); state.graph.edges = state.graph.edges.filter(e => e.from !== n.id && e.to !== n.id); if (state.graph.selectedNodeIds) state.graph.selectedNodeIds = state.graph.selectedNodeIds.filter(id => id !== n.id); renderGraph(); })); card.append(actions); $("graph-nodes").append(card);
    }); updateGraphResults();
  }
  function updateGraphResults() {
    if (!state?.graph) return; const result = safe(() => K.evaluateGraph(state.graph, state.time)); $("graph-results").replaceChildren(); if (!result) { $("builder-disposition").textContent = "Admission error"; return; }
    $("builder-disposition").textContent = result.disposition;
    state.graph.nodes.forEach(n => { const r = result.nodes[n.id], row = cells(element("tr"), [n.id + " · " + modelName(n.componentId), defs.get(n.componentId)?.outPort || "OPEN", valueText(r?.value), r?.status || "OPEN"]); if (r?.note) row.lastChild.append(element("p", r.note, "hint")); $("graph-results").append(row); });
  }
  function workspace() { pause(); return { schema: SCHEMA, layers: state.layers.map(l => ({ ...l })), focus: state.focus, view: state.view, receiver: state.receiver, scale: state.scale, span: state.span, time: state.time, speed: state.speed, graph: K.cleanSnapshot(state.graph) }; }
  function validateWorkspace(raw) {
    const keys = ["schema", "layers", "focus", "view", "receiver", "scale", "span", "time", "speed", "graph"];
    if (!raw || typeof raw !== "object" || Array.isArray(raw) || Object.keys(raw).sort().join() !== keys.sort().join() || raw.schema !== SCHEMA) throw new Error("Choose a clean rprm-motion-workspace/v1 JSON file.");
    if (!Array.isArray(raw.layers) || raw.layers.length !== 20 || new Set(raw.layers.map(l => l.id)).size !== 20) throw new Error("A workspace must declare each of the twenty model layers exactly once.");
    for (const l of raw.layers) if (!l || Object.keys(l).sort().join() !== ["id", "enabled", "aperture", "offset"].sort().join() || !byId.has(l.id) || typeof l.enabled !== "boolean" || !number(l.aperture) || l.aperture < 0 || l.aperture > 1 || !SHIFTS.includes(l.offset)) throw new Error("Invalid layer settings.");
    if (!byId.has(raw.focus) || !["trace", "phase", "mechanism"].includes(raw.view) || !["output", "hidden"].includes(raw.receiver) || !["layer", "shared", "raw"].includes(raw.scale) || !SPANS.includes(raw.span) || !number(raw.time) || raw.time < 0 || raw.time > raw.span || ![.1, .25, .5, 1].includes(raw.speed)) throw new Error("A view, clock or receiver is outside this workspace's admitted values.");
    const graph = K.cleanSnapshot(raw.graph); if (graph.nodes.length > 24 || graph.intervalTurns[0] !== 0 || graph.intervalTurns[1] !== raw.span) throw new Error("The graph must have at most 24 nodes and the same finite time interval as the workspace.");
    return { ...raw, layers: models.map(m => ({ ...raw.layers.find(l => l.id === m.id) })), graph, playing: false };
  }
  async function importWorkspace(event) { const file = event.target.files?.[0]; if (!file) return; try { if (file.size > 262144) throw new Error("Workspace files are limited to 256 KiB."); const admitted = validateWorkspace(JSON.parse(await file.text())); pause(); state = admitted; syncControls(); renderLibrary(); rebuild(); renderGraph(); status("Workspace imported and paused. All retained model settings were restored."); } catch (error) { status(error.message || String(error), true); } finally { event.target.value = ""; } }
  function download(name, data, type) { return safe(() => { pause(); const blob = data instanceof Blob ? data : new Blob([data], { type }); const url = URL.createObjectURL(blob), a = element("a"); try { a.href = url; a.download = name; document.body.append(a); a.click(); status("Exported " + name + "."); } finally { a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000); } }); }
  function exportCSV() { pause(); const quote = x => '"' + String(x).replaceAll('"', '""') + '"'; const rows = [["mechanism", "receiver", "aperture", "phase_shift_turns", "display_turns", "input_turns", "raw_channel", "slope_per_radian", "seam_before"]]; records.forEach(r => r.points.forEach((p, i) => rows.push([r.id, state.receiver, r.layer.aperture, r.layer.offset, p.t, p.input, p.raw ?? "", p.slope ?? "", r.seams.has(i)]))); download("motion-samples.csv", rows.map(row => row.map(quote).join(",")).join("\n") + "\n", "text/csv;charset=utf-8"); }
  // Small deterministic seams for offline UI checks; no browser state is read or saved.
  globalThis.MMAAtlas = Object.freeze({ getWorkspace: () => workspace(), validateWorkspace, sampleRecords: () => records.map(r => ({ id: r.id, points: r.points.map(p => ({ ...p })), seams: [...r.seams] })) });
  initialize();
})();
