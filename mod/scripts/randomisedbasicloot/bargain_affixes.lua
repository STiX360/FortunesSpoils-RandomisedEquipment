local M = {}
local families = {
    { id = 'winter_pact', names = { 'Rime-Pledged', 'Frost-Pledged', 'Winter-Pledged', 'Icebound', 'Glacier-Sworn', 'Winter-Sacrificed' }, side = 'prefix',
        boon = { id = 'resistfrost' }, cost = { id = 'weaknesstofire' },
        benefits = { 4, 6, 9, 12, 15, 20 }, penalties = { 4, 6, 9, 13, 18, 25 } },
    { id = 'storm_pact', names = { 'Spark-Pledged', 'Static-Pledged', 'Storm-Pledged', 'Thunderbound', 'Tempest-Sworn', 'Storm-Sacrificed' }, side = 'prefix',
        boon = { id = 'resistshock' }, cost = { id = 'weaknesstofrost' },
        benefits = { 4, 6, 9, 12, 15, 20 }, penalties = { 4, 6, 9, 13, 18, 25 } },
    { id = 'silver_tongue', names = { 'of Borrowed Words', 'of Costly Persuasion', 'of Costly Eloquence', 'of Burdened Oratory', 'of the Frail Envoy', 'of the Wasted Sovereign' }, side = 'suffix',
        boon = { id = 'fortifyskill', skill = 'speechcraft' }, cost = { id = 'drainattribute', attribute = 'strength' },
        benefits = { 2, 3, 4, 5, 7, 8 }, penalties = { 2, 3, 4, 6, 8, 10 } },
    { id = 'scholar_burden', names = { 'of Borrowed Runework', 'of Costly Soulcraft', 'of the Burdened Scholar', 'of the Shackled Artisan', 'of the Leaden Soulmaster', 'of the Earthbound Archmage' }, side = 'suffix',
        boon = { id = 'fortifyskill', skill = 'enchant' }, cost = { id = 'drainattribute', attribute = 'speed' },
        benefits = { 2, 3, 4, 5, 7, 8 }, penalties = { 1, 2, 3, 4, 6, 8 } },
    { id = 'hobbling_fury', names = { 'of Stumbling Anger', 'of Hampered Wrath', 'of Hobbling Fury', 'of Shackled Rage', 'of the Fettered Berserker', 'of the Rooted Titan' }, side = 'suffix', strike = true,
        boon = { id = 'drainattribute', attribute = 'speed' }, cost = { id = 'fortifyattribute', attribute = 'strength' },
        benefits = { 4, 6, 9, 12, 16, 20 }, penalties = { 1, 1, 2, 2, 3, 4 } },
    { id = 'blinding_vigor', names = { 'of Clouded Reflexes', 'of Dazzled Poise', 'of Blinding Vigor', 'of Sightless Grace', 'of the Blind Duelist', 'of the Eyeless Champion' }, side = 'suffix', strike = true,
        boon = { id = 'blind' }, cost = { id = 'fortifyattribute', attribute = 'agility' },
        benefits = { 5, 8, 12, 18, 25, 35 }, penalties = { 1, 1, 2, 2, 3, 4 } },
}
local function effect(spec, magnitude, strike)
    return { id = spec.id, skill = spec.skill, attribute = spec.attribute, magnitude = magnitude,
        range = strike and 'Touch' or 'Self', duration = strike and 3 or 0, area = 0 }
end
function M.candidates(info, side, tier)
    local result = {}
    for _, f in ipairs(families) do
        local melee = info.category == 'weapon' and info.slot ~= 'bow' and info.slot ~= 'crossbow'
            and info.slot ~= 'arrow' and info.slot ~= 'bolt' and info.slot ~= 'thrown'
        local matchesSlot = f.id ~= 'silver_tongue' or (info.category == 'clothing' and info.slot == 'amulet')
        if f.side == side and matchesSlot and (f.strike and melee or not f.strike and info.category ~= 'weapon') then
            result[#result + 1] = { id = 'bargain:' .. f.id, name = f.names[tier], bargain = true,
                effect = f.boon.id, skill = f.boon.skill, attribute = f.boon.attribute,
                mode = f.strike and 'CastOnStrike' or 'ConstantEffect',
                effects = { effect(f.boon, f.benefits[tier], f.strike), effect(f.cost, f.penalties[tier], f.strike) } }
        end
    end
    return result
end
return M
