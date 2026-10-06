local M = {}

function M.weights(config, level)
    local rarity = 1
    if config.npcTierScaling and type(level) == 'number' and level == level then
        local endpoint = math.max(2, config.equalTierLevel or 25)
        rarity = 1 - math.max(0, math.min(1, (level - 1) / (endpoint - 1)))
    end
    local weights = {}
    for tier = 1, 6 do
        local weight = config.tierWeights[tier]
        -- A zero-weight tier remains excluded, including at the equality endpoint.
        weights[tier] = weight > 0 and weight ^ rarity or 0
    end
    return weights
end

return M
