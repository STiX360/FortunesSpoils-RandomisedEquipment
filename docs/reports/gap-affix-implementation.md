# Gap Affix Implementation

Implemented 2026-10-04 in `scripts/randomisedbasicloot/gap_affixes.lua` and integrated into the global generator.
These are native Self affixes. Slowfall is on-use at T1-T3 and CE at T4-T6;
other utility families remain CE. All six tiers are available on otherwise eligible
bases. Numbers are provisional engine-test values. The older rollout notes below
are historical; [current progression](../AFFIX-PROGRESSION.md) records live allocations.

## Current Affix Slot Rules

Slowfall: skirts, robes and amulets only. Hand-to-hand: gloves, gauntlets and bracers.
Block: shields only. Alchemy: robes and amulets. Armor skills: matching final-weight armor only.
Unique templates are exempt; Unarmored and Enchant eligibility are unchanged.

## Current Tier Policy

All 21 utility families now have T5/T6 names and magnitudes in `gap_affixes.lua`.
Base-specific tier gates are removed; only slot, class, effect and configuration restrictions apply.
The preview is regenerated from those literal runtime arrays. The older T1-T4 context table below
records the initial values; it is not a tier cap.

## Historical Initial Rollout

- `gapAffixes = true` enables these families on approved static IDs across armor, clothing, and weapons.
- `gapTier = 1` is the initial live tier; valid values 1-4. This selects a tier, not a tier probability distribution.
- `advancedGapAffixes = false` initially gates Sanctuary, elemental shields, multiplicative Magicka,
  Alchemy, and Enchant behind an explicit opt-in. Their selection and generation code is implemented.
- `sourcePacks` enables each static source list. Missing game records have no effect on other packs.
- The existing 150-gold source-value cap, 100% testing chance, script protection, and unenchanted-base
  requirement still apply. Presence in the pool does not bypass those live checks.
- Corpse generation still adds one bonus item and rolls one affix. Replacement, weighted dual layouts,
  physical-affix composition, and unique drops remain unimplemented. The JSON is not runtime configuration.
- Previously processed corpses are not rerolled. Existing generated records are not rewritten.

Armor skill matching uses the item's current weight and loaded slot-weight/light/medium GMST thresholds,
not the material name. Armor-skill affixes now require matching final-weight armor; jewelry is excluded. Custom Combat-interface overrides
of armor classification are not modeled; this needs compatibility testing. Unreviewed scripts stay excluded.

The later [unique-design revision](unique-design-rules.md) factors this into shared `item_rules.lua`:
selection takes resolved final weight, record construction checks it again, and unique armor skills
are bound only after all physical overrides. Weight-induced class transitions are allowed.

## Families And Context

| Effect / Skill | T1 / T2 / T3 / T4 | Appropriate Items | Scenario / Restriction |
| --- | --- | --- | --- |
| Light | 5 / 10 / 15 / 20 | Helmets, shields, jewelry | Illumination; not a Night Eye alias |
| Slowfall | 1 / 2 / 3 / 5 | Skirts, robes, amulets | Descent gear; no boots or shoes; uniques exempt |
| Swift Swim | 5 / 10 / 15 / 20 | Feet, greaves, pants, jewelry | Underwater travel |
| Telekinesis | 1 / 2 / 3 / 5 | Clothing gloves, jewelry | Interaction reach, not weapon reach |
| Detect Key | 10 / 20 / 30 / 40 | Head, clothing gloves, jewelry | Searching, not unlocking |
| Detect Enchantment | 10 / 20 / 30 / 40 | Head, jewelry | Finding magical objects |
| Sanctuary | 1 / 2 / 3 / 4 | Body clothing, jewelry | Unarmored evasion; advanced gate |
| Resist Blight Disease | 3 / 5 / 7 / 9 / 12 / 15 | Rings, amulets, belts | Ashland protection; ordinary affixes only |
| Fire Shield | 1 / 2 / 3 / 4 | Cuirasses, shields, amulets | Fire ward; advanced gate |
| Frost Shield | 1 / 2 / 3 / 4 | Cuirasses, shields, amulets | Frost ward; advanced gate |
| Lightning Shield | 1 / 2 / 3 / 4 | Cuirasses, shields, amulets | Shock ward; advanced gate |
| Fortify Attack | 1 / 2 / 3 / 4 | Melee weapons, bows, crossbows | Equipped accuracy, not raw damage; no projectiles |
| Fortify Maximum Magicka | 1 / 2 / 3 / 4 native units | Head, robes, jewelry | Multiplicative resource effect, not flat Magicka; advanced gate |
| Heavy Armor | 1 / 2 / 3 / 4 | Heavy-class armor only | Final-weight matching protection skill; no jewelry; uniques exempt |
| Medium Armor | 1 / 2 / 3 / 4 | Medium-class armor only | Final-weight matching protection skill; no jewelry; uniques exempt |
| Light Armor | 1 / 2 / 3 / 4 | Light-class armor only | Final-weight matching protection skill; no jewelry; uniques exempt |
| Unarmored | 1 / 2 / 3 / 4 | Body clothing, clothing gloves, shoes, jewelry | No native armor is added |
| Block | 1 / 2 / 3 / 4 | Shields only | No clothing gloves; uniques exempt |
| Hand-to-hand | 1 / 2 / 3 / 4 | Clothing gloves, armor gauntlets and bracers | Unarmed fighting; never weapons; uniques exempt |
| Enchant | 1 / 2 / 3 / 4 | Head, robes, jewelry | Enchantment use/crafting; advanced gate |
| Alchemy | 1 / 2 / 3 / 4 | Robes, amulets | Potion crafting; advanced gate; uniques exempt |

Skill values are skill points. Detection and Telekinesis use native distance magnitudes.
Maximum Magicka uses native effect units, not a literal multiplier of 1x-4x; compare its actual
resource delta in-engine before release. Light and elemental shield presentation also require engine tests.
Tier-specific display names and applicability predicates live in the Lua module, not inferred from this table.

## Unique Revisions

The examples in this section describe the earlier repeated-profile revision. They are superseded
by [Unique Design Rules](unique-design-rules.md) and the current full registry.

The registry now has four designs per exact base ID: **2,960 templates**, including 740 new specialties.
The original twelve manually authored examples are preserved. Profile-generated armor drafts no longer
use a lone low-tier resistance/utility effect: defensive packages combine resistance, a stat, utility,
and modest physical changes. Their draft template versions record this pre-v1 revision.

Examples of the new fourth designs:

- Clothing gloves: Hand-to-hand 6, Unarmored 4, Fatigue 10, Drain Intelligence 3.
- Helmets: Light 15, Detect Enchantment 40, Blight Resistance 10, Drain Strength 2.
- Footwear: Slowfall 5, Swift Swim 15, Speed 3, Drain Strength 2.
- Shields: Block 6, Lightning Shield 4, Weakness to Fire 10.
- Rings: one fixed specialist package for remote keyfinding, Alchemy, Enchant, or unarmored evasion.
- Robes: one fixed mage/crafter package, including multiplicative Magicka, Enchant, or Alchemy.
- Non-projectile weapons: accuracy plus Agility, physical handling changes, and a durability tradeoff.
- Projectiles: a lighter/lower-damage travel variant; no unsupported equipped spell effects.

These are deterministic authoring profiles, not random effects at loot time and not individually
playtested designs. Higher skill/resource values and combinations on uniques are intentional specialties,
often with drawbacks, not permission to give every ordinary affix the same package.
Best-dual comparisons remain build-specific; the current runtime cannot yet generate those comparisons.

See [Unique Item Registry](unique-item-registry.md) for every fixed name, exact base ID, physical stat,
effect, mode, and drawback. Unique drop integration remains future work.

## Console Testing

In global Lua console mode (`luag`), these commands give eligible new-family sample variants:

```lua
require('openmw.interfaces').RandomisedBasicLoot.giveGapSamples('common_glove_left_01')
require('openmw.interfaces').RandomisedBasicLoot.giveGapSamples('iron_helmet')
require('openmw.interfaces').RandomisedBasicLoot.giveGapSamples('iron longsword')
```

If another mod scripts or enchants a base, or raises its value above the configured cap, sample
generation rejects it. Use a separate testing save. Mocked Lua tests validate generation and routing;
they do not replace equip/unequip, visual, resource, and save/reload checks in OpenMW.
