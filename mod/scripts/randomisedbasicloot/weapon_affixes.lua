local policy = require('scripts.randomisedbasicloot.weapon_affix_policy')
local M = {}

function M.resolve(modifier, slot, records)
    if modifier.mode ~= 'CastOnStrike' then return true end
    local profile = policy.profiles[slot]
    if not profile then return true end
    local effects = modifier.effects or { { id = modifier.effect, magnitude = modifier.magnitude,
        skill = modifier.skill, attribute = modifier.attribute,
        duration = modifier.duration or 1, range = modifier.range or 'Touch', area = modifier.area or 0 } }
    local control = false
    for _, effect in ipairs(effects) do
        if policy.controlEffects[effect.id] then control = true end
        if profile.range == 'Target' and not records[effect.id].onTarget then return false end
    end
    -- Bargain benefits and drawbacks retain the same duration and delivery.
    for _, effect in ipairs(effects) do
        if control then effect.duration = math.max(1, math.floor(effect.duration * profile.controlDuration + .5)) end
        if profile.magnitude then
            if records[effect.id].hasMagnitude then
                effect.magnitude = math.max(1, math.floor(effect.magnitude * profile.magnitude + .5))
            end
            effect.range, effect.area = profile.range, profile.area
        end
    end
    modifier.effects = effects
    modifier.mode = profile.mode or modifier.mode
    return true
end

return M
