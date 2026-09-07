/* Original software: 0BSD. A local, dependency-free display of LensModel. */
"use strict";
(() => {
  const M = window.LensModel;
  const $ = id => document.getElementById(id);
  const letters = ["A", "B", "C", "D", "E"];
  const offsets = [0, 48, 126, 172, 278];
  const controls = ["saturation", "lightness", "amplitude", "cycles", "radius", "rotation"];
  const presets = {
    studio: {anchor:232, saturation:68, lightness:62, amplitude:70, cycles:1, radius:75, rotation:0},
    dusk: {anchor:285, saturation:56, lightness:57, amplitude:45, cycles:2, radius:85, rotation:34},
    citrus: {anchor:58, saturation:70, lightness:57, amplitude:85, cycles:1, radius:95, rotation:315}
  };
  let state = M.createState(presets.studio.anchor, offsets);
  let selected = 0;
  let locked = true;
  let activePointer = null;
  let announcementTimer;
  const values = () => Object.fromEntries(controls.map(id => [id, Number($(id).value)]));
  const f = n => Number(n.toFixed(3));
  const ink = hex => {
    const linear = [1,3,5].map(i => parseInt(hex.slice(i,i+2),16)/255)
      .map(v => v <= .04045 ? v/12.92 : ((v+.055)/1.055)**2.4);
    const luminance=.2126*linear[0]+.7152*linear[1]+.0722*linear[2];
    return (luminance+.05)/.05 >= 1.05/(luminance+.05) ? "#000000" : "#ffffff";
  };
  const announce = message => {
    clearTimeout(announcementTimer);
    announcementTimer = setTimeout(() => { $("announcement").textContent = message; }, 220);
  };
  const markCustom = () => document.querySelectorAll("[data-preset]").forEach(el => el.setAttribute("aria-pressed","false"));

  // Controls remain stable DOM nodes throughout a drag, preserving keyboard focus.
  $("point-pickers").innerHTML = letters.map((letter,i) => `<button type="button" data-select="${i}" aria-label="Select point ${letter}" aria-pressed="${i===0}"><span class="point-dot" aria-hidden="true"></span>${letter}</button>`).join("");
  $("palette").innerHTML = letters.map((letter,i) => `<button type="button" class="swatch" data-select="${i}" aria-label="Select swatch ${letter}" aria-pressed="${i===0}"><span class="swatch-letter">${letter}</span><span class="swatch-hex"></span></button>`).join("");
  $("wheel-nodes").innerHTML = letters.map((letter,i) => `<g class="wheel-node" data-point="${i}"><circle class="selection-ring" r="20" fill="none" stroke="#eaf3e7"/><circle class="point-fill" r="14"/><text text-anchor="middle" dominant-baseline="central">${letter}</text></g>`).join("");
  $("wave-paths").innerHTML = letters.map(() => `<path fill="none"/>`).join("");
  $("wave-dots").innerHTML = letters.map(letter => `<g><circle r="8" fill="#fdfef9" stroke="#566d56"/><text text-anchor="middle" dominant-baseline="central" font-size="8" fill="#20352b">${letter}</text></g>`).join("");
  $("orbit-points").innerHTML = letters.map(letter => `<g><circle r="11"/><text text-anchor="middle" dominant-baseline="central" font-size="9" font-weight="600">${letter}</text></g>`).join("");
  function render() {
    const v = values();
    const phases = M.phases(state);
    const colors = phases.map(p => M.colorHex(p,v.saturation,v.lightness));
    $("phase").value = phases[selected];
    $("phase").setAttribute("aria-valuetext",`${phases[selected]} degrees, point ${letters[selected]}`);
    $("selected-letter").textContent = letters[selected];
    $("phase-value").textContent = `${phases[selected]}°`;
    $("lock").setAttribute("aria-pressed",String(locked));
    $("lock-label").textContent = locked ? "Move together" : "Move one point";
    $("lock-icon").textContent = locked ? "↔" : "↗";
    $("lock-state").textContent = locked ? "ON" : "OFF";
    $("wheel-mode").textContent = locked ? "locked" : "editable";
    $("mode-hint").textContent = locked ? "The offsets stay fixed. Every point moves by the same amount." : "Only the selected point moves. You are reshaping the relationship.";
    $("relation-state").textContent = locked ? "Preserved" : "Editing";
    $("offsets").textContent = state.offsets.map(x=>`${x}°`).join(" · ");
    controls.forEach(id => { $(`${id}-value`).textContent = `${v[id]}${id==="rotation" ? "°" : id==="cycles" ? "" : "%"}`; });
    document.querySelectorAll("[data-select]").forEach(button => {
      const i = Number(button.dataset.select);
      button.setAttribute("aria-pressed",String(i===selected));
      if (button.classList.contains("swatch")) {
        button.style.backgroundColor = colors[i];
        button.style.color = ink(colors[i]);
        button.style.setProperty("--swatch",colors[i]);
        button.style.setProperty("--swatch-ink",ink(colors[i]));
        button.querySelector(".swatch-hex").textContent = colors[i].toUpperCase();
        button.setAttribute("aria-label",`Select swatch ${letters[i]}, ${phases[i]} degrees, ${colors[i]}`);
      } else button.querySelector(".point-dot").style.backgroundColor = colors[i];
    });
    const wheelPoints = phases.map(p => { const pt=M.orbitPoint(p,1,270); return {x:160+120*pt.x,y:160+120*pt.y}; });
    $("wheel-links").innerHTML = `<path class="wheel-link" d="${wheelPoints.map((p,i)=>`${i?'L':'M'}${f(p.x)} ${f(p.y)}`).join(" ")} Z"/>`;
    [...$("wheel-nodes").children].forEach((g,i) => {
      g.setAttribute("transform",`translate(${f(wheelPoints[i].x)} ${f(wheelPoints[i].y)})`);
      g.querySelector(".point-fill").setAttribute("fill",colors[i]);
      g.querySelector(".point-fill").setAttribute("stroke","#142c25");
      g.querySelector("text").setAttribute("fill",ink(colors[i]));
      g.querySelector(".selection-ring").setAttribute("opacity",i===selected?"1":"0");
    });
    [...$("wave-paths").children].forEach((path,i) => {
      const d = Array.from({length:241},(_,j)=>{
        const t=j/240;
        return `${j?"L":"M"}${f(20+420*t)} ${f(80-62*M.wavePoint(phases[i],t,v.amplitude/100,v.cycles))}`;
      }).join(" ");
      path.setAttribute("d",d);
      path.setAttribute("stroke",colors[i]);
      path.setAttribute("stroke-width",i===selected?"3.2":"2");
      const dot=$("wave-dots").children[i];
      dot.setAttribute("transform",`translate(${40+i*90} ${f(80-62*M.wavePoint(phases[i],(20+i*90)/420,v.amplitude/100,v.cycles))})`);
    });
    const orbit = phases.map(p => M.orbitPoint(p,v.radius/100,v.rotation));
    const xy = orbit.map(p => ({x:230+150*p.x,y:80+64*p.y}));
    $("orbit-rings").innerHTML = `<ellipse cx="230" cy="80" rx="${150*v.radius/100}" ry="${64*v.radius/100}" fill="none" stroke="#cad6c1" stroke-dasharray="3 5"/><circle cx="230" cy="80" r="2.5" fill="#6d8469"/>`;
    $("orbit-links").innerHTML = `<path d="${xy.map((p,i)=>`${i?'L':'M'}${f(p.x)} ${f(p.y)}`).join(" ")} Z" stroke="#687d63" stroke-width="1.2" fill="none"/>`;
    [...$("orbit-points").children].forEach((g,i)=>{
      g.setAttribute("transform",`translate(${f(xy[i].x)} ${f(xy[i].y)})`);
      g.querySelector("circle").setAttribute("fill",colors[i]);
      g.querySelector("circle").setAttribute("stroke",i===selected?"#243b2d":"#fdfef9");
      g.querySelector("circle").setAttribute("stroke-width",i===selected?"2.5":"1.5");
      g.querySelector("text").setAttribute("fill",ink(colors[i]));
    });
    $("wave-caption").textContent = v.amplitude===0 ? "Collapsed view: all five waves coincide. Their source offsets are still retained." : locked ? "Move the wheel to slide all five curves together." : "Move one point to shift its curve. The other four stay put.";
    $("geometry-caption").textContent = v.radius===0 ? "Collapsed view: five points, one position. Increase Spread to reopen the view." : "Turn this view without changing the source or the other lenses.";
    // The composition consumes all three display adapters.
    $("composition").style.backgroundColor = M.colorHex(phases[3],v.saturation*.45,91);
    const shapes = orbit.map((p,i) => {
      const x=230+142*p.x, y=115+78*p.y;
      const wobble=M.wavePoint(phases[i],.2,v.amplitude/100,v.cycles);
      const rx=30+20*(1+wobble), ry=18+20*(1-wobble);
      return `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(rx)}" ry="${f(ry)}" transform="rotate(${phases[i]} ${f(x)} ${f(y)})" fill="${colors[i]}" fill-opacity=".88"/>`;
    });
    $("composition-shapes").innerHTML = shapes.join("");
  }
  function move(target) {
    state = M.movePoint(state,selected,target,locked);
    markCustom();
    render();
  }
  document.querySelectorAll("[data-select]").forEach(button=>button.addEventListener("click",()=>{
    selected=Number(button.dataset.select);render();announce(`Point ${letters[selected]} selected.`);
  }));
  $("phase").addEventListener("input",event=>move(Number(event.target.value)));
  $("phase").addEventListener("change",()=>announce(`Point ${letters[selected]} at ${M.phases(state)[selected]} degrees. ${locked?"Relative offsets preserved.":"Relationship updated."}`));
  $("lock").addEventListener("click",()=>{locked=!locked;render();announce(locked?"Moving together. Relative offsets are locked.":"Moving one point. Relative offsets can change.");});
  controls.forEach(id=>$(id).addEventListener("input",()=>{markCustom();render();}));
  const loadPreset = name => {
    const p=presets[name];state=M.createState(p.anchor,offsets);selected=0;locked=true;
    controls.forEach(id=>{$(id).value=p[id];});
    document.querySelectorAll("[data-preset]").forEach(el=>el.setAttribute("aria-pressed",String(el.dataset.preset===name)));
    render();
  };
  document.querySelectorAll("[data-preset]").forEach(el=>el.addEventListener("click",()=>{loadPreset(el.dataset.preset);announce(`${el.textContent.trim()} scene loaded.`);}));
  $("reset").addEventListener("click",()=>{loadPreset("studio");announce("Playful studio restored. All lenses reset.");});
  const wheel=$("wheel");
  wheel.addEventListener("pointerdown",event=>{
    if (event.button!==0 || activePointer!==null) return;
    const node=event.target.closest("[data-point]");
    if (!node) return;
    selected=Number(node.dataset.point);activePointer=event.pointerId;
    wheel.setPointerCapture(activePointer);render();event.preventDefault();
  });
  wheel.addEventListener("pointermove",event=>{
    if (event.pointerId!==activePointer) return;
    const rect=wheel.getBoundingClientRect();
    const x=event.clientX-rect.left-rect.width/2, y=event.clientY-rect.top-rect.height/2;
    if (Math.hypot(x,y)<12) return;
    move(M.mod(Math.round(Math.atan2(y,x)*180/Math.PI+90)));
  });
  const finishDrag=event=>{
    if (event.pointerId!==activePointer) return;
    if (wheel.hasPointerCapture(activePointer)) wheel.releasePointerCapture(activePointer);
    activePointer=null;
    announce(`Point ${letters[selected]} at ${M.phases(state)[selected]} degrees. ${locked?"Relative offsets preserved.":"Relationship updated."}`);
  };
  wheel.addEventListener("pointerup",finishDrag);
  wheel.addEventListener("pointercancel",finishDrag);
  wheel.addEventListener("lostpointercapture",()=>{activePointer=null;});
  loadPreset("studio");
})();
