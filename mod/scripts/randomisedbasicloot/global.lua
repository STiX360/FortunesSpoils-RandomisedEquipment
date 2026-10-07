local core = require('openmw.core')
local types = require('openmw.types')
local world = require('openmw.world')
local settings = require('scripts.randomisedbasicloot.settings')
settings.registerGroups()
local config = settings.snapshot()
local rules = require('scripts.randomisedbasicloot.item_rules')
local loot = require('scripts.randomisedbasicloot.loot')
local projectileLoot = require('scripts.randomisedbasicloot.projectile_loot')
local tierProgression = require('scripts.randomisedbasicloot.tier_progression')
local gaps = require('scripts.randomisedbasicloot.gap_affixes')
local regional = require('scripts.randomisedbasicloot.regional_flavor')
local bargains = require('scripts.randomisedbasicloot.bargain_affixes')
local availability = require('scripts.randomisedbasicloot.effect_availability')

assert(core.magic.enchantments.createRecordDraft, 'Randomised Basic Loot requires OpenMW 0.51 or newer.')
assert(config.dropChance >= 0 and config.dropChance <= 1, 'dropChance must be 0-1')
assert(config.uniqueChance >= 0 and config.uniqueChance <= 1, 'uniqueChance must be 0-1')
for _, layout in ipairs({ 'prefix', 'suffix', 'both' }) do
    assert(config.affixLayoutWeights[layout] >= 0, 'Layout weights cannot be negative')
end
for tier = 1, 6 do assert(config.tierWeights[tier] >= 0, 'Tier weights cannot be negative') end
local itemTypes = { armor = types.Armor, clothing = types.Clothing, weapon = types.Weapon }
local slots = {
    armor = { 'helmet','cuirass','left_pauldron','right_pauldron','greaves','boots','left_gauntlet','right_gauntlet','shield','left_bracer','right_bracer' },
    clothing = { 'pants','shoes','shirt','belt','robe','right_glove','left_glove','skirt','ring','amulet' },
    weapon = { 'short_blade','long_blade_one_hand','long_blade_two_hand','blunt_one_hand','blunt_two_hand_close','blunt_two_hand_wide','spear','axe_one_hand','axe_two_hand','bow','crossbow','thrown','arrow','bolt' },
}
local pool, uniques = {}, {}
for _, pack in ipairs({ 'base', 'tribunal', 'bloodmoon', 'oaab' }) do
    for category, subtypes in pairs(require('scripts.randomisedbasicloot.' .. pack .. '_items')) do
        for slot, ids in pairs(subtypes) do
            for _, id in ipairs(ids) do pool[id] = { category = category, slot = slot, pack = pack } end
        end
    end
    for id, entries in pairs(require('scripts.randomisedbasicloot.' .. pack .. '_uniques')) do uniques[id] = entries end
end
local state = { random = config.seed, enchantments = {}, helmets = {}, processed = {}, generated = {}, discoveries = {}, outcomes = {}, metadata = {},
    inventoryAllowances = {}, policyRejectedAllowances = {}, inventoryPolicyVersion = 2, baselineMode = 'new-game-required' }
local function log(message) if config.debug then print('Randomised Basic Loot: ' .. message) end end
local function random()
    state.random = (state.random * 48271) % 2147483647
    return state.random / 2147483647
end
local function exclusionReason(base, info)
    if not base then return 'missing base record' end
    if not info then return 'not in the approved static item pool' end
    local packEnabled = false
    for _, pack in ipairs(config.sourcePacks) do
        if info and info.pack == pack then packEnabled = true end
    end
    if not packEnabled then return 'source pack disabled: ' .. info.pack end
    if slots[info.category][base.type + 1] ~= info.slot then return 'record subtype differs from approved slot' end
    if base.enchant and base.enchant ~= '' then return 'base already enchanted: ' .. base.enchant end
    if base.mwscript and base.mwscript ~= '' then return 'scripted base: ' .. base.mwscript end
    if base.value <= 0 then return 'base value is zero or negative' end
    if base.value > config.maxBaseValue then return 'base value exceeds configured cap: ' .. tostring(base.value) end
    return nil
end
local function eligible(base, info) return exclusionReason(base, info) == nil end
local function captureInventory(request)
    local actor = request.actor
    if not actor or not actor:isValid() or not types.NPC.objectIsInstance(actor)
        or types.Player.objectIsInstance(actor) or state.processed[actor.id]
        or types.Actor.isDead(actor) then return end
    config = settings.snapshot()
    local rejected = state.policyRejectedAllowances[actor.id]
    if state.inventoryAllowances[actor.id] and (not rejected or config.requireNewGameInventory) then return end
    -- Compatibility mode trusts first observation, not historical inventory provenance.
    local allowance = {}
    state.inventoryAllowances[actor.id] = allowance
    if config.requireNewGameInventory and (not request.fresh or state.baselineMode == 'new-game-required') then
        state.policyRejectedAllowances[actor.id] = true
        log('no trusted initial inventory for ' .. tostring(actor.id) .. '; generation allowance is zero')
        return
    end
    state.policyRejectedAllowances[actor.id] = nil
    local ok, err = pcall(function()
        local inventory = types.Actor.inventory(actor)
        inventory:resolve()
        for category, itemType in pairs(itemTypes) do
            for _, item in ipairs(inventory:getAll(itemType)) do
                local base = itemType.record(item)
                local info = base and pool[base.id]
                if eligible(base, info) and info.category == category and not types.Item.isRestocking(item)
                    and item.count > 0 then
                    allowance[base.id] = (allowance[base.id] or 0) + item.count
                end
            end
        end
    end)
    if not ok then
        state.inventoryAllowances[actor.id] = {}
        print('Randomised Basic Loot inventory snapshot error for ' .. tostring(actor.id) .. ': ' .. tostring(err))
    else
        log('captured ' .. (config.requireNewGameInventory and 'strict initial' or 'first-observed')
            .. ' inventory for ' .. tostring(actor.id))
    end
end
local function source(baseId)
    config = settings.snapshot()
    assert(type(baseId) == 'string', 'Supply an exact base record ID.')
    baseId = string.lower(baseId)
    local info = pool[baseId]
    assert(info, 'ID is not in an enabled static source pack: ' .. baseId)
    local itemType = itemTypes[info.category]
    local base = itemType.records[baseId]
    assert(eligible(base, info), 'Base missing, scripted, enchanted, mismatched, or above the value cap: ' .. baseId)
    return base, info, itemType
end
local function serialize(value)
    if type(value) ~= 'table' then return type(value) .. ':' .. tostring(value) end
    local keys, parts = {}, {}
    for key in pairs(value) do keys[#keys + 1] = key end
    table.sort(keys, function(a, b) return tostring(a) < tostring(b) end)
    for _, key in ipairs(keys) do
        local part = serialize(key) .. '=' .. serialize(value[key])
        parts[#parts + 1] = #part .. ':' .. part
    end
    return '{' .. table.concat(parts) .. '}'
end
local function createVariant(base, info, outcome)
    local itemType = itemTypes[info.category]
    local physical = outcome.record or {}
    local effects = rules.resolveUniqueEffects(outcome.effects or {}, info.category, info.slot,
        physical.weight or base.weight, core.getGMST)
    local key = base.id .. '|' .. serialize({ name = outcome.name, record = physical, effects = effects,
        mode = outcome.mode, charge = outcome.charge, cost = outcome.cost, isAutocalc = outcome.isAutocalc,
        templateVersion = outcome.templateVersion, uniqueId = outcome.id })
    if outcome.projectileGrade then
        key = base.id .. '|projectile-quality-v1|' .. outcome.projectileGrade
    end
    local id = state.generated[key]
    if id and itemType.records[id] then return id end
    local enchantId = ''
    if #effects > 0 then
        local mode = core.magic.ENCHANTMENT_TYPE[outcome.mode]
        assert(mode, 'Unsupported enchantment mode')
        local native = {}
        for _, effect in ipairs(effects) do
            assert(core.magic.effects.records[effect.id], 'Unavailable spell effect: ' .. effect.id)
            native[#native + 1] = { id = effect.id, affectedAttribute = effect.attribute, affectedSkill = effect.skill,
                range = core.magic.RANGE[effect.range or 'Self'], duration = effect.duration or 0,
                area = effect.area or 0, magnitudeMin = effect.magnitude, magnitudeMax = effect.magnitude }
        end
        local enchantKey = serialize({ mode = outcome.mode, effects = native, charge = outcome.charge,
            cost = outcome.cost, isAutocalc = outcome.isAutocalc })
        enchantId = state.enchantments[enchantKey]
        if not enchantId or not core.magic.enchantments.records[enchantId] then
            enchantId = world.createRecord(core.magic.enchantments.createRecordDraft({ type = mode,
                effects = native, charge = outcome.charge or 0, cost = outcome.cost or 0,
                isAutocalc = outcome.isAutocalc or false })).id
            state.enchantments[enchantKey] = enchantId
        end
    end
    local draft = { template = base, name = outcome.name, enchant = enchantId }
    for field, value in pairs(physical) do draft[field] = value end
    id = world.createRecord(itemType.createRecordDraft(draft)).id
    state.generated[key] = id
    state.metadata[id] = { baseId = base.id, uniqueId = outcome.id, templateVersion = outcome.templateVersion,
        modifiers = outcome.modifiers, record = physical, effects = effects,
        projectileGrade = outcome.projectileGrade, build = 'full-dev-14-projectile-quality' }
    return id
end
local function uniqueOptions(base, includeDiscovered)
    local options = {}
    for _, entry in ipairs(uniques[base.id] or {}) do
        local valid, effects = pcall(rules.resolveUniqueEffects, entry.effects or {}, pool[base.id].category,
            pool[base.id].slot, (entry.record or {}).weight or base.weight, core.getGMST)
        if valid then
            for _, effect in ipairs(effects) do
                if not core.magic.effects.records[effect.id] then valid = false end
            end
            if #effects > 0 and not core.magic.ENCHANTMENT_TYPE[entry.mode] then valid = false end
        end
        if valid and (includeDiscovered or config.allowUniqueDuplicates or not state.discoveries[entry.id]) then
            options[#options + 1] = { value = entry, weight = entry.weight or 1 }
        end
    end
    return options
end
local function generate(base, info, layout, tier, profiles, uniqueRoll, rollConfig)
    if projectileLoot.applies(info) then return projectileLoot.roll(base, random, layout, tier) end
    if layout == 'unique' or uniqueRoll or (uniqueRoll == nil and not layout and random() < config.uniqueChance) then
        local outcome = loot.draw(uniqueOptions(base, layout == 'unique'), random)
        if outcome then return outcome end
        assert(layout ~= 'unique', 'No unique templates available for this exact base.')
        layout = 'both'
    end
    return loot.roll(base, info, rollConfig or config, random, layout, tier, profiles)
end
local function replace(item, base, info, outcome, actor, count)
    count = count or 1
    local id = createVariant(base, info, outcome)
    local object = world.createObject(id, count)
    local oldData, newData = types.Item.itemData(item), types.Item.itemData(object)
    local baseHealth = info.category ~= 'clothing' and base.health or nil
    local finalHealth = outcome.record.health or baseHealth
    if baseHealth and baseHealth > 0 and oldData.condition ~= nil then
        newData.condition = math.max(0, math.min(1, oldData.condition / baseHealth)) * finalHealth
    end
    object.owner.recordId = item.owner.recordId
    object.owner.factionId = item.owner.factionId
    object.owner.factionRank = item.owner.factionRank
    object:moveInto(actor)
    item:remove(count)
    if outcome.id then state.discoveries[outcome.id] = true end
    local outcomes = state.outcomes[actor.id] or {}
    if outcomes.recordId then outcomes = { outcomes } end
    outcomes[#outcomes + 1] = { recordId = id, baseId = base.id, layout = outcome.id and 'unique' or outcome.layout,
        uniqueId = outcome.id, templateVersion = outcome.templateVersion,
        count = count, projectileGrade = outcome.projectileGrade }
    state.outcomes[actor.id] = outcomes
    outcomes[#outcomes].regionalProfiles = regional.profiles(actor.cell)
    log('replaced ' .. count .. ' ' .. base.name .. ' with ' .. outcome.name)
    return object
end
local function onDeath(actor, reason)
    config = settings.snapshot()
    if not config.enabled or not actor or not actor:isValid() or not types.NPC.objectIsInstance(actor)
        or types.Player.objectIsInstance(actor) or not types.Actor.isDead(actor) or state.processed[actor.id] then return end
    if config.requireNewGameInventory and state.baselineMode == 'new-game-required' then
        log('strict inventory tracking requires a new game; left corpse unchanged')
        state.processed[actor.id] = true
        return
    end
    state.processed[actor.id] = true
    local allowance = state.inventoryAllowances[actor.id]
    if not allowance then
        log('no pre-interaction snapshot for ' .. tostring(actor.id) .. '; left inventory unchanged')
        return
    end
    local remaining = {}
    local okLevel, npcLevel = pcall(function() return types.Actor.stats.level(actor).current end)
    if not okLevel then npcLevel = nil end
    local rollConfig = {}
    for key, value in pairs(config) do rollConfig[key] = value end
    rollConfig.tierWeights = tierProgression.weights(config, npcLevel)
    log('tier weights for NPC ' .. tostring(actor.id) .. ' at level ' .. tostring(npcLevel or 'unknown'))
    for id, count in pairs(allowance) do remaining[id] = count end
    local inventory = types.Actor.inventory(actor)
    inventory:resolve()
    local equipment = types.Actor.getEquipment(actor)
    -- Snapshot original stacks before replacement, so generated items are never rerolled.
    local candidates = {}
    for _, category in ipairs({ 'armor', 'clothing', 'weapon' }) do
        local itemType = itemTypes[category]
        for _, item in ipairs(inventory:getAll(itemType)) do
            local base = itemType.record(item)
            local info = base and pool[base.id]
            local excluded = exclusionReason(base, info)
            if not excluded and info.category ~= category then excluded = 'record category differs from approved category' end
            if not excluded and types.Item.isRestocking(item) then excluded = 'restocking inventory item' end
            if not excluded and item.count <= 0 then excluded = 'empty inventory stack' end
            if not excluded then
                local equippedSlots = {}
                for slot, equipped in pairs(equipment) do
                    if equipped.id == item.id then equippedSlots[#equippedSlots + 1] = slot end
                end
                candidates[#candidates + 1] = { item = item, base = base, info = info,
                    count = item.count, equippedSlots = equippedSlots }
            else
                log('skipped ' .. (base and base.id or item.recordId) .. ': ' .. excluded)
            end
        end
    end
    if #candidates == 0 then log('no safe static-pool item on corpse via ' .. (reason or 'death')); return end
    table.sort(candidates, function(a, b)
        return #a.equippedSlots > 0 and #b.equippedSlots == 0
    end)
    local equipmentChanges = {}
    for _, candidate in ipairs(candidates) do
        candidate.count = math.min(candidate.count, remaining[candidate.base.id] or 0)
        remaining[candidate.base.id] = (remaining[candidate.base.id] or 0) - candidate.count
        -- Projectiles roll once per original stack; other equipment rolls per copy.
        local batch = projectileLoot.applies(candidate.info)
        for copy = 1, (batch and candidate.count > 0 and 1 or candidate.count) do
            local uniqueRoll = not batch and random() < config.uniqueChance
            if uniqueRoll or random() < config.dropChance then
                local ok, err = pcall(function()
                    local outcome = generate(candidate.base, candidate.info, nil, nil, regional.profiles(actor.cell), uniqueRoll, rollConfig)
                    if outcome then
                        local replacement = replace(candidate.item, candidate.base, candidate.info, outcome, actor,
                            batch and candidate.count or 1)
                        for _, slot in ipairs(candidate.equippedSlots) do
                            equipmentChanges[#equipmentChanges + 1] = { slot = slot, item = replacement }
                        end
                        -- A worn stack has one equipped copy, not one equipment slot per copy.
                        candidate.equippedSlots = {}
                    else log('no feasible layout for ' .. candidate.base.id .. '; left original unchanged') end
                end)
                if not ok then
                    print('Randomised Basic Loot generation error for ' .. candidate.base.id
                        .. ' copy ' .. tostring(copy) .. ': ' .. tostring(err))
                end
            end
        end
    end
    if #equipmentChanges > 0 then
        actor:sendEvent('RandomisedBasicLoot_RestoreEquipment', equipmentChanges)
    end
end
local function giveOutcome(base, info, outcome)
    local player = world.players[1]
    assert(player, 'Load a game first.')
    assert(outcome, 'No feasible layout for this item.')
    local id = createVariant(base, info, outcome)
    world.createObject(id, 1):moveInto(player)
    log('sample: ' .. outcome.name .. ' (' .. id .. ')')
end
local function giveRoll(baseId, layout, tier)
    assert(layout == nil or layout == 'prefix' or layout == 'suffix' or layout == 'both' or layout == 'unique', 'Invalid layout')
    assert(tier == nil or (tier >= 1 and tier <= 6 and tier == math.floor(tier)), 'Tier must be 1-6')
    local base, info = source(baseId)
    giveOutcome(base, info, generate(base, info, layout, tier))
end
local function giveUniqueSamples(baseId)
    local base, info = source(baseId)
    assert(not projectileLoot.applies(info), 'Projectile uniques are disabled; use giveTestKit for all three quality grades.')
    for _, entry in ipairs(uniques[base.id] or {}) do giveOutcome(base, info, entry) end
end
local function giveGapSamples(baseId)
    local base, info = source(baseId)
    assert(not projectileLoot.applies(info), 'Projectiles do not support magical affixes.')
    local class = info.category == 'armor' and rules.armorClass(info.slot, base.weight, core.getGMST) or nil
    for _, affix in ipairs(gaps.candidates(info.category, info.slot, class, config.gapTier, config.advancedGapAffixes)) do
        local effects = { { id = affix.effect, skill = affix.skill, magnitude = affix.magnitude,
            duration = affix.duration, range = 'Self' } }
        local cost, charge = 0, 0
        if affix.mode ~= 'ConstantEffect' then cost, charge = availability.budget(effects, affix.tier) end
        giveOutcome(base, info, { name = base.name .. affix.suffix, record = { value = base.value + config.valueBonus },
            mode = affix.mode, effects = effects, cost = cost, charge = charge, isAutocalc = false })
    end
end
local function giveBargainSamples(baseId, tier)
    tier = tier or 1
    assert(tier >= 1 and tier <= 6 and tier == math.floor(tier), 'Tier must be 1-6')
    local base, info = source(baseId)
    assert(not projectileLoot.applies(info), 'Projectiles do not support bargain affixes.')
    for _, side in ipairs({ 'prefix', 'suffix' }) do
        for _, m in ipairs(bargains.candidates(info, side, tier)) do
            m.tier = tier
            giveOutcome(base, info, { name = side == 'prefix' and m.name .. ' ' .. base.name or base.name .. ' ' .. m.name,
                record = { value = base.value + config.valueBonus * tier }, effects = m.effects, modifiers = { m },
                mode = m.mode, charge = m.mode == 'CastOnStrike' and 40 + tier * 20 or 0,
                isAutocalc = m.mode == 'CastOnStrike', layout = side })
        end
    end
end
local function giveTestKit(baseId)
    baseId = baseId or 'iron_helmet'
    local base, info = source(baseId)
    if projectileLoot.applies(info) then
        for grade = 1, #projectileLoot.grades do
            giveOutcome(base, info, projectileLoot.roll(base, random, 'prefix', grade))
        end
        return
    end
    for _, layout in ipairs({ 'prefix', 'suffix', 'both' }) do giveRoll(baseId, layout, 1) end
    giveUniqueSamples(baseId)
end
return {
    interfaceName = 'RandomisedBasicLoot',
    interface = { giveSamples = giveTestKit, giveTestKit = giveTestKit, giveRoll = giveRoll,
        giveUniqueSamples = giveUniqueSamples, giveGapSamples = giveGapSamples, giveBargainSamples = giveBargainSamples },
    eventHandlers = { RandomisedBasicLoot_Death = onDeath, RandomisedBasicLoot_InitialInventory = captureInventory },
    engineHandlers = {
        onNewGame = function() state.baselineMode = 'tracked' end,
        onActivate = function(object) onDeath(object, 'activation') end,
        onSave = function() return state end,
        onLoad = function(saved)
            if saved then
                for key, value in pairs(saved) do state[key] = value end
                state.baselineMode = saved.baselineMode or 'migrating'
                state.inventoryAllowances = saved.inventoryAllowances or {}
                state.policyRejectedAllowances = saved.policyRejectedAllowances or {}
                -- Old first-install blocks stored only empty allowances; mark those recoverable.
                if not saved.inventoryPolicyVersion and state.baselineMode == 'new-game-required' then
                    for id, allowance in pairs(state.inventoryAllowances) do
                        if not next(allowance) and not state.processed[id] then
                            state.policyRejectedAllowances[id] = true
                        end
                    end
                end
                state.inventoryPolicyVersion = 2
            end
        end,
    },
}
