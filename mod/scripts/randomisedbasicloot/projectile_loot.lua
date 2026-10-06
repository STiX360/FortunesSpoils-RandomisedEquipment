local M = {}
local slots = { arrow = true, bolt = true, thrown = true }
M.grades = {
    { name = 'Honed', bonus = 1, weight = 80 },
    { name = 'Keen', bonus = 2, weight = 18 },
    { name = 'Piercing', bonus = 3, weight = 2 },
}

function M.applies(info)
    return info.category == 'weapon' and slots[info.slot] == true
end

function M.roll(base, random, layout, forcedGrade)
    assert(not layout or layout == 'prefix', 'Projectiles only support a quality prefix, not suffixes, dual affixes or uniques.')
    assert(not forcedGrade or M.grades[forcedGrade], 'Projectile grade must be 1-3.')
    local grade = forcedGrade
    if not grade then
        local target = random() * 100
        for index, entry in ipairs(M.grades) do
            target = target - entry.weight
            if target < 0 then grade = index; break end
        end
        grade = grade or #M.grades
    end
    local entry, record = M.grades[grade], {}
    -- Zero damage channels stay zero; there are no independently rolled values.
    for _, attack in ipairs({ 'chop', 'slash', 'thrust' }) do
        for _, limit in ipairs({ 'Min', 'Max' }) do
            local key = attack .. limit .. 'Damage'
            record[key] = base[key] > 0 and math.min(255, base[key] + entry.bonus) or 0
        end
    end
    return { name = entry.name .. ' ' .. base.name, record = record, effects = {},
        layout = 'prefix', projectileGrade = grade, templateVersion = 1,
        modifiers = { { id = 'projectile_quality', name = entry.name, tier = grade, bonus = entry.bonus } } }
end

return M
