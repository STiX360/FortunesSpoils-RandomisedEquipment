const baseGroups={
  helmet:'Helmets',cuirass:'Cuirasses',greaves:'Greaves',boots:'Boots',
  left_gauntlet:'Gauntlets & Bracers',right_gauntlet:'Gauntlets & Bracers',
  left_bracer:'Gauntlets & Bracers',right_bracer:'Gauntlets & Bracers',
  left_pauldron:'Pauldrons',right_pauldron:'Pauldrons',shield:'Shields',
  short_blade:'Short Blades',long_blade_one_hand:'Long Blades',long_blade_two_hand:'Long Blades',
  axe_one_hand:'Axes',axe_two_hand:'Axes',blunt_one_hand:'Blunt Weapons',
  blunt_two_hand_close:'Blunt Weapons',blunt_two_hand_wide:'Staves',spear:'Spears',
  bow:'Bows & Crossbows',crossbow:'Bows & Crossbows',arrow:'Projectiles',bolt:'Projectiles',thrown:'Projectiles',
  shirt:'Shirts',pants:'Pants',skirt:'Skirts',robe:'Robes',left_glove:'Gloves',right_glove:'Gloves',
  shoes:'Shoes',belt:'Belts',ring:'Rings',amulet:'Amulets'
};
const projectileSlots=['arrow','bolt','thrown'];
function currentBase(){return baseData.find(b=>b.id===$('baseSelect').value);}
function updateBaseOptions(){
  const previous=$('baseSelect').value,query=$('baseQuery').value.trim().toLowerCase(),source=$('baseSource').value;
  const list=baseData.filter(b=>(selected==='All Equipment'||baseGroups[b.slot]===selected||
    selected==='Blunt Weapons'&&b.slot==='blunt_two_hand_wide')&&(!source||b.source===source)&&
    (!query||(b.name+' '+b.id).toLowerCase().includes(query))).sort((a,b)=>a.name.localeCompare(b.name)||a.id.localeCompare(b.id));
  $('baseSelect').replaceChildren(new Option('All Bases ('+list.length+')',''));
  for(const b of list)$('baseSelect').add(new Option(b.name+' / '+b.id,b.id));
  $('baseSelect').value=list.some(b=>b.id===previous)?previous:'';
}
function baseFits(f,b){
  const projectile=projectileSlots.includes(b.slot),weapon=b.category==='weapon';
  if(projectile)return f.source==='projectile_loot.lua';
  if(f.source==='projectile_loot.lua')return false;
  if(f.kind==='Crafted'){
    if(f.field==='damage'||f.field==='speed')return weapon;
    if(f.field==='baseArmor')return b.category==='armor';
    if(f.field==='health')return b.category!=='clothing';
    if(f.field==='reach')return weapon&&!['bow','crossbow'].includes(b.slot);
    return true;
  }
  const r=f.rule||{};
  if(r.baseIds)return r.baseIds.includes(b.id);
  if(r.category&&r.category!==b.category)return false;
  if(r.wearable&&weapon)return false;
  if(r.slots&&!r.slots.includes(b.slot)&&!(r.allArmor&&b.category==='armor'))return false;
  if(f.slots&&!f.slots.includes(b.slot))return false;
  return true;
}
function effectKeys(f){
  if(f.kind==='Crafted')return [];
  if(f.effectSpecs)return f.effectSpecs.map(e=>e.id+':'+(e.skill||e.attribute||''));
  const name=f.effect.toLowerCase().replace(/[ -]/g,'');
  if(name.startsWith('fortify')){
    const target=name.slice(7);
    if(['strength','intelligence','willpower','agility','speed','endurance','personality','luck'].includes(target))return ['fortifyattribute:'+target];
    if(!['health','magicka','fatigue','attack','maximummagicka'].includes(target))return ['fortifyskill:'+target];
  }
  return [name+':'];
}
function pairFits(f,row){
  if(!$('pairSelect').value)return true;
  const [index,tier]=$('pairSelect').value.split(':').map(Number),other=data[index];
  if(f===other)return row.tier===tier;
  if(f.side===other.side)return false;
  const otherMode=other.tierModes?.[tier-1]||other.mode;
  if(row.mode!=='Record stat'&&otherMode!=='Record stat'&&row.mode!==otherMode)return false;
  const keys=effectKeys(f),otherKeys=effectKeys(other);
  if((f.runtimeId&&f.runtimeId===other.runtimeId)||keys.length===1&&otherKeys.length===1&&keys[0]===otherKeys[0])return false;
  if(f.kind==='Hybrid'||other.kind==='Hybrid'){
    const opposites={drainattribute:'fortifyattribute',drainskill:'fortifyskill',weaknesstofire:'resistfire',
      weaknesstofrost:'resistfrost',weaknesstoshock:'resistshock',weaknesstopoison:'resistpoison',blind:'nighteye'};
    for(const x of keys)for(const y of otherKeys){
      const [xi,xp]=x.split(':'),[yi,yp]=y.split(':');
      if(xp===yp&&(opposites[xi]===yi||opposites[yi]===xi))return false;
    }
  }
  return true;
}
function updatePairOptions(){
  const previous=$('pairSelect').value,b=currentBase();
  $('pairSelect').replaceChildren(new Option('Any affix',''));
  if(!b){$('pairSelect').disabled=true;return;}
  $('pairSelect').disabled=projectileSlots.includes(b.slot);
  if($('pairSelect').disabled)return;
  data.forEach((f,index)=>{
    if(!baseFits(f,b))return;
    f.tiers.forEach((cell,i)=>{
      if(cell!=='-')$('pairSelect').add(new Option(f.side+' / '+tierLabel(i+1)+' / '+tierCell(cell)[0],index+':'+(i+1)));
    });
  });
  if([...$('pairSelect').options].some(o=>o.value===previous))$('pairSelect').value=previous;
}
function baseBias(b){
  const rules=[];
  if(b.id.startsWith('bm bear ')||b.id==='extravagant_amulet_01')rules.push('Resist Frost x3');
  if(b.id==='fur_bearskin_cuirass')rules.push('Resist Frost x2');
  if(b.id==='extravagant_amulet_02')rules.push('Resist Fire x3');
  if(b.id==='ab_c_dwemeramuletclock')rules.push('Resist Shock x2');
  if(b.id==='ab_w_silverscepter')rules.push('Blunt Weapon x2');
  if(b.id.startsWith('bm wolf '))rules.push('Athletics / Sneak x2 when eligible');
  return rules.length?rules.join('; '):'Neutral';
}
function renderBase(){
  const b=currentBase();
  $('baseSummary').classList.toggle('hidden',!b);
  $('baseUniques').classList.toggle('hidden',!b);
  if(!b)return;
  const projectile=projectileSlots.includes(b.slot);
  const details=[b.source,b.category+' / '+b.slot.replaceAll('_',' '),'Base value '+b.value+' gold'];
  $('baseSummary').innerHTML='<h3>'+escape(b.name)+'</h3><p><code>'+escape(b.id)+'</code> &middot; '+escape(details.join(' / '))+'</p>'+
    '<p>Base bias: '+escape(baseBias(b))+'</p>'+
    (b.category==='armor'?'<p>Armor-skill modifiers follow the final item weight class. The corresponding Light, Medium or Heavy Armor skill uses the same tier and magnitude; these are alternatives, not three simultaneous rolls.</p>':'')+
    '<p>'+(projectile?'Stack-quality prefixes only; no suffixes or uniques.':
      'Full authoring pool. Settings and loaded effect records still apply. Enchantment-capacity affixes require a positive base capacity; installed overrides are not modeled.')+'</p>';
  if(projectile){$('baseUniques').innerHTML='';return;}
  const effectLabels={fortifyattribute:'Fortify Attribute',drainattribute:'Drain Attribute',damageattribute:'Damage Attribute',
    fortifyskill:'Fortify Skill',drainskill:'Drain Skill',absorbattribute:'Absorb Attribute',absorbskill:'Absorb Skill',
    resistfire:'Resist Fire',resistfrost:'Resist Frost',resistshock:'Resist Shock',resistpoison:'Resist Poison',
    resistmagicka:'Resist Magicka',resistcommondisease:'Resist Common Disease',resistblightdisease:'Resist Blight Disease',
    weaknesstofire:'Weakness to Fire',weaknesstofrost:'Weakness to Frost',weaknesstoshock:'Weakness to Shock',
    weaknesstopoison:'Weakness to Poison',weaknesstomagicka:'Weakness to Magicka',
    restorehealth:'Restore Health',restorefatigue:'Restore Fatigue',restoremagicka:'Restore Magicka',
    fortifyhealth:'Fortify Health',fortifyfatigue:'Fortify Fatigue',fortifymagicka:'Fortify Magicka',
    nighteye:'Night Eye',swiftswim:'Swift Swim',slowfall:'Slowfall',waterbreathing:'Water Breathing',
    waterwalking:'Water Walking',spellabsorption:'Spell Absorption',fireshield:'Fire Shield',
    frostshield:'Frost Shield',lightningshield:'Lightning Shield',detectkey:'Detect Key',
    detectenchantment:'Detect Enchantment',fortifyattack:'Fortify Attack'};
  const effectText=e=>{
    const percent=e.id.startsWith('resist')||e.id.startsWith('weakness')||['blind','sound','reflect','chameleon','spellabsorption'].includes(e.id);
    return [effectLabels[e.id]||e.id,e.attribute||e.skill,
      e.magnitude===undefined?'':e.magnitude+(percent?'%':' pts'),
      e.duration?e.duration+' sec':'',e.range||''].filter(Boolean).join(' / ');
  };
  const statLabels={weight:'Weight',value:'Value',health:'Condition',baseArmor:'Base Armor',
    enchantCapacity:'Enchant Capacity',speed:'Weapon Speed',reach:'Reach'};
  const recordText=r=>Object.entries(r||{}).map(([key,value])=>
    (statLabels[key]||key.replace(/([A-Z])/g,' $1'))+': '+value).join('; ');
  $('baseUniques').innerHTML='<h3>Unique Variants <span class="count">'+b.uniques.length+'</span></h3>'+
    (b.uniques.length?'<div class="table-wrap"><table class="unique-table"><thead><tr><th>Name / Identity</th><th>Fixed Stats</th><th>Effects / Drawbacks</th></tr></thead><tbody>'+
      b.uniques.map(u=>'<tr><td><strong>'+escape(u.name)+'</strong><p class="note">'+escape(u.identity||'')+'</p><code>'+escape(u.id)+'</code></td><td>'+escape(recordText(u.record))+
        '</td><td>'+escape(({ConstantEffect:'Constant Effect',CastOnUse:'When Used',CastOnStrike:'When Strikes'})[u.mode]||'No enchantment')+'<p>'+escape((u.effects||[]).map(effectText).join('; ')||'No spell effects')+'</p>'+
        escape((u.drawbacks||[]).join('; '))+'</td></tr>').join('')+'</tbody></table></div>':'<p class="empty">No registered unique variants.</p>');
}
for(const source of [...new Set(baseData.map(b=>b.source))])$('baseSource').add(new Option(source,source));
for(const id of ['baseSource','baseQuery','baseSelect','pairSelect'])$(id).addEventListener('input',()=>{
  if(id!=='pairSelect')$('pairSelect').value='';
  render();
});
