const {chromium}=require('playwright');
const {pathToFileURL}=require('node:url');
const path=require('node:path');
const assert=require('node:assert/strict');
(async()=>{
  const browser=await chromium.launch({headless:true,channel:'chrome'});
  try{
    const page=await browser.newPage({viewport:{width:1440,height:1000}});
    const errors=[];page.on('pageerror',e=>errors.push(String(e)));
    await page.route('https://images.uesp.net/**',route=>route.abort());
    await page.goto(pathToFileURL(path.resolve('build/site/simulator.html')).href);
    await page.waitForFunction(()=>document.getElementById('imageFallback').textContent==='Image unavailable');
    assert.equal(await page.locator('#error').innerText(),'');
    assert.match(await page.locator('#imageCredit a').first().getAttribute('href'),/wiki\/File:/);
    assert.equal(await page.locator('footer #imageCredit').count(),1);
    async function checkStableControls(){
      await page.locator('#reset').click();
      const before=await page.locator('#generate').boundingBox();
      const image=await page.locator('.image-frame').boundingBox();
      assert(before.y>=image.y+image.height);
      await page.evaluate(()=>show({name:'A very long generated item name '.repeat(8),record:base.record,layout:'both',identity:'An unusually long unique description. '.repeat(20),effects:Array.from({length:8},()=>({id:'resistfire',magnitude:15})),modifiers:[]}));
      const after=await page.locator('#generate').boundingBox();
      assert.deepEqual(after,before,'Roll control must not move when item details grow');
      await page.locator('#reset').click();
    }
    await checkStableControls();
    const firstImage=await page.locator('#itemImage').getAttribute('src');
    await page.locator('#generate').click();
    await page.waitForFunction(()=>document.getElementById('rollCount').textContent==='1 rolls');
    assert.equal(await page.locator('#itemImage').getAttribute('src'),firstImage);
    const firstDetails=await page.locator('#itemName,#identity,#effects,#stats,#outcome').allTextContents();
    await page.locator('#generate').click();
    await page.waitForFunction(()=>document.getElementById('rollCount').textContent==='2 rolls');
    const discovery=await page.locator('#discovery').textContent();
    await page.locator('#history tr').last().locator('button').click();
    assert.deepEqual(await page.locator('#itemName,#identity,#effects,#stats,#outcome').allTextContents(),firstDetails);
    assert.equal(await page.locator('#rollCount').textContent(),'2 rolls');
    assert.equal(await page.locator('#discovery').textContent(),discovery);
    assert.equal(await page.locator('#history tr.selected td').first().textContent(),'1');
    const latest=page.locator('#history tr').first().locator('button');
    await latest.focus();await page.keyboard.press('Enter');
    assert.equal(await latest.getAttribute('aria-pressed'),'true');
    await page.locator('#generate').click();
    await page.waitForFunction(()=>document.getElementById('rollCount').textContent==='3 rolls');
    assert.equal(await page.locator('#history tr').count(),3);
    await page.getByRole('button',{name:'Robes',exact:true}).click();
    assert(await page.evaluate(()=>[...document.querySelectorAll('#bases option')].every(o=>basesByLabel.get(o.value).slot==='robe')));
    const missing=await page.evaluate(()=>simBases.find(b=>!b.image).id);
    await page.locator('#base').fill(missing);await page.locator('#base').dispatchEvent('change');
    assert.equal(await page.locator('#imageFallback').textContent(),'No wiki image');
    assert.equal(await page.locator('#imageCredit a').count(),0);
    await page.locator('#base').fill('iron_helmet');await page.locator('#base').dispatchEvent('change');
    await page.getByRole('button',{name:'All Equipment',exact:true}).click();
    await page.screenshot({path:'build/simulator-images-desktop.png',fullPage:true});
    for(const theme of ['light','dark']){
      await page.locator('#theme').selectOption(theme);
      await page.setViewportSize({width:390,height:844});
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
      await checkStableControls();
      await page.screenshot({path:`build/simulator-images-mobile-${theme}.png`,fullPage:true});
    }
    await page.unroute('https://images.uesp.net/**');
    // A tiny fixture validates successful-load UI separately from UESP availability.
    await page.route('https://images.uesp.net/**',route=>route.fulfill({contentType:'image/png',body:Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aY1sAAAAASUVORK5CYII=','base64')}));
    await page.reload();
    await page.waitForFunction(()=>document.getElementById('itemImage').naturalWidth>0);
    assert(await page.locator('#itemImage').isVisible());
    assert(!(await page.locator('#imageFallback').isVisible()));
    await page.getByRole('link',{name:'Rules & Profiles'}).click();
    await page.locator('#rulesView').waitFor({state:'visible'});
    assert(await page.locator('#rulesView').isVisible());
    assert.deepEqual(errors,[]);
    console.log('PASS: image attribution, failed/missing/successful images, reroll preservation, equipment filters, rules link, mobile themes and overflow');
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
