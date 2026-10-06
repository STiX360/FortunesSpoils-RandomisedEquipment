local M = {}
local weightSettings = {
    helmet = 'iHelmWeight', cuirass = 'iCuirassWeight', left_pauldron = 'iPauldronWeight',
    right_pauldron = 'iPauldronWeight', greaves = 'iGreavesWeight', boots = 'iBootsWeight',
    left_gauntlet = 'iGauntletWeight', right_gauntlet = 'iGauntletWeight', shield = 'iShieldWeight',
    left_bracer = 'iGauntletWeight', right_bracer = 'iGauntletWeight',
}
local armorSkills = { lightarmor = true, mediumarmor = true, heavyarmor = true }

function M.armorClass(slot, finalWeight, getGMST)
    if not weightSettings[slot] or not getGMST or finalWeight <= 0 then return nil end
    local baseline = math.floor(getGMST(weightSettings[slot]))
    if finalWeight <= baseline * getGMST('fLightMaxMod') + 0.0005 then return 'lightarmor' end
    if finalWeight <= baseline * getGMST('fMedMaxMod') + 0.0005 then return 'mediumarmor' end
    return 'heavyarmor'
end

function M.matchesArmorSkill(skill, category, slot, finalWeight, getGMST)
    if not armorSkills[skill] then return true end
    if category == 'clothing' then return slot == 'ring' or slot == 'amulet' end
    return category == 'armor' and skill == M.armorClass(slot, finalWeight, getGMST)
end

-- Bind unique armor skills only after every physical override has been resolved.
function M.resolveUniqueEffects(effects, category, slot, finalWeight, getGMST)
    local result = {}
    for _, effect in ipairs(effects) do
        local copy = {}
        for key, value in pairs(effect) do copy[key] = value end
        if copy.armorClassBound and category == 'armor' then
            copy.skill = M.armorClass(slot, finalWeight, getGMST)
            assert(copy.skill, 'Cannot bind armor skill to unclassified final armor')
        end
        assert(copy.id ~= 'fortifyskill' or M.matchesArmorSkill(copy.skill, category, slot, finalWeight, getGMST),
            'Unique armor skill does not match final item weight')
        result[#result + 1] = copy
    end
    return result
end

return M
