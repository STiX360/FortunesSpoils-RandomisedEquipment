const simLocations=/*SIM_LOCATIONS*/[];
const simEffectLabels=/*SIM_EFFECT_LABELS*/{};
const el=id=>document.getElementById(id);
const node=(tag,text)=>{const n=document.createElement(tag);n.textContent=text;return n;};
const basesByLabel=new Map();
const equipmentGroups={Browse:{'All Equipment':[]},Armor:{Helmets:['helmet'],Cuirasses:['cuirass'],Greaves:['greaves'],Boots:['boots'],'Gauntlets & Bracers':['left_gauntlet','right_gauntlet','left_bracer','right_bracer'],Pauldrons:['left_pauldron','right_pauldron'],Shields:['shield']},Weapons:{'Short Blades':['short_blade'],'Long Blades':['long_blade_one_hand','long_blade_two_hand'],Axes:['axe_one_hand','axe_two_hand'],'Blunt Weapons':['blunt_one_hand','blunt_two_hand_close','blunt_two_hand_wide'],Spears:['spear'],'Bows & Crossbows':['bow','crossbow'],Projectiles:['arrow','bolt','thrown']},Clothing:{Shirts:['shirt'],Pants:['pants'],Skirts:['skirt'],Robes:['robe'],Gloves:['left_glove','right_glove'],Shoes:['shoes'],Belts:['belt']},Jewelry:{Rings:['ring'],Amulets:['amulet']}};
simBases.sort((a,b)=>a.name.localeCompare(b.name)||a.id.localeCompare(b.id));
for(const b of simBases){
  const label=b.name+' / '+b.id;
  basesByLabel.set(label,b);
}
function filterBases(slots){
  const choices=simBases.filter(b=>!slots.length||slots.includes(b.slot));
  el('bases').replaceChildren(...choices.map(b=>{const option=node('option','');option.value=b.name+' / '+b.id;return option;}));
  el('baseCount').textContent=choices.length+' base items';
}
for(const [group,entries] of Object.entries(equipmentGroups)){
  el('equipmentNav').append(node('h2',group));
  const buttons=node('div','');buttons.className='group';
  for(const [label,slots] of Object.entries(entries)){
    const button=node('button',label);button.type='button';button.setAttribute('aria-pressed',String(label==='All Equipment'));
    button.addEventListener('click',()=>{for(const other of el('equipmentNav').querySelectorAll('button'))other.setAttribute('aria-pressed',String(other===button));filterBases(slots);});buttons.append(button);
  }
  el('equipmentNav').append(buttons);
}
filterBases([]);
let imageBaseId=null;
function showBaseImage(){
  if(imageBaseId===base.id)return;
  imageBaseId=base.id;
  const image=el('itemImage'),fallback=el('imageFallback');
  image.onload=null;image.onerror=null;image.hidden=true;image.removeAttribute('src');
  fallback.hidden=false;fallback.textContent=base.image?'Loading image...':'No wiki image';
  el('imageCredit').replaceChildren();
  if(!base.image)return;
  const link=node('a','Image: UESP');link.href=base.image.filePage;link.target='_blank';link.rel='noopener noreferrer';
  const source=node('a','Item source');source.href=base.image.sourcePage;source.target='_blank';source.rel='noopener noreferrer';
  el('imageCredit').append(link,source);
  image.alt=base.name+' inventory icon';
  image.onload=()=>{image.hidden=false;fallback.hidden=true;};
  image.onerror=()=>{image.hidden=true;fallback.hidden=false;fallback.textContent='Image unavailable';};
  image.src=base.image.url;
}
for(const [i,location] of simLocations.entries()){
  const option=node('option',location.label);option.value=i;el('location').append(option);
}
let base=null,rolls=0,last=null,discovered=new Set(),defaults;
const labels={weight:'Weight',value:'Value',health:'Condition',baseArmor:'Base Armor',enchantCapacity:'Enchant Capacity',speed:'Weapon Speed',reach:'Reach',
  chopMinDamage:'Chop Minimum',chopMaxDamage:'Chop Maximum',slashMinDamage:'Slash Minimum',slashMaxDamage:'Slash Maximum',thrustMinDamage:'Thrust Minimum',thrustMaxDamage:'Thrust Maximum'};
const modes={ConstantEffect:'Constant Effect',CastOnUse:'When Used',CastOnStrike:'When Strikes'};
const paramLabels={heavyarmor:'Heavy Armor',mediumarmor:'Medium Armor',lightarmor:'Light Armor',handtohand:'Hand-to-Hand',shortblade:'Short Blade',longblade:'Long Blade',bluntweapon:'Blunt Weapon',block:'Block',enchant:'Enchant',mercantile:'Mercantile',speechcraft:'Speechcraft'};
const paramLabel=value=>paramLabels[value]||(value?value[0].toUpperCase()+value.slice(1):'');
function numeric(id,min,max){const n=Number(el(id).value);return Math.max(min,Math.min(max,Number.isFinite(n)?n:min));}
function updateOdds(){
  if(!defaults)return;
  const rarity=defaults.npcTierScaling?1-Math.max(0,Math.min(1,(numeric('level',1,1000)-1)/(defaults.equalTierLevel-1))):1;
  const weights=defaults.tierWeights.map(w=>w>0?w**rarity:0),sum=weights.reduce((a,b)=>a+b,0);
  el('tierOdds').replaceChildren(...weights.map((w,i)=>{const row=node('tr','');row.append(node('td','T'+(i+1)),node('td',(w/sum*100).toFixed(3)+'%'));return row;}));
  const ammo=base&&['arrow','bolt','thrown'].includes(base.slot),u=ammo?0:defaults.uniqueChance,d=defaults.dropChance;
  const layout=defaults.affixLayoutWeights,total=layout.prefix+layout.suffix+layout.both;
  const chances=ammo?[['Quality',d],['Unchanged',1-d]]:[['Single',(1-u)*d*(layout.prefix+layout.suffix)/total],['Dual',(1-u)*d*layout.both/total],['Unchanged',(1-u)*(1-d)],['Unique',u]];
  el('layoutOdds').replaceChildren(...chances.map(([name,p])=>node('span',name+' '+(p*100).toFixed(2)+'%')));
}
function show(outcome){
  last=outcome;
  showBaseImage();
  el('item').classList.toggle('unique',outcome.layout==='unique');
  el('outcome').textContent=outcome.layout==='base'?'Base item':({both:'Prefix + Suffix',unchanged:'Unchanged',unique:'Unique',prefix:'Prefix',suffix:'Suffix'})[outcome.layout]||'Quality';
  el('itemName').textContent=outcome.name;
  el('itemId').textContent=base.id+' / '+base.source+' / '+base.slot.replaceAll('_',' ')+(outcome.armorClass?' / '+paramLabel(outcome.armorClass):'');
  el('identity').textContent=outcome.identity||outcome.reason||'';
  el('effects').replaceChildren();
  for(const m of Array.isArray(outcome.modifiers)?outcome.modifiers:[]){
    const row=node('div','');row.className='effect';
    row.append(node('strong',m.name),node('span','T'+m.tier+(m.field?' / '+(labels[m.field]||m.field)+' '+(m.percent*100).toFixed(0)+'%':'')));
    el('effects').append(row);
  }
  for(const e of Array.isArray(outcome.effects)?outcome.effects:[]){
    const row=node('div','');row.className='effect';
    const percent=/^(resist|weakness)/.test(e.id)||['reflect','chameleon','spellabsorption','blind','sound'].includes(e.id);
    const text=[simEffectLabels[e.id]||e.id,paramLabel(e.attribute||e.skill),e.magnitude===undefined?'':e.magnitude+(percent?'%':' pts'),e.duration?e.duration+' sec':'',e.range,e.area?e.area+' ft area':''].filter(Boolean).join(' / ');
    row.append(node('strong',text),node('span',modes[outcome.mode]||''));el('effects').append(row);
  }
  if(outcome.charge)el('effects').append(node('p','Charge '+outcome.charge+' / Cost '+outcome.cost));
  el('stats').replaceChildren(...Object.entries(labels).filter(([k])=>base.record[k]!==undefined).map(([key,label])=>{
    const row=node('tr',''),format=v=>Number.isInteger(v)?String(v):Number(v.toFixed(3)).toString();
    row.append(node('td',label),node('td',format(base.record[key])),node('td',format(outcome.record[key]??base.record[key])));return row;
  }));
  el('generate').textContent=rolls?'Reroll':'Generate';el('rollCount').textContent=rolls+' rolls';
  el('discovery').textContent=discovered.size+' uniques discovered';
}
function selectBase(){
  base=basesByLabel.get(el('base').value)||simBases.find(b=>b.id===el('base').value);
  el('generate').disabled=!base;el('error').textContent=base?'':'Select an included base item.';
  if(base){rolls=0;show({name:base.name,record:base.record,layout:'base'});el('history').replaceChildren();}
  updateOdds();
}
function selectHistoryRoll(row,outcome){
  show(outcome);
  for(const other of el('history').children){
    const selected=other===row;
    other.classList.toggle('selected',selected);
    other.querySelector('button').setAttribute('aria-pressed',String(selected));
  }
}
el('theme').value=document.documentElement.dataset.theme||'system';
el('theme').addEventListener('change',()=>{document.documentElement.dataset.theme=el('theme').value;try{localStorage.setItem('rbl-catalogue-theme',el('theme').value)}catch(_){}});
el('base').addEventListener('change',selectBase);
for(const id of ['level','location'])el(id).addEventListener('input',updateOdds);
el('generate').addEventListener('click',()=>{
  selectValidBase();if(!base)return;
  el('generate').disabled=true;el('error').textContent='';
  // Yield a frame so the pending state is visible during large compatible-pair draws.
  setTimeout(()=>{
    try{
      const location=simLocations[Number(el('location').value)];
      const args=[JSON.stringify(base.id),numeric('level',1,1000),JSON.stringify(location.region),JSON.stringify(location.interior),defaults.sourcePacks.includes('tribunal'),defaults.sourcePacks.includes('bloodmoon'),defaults.dropChance*100,defaults.uniqueChance*100,defaults.npcTierScaling,defaults.equalTierLevel].join(',');
      const outcome=JSON.parse(fengari.load('return simulate('+args+')')());
      rolls++;if(outcome.id)discovered.add(outcome.id);show(outcome);
      const row=node('tr',''),nameCell=node('td',''),button=node('button',outcome.name);
      button.type='button';button.className='history-item';button.setAttribute('aria-label','View roll '+rolls+': '+outcome.name);
      nameCell.append(button);row.append(node('td',String(rolls)),nameCell,node('td',el('outcome').textContent));
      row.addEventListener('click',()=>selectHistoryRoll(row,outcome));
      el('history').prepend(row);while(el('history').children.length>20)el('history').lastChild.remove();
      selectHistoryRoll(row,outcome);
    }catch(error){el('error').textContent=String(error.message||error);}
    finally{el('generate').disabled=false;}
  },20);
});
function selectValidBase(){if(!base||!([base.id,base.name+' / '+base.id].includes(el('base').value)))selectBase();}
el('reset').addEventListener('click',()=>{if(base){rolls=0;show({name:base.name,record:base.record,layout:'base'});el('history').replaceChildren();}});
el('sessionReset').addEventListener('click',()=>{fengari.load('resetSimulator()')();discovered.clear();el('reset').click();});
try{
  fengari.load(simLua)();defaults=JSON.parse(fengari.load('return simulatorDefaults()')());
  const first=simBases.find(b=>b.id==='iron_helmet')||simBases[0];el('base').value=first.name+' / '+first.id;selectBase();
}catch(error){el('error').textContent='Simulator could not initialize: '+String(error.message||error);el('generate').disabled=true;}
