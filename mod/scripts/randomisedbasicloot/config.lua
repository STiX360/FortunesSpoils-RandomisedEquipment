return {
    enabled = true,
    debug = true, -- Routine logs: true for testing; production builds should default to false.
    dropChance = 1.0, -- Per equipment copy; projectiles roll once per original stack.
    maxBaseValue = 1000000,
    valueBonus = 15,
    seed = 1662,
    gapAffixes = true,
    expandedAffixes = true,
    gapTier = 1,
    advancedGapAffixes = true,
    uniqueChance = 0.05,
    allowUniqueDuplicates = false,
    bargainAffixes = true,
    regionalFlavor = true,
    affixLayoutWeights = { prefix = 1, suffix = 1, both = 1 },
    tierWeights = { 78, 15, 5, 1.5, 0.4, 0.1 },
    enabledTiers = { 1, 2, 3, 4, 5, 6 },
    appraisal = false,
    compositionCaps = { damage = 0.6, baseArmor = 0.6, health = 0.8,
        weight = 0.4, speed = 0.2, reach = 0.1, enchantCapacity = 0.6 },
    sourcePacks = { 'base', 'tribunal', 'bloodmoon', 'oaab' },
}
