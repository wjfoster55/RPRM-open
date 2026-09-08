/* Three compatible scenes share one editable shadow; each has its own height. */
(() => {
  'use strict';
  const M=window.ShadowLens, F=window.ShadowFamily;
  const $=id=>document.getElementById(id), NS='http://www.w3.org/2000/svg';
  const fields=['shape','size','centerX','centerY','lightX','lightY'];
  const colors=['#88dcc1','#f0b297','#bba9f4'];
  const vertices=['#efcd76','#ef999b','#98b7f4','#90e0c5','#c5a8eb','#dfa984','#c9d68f'];
  const startingSource=()=>M.createState({size:100});
  let shared=startingSource(), depths=[2,5,8], observer='A', rays=true, drag=null, announceTimer;
  const clamp=(v,min,max)=>Math.max(min,Math.min(max,Math.round(v)));
  const xy=p=>({x:450+1.7*p.x-.9*p.y,y:350+.55*p.x+.82*p.y-2*p.z});
  const targetMap=p=>({x:170+.95*p.x,y:120+.95*p.y});
  // One fixed frame for both lights and all scenes. B's largest shift fits too.
  const readMap=p=>({x:219+.58*p.x,y:84+.58*p.y});
  const round=n=>Number(n.toFixed(3));
  function add(parent,tag,attrs={},text) {
    const node=document.createElementNS(NS,tag);
    for(const [key,value] of Object.entries(attrs))node.setAttribute(key,String(value));
    if(text!==undefined)node.textContent=text;
    parent.append(node);return node;
  }
  function polygon(parent,points,map,attrs={}) {
    return add(parent,'polygon',{points:points.map(p=>{const q=map(p);return `${round(q.x)},${round(q.y)}`;}).join(' '),...attrs});
  }
  function line(parent,p,q,map,attrs={}) {
    const a=map(p),b=map(q);
    return add(parent,'line',{x1:round(a.x),y1:round(a.y),x2:round(b.x),y2:round(b.y),...attrs});
  }
  function dot(parent,point,map,r,attrs={}) {const p=map(point);return add(parent,'circle',{cx:round(p.x),cy:round(p.y),r,...attrs});}
  function markerDots(parent,points,map,r) {points.forEach((p,i)=>dot(parent,p,map,r,{fill:vertices[i],stroke:'#10222a','stroke-width':r*.25,'pointer-events':'none'}));}
  function grid(parent,map,lo,hi,step,cls) {
    for(let t=lo;t<=hi;t+=step) {
      line(parent,{x:t,y:lo,z:0},{x:t,y:hi,z:0},map,{class:cls});
      line(parent,{x:lo,y:t,z:0},{x:hi,y:t,z:0},map,{class:cls});
    }
  }
  function drawSwatch(family) {
    const root=$('swatchContent');root.replaceChildren();
    grid(root,targetMap,-150,150,25,'view-grid');
    const group=add(root,'g',{'data-handle':'target',class:'drag-target'});
    polygon(group,family.target,targetMap,{fill:'#adcdbd','fill-opacity':.16,stroke:'#d6ecde','stroke-width':2,class:'target-polygon'});
    markerDots(group,family.target,targetMap,5);
    const center={x:shared.centerX,y:shared.centerY,z:0};
    const cp=targetMap(center);
    add(group,'path',{d:`M${cp.x-7} ${cp.y}h14 M${cp.x} ${cp.y-7}v14`,stroke:'#e7eee2','stroke-width':1.4,'pointer-events':'none'});
    const maxX=Math.max(...family.target.map(p=>p.x));
    const handle={x:maxX+14,y:shared.centerY,z:0};
    line(root,{x:maxX,y:shared.centerY,z:0},handle,targetMap,{stroke:'#abcbc0','stroke-dasharray':'2 3'});
    dot(root,handle,targetMap,6,{fill:'#152b2c',stroke:'#e7eee2','stroke-width':1.5,'pointer-events':'none'});
    dot(root,handle,targetMap,17,{'data-handle':'size',class:'size-target',fill:'transparent'});
    const hp=targetMap(handle);
    add(root,'text',{x:hp.x,y:hp.y+28,'text-anchor':'middle',class:'svg-label','font-size':10,'pointer-events':'none'},'SIZE');
    $('swatchTitle').textContent=`Shared ${M.SHAPES[shared.shape].name} shadow at (${shared.centerX}, ${shared.centerY}), scale ${shared.size} percent. Drag the polygon to move all three scenes; the round handle changes size. Sliders provide the same edits.`;
  }
  function drawScene(scene,index) {
    const root=$('stageContent'+index);root.replaceChildren();
    const color=colors[index];
    polygon(root,[{x:-130,y:-130,z:0},{x:130,y:-130,z:0},{x:130,y:130,z:0},{x:-130,y:130,z:0}],xy,{fill:'#193a34',stroke:'#396358','stroke-width':1.4});
    grid(root,xy,-125,125,25,'floor-grid');
    polygon(root,scene.shadow,xy,{fill:color,'fill-opacity':.24,stroke:color,'stroke-width':2,class:'ground-shadow'});
    markerDots(root,scene.shadow,xy,5);
    if(rays) {
      scene.shadow.forEach((p,i)=>{
        const next=scene.shadow[(i+1)%scene.shadow.length];
        polygon(root,[scene.light,p,next],xy,{fill:'#ffdfac',opacity:.022,'pointer-events':'none'});
        line(root,scene.light,p,xy,{stroke:'#e8c77f','stroke-width':1.6,'stroke-opacity':.48});
      });
    }
    line(root,{...scene.light,z:0},scene.light,xy,{stroke:'#d0b77b','stroke-opacity':.35,'stroke-dasharray':'5 8'});
    dot(root,{...scene.light,z:0},xy,5,{fill:'none',stroke:'#d0b77b','stroke-opacity':.5});
    const cutout=add(root,'g',{'data-handle':'height','data-scene':index,class:'drag-target'});
    polygon(cutout,scene.cutout,xy,{fill:color,'fill-opacity':.94,stroke:'#f1ece1','stroke-width':2,class:'cutout'});
    markerDots(cutout,scene.cutout,xy,6);
    polygon(cutout,scene.cutout,xy,{fill:'transparent',stroke:'transparent','stroke-width':30});
    // Both lamp positions are always shown. The observer switch changes only readouts.
    dot(root,scene.probe,xy,7,{fill:'#bba9f4','fill-opacity':.45,stroke:'#cfc2fa','stroke-width':1.5});
    const bp=xy(scene.probe);
    add(root,'text',{x:bp.x+17,y:bp.y+6,fill:'#cfc2fa','font-size':18,'pointer-events':'none'},'B');
    dot(root,scene.light,xy,25,{fill:'#f8d994',opacity:.07,'pointer-events':'none'});
    dot(root,scene.light,xy,15,{fill:'#f8d994',opacity:.14,'pointer-events':'none'});
    const lamp=add(root,'g',{'data-handle':'light',class:'drag-target'});
    dot(lamp,scene.light,xy,9,{fill:'#ffe5ad',stroke:'#fff3d6','stroke-width':1.3});
    dot(lamp,scene.light,xy,29,{fill:'transparent'});
    const ap=xy(scene.light);
    add(root,'text',{x:ap.x+17,y:ap.y+6,fill:'#ffe5ad','font-size':18,'pointer-events':'none'},'A');
    $('stageTitle'+index).textContent=`Scene ${index+1}: cutout at height ${depths[index]*10}, size ${100-depths[index]*10}% of the shared shadow. It is a separate scene fitted to the same target. Drag its cutout to change this height or its lamp to move all lamps.`;
  }
  function drawObservation(scene,read,index) {
    const root=$('observedContent'+index);root.replaceChildren();
    grid(root,readMap,-350,300,50,'view-grid');
    if(observer==='B')polygon(root,scene.shadow,readMap,{fill:'none',stroke:'#8eafa3','stroke-width':1.4,'stroke-dasharray':'4 4',class:'a-reference'});
    polygon(root,read.polygons[index],readMap,{fill:colors[index],'fill-opacity':.48,stroke:colors[index],'stroke-width':2,class:'observed-shadow'});
    markerDots(root,read.polygons[index],readMap,3.1);
    if(observer==='B')line(root,{x:shared.centerX,y:shared.centerY,z:0},{x:shared.centerX+read.shifts[index].x,y:shared.centerY+read.shifts[index].y,z:0},readMap,{stroke:colors[index],'stroke-width':1.2,'stroke-dasharray':'2 3'});
    $('observationLabel'+index).textContent=`Shadow under ${observer}`;
    $('match'+index).textContent=observer==='A'?'= shared swatch':`Height ${read.recoveredDepths[index]*10} revealed`;
  }
  function render() {
    const family=F.build(shared,depths), read=F.observe(family,observer);
    for(const key of fields) {
      $(key).value=shared[key];
      const out=$(key+'Out');if(out)out.textContent=key==='size'?`${shared[key]}%`:String(shared[key]);
    }
    $('viewA').setAttribute('aria-pressed',String(observer==='A'));
    $('viewB').setAttribute('aria-pressed',String(observer==='B'));
    $('raysToggle').setAttribute('aria-pressed',String(rays));
    document.body.dataset.observer=observer;
    $('relationStatus').textContent=`3 scenes · ${read.groups} ${read.groups===1?'matching shadow':'different shadows'}`;
    $('relationHint').textContent=observer==='A'?'Every cutout is fitted to the swatch above. Change the swatch to move all three scenes together.':read.allMatch?'These heights are equal, so B also sees a match. Change one height to separate its shadow.':'Same scenes, different light. B separates their shadows by height; the dashed outlines retain A.';
    drawSwatch(family);
    family.scenes.forEach((scene,i)=>{
      $('depth'+i).value=depths[i];
      $('depth'+i).setAttribute('aria-valuetext',`Height ${depths[i]*10} out of 100`);
      $('depthOut'+i).textContent=String(depths[i]*10);
      $('cutoutScale'+i).textContent=`Cutout size ${100-depths[i]*10}% of shadow`;
      drawScene(scene,i);drawObservation(scene,read,i);
    });
  }
  function say(text) {clearTimeout(announceTimer);announceTimer=setTimeout(()=>{$('live').textContent=text;},160);}
  function change(patch,source='swatch') {
    try {
      shared=M.update(shared,patch);render();$('error').textContent='';
      $('activity').textContent=source==='light'?'Shared lamp moved · all 3 cutouts refitted · shadow A held':'Shared swatch changed · all 3 scenes updated';
    } catch(error) {$('error').textContent=error.message;}
  }
  function changeHeight(index,value) {
    const next=depths.slice();next[index]=value;
    try {F.build(shared,next);depths=next;render();$('error').textContent='';$('activity').textContent=`Scene ${index+1} refitted at height ${10*value} · its shadow A still matches`;}catch(error){$('error').textContent=error.message;}
  }
  for(const key of fields) {
    $(key).addEventListener('input',()=>change({[key]:Number($(key).value)},key.startsWith('light')?'light':'swatch'));
    $(key).addEventListener('change',()=>say($('activity').textContent));
  }
  for(let i=0;i<3;i++) {
    $('depth'+i).addEventListener('input',()=>changeHeight(i,Number($('depth'+i).value)));
    $('depth'+i).addEventListener('change',()=>say($('activity').textContent));
  }
  for(const name of ['A','B'])$('view'+name).addEventListener('click',()=>{observer=name;render();say($('relationStatus').textContent);});
  $('raysToggle').addEventListener('click',()=>{rays=!rays;render();});
  $('reset').addEventListener('click',()=>{shared=startingSource();depths=[2,5,8];observer='A';rays=true;drag=null;render();$('activity').textContent='Shared swatch connected to 3 scenes';say('Default shared swatch and three heights restored.');});
  function point(event,surface) {const matrix=surface.getScreenCTM();return matrix?new DOMPoint(event.clientX,event.clientY).matrixTransform(matrix.inverse()):null;}
  for(const surface of [$('swatch'),$('stage0'),$('stage1'),$('stage2')]) {
    surface.addEventListener('pointerdown',event=>{
      if(event.button!==0||drag)return;
      const handle=event.target.closest('[data-handle]');if(!handle)return;
      const p=point(event,surface);if(!p)return;
      drag={id:event.pointerId,surface,p,kind:handle.dataset.handle,index:Number(handle.dataset.scene),shared,depths:depths.slice()};
      surface.setPointerCapture(event.pointerId);event.preventDefault();
    });
    surface.addEventListener('pointermove',event=>{
      if(!drag||drag.id!==event.pointerId||drag.surface!==surface)return;
      const p=point(event,surface);if(!p)return;
      const dx=p.x-drag.p.x,dy=p.y-drag.p.y,s=drag.shared;
      if(drag.kind==='target')change({centerX:clamp(s.centerX+dx/.95,-50,50),centerY:clamp(s.centerY+dy/.95,-50,50)});
      if(drag.kind==='size') {
        const rightEdge=Math.max(...M.SHAPES[s.shape].vertices.map(p=>p.x));
        change({size:clamp(s.size+dx/(.95*rightEdge/100),40,120)});
      }
      if(drag.kind==='height')changeHeight(drag.index,clamp(drag.depths[drag.index]-dy/26,2,8));
      if(drag.kind==='light') {
        const det=1.7*.82+.9*.55;
        change({lightX:clamp(s.lightX+(.82*dx+.9*dy)/det,-80,80),lightY:clamp(s.lightY+(-.55*dx+1.7*dy)/det,-80,80)},'light');
      }
    });
    const end=event=>{
      if(!drag||drag.id!==event.pointerId||drag.surface!==surface)return;
      drag=null;if(surface.hasPointerCapture(event.pointerId))surface.releasePointerCapture(event.pointerId);
      say($('activity').textContent);
    };
    surface.addEventListener('pointerup',end);surface.addEventListener('pointercancel',end);
    surface.addEventListener('lostpointercapture',()=>{if(drag?.surface===surface)drag=null;});
  }
  render();
})();
