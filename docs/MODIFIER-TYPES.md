# Modifier Types

The catalogue uses three modifier types, classified per individual affix:

| Type | Definition | Examples |
| --- | --- | --- |
| Crafted | Changes a base item property | Damage, armor, weight, condition, value, weapon speed, reach, enchantment capacity |
| Magical | Adds one spell effect, regardless of delivery mode | Fortify Strength, Light, Water Breathing, cast-on-use Levitate, on-strike Fire Damage |
| Hybrid | Adds two or more effects within one affix | Resist Shock plus Weakness to Frost; a base-stat change paired with a spell effect |

Hybrid takes precedence when an affix has multiple effects, whether these are
beneficial, detrimental or mixed. Two base-stat effects also count as Hybrid.
A prefix-plus-suffix item is not automatically Hybrid: classify each affix
separately. Enchantment capacity is Crafted because it changes the base item
property rather than adding a spell effect.

## Catalogue Mapping

- Former Physical entries are Crafted.
- Former Magic and Utility entries are Magical.
- The current two-effect Bargain entries are Hybrid.

The current exporter has single-effect physical and magical families plus paired
bargain families. Future multi-effect families must be classified Hybrid even if
they are not bargains or contain no drawback. Utility remains a description of
an effect's purpose, not a separate modifier type.

These are website/documentation labels only. Runtime module names, setting keys,
Lua interfaces, generation probabilities and effect values are unchanged.
No tests were run for this presentation update.
