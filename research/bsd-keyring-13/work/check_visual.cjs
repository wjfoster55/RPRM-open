const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {createHash} = require('node:crypto');
const runtime = process.env.CODEX_NODE_MODULES || 'C:/Users/bkbee/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium} = require(path.join(runtime,'playwright'));
const root = path.resolve(__dirname,'..');
(async()=>{
  const browser = await chromium.launch({headless:true});
  const page = await browser.newPage({viewport:{width:800,height:650}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.join(root,'evidence/keyring-preview.html')).href);
  const frame = page.frameLocator('iframe');
  await frame.locator('#keyring13[data-rendered="true"]').waitFor();
  const before = await frame.locator('canvas').evaluate(c=>c.toDataURL());
  await frame.locator('#kr-orbit').fill('35');
  await frame.locator('#kr-orbit').dispatchEvent('input');
  const after = await frame.locator('canvas').evaluate(c=>c.toDataURL());
  if(before===after) throw Error('Rotation did not change canvas');
  await frame.locator('#kr-orbit').fill('0');
  await frame.locator('#kr-orbit').dispatchEvent('input');
  await page.screenshot({path:path.join(root,'evidence/keyring-desktop.png'),fullPage:true});
  await page.setViewportSize({width:375,height:700});
  await frame.locator('canvas').evaluate(c=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
  const fits = await frame.locator('#keyring13').evaluate(r=>({
    rootWidth:r.getBoundingClientRect().width,
    viewport:window.innerWidth,
    scrollWidth:document.documentElement.scrollWidth,
    rendered:r.dataset.rendered,
    labels:[...r.querySelectorAll('label')].map(e=>e.textContent.trim())
  }));
  if(fits.scrollWidth>fits.viewport+1) throw Error('Narrow viewport horizontal overflow');
  await page.screenshot({path:path.join(root,'evidence/keyring-mobile.png'),fullPage:true});
  if(errors.length) throw Error(errors.join('\n'));
  const result={status:'VISUAL_RENDER_AND_ROTATION_CHECKED',errors,canvas_changed_after_rotation:true,narrow_view:fits,
    preview_sha256:createHash('sha256').update(fs.readFileSync(path.join(root,'evidence/keyring-preview.html'))).digest('hex')};
  fs.writeFileSync(path.join(root,'evidence/visual-check.json'),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify(result,null,2));
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
