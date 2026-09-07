"use strict";
/* Executes actual application handlers with finite DOM/Canvas stubs. This is a
   state/export regression check, not browser or visual/accessibility QA. */
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const root = path.resolve(__dirname, "../..");
async function run() {
  let checks = 0;
  function check(condition, message) { checks++; assert.ok(condition, message); }
  const events = new Map(), downloads = [], urls = new Map(); let failDownloads = false;
  class Element {
    constructor(tag = "div") { this.tagName = tag; this.children = []; this.style = {}; this.handlers = {}; this.attributes = {}; this.value = ""; this.checked = false; this.hidden = false; this.className = ""; this._text = ""; this.classList = { toggle() {}, add() {}, remove() {} }; }
    append(...items) { for (const item of items) { this.children.push(item); if (item && typeof item === "object") item.parent = this; } }
    prepend(item) { this.children.unshift(item); }
    replaceChildren(...items) { this.children = []; this.append(...items); }
    remove() { if (this.parent) this.parent.children = this.parent.children.filter(x => x !== this); }
    set textContent(value) { this._text = String(value); this.children = []; }
    get textContent() { return this._text + this.children.map(x => x.textContent || "").join(""); }
    get lastChild() { return this.children.at(-1); }
    setAttribute(key, value) { this.attributes[key] = value; }
    addEventListener(kind, action) { this.handlers[kind] = action; }
    click() { if (this.tagName === "a") downloads.push({ name: this.download, blob: urls.get(this.href) }); return this.handlers.click?.({ target: this }); }
    getBoundingClientRect() { return { width: 700, height: 360 }; }
    getContext() { return canvas; }
    toBlob(callback) { callback(new Blob(["finite canvas stub"], { type: "image/png" })); }
  }
  const canvas = new Proxy({}, { get(target, key) { if (key in target) return target[key]; return (...values) => { for (const v of values) if (typeof v === "number") check(Number.isFinite(v), "Canvas coordinate must be finite: " + key); }; }, set(target, key, value) { target[key] = value; return true; } });
  const html = fs.readFileSync(path.join(root, "atlas/index.html"), "utf8");
  const elements = new Map([...html.matchAll(/\bid="([^"]+)"/g)].map(match => [match[1], new Element(match[1] === "plot" ? "canvas" : "div")]));
  const radios = ["trace", "phase", "mechanism"].map(value => Object.assign(new Element("input"), { value }));
  elements.get("search").value = "";
  const document = { body: new Element("body"), documentElement: new Element("html"), hidden: false, createElement: tag => new Element(tag), getElementById: id => { check(elements.has(id), "Referenced HTML ID exists: " + id); return elements.get(id); }, querySelectorAll: selector => { check(selector === 'input[name="view"]', "Only declared radio query is stubbed"); return radios; }, addEventListener: (kind, action) => events.set(kind, action) };
  const context = vm.createContext({ document, console, Blob, URL: { createObjectURL(blob) { if (failDownloads) throw new Error("download unavailable"); const url = "blob:stub-" + urls.size; urls.set(url, blob); return url; }, revokeObjectURL() {} }, matchMedia: () => ({ matches: false, addEventListener() {} }), getComputedStyle: () => ({ getPropertyValue: key => ({ "--soft": "#ffffff", "--ink": "#000000", "--muted": "#333333", "--line": "#888888" })[key] }), devicePixelRatio: 1, ResizeObserver: class { observe() {} }, requestAnimationFrame: () => 1, cancelAnimationFrame() {}, setTimeout() {}, window: { addEventListener() {} } });
  for (const file of ["kernel.js", "math-export.js", "app.js"]) vm.runInContext(fs.readFileSync(path.join(root, "atlas", file), "utf8"), context, { filename: "atlas/" + file });
  const A = context.MMAAtlas, K = context.MMAKernel;
  const json = value => JSON.parse(JSON.stringify(value));
  check(!!A, "Actual application initializes");
  const initial = json(A.getWorkspace());
  check(initial.schema === "rprm-motion-workspace/v1" && initial.layers.length === 20, "Clean complete workspace");
  check(elements.get("play").textContent === "Play", "Static initial state");
  check(A.sampleRecords().length === 3, "Initial comparison has three visible layers");
  check(json(A.validateWorkspace(initial)).layers.length === 20, "Complete clean round trip");
  elements.get("show-all").click();
  check(A.sampleRecords().length === 20, "Native layer action enables all 20");
  elements.get("show-none").click();
  check(A.sampleRecords().length === 0, "Native clear action empties sample display");
  async function importValue(value) {
    const target = elements.get("import-file"); target.files = [{ size: JSON.stringify(value).length, text: async () => JSON.stringify(value) }];
    await target.handlers.change({ target });
  }
  const shifted = json(initial); shifted.focus = "rack"; shifted.layers.forEach(l => { l.enabled = l.id === "rack"; if (l.id === "rack") l.offset = .75; });
  await importValue(shifted);
  let record = json(A.sampleRecords()[0]);
  check(record.id === "rack", "Imported focus/display state");
  check(record.points[0].input === .75 && record.points.at(-1).input === 2, "Shift retains source interval endpoint");
  check(record.points.at(-1).t === 1.25, "Shifted curve has its own display support");
  check(record.points.every(p => p.input <= 2 && p.input >= .75), "No shifted extrapolation");
  for (const p of record.points) check(Math.abs(p.raw - K.sample("rack", p.input * 2 * Math.PI, .45, "output")) < 1e-10, "Rendered record keeps actual raw law");
  const hidden = json(shifted); hidden.receiver = "hidden"; hidden.layers.find(l => l.id === "rack").offset = 0;
  await importValue(hidden); record = json(A.sampleRecords()[0]);
  check(record.seams.length === 2, "Hidden rack wraps retain two seam events");
  for (const seam of record.seams) { check(record.points[seam].slope === null, "No slope at wrap"); check(record.points[seam - 1].slope === null, "No derivative across wrap"); }
  const longWindow = json(hidden); longWindow.span = 16; longWindow.graph.intervalTurns = [0,16];
  await importValue(longWindow);
  const longRecord = json(A.sampleRecords()[0]);
  for (let i = 1; i < longRecord.points.length; i++) if (Math.abs(longRecord.points[i].raw - longRecord.points[i-1].raw) > 1) {
    check(longRecord.seams.includes(i), "Actual sampled sawtooth jump is a seam even beside rounded nominal integer time");
    check(longRecord.points[i].slope === null && longRecord.points[i-1].slope === null, "No derivative across rounded wrap");
  }
  await importValue(hidden);
  const prior = json(A.getWorkspace());
  const malformed = [ { ...prior, extra: "unsupported payload" }, { ...prior, time: true }, { ...prior, layers: prior.layers.slice(1) }, { ...prior, span: 64 }, { ...prior, graph: { ...prior.graph, runtime: "unsupported" } } ];
  for (const bad of malformed) { checks++; assert.throws(() => A.validateWorkspace(bad)); await importValue(bad); checks++; assert.deepEqual(json(A.getWorkspace()), prior, "Rejected import must not mutate live state"); }
  elements.get("workspace-export").click();
  const saved = downloads.at(-1); check(saved.name === "motion-workspace.json", "Workspace download action"); checks++; assert.deepEqual(JSON.parse(await saved.blob.text()), prior, "Actual workspace payload is the validated state");
  elements.get("csv-export").click();
  const csv = await downloads.at(-1).blob.text(); check(downloads.at(-1).name === "motion-samples.csv", "Sample CSV action"); check(csv.includes('"raw_channel"') && csv.includes('"slope_per_radian"'), "CSV exposes raw values and slope semantics"); check(csv.split("\n").length === record.points.length + 2, "CSV exports every retained sample");
  const preset = elements.get("builder-preset"); preset.value = "carry"; preset.handlers.change();
  check(elements.get("builder-disposition").textContent === "ONE", "Two-input carry example is wired and evaluates");
  const graph = json(A.getWorkspace()).graph;
  check(graph.nodes.some(n => n.componentId === "carry-cell") && graph.edges.some(e => e.toPort === "digit") && graph.edges.some(e => e.toPort === "carry"), "Separate carry input roles retained");
  elements.get("python-export").click(); const python = await downloads.at(-1).blob.text();
  check(python.includes("rprm-motion-graph/v1") && !python.includes("rprm-motion-workspace/v1"), "Python keeps only the clean graph, not whole workspace");
  elements.get("latex-export").click(); const tex = await downloads.at(-1).blob.text(); check(tex.includes("\\begin{document}") && tex.includes("\\end{document}"), "Actual LaTeX export completes its document");
  elements.get("png-export").click(); check(downloads.at(-1).name === "motion-plot.png", "Actual PNG action delegates to canvas blob export");
  failDownloads = true;
  for (const id of ["workspace-export","csv-export","png-export","python-export","latex-export","graph-export"]) {
    checks++; assert.doesNotThrow(() => elements.get(id).click(), "Download failure is handled in " + id);
    check(elements.get("status").textContent.includes("download unavailable"), "Download failure is reported in " + id);
  }
  failDownloads = false;
  const selected = json(initial); selected.graph.selectedNodeIds = ["n2"];
  await importValue(selected);
  function descendants(e) { return [e,...e.children.flatMap(x => typeof x === "object" ? descendants(x) : [])]; }
  descendants(elements.get("graph-nodes")).find(e => e.tagName === "button" && e.textContent === "Remove n2").click();
  check(!A.getWorkspace().graph.selectedNodeIds.includes("n2"), "Removing selected node also removes retained selection reference");
  const collision = json(initial); collision.graph.nodes = collision.graph.nodes.slice(0,2); collision.graph.edges = [{ id:"edge-n3-in",from:"n1",to:"n2",toPort:"in" }];
  await importValue(collision); elements.get("component").value = "bevel"; elements.get("add-component").click();
  const added = json(A.getWorkspace()).graph;
  check(new Set(added.edges.map(e => e.id)).size === added.edges.length, "Adding a node cannot collide with arbitrary retained edge IDs");
  const multi = json(initial); multi.graph = {schema:"rprm-motion-graph/v1",intervalTurns:[0,2],nodes:[{id:"d",componentId:"digit-clock",aperture:.45},{id:"c",componentId:"carry-one",aperture:.45},{id:"cell",componentId:"carry-cell",aperture:.45}],edges:[{id:"ed",from:"d",to:"cell",toPort:null},{id:"ec",from:"c",to:"cell",toPort:"carry"}]};
  await importValue(multi);
  const carryPort = descendants(elements.get("graph-nodes")).find(e => e.tagName === "select" && e.id === "node-port-2-carry");
  check(carryPort.value === "c", "Default null target denotes only the first input, not every input");
  carryPort.value = "c"; carryPort.handlers.change();
  const rewired = json(A.getWorkspace()).graph;
  check(rewired.edges.some(e => e.id === "ed" && e.from === "d"), "Reconnecting carry preserves default first-port digit edge");
  check(K.evaluateGraph(rewired,0).disposition === "ONE", "Multiport graph remains complete after carry reconnection");
  // This boundary is lexical source inspection, distinct from the stub execution.
  const source = fs.readFileSync(path.join(root, "atlas/app.js"), "utf8");
  check(!/\b(fetch|XMLHttpRequest|WebSocket|localStorage|indexedDB)\b/.test(source), "No app network or browser-persistence API");
  check(!/\b(?:https?):\/\//.test(html), "No remote page dependency");
  for (const view of radios) { view.handlers.change(); check(elements.get("view-title").textContent.length > 0, "View is reachable by native radio change"); }
  return { schema: "rprm-motion-view-check/v1", status: "PASS", assertions: checks, scope: "Actual app initialization/actions with finite DOM and Canvas stubs; clean round trips, exported payloads, phase-shift support and hidden-wrap seams. Browser, visuals and accessibility NOT_RUN.", sourceHashes: Object.fromEntries(["atlas/app.js", "atlas/index.html", "atlas/style.css", "checks/atlas/view-checks.js"].map(file => [file, crypto.createHash("sha256").update(fs.readFileSync(path.join(root, file))).digest("hex")])) };
}
async function main() {
  const args = process.argv.slice(2);
  if (args.length && (args.length !== 2 || args[0] !== "--output" || !path.isAbsolute(args[1])))
    throw new Error("Use --output ABSOLUTE_PATH or no arguments");
  function publish(result) {
    const payload = JSON.stringify(result, null, 2) + "\n";
    if (args.length) {
      fs.mkdirSync(path.dirname(args[1]), {recursive:true}); fs.writeFileSync(args[1], payload);
    }
    return payload;
  }
  publish({status:"PENDING"});
  try { process.stdout.write(publish(await run())); }
  catch (error) { publish({status:"FAIL", error:String(error)}); throw error; }
}
if (require.main === module) main().catch(error => { process.stderr.write(error.stack + "\n"); process.exitCode = 1; });
module.exports = { run };
