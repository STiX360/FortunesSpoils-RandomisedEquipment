# Equipment Modifier Catalogue

Updated 2026-10-04. Catalogue exported into the full development runtime; power levels remain provisional.

Every family tier is available on every otherwise eligible base. Functionally redundant tiers are omitted; Water Breathing/Walking end at T4. Base-item profiles apply biases only; they never unlock or cap tiers. Settings and slot/mode restrictions still apply. See [current utility progression](../AFFIX-PROGRESSION.md).

This catalogue covers the approved static equipment pool in [Included Items Report](included-items-report.md).
The magic tables are exported by `tools/export_runtime_design.py`; physical families live in `loot.lua`
and utility families in `gap_affixes.lua`. The [interactive preview](preview-modifier-catalog.html)
combines all three and is rebuilt with `tools/build_modifier_preview.py`.

The [Affix And Unique Loot Design](loot-generation-design.md) records physical composition and
roll structure. The [Effect Coverage Review](effect-coverage-review.md) records effect choices.
Earlier rollout notes below are historical context, not current runtime configuration.

## Vanilla Calibration

The [Vanilla Enchantment Review](vanilla-enchantment-review.md) compares all ten supplied generic/unique
pages and audits the four supplied quest/artifact pages. It distinguishes charged enchantments from
constant effects; bigger temporary vanilla bonuses do not justify the same permanent magnitudes.
Bloodmoon's constant 5-point Frost Resistance per Snow Bear/Snow Wolf piece supports our T2 resistance.
The calibrated draft raises charged elemental weapon damage to 1/3/6/9 and permanent Magicka
to 2/4/8/12 across T1-T4. These are balance proposals, not changes to the running prototype.
The review supports stronger charged offense, not a blanket increase to permanent outfit bonuses.

T6 resistance 15 stays deliberately below The Icecap's constant 30-point frost bonus.
T5/T6 names and values are defined for every family below, including weapon skills and Shield.
They remain provisional balance values; outfit-level review is still needed.
Exact protected source IDs are blocked during static-pool
generation by `data/protected_item_ids.json`; those items are references, never generation templates.

## Recommended Starting Rules

- Affixed items have configurable prefix-only, suffix-only, or both layouts; default weights 1/1/1.
- Roll a separate curated unique chance before the affix layout; uniques have fixed values, not random affixes.
- All six tiers apply to every eligible base; enabled tier settings control the rollout.
- Use fixed magnitudes per tier, not randomly varying constant-effect magnitudes.
- Only approved, unenchanted base items may roll. Themes never admit an otherwise excluded item.
- Theme membership uses explicit record IDs, not display names or broad substring matching.
- Item themes are fictional design associations, not claims about existing equipment effects.
- Drop chance, modifier weight, and tier chance are three separate settings.
- Keep all source packs optional. Missing records or unsupported effects disable their own candidates.

### Tier Model

| Tier | Name | Role | Full-System Roll Chance |
| --- | --- | --- | ---: |
| T1 | Minor | Small everyday bonuses | 78% |
| T2 | Improved | Modest upgrades | 15% |
| T3 | Greater | Noticeable but restrained upgrades | 5% |
| T4 | Potent | Highest ordinary modifier tier | 1.5% |
| T5 | Superior | Strong modifier on any eligible base | 0.4% |
| T6 | Exalted | Highest modifier tier on any eligible base | 0.1% |

This is a proposed mature-system distribution, totaling 100%, per selected affix after a successful
drop-chance roll and the non-unique branch. It is not the starting configuration: T1-only testing remains 100% T1.
T5 and T6 are stronger versions of the same families, not permission to generate named artifacts.

All six tiers are available wherever a family applies. Optional item profiles only adjust
family-selection weights. Slot restrictions, enabled settings, and compatible enchantment modes
still apply. Draw the configured tier independently for each selected affix; a disabled or
otherwise unavailable tier falls back downward, never upward. No base-specific tier gates remain.

### Tier Identity

Each available tier has its own prefix/suffix name, following an ARPG-style progression.
A table cell gives the exact display name and magnitude; the family column groups related rolls.
For example: Guarded Iron Helmet (T1) -> Warded Iron Helmet (T2) ->
Fortified Iron Helmet (T3) -> Bastioned Iron Helmet (T4).
These are original proposed names, not a copied Path of Exile modifier catalogue.

Names do not unlock effects or tiers. Each eligible family has separate T1-T6 names. Use stable family IDs plus tier in configuration
and generated-record cache keys; never use the display name to determine effect, eligibility, or bias.
Record metadata should retain the numeric tier even when the item name already signals strength.
A tier is not an extra affix: a dual item has one prefix and one suffix, each with its own tier.
Tier metadata for a T6/T2 item must preserve both tiers, not flatten them into a single item tier.

### Applicability Terms

| Term | Included items |
| --- | --- |
| Wearables | All armor and clothing slots, including shields, rings, and amulets; no weapons |
| Armor | Helmet, cuirass, pauldrons, greaves, boots, gauntlets, bracers, shield |
| Body clothing | Shirt, pants, skirt, robe; not jewelry, belts, gloves, or shoes |
| Head | Armor-type helmets, including approved hats, hoods, masks, and wraps |
| Hands | Armor gauntlets/bracers and clothing gloves, either side |
| Feet | Armor boots and clothing shoes |
| Jewelry | Rings and amulets |
| Melee weapons | Short/long blades, axes, blunt weapons, staves, and spears; includes tool-shaped WEAP records |
| Launchers | Bows and crossbows; not arrows or bolts |
| Projectiles | Arrows, bolts, and thrown weapons; deferred from the initial modifier system |

Every term means only IDs already present in the static allowlist. A hood is classified by its record type,
not by its name. Left/right items remain separate base IDs, but share modifier rules.

## Prefixes: Equipped Bonuses

All effects in this table are constant effects on the wearer while equipped.
The T1-T6 columns give tier-specific names and exact proposed magnitudes. A dash means that tier is unavailable.
All six tiers share the same family applicability.
Percentages are resistance points, not percentage increases to an existing resistance.

| Prefix Family | Effect | T1 | T2 | T3 | T4 | T5 | T6 | Applies To | Notes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Guarded | Shield | **Guarded** (5 pts) | **Warded** (8 pts) | **Fortified** (12 pts) | **Bastioned** (16 pts) | **Bulwarked** (22 pts) | **Citadel-forged** (30 pts) | Shields, amulets | Adds overall armor rating; restricted to shields and amulets, not a change to base armor stats |
| Sturdy | Fortify Endurance | **Sturdy** (1 pt) | **Hardy** (2 pts) | **Stalwart** (3 pts) | **Indomitable** (4 pts) | **Unbreakable** (5 pts) | **Deathless** (6 pts) | Cuirass, greaves, boots, body clothing, belts | Do not describe as a permanent health-growth bonus |
| Mighty | Fortify Strength | **Mighty** (1 pt) | **Forceful** (2 pts) | **Powerful** (3 pts) | **Titanic** (4 pts) | **Colossal** (5 pts) | **Herculean** (6 pts) | Cuirass, hands, belts, jewelry | Also increases carrying capacity through Strength |
| Nimble | Fortify Agility | **Nimble** (1 pt) | **Deft** (2 pts) | **Agile** (3 pts) | **Effortless** (4 pts) | **Preternatural** (5 pts) | **Faultless** (6 pts) | Hands, feet, greaves, pants, skirts, jewelry | Small combat/handling bonus |
| Swift | Fortify Speed | **Swift** (1 pt) | **Fleet** (2 pts) | **Racing** (3 pts) | **Windborne** (4 pts) | **Gale-borne** (5 pts) | **Stormfleet** (6 pts) | Feet | Boots and shoes only; unique designs are exempt |
| Learned | Fortify Intelligence | **Learned** (1 pt) | **Scholarly** (2 pts) | **Sagacious** (3 pts) | **Erudite** (4 pts) | **Enlightened** (5 pts) | **Omniscient** (6 pts) | Head, robes, shirts, jewelry | Attribute effect, not Restore Magicka |
| Resolute | Fortify Willpower | **Resolute** (1 pt) | **Steadfast** (2 pts) | **Unwavering** (3 pts) | **Adamant** (4 pts) | **Iron-souled** (5 pts) | **Unshakable** (6 pts) | Head, robes, belts, jewelry | Prefix-only; legacy suffix items remain unchanged |
| Charming | Fortify Personality | **Charming** (1 pt) | **Gracious** (2 pts) | **Captivating** (3 pts) | **Majestic** (4 pts) | **Radiant** (5 pts) | **Sovereign** (6 pts) | Body clothing, jewelry | Social equipment emphasis |
| Lucky | Fortify Luck | **Lucky** (1 pt) | **Fortunate** (2 pts) | **Favored** (3 pts) | **Blessed** (4 pts) | **Fated** (5 pts) | **Destined** (6 pts) | Jewelry | Low weight: 1, versus ordinary modifiers at 10 |
| Lightened | Feather | **Lightened** (3 pts) | **Unburdened** (5 pts) | **Weightless** (8 pts) | **Featherborne** (12 pts) | **Cloudborne** (16 pts) | **Skybound** (20 pts) | Wearables | Changes effective encumbrance, not item weight |
| Vigorous | Fortify Fatigue | **Vigorous** (3 pts) | **Energetic** (5 pts) | **Tireless** (8 pts) | **Unflagging** (12 pts) | **Inexhaustible** (16 pts) | **Unrelenting** (20 pts) | Armor, body clothing, belts | Extra fatigue capacity, not regeneration |
| Vital | Fortify Health | **Vital** (2 pts) | **Hearty** (3 pts) | **Robust** (4 pts) | **Lifeweaving** (6 pts) | **Lifebound** (8 pts) | **Undying** (10 pts) | Cuirass, robes, amulets | Defer until equip/unequip and low-health behavior are tested |
| Arcane | Fortify Magicka | **Arcane** (2 pts) | **Attuned** (4 pts) | **Empowered** (8 pts) | **Aetheric** (12 pts) | **Astral** (16 pts) | **Aetherbound** (20 pts) | Head, robes, jewelry | Calibrated below the Hortator belt's 20; defer until resource and outfit stacking are tested |
| Emberward | Resist Fire | **Emberward** (3%) | **Cinderward** (5%) | **Flameward** (7%) | **Phoenixward** (9%) | **Hearthward** (12%) | **Sunward** (15%) | Wearables | General pool; existing ruby bias retained |
| Rimeward | Resist Frost | **Rimeward** (3%) | **Frostward** (5%) | **Hoarfrostward** (7%) | **Winterward** (9%) | **Starfrostward** (12%) | **Borealward** (15%) | Wearables | General pool; existing bear/sapphire biases retained |

## Suffixes: Protection And Utility

All effects are constant effects on the wearer while equipped.
All utility entries below have explicit magnitudes; no on/off utility effects are proposed initially.

| Suffix Family | Effect | T1 | T2 | T3 | T4 | T5 | T6 | Applies To | Notes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| of Grounding | Resist Shock | **of Grounding** (3%) | **of Insulation** (5%) | **of Storm Shelter** (7%) | **of the Lightning Rod** (9%) | **of the Dynamo** (12%) | **of the Stormheart** (15%) | Wearables | General pool, Dwemer jewelry bias proposed |
| of Antidotes | Resist Poison | **of Antidotes** (3%) | **of Antivenom** (5%) | **of Purification** (7%) | **of the Unvenomed** (9%) | **of Pure Blood** (12%) | **of the Untainted** (15%) | Wearables | General pool; no immunity |
| of Cleanliness | Resist Common Disease | **of Cleanliness** (3%) | **of Hygiene** (5%) | **of Convalescence** (7%) | **of the Physician** (9%) | **of Renewal** (12%) | **of the Unblemished** (15%) | Jewelry, belts | Does not imply Blight or Corprus resistance |
| of Night Eyes | Night Eye | **of Night Eyes** (3 pts) | **of Twilight Sight** (6 pts) | **of Moonlit Sight** (9 pts) | **of Midnight Sight** (12 pts) | **of Star Sight** (15 pts) | **of the Everwatchful** (18 pts) | Head, jewelry | Test readability under the player's lighting/shader setup |
| of the Watch | Detect Creature | **of the Watch** (20 ft) | **of Vigilance** (40 ft) | **of Awareness** (60 ft) | **of the Sentinel** (80 ft) | **of the Far Watch** (100 ft) | **of the All-seeing Sentinel** (120 ft) | Head, jewelry | Does not mean detecting every NPC; deliberately short range |
| of the Locksmith | Fortify Security | **of the Locksmith** (1 pt) | **of the Lockpicker** (2 pts) | **of the Safecracker** (3 pts) | **of the Master Key** (4 pts) | **of the Vaultbreaker** (5 pts) | **of the Skeleton Key** (6 pts) | Hands, rings, belts | No automatic opening or extra lockpick charges |
| of Quiet Steps | Fortify Sneak | **of Quiet Steps** (1 pt) | **of Soft Footfalls** (2 pts) | **of Silent Passage** (3 pts) | **of the Unseen** (4 pts) | **of the Ghost Step** (5 pts) | **of the Soundless** (6 pts) | Feet, pants, skirts, rings | No Chameleon in the initial pool |
| of the Acrobat | Fortify Acrobatics | **of the Acrobat** (1 pt) | **of the Tumbler** (2 pts) | **of the Leaper** (3 pts) | **of the Vaulting Star** (4 pts) | **of the Sky Dancer** (5 pts) | **of the Bounding Star** (6 pts) | Feet, pants, skirts | Skill bonus, not a Jump effect |
| of the Runner | Fortify Athletics | **of the Runner** (2 pts) | **of the Strider** (3 pts) | **of the Marathoner** (5 pts) | **of the Tireless Road** (6 pts) | **of the Endless Road** (8 pts) | **of the Horizon Chaser** (9 pts) | Feet, greaves, pants | No skirts; unique designs are exempt. Running-speed calibration: 1.5 Athletics per Speed at 50/50, rounded half upward; walking/swimming differ |
| of the Merchant | Fortify Mercantile | **of the Merchant** (1 pt) | **of the Trader** (2 pts) | **of the Broker** (3 pts) | **of the Magnate** (4 pts) | **of the Tycoon** (5 pts) | **of the Golden Ledger** (6 pts) | Clothing | Economic effect; monitor resale balance |
| of Persuasion | Fortify Speechcraft | **of Persuasion** (1 pt) | **of Eloquence** (2 pts) | **of Oratory** (3 pts) | **of the Silver Tongue** (4 pts) | **of the Envoy** (5 pts) | **of the Sovereign Voice** (6 pts) | Amulets | No Charm spell or forced dialogue changes |
| Alteration | Fortify Alteration | **of Alteration** (1 pt) | **of Shaping** (2 pts) | **of Transmutation** (3 pts) | **of the Worldshaper** (4 pts) | **of the Matter Weaver** (5 pts) | **of the Reality Shaper** (6 pts) | Robes, amulets | One skill only; no combined six-skill roll |
| Conjuration | Fortify Conjuration | **of Conjuration** (1 pt) | **of Summoning** (2 pts) | **of Binding** (3 pts) | **of the Planar Master** (4 pts) | **of the Gatekeeper** (5 pts) | **of the Planar Sovereign** (6 pts) | Robes, amulets | One skill only; no combined six-skill roll |
| Destruction | Fortify Destruction | **of Destruction** (1 pt) | **of Ruin** (2 pts) | **of Devastation** (3 pts) | **of the Annihilator** (4 pts) | **of Cataclysm** (5 pts) | **of the Worldbreaker** (6 pts) | Robes, amulets | One skill only; no combined six-skill roll |
| Illusion | Fortify Illusion | **of Illusion** (1 pt) | **of Glamour** (2 pts) | **of Phantoms** (3 pts) | **of the Dreamweaver** (4 pts) | **of the Mind Weaver** (5 pts) | **of the Waking Dream** (6 pts) | Robes, amulets | One skill only; no combined six-skill roll |
| Mysticism | Fortify Mysticism | **of Mysticism** (1 pt) | **of Communion** (2 pts) | **of the Veil** (3 pts) | **of the Unfathomable** (4 pts) | **of the Beyond** (5 pts) | **of the Boundless Veil** (6 pts) | Robes, amulets | One skill only; no combined six-skill roll |
| Restoration | Fortify Restoration | **of Restoration** (1 pt) | **of Mending** (2 pts) | **of Renewal** (3 pts) | **of the Lifekeeper** (4 pts) | **of Rebirth** (5 pts) | **of the Life Sovereign** (6 pts) | Robes, amulets | One skill only; no combined six-skill roll |
| of the Armorer | Fortify Armorer | **of the Armorer** (1 pt) | **of the Smith** (2 pts) | **of the Forgemaster** (3 pts) | **of the Masterwork** (4 pts) | **of the Grand Smith** (5 pts) | **of the Eternal Forge** (6 pts) | Hands, belts | Improves skill; does not restore condition automatically |

### Speed And Athletics Calibration

Speed remains 1 / 2 / 3 / 4 / 5 / 6; Athletics is now 2 / 3 / 5 / 6 / 8 / 9.
Using vanilla movement settings, running speed is proportional to
`(100 + Speed) * (1.75 + Athletics / 100)` at fixed encumbrance and other multipliers.
At 50 Speed / 50 Athletics, one Speed point gives the same running-speed increase
as 1.5 Athletics points. Athletics tiers use that ratio, rounded half upward to
native integer effect magnitudes. T2/T4/T6 match exactly at this reference point;
T1/T3/T5 favor Athletics slightly in absolute movement gain because of rounding.
This is a running-speed balance target, not a universal equivalence: Speed also
affects walking, while swimming uses additional Athletics-dependent terms.
Existing unique templates and previously generated item records are not changed.

Sources: [OpenMW movement calculation](https://raw.githubusercontent.com/OpenMW/openmw/master/apps/openmw/mwclass/npc.cpp)
and [vanilla GMST values](https://mwse.github.io/MWSE/references/gmst/).

The six magic-skill families above are separate candidates with their own tier names.
Freeze the chosen skill and tier in the generated enchantment and cache key.
Do not give all six skills from one roll. Budget their combined family weight explicitly so adding
six names does not accidentally make magic-skill bonuses six times as common as other families.

## Weapons

Weapon families are exported into the full runtime. Slot and enchantment-mode restrictions remain in force.

### Weapon Suffixes: Equipped Bonuses

| Suffix Family | Effect | T1 | T2 | T3 | T4 | T5 | T6 | Applies To |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| of the Duelist | Fortify Short Blade | **of the Duelist** (1 pt) | **of the Knife Adept** (2 pts) | **of the Blade Dancer** (3 pts) | **of the Perfect Thrust** (4 pts) | **of the Knife Master** (5 pts) | **of the Final Thrust** (6 pts) | Short blades |
| of the Swordsman | Fortify Long Blade | **of the Swordsman** (1 pt) | **of the Sword Adept** (2 pts) | **of the Swordmaster** (3 pts) | **of the Peerless Edge** (4 pts) | **of the Edge Sovereign** (5 pts) | **of the Unerring Blade** (6 pts) | One-/two-handed long blades |
| of the Reaver | Fortify Axe | **of the Reaver** (1 pt) | **of the Cleaver** (2 pts) | **of the Headsman** (3 pts) | **of the Sundering Axe** (4 pts) | **of the Great Cleaver** (5 pts) | **of the Final Sundering** (6 pts) | One-/two-handed axes |
| of the Crusher | Fortify Blunt Weapon | **of the Crusher** (1 pt) | **of the Breaker** (2 pts) | **of the Mauler** (3 pts) | **of the Shattering Blow** (4 pts) | **of the Earthshaker** (5 pts) | **of the Mountain Breaker** (6 pts) | Maces, clubs, hammers, staves, scepters |
| of the Lancer | Fortify Spear | **of the Lancer** (1 pt) | **of the Pikeman** (2 pts) | **of the Spearmaster** (3 pts) | **of the Unerring Point** (4 pts) | **of the Lance Master** (5 pts) | **of the Horizon Spear** (6 pts) | Spears and halberds classified as spear records |
| of the Archer | Fortify Marksman | **of the Archer** (1 pt) | **of the Bowman** (2 pts) | **of the Marksman** (3 pts) | **of the Deadeye** (4 pts) | **of the Eagle Eye** (5 pts) | **of the Unerring Arrow** (6 pts) | Bows and crossbows |

These strengthen the wielder's skill, not the base weapon's damage, reach, speed, or durability.
Weapon skill mapping follows record subtype, even for a shovel, kitchen knife, or other tool.
Projectiles never receive equipped bonuses.

### Weapon Prefixes: Offensive Effects

| Prefix Family | Effect On Hit | T1 | T2 | T3 | T4 | T5 | T6 | Applies To | Mode |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| Smoldering | Fire Damage | **Smoldering** (1 pt for 1 sec) | **Kindled** (3 pts for 1 sec) | **Blazing** (6 pts for 1 sec) | **Incandescent** (9 pts for 1 sec) | **Infernal** (12 pts for 1 sec) | **Sunscorched** (15 pts for 1 sec) | Melee weapons | When Strikes, Touch, area 0 |
| Chilling | Frost Damage | **Chilling** (1 pt for 1 sec) | **Frigid** (3 pts for 1 sec) | **Freezing** (6 pts for 1 sec) | **Glacial** (9 pts for 1 sec) | **Boreal** (12 pts for 1 sec) | **Winterbound** (15 pts for 1 sec) | Melee weapons | When Strikes, Touch, area 0 |
| Sparking | Shock Damage | **Sparking** (1 pt for 1 sec) | **Crackling** (3 pts for 1 sec) | **Arcing** (6 pts for 1 sec) | **Thunderous** (9 pts for 1 sec) | **Tempestuous** (12 pts for 1 sec) | **Stormcrowned** (15 pts for 1 sec) | Melee weapons | When Strikes, Touch, area 0 |
| Venomous | Poison | **Venomous** (1 pt for 1 sec) | **Toxic** (2 pts for 1 sec) | **Virulent** (3 pts for 1 sec) | **Pestilent** (4 pts for 1 sec) | **Noxious** (5 pts for 1 sec) | **Plagueborne** (6 pts for 1 sec) | Short blades, spears | When Strikes, Touch, area 0 |
| Wearying | Damage Fatigue | **Wearying** (2 pts for 1 sec) | **Exhausting** (3 pts for 1 sec) | **Enervating** (4 pts for 1 sec) | **Debilitating** (6 pts for 1 sec) | **Withering** (8 pts for 1 sec) | **Soulweary** (10 pts for 1 sec) | Melee weapons | When Strikes, Touch, area 0 |

Do not put elemental damage on Self or make it constant effect.
Charged offensive enchantments need explicit charge, cost, depletion/recharge behavior, and engine tests.
The 1/3/6/9 elemental progression is inferred from the Iron/Steel/Silver Flamesword magnitude bands,
not copied from their full enchantments: source durations still need record validation.
Frost and shock share that provisional budget for consistency, not because the fire examples prove
equal performance against every target. Poison and Damage Fatigue retain their lower original budgets.
Recalculate native cost for the resolved effects; higher tiers must not retain T1 cost for free.
No free unlimited on-hit damage. Absorb Health, Paralysis, Silence, and area damage remain excluded initially.
Bows, crossbows, arrows, bolts, and thrown weapons need a separate projectile delivery design;
do not assume melee When Strikes behavior transfers correctly to them.

## Item-Specific Biases

Bias adjusts the relative weight of an already eligible family at every tier. It never unlocks
an effect, increases drop chance, or changes tier odds. All bases with appropriate slots may roll T6.

| Item Profile | Exact Membership | Family Bias |
| --- | --- | --- |
| Bear Armor | Nine approved Bloodmoon Bear armor IDs | Resist Frost x3 |
| Ruby Amulet | `extravagant_amulet_02` | Resist Fire x3 |
| Sapphire Amulet | `extravagant_amulet_01` | Resist Frost x3 |
| Wolf Armor | Nine approved Bloodmoon Wolf armor IDs | Athletics / Sneak x2 where eligible |
| Dwemer Amulet | `ab_c_dwemeramuletclock` | Resist Shock x2 |
| Silver Scepter | `ab_w_silverscepter` | Blunt Weapon x2 |
| Nordic Bearskin Cuirass | `fur_bearskin_cuirass` | Resist Frost x2 |

The former themed-only T5/T6 resistance entries have been folded into the ordinary resistance
families. They are not additional candidates or separate base-ID unlocks.

### Weight Example

Suppose ten eligible ordinary candidates each have weight 10. An unthemed item has a 10% chance
of selecting Rimeward. On a Bear piece, its weight becomes 30 while the other nine remain 10:

`P(Rimeward | ordinary modifier roll) = 30 / (30 + 9 * 10) = 25%`.

This is not a flat +20 percentage points and not necessarily three times the final probability.
Real probabilities depend on the slot's eligible candidates. Feather, Intelligence and
Willpower now have prefix-only families; their legacy suffix aliases are not candidates.

## Selection And Safety Rules

1. Resolve the base ID from an enabled static source pack and run the existing item protections.
2. Resolve explicit item profiles, category, and subtype. Never infer a ruby from a translated name.
3. Build candidates matching slot, mode, available effect, and current tier settings.
4. Draw once from the configured tier distribution. If its candidate set is empty or disabled, fall back to the highest eligible lower tier.
5. Apply item-profile weight multipliers to stable effect-family IDs within the selected tier's candidate set.
   A frost bias applies to the full Rimeward family, not only the grade-one name.
6. For each side selected by the configured layout, pick a family and tier-specific name. Aliases do not get extra weight.
   Validate the prefix/suffix pair using the compatibility rules in the linked loot design.
7. Compose physical record changes and any compatible magic effects, inheriting the base item's appearance.
8. Preserve the roll in save state. Reopening loot or reloading scripts must not reroll it.

Multiple profiles should not multiply the same bias repeatedly. Use the highest matching multiplier,
initially capped at x3. Explicit per-item rules take precedence over set defaults.
Never let an optional missing pack prevent unrelated items from rolling.

### Balance And Compatibility Guardrails

- Different resistance effects may coexist on a compatible dual-affix item; reject duplicate exact magic effects.
- Bonuses from different equipped pieces may stack. Low per-item values are not a global cap.
- Every eligible piece may roll T6. Nine T6 Frost Resistance pieces total 135% before racial or other bonuses;
  outfit-level balance still requires review. Rarity is not a stacking cap.
- If mature-system stacking is too strong, lower per-tier magnitudes;
  rarity alone is not a balance cap. Bases do not restrict tiers.
- Do not introduce a scripted outfit-wide cap until ordinary engine stacking is tested.
- The expanded effect catalogue now includes regeneration, advanced defenses, movement,
  casting utility and melee debuffs. See [Expanded Spell-Effect Affixes](expanded-affixes.md)
  for exact slots, tiers, weights, dependencies and explicit exclusions.
- Physical affixes deliberately modify weight, maximum condition, armor rating, damage, or other approved fields.
  Apply explicit field rules from the linked loot design; unrelated fields still inherit unchanged.
- Full condition/ownership and approved-script preservation still require the planned replacement implementation.
- A bias does not solve exact-ID quest checks. Source-item compatibility policy still applies.
- Two-affix items with two magic components must use one compatible enchantment mode.
  A When Strikes offensive prefix cannot simply be combined with a constant-effect skill suffix in one native enchantment.

## Historical Initial Rollout

Suggested first catalogue: Guarded, Mighty, Nimble, of Clarity, of Embers, of Rime, of Grounding,
of Antidotes, of the Locksmith, and of Quiet Steps. Apply the slot restrictions above and use T1 only.
Enable Bear/Ruby/Sapphire biases, but keep T2-T6 and all weapon modifiers disabled.
Keep the current three modifiers available for helmet regression tests.

After this is stable, test weapon equipped-skill modifiers independently, then charged offensive effects,
then T2-T4 upgrades one tier at a time, and finally the four themed families at T5 and T6. Generation across all equipment slots and
one-for-one replacement remain separate implementation work; this catalogue does not enable them.

## Implementation References

The [OpenMW 0.51 core API](https://openmw.readthedocs.io/en/openmw-0.51.0/reference/lua-scripting/openmw_core.html)
documents enchantment types, effect parameters, and affected attributes/skills.
These API facilities do not establish the balance or in-game correctness of the proposed catalogue;
the new effects and equipment modes need focused engine tests.

Current implemented magnitudes are taken from `mod/scripts/randomisedbasicloot/config.lua`.
Exact themed base IDs are taken from this project's included-items report, not inferred from outside mod lists.
