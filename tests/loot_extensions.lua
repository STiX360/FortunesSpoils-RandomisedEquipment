package.path = 'mod/?.lua;' .. package.path
local config = require('scripts.randomisedbasicloot.config')
assert(config.allowUniqueDuplicates == false)
local records, enchantments, objects = {}, {}, {}
local core = { contentFiles = { has = function() return false end },
    magic = { effects = { records = setmetatable({}, { __index = function()
        return { onSelf = true, onTouch = true, onTarget = true, hasMagnitude = true, hasDuration = true, baseCost = 1 }
    end }) },
    ENCHANTMENT_TYPE = { ConstantEffect = 3, CastOnStrike = 1, CastOnUse = 2 }, RANGE = { Self = 0, Touch = 1, Target = 2 },
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
types.Creature = { records = {} }
for _, category in ipairs({ 'Armor', 'Clothing', 'Weapon' }) do
    types[category] = { records = records, createRecordDraft = draft,
        record = function(item) return records[item.recordId] end }
end
types.NPC = { objectIsInstance = function(actor) return actor.kind == 'npc' end }
types.Player = { objectIsInstance = function(actor) return actor.kind == 'player' end }
types.Actor = { isDead = function(actor) return actor.dead end,
    inventory = function(actor) return actor.inventory end, getEquipment = function() return {} end }
types.Item = { itemData = function(item) return item.data end, isRestocking = function(item) return item.restocking == true end }
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
                    assert(boon.magnitude > previous[m.id][1] and m.effects[2].magnitude >= previous[m.id][2])
                end
                previous[m.id] = { boon.magnitude, m.effects[2].magnitude }
                for _, effect in ipairs(m.effects) do
                    assert(effect.magnitude > 0)
                    assert(effect.range == (info.category == 'weapon' and 'Touch' or 'Self'))
                    assert(effect.duration == (info.category == 'weapon' and 3 or 0))
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
    assert(outcome.mode == nil or outcome.mode == 'ConstantEffect' or outcome.mode == 'CastOnUse')
    for _, x in ipairs(outcome.effects) do
        assert(x.range == 'Self' and (outcome.mode ~= 'ConstantEffect' or x.duration == 0))
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
mod.engineHandlers.onNewGame()
local activeMod = mod
local function corpse(id, count, recordId)
    local item = { recordId = recordId or sword.id, count = count or 1, owner = { recordId = 'owner' }, data = { condition = 50 } }
    function item:remove(n) self.count = self.count - n end
    local inventory = { resolve = function() end, getAll = function(_, t) return t == types.Weapon and { item } or {} end }
    local actor = { id = id, kind = 'npc', dead = false, inventory = inventory,
        cell = { name = 'Arkngthand, Hall of Centrifuge' }, isValid = function() return true end }
    activeMod.eventHandlers.RandomisedBasicLoot_InitialInventory({ actor = actor, fresh = true })
    actor.dead = true
    return actor, item
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
activeMod = restored
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
    assert(e.effects[2].id == 'fortifyattribute' and e.effects[2].duration == 3)
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

local arrow = draft({ template = sword, id = 'iron arrow', type = 12, name = 'Iron Arrow',
    weight = .1, value = 1, health = 1, thrustMinDamage = 1, thrustMaxDamage = 4 })
records[arrow.id] = arrow
local function arrowCorpse(id, count, worn)
    local actor, item = corpse(id, count, arrow.id)
    item.recordId, item.id = arrow.id, id .. '-stack'
    item.data.condition = 1
    actor.equipment = worn and { [17] = item } or {}
    actor.sendEvent = function(_, name, changes)
        assert(name == 'RandomisedBasicLoot_RestoreEquipment')
        actor.changes = changes
    end
    return actor, item
end
types.Actor.getEquipment = function(actor) return actor.equipment or {} end
local ammoActor, ammoOriginal = arrowCorpse('ammo', 200, true)
before = #objects
restored.eventHandlers.RandomisedBasicLoot_Death(ammoActor)
local ammoState = restored.engineHandlers.onSave()
assert(ammoOriginal.count == 0 and #objects == before + 1)
local stack = objects[#objects]
assert(stack.count == 200 and stack.owner.recordId == 'owner')
assert(#ammoState.outcomes.ammo == 1 and not ammoState.outcomes.ammo[1].uniqueId)
assert(ammoState.outcomes.ammo[1].count == 200 and ammoState.outcomes.ammo[1].projectileGrade)
assert(ammoActor.changes[1].slot == 17 and ammoActor.changes[1].item == stack)
assert(records[stack.recordId].value == 1 and records[stack.recordId].weight == .1)
assert(records[stack.recordId].enchant == '')
local oldRecordId, grade = stack.recordId, ammoState.outcomes.ammo[1].projectileGrade
local cached = dofile('mod/scripts/randomisedbasicloot/global.lua')
cached.engineHandlers.onLoad(ammoState)
activeMod = cached
config.valueBonus = 999
cached.interface.giveRoll('iron arrow', 'prefix', grade)
assert(objects[#objects].recordId == oldRecordId, 'Canonical ammo ignores surcharge and survives reload')
assert(not pcall(cached.interface.giveRoll, 'iron arrow', 'both', 1))
assert(not pcall(cached.interface.giveUniqueSamples, 'iron arrow'))
config.dropChance = 0
local failedActor, failedOriginal = arrowCorpse('failed-ammo', 80)
before = #objects
cached.eventHandlers.RandomisedBasicLoot_Death(failedActor)
assert(failedOriginal.count == 80 and #objects == before)
config.dropChance = 1
cached.eventHandlers.RandomisedBasicLoot_Death(failedActor)
assert(failedOriginal.count == 80, 'Failed corpse rolls must not reroll')
local randomBefore = ammoState.random
local batch = dofile('mod/scripts/randomisedbasicloot/global.lua')
batch.engineHandlers.onLoad({ random = randomBefore })
activeMod = batch
batch.eventHandlers.RandomisedBasicLoot_Death(arrowCorpse('count-check', 200))
local expected = (randomBefore * 48271) % 2147483647
expected = (expected * 48271) % 2147483647
assert(batch.engineHandlers.onSave().random == expected, 'One replacement roll and one grade roll per stack')
print('PASS: whole-stack projectiles, equipped stack mapping, quantities, failed rolls, cache persistence, unique bypass, one roll per stack')

config.uniqueChance, config.valueBonus = 0, 15
local originalDraw = loot.draw
loot.draw = function(entries, random)
    for _, entry in ipairs(entries) do
        local pair = entry.value
        if type(pair) == 'table' and pair[1] and pair[2]
            and pair[1].effect == 'firedamage' and pair[2].id == 'handling' then return pair end
    end
    return originalDraw(entries, random)
end
for _, example in ipairs({ { 1.5, 11 }, { 1, 15 }, { .75, 20 } }) do
    local base = draft({ template = sword, speed = example[1] })
    local outcome = loot.roll(base, info, config, function() return 0 end, 'both', 6)
    assert(outcome.modifiers[1].effect == 'firedamage' and outcome.modifiers[2].id == 'handling')
    assert(outcome.effects[1].magnitude == example[2] and outcome.effects[1].duration == 1)
    assert(math.abs(outcome.record.speed - example[1] * 1.2) < .00001)
    assert(base.speed == example[1], 'Never mutate the original record')
end
loot.draw = originalDraw
print('PASS: real dual-affix generation uses original base speed, not generated handling speed')

local merchant, merchantStock = corpse('merchant-cap', 1)
merchantStock.count = 101
local planted = { recordId = arrow.id, count = 200, owner = {}, data = {} }
function planted:remove(n) self.count = self.count - n end
function merchant.inventory:getAll(itemType)
    return itemType == types.Weapon and { merchantStock, planted } or {}
end
merchant.dead = false
batch.eventHandlers.RandomisedBasicLoot_InitialInventory({ actor = merchant, fresh = true })
merchant.dead = true
before = #objects
batch.eventHandlers.RandomisedBasicLoot_Death(merchant)
assert(merchantStock.count == 100 and planted.count == 200 and #objects == before + 1)
assert(#batch.engineHandlers.onSave().outcomes['merchant-cap'] == 1)

local merged, mergedStack = arrowCorpse('merged-ammo-cap', 20)
mergedStack.count = 220
before = #objects
batch.eventHandlers.RandomisedBasicLoot_Death(merged)
assert(mergedStack.count == 200 and objects[#objects].count == 20 and #objects == before + 1)

local equipped, initial = corpse('worn-first', 1)
initial.id = 'initial'
local added = { recordId = sword.id, id = 'added', count = 50, owner = {}, data = { condition = 50 } }
function added:remove(n) self.count = self.count - n end
equipped.equipment = { [16] = initial }
equipped.sendEvent = function(_, _, changes) equipped.changes = changes end
function equipped.inventory:getAll(itemType)
    return itemType == types.Weapon and { added, initial } or {}
end
batch.eventHandlers.RandomisedBasicLoot_Death(equipped)
assert(initial.count == 0 and added.count == 50 and equipped.changes[1].slot == 16)

local deferred, deferredItem = corpse('allowance-reload', 1)
local trackedState = batch.engineHandlers.onSave()
local reloaded = dofile('mod/scripts/randomisedbasicloot/global.lua')
reloaded.engineHandlers.onLoad(trackedState)
deferredItem.count = 40
deferred.dead = false
reloaded.eventHandlers.RandomisedBasicLoot_InitialInventory({ actor = deferred, fresh = false })
deferred.dead = true
reloaded.eventHandlers.RandomisedBasicLoot_Death(deferred)
assert(deferredItem.count == 39, 'Reload must retain the original quantity cap')

local legacy = dofile('mod/scripts/randomisedbasicloot/global.lua')
legacy.engineHandlers.onLoad({ processed = {} })
local oldActor, oldItem = corpse('legacy-inventory', 50)
oldActor.dead = false
legacy.eventHandlers.RandomisedBasicLoot_InitialInventory({ actor = oldActor, fresh = false })
oldActor.dead = true
before = #objects
legacy.eventHandlers.RandomisedBasicLoot_Death(oldActor)
assert(oldItem.count == 50 and #objects == before)
local absentActor, absentItem = corpse('absent-snapshot', 50)
legacy.eventHandlers.RandomisedBasicLoot_Death(absentActor)
assert(absentItem.count == 50 and #objects == before)
local installed = dofile('mod/scripts/randomisedbasicloot/global.lua')
oldActor.id, oldActor.dead = 'first-install-old-save', false
installed.eventHandlers.RandomisedBasicLoot_InitialInventory({ actor = oldActor, fresh = true })
oldActor.dead = true
installed.eventHandlers.RandomisedBasicLoot_Death(oldActor)
assert(oldItem.count == 50 and #objects == before)
print('PASS: merchant/plant quantity caps, merged ammo excess retained, worn priority, snapshot immutability, reload caps, legacy and missing snapshots fail closed')

-- Global unique chance must work even when ordinary generation is disabled.
config.dropChance, config.uniqueChance, config.allowUniqueDuplicates = 0, 1, true
local globalUnique = dofile('mod/scripts/randomisedbasicloot/global.lua')
globalUnique.engineHandlers.onNewGame()
activeMod = globalUnique
local uniqueActor, uniqueItem = corpse('global-unique-without-ordinary', 1)
before = #objects
globalUnique.eventHandlers.RandomisedBasicLoot_Death(uniqueActor)
assert(uniqueItem.count == 0 and #objects == before + 1)
assert(globalUnique.engineHandlers.onSave().outcomes[uniqueActor.id][1].uniqueId)
config.uniqueChance = 0
local unchangedActor, unchangedItem = corpse('both-chances-zero', 1)
before = #objects
globalUnique.eventHandlers.RandomisedBasicLoot_Death(unchangedActor)
assert(unchangedItem.count == 1 and #objects == before)
print('PASS: global unique chance is independent of ordinary generation; zero chances preserve originals')

local progression = require('scripts.randomisedbasicloot.tier_progression')
local curve = { npcTierScaling = true, equalTierLevel = 25, tierWeights = {78,15,5,1.5,.4,.1} }
local function t6Chance(weights)
    local total = 0
    for _, w in ipairs(weights) do total = total + w end
    return weights[6] / total
end
assert(math.abs(t6Chance(progression.weights(curve, 1)) - .001) < 1e-12)
assert(math.abs(t6Chance(progression.weights(curve, 13)) - .018477464343997256) < 1e-12)
local previous = 0
for level = 1, 25 do
    local weights = progression.weights(curve, level)
    assert(t6Chance(weights) >= previous)
    previous = t6Chance(weights)
    for tier = 2, 6 do assert(weights[tier-1] >= weights[tier]) end
end
for _, level in ipairs({25,50,99}) do
    for _, weight in ipairs(progression.weights(curve, level)) do assert(weight == 1) end
end
for _, level in ipairs({0,-10}) do assert(progression.weights(curve, level)[1] == 78) end
assert(progression.weights(curve, nil)[1] == 78)
assert(progression.weights(curve, 0/0)[1] == 78)
curve.npcTierScaling = false
assert(progression.weights(curve, 99)[6] == .1)
curve.npcTierScaling, curve.equalTierLevel = true, 49
assert(math.abs(t6Chance(progression.weights(curve, 25)) - .018477464343997256) < 1e-12)
curve.tierWeights[6] = 0
assert(progression.weights(curve, 99)[6] == 0)

-- Exercise runtime NPC level without mutating configured starting weights.
types.Actor.stats = { level = function(actor) return { current = actor.level } end }
config.dropChance, config.uniqueChance, config.npcTierScaling, config.equalTierLevel = 1, 0, true, 25
local runtimeLoot = require('scripts.randomisedbasicloot.loot')
local originalRoll, capturedWeights = runtimeLoot.roll, nil
runtimeLoot.roll = function(base, info, rollConfig, ...)
    capturedWeights = rollConfig.tierWeights
    return originalRoll(base, info, rollConfig, ...)
end
local highActor = corpse('level-25-curve', 1)
highActor.level = 25
globalUnique.eventHandlers.RandomisedBasicLoot_Death(highActor)
for _, weight in ipairs(capturedWeights) do assert(weight == 1) end
assert(config.tierWeights[1] == 78 and config.tierWeights[6] == .1)
local lowActor = corpse('level-1-curve', 1)
lowActor.level = 1
globalUnique.eventHandlers.RandomisedBasicLoot_Death(lowActor)
assert(capturedWeights[1] == 78 and capturedWeights[6] == .1)
runtimeLoot.roll = originalRoll
print('PASS: NPC tier curve endpoints, midpoint, monotonicity, exclusions, toggle, configurable endpoint and corpse integration')
