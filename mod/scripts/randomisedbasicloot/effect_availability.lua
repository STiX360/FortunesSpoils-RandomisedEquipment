local core = require('openmw.core')
local types = require('openmw.types')
local M = {}
local expansions = { tribunal = 'Tribunal.esm', bloodmoon = 'Bloodmoon.esm' }

local function enabled(list, value)
    for _, entry in ipairs(list or {}) do if entry == value then return true end end
    return false
end

local function settingRecord(gmst, records)
    local ok, id = pcall(core.getGMST, gmst)
    return ok and type(id) == 'string' and id ~= '' and records[id] ~= nil
end

function M.available(f, config)
    if f.expansion and (not enabled(config.sourcePacks, f.expansion)
        or not core.contentFiles.has(expansions[f.expansion])) then return false end
    local effect = core.magic.effects.records[f.effect]
    if not effect then return false end
    local range = f.range or 'Self'
    if (range == 'Self' and not effect.onSelf) or (range == 'Touch' and not effect.onTouch)
        or (range == 'Target' and not effect.onTarget) then return false end
    if f.requiredCreatureGMST and not settingRecord(f.requiredCreatureGMST, types.Creature.records) then return false end
    for _, gmst in ipairs(f.requiredItemGMSTs or {}) do
        if not settingRecord(gmst, types[f.requiredType].records) then return false end
    end
    return true
end

-- Use the engine's effect-cost formula, but store explicit cost/charge: autocalc
-- also overrides charge capacity and would erase charge-based instant-effect tiers.
function M.budget(effects, tier)
    local total = 0
    for _, e in ipairs(effects) do
        local record = core.magic.effects.records[e.id]
        local magnitude = record.hasMagnitude and e.magnitude or 1
        local duration = record.hasDuration and (e.duration or 0) or 1
        if not record.isAppliedOnce then duration = math.max(1, duration) end
        local cost = magnitude * .1 * record.baseCost * duration
            + .05 * (e.area or 0) * record.baseCost
        if e.range == 'Target' then cost = cost * 1.5 end
        total = total + cost * core.getGMST('fEffectCostMult')
    end
    local cost = math.max(1, math.ceil(total))
    return cost, math.max(40 + tier * 20, cost * (3 + tier))
end

return M
