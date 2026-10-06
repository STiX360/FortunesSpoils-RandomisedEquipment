local M = {}
local jewelry = { ring = true, amulet = true }
local body = { shirt = true, pants = true, skirt = true, robe = true }
local gloves = { left_glove = true, right_glove = true }
local armoredHands = { left_gauntlet = true, right_gauntlet = true, left_bracer = true, right_bracer = true }
local feet = { boots = true, shoes = true }
local projectile = { arrow = true, bolt = true, thrown = true }

local function wearable(category) return category == 'armor' or category == 'clothing' end
local function mage(category, slot)
    return wearable(category) and (slot == 'helmet' or slot == 'robe' or jewelry[slot])
end
local function armorSkill(skill)
    return function(category, slot, class)
        return category == 'armor' and class == skill
    end
end

M.families = {
    { id = 'light', effect = 'light', magnitudes = { 5, 10, 15, 20, 25, 30 },
      names = { 'of Candlelight', 'of Lamplight', 'of Beacon Light', 'of the Guiding Star', 'of Radiance', 'of the Unsetting Sun' },
      applies = function(c, s) return wearable(c) and (s == 'helmet' or s == 'shield' or jewelry[s]) end },
    { id = 'slowfall', effect = 'slowfall', magnitudes = { 1, 2, 3, 5, 7, 10 },
      names = { 'of Soft Landings', 'of Safe Descent', 'of Drifting', 'of the Falling Leaf', 'of Airborne Grace', 'of the Weightless Descent' },
      modes = { 'CastOnUse', 'CastOnUse', 'CastOnUse', 'ConstantEffect', 'ConstantEffect', 'ConstantEffect' },
      durations = { 15, 30, 60, 0, 0, 0 },
      applies = function(c, s) return c == 'clothing' and (s == 'robe' or s == 'skirt' or s == 'amulet') end },
    { id = 'swiftswim', effect = 'swiftswim', magnitudes = { 5, 10, 15, 20, 25, 30 },
      names = { 'of Wading', 'of Swimming', 'of the Current', 'of the River Runner', 'of the Tide Rider', 'of the Deep Current' },
      applies = function(c, s) return wearable(c) and (feet[s] or s == 'greaves' or s == 'pants' or jewelry[s]) end },
    { id = 'telekinesis', effect = 'telekinesis', magnitudes = { 1, 2, 3, 5, 7, 10 },
      names = { 'of Distant Touch', 'of Remote Grasp', 'of Far Handling', 'of the Unseen Hand', 'of Far Reach', 'of the Boundless Hand' },
      applies = function(c, s) return c == 'clothing' and (gloves[s] or jewelry[s]) end },
    { id = 'detectkey', effect = 'detectkey', magnitudes = { 5, 10, 15, 20, 25, 30 },
      names = { 'of Key Seeking', 'of Keyfinding', 'of Hidden Keys', 'of the Key Seer', 'of the Vault Seer', 'of the Hidden Threshold' },
      applies = function(c, s) return wearable(c) and (s == 'helmet' or gloves[s] or jewelry[s]) end },
    { id = 'detectenchantment', effect = 'detectenchantment', magnitudes = { 10, 20, 30, 40, 50, 60 },
      names = { 'of Enchantment Seeking', 'of Magicfinding', 'of Arcane Sight', 'of the Relic Seer', 'of the Arcane Watch', 'of the Relic Oracle' },
      applies = function(c, s) return wearable(c) and (s == 'helmet' or jewelry[s]) end },
    { id = 'sanctuary', effect = 'sanctuary', advanced = true, magnitudes = { 1, 2, 3, 4, 5, 6 },
      names = { 'of Reprieve', 'of Refuge', 'of Sanctuary', 'of the Sheltered Soul', 'of the Unbroken Refuge', 'of the Untouchable Soul' },
      applies = function(c, s) return c == 'clothing' and (body[s] or jewelry[s]) end },
    { id = 'blight', effect = 'resistblightdisease', magnitudes = { 3, 5, 7, 9, 12, 15 },
      names = { 'of Blight Warding', 'of Blight Shelter', 'of Blight Defiance', 'of the Ashland Physician', 'of Ashland Renewal', 'of the Blightless' },
      applies = function(c, s) return c == 'clothing' and (jewelry[s] or s == 'belt') end },
    { id = 'fireshield', effect = 'fireshield', advanced = true, magnitudes = { 1, 2, 3, 4, 5, 6 },
      names = { 'of Warm Warding', 'of Ember Warding', 'of Flame Warding', 'of the Burning Bulwark', 'of the Infernal Bulwark', 'of the Solar Bastion' },
      applies = function(c, s) return wearable(c) and (s == 'cuirass' or s == 'shield' or s == 'amulet') end },
    { id = 'frostshield', effect = 'frostshield', advanced = true, magnitudes = { 1, 2, 3, 4, 5, 6 },
      names = { 'of Cool Warding', 'of Rime Warding', 'of Ice Warding', 'of the Frozen Bulwark', 'of the Boreal Bulwark', 'of the Glacial Bastion' },
      applies = function(c, s) return wearable(c) and (s == 'cuirass' or s == 'shield' or s == 'amulet') end },
    { id = 'lightningshield', effect = 'lightningshield', advanced = true, magnitudes = { 1, 2, 3, 4, 5, 6 },
      names = { 'of Static Warding', 'of Spark Warding', 'of Storm Warding', 'of the Thunder Bulwark', 'of the Tempest Bulwark', 'of the Storm Bastion' },
      applies = function(c, s) return wearable(c) and (s == 'cuirass' or s == 'shield' or s == 'amulet') end },
    { id = 'attack', effect = 'fortifyattack', magnitudes = { 5, 8, 12, 16, 20, 25 },
      names = { 'of Aim', 'of True Aim', 'of Precision', 'of the Unerring Strike', 'of Faultless Aim', 'of the Certain Strike' },
      applies = function(c, s) return c == 'weapon' and not projectile[s] end },
    { id = 'maxmagicka', effect = 'fortifymaximummagicka', advanced = true, magnitudes = { 1, 2, 3, 4, 5, 6 },
      names = { 'of the Small Reservoir', 'of the Deep Reservoir', 'of the Mana Well', 'of the Arcane Wellspring', 'of the Astral Reservoir', 'of the Endless Wellspring' },
      applies = mage },
    { id = 'heavyarmor', effect = 'fortifyskill', skill = 'heavyarmor', magnitudes = { 1, 2, 3, 4, 5, 6 },
      names = { 'of Heavy Harness', 'of Heavy Armor', 'of Plate Mastery', 'of the Iron Sentinel', 'of the Plate Sovereign', 'of the Iron Citadel' }, applies = armorSkill('heavyarmor') },
    { id = 'mediumarmor', effect = 'fortifyskill', skill = 'mediumarmor', magnitudes = { 1, 2, 3, 4, 5, 6 },
      names = { 'of Medium Harness', 'of Medium Armor', 'of Mail Mastery', 'of the Balanced Sentinel', 'of the Mail Sovereign', 'of the Balanced Citadel' }, applies = armorSkill('mediumarmor') },
    { id = 'lightarmor', effect = 'fortifyskill', skill = 'lightarmor', magnitudes = { 1, 2, 3, 4, 5, 6 },
      names = { 'of Light Harness', 'of Light Armor', 'of Light Armor Mastery', 'of the Agile Sentinel', 'of the Agile Sovereign', 'of the Feather Citadel' }, applies = armorSkill('lightarmor') },
    { id = 'unarmored', effect = 'fortifyskill', skill = 'unarmored', magnitudes = { 1, 2, 3, 4, 5, 6 },
      names = { 'of Unarmored Practice', 'of Unarmored Defense', 'of Unarmored Mastery', 'of the Bare Sentinel', 'of the Bare Sovereign', 'of the Unarmored Citadel' },
      applies = function(c, s) return c == 'clothing' and (body[s] or gloves[s] or s == 'shoes' or jewelry[s]) end },
    { id = 'block', effect = 'fortifyskill', skill = 'block', magnitudes = { 1, 2, 3, 4, 5, 6 },
      names = { 'of Blocking', 'of Deflection', 'of Shieldwork', 'of the Perfect Guard', 'of the Shield Sovereign', 'of the Unbroken Guard' },
      applies = function(c, s) return c == 'armor' and s == 'shield' end },
    { id = 'handtohand', effect = 'fortifyskill', skill = 'handtohand', magnitudes = { 1, 2, 3, 4, 5, 6 },
      names = { 'of the Brawler', 'of the Pugilist', 'of the Unarmed Adept', 'of the Empty Hand', 'of the Fist Master', 'of the Unarmed Sovereign' },
      applies = function(c, s) return (c == 'clothing' and gloves[s]) or (c == 'armor' and armoredHands[s]) end },
    { id = 'enchant', effect = 'fortifyskill', skill = 'enchant', advanced = true, magnitudes = { 1, 2, 3, 4, 5, 6 },
      names = { 'of Enchanting', 'of Runework', 'of Soulcraft', 'of the Soul Artisan', 'of the Soul Master', 'of the Eternal Runework' }, applies = mage },
    { id = 'alchemy', effect = 'fortifyskill', skill = 'alchemy', advanced = true, magnitudes = { 1, 2, 3, 4, 5, 6 },
      names = { 'of Mixing', 'of Brewing', 'of Distillation', 'of the Master Alchemist', 'of the Elixir Master', 'of the Grand Transmuter' },
      applies = function(c, s) return c == 'clothing' and (s == 'robe' or s == 'amulet') end },
}

function M.candidates(category, slot, class, tier, advanced)
    assert(tier >= 1 and tier <= 6 and tier == math.floor(tier), 'Invalid gap affix tier')
    local result = {}
    for _, family in ipairs(M.families) do
        if (advanced or not family.advanced) and family.applies(category, slot, class) then
            result[#result + 1] = { id = family.id .. '_t' .. tier, effect = family.effect,
                skill = family.skill, magnitude = family.magnitudes[tier],
                mode = family.modes and family.modes[tier] or 'ConstantEffect',
                duration = family.durations and family.durations[tier] or 0,
                suffix = ' ' .. family.names[tier], tier = tier }
        end
    end
    return result
end

return M
