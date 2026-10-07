# Fortune's Spoils 0.1.0 - Early Beta

The first 0.X.X release: functional early beta, not balanced for regular play.

Fortune's Spoils brings randomised equipment loot to OpenMW: familiar base items
can gain named prefixes and suffixes, physical stat changes, magical effects, or
become predetermined named uniques with specialised benefits and drawbacks.

This is a functional early beta, **not a balanced playthrough recommendation**.
Expect rough edges and changing balance. Bug reports, overlooked interactions,
unexpectedly strong or weak rolls, and general balance feedback are welcome.
Use a separate profile and disposable saves when trying it out.

![Generated corpse loot and dual-affix shirt tooltip](https://raw.githubusercontent.com/STiX360/FortunesSpoils-RandomisedEquipment/v0.1.0/docs/images/loot-example.png)

*Player-provided screenshot from a modded game; other visible mods are not included.*

## Highlights

- Rolls independently for eligible equipment copies on a corpse.
- Production chances: 33% single affix, 33% prefix and suffix, 33% unchanged,
  and 1% unique. These rates apply after eligibility checks; projectiles differ.
- Tier-specific modifier names, contextual slot restrictions and regional biases.
- NPC-level tier progression reaches equal tier weights at level 25; powerful
  rolls remain possible below that level.
- Projectile stacks use three fixed quality grades rather than a sprawling
  affix pool. No projectile unique drops.
- Optional Tribunal, Bloodmoon and OAAB Data support without hard dependencies.
- Configurable settings under Options > Scripts > Randomised Basic Loot.

## Requirements And Limitations

Requires Morrowind and OpenMW 0.51+. Existing saves are supported by default:
living NPC inventories are capped on first observation. Accepted trade-off:
items traded or planted before that snapshot may roll. Later additions cannot
expand the cap. Strict Inventory Tracking is an optional toggle restoring the
new-game-on-first-install requirement. Already generated items are not
retroactively rebalanced, and processed corpses never reroll.

Only approved eligible bases roll. Scripted and already enchanted source items
are excluded, including some guard equipment. This is not a blanket replacement
of every item in the game. Selling or planting items after an NPC's snapshot
does not expand their captured roll allowance.

Pre-v1 save compatibility is not a final legacy-affix guarantee. Back up saves
before updates; safe removal/downgrading is not promised. In-game release
validation remains incomplete. Corpse loot on an existing save has been manually
reported working; this is not blanket verification of stacking, persistence,
optional content or every effect. See the separate `INSTALL.md` release download.

## Website Companion

The modifier catalogue and Loot Simulator are player-reference website resources,
not in-game features. Explore a base item, NPC level and location using standard
mod probabilities; actual results can differ with saved settings and other mods.
Item imagery is attributed to UESP and the OAAB Library on the website.

## Downloads And Feedback

Install `fortunes-spoils-0.1.0-production.zip`. It contains only the mod's runtime
files, not the website, screenshot, development tools, or build metadata. The
companion `.manifest.json` and `.zip.sha256` support artifact verification.
Do not install GitHub's source-code ZIP as the mod.

[Installation](https://github.com/STiX360/FortunesSpoils-RandomisedEquipment/blob/v0.1.0/release/INSTALL.md)
| [Modifier Catalogue](https://stix360.github.io/FortunesSpoils-RandomisedEquipment/)
| [Loot Simulator](https://stix360.github.io/FortunesSpoils-RandomisedEquipment/simulator.html)
| [Bug Reports And Balance Feedback](https://github.com/STiX360/FortunesSpoils-RandomisedEquipment/issues)

Please include OpenMW version, relevant settings, installed optional content,
base item IDs, screenshots and relevant logs when reporting a problem.
