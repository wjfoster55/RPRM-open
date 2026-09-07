"use strict";

// Deterministic transport checks, not an acoustic/browser conformance test.
// Run: node --test experimental/music-lens/audio.test.cjs
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const source = fs.readFileSync(path.join(__dirname, "audio.js"), "utf8");
const pattern = () => Array.from("ABCDEF", (id, i) => ({ id, step: i * 2, midi: 60 + i }));

function harness({ unsupported = false, deferred = false, failResume = false } = {}) {
  let clock = 0;
  let sequence = 0;
  const timeouts = new Map();
  const frames = new Map();
  const contexts = [];
  const oscillators = [];
  const gains = [];
  const steps = [];
  const states = [];
  const errors = [];
  function target() {
    const listeners = new Map();
    return {
      addEventListener(type, fn) { if (!listeners.has(type)) listeners.set(type, new Set()); listeners.get(type).add(fn); },
      removeEventListener(type, fn) { listeners.get(type)?.delete(fn); },
      dispatch(type) { for (const fn of listeners.get(type) || []) fn(); }
    };
  }
  const document = Object.assign(target(), { hidden: false });
  function param() {
    return {
      changes: [],
      setValueAtTime(value, time) { this.changes.push({ value, time }); },
      linearRampToValueAtTime(value, time) { this.changes.push({ value, time }); }
    };
  }
  class FakeContext {
    constructor() {
      Object.assign(this, target());
      this.state = deferred || failResume ? "suspended" : "running";
      this.destination = {};
      this.resumeCalls = 0;
      this.closed = false;
      contexts.push(this);
    }
    get currentTime() { return clock / 1000; }
    createGain() {
      const node = { gain: param(), disconnected: false, connect() {}, disconnect() { this.disconnected = true; } };
      gains.push(node);
      return node;
    }
    createOscillator() {
      const node = {
        frequency: param(), disconnected: false, stops: [],
        connect() {}, disconnect() { this.disconnected = true; },
        start(time) { this.started = time; }, stop(time) { this.stops.push(time); }
      };
      oscillators.push(node);
      return node;
    }
    resume() {
      this.resumeCalls += 1;
      if (failResume) return Promise.reject(new Error("Audio permission denied."));
      if (deferred) return new Promise((resolve) => { this.finishResume = () => { this.state = "running"; resolve(); }; });
      this.state = "running";
      return Promise.resolve();
    }
    close() { this.closed = true; this.state = "closed"; return Promise.resolve(); }
  }
  const sandbox = Object.assign(target(), {
    document, performance: { now: () => clock },
    setTimeout(fn, delay) { const id = ++sequence; timeouts.set(id, { fn, due: clock + delay }); return id; },
    clearTimeout(id) { timeouts.delete(id); },
    requestAnimationFrame(fn) { const id = ++sequence; frames.set(id, fn); return id; },
    cancelAnimationFrame(id) { frames.delete(id); }
  });
  if (!unsupported) sandbox.AudioContext = FakeContext;
  vm.runInNewContext(source, sandbox);
  const player = sandbox.MusicAudio.create({ onStep: (v) => steps.push(v), onChange: (v) => states.push(v), onError: (v) => errors.push(v) });
  function advance(ms) {
    const end = clock + ms;
    while (true) {
      const entries = [...timeouts.entries()].filter(([, item]) => item.due <= end).sort((a, b) => a[1].due - b[1].due);
      if (!entries.length) break;
      const [id, item] = entries[0];
      clock = item.due;
      timeouts.delete(id);
      item.fn();
      const pendingFrames = [...frames.values()];
      frames.clear();
      pendingFrames.forEach((fn) => fn(clock));
    }
    clock = end;
    const pendingFrames = [...frames.values()];
    frames.clear();
    pendingFrames.forEach((fn) => fn(clock));
  }
  return { player, contexts, oscillators, gains, steps, states, errors, document, sandbox, advance,
    pending: () => timeouts.size + frames.size,
    stall(ms) { clock += ms; const jobs = [...timeouts.values()]; timeouts.clear(); jobs.forEach((job) => job.fn()); }
  };
}

test("visual playback needs no AudioContext and uses 16 quarter-beat steps", async () => {
  const h = harness({ unsupported: true });
  assert.equal(h.player.getState().tempo, 96);
  assert.equal(h.player.getState().sound, false);
  assert.equal(h.player.getState().audioState, "unsupported");
  h.player.setEvents(pattern());
  await h.player.play();
  h.advance(200);
  assert.equal(h.player.getState().step, 1);
  h.advance(2400);
  assert.equal(h.player.getState().step, 0);
  assert(h.steps.every((step, i) => !i || step !== h.steps[i - 1]));
  assert.equal(h.errors.length, 0);
  await h.player.setSound(true);
  assert.equal(h.player.getState().playing, true);
  assert.equal(h.player.getState().sound, false);
  assert.match(h.errors[0], /unavailable/);
  h.player.stop();
  assert.equal(h.pending(), 0);
});

test("admission rejects malformed/sparse inputs atomically and clones events", async () => {
  const h = harness();
  const input = pattern();
  h.player.setEvents(input);
  input[0].midi = 84;
  assert.throws(() => h.player.setEvents(new Array(6)), /unique/);
  assert.throws(() => h.player.setEvents(pattern().map((x) => ({ ...x, step: 0 }))), /unique/);
  assert.throws(() => h.player.setEvents(pattern().map((x) => ({ ...x, id: "A" }))), /unique/);
  assert.throws(() => h.player.setTempo(48.5), /integer/);
  assert.throws(() => h.player.setTempo(161), /integer/);
  assert.equal(h.contexts.length, 0);
  await h.player.setSound(true);
  assert.equal(h.oscillators.length, 0);
  await h.player.play();
  assert.equal(h.oscillators.length, 1);
  assert(Math.abs(h.oscillators[0].frequency.changes[0].value - 261.6255653005986) < 1e-8);
  assert.equal(h.gains[0].gain.changes[0].value, 0.12);
  assert(h.gains[1].gain.changes.every((p) => Number.isFinite(p.value) && p.value >= 0 && p.value <= 0.8));
  h.player.destroy();
});

test("edits cancel every old voice and restart with the new source and tempo", async () => {
  const h = harness();
  h.player.setEvents(pattern());
  await h.player.setSound(true);
  await h.player.play();
  h.advance(350);
  const old = h.oscillators.slice();
  const changed = pattern();
  changed[0].midi = 69;
  h.player.setEvents(changed);
  assert(old.every((voice) => voice.disconnected && voice.stops.includes(undefined)));
  assert.equal(h.player.getState().step, 0);
  assert.equal(h.oscillators.at(-1).frequency.changes[0].value, 440);
  const beforeTempo = h.oscillators.slice();
  h.player.setTempo(160);
  assert(beforeTempo.every((voice) => voice.disconnected));
  h.advance(140);
  assert.equal(h.player.getState().step, 1);
  h.player.pause();
  assert.equal(h.player.getState().step, 0);
  assert.equal(h.player.getState().playing, false);
  assert.equal(h.pending(), 0);
  assert(h.oscillators.every((voice) => voice.disconnected));
});

test("sound-off cancels active/queued audio immediately while the visual clock continues", async () => {
  const h = harness();
  h.player.setEvents(pattern());
  await h.player.setSound(true);
  await h.player.play();
  await h.player.setSound(false);
  assert(h.oscillators.every((voice) => voice.disconnected));
  const count = h.oscillators.length;
  h.advance(900);
  assert.equal(h.oscillators.length, count);
  assert.equal(h.player.getState().playing, true);
  assert(h.player.getState().step > 0);
  h.player.destroy();
});

test("late resume cannot resurrect sound or playback after stop, sound-off or destroy", async () => {
  for (const action of ["stop", "off", "destroy"]) {
    const h = harness({ deferred: true });
    h.player.setEvents(pattern());
    const enable = h.player.setSound(true);
    const play = h.player.play();
    assert.equal(h.contexts[0].resumeCalls, 1);
    if (action === "off") await h.player.setSound(false); else h.player[action]();
    h.contexts[0].finishResume();
    await Promise.all([enable, play]);
    assert.equal(h.player.getState().sound, false, action);
    assert.equal(h.player.getState().playing, action === "off", action);
    assert.equal(h.oscillators.length, 0, action);
    if (action !== "off") assert.equal(h.pending(), 0, action);
    h.player.destroy();
  }
});

test("shared pending enable/play cannot schedule duplicate onsets", async () => {
  const h = harness({ deferred: true });
  h.player.setEvents(pattern());
  const enable = h.player.setSound(true);
  const play = h.player.play();
  h.contexts[0].finishResume();
  await Promise.all([enable, play]);
  assert.equal(h.oscillators.length, 1);
  assert.equal(h.player.getState().audioState, "running");
  h.player.destroy();
});

test("failed permission leaves a usable visual loop and a readable error", async () => {
  const h = harness({ failResume: true });
  const enable = h.player.setSound(true);
  await h.player.play();
  await enable;
  assert.equal(h.player.getState().playing, true);
  assert.equal(h.player.getState().sound, false);
  assert.match(h.errors[0], /permission denied/);
  h.advance(500);
  assert(h.player.getState().step > 0);
  h.player.destroy();
});

test("hidden/pagehide stops all work and visibility return does not restart", async () => {
  const h = harness();
  h.player.setEvents(pattern());
  await h.player.setSound(true);
  await h.player.play();
  h.document.hidden = true;
  h.document.dispatch("visibilitychange");
  assert.equal(h.player.getState().playing, false);
  assert.equal(h.pending(), 0);
  assert(h.oscillators.every((voice) => voice.disconnected));
  h.document.hidden = false;
  h.document.dispatch("visibilitychange");
  assert.equal(h.player.getState().playing, false);
  await h.player.play();
  h.sandbox.dispatch("pagehide");
  assert.equal(h.player.getState().playing, false);
  assert.equal(h.pending(), 0);
  h.player.destroy();
});

test("a delayed scheduler skips missed notes instead of queuing a burst", async () => {
  const h = harness();
  h.player.setEvents(pattern());
  await h.player.setSound(true);
  await h.player.play();
  const count = h.oscillators.length;
  h.stall(100000);
  assert(h.oscillators.length - count <= 1);
  h.player.destroy();
});
