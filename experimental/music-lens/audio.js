/* Optional, dependency-free playback. Load as a classic script after model.js.
 * Audio is a listening aid, not a retained representation or a music-analysis claim.
 * Call setSound(true) and play() directly from user gestures. No audio is created
 * by construction, edits, timers, visibility events, or visual-only playback.
 * pause()/stop() both reset to step 0. Confirmed sound choice survives stopping;
 * an unresolved activation does not. Editing events/tempo restarts the loop.
 * Scheduling: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Advanced_techniques
 * User control: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Best_practices
 */
(function (global) {
  "use strict";

  function create(callbacks = {}) {
    const onStep = typeof callbacks.onStep === "function" ? callbacks.onStep : () => {};
    const onChange = typeof callbacks.onChange === "function" ? callbacks.onChange : () => {};
    const onError = typeof callbacks.onError === "function" ? callbacks.onError : () => {};
    const AudioCtor = global.AudioContext || global.webkitAudioContext;
    const doc = global.document;
    const voices = new Set();
    let events = [];
    let tempo = 96;
    let playing = false;
    let sound = false;
    let step = 0;
    let destroyed = false;
    let context = null;
    let master = null;
    let ready = false;
    let resumePromise = null;
    let activationVersion = 0;
    let transportVersion = 0;
    let timer = null;
    let frame = null;
    let origin = 0;
    let nextAudioIndex = 0;
    const now = () => global.performance.now() / 1000;
    const stepDuration = () => 60 / tempo / 4;

    function getState() {
      return {
        playing, sound, tempo, step,
        audioState: destroyed ? "closed" : context ? context.state : AudioCtor ? "uninitialized" : "unsupported"
      };
    }

    function changed() { if (!destroyed) onChange(getState()); }
    function updateStep(next) {
      if (step !== next) {
        step = next;
        onStep(step);
      }
    }
    function assertLive() {
      if (destroyed) throw new Error("This music transport has been destroyed.");
    }

    function cancelVoices() {
      for (const voice of voices) {
        // Disconnect immediately: even a scheduled source that has not started
        // cannot escape after a stop or source edit. No exponential ramp to zero.
        voice.oscillator.onended = null;
        try { voice.oscillator.stop(); } catch (_) { /* Already ended. */ }
        voice.oscillator.disconnect();
        voice.envelope.disconnect();
      }
      voices.clear();
    }

    function clearTransport() {
      transportVersion += 1;
      if (timer !== null) global.clearTimeout(timer);
      if (frame !== null) global.cancelAnimationFrame(frame);
      timer = frame = null;
      cancelVoices();
    }

    function audioFailed(message) {
      sound = false;
      ready = false;
      activationVersion += 1;
      cancelVoices();
      changed();
      if (!destroyed) onError(message);
    }

    function contextChanged() {
      if (destroyed) return;
      if (context.state !== "running" && ready) {
        audioFailed("Sound was interrupted by the browser. Enable sound again to continue listening; the visual loop is still available.");
      } else {
        changed();
      }
    }

    // This helper is called only in setSound(true) or play()'s gesture stack.
    // Creation and resume both happen before the first await.
    async function activateAudio(version) {
      if (destroyed || version !== activationVersion || !sound) return;
      try {
        if (!AudioCtor) throw new Error("Web Audio is unavailable in this browser. Visual playback still works.");
        if (!context || context.state === "closed") {
          if (context) context.removeEventListener("statechange", contextChanged);
          context = new AudioCtor();
          context.addEventListener("statechange", contextChanged);
          master = context.createGain();
          master.gain.setValueAtTime(0.12, context.currentTime);
          master.connect(context.destination);
        }
        if (context.state !== "running") {
          if (!resumePromise) {
            const pending = context.resume();
            resumePromise = pending;
            // Cleanup is registered once, independently of canceled consumers.
            pending.then(
              () => { if (resumePromise === pending) resumePromise = null; },
              () => { if (resumePromise === pending) resumePromise = null; }
            );
          }
          await resumePromise;
        }
        if (destroyed || version !== activationVersion || !sound) return;
        if (context.state !== "running") throw new Error("The browser did not enable sound. Try enabling sound again from its control.");
        if (ready) return;
        ready = true;
        // The visual clock may have moved while browser activation was pending.
        // Join its next step, never replay missed notes in a burst.
        if (playing) {
          nextAudioIndex = Math.max(0, Math.ceil((now() - origin) / stepDuration()));
          scheduleAudio();
        }
        changed();
      } catch (error) {
        if (destroyed || version !== activationVersion || !sound) return;
        const detail = error && error.message ? error.message : "Audio activation failed.";
        audioFailed(`${detail} Use visual playback or retry the sound control.`);
      }
    }

    function note(midi, time) {
      const oscillator = context.createOscillator();
      const envelope = context.createGain();
      const voice = { oscillator, envelope };
      voices.add(voice);
      oscillator.type = "sine";
      oscillator.frequency.setValueAtTime(440 * Math.pow(2, (midi - 69) / 12), time);
      // A note ends before the next possible onset, so the admitted single-voice
      // pattern never stacks peaks. The short linear ADSR avoids clicks at normal
      // note boundaries, with an exact zero endpoint and no log(0) automation.
      const duration = Math.min(0.18, stepDuration() * 0.8);
      envelope.gain.setValueAtTime(0, time);
      envelope.gain.linearRampToValueAtTime(0.8, time + 0.008);
      envelope.gain.linearRampToValueAtTime(0.5, time + 0.026);
      envelope.gain.setValueAtTime(0.5, time + duration * 0.62);
      envelope.gain.linearRampToValueAtTime(0, time + duration);
      oscillator.connect(envelope);
      envelope.connect(master);
      oscillator.onended = () => {
        oscillator.disconnect();
        envelope.disconnect();
        voices.delete(voice);
      };
      oscillator.start(time);
      oscillator.stop(time + duration + 0.005);
    }

    function scheduleAudio() {
      if (!playing || !sound || !ready || context.state !== "running") return;
      const perfTime = now();
      const audioTime = context.currentTime;
      const duration = stepDuration();
      // A stalled main thread skips missed onsets instead of bunching them up.
      const firstFresh = Math.max(0, Math.ceil((perfTime - origin - 0.015) / duration));
      nextAudioIndex = Math.max(nextAudioIndex, firstFresh);
      try {
        while (origin + nextAudioIndex * duration < perfTime + 0.1) {
          const event = events.find((entry) => entry.step === nextAudioIndex % 16);
          const target = audioTime + origin + nextAudioIndex * duration - perfTime;
          if (event) note(event.midi, Math.max(audioTime + 0.003, target));
          nextAudioIndex += 1;
        }
      } catch (_) {
        audioFailed("Sound could not be scheduled. Visual playback still works; try enabling sound again.");
      }
    }

    function startLoop() {
      clearTransport();
      origin = now() + 0.03;
      nextAudioIndex = 0;
      const version = transportVersion;
      updateStep(0);
      if (destroyed || !playing || version !== transportVersion) return;
      const tick = () => {
        if (destroyed || !playing || version !== transportVersion) return;
        scheduleAudio();
        if (!destroyed && playing && version === transportVersion) timer = global.setTimeout(tick, 25);
      };
      const draw = () => {
        if (destroyed || !playing || version !== transportVersion) return;
        const index = Math.max(0, Math.floor((now() - origin) / stepDuration()));
        updateStep(index % 16);
        // A consumer may stop the transport from onStep.
        if (!destroyed && playing && version === transportVersion) frame = global.requestAnimationFrame(draw);
      };
      tick();
      if (!destroyed && playing && version === transportVersion) frame = global.requestAnimationFrame(draw);
      changed();
    }

    function setEvents(source) {
      assertLive();
      if (!Array.isArray(source) || source.length !== 6) throw new TypeError("Supply exactly six events A through F.");
      const ids = new Set();
      const steps = new Set();
      const cloned = Array.from(source, (event) => {
        if (!event || typeof event.id !== "string" || !/^[A-F]$/.test(event.id) || ids.has(event.id) ||
            !Number.isInteger(event.step) || event.step < 0 || event.step > 15 || steps.has(event.step) ||
            !Number.isInteger(event.midi) || event.midi < 36 || event.midi > 84) {
          throw new TypeError("Events need unique IDs A–F, unique integer steps 0–15, and integer MIDI pitches 36–84.");
        }
        ids.add(event.id);
        steps.add(event.step);
        return { id: event.id, step: event.step, midi: event.midi };
      });
      events = cloned;
      if (playing) startLoop();
      return getState();
    }

    function setTempo(bpm) {
      assertLive();
      if (!Number.isInteger(bpm) || bpm < 48 || bpm > 160) throw new TypeError("Tempo must be an integer from 48 to 160 BPM.");
      if (bpm === tempo) return getState();
      tempo = bpm;
      if (playing) startLoop(); else changed();
      return getState();
    }

    async function setSound(enabled) {
      assertLive();
      if (typeof enabled !== "boolean") throw new TypeError("Sound must be true or false.");
      const version = ++activationVersion;
      sound = enabled;
      if (!enabled) {
        ready = false;
        cancelVoices();
        changed();
      } else {
        changed();
        await activateAudio(version);
      }
      return getState();
    }

    async function play() {
      assertLive();
      if (doc && doc.hidden) return getState();
      if (!playing) {
        playing = true;
        startLoop();
      }
      if (sound && !ready) await activateAudio(activationVersion);
      return getState();
    }

    function stop() {
      if (destroyed) return getState();
      activationVersion += 1;
      if (!ready) sound = false;
      playing = false;
      clearTransport();
      updateStep(0);
      changed();
      return getState();
    }

    function hidden() { if (doc.hidden) stop(); }
    function destroy() {
      if (destroyed) return;
      stop();
      destroyed = true;
      sound = ready = false;
      if (doc) doc.removeEventListener("visibilitychange", hidden);
      global.removeEventListener("pagehide", stop);
      if (context) {
        context.removeEventListener("statechange", contextChanged);
        master.disconnect();
        if (context.state !== "closed") context.close().catch(() => {});
      }
    }

    if (doc) doc.addEventListener("visibilitychange", hidden);
    global.addEventListener("pagehide", stop);
    return Object.freeze({ setEvents, setTempo, setSound, play, pause: stop, stop, getState, destroy });
  }

  global.MusicAudio = Object.freeze({ create });
})(typeof window === "undefined" ? globalThis : window);
