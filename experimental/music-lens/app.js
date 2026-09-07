/* Original software: 0BSD. Six retained events, three displays, optional sound. */
"use strict";
(() => {
  const M = window.MusicModel;
  const $ = id => document.getElementById(id);
  const ids = ["A", "B", "C", "D", "E", "F"];
  const classes = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"];
  const colors = ["#aa9aff", "#cda0ec", "#f099c6", "#f09ea2", "#f2b88b", "#e9d386", "#bfe197", "#8edeb7", "#88dce0", "#85c6f2", "#9caef6", "#b19bed"];
  const presets = {
    rise: {root:60,phase:0,steps:[0,3,6,8,10,14],offsets:[0,4,7,12,7,4],tempo:96},
    night: {root:57,phase:0,steps:[0,2,5,8,11,14],offsets:[0,3,7,10,7,3],tempo:78},
    steps: {root:62,phase:0,steps:[0,1,4,7,10,12],offsets:[0,7,2,9,4,12],tempo:116}
  };
  let state = M.createState();
  let selected = 0;
  let locked = true;
  let activePointer = null;
  let dragOffsetY = 0;
  let announceTimer;
  const f = x => Number(x.toFixed(3));
  const px = step => 80 + 51.5*step;
  const py = midi => 30 + (84-midi)*7.7;
  const circular = (index, count, radius, cy=127) => {
    const theta = index/count*2*Math.PI-Math.PI/2;
    return {x:165+Math.cos(theta)*radius,y:cy+Math.sin(theta)*radius};
  };
  const signed = n => n>0?`+${n}`:n<0?`−${-n}`:"0";
  const announce = message => {
    clearTimeout(announceTimer);
    announceTimer=setTimeout(()=>{$("announcement").textContent=message;},200);
  };
  const notice = message => {$("notice").textContent=message;$("notice").hidden=!message;};
  const custom = () => {
    if (!$("preset").querySelector('option[value="custom"]')) {
      const option=document.createElement("option");option.value="custom";option.textContent="Your variation";$("preset").append(option);
    }
    $("preset").value="custom";
  };

  $("pitch-rows").innerHTML = Array.from({length:49},(_,i)=>{
    const midi=84-i, black=[1,3,6,8,10].includes(midi%12), y=py(midi);
    return `<rect x="54" y="${f(y-3.85)}" width="827" height="7.7" fill="${black?'#162135':'#1c2940'}"/><line x1="54" x2="881" y1="${f(y+3.85)}" y2="${f(y+3.85)}" stroke="${midi%12===0?'#53627e':'#283750'}" stroke-width="${midi%12===0?'1':'.45'}"/>${midi%12===0?`<text x="42" y="${f(y+3)}" text-anchor="end" fill="#b7c6dd" font-size="9">${M.noteName(midi)}</text>`:''}`;
  }).join("");
  $("step-lines").innerHTML=Array.from({length:17},(_,s)=>`<line x1="${f(54+s*51.75)}" x2="${f(54+s*51.75)}" y1="24" y2="407" stroke="${s%4===0?'#60708b':'#334159'}" stroke-width="${s%4===0?'1.2':'.6'}"/>`).join("");
  $("beat-labels").innerHTML=Array.from({length:16},(_,s)=>`<text x="${px(s)}" y="423" text-anchor="middle" fill="${s%4===0?'#d1dbed':'#8b9db8'}" font-size="9">${s+1}</text>${s%4===0?`<text x="${px(s)}" y="15" fill="#b5c4dd" font-size="8">BEAT ${s/4+1}</text>`:''}`).join("");
  $("note-blocks").innerHTML=ids.map((id,i)=>`<g class="note-group" data-note="${i}"><rect x="-23" y="-15" width="46" height="30" fill="transparent"/><rect class="note-face" x="-21" y="-8" width="42" height="16" rx="4"/><text text-anchor="middle" dominant-baseline="central" fill="#111b2a">${id}</text></g>`).join("");
  $("note-strip").innerHTML=ids.map((id,i)=>`<button type="button" data-select="${i}" aria-pressed="${i===0}"><span class="event-id">${id}</span><span class="event-dot" aria-hidden="true"></span><span class="event-note"></span><span class="event-step"></span></button>`).join("");
  $("class-nodes").innerHTML=classes.map((name,p)=>{
    const a=circular(p,12,86), label=circular(p,12,110);
    return `<g data-class="${p}"><circle cx="${f(a.x)}" cy="${f(a.y)}" r="10"/><text x="${f(a.x)}" y="${f(a.y+3)}" text-anchor="middle" fill="#172032" font-size="8" font-weight="600" class="class-members"></text><text x="${f(label.x)}" y="${f(label.y+4)}" text-anchor="middle" fill="#b4c1d8" font-size="10">${name}</text></g>`;
  }).join("");
  $("rhythm-spokes").innerHTML=Array.from({length:16},(_,s)=>{
    const p=circular(s,16,86,124),q=circular(s,16,108,124);
    return `<g><circle cx="${f(p.x)}" cy="${f(p.y)}" r="${s%4===0?4:2.5}" fill="#6b7a96"/><text x="${f(q.x)}" y="${f(q.y+3)}" text-anchor="middle" fill="${s%4===0?'#e1e7f4':'#96a9c3'}" font-size="8">${s+1}</text></g>`;
  }).join("");
  $("rhythm-nodes").innerHTML=ids.map(id=>`<g><circle r="10"/><text text-anchor="middle" dominant-baseline="central" fill="#122033" font-size="8" font-weight="600">${id}</text></g>`).join("");

  let player;
  function renderStep(step) {
    const playing=player?.getState().playing===true;
    $("play-column").setAttribute("x",f(54+step*51.75));
    $("play-column").setAttribute("opacity",playing?".085":"0");
    const q=circular(step,16,79,124);
    $("rhythm-hand").setAttribute("x2",f(q.x));$("rhythm-hand").setAttribute("y2",f(q.y));
    $("rhythm-hand").setAttribute("opacity",playing?".75":"0");
    $("step-readout").textContent=playing?String(step+1):"—";
    M.events(state).forEach((event,i)=>{
      const active=playing&&event.step===step;
      const circle=$("rhythm-nodes").children[i].querySelector("circle");
      circle.setAttribute("r",active?"13":"10");
      circle.setAttribute("stroke",active?"#f2f6ff":"none");
      circle.setAttribute("stroke-width","2");
      $("note-blocks").children[i].querySelector(".note-face").setAttribute("stroke-width",active?"3":i===selected?"2":".5");
    });
  }
  player=window.MusicAudio.create({
    onStep:renderStep,
    onChange:s=>{
      $("play-label").textContent=s.playing?"Pause":"Play";
      $("play-icon").textContent=s.playing?"Ⅱ":"▶";
      $("sound").setAttribute("aria-pressed",String(s.sound));
      $("sound-label").textContent=s.sound?"Sound on":"Sound off";
      $("transport-state").textContent=s.playing?(s.sound?"Playing · soft synth":"Playing · visual only"):"Ready · sound is optional";
      renderStep(s.step);
    },
    onError:message=>{notice(message);announce(message);}
  });

  function render() {
    const events=M.events(state), bounds=M.pitchMoveBounds(state,selected,locked);
    $("root").value=state.root;$("root-name").textContent=M.noteName(state.root);
    $("root").setAttribute("aria-valuetext",`${M.noteName(state.root)}, MIDI ${state.root}`);
    $("phase").value=state.phase;$("phase-value").textContent=`${state.phase} ${state.phase===1?'step':'steps'}`;
    $("lock").setAttribute("aria-pressed",String(locked));
    $("lock").textContent=locked?"↔ Pitches linked":"↗ Edit one note";
    $("drag-hint").textContent=locked?"Drag a note up or down. With pitches linked, the whole melody follows.":"Drag a note up or down. Only that note moves; the other five stay put.";
    $("selected-id").textContent=ids[selected];
    $("note-value").textContent=`${M.noteName(events[selected].midi)} · ${M.frequency(events[selected].midi).toFixed(1)} Hz`;
    $("note-pitch").min=bounds.min;$("note-pitch").max=bounds.max;$("note-pitch").value=events[selected].midi;
    $("note-pitch").setAttribute("aria-valuetext",`${M.noteName(events[selected].midi)}, MIDI ${events[selected].midi}`);
    $("octave-up").disabled=state.root>60;$("octave-down").disabled=state.root<60;
    events.forEach((event,i)=>{
      const group=$("note-blocks").children[i];
      group.setAttribute("transform",`translate(${px(event.step)} ${f(py(event.midi))})`);
      group.querySelector(".note-face").setAttribute("fill",colors[event.pitchClass]);
      group.querySelector(".note-face").setAttribute("stroke",i===selected?"#f1eaff":"#24334c");
      group.querySelector("text").textContent=`${event.id}·${M.noteName(event.midi)}`;
      const button=$("note-strip").children[i];
      button.setAttribute("aria-pressed",String(i===selected));
      button.setAttribute("aria-label",`Select note ${event.id}, ${M.noteName(event.midi)}, step ${event.step+1}`);
      button.querySelector(".event-dot").style.backgroundColor=colors[event.pitchClass];
      button.querySelector(".event-note").textContent=M.noteName(event.midi);
      button.querySelector(".event-step").textContent=`step ${event.step+1}`;
      const p=circular(event.step,16,86,124), rhythm=$("rhythm-nodes").children[i];
      rhythm.setAttribute("transform",`translate(${f(p.x)} ${f(p.y)})`);
      rhythm.querySelector("circle").setAttribute("fill",colors[event.pitchClass]);
    });
    const chronological=[...events].sort((a,b)=>a.step-b.step);
    $("melody-line").setAttribute("d",chronological.map((e,i)=>`${i?'L':'M'}${px(e.step)} ${f(py(e.midi))}`).join(" "));
    const present=M.pitchClasses(state);
    $("class-count").textContent=present.length;
    [...$("class-nodes").children].forEach((g,p)=>{
      const members=events.filter(e=>e.pitchClass===p), circle=g.querySelector("circle");
      circle.setAttribute("fill",members.length?colors[p]:"#172032");
      circle.setAttribute("stroke",members.length?colors[p]:"#6d7d99");
      circle.setAttribute("r",members.length?"12":"4");
      g.querySelector(".class-members").textContent=members.length>1?String(members.length):"";
    });
    const pitchPts=present.map(p=>circular(p,12,86));
    $("class-links").innerHTML=`<path d="${pitchPts.map((p,i)=>`${i?'L':'M'}${f(p.x)} ${f(p.y)}`).join(' ')}${pitchPts.length>2?' Z':''}" stroke="#c0b2fa" stroke-width="1.3" fill="${pitchPts.length>2?'#b4a2f010':'none'}"/>`;
    $("intervals").textContent=state.offsets.slice(1).map((o,i)=>signed(o-state.offsets[i])).join(" · ");
    $("gaps").textContent=M.rhythmGaps(state).join(" · ");
    renderStep(player.getState().step);
  }
  function update(next) {
    state=next;custom();notice("");render();player.setEvents(M.events(state));
  }
  function safeUpdate(callback) {
    try { update(callback()); }
    catch(error) {notice(error.message);render();}
  }
  $("note-strip").addEventListener("click",event=>{
    const button=event.target.closest("[data-select]");if(!button)return;
    selected=Number(button.dataset.select);render();announce(`Note ${ids[selected]} selected.`);
  });
  $("lock").addEventListener("click",()=>{locked=!locked;render();announce(locked?"Pitches linked. The melody moves together.":"Editing one note. The other notes stay put.");});
  $("root").addEventListener("input",e=>safeUpdate(()=>M.transpose(state,Number(e.target.value))));
  $("phase").addEventListener("input",e=>safeUpdate(()=>M.rotate(state,Number(e.target.value))));
  $("note-pitch").addEventListener("input",e=>safeUpdate(()=>M.movePitch(state,selected,Number(e.target.value),locked)));
  $("octave-up").addEventListener("click",()=>safeUpdate(()=>M.transpose(state,state.root+12)));
  $("octave-down").addEventListener("click",()=>safeUpdate(()=>M.transpose(state,state.root-12)));
  $("invert").addEventListener("click",()=>{safeUpdate(()=>M.invert(state));announce("Pitch contour reflected around note A.");});
  $("reverse").addEventListener("click",()=>{safeUpdate(()=>M.reverse(state));announce("Rhythm reflected around the phrase origin.");});
  $("tempo").addEventListener("input",e=>{const bpm=Number(e.target.value);$("tempo-value").textContent=`${bpm} BPM`;player.setTempo(bpm);custom();});
  $("play").addEventListener("click",async()=>{notice("");if(player.getState().playing)player.pause();else await player.play();});
  $("sound").addEventListener("click",async()=>{notice("");await player.setSound(!player.getState().sound);});
  function loadPreset(name) {
    const p=presets[name];if(!p)return;
    player.stop();state=M.createState(p.root,p.phase,p.steps,p.offsets);selected=0;locked=true;
    $("preset").value=name;$("tempo").value=p.tempo;$("tempo-value").textContent=`${p.tempo} BPM`;
    notice("");render();player.setTempo(p.tempo);player.setEvents(M.events(state));
  }
  $("preset").addEventListener("change",e=>loadPreset(e.target.value));
  $("reset").addEventListener("click",()=>{loadPreset("rise");announce("Starting phrase restored. Playback stopped.");});
  const roll=$("roll");
  roll.addEventListener("pointerdown",event=>{
    if(event.button!==0||activePointer!==null)return;
    const note=event.target.closest("[data-note]");if(!note)return;
    const matrix=roll.getScreenCTM();if(!matrix)return;
    selected=Number(note.dataset.note);
    const grab=new DOMPoint(event.clientX,event.clientY).matrixTransform(matrix.inverse());
    dragOffsetY=grab.y-py(M.events(state)[selected].midi);
    activePointer=event.pointerId;roll.setPointerCapture(activePointer);render();event.preventDefault();
  });
  roll.addEventListener("pointermove",event=>{
    if(event.pointerId!==activePointer)return;
    const matrix=roll.getScreenCTM();if(!matrix)return;
    const p=new DOMPoint(event.clientX,event.clientY).matrixTransform(matrix.inverse());
    const bounds=M.pitchMoveBounds(state,selected,locked);
    const target=Math.max(bounds.min,Math.min(bounds.max,Math.round(84-(p.y-dragOffsetY-30)/7.7)));
    if(target!==M.events(state)[selected].midi)safeUpdate(()=>M.movePitch(state,selected,target,locked));
  });
  const finish=event=>{
    if(event.pointerId!==activePointer)return;
    if(roll.hasPointerCapture(activePointer))roll.releasePointerCapture(activePointer);
    activePointer=null;announce(`Note ${ids[selected]}: ${M.noteName(M.events(state)[selected].midi)}.`);
  };
  roll.addEventListener("pointerup",finish);roll.addEventListener("pointercancel",finish);
  roll.addEventListener("lostpointercapture",()=>{activePointer=null;});
  loadPreset("rise");
})();
