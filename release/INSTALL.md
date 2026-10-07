# Fortune's Spoils - Randomised Equipment

Randomised equipment drops for OpenMW. This is a functional early beta, not a
balanced or stable-release recommendation for a long-term playthrough. Bugs,
oversights and balance feedback are welcome. In-game release validation remains
pending. Keep a backup of your saves and use a separate profile.

## Requirements

- OpenMW 0.51 or newer and Morrowind.
- Tribunal, Bloodmoon and OAAB Data are optional. They are not hard dependencies;
  their original assets are not included.
- Existing saves are supported by default; back up your save before installation.

## Installation

1. Install the ZIP in Mod Organizer as a mod named `Fortune's Spoils`.
2. Select the archive root as the data directory if prompted. It contains
   `scripts/`, `l10n/`, and `Randomised Basic Loot.omwscripts`.
3. Disable any previous prototype copy to avoid loading duplicate scripts.
4. Use your OpenMW/Mod Organizer export workflow to register the mod's data
   directory, then enable `Randomised Basic Loot.omwscripts` in OpenMW's content
   list. The configuration should contain this entry once:
   `content=Randomised Basic Loot.omwscripts`.
5. Restart OpenMW and load your save or start a new game. The Mod Organizer checkbox alone does
   not guarantee that OpenMW has loaded the mod.

For pre-release testing, use a disposable save and a separate profile rather
than replacing a mod installation used by an ongoing playthrough.

## Saves And Updates

By default, the mod freezes each living NPC's eligible inventory counts when it
first observes them, including in an existing save. Later selling or planting
items does not increase that allowance. Existing generated items, saved inventory
caps and processed corpses are retained; processed corpses never reroll.

**Accepted trade-off:** inventory already sold or planted before that first
snapshot can be treated as original loot and roll. The mod cannot reconstruct
an NPC's past inventory. Existing-save support is preferred over blocking all
loot on those saves. A new game gives stronger provenance protection.

To restore the earlier conservative policy, enable **Strict Inventory Tracking
(Require New Game On First Install)** under General. Its config key is
`requireNewGameInventory`, default `false`. Strict mode blocks first-install
existing-save corpse rolls and refuses loaded NPCs without a trusted snapshot.
Switching modes does not expand a saved cap, erase generated items or reroll
processed corpses. After disabling strict mode, missing/policy-blocked snapshots
can be captured when living NPCs next activate or load; genuine empty snapshots
and failed captures are not expanded.

The runtime identity and file name intentionally retain Randomised Basic Loot
to avoid changing saved-script identity. Settings are under Options > Scripts >
Randomised Basic Loot after loading a game.

Do not assume removing the mod or downgrading a save containing generated items
is safe. Back up the save before updates. A final legacy-affix compatibility
guarantee will be established at v1, not during this pre-release stage.

## Loot And Settings

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

Only approved, eligible base items roll. Scripted, already enchanted and other
excluded items stay unchanged. A generation setting of 100% does not bypass
these safety checks. Projectiles use a small fixed quality pool to limit stack
fragmentation; they do not receive ordinary affix combinations or uniques.

## Website Resources

The website provides a modifier catalogue and a Loot Simulator for player
reference. The simulator is a website tool, not an in-game mod feature. It uses
standard mod settings; your saved settings and other mods can change actual
results. Website images require internet access; the mod does not.

## Reporting Problems

Include your OpenMW version, optional content installed, relevant settings,
whether the save is new or upgraded, the base item ID if known, and a tooltip
screenshot. Include relevant OpenMW log lines for missing loot, equipment
restoration errors or save/load issues. Avoid sharing API keys or private paths.

## A Note on Save Scumming

Yes, reloading a save to fish for better loot is an exploit. But you wouldn't
do that... right?
