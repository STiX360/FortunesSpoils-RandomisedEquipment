local core = require('openmw.core')
local rules = require('scripts.randomisedbasicloot.item_rules')
local gaps = require('scripts.randomisedbasicloot.gap_affixes')
local catalogue = require('scripts.randomisedbasicloot.magic_catalogue')
local expanded = require('scripts.randomisedbasicloot.expanded_catalogue')
local availability = require('scripts.randomisedbasicloot.effect_availability')
local bargains = require('scripts.randomisedbasicloot.bargain_affixes')
local regional = require('scripts.randomisedbasicloot.regional_flavor')
local weaponAffixes = require('scripts.randomisedbasicloot.weapon_affixes')
local projectileLoot = require('scripts.randomisedbasicloot.projectile_loot')
local M = {}
local projectile = { arrow = true, bolt = true, thrown = true }
local bear = {}
local wolf = {}
for _, slot in ipairs({ 'helmet', 'cuirass', 'greaves', 'boots', 'left gauntlet', 'right gauntlet', 'left pauldron', 'right pauldron', 'shield' }) do
    bear['bm bear ' .. slot] = true
    wolf['bm wolf ' .. slot] = true
end
local function contains(list, value)
    for _, entry in ipairs(list or {}) do if entry == value then return true end end
    return false
end
local function fits(f, base, info)
    if f.baseIds then return contains(f.baseIds, base.id) end
    if f.category and f.category ~= info.category then return false end
    if f.wearable and info.category == 'weapon' then return false end
    if f.melee and (projectile[info.slot] or info.slot == 'bow' or info.slot == 'crossbow') then return false end
    return not f.slots or contains(f.slots, info.slot) or (f.allArmor and info.category == 'armor')
end
local function bias(effect, skill, base, attribute)
    if effect == 'resistfrost' and (bear[base.id] or base.id == 'extravagant_amulet_01') then return 3 end
    if effect == 'resistfrost' and base.id == 'fur_bearskin_cuirass' then return 2 end
    if effect == 'resistfire' and base.id == 'extravagant_amulet_02' then return 3 end
    if effect == 'resistshock' and base.id == 'ab_c_dwemeramuletclock' then return 2 end
    if skill == 'bluntweapon' and base.id == 'ab_w_silverscepter' then return 2 end
    if wolf[base.id] and (skill == 'athletics' or skill == 'sneak') then return 2 end
    if skill == 'alteration' or skill == 'conjuration' or skill == 'destruction'
        or skill == 'illusion' or skill == 'mysticism' or skill == 'restoration' then return 1 / 6 end
    if effect == 'fortifyattribute' and attribute == 'luck' then return 0.1 end
    return 1
end
local function rounded(value, integer)
    local scale = integer and 1 or 10000
    return math.floor(value * scale + 0.5) / scale
end
local families = {
    { id = 'edge', side = 'prefix', field = 'damage', values = { .05,.08,.12,.18,.25,.35 }, names = { 'Honed','Keen','Sharpened','Razor-edged','Murderous','Peerless' } },
    { id = 'construction', side = 'prefix', field = 'baseArmor', values = { .05,.08,.12,.18,.25,.35 }, names = { 'Hardened','Tempered','Reinforced','Adamantine','Unyielding','Impregnable' } },
    { id = 'durability', side = 'prefix', field = 'health', values = { .1,.2,.3,.45,.6,.8 }, names = { 'Sound','Durable','Enduring','Resilient','Ironbound','Everlasting' } },
    { id = 'lightwork', side = 'prefix', field = 'weight', values = { -.05,-.08,-.12,-.18,-.25,-.35 }, names = { 'Trimmed','Lightworked','Streamlined','Featherforged','Gossamer','Zephyr-forged' } },
    { id = 'appraisal', side = 'suffix', field = 'value', values = { .1,.2,.35,.5,.75,1 }, names = { 'of Polish','of Ornament','of Gilding','of Opulence','of Regality','of Splendor' } },
    { id = 'handling', side = 'suffix', field = 'speed', values = { .02,.04,.07,.1,.15,.2 }, names = { 'of Readiness','of Quick Handling','of Quickness','of Alacrity','of the Swift Stroke','of the Flurry' } },
    { id = 'measure', side = 'suffix', field = 'reach', values = { .01,.02,.03,.05,.07,.1 }, names = { 'of Measure','of Extension','of Long Measure','of Long Reach','of the Outstretched Hand','of the Far Point' } },
    { id = 'receptivity', side = 'suffix', field = 'enchantCapacity', values = { .05,.1,.15,.25,.4,.6 }, names = { 'of Receptivity','of Attunement','of Imbuing','of Binding','of the Rune Vessel','of the Deep Vessel' } },
}

function M.physical(base, modifiers, config)
    local sums = {}
    for _, m in ipairs(modifiers) do
        if m.field then sums[m.field] = (sums[m.field] or 0) + m.percent end
    end
    local result = {}
    local caps = config.compositionCaps
    for field, percent in pairs(sums) do
        if field == 'weight' then percent = math.max(percent, -caps.weight)
        elseif caps[field] then percent = math.min(percent, caps[field]) end
        if field == 'damage' then
            for _, attack in ipairs({ 'chop', 'slash', 'thrust' }) do
                for _, limit in ipairs({ 'Min', 'Max' }) do
                    local key = attack .. limit .. 'Damage'
                    result[key] = math.min(255, rounded(base[key] * (1 + percent), true))
                end
            end
        else
            local integer = field == 'baseArmor' or field == 'health' or field == 'value'
            result[field] = rounded(base[field] * (1 + percent), integer)
        end
    end
    return result
end

local function tierCandidates(base, info, side, tier, physical, config, profiles)
    local result, seen = {}, {}
    local function add(m)
        if seen[m.id] then return end
        if m.effect and not core.magic.effects.records[m.effect] then return end
        for _, effect in ipairs(m.effects or {}) do
            if not core.magic.effects.records[effect.id] then return end
        end
        if info.category == 'weapon' and not weaponAffixes.resolve(m, info.slot, core.magic.effects.records, base.speed) then return end
        seen[m.id] = true
        m.tier = tier
        m.weight = (m.weight or 1) * bias(m.effect, m.skill, base, m.attribute)
            * regional.weight(m.effect, m.skill, m.field, profiles)
        if m.bargain then m.weight = m.weight * 0.35 end
        result[#result + 1] = m
    end
    for _, f in ipairs(families) do
        local ammo = projectile[info.slot]
        local allowed = f.side == side
        if f.ammo then allowed = allowed and ammo
        elseif f.field == 'damage' then allowed = allowed and info.category == 'weapon'
        elseif f.field == 'baseArmor' then allowed = allowed and info.category == 'armor'
        elseif f.field == 'health' then allowed = allowed and info.category ~= 'clothing' and not ammo
        elseif f.field == 'speed' then allowed = allowed and info.category == 'weapon' and not ammo
        elseif f.field == 'reach' then allowed = allowed and info.category == 'weapon' and not ammo and info.slot ~= 'bow' and info.slot ~= 'crossbow'
        elseif f.field == 'enchantCapacity' then allowed = allowed and base.enchantCapacity > 0 and not ammo
        elseif f.field == 'value' then allowed = allowed and config.appraisal end
        if allowed then add({ id = f.id, name = f.names[tier], field = f.field, percent = f.values[tier] }) end
    end
    for _, f in ipairs(catalogue) do
        local t = f.tiers[tostring(tier)]
        if t and f.side == side and fits(f, base, info) then
            add({ id = f.id, name = t.name, effect = f.effect, skill = f.skill,
                attribute = f.attribute, magnitude = t.magnitude, mode = f.mode or 'ConstantEffect' })
        end
    end
    if config.expandedAffixes then
        for _, f in ipairs(expanded) do
            local t = f.tiers[tostring(tier)]
            if t and f.side == side and fits(f, base, info) and availability.available(f, config) then
                add({ id = f.id, name = t.name, effect = f.effect, skill = f.skill,
                    attribute = f.attribute, magnitude = t.magnitude, mode = t.mode or f.mode,
                    range = f.range, duration = t.duration, weight = f.weight })
            end
        end
    end
    if side == 'suffix' and config.gapAffixes then
        local weight = physical.weight or base.weight
        local class = info.category == 'armor' and rules.armorClass(info.slot, weight, core.getGMST) or nil
        for _, f in ipairs(gaps.candidates(info.category, info.slot, class, tier, config.advancedGapAffixes)) do
            add({ id = f.effect .. ':' .. (f.skill or ''), name = f.suffix:sub(2), effect = f.effect,
                skill = f.skill, magnitude = f.magnitude, mode = f.mode,
                duration = f.duration, range = 'Self' })
        end
    end
    if config.bargainAffixes then
        for _, m in ipairs(bargains.candidates(info, side, tier)) do add(m) end
    end
    return result
end

local function distribution(base, info, side, physical, config, forcedTier, profiles)
    local result, available = {}, {}
    for tier = 1, 6 do available[tier] = tierCandidates(base, info, side, tier, physical, config, profiles) end
    for drawn = 1, 6 do
        local weight = forcedTier and (drawn == forcedTier and 1 or 0) or config.tierWeights[drawn]
        local tier = drawn
        while tier > 0 and (not contains(config.enabledTiers, tier) and not forcedTier or #available[tier] == 0) do tier = tier - 1 end
        if tier > 0 and weight > 0 then
            local total = 0
            for _, m in ipairs(available[tier]) do total = total + m.weight end
            for _, m in ipairs(available[tier]) do
                result[#result + 1] = { value = m, weight = weight * m.weight / total }
            end
        end
    end
    return result
end

function M.draw(entries, random)
    local total = 0
    for _, entry in ipairs(entries) do total = total + entry.weight end
    if total <= 0 then return nil end
    local target = random() * total
    for _, entry in ipairs(entries) do
        target = target - entry.weight
        if target < 0 then return entry.value end
    end
    return entries[#entries].value
end

local opposites = {
    drainattribute = 'fortifyattribute', drainskill = 'fortifyskill',
    weaknesstofire = 'resistfire', weaknesstofrost = 'resistfrost',
    weaknesstoshock = 'resistshock', weaknesstopoison = 'resistpoison', blind = 'nighteye',
}
local function modifierEffects(m)
    return m.effects or (m.effect and { { id = m.effect, skill = m.skill, attribute = m.attribute } } or {})
end
local function compatible(a, b)
    if a.id == b.id then return false end
    if a.mode and b.mode and a.mode ~= b.mode then return false end
    if a.bargain or b.bargain then
        for _, x in ipairs(modifierEffects(a)) do
            for _, y in ipairs(modifierEffects(b)) do
                if (opposites[x.id] == y.id or opposites[y.id] == x.id)
                    and x.skill == y.skill and x.attribute == y.attribute then return false end
            end
        end
    end
    return true
end

function M.roll(base, info, config, random, forcedLayout, forcedTier, profiles)
    if projectileLoot.applies(info) then return projectileLoot.roll(base, random, forcedLayout, forcedTier) end
    if not config.regionalFlavor then profiles = nil end
    local prefixes = distribution(base, info, 'prefix', {}, config, forcedTier, profiles)
    local suffixes = distribution(base, info, 'suffix', {}, config, forcedTier, profiles)
    -- Class-sensitive suffixes are enumerated against each prefix's final weight.
    local pairs, suffixCache = {}, {}
    for _, p in ipairs(prefixes) do
        local physical = M.physical(base, { p.value }, config)
        local class = info.category == 'armor' and rules.armorClass(info.slot, physical.weight or base.weight, core.getGMST) or 'other'
        if not suffixCache[class] then
            suffixCache[class] = distribution(base, info, 'suffix', physical, config, forcedTier, profiles)
        end
        for _, s in ipairs(suffixCache[class]) do
            if compatible(p.value, s.value) then
                pairs[#pairs + 1] = { value = { p.value, s.value }, weight = p.weight * s.weight }
            end
        end
    end
    local layouts = {}
    for _, candidate in ipairs({ { 'prefix', prefixes }, { 'suffix', suffixes }, { 'both', pairs } }) do
        if #candidate[2] > 0 and (not forcedLayout or forcedLayout == candidate[1]) then
            layouts[#layouts + 1] = { value = candidate[1], weight = forcedLayout and 1 or config.affixLayoutWeights[candidate[1]] }
        end
    end
    local layout = M.draw(layouts, random)
    if not layout then return nil end
    local mods = layout == 'both' and M.draw(pairs, random) or { M.draw(layout == 'prefix' and prefixes or suffixes, random) }
    local record = M.physical(base, mods, config)
    local effects, mode, charge, cost, chargeTier = {}, nil, 0, 0, 1
    local name = base.name
    for index, m in ipairs(mods) do
        if layout == 'prefix' or (layout == 'both' and index == 1) then name = m.name .. ' ' .. name
        else name = name .. ' ' .. m.name end
        if m.effect then
            mode = m.mode
            local strike = mode == 'CastOnStrike'
            if m.effects then
                for _, effect in ipairs(m.effects) do effects[#effects + 1] = effect end
            else
                effects[#effects + 1] = { id = m.effect, skill = m.skill, attribute = m.attribute,
                    magnitude = m.magnitude, range = m.range or (strike and 'Touch' or 'Self'),
                    duration = m.duration or (strike and 1 or 0), area = m.area or 0 }
            end
            chargeTier = math.max(chargeTier, m.tier)
        end
    end
    if mode and mode ~= 'ConstantEffect' then cost, charge = availability.budget(effects, chargeTier) end
    local surcharge = 0
    for _, m in ipairs(mods) do surcharge = surcharge + config.valueBonus * m.tier end
    record.value = (record.value or base.value) + surcharge
    return { name = name, record = record, effects = effects, mode = mode, charge = charge, cost = cost,
        isAutocalc = false, layout = layout, modifiers = mods }
end

return M
