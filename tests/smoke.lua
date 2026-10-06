package.path = 'mod/?.lua;' .. package.path

local config = require('scripts.randomisedbasicloot.config')
local armorRecords, enchantRecords = {}, {}
local objects, generated = {}, 0
local function draft(fields)
    local result = {}
    for key, value in pairs(fields.template or {}) do result[key] = value end
    for key, value in pairs(fields) do
        if key ~= 'template' then result[key] = value end
    end
    return result
end
local core = { magic = {
    ENCHANTMENT_TYPE = { ConstantEffect = 3 }, RANGE = { Self = 0 },
    enchantments = { records = enchantRecords, createRecordDraft = draft },
} }
local types = {
    Armor = { TYPE = { Helmet = 0 }, records = armorRecords, createRecordDraft = draft },
    NPC = { objectIsInstance = function(actor) return actor.kind == 'npc' end },
    Player = { objectIsInstance = function(actor) return actor.kind == 'player' end },
    Actor = {
        inventory = function(actor) return actor.inventory end,
        isDead = function(actor) return actor.dead end,
        isDeathFinished = function(actor) return actor.finished end,
    },
}
types.Armor.record = function(value)
    return armorRecords[type(value) == 'string' and value or value.recordId]
end
local player = { kind = 'player' }
local world = { players = { player } }
world.createRecord = function(record)
    generated = generated + 1
    record.id = '$generated' .. generated
    if record.effects then enchantRecords[record.id] = record
    else armorRecords[record.id] = record end
    return record
end
world.createObject = function(id, count)
    assert(armorRecords[id], 'Unknown item')
    local object = { recordId = id, count = count }
    function object:moveInto(actor) self.owner = actor end
    objects[#objects + 1] = object
    return object
end
package.preload['openmw.core'] = function() return core end
package.preload['openmw.types'] = function() return types end
package.preload['openmw.world'] = function() return world end

local base = { id = 'test_helmet', type = 0, name = 'Iron Helmet', value = 30,
    weight = 5, health = 100, baseArmor = 10, enchantCapacity = 5,
    model = 'original.nif', icon = 'original.dds', bodyParts = { 'head' } }
armorRecords[1], armorRecords[base.id] = base, base
local function addBase(id, overrides)
    local record = draft({ template = base, id = id })
    for key, value in pairs(overrides) do record[key] = value end
    armorRecords[#armorRecords + 1], armorRecords[id] = record, record
end
addBase('expensive', { value = 500 })
addBase('enchanted', { enchant = 'existing' })
addBase('scripted', { mwscript = 'quest' })
addBase('bound', { value = 0 })
addBase('boots', { type = 1 })

local mod = dofile('mod/scripts/randomisedbasicloot/global.lua')
mod.interface.giveSamples()
assert(#objects == 3 and generated == 6, 'Three sample variants and enchantments')
local expectedNames = { 'Guarded Iron Helmet', 'Iron Helmet of Clarity', 'Iron Helmet of Embers' }
for index, object in ipairs(objects) do
    local record = armorRecords[object.recordId]
    local effect = enchantRecords[record.enchant].effects[1]
    assert(record.name == expectedNames[index] and record.value == 45)
    assert(record.bodyParts == base.bodyParts and record.model == base.model)
    assert(record.weight == base.weight and record.health == base.health)
    assert(record.baseArmor == base.baseArmor and record.enchantCapacity == base.enchantCapacity)
    assert(effect.id == config.affixes[index].effect and effect.range == 0)
    assert(effect.magnitudeMin == config.affixes[index].magnitude)
    assert(effect.magnitudeMin == effect.magnitudeMax and effect.duration == 0)
    assert(enchantRecords[record.enchant].type == 3)
end
assert(enchantRecords[armorRecords[objects[2].recordId].enchant].effects[1].affectedAttribute == 'willpower')
mod.interface.giveSamples()
assert(#objects == 6 and generated == 6, 'Variants should be reused')

local function actor(id, ids, kind, dead)
    local inventory = { items = {}, resolved = false }
    for _, recordId in ipairs(ids) do
        inventory.items[#inventory.items + 1] = { recordId = recordId, count = 1 }
    end
    function inventory:resolve() self.resolved = true end
    function inventory:getAll(itemType)
        assert(itemType == types.Armor)
        return self.items
    end
    return { id = id, inventory = inventory, kind = kind or 'npc',
        dead = dead ~= false, finished = true, isValid = function() return true end }
end
config.dropChance = 1
local corpse = actor('corpse', { 'test_helmet' })
mod.eventHandlers.RandomisedBasicLoot_Death(corpse)
assert(#objects == 7 and objects[7].owner == corpse)
assert(#corpse.inventory.items == 1, 'Original loot is preserved')
mod.eventHandlers.RandomisedBasicLoot_Death(corpse)
assert(#objects == 7, 'Duplicate events must not duplicate loot')
for _, excluded in ipairs({ 'expensive', 'enchanted', 'scripted', 'bound', 'boots' }) do
    mod.eventHandlers.RandomisedBasicLoot_Death(actor(excluded, { excluded }))
end
mod.eventHandlers.RandomisedBasicLoot_Death(actor('alive', { 'test_helmet' }, 'npc', false))
mod.eventHandlers.RandomisedBasicLoot_Death(actor('creature', { 'test_helmet' }, 'creature'))
mod.eventHandlers.RandomisedBasicLoot_Death(actor('player', { 'test_helmet' }, 'player'))
assert(#objects == 7, 'Excluded bases and actors cannot drop loot')

config.dropChance = 0
local failed = actor('failed', { 'test_helmet' })
mod.eventHandlers.RandomisedBasicLoot_Death(failed)
local saved = mod.engineHandlers.onSave()
local restored = dofile('mod/scripts/randomisedbasicloot/global.lua')
restored.engineHandlers.onLoad(saved)
config.dropChance = 1
restored.eventHandlers.RandomisedBasicLoot_Death(failed)
restored.eventHandlers.RandomisedBasicLoot_Death(corpse)
assert(#objects == 7, 'Successful and failed rolls persist through load')
restored.interface.giveSamples()
assert(generated == 6, 'Record caches persist through load')
config.enabled = false
restored.eventHandlers.RandomisedBasicLoot_Death(actor('disabled', { 'test_helmet' }))
assert(#objects == 10, 'Disabled distribution')

config.enabled = true
local activatedCorpse = actor('activated', { 'test_helmet' })
activatedCorpse.finished = false
mod.engineHandlers.onActivate(activatedCorpse)
assert(#objects == 11 and objects[11].owner == activatedCorpse,
    'Corpse activation must work without a finished death animation')
mod.engineHandlers.onActivate(activatedCorpse)
mod.eventHandlers.RandomisedBasicLoot_Death(activatedCorpse)
assert(#objects == 11, 'Activation and death events share the one-time roll')
mod.engineHandlers.onActivate(actor('living_activated', { 'test_helmet' }, 'npc', false))
assert(#objects == 11, 'Activating a living NPC cannot generate loot')

local npc = actor('local', {})
package.preload['openmw.self'] = function() return { object = npc } end
local sent = 0
core.sendGlobalEvent = function(name, value)
    assert(name == 'RandomisedBasicLoot_Death' and value == npc)
    sent = sent + 1
end
local localMod = dofile('mod/scripts/randomisedbasicloot/npc.lua')
localMod.engineHandlers.onUpdate(0.25)
assert(sent == 0)
localMod.engineHandlers.onUpdate(0.25)
localMod.engineHandlers.onUpdate(1)
assert(sent == 1, 'One death notification')
local localSaved = localMod.engineHandlers.onSave()
localMod = dofile('mod/scripts/randomisedbasicloot/npc.lua')
localMod.engineHandlers.onLoad(localSaved)
localMod.engineHandlers.onUpdate(1)
assert(sent == 1, 'Local notification flag persists')
print('PASS: samples, effects, inheritance, caches, loot exclusions, one-time rolls, save/load, NPC notifications, activation fallback')

local gaps = require('scripts.randomisedbasicloot.gap_affixes')
local function contains(candidates, id)
    for _, value in ipairs(candidates) do if value.id == id .. '_t1' then return true end end
    return false
end
assert(#gaps.families == 21)
assert(contains(gaps.candidates('clothing', 'left_glove', nil, 1, false), 'handtohand'))
assert(not contains(gaps.candidates('weapon', 'short_blade', nil, 1, true), 'handtohand'))
assert(not contains(gaps.candidates('armor', 'left_gauntlet', 'heavyarmor', 1, true), 'handtohand'))
assert(contains(gaps.candidates('armor', 'helmet', 'heavyarmor', 1, false), 'heavyarmor'))
assert(not contains(gaps.candidates('armor', 'helmet', 'lightarmor', 1, false), 'heavyarmor'))
assert(not contains(gaps.candidates('clothing', 'shirt', nil, 1, false), 'sanctuary'))
assert(contains(gaps.candidates('clothing', 'shirt', nil, 1, true), 'sanctuary'))
assert(#gaps.candidates('weapon', 'arrow', nil, 1, true) == 0)
for _, family in ipairs(gaps.families) do
    local seenNames = {}
    for tier = 1, 4 do
        assert(family.magnitudes[tier] > 0 and not seenNames[family.names[tier]])
        seenNames[family.names[tier]] = true
    end
end

local clothingRecords, weaponRecords = {}, {}
local function addType(category, records)
    return { records = records, record = function(item)
        return records[type(item) == 'string' and item or item.recordId]
    end, createRecordDraft = function(fields)
        local result = draft(fields)
        result.mockCategory = category
        return result
    end }
end
types.Clothing = addType('clothing', clothingRecords)
types.Weapon = addType('weapon', weaponRecords)
local oldCreateRecord = world.createRecord
world.createRecord = function(record)
    if not record.mockCategory then return oldCreateRecord(record) end
    generated = generated + 1
    record.id = '$generated' .. generated
    local records = record.mockCategory == 'clothing' and clothingRecords or weaponRecords
    records[record.id] = record
    return record
end
world.createObject = function(id, count)
    assert(armorRecords[id] or clothingRecords[id] or weaponRecords[id])
    local object = { recordId = id, count = count }
    function object:moveInto(owner) self.owner = owner end
    objects[#objects + 1] = object
    return object
end
clothingRecords['common_glove_left_01'] = { id = 'common_glove_left_01', type = 6,
    name = 'Common Left Glove', value = 2, model = 'glove.nif', weight = 0.1 }
weaponRecords['iron longsword'] = { id = 'iron longsword', type = 1,
    name = 'Iron Longsword', value = 40, weight = 20, speed = 1.35 }
local extended = dofile('mod/scripts/randomisedbasicloot/global.lua')
core.getGMST = function(name)
    if name == 'fLightMaxMod' then return 1 end
    if name == 'fMedMaxMod' then return 1.5 end
    return 5
end
addBase('iron_helmet', {})
local headBefore = #objects
extended.interface.giveGapSamples('iron_helmet')
local foundLight, foundClass = false, false
for index = headBefore + 1, #objects do
    local e = enchantRecords[armorRecords[objects[index].recordId].enchant].effects[1]
    if e.id == 'light' then foundLight = true end
    if e.affectedSkill == 'lightarmor' then foundClass = true end
    assert(e.affectedSkill ~= 'heavyarmor' and e.affectedSkill ~= 'mediumarmor')
end
assert(foundLight and foundClass, 'Head utility and GMST-matched armor skill must generate')
local before = #objects
extended.interface.giveGapSamples('common_glove_left_01')
local handFound = false
for index = before + 1, #objects do
    local record = clothingRecords[objects[index].recordId]
    assert(record.model == 'glove.nif' and record.weight == 0.1)
    local e = enchantRecords[record.enchant].effects[1]
    if e.affectedSkill == 'handtohand' then handFound = true end
end
assert(handFound, 'Clothing glove sample must carry native Hand-to-hand skill parameter')
before = #objects
extended.interface.giveGapSamples('iron longsword')
assert(#objects == before + 1)
local sword = weaponRecords[objects[#objects].recordId]
assert(enchantRecords[sword.enchant].effects[1].id == 'fortifyattack' and sword.speed == 1.35)
local gloveCorpse = actor('glove_corpse', {})
function gloveCorpse.inventory:getAll(itemType)
    if itemType == types.Clothing then return { { recordId = 'common_glove_left_01', count = 1 } } end
    return {}
end
before = #objects
extended.eventHandlers.RandomisedBasicLoot_Death(gloveCorpse)
assert(#objects == before + 1 and clothingRecords[objects[#objects].recordId])
extended.eventHandlers.RandomisedBasicLoot_Death(gloveCorpse)
assert(#objects == before + 1)
clothingRecords['common_glove_left_01'].mwscript = 'quest'
assert(not pcall(extended.interface.giveGapSamples, 'common_glove_left_01'), 'Scripted bases must stay protected')
print('PASS: gap slot rules, tier names, advanced gating, native skills, clothing/weapon generation, corpse rolls, script protection')
