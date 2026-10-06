# NPC-Level Tier Progression

Ordinary corpse affixes use the defeated NPC's current level at generation time,
not player level. Starting tier weights remain 78 / 15 / 5 / 1.5 / 0.4 / 0.1.

```
rarity = 1 - clamp((NPC level - 1) / (equalTierLevel - 1), 0, 1)
effective weight = starting weight ^ rarity
```

Defaults: `npcTierScaling = true`, `equalTierLevel = 25`. Both are configurable
under Options > Scripts > Randomised Basic Loot > Tier Distribution.
Level 1 preserves starting weights; level 13 gives the square-root weights;
level 25 and above gives equal weights. Missing/invalid levels use starting weights.
Zero starting weights stay zero and existing disabled-tier rules remain respected.
Turning scaling off restores configured starting weights at every NPC level.

The corpse reads `types.Actor.stats.level(actor).current`, documented by
[OpenMW 0.51](https://openmw.readthedocs.io/en/openmw-0.51.0/reference/lua-scripting/openmw_types.html#ActorStats).
The adjusted weights are separate from saved configuration and do not accumulate.

Prefix and suffix retain the existing independently weighted tier selection,
subject to compatibility filtering. Families with fewer tiers retain lower-tier
fallback, so equal requested-tier weights do not guarantee equal final tiers for
every effect. Configured generation/layout chances and global unique chance stay
unchanged. Unique exhaustion's ordinary fallback uses the NPC curve too.
Projectiles keep fixed quality grades. Console samples have no corpse level and
retain their existing behavior, including explicit forced tiers.

Existing generated items are not rewritten. New settings default on in older saves
when unset; trusted inventory allowances are still required for corpse generation.

At launch defaults, theoretical T6/T6 per eligible item is 0.000033% at level 1,
0.011267% at level 13, 0.189495% at level 20 and 0.916667% at level 25+.
These assume feasible independent T6 affixes and exclude unique-exhaustion fallback.
