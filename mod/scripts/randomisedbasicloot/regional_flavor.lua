local M = {}
-- Curated vanilla ruin families, including their comma-separated interior sections.
-- Sources and coverage policy: docs/reports/regional-bargain-loot.md.
local dwemer = {
    'Aleft', 'Arkngthand', 'Arkngthunch-Sturdumz', 'Bethamez', 'Bthanchend',
    'Bthanual', 'Bthungthumz', 'Dagoth Ur', 'Druscashti', 'Endusal',
    'Galom Daeus', 'Mudan', 'Mzahnch', 'Mzuleft', 'Nchardahrk', 'Nchardumz',
    'Nchuleft', 'Nchuleftingth', 'Nchurdamz', 'Odrosal', 'Rkugamz',
    'Tureynulal', 'Vemynal',
}
local citadels = { 'Dagoth Ur', 'Endusal', 'Odrosal', 'Tureynulal', 'Vemynal' }
local regions = {
    ['ashlands'] = 'ash', ['molag amur'] = 'ash', ['red mountain'] = 'ash',
    ['bitter coast'] = 'marsh', ['azura\'s coast'] = 'coast', ['sheogorad'] = 'coast',
    ['solstheim'] = 'frost', ['brodir grove'] = 'frost', ['felsaad coast'] = 'frost',
    ['hirstaang forest'] = 'frost', ['isinfier plains'] = 'frost', ['moesring mountains'] = 'frost',
    ['ensleth valley'] = 'frost',
}
local effects = {
    ash = { resistblightdisease = 3, resistfire = 2, fireshield = 2, firedamage = 2 },
    marsh = { resistpoison = 2, resistcommondisease = 2, waterbreathing = 2, swiftswim = 2, poison = 2 },
    coast = { waterbreathing = 2, waterwalking = 2, swiftswim = 2 },
    frost = { resistfrost = 3, frostshield = 2, frostdamage = 2 },
    dwemer = { resistshock = 2, shockdamage = 2, lightningshield = 2, detectenchantment = 3 },
}
local function inFamily(name, families)
    for _, root in ipairs(families) do
        root = root:lower()
        if name == root or name:sub(1, #root + 2) == root .. ', ' then return true end
    end
    return false
end
function M.profiles(cell)
    local result = {}
    if not cell then return result end
    if cell.isExterior then
        local region = (cell.region or ''):lower():gsub('%s+region$', '')
        region = region:gsub('^solstheim,%s*', '')
        if regions[region] then result[1] = regions[region] end
    else
        local name = (cell.name or cell.id or ''):lower()
        if inFamily(name, dwemer) then result[#result + 1] = 'dwemer' end
        if inFamily(name, citadels) then result[#result + 1] = 'ash' end
    end
    return result
end
function M.weight(effect, skill, field, profiles)
    local weight = 1
    for _, profile in ipairs(profiles or {}) do
        weight = weight * ((effects[profile] or {})[effect] or 1)
        if profile == 'dwemer' and (skill == 'enchant' or field == 'enchantCapacity') then weight = weight * 3 end
    end
    return math.min(weight, 4)
end
return M
