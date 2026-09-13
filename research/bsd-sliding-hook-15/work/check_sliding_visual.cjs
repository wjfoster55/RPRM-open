const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const {createHash}=require('node:crypto');
const modules=process.env.CODEX_NODE_MODULES||'C:/Users/bkbee/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium}=require(path.join(modules,'playwright'));
const root=path.resolve(__dirname,'..');
(async()=>{
  const browser=await chromium.launch({headless:true});
  const page=await browser.newPage({viewport:{width:800,height:850}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.join(root,'evidence/sliding-preview.html')).href);
  const frame=page.frameLocator('iframe');
  await frame.locator('#keyring15[data-rendered="true"]').waitFor();
  const pause=()=>frame.locator('canvas').evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
  const state=()=>frame.locator('#keyring15').getAttribute('data-state');
  const canvas=()=>frame.locator('canvas').evaluate(c=>c.toDataURL());
  const changes=[];
  for(const [name,value] of [['spacing','12'],['slide','45'],['orbit','30'],['tilt','90']]){
    const before=await canvas();
    await frame.locator('#ks-'+name).fill(value);await frame.locator('#ks-'+name).dispatchEvent('input');await pause();
    const after=await canvas();if(before===after)throw Error(name+' did not change geometry/view');
    changes.push({control:name,value,state:await state(),canvas_changed:true});
  }
  for(const [name,value] of [['spacing','35'],['slide','0'],['orbit','-40'],['tilt','55']]){
    await frame.locator('#ks-'+name).fill(value);await frame.locator('#ks-'+name).dispatchEvent('input');
  }
  await pause();await page.screenshot({path:path.join(root,'evidence/sliding-desktop.png'),fullPage:true});
  const clearances=[];
  for(const angle of [12,30,35,120]){
    await frame.locator('#ks-spacing').fill(String(angle));await frame.locator('#ks-spacing').dispatchEvent('input');await pause();
    const gap=Number(await frame.locator('#keyring15').getAttribute('data-min-centerline-distance'));
    // dataset camel case uses this attribute spelling.
    const actual=await frame.locator('#keyring15').evaluate(r=>Number(r.dataset.minCenterlineDistance));
    if(!(actual>0.15))throw Error('Tube clearance failed');
    clearances.push({spacing:angle,centerline_separation:actual,combined_tube_radii:0.15});
  }
  await frame.locator('#ks-spacing').fill('12');await frame.locator('#ks-spacing').dispatchEvent('input');
  await frame.locator('#ks-orbit').fill('0');await frame.locator('#ks-orbit').dispatchEvent('input');
  await frame.locator('#ks-tilt').fill('90');await frame.locator('#ks-tilt').dispatchEvent('input');await pause();
  await page.screenshot({path:path.join(root,'evidence/sliding-edge-on.png'),fullPage:true});
  await frame.locator('#ks-spacing').fill('35');await frame.locator('#ks-spacing').dispatchEvent('input');
  await frame.locator('#ks-orbit').fill('-40');await frame.locator('#ks-orbit').dispatchEvent('input');
  await frame.locator('#ks-tilt').fill('55');await frame.locator('#ks-tilt').dispatchEvent('input');
  await page.setViewportSize({width:375,height:1050});await pause();
  const narrow=await frame.locator('#keyring15').evaluate(r=>({viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth,
    controls:[...r.querySelectorAll('input')].map(x=>({id:x.id,value:x.value,min:x.min,max:x.max}))}));
  if(narrow.scrollWidth>narrow.viewport+1)throw Error('Narrow overflow');
  await page.screenshot({path:path.join(root,'evidence/sliding-mobile.png'),fullPage:true});
  if(errors.length)throw Error(errors.join('\n'));
  const result={status:'SLIDING_AND_VIEW_CONTROLS_CHECKED',changes,clearances,narrow,errors,
    preview_sha256:createHash('sha256').update(fs.readFileSync(path.join(root,'evidence/sliding-preview.html'))).digest('hex')};
  fs.writeFileSync(path.join(root,'evidence/visual-check.json'),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify(result,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
