const { chromium } = require('playwright');
const { pathToFileURL } = require('node:url');
const path = require('node:path');
const assert = require('node:assert/strict');
(async()=>{
  const browser=await chromium.launch({headless:true,channel:process.env.SIM_BROWSER_CHANNEL||'chrome'});
  try{
    const page=await browser.newPage({viewport:{width:1440,height:1000}});
    const errors=[];page.on('pageerror',e=>errors.push(String(e)));
    await page.goto(pathToFileURL(path.resolve('build/site/simulator.html')).href);
    assert.equal(await page.locator('#error').innerText(),'');
    assert.equal(await page.locator('#outcome').textContent(),'Base item');
    assert.equal(await page.locator('#drop,#unique,#endpoint,#scaling,#tribunal,#bloodmoon').count(),0);
    assert.match(await page.locator('#layoutOdds').innerText(),/Single 33.00%.*Dual 33.00%.*Unchanged 33.00%.*Unique 1.00%/s);
    await page.locator('#level').fill('25');
    assert.match(await page.locator('#tierOdds').innerText(),/16.667%/);
    await page.locator('#generate').click();await page.waitForFunction(()=>document.getElementById('rollCount').textContent==='1 rolls');
    assert.equal(await page.locator('#error').innerText(),'');
    await page.locator('#generate').click();await page.waitForFunction(()=>document.getElementById('rollCount').textContent==='2 rolls');
    assert.equal(await page.locator('#generate').textContent(),'Reroll');
    await page.locator('#reset').click();assert.equal(await page.locator('#outcome').textContent(),'Base item');
    await page.locator('#generate').click();await page.waitForFunction(()=>document.getElementById('rollCount').textContent==='1 rolls');
    assert.equal(await page.locator('#error').innerText(),'');
    const simulationChecks=await page.evaluate(()=>{
      function roll(id,unique=0,region='',interior='',tribunal=true,bloodmoon=true){
        return JSON.parse(fengari.load('return simulate('+[JSON.stringify(id),25,JSON.stringify(region),JSON.stringify(interior),tribunal,bloodmoon,100,unique,true,25].join(',')+')')());
      }
      fengari.load('resetSimulator()')();
      const seen=[];
      for(let i=0;i<4;i++)seen.push(roll('iron_helmet',100));
      if(new Set(seen.map(r=>r.id)).size!==4||seen.some(r=>r.layout!=='unique'))throw Error('unique repeats');
      if(roll('iron_helmet',100).layout!=='both')throw Error('unique exhaustion fallback');
      const arrow=roll('iron arrow',100);
      if(!arrow.projectileGrade||Object.keys(arrow.effects).length)throw Error('projectile rules');
      const combined=roll('iron_helmet',0,'','Dagoth Ur');
      if(!combined.profiles.includes('ash')||!combined.profiles.includes('dwemer'))throw Error('combined region');
      const bm=simBases.find(b=>b.source.includes('Bloodmoon'));
      if(roll(bm.id,0,'','',true,false).layout!=='unchanged')throw Error('disabled expansion');
      let checked=0;
      for(const b of simBases){const r=roll(b.id);if(!r.name||!r.record)throw Error('Invalid base '+b.id);checked++;}
      return checked;
    });
    assert.equal(simulationChecks,750);
    await page.screenshot({path:'build/simulator-desktop.png',fullPage:true});
    await page.setViewportSize({width:390,height:844});
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    await page.screenshot({path:'build/simulator-mobile.png',fullPage:true});
    await page.locator('#theme').selectOption('dark');
    assert.equal(await page.evaluate(()=>getComputedStyle(document.body).backgroundColor),'rgb(28, 32, 31)');
    await page.screenshot({path:'build/simulator-mobile-dark.png',fullPage:true});
    assert.deepEqual(errors,[]);
    console.log('PASS: offline initialization, defaults, tier odds, unchanged, discovery/exhaustion, reset, all 750 bases, projectile grades, combined regions, expansion gate, responsive layout and dark theme');
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
