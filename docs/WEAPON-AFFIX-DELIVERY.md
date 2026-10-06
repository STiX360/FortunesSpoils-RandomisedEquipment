# Weapon Affix Delivery

Applied to ordinary affixes only. Existing generated records and authored unique
templates keep their effects, values and delivery. Base item attack speed and
physical damage are not modified by this policy.

| Weapon class | Native slots | Control duration factor |
| --- | --- | ---: |
| Short blades | short_blade | x1.00 |
| One-handed blades, axes and blunt | long_blade_one_hand, axe_one_hand, blunt_one_hand | x0.75 |
| Two-handed blades and axes | long_blade_two_hand, axe_two_hand | x0.55 |
| Warhammers and spears | blunt_two_hand_close, spear | x0.45 |
| Staves | blunt_two_hand_wide | x1.25 |

Control families: Paralysis, Silence, Blind, Sound, Burden, Drain Attribute/Skill,
and Absorb Attribute/Skill. Their duration is rounded half upward to a minimum
of one second. Magnitudes stay unchanged on non-staff weapons. If a bargain
contains a control effect, both the benefit and drawback share the scaled
duration, preserving the authored tradeoff.

| Paralysis tier | Short blades | One-handed | Two-handed blades/axes | Warhammers/spears | Staves |
| --- | ---: | ---: | ---: | ---: | ---: |
| T1 | 2 | 2 | 1 | 1 | 3 |
| T2 | 3 | 2 | 2 | 1 | 4 |
| T3 | 5 | 4 | 3 | 2 | 6 |
| T4 | 7 | 5 | 4 | 3 | 9 |
| T5 | 10 | 8 | 6 | 5 | 13 |
| T6 | 15 | 11 | 8 | 7 | 19 |

## Staves

Offensive affixes that would normally be CastOnStrike instead use **CastOnUse,
Target**, launching a ranged spell when activated. Non-binary offensive
magnitudes are x1.5, rounded half upward. Control durations are x1.25. Binary
effects such as Paralysis and Silence retain their enabling magnitude.
All converted effects have a fixed **3-foot area**, never increasing by tier.
Paired target buffs/debuffs share the target, area and duration.

Only already eligible affixes are converted: no new effect pools are unlocked.
Effects without native on-target support are excluded on staves, not silently
changed to self or touch. Equipped CE bonuses and physical affixes are unchanged.
Native mixed-delivery restrictions remain: an activated target enchantment cannot
pair with a CE enchantment, but it can pair with another activated target affix
or a physical modifier. Costs and charge budgets use the final payload, including
the stronger magnitude, scaled duration, target cost multiplier and small area.

Non-staff direct strike-damage allocations are unchanged; their proposed class
multipliers have not been approved. Switching weapon skills is permitted.

Authoring policy: `tools/weapon_affix_rules.py`; exported native policy:
`weapon_affix_policy.lua`; runtime resolution: `weapon_affixes.lua`.
The website displays resolved class-specific rows, not unscaled baseline values.

Native delivery is supported by [OpenMW's enchantment type and spell range API](https://openmw.readthedocs.io/en/latest/reference/lua-scripting/openmw_core.html).
No tests were run; in-game staff projectile and area behavior remain unverified.
