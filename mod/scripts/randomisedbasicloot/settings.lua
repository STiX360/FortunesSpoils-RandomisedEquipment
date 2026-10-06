local defaults = require('scripts.randomisedbasicloot.config')
local storage = require('openmw.storage')
local M = {}
local context = 'RandomisedBasicLoot'
local groups = {}
local function group(key, name)
    local g = { key = 'SettingsGlobalRandomisedBasicLoot' .. key, name = name,
        page = context, l10n = context, permanentStorage = false, order = #groups, settings = {} }
    groups[#groups + 1] = g
    return g
end
local function add(g, key, value, min, max, integer)
    local argument
    if type(value) ~= 'boolean' then argument = { min = min, max = max, integer = integer or false } end
    g.settings[#g.settings + 1] = { key = key, name = key, default = value,
        renderer = type(value) == 'boolean' and 'checkbox' or 'number',
        argument = argument }
end
local function contains(list, value)
    for _, v in ipairs(list) do if v == value then return true end end
    return false
end
local general = group('General', 'general')
for _, key in ipairs({ 'enabled','debug','allowUniqueDuplicates','gapAffixes','advancedGapAffixes','expandedAffixes','appraisal','bargainAffixes','regionalFlavor' }) do add(general, key, defaults[key]) end
add(general, 'dropChancePercent', defaults.dropChance * 100, 0, 100)
add(general, 'uniqueChancePercent', defaults.uniqueChance * 100, 0, 100)
add(general, 'maxBaseValue', defaults.maxBaseValue, 1, 100000000, true)
add(general, 'valueBonus', defaults.valueBonus, 0, 100000, true)
add(general, 'gapTier', defaults.gapTier, 1, 6, true)
local layouts = group('Layouts', 'layouts')
for _, side in ipairs({ 'prefix','suffix','both' }) do add(layouts, side .. 'Weight', defaults.affixLayoutWeights[side], 0, 100000) end
local tiers = group('Tiers', 'tiers')
add(tiers, 'npcTierScaling', defaults.npcTierScaling)
add(tiers, 'equalTierLevel', defaults.equalTierLevel, 2, 1000, true)
for tier = 1, 6 do
    add(tiers, 'tier' .. tier .. 'Enabled', contains(defaults.enabledTiers, tier))
    add(tiers, 'tier' .. tier .. 'Weight', defaults.tierWeights[tier], 0, 100000)
end
local packs = group('Sources', 'sources')
for _, pack in ipairs({ 'base','tribunal','bloodmoon','oaab' }) do add(packs, pack .. 'Enabled', contains(defaults.sourcePacks, pack)) end
local caps = group('Caps', 'caps')
for _, key in ipairs({ 'damage','baseArmor','health','weight','speed','reach','enchantCapacity' }) do
    add(caps, key .. 'CapPercent', defaults.compositionCaps[key] * 100, 0, key == 'weight' and 99 or 1000)
end

function M.registerGroups()
    local I = require('openmw.interfaces')
    for _, g in ipairs(groups) do I.Settings.registerGroup(g) end
end

local function read(g, key)
    local value = storage.globalSection(g.key):get(key)
    for _, spec in ipairs(g.settings) do
        if spec.key == key then
            if type(spec.default) == 'boolean' then
                if type(value) == 'boolean' then return value end
                return spec.default
            end
            if type(value) ~= 'number' or value ~= value then value = spec.default end
            value = math.max(spec.argument.min, math.min(spec.argument.max, value))
            return spec.argument.integer and math.floor(value) or value
        end
    end
    error('Unknown setting: ' .. key)
end

function M.debugEnabled() return read(general, 'debug') end

function M.snapshot()
    local config = {}
    for key, value in pairs(defaults) do config[key] = value end
    for _, key in ipairs({ 'enabled','debug','allowUniqueDuplicates','gapAffixes','advancedGapAffixes','expandedAffixes','appraisal','bargainAffixes','regionalFlavor','maxBaseValue','valueBonus','gapTier' }) do
        config[key] = read(general, key)
    end
    config.dropChance = read(general, 'dropChancePercent') / 100
    config.uniqueChance = read(general, 'uniqueChancePercent') / 100
    config.affixLayoutWeights = {}
    for _, side in ipairs({ 'prefix','suffix','both' }) do config.affixLayoutWeights[side] = read(layouts, side .. 'Weight') end
    config.tierWeights, config.enabledTiers = {}, {}
    config.npcTierScaling = read(tiers, 'npcTierScaling')
    config.equalTierLevel = read(tiers, 'equalTierLevel')
    for tier = 1, 6 do
        config.tierWeights[tier] = read(tiers, 'tier' .. tier .. 'Weight')
        if read(tiers, 'tier' .. tier .. 'Enabled') then config.enabledTiers[#config.enabledTiers + 1] = tier end
    end
    config.sourcePacks = {}
    for _, pack in ipairs({ 'base','tribunal','bloodmoon','oaab' }) do
        if read(packs, pack .. 'Enabled') then config.sourcePacks[#config.sourcePacks + 1] = pack end
    end
    config.compositionCaps = {}
    for _, key in ipairs({ 'damage','baseArmor','health','weight','speed','reach','enchantCapacity' }) do
        config.compositionCaps[key] = read(caps, key .. 'CapPercent') / 100
    end
    return config
end
return M
