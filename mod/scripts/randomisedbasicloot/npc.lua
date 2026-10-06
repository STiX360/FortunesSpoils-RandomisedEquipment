local core = require('openmw.core')
local self = require('openmw.self')
local types = require('openmw.types')
local settings = require('scripts.randomisedbasicloot.settings')

local sent = false
local elapsed = 0
local pendingEquipment = nil
local equipmentWait = 0
local freshInventory = false
local function requestSnapshot()
    core.sendGlobalEvent('RandomisedBasicLoot_InitialInventory', { actor = self.object, fresh = freshInventory })
end

local function restoreEquipment(dt)
    if not pendingEquipment then return end
    equipmentWait = equipmentWait + dt
    local equipment = types.Actor.getEquipment(self.object)
    local changed, waiting = false, false
    for _, entry in ipairs(pendingEquipment) do
        if entry.item:isValid() then
            local container = entry.item.parentContainer
            if container and container.id == self.object.id then
                equipment[entry.slot] = entry.item
                changed = true
            elseif not container then
                -- Inventory moves are queued; wait until the new item belongs to this NPC.
                waiting = true
            end
        end
    end
    if waiting and equipmentWait < 2 then return end
    if changed then
        local ok, err = pcall(types.Actor.setEquipment, self, equipment)
        if not ok then print('Randomised Basic Loot equipment restore error: ' .. tostring(err)) end
    end
    if waiting then print('Randomised Basic Loot: equipment transfer timed out for ' .. tostring(self.object.id)) end
    pendingEquipment = nil
    equipmentWait = 0
end

return {
    eventHandlers = {
        RandomisedBasicLoot_RestoreEquipment = function(changes)
            pendingEquipment = changes
            equipmentWait = 0
        end,
    },
    engineHandlers = {
        onInit = function()
            freshInventory = true
            requestSnapshot()
        end,
        onActive = requestSnapshot,
        onUpdate = function(dt)
            restoreEquipment(dt)
            if sent then return end
            elapsed = elapsed + dt
            if elapsed < 0.5 then return end
            elapsed = 0
            if types.Actor.isDeathFinished(self.object) then
                sent = true
                if settings.debugEnabled() then
                    print('Randomised Basic Loot: death notification for ' .. tostring(self.object.id))
                end
                core.sendGlobalEvent('RandomisedBasicLoot_Death', self.object)
            end
        end,
        onSave = function() return { sent = sent, pendingEquipment = pendingEquipment, inventoryBaselineVersion = 1,
            freshInventory = freshInventory } end,
        onLoad = function(data)
            sent = data and data.sent or false
            pendingEquipment = data and data.pendingEquipment or nil
            equipmentWait = 0
            -- Global saved allowances are authoritative; never recapture loaded inventories.
            freshInventory = false
            requestSnapshot()
        end,
    },
}
