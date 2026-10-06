# Utility Affix Progression

Applied to ordinary affixes only. Unique designs and already generated records
are unchanged. All eligible bases can roll all available tiers; no base unlocks
are introduced. Missing/functionally redundant tiers remain absent.

| Effect | T1 | T2 | T3 | T4 | T5 | T6 |
| --- | --- | --- | --- | --- | --- | --- |
| Water Breathing / Walking | Use: 15 sec | Use: 30 sec | Use: 60 sec | CE | - | - |
| Slowfall | Use: 1, 15 sec | Use: 2, 30 sec | Use: 3, 60 sec | CE: 5 | CE: 7 | CE: 10 |
| Levitate | Use: 15, 15 sec | Use: 15, 30 sec | Use: 15, 60 sec | CE: 15 | CE: 25 | CE: 50 |
| Light | CE: 5 | CE: 10 | CE: 15 | CE: 20 | CE: 25 | CE: 30 |
| Night Eye | CE: 3 | CE: 6 | CE: 9 | CE: 12 | CE: 15 | CE: 18 |
| Detect Creature (ft) | CE: 20 | CE: 40 | CE: 60 | CE: 80 | CE: 100 | CE: 120 |
| Detect Enchantment (ft) | CE: 10 | CE: 20 | CE: 30 | CE: 40 | CE: 50 | CE: 60 |
| Detect Key (ft) | CE: 5 | CE: 10 | CE: 15 | CE: 20 | CE: 25 | CE: 30 |
| Telekinesis (ft) | CE: 1 | CE: 2 | CE: 3 | CE: 5 | CE: 7 | CE: 10 |
| Swift Swim | CE: 5 | CE: 10 | CE: 15 | CE: 20 | CE: 25 | CE: 30 |
| Jump | CE: 3 | CE: 6 | CE: 10 | CE: 16 | CE: 25 | CE: 35 |
| Open (lock level) | Use: 10 | Use: 20 | Use: 30 | Use: 45 | Use: 65 | Use: 85 |
| Disintegrate Armor / Weapon | Strike: 5, 1 sec | Strike: 10, 1 sec | Strike: 15, 1 sec | Strike: 25, 1 sec | Strike: 40, 1 sec | Strike: 60, 1 sec |
| Command Humanoid / Creature (level cap) | Use: 5, 10 sec | Use: 15, 20 sec | Use: 25, 30 sec | - | - | - |
| Calm / Frenzy Humanoid / Creature (AI magnitude) | Use: 25, 10 sec | Use: 50, 20 sec | Use: 100, 30 sec | - | - | - |
| Rally / Demoralize Humanoid / Creature / Turn Undead (AI magnitude) | Use: 25, 10 sec | Use: 50, 20 sec | Use: 100, 30 sec | - | - | - |
| Restore Health / Magicka / Fatigue (pts/sec) | CE: 1 | CE: 2 | CE: 3 | - | - | - |
| Fortify Attack | CE: 5 | CE: 8 | CE: 12 | CE: 16 | CE: 20 | CE: 25 |
| Magical Shield (overall armor rating) | CE: 5 | CE: 8 | CE: 12 | CE: 16 | CE: 22 | CE: 30 |
| Reflect (percent) | CE: 3 | CE: 5 | CE: 7 | CE: 9 | CE: 12 | CE: 15 |
| Spell Absorption (percent) | CE: 1 | CE: 2 | CE: 3 | CE: 4 | CE: 5 | - |
| Paralysis | Strike: 2 sec | Strike: 3 sec | Strike: 5 sec | Strike: 7 sec | Strike: 10 sec | Strike: 15 sec |

CE means active while equipped, not a permanent character upgrade. Water effects
gain clean permanency at T4 without draining drawbacks. Slowfall and Levitate
retain distinct upper-tier names because their magnitudes differ.

Night Eye scales less than Light as a balance choice, not a claim that their
magnitudes are directly interchangeable. Detection ranges follow
Creature > Enchantment > Key at every tier.

Existing slot restrictions remain: Water Breathing on helmets/amulets; Water
Walking on boots/shoes; Slowfall on skirts/robes/amulets; Levitate on
shoes/robes/amulets, never boots. Chameleon remains robes/amulets only.
Cure Blight is excluded. Expansion effects still require loaded content and
the corresponding enabled source configuration.

Invisibility, summons, bound equipment and activated actions remain on-use.
CE regeneration is amulet-only and suffix-only. The generator selects at most
one suffix, so Health, Magicka and Fatigue regeneration cannot combine on an
ordinary generated item. These families have no T4-T6 candidates. Unique
templates remain exempt from ordinary-affix restrictions.

Command uses target level caps; Calm/Frenzy modify AI settings, not target level.
Rally, Demoralize and Turn Undead modify AI Flee settings and use the same
three-tier AI magnitude/duration progression. Charm retains its existing allocation.
Fortify Attack is restricted to wielded weapons (not projectiles). Magical Shield
is restricted to shields and amulets. Other defenses and Fortify effects retain
their existing allocations.

Dispel remains on-use on self, from ring/amulet suffixes,
at 5/10/15/20/30/40 percent removal chance. It is not an outgoing strike effect.
Reflect is a CE amulet suffix at 3/5/7/9/12/15 percent. Spell Absorption is a CE
ring/amulet suffix with only T1-T5 at 1/2/3/4/5 percent; no redundant T6 is added.
Both have family weight x0.25. Paralysis uses baseline 2/3/5/7/10/15-second
durations and family weight x0.25. Ordinary weapon control durations are
class-scaled; staves instead cast on use, on target with stronger values and a
fixed 3-foot area. See [Weapon Affix Delivery](WEAPON-AFFIX-DELIVERY.md).
Higher charged tiers also increase the minimum base-cost cast budget.

Paralysis reference: read-only inspection of the unmodified Morrowind.esm ENCH
and WEAP records found `paralysis_en` at 10 seconds (Steel/Glass Jinkblade,
Steel/Dwemer Jinksword and staves of peace), and `steel jinkblade of the aegis_en`
at 20 seconds. The new curve reaches the common vanilla benchmark at T5 and
remains below the Aegis duration at T6. No game tests were run.
Different native enchantment modes cannot pair, including across a family's
delivery transition. Physical modifiers can pair with either mode.

The static catalogue keeps mixed-delivery utility families in one entry, with
delivery shown in tier values. Weapon-specific profiles have separate resolved
class rows so their values and delivery remain accurate under equipment filters.
No tests were run for this update; these allocations need permitted engine testing.
# Equipment Pool Redistribution

Ordinary Resist Common Disease, Resist Blight Disease, Resist Paralysis and
Resist Magicka are restricted to rings, amulets and belts. Their magnitudes,
suffix placement and unique templates are unchanged.

Gold value is now a suffix (still controlled by `appraisal`). Fire/Frost Resistance,
Jump, summons, bound equipment, Burden, Blind and Sound are prefixes. Feather,
Intelligence and Willpower no longer have duplicate suffix families. Weight reduction
remains a prefix; final-weight armor skill selection is unchanged. Belts cannot roll
cures or restores. Unique templates and existing generated items are unchanged.

Projectiles use three fixed quality prefixes and one roll per original stack instead
of normal affix tiers, layout weights and unique chance. See
[Projectile Quality](PROJECTILE-QUALITY.md) for values and record reuse rules.
