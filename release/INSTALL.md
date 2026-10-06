# Fortune's Spoils - Randomised Equipment

Development build for OpenMW. Not validated for production saves.

Start a new game with this build enabled for corpse-loot testing. Initial NPC
inventory counts are frozen before interaction; selling or planting extra items
does not increase their roll allowance. First-time installation into an existing
save disables corpse rolls. Upgrading an older mod save skips already visited
NPCs without a trusted snapshot; newly initialized NPCs can be tracked. Existing
generated items and saved trusted allowances are retained. Console samples work
regardless. This deliberately conservative policy avoids trusting traded inventory.

Install this archive into a separate Mod Organizer test profile. The archive
root contains `scripts/`, `l10n/`, and `Randomised Basic Loot.omwscripts`.
Register the mod data directory with OpenMW and enable
`content=Randomised Basic Loot.omwscripts`, then restart OpenMW.

The runtime identity and file name intentionally retain Randomised Basic Loot
to avoid changing saved-script identity. Settings are under Options > Scripts >
Randomised Basic Loot after loading a game.

Testing builds default to 100% replacement and routine logging enabled.
Production builds default to 33% single affix (split equally between prefix and
suffix), 33% dual affix, 33% unchanged and 1% unique per eligible equipment copy.
The ordinary modification setting is 66.6667% after the independent unique check;
layout weights are 1 / 1 / 2. Projectiles remain unique-exempt fixed-grade rolls.
Routine logging is off. A production profile is not evidence of validation.
Ordinary affix tiers scale with NPC level by default: starting weights at level 1,
equal tier weights at level 25+. Player level does not affect rewards. The toggle
and equality endpoint are under Tier Distribution. Uniques/projectiles are exempt.
Saved settings override these defaults. Use disposable saves for testing.

Morrowind is required. Tribunal, Bloodmoon, and OAAB Data are optional installed
content sources; their original assets are not included.
