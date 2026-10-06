# Projectile Quality And Pool Redistribution

Applies to new generation only. Existing generated records and the unique
registry are retained. No engine or automated tests have been run for this update.

## Fixed Projectile Grades

Arrows, bolts and thrown weapons use a dedicated pool, outside normal tier,
layout, unique, appraisal and regional settings. The configured generation
chance still applies, once per original inventory stack, not per projectile.
A successful roll replaces the whole quantity with one grade.

| Grade | Prefix | Damage bonus | Conditional chance |
| --- | --- | --- | --- |
| 1 | Honed | +1 | 80% |
| 2 | Keen | +2 | 18% |
| 3 | Piercing | +3 | 2% |

Each positive minimum and maximum attack damage channel receives the bonus;
zero channels stay zero and values are capped at 255. Weight, value and all
other base stats are unchanged. No enchantments, suffixes, dual rolls or unique
drops are generated. There are at most three new quality records per exact base
per save, keyed by base ID and grade. Existing unique definitions are not deleted.
Native condition/equipment rules can still affect stacking; record reuse avoids
random affix permutations but does not promise every engine stack will merge.

`giveTestKit(baseId)` produces the three grades for a projectile base.
`giveRoll(baseId, 'prefix', grade)` accepts grades 1-3; incompatible layouts
and unique sample requests are rejected explicitly.

## Equipment Pool Changes

- Gold value moves to suffix; its opt-in `appraisal` toggle is unchanged.
- Weight reduction remains prefix so armor skills resolve against final weight.
- Fire and Frost Resistance, Jump, summons and bound equipment become prefixes.
- Burden, Blind and Sound become weapon prefixes, retaining class/delivery scaling.
- Feather, Fortify Intelligence and Fortify Willpower are prefix-only.
- CE regeneration remains amulet-only suffixes, mutually exclusive on ordinary items.
- Belts cannot roll cures or restores. Cures remain on amulets; Attribute/Skill
  restores remain on rings. Other applicability and unique templates are unchanged.

## Deferred Manual Checks

When testing is authorised, check full quantity replacement at 100% generation,
unchanged original stacks on a failed roll, shared record IDs for repeated grades,
save/reload record reuse, equipped projectile restoration, and that old generated
projectiles remain usable. Also inspect the updated prefix/suffix catalogue.
