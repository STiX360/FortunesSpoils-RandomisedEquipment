local js = require('js')
local types = {}
for kind, records in pairs(simSnapshot.available) do types[kind] = { records = records } end
local sourceEnabled = { ['Tribunal.esm'] = true, ['Bloodmoon.esm'] = true }
local core = {
    magic = { effects = { records = simSnapshot.effects },
        ENCHANTMENT_TYPE = { ConstantEffect = 3, CastOnStrike = 1, CastOnUse = 2 } },
    getGMST = function(key) return simSnapshot.gmsts[key] end,
    contentFiles = { has = function(name) return sourceEnabled[name] == true end },
}
package.preload['openmw.core'] = function() return core end
package.preload['openmw.types'] = function() return types end
local config = require('scripts.randomisedbasicloot.config')
local loot = require('scripts.randomisedbasicloot.loot')
local progression = require('scripts.randomisedbasicloot.tier_progression')
local regional = require('scripts.randomisedbasicloot.regional_flavor')
local rules = require('scripts.randomisedbasicloot.item_rules')
local projectiles = require('scripts.randomisedbasicloot.projectile_loot')
local discoveries = {}
local function random() return js.global.Math:random() end
local function json(value)
    if type(value) == 'string' then return js.global.JSON:stringify(value) end
    if type(value) ~= 'table' then return tostring(value) end
    local entries = {}
    if #value > 0 then
        for _, entry in ipairs(value) do entries[#entries + 1] = json(entry) end
        return '[' .. table.concat(entries, ',') .. ']'
    end
    for key, entry in pairs(value) do entries[#entries + 1] = json(tostring(key)) .. ':' .. json(entry) end
    return '{' .. table.concat(entries, ',') .. '}'
end
function resetSimulator() discoveries = {} end
function simulatorDefaults() return json(config) end
function simulate(baseId, level, region, interior, tribunal, bloodmoon, drop, unique, scaling, endpoint)
    local baseInfo = assert(simBases[baseId], 'Unknown base')
    local base = baseInfo.record
    sourceEnabled['Tribunal.esm'], sourceEnabled['Bloodmoon.esm'] = tribunal, bloodmoon
    local cfg = {}
    for key, value in pairs(config) do cfg[key] = value end
    cfg.dropChance, cfg.uniqueChance = drop / 100, unique / 100
    cfg.npcTierScaling, cfg.equalTierLevel = scaling, endpoint
    cfg.sourcePacks = {'base', 'oaab'}
    if tribunal then cfg.sourcePacks[#cfg.sourcePacks + 1] = 'tribunal' end
    if bloodmoon then cfg.sourcePacks[#cfg.sourcePacks + 1] = 'bloodmoon' end
    cfg.tierWeights = progression.weights(cfg, level)
    local profiles = regional.profiles({ isExterior = interior == '', region = region, name = interior })
    local info = { category = baseInfo.category, slot = baseInfo.slot }
    local outcome, uniqueRoll, fallback
    if base.mwscript ~= '' or base.enchant ~= '' or base.value <= 0 or base.value > cfg.maxBaseValue then
        return json({ name = base.name, record = base, layout = 'unchanged', reason = 'Base excluded by runtime eligibility rules' })
    end
    if baseInfo.source:find('Tribunal') and not tribunal or baseInfo.source:find('Bloodmoon') and not bloodmoon then
        return json({ name = base.name, record = base, layout = 'unchanged', reason = 'Source pack disabled' })
    end
    if not projectiles.applies(info) then uniqueRoll = random() < cfg.uniqueChance end
    if uniqueRoll then
        local options = {}
        for _, entry in ipairs(baseInfo.uniques) do
            local valid, effects = pcall(rules.resolveUniqueEffects, entry.effects or {}, info.category,
                info.slot, entry.record.weight or base.weight, core.getGMST)
            if valid then
                for _, e in ipairs(effects) do if not core.magic.effects.records[e.id] then valid = false end end
                if #effects > 0 and not core.magic.ENCHANTMENT_TYPE[entry.mode] then valid = false end
            end
            if valid and (cfg.allowUniqueDuplicates or not discoveries[entry.id]) then
                options[#options + 1] = { value = { name = entry.name, id = entry.id, record = entry.record,
                    effects = effects, mode = entry.mode, charge = entry.charge, cost = entry.cost,
                    identity = entry.identity, drawbacks = entry.drawbacks,
                    layout = 'unique' }, weight = entry.weight or 1 }
            end
        end
        outcome = loot.draw(options, random)
        if outcome then discoveries[outcome.id] = true else fallback = 'both' end
    end
    if not outcome and (uniqueRoll or random() < cfg.dropChance) then
        outcome = loot.roll(base, info, cfg, random, fallback, nil, profiles)
    end
    outcome = outcome or { name = base.name, record = {}, effects = {}, layout = 'unchanged' }
    local record = {}
    for key, value in pairs(base) do record[key] = value end
    for key, value in pairs(outcome.record) do record[key] = value end
    outcome.record, outcome.profiles, outcome.tierWeights = record, profiles, cfg.tierWeights
    if info.category == 'armor' then outcome.armorClass = rules.armorClass(info.slot, record.weight, core.getGMST) end
    return json(outcome)
end
