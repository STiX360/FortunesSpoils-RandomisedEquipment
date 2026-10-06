# Fortune's Spoils: Full Development Build

Development snapshot. Prior harness results do not validate this reorganised
package; no tests have been run during repository preparation.
Start a new game with this build enabled: corpse rolls require a trusted initial
NPC inventory allowance. An existing save receiving the mod for the first time
has no corpse rolls; previously visited NPCs in an upgraded mod save without a
snapshot also remain unchanged. See [Inventory Allowances](INVENTORY-ALLOWANCES.md)
and [Current In-Game Validation](CURRENT-INGAME-CHECKLIST.md).

Use a separate Mod Organizer profile and a disposable save. Do not install it
over the copy used by your separate POTI playthrough.

## Install In Mod Organizer

1. Install the versioned `fortunes-spoils-<version>-testing.zip` as a new mod, named `Fortune's Spoils`.
2. The archive's data root contains `Randomised Basic Loot.omwscripts` and `scripts/`.
   If MO asks for a data directory, select that root.
3. Disable the previous prototype package in this test profile. Enable this one.
4. Use your existing OpenMW/MO export workflow to register this mod's data folder.
   Ensure `content=Randomised Basic Loot.omwscripts` is present once in the test OpenMW
   configuration and that the new data folder is registered. MO's checkbox alone
   does not guarantee OpenMW sees the scripts.
5. Restart OpenMW. Runtime record creation requires OpenMW 0.51+.

There are no required expansion/OAAB masters. Missing optional base IDs simply
cannot be selected. This package does not edit the installed masters or profiles.

## Included

- Exact static pools for Morrowind, Tribunal, Bloodmoon, and OAAB Data.
- Independent chance and modifier/unique roll for every eligible non-projectile item copy on a corpse.
- Projectile stacks roll once and replace the initially allowed quantity with one of three fixed quality grades; later added excess stays ordinary. No projectile unique drops.
- Prefix, suffix, or both, configurable with equal `1/1/1` weights by default.
- Independent six-tier distributions, tier-specific names, and upper-tier gates.
- Physical damage, armor, condition, weight, speed, reach, capacity; optional value.
- The magic catalogue plus slot-aware gap families, including charged melee effects.
- All 3,000 fixed unique registry drafts; four per approved exact base ID.
- Final-weight armor classification before armor-skill selection/binding.
- Preserved condition percentage and ownership during corpse replacement.
- Worn replacements are re-equipped in their original slots by the NPC's local script.
- Unworn inventory replacements remain unworn; an equipped stack assigns only one copy.
- Saved rolls, generated records, resolved modifier metadata, and no corpse rerolls.
- Once-per-save uniques by default, with double-affix fallback when valid uniques run out.
- Paired bargain affixes, including on-strike target debuffs with target buffs.
- Distinct names at all six bargain tiers; stronger benefits with growing costs.
- Exterior regional biases and curated vanilla Dwemer interior-family biases.

The test preset has 100% ordinary modification chance per eligible item and a 1%
global unique chance, all six tiers enabled, advanced gap families enabled, and a
high value cap. All otherwise eligible bases may roll T6. Unsupported family tiers
fall downward to an available lower tier.

Scripted, source-enchanted, restocking, missing, or subtype-mismatched bases are
skipped even if listed. This conservative script policy means some guards still
will not qualify. Uniques do not bypass it. No vampire/Legion script compat is
claimed in this build.
The base-game pool was derived from approved normal leveled lists and standard
clothing IDs, plus the ten explicitly approved standard Glass armor bases. It is
not every unenchanted item in Morrowind. A 100% chance applies only after the static-pool and
safety checks. With Routine Logging enabled, skipped inventory entries now report
their exact record ID and exclusion reason.

Standard Glass IDs: `glass_helm`, `glass_cuirass`, `glass_greaves`, `glass_boots`,
`glass_pauldron_left`, `glass_pauldron_right`, `glass_bracer_left`,
`glass_bracer_right`, `glass_shield`, and `glass_towershield`. No named or enchanted
variants are added. Optional mods that attach scripts/enchantments to these bases
can still cause them to be skipped under the existing runtime safety policy.

## Console Samples

Open the console and enter `luag`. Then enter one command at a time:

```lua
require('openmw.interfaces').RandomisedBasicLoot.giveTestKit('iron_helmet')
```

Adds a T1 prefix sample, a T1 suffix sample, a T1 dual sample, and all four Iron
Helmet uniques. The revised named helmets exercise different final armor classes.

```lua
require('openmw.interfaces').RandomisedBasicLoot.giveTestKit('iron longsword')
require('openmw.interfaces').RandomisedBasicLoot.giveTestKit('common_glove_left_01')
require('openmw.interfaces').RandomisedBasicLoot.giveTestKit('extravagant_amulet_02')
```

Optional Bloodmoon content:

```lua
require('openmw.interfaces').RandomisedBasicLoot.giveTestKit('bm bear cuirass')
```

Force a layout/tier or spawn only the uniques for a particular base:

```lua
require('openmw.interfaces').RandomisedBasicLoot.giveRoll('iron longsword', 'both', 6)
require('openmw.interfaces').RandomisedBasicLoot.giveRoll('iron_helmet', 'prefix', 6)
require('openmw.interfaces').RandomisedBasicLoot.giveRoll('iron_helmet', 'unique')
require('openmw.interfaces').RandomisedBasicLoot.giveUniqueSamples('iron_helmet')
require('openmw.interfaces').RandomisedBasicLoot.giveGapSamples('common_glove_left_01')
require('openmw.interfaces').RandomisedBasicLoot.giveBargainSamples('iron_helmet', 1)
require('openmw.interfaces').RandomisedBasicLoot.giveBargainSamples('iron longsword', 6)
```

The forced tier still respects each base's available families and folds downward
if unavailable. Families remain random, so forcing T6/both does not guarantee
one particular perfect pair. The unique command ignores tier arguments.
With `debug = true`, commands print each generated name and dynamic record ID in the OpenMW log.
Samples do not consume once-per-save unique discovery state.

## Suggested In-Game Checks

These are instructions for your manual testing, not tests already performed.

1. Inspect sample names, weights, physical stats, effects, and armor classes.
2. Equip/unequip CE samples. Check effects disappear, especially drained attributes.
3. Strike with a charged melee sample; check Touch delivery, charge use, and recharge.
4. Check a physical-only item has no enchantment and remains self-enchantable.
5. Capacity plus a magic affix is intentionally a dead capacity modifier. Do not
   treat that ordinary combination as an error or apply this policy to uniques.
6. Kill a fresh NPC carrying several eligible items. At 100%, every eligible copy
   should be replaced, not retained alongside its generated copy. Each item gets
   its own prefix/suffix/both/unique selection, except projectiles: each original
   projectile stack rolls once for a fixed quality prefix. Total counts stay unchanged.
7. A damaged source should retain its condition percentage after replacement.
   Armor/clothing originally worn should remain visible on the corpse after the
   replacement equipment update. Spare inventory items must not displace it.
8. Close/reopen the corpse window if needed for queued inventory changes to appear.
9. Save/reload, then revisit that corpse: no second generation should occur.

Within this renamed build, previously processed corpses stay processed. Existing
generated item records are not rewritten. However, the script namespace has
changed: saved state and script attachments from the older prototype are not
automatically migrated. Start a fresh disposable test save for this package.
For the per-item update, use NPCs not already processed by an earlier build.
The equipment fix applies to new replacements, not previously stripped corpses.
The latest fix passes the local `self` object required by `Actor.setEquipment`,
not the read-only `self.object` wrapper rejected by the installed engine.
Report `Randomised Basic Loot equipment restore error` or equipment transfer
timeout messages if the NPC still loses worn items.
Large ammunition stacks can produce many variants and may take longer to process.

## Configuration

After loading a game, open **Options > Scripts > Randomised Basic Loot**.
Install the complete package, including the updated `.omwscripts` file and new
`settings_player.lua`, then re-export and restart OpenMW. Page registration runs
in the player context; the globally registered groups still supply saved loot settings.
The page now exposes general toggles, chances, affix layout weights, six-tier
weights and enables, optional source packs, and physical percentage caps.
**Routine Logging** controls the informational messages shown in the console/log.
Errors remain visible even when routine logging is off.

Menu chances and caps use percentages: `100` means 100%, not a probability of 100.
Changes affect the next corpse or console sample roll without restarting.
They never reroll processed corpses or rewrite existing generated items.
Settings are stored in the save, not as permanent cross-profile preferences.
Turning on an optional source pack does not install or require its content.

`scripts/randomisedbasicloot/config.lua` supplies initial defaults for settings
that have not been stored yet, plus the RNG seed. Saved menu values take precedence
over file defaults. Reset a setting in the menu to use its current file default.
Edit that file in this test mod only when changing the development defaults.

- `debug`: routine output toggle. Testing builds use `true`; production builds
  should default to `false`. This controls death notifications, replacement
  messages, skipped-item diagnostics, and sample-spawn messages. Generation errors,
  equipment restore errors, and transfer timeouts remain visible regardless.
- `dropChance`: ordinary modification chance after the unique check (launch: `2/3`; testing package: `1.0`). Projectiles use this chance directly per allowed stack.
- `uniqueChance`: independent global chance per eligible equipment copy (default: `0.01`; force `1` for corpse testing). Projectiles are exempt.
- `affixLayoutWeights`: `prefix`, `suffix`, `both`; zero disables that branch.
- `npcTierScaling`: defaults true; ordinary corpse tier weights flatten with NPC level, not player level.
- `equalTierLevel`: defaults 25; level 1 retains starting weights, level 25+ reaches equality. See [NPC Tier Progression](NPC-TIER-PROGRESSION.md).
- `tierWeights`: weights for T1 through T6; `enabledTiers` controls available tiers.
- `sourcePacks`: optional `base`, `tribunal`, `bloodmoon`, `oaab` ID packs.
- `allowUniqueDuplicates`: defaults false; successful insertions consume unique IDs per save.
- `bargainAffixes`: paired boon/drawback affixes, enabled by default.
- `regionalFlavor`: regional affix selection biases, enabled by default.
- `compositionCaps`: ordinary physical percentage bounds.
- `appraisal`: opt-in gold-value modifier, initially false.

Restart after changing file defaults or the RNG seed; use the menu for live edits.
The seed initializes a new loot state, not an existing saved RNG sequence.
The JSON/MD registry is development source;
the packaged `*_uniques.lua` files are exported runtime snapshots. Regenerate
them with `tools/export_runtime_design.py` after editing the registry.

## Limits And Risk

This is the full currently specified loot-generation path, not a release-ready v1.
The focused Lua extension harness checks discovery, bargains, regional selection,
and native record construction with mocked OpenMW APIs. No engine tests were run.
Queued replacement timing, enchantment behavior, engine limits, other mods'
exact-ID checks, and balance require in-game validation. Native mechanisms cannot
promise compatibility with unrelated quest mods that reference approved base IDs.
Most unique entries are distinct compiled design drafts, not bespoke authored
conditional mechanics. Physical ammunition designs have limited native mechanics.

Merchants, containers, player inventory, creatures, lore tooltips, and custom
scripted unique powers are not generation targets. Current loot changes occur on
NPC corpses; sample commands explicitly add items to the player for inspection.

API references: [record templates and item instance data](https://openmw.readthedocs.io/en/openmw-0.51.0/reference/lua-scripting/openmw_types.html),
[enchantments, removal, and ownership](https://openmw.readthedocs.io/en/openmw-0.51.0/reference/lua-scripting/openmw_core.html).
The in-game page uses the built-in [Settings interface](https://openmw.readthedocs.io/en/openmw-0.51.0/reference/lua-scripting/interface_settings.html).
# Expanded-Effect Update (2026-10-04)

Replace the test mod with the rebuilt archive and restart OpenMW. Existing corpses
and generated items are not rerolled. In Options > Scripts > Randomised Basic Loot,
**Expanded Spell-Effect Affixes** controls the new families. Expansion summons
also require the installed expansion and its enabled source switch.
Cast When Used items use the normal enchanted-item selection/casting workflow;
they are not constant effects. Weapon strike effects are melee-only.
The detailed allocations and exclusions are in `docs/reports/expanded-affixes.md`
in the working project. This update has not been tested; no tests were run.
