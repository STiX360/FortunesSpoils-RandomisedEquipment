# Current In-Game Validation

Prepared 2026-10-07. Automated checks: 39 Python tests, Lua 5.1 compilation,
the current smoke harness and loot-extension harness pass. These use mocked
OpenMW APIs, not a running engine. The package remains release-unvalidated.

## Setup

Install the rebuilt testing ZIP into a disposable Mod Organizer profile, enable
`Randomised Basic Loot.omwscripts` in OpenMW and restart the game. Do not replace
the separate POTI playthrough. Start a new game with this build enabled so NPC
inventory allowances can be captured before interaction. First-time installation
into an existing save deliberately disables corpse rolls; upgrading an older
mod save skips previously visited NPCs without a trusted snapshot. Already
processed corpses never reroll. Saved settings override package defaults.

Under Options > Scripts > Randomised Basic Loot, set generation to 100%, unique
chance to 0%, and logging on for ordinary-affix checks. Keep expanded affixes on.
Restore your preferred settings after testing.

## Corpse Replacement And Appearance

Kill a fresh NPC normally with an eligible robe/shirt, armor and weapon. Every
eligible copy should be replaced, with no retained original alongside it.
Originally worn clothes and armor should remain on the corpse; unworn spares
must not displace worn items. Wait briefly for the queued equipment update.
Look for generation errors, equipment restore errors or transfer timeouts in logs.
Scripted, already enchanted and non-allowlisted items are expected to stay unchanged.

## Projectile Stacks

Use a fresh NPC carrying a known quantity of ordinary Iron Arrows, ideally 200.
At 100% generation, the entire original stack should become one Honed, Keen or
Piercing stack with exactly that quantity. No suffixes, enchantments or uniques.
Base weight/value stay unchanged. Equip and fire them: they must function normally.
Collect two matching quality stacks from separate corpses and check whether they
merge, both while unequipped and while the matching arrows are equipped. Report
any difference: mocked record reuse does not validate native stacking behavior.
Repeat with bolts and thrown weapons if available.

## Sold And Planted Items

On the new test game, meet a living merchant before selling anything. Record
their eligible original equipment counts. Sell or reverse-pickpocket many eligible
items into them, including both a different base and extra copies of an original
base. Save/reload before killing them normally, with generation at 100%.

Only the frozen initial counts may roll. Added base IDs must remain ordinary;
extras of an original base must remain beyond its original quantity allowance.
For arrows, an initial 20 merged with 200 added arrows must yield 20 graded arrows
and 200 ordinary arrows, not 220 graded arrows. Worn originals take priority over
unworn extras. Repeat without a reload to compare behavior.

Also check an older mod save: already visited NPCs with no saved allowance must
remain unchanged. A first-time installation on an existing save must produce no
corpse replacements. Console samples remain available in either case.

This is a quantity cap, not perfect provenance: replacing an original with an
identical base can still use its original allowance. Legitimate later acquisitions
also do not expand it. See [Inventory Allowances](INVENTORY-ALLOWANCES.md).

## Resistance Slots

Inspect new ordinary suffix loot on helmets, robes, shields, rings, amulets and
belts. Common Disease, Blight Disease, Paralysis and Magicka resistance must only
appear on rings, amulets and belts. Existing legacy items and uniques are exempt.
Use sample commands below for belts and jewelry. Random sampling is not proof
that a valid affix exists, but any forbidden new placement is a failure.

## Melee Damage Scaling

For T6 Sunscorched (Fire Damage), expect
`max(1, floor(15 * clamp(1 / baseSpeed, 0.75, 1.50) + 0.5))` points for one second.
Base speed 1.5 gives 11, 1.0 gives 15, and 0.75 gives 20. Check the actual loaded
base speed rather than assuming speed from weapon class or the item's final speed.
Other mods may override the base record. A speed suffix must not alter the fire
magnitude at the same tier on the same base. Strike a target and check charge use
and delivery; target resistance can reduce actual damage below the tooltip value.

## Console Samples

Enter `luag` first, then run these lines separately. `giveRoll` is random within
the requested layout/tier, not a command that selects a particular effect.
Repeat the weapon calls until a Sunscorched sample appears. Avoid large loops.

```lua
require('openmw.interfaces').RandomisedBasicLoot.giveRoll('iron dagger', 'prefix', 6)
require('openmw.interfaces').RandomisedBasicLoot.giveRoll('iron claymore', 'prefix', 6)
require('openmw.types').Weapon.records['iron dagger'].speed
require('openmw.types').Weapon.records['iron claymore'].speed
require('openmw.interfaces').RandomisedBasicLoot.giveRoll('common_belt_01', 'suffix', 6)
require('openmw.interfaces').RandomisedBasicLoot.giveRoll('common_ring_01', 'suffix', 6)
require('openmw.interfaces').RandomisedBasicLoot.giveRoll('common_amulet_01', 'suffix', 6)
require('openmw.interfaces').RandomisedBasicLoot.giveTestKit('iron arrow')
```

The arrow kit gives all three fixed grades. Use `exit()` to leave Lua mode.

## Uniques And Persistence

Change unique chance to 100% temporarily, leaving duplicate uniques disabled.
On disposable NPCs carrying the same base, check that named templates do not repeat
until exhausted; subsequent rolls fall back to ordinary dual affixes where feasible.
Projectiles must still produce quality grades, not unique drops.
Save, fully exit/reload, then revisit a corpse: no extra generation. Previously
looted items must retain names, effects, counts and equipped behavior. Matching
projectile grades generated after reload should continue to reuse their records.

## NPC-Level Tier Scaling

Under Tier Distribution, enable NPC tier scaling and set the equality level to 25.
Use generation 100%, unique chance 0%, logging on and all six default tier weights.
Kill fresh tracked NPCs across low levels, level 20 and level 25+. Logs should show
the NPC's level (not unknown). Higher-level loot should trend toward higher tiers;
a small sample cannot prove the distribution. Level 25+ requests equal tier weights,
but shorter-tier effect families and compatibility filtering still affect outcomes.
Disable scaling to restore the starting distribution. Console forced-tier samples
are unaffected. Existing items must not change. See [the curve](NPC-TIER-PROGRESSION.md).

## Report

Send the base item ID, generated name, tooltip screenshot and relevant log lines
for a failure. For stacking issues, include both stack counts and whether one was
equipped. For tier-scaling issues, also include the NPC level and tier settings.
