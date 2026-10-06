package.path = 'mod/?.lua;' .. package.path
local effectRecords = setmetatable({}, { __index = function()
    return { hasMagnitude = true, onTarget = true }
end })
local core = { magic = { effects = { records = effectRecords } } }
local actor = { id = 'npc', finished = false, equipment = {} }
local self = { object = actor }
local notifications, equips, snapshots = 0, 0, {}
core.sendGlobalEvent = function(name, object)
    if name == 'RandomisedBasicLoot_InitialInventory' then
        assert(object.actor == actor)
        snapshots[#snapshots + 1] = object.fresh
        return
    end
    assert(name == 'RandomisedBasicLoot_Death' and object == actor)
    notifications = notifications + 1
end
local types = { Actor = {
    isDeathFinished = function(object) return object.finished end,
    getEquipment = function(object) return object.equipment end,
    setEquipment = function(localSelf, equipment)
        assert(localSelf == self, 'Equipment restoration must use local Self')
        equips = equips + 1
        actor.equipment = equipment
    end,
} }
package.preload['openmw.core'] = function() return core end
package.preload['openmw.types'] = function() return types end
package.preload['openmw.self'] = function() return self end
package.preload['scripts.randomisedbasicloot.settings'] = function()
    return { debugEnabled = function() return false end }
end
local npc = dofile('mod/scripts/randomisedbasicloot/npc.lua')
npc.engineHandlers.onInit()
assert(snapshots[1] == true)
npc.engineHandlers.onUpdate(.5)
assert(notifications == 0)
actor.finished = true
npc.engineHandlers.onUpdate(.5)
npc.engineHandlers.onUpdate(1)
assert(notifications == 1)
local saved = npc.engineHandlers.onSave()
npc = dofile('mod/scripts/randomisedbasicloot/npc.lua')
npc.engineHandlers.onLoad(saved)
assert(snapshots[#snapshots] == false, 'Loaded inventory must not be recaptured as fresh')
npc.engineHandlers.onUpdate(1)
assert(notifications == 1, 'Death notification persists through reload')
local replacement = { isValid = function() return true end }
npc.eventHandlers.RandomisedBasicLoot_RestoreEquipment({ { slot = 3, item = replacement } })
npc.engineHandlers.onUpdate(.1)
assert(equips == 0, 'Wait for queued transfer')
replacement.parentContainer = actor
npc.engineHandlers.onUpdate(.1)
assert(equips == 1 and actor.equipment[3] == replacement)
npc.engineHandlers.onUpdate(1)
assert(equips == 1, 'Restore only once')
local removed = { isValid = function() return false end }
npc.eventHandlers.RandomisedBasicLoot_RestoreEquipment({ { slot = 3, item = removed } })
npc.engineHandlers.onUpdate(.1)
assert(equips == 1, 'Do not equip removed items')

local resolver = require('scripts.randomisedbasicloot.weapon_affixes')
local function fire(slot, speed)
    local modifier = { mode = 'CastOnStrike', effect = 'firedamage', magnitude = 15, duration = 1 }
    assert(resolver.resolve(modifier, slot, effectRecords, speed))
    return modifier
end
assert(fire('short_blade', 1.5).effects[1].magnitude == 11)
assert(fire('long_blade_two_hand', .75).effects[1].magnitude == 20)
assert(fire('short_blade', 1).effects[1].magnitude == 15)
assert(fire('short_blade', 100).effects[1].magnitude == 11)
assert(fire('short_blade', .01).effects[1].magnitude == 23)
assert(fire('short_blade', 0).effects[1].magnitude == 15)
assert(fire('short_blade', nil).effects[1].magnitude == 15)
assert(fire('short_blade', 0/0).effects[1].magnitude == 15)
local staff = fire('blunt_two_hand_wide', .75)
assert(staff.mode == 'CastOnUse' and staff.effects[1].magnitude == 23)
assert(staff.effects[1].range == 'Target' and staff.effects[1].area == 3)
local control = { mode = 'CastOnStrike', effect = 'paralyze', magnitude = 1, duration = 15 }
resolver.resolve(control, 'long_blade_two_hand', effectRecords, .75)
assert(control.effects[1].magnitude == 1 and control.effects[1].duration == 8)
local disintegrate = { mode = 'CastOnStrike', effect = 'disintegratearmor', magnitude = 60, duration = 1 }
resolver.resolve(disintegrate, 'short_blade', effectRecords, 1.5)
assert(disintegrate.effects[1].magnitude == 60)

local gaps = require('scripts.randomisedbasicloot.gap_affixes')
local function hasBlight(category, slot)
    for _, entry in ipairs(gaps.candidates(category, slot, nil, 1, true)) do
        if entry.effect == 'resistblightdisease' then return true end
    end
    return false
end
for _, slot in ipairs({ 'ring', 'amulet', 'belt' }) do assert(hasBlight('clothing', slot)) end
for _, slot in ipairs({ 'robe', 'shirt', 'pants', 'skirt', 'shoes' }) do assert(not hasBlight('clothing', slot)) end
assert(not hasBlight('armor', 'helmet') and not hasBlight('armor', 'shield'))
local restricted = { resistcommondisease = true, resistmagicka = true, resistparalysis = true }
local seen = {}
for _, catalogue in ipairs({ require('scripts.randomisedbasicloot.magic_catalogue'),
                            require('scripts.randomisedbasicloot.expanded_catalogue') }) do
    for _, family in ipairs(catalogue) do
        if restricted[family.effect] then
            assert(family.side == 'suffix' and #family.slots == 3)
            local slots = {}
            for _, slot in ipairs(family.slots) do slots[slot] = true end
            assert(slots.ring and slots.amulet and slots.belt)
            seen[family.effect] = true
        end
        if family.effect:match('^cure') or family.effect:match('^restore') then
            for _, slot in ipairs(family.slots or {}) do assert(slot ~= 'belt') end
        end
    end
end
for effect in pairs(restricted) do assert(seen[effect]) end

local ammo = require('scripts.randomisedbasicloot.projectile_loot')
local base = { name = 'Arrow', chopMinDamage = 0, chopMaxDamage = 0,
    slashMinDamage = 0, slashMaxDamage = 0, thrustMinDamage = 1, thrustMaxDamage = 254 }
for grade = 1, 3 do
    local outcome = ammo.roll(base, function() error('Forced grade must not draw') end, 'prefix', grade)
    assert(outcome.projectileGrade == grade and outcome.record.thrustMinDamage == 1 + grade)
    assert(outcome.record.thrustMaxDamage == 255 and outcome.record.chopMaxDamage == 0)
    assert(not outcome.record.weight and not outcome.record.value and #outcome.effects == 0)
end
assert(ammo.roll(base, function() return .79 end).projectileGrade == 1)
assert(ammo.roll(base, function() return .80 end).projectileGrade == 2)
assert(ammo.roll(base, function() return .98 end).projectileGrade == 3)
for _, layout in ipairs({ 'suffix', 'both', 'unique' }) do
    assert(not pcall(ammo.roll, base, function() return 0 end, layout))
end
print('PASS: notifications, equipment restoration, damage scaling, resistance scopes, belt exclusions, projectile grades')
