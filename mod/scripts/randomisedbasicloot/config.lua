return {
    enabled = true,
    requireNewGameInventory = false, -- Strict opt-in; otherwise snapshot living NPCs on first observation.
    debug = false, -- Testing packages explicitly enable routine logs.
    dropChance = 0.6666666666666666, -- Ordinary modification chance after the global unique check.
    maxBaseValue = 1000000,
    valueBonus = 15,
    seed = 1662,
    gapAffixes = true,
    expandedAffixes = true,
    gapTier = 1,
    advancedGapAffixes = true,
    uniqueChance = 0.01, -- Global per-item chance; projectiles are exempt.
    allowUniqueDuplicates = false,
    bargainAffixes = true,
    regionalFlavor = true,
    affixLayoutWeights = { prefix = 1, suffix = 1, both = 2 },
    tierWeights = { 78, 15, 5, 1.5, 0.4, 0.1 },
    npcTierScaling = true,
    equalTierLevel = 25,
    enabledTiers = { 1, 2, 3, 4, 5, 6 },
    appraisal = false,
    compositionCaps = { damage = 0.6, baseArmor = 0.6, health = 0.8,
        weight = 0.4, speed = 0.2, reach = 0.1, enchantCapacity = 0.6 },
    sourcePacks = { 'base', 'tribunal', 'bloodmoon', 'oaab' },
}
