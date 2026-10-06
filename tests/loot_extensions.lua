package.path = 'mod/?.lua;' .. package.path
local config = require('scripts.randomisedbasicloot.config')
assert(config.allowUniqueDuplicates == false)
local records, enchantments, objects = {}, {}, {}
local core = { magic = { effects = { records = setmetatable({}, { __index = function() return {} end }) },
    ENCHANTMENT_TYPE = { ConstantEffect = 3, CastOnStrike = 1 }, RANGE = { Self = 0, Touch = 1 },
    enchantments = { records = enchantments } }, getGMST = function(key)
        if key == 'fLightMaxMod' then return 1 end
        if key == 'fMedMaxMod' then return 1.5 end
        return 10
    end }
local function draft(fields)
    local result = {}
    for key, value in pairs(fields.template or {}) do result[key] = value end
    for key, value in pairs(fields) do if key ~= 'template' then result[key] = value end end
    return result
end
core.magic.enchantments.createRecordDraft = draft
local types = {}
for _, category in ipairs({ 'Armor', 'Clothing', 'Weapon' }) do
    types[category] = { records = records, createRecordDraft = draft,
        record = function(item) return records[item.recordId] end }
end
types.NPC = { objectIsInstance = function(actor) return actor.kind == 'npc' end }
types.Player = { objectIsInstance = function(actor) return actor.kind == 'player' end }
types.Actor = { isDead = function(actor) return actor.dead end,
    inventory = function(actor) return actor.inventory end, getEquipment = function() return {} end }
types.Item = { itemData = function(item) return item.data end, isRestocking = function() return false end }
local world = { players = { { kind = 'player' } } }
local nextId = 0
world.createRecord = function(record)
    nextId = nextId + 1
    record.id = '$test' .. nextId
    local target = record.effects and enchantments or records
    target[record.id] = record
    return record
end
world.createObject = function(id, count)
    local object = { recordId = id, count = count, owner = {}, data = {} }
    function object:moveInto(actor) self.container = actor end
    objects[#objects + 1] = object
    return object
end
package.preload['openmw.core'] = function() return core end
package.preload['openmw.types'] = function() return types end
package.preload['openmw.world'] = function() return world end
package.preload['scripts.randomisedbasicloot.settings'] = function()
    return { registerGroups = function() end, snapshot = function() return config end }
end
local regional = require('scripts.randomisedbasicloot.regional_flavor')
assert(regional.profiles(nil)[1] == nil)
assert(regional.profiles({ isExterior = true, region = 'Ashlands Region' })[1] == 'ash')
assert(regional.profiles({ isExterior = true, region = 'Felsaad Coast' })[1] == 'frost')
assert(regional.profiles({ isExterior = true, region = 'Solstheim, Felsaad Coast' })[1] == 'frost')
assert(regional.profiles({ name = "Arkngthand, Land's Blood Gallery" })[1] == 'dwemer')
assert(regional.profiles({ name = 'Nchuleftingth, Lower Levels' })[1] == 'dwemer')
assert(#regional.profiles({ name = 'Tureynulal, Eye of Thom Wye' }) == 2)
assert(#regional.profiles({ name = 'Dwemer-themed Player Home' }) == 0)
assert(#regional.profiles({ name = 'Arkngthandish' }) == 0)
assert(#regional.profiles({ name = 'Unknown Interior', region = 'Ashlands' }) == 0)
assert(regional.weight('resistfrost', nil, nil, { 'frost' }) == 3)
assert(regional.weight(nil, 'enchant', nil, { 'dwemer' }) == 3)
assert(regional.weight(nil, nil, 'enchantCapacity', { 'dwemer' }) == 3)
local bargains = require('scripts.randomisedbasicloot.bargain_affixes')
local catalogue = require('scripts.randomisedbasicloot.magic_catalogue')
local gaps = require('scripts.randomisedbasicloot.gap_affixes')
local tierNames, previous = {}, {}
for tier = 1, 6 do
    for _, info in ipairs({ { category = 'armor', slot = 'helmet' }, { category = 'weapon', slot = 'long_blade_one_hand' } }) do
        for _, side in ipairs({ 'prefix', 'suffix' }) do
            for _, m in ipairs(bargains.candidates(info, side, tier)) do
                tierNames[m.id] = tierNames[m.id] or {}
                assert(not tierNames[m.id][m.name], 'Each bargain tier needs a distinct name')
                tierNames[m.id][m.name] = true
                assert(#m.effects == 2)
                local boon = m.effects[1]
                for _, clean in ipairs(catalogue) do
                    if clean.effect == boon.id and clean.skill == boon.skill and clean.attribute == boon.attribute
                        and (clean.mode or 'ConstantEffect') == m.mode and clean.tiers[tostring(tier)] then
                        assert(boon.magnitude > clean.tiers[tostring(tier)].magnitude, 'Bargain must exceed clean benefit')
                    end
                end
                for _, clean in ipairs(gaps.families) do
                    if m.mode == 'ConstantEffect' and clean.effect == boon.id and clean.skill == boon.skill then
                        assert(boon.magnitude > clean.magnitudes[tier], 'Bargain must exceed clean utility benefit')
                    end
                end
                if previous[m.id] then
                    assert(boon.magnitude > previous[m.id][1] and m.effects[2].magnitude > previous[m.id][2])
                end
                previous[m.id] = { boon.magnitude, m.effects[2].magnitude }
                for _, effect in ipairs(m.effects) do
                    assert(effect.magnitude > 0)
                    assert(effect.range == (info.category == 'weapon' and 'Touch' or 'Self'))
                    assert(effect.duration == (info.category == 'weapon' and 5 or 0))
                end
            end
        end
    end
end
assert(#bargains.candidates({ category = 'weapon', slot = 'arrow' }, 'suffix', 1) == 0)
local sword = { id = 'iron longsword', type = 1, name = 'Iron Longsword', value = 40, weight = 20,
    health = 100, speed = 1.35, reach = 1, enchantCapacity = 10,
    chopMinDamage = 1, chopMaxDamage = 20, slashMinDamage = 1, slashMaxDamage = 20,
    thrustMinDamage = 1, thrustMaxDamage = 20 }
records[sword.id] = sword
local loot = require('scripts.randomisedbasicloot.loot')
local info = { category = 'weapon', slot = 'long_blade_one_hand' }
local draw = loot.draw
local function shockProbability(profiles)
    local probability
    loot.draw = function(entries, random)
        if not probability and entries[1] and type(entries[1].value) == 'table' and entries[1].value.id then
            local shock, total = 0, 0
            for _, entry in ipairs(entries) do
                total = total + entry.weight
                if entry.value.effect == 'shockdamage' then shock = shock + entry.weight end
            end
            probability = shock / total
        end
        return draw(entries, random)
    end
    loot.roll(sword, info, config, function() return 0 end, 'prefix', 1, profiles)
    loot.draw = draw
    return probability
end
local ordinary = shockProbability(nil)
assert(shockProbability({ 'dwemer' }) > ordinary)
config.regionalFlavor = false
assert(shockProbability({ 'dwemer' }) == ordinary)
config.regionalFlavor = true
local armorInfo = { category = 'armor', slot = 'helmet' }
local armor = draft({ template = sword, name = 'Helmet', baseArmor = 10 })
local sawWearable = false
for i = 0, 300 do
    local outcome = loot.roll(armor, armorInfo, config, function() return i / 301 end, 'both', 1)
    for _, m in ipairs(outcome.modifiers) do
        if m.bargain then sawWearable = true end
    end
    assert(outcome.mode == nil or outcome.mode == 'ConstantEffect')
    for _, x in ipairs(outcome.effects) do
        assert(x.range == 'Self' and x.duration == 0)
        for _, y in ipairs(outcome.effects) do
            assert(not (x.id == 'drainattribute' and y.id == 'fortifyattribute' and x.attribute == y.attribute))
            assert(not (x.id == 'weaknesstofire' and y.id == 'resistfire'))
            assert(not (x.id == 'weaknesstofrost' and y.id == 'resistfrost'))
        end
    end
end
assert(sawWearable)
-- Enumerate draw positions to exercise the real candidate/pair distributions.
local sawBargain, sawStrikePair = false, false
for i = 0, 300 do
    local r = i / 301
    local outcome = loot.roll(sword, info, config, function() return r end, 'suffix', 1, { 'dwemer' })
    for _, m in ipairs(outcome.modifiers) do
        if m.bargain then
            sawBargain = true
            assert(#outcome.effects == 2 and outcome.mode == 'CastOnStrike' and outcome.charge > 0)
        end
    end
    local both = loot.roll(sword, info, config, function() return r end, 'both', 1)
    if both.modifiers[2].bargain then
        sawStrikePair = true
        assert(#both.effects == (both.modifiers[1].effect and 3 or 2) and both.mode == 'CastOnStrike')
    end
end
assert(sawBargain and sawStrikePair, 'bargain=' .. tostring(sawBargain) .. ', strike pair=' .. tostring(sawStrikePair))
config.bargainAffixes = false
for i = 0, 100 do
    local outcome = loot.roll(sword, info, config, function() return i / 101 end, 'suffix', 1)
    assert(not outcome.modifiers[1].bargain)
end
config.bargainAffixes = true
config.dropChance, config.uniqueChance = 1, 1
local mod = dofile('mod/scripts/randomisedbasicloot/global.lua')
local function corpse(id, count)
    local item = { recordId = sword.id, count = count or 1, owner = { recordId = 'owner' }, data = { condition = 50 } }
    function item:remove(n) self.count = self.count - n end
    local inventory = { resolve = function() end, getAll = function(_, t) return t == types.Weapon and { item } or {} end }
    return { id = id, kind = 'npc', dead = true, inventory = inventory,
        cell = { name = 'Arkngthand, Hall of Centrifuge' }, isValid = function() return true end }, item
end
local actor, original = corpse('stack', 5)
mod.eventHandlers.RandomisedBasicLoot_Death(actor)
local saved = mod.engineHandlers.onSave()
assert(original.count == 0 and #saved.outcomes.stack == 5)
local seen = {}
for index, outcome in ipairs(saved.outcomes.stack) do
    assert(objects[index].data.condition > 0 and objects[index].owner.recordId == 'owner')
    assert(outcome.regionalProfiles[1] == 'dwemer')
    if index <= 4 then
        assert(outcome.uniqueId and not seen[outcome.uniqueId])
        seen[outcome.uniqueId] = true
    else
        assert(not outcome.uniqueId and outcome.layout == 'both')
    end
end
local restored = dofile('mod/scripts/randomisedbasicloot/global.lua')
restored.engineHandlers.onLoad(saved)
restored.eventHandlers.RandomisedBasicLoot_Death(actor)
assert(#objects == 5)
local nextActor = corpse('after-load')
restored.eventHandlers.RandomisedBasicLoot_Death(nextActor)
assert(restored.engineHandlers.onSave().outcomes['after-load'][1].layout == 'both')
config.allowUniqueDuplicates = true
restored.eventHandlers.RandomisedBasicLoot_Death(corpse('duplicates-enabled'))
assert(restored.engineHandlers.onSave().outcomes['duplicates-enabled'][1].uniqueId)
local availableEffects = core.magic.effects.records
core.magic.effects.records = {}
restored.eventHandlers.RandomisedBasicLoot_Death(corpse('unavailable-effects'))
assert(restored.engineHandlers.onSave().outcomes['unavailable-effects'][1].layout == 'both')
core.magic.effects.records = availableEffects
local discoveredCount = 0
for _ in pairs(restored.engineHandlers.onSave().discoveries) do discoveredCount = discoveredCount + 1 end
restored.interface.giveUniqueSamples('iron longsword')
local afterSamples = 0
for _ in pairs(restored.engineHandlers.onSave().discoveries) do afterSamples = afterSamples + 1 end
assert(discoveredCount == afterSamples and discoveredCount == 4)
local before = #objects
restored.interface.giveBargainSamples('iron longsword', 6)
assert(#objects == before + 2)
for index = before + 1, #objects do
    local e = enchantments[records[objects[index].recordId].enchant]
    assert(e.type == 1 and #e.effects == 2 and e.effects[2].range == 1)
    assert(e.effects[2].id == 'fortifyattribute' and e.effects[2].duration == 5)
end
local stored, groups = {}, {}
package.preload['openmw.storage'] = function()
    return { globalSection = function() return { get = function(_, key) return stored[key] end } end }
end
package.preload['openmw.interfaces'] = function()
    return { Settings = { registerGroup = function(group) groups[#groups + 1] = group end } }
end
config.allowUniqueDuplicates = false
local settings = dofile('mod/scripts/randomisedbasicloot/settings.lua')
settings.registerGroups()
local snapshot = settings.snapshot()
assert(not snapshot.allowUniqueDuplicates and snapshot.bargainAffixes and snapshot.regionalFlavor)
stored.allowUniqueDuplicates, stored.bargainAffixes, stored.regionalFlavor = true, false, false
snapshot = settings.snapshot()
assert(snapshot.allowUniqueDuplicates and not snapshot.bargainAffixes and not snapshot.regionalFlavor)
assert(#groups == 5)
print('PASS: unique exhaustion, stack independence, save/load, duplicate opt-in, ownership/condition, regional maps, paired bargains, native strike samples')
