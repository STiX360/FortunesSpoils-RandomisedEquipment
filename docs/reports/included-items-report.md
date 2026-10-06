# Included Items Report

Prepared 2026-10-04.

This reports the current static item pool, not the equipment categories supported by the running prototype.
Hierarchy: mod/expansion -> category -> sub-category. Each included ID appears once.
Names and values are original source-master values, not POTI overrides.

Record IDs ending in `_unique` are excluded from every source pack.

Exact quest, unique, and artifact IDs are additionally excluded using `data/protected_item_ids.json`.
Wiki references and the current intersection audit: [Vanilla Enchantment Review](vanilla-enchantment-review.md).

## Mod / Expansion Summary

| Mod / Expansion | Armor | Weapons | Clothing | Total | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| Morrowind (Base Game) | 122 | 88 | 141 | 351 | Included |
| Tribunal | 8 | 6 | 12 | 26 | Included |
| Bloodmoon | 28 | 16 | 22 | 66 | Included |
| OAAB Data | 123 | 164 | 20 | 307 | Included |
| Tamriel Data / Other Mods | 0 | 0 | 0 | 0 | Not included |

**Total included IDs: 750.**

Base-game IDs: `mod/scripts/randomisedbasicloot/base_items.lua`.
Selection policy and generation limitations: [Base-Game Item Pool](base-game-item-pool.md).

Bloodmoon IDs: `mod/scripts/randomisedbasicloot/bloodmoon_items.lua`.
Bloodmoon selection is exactly the user-approved Nordic Mail, Wolf, and Bear armor sets
plus the Riekling Shield (28 armor IDs), the linked base clothing (22 IDs), and base weapons
excluding Stalhrim (16 IDs). Named enchanted variants and other unlisted items are not included.
This is an optional data pack, not a hard dependency.
IDs and values were checked against the installed vanilla `Bloodmoon.esm`, without editing POTI.
No value cap is applied to pool membership; Nordic Mail entries exceed the prototype's unchanged gameplay cap.

References: [Bloodmoon Base Clothing](https://en.uesp.net/wiki/Bloodmoon:Base_Clothing) and
[Bloodmoon Base Weapons](https://en.uesp.net/wiki/Bloodmoon:Base_Weapons).
Page item lists were verified in the browser and matched to expansion records.

Tribunal IDs: `mod/scripts/randomisedbasicloot/tribunal_items.lua`.
Tribunal includes eight Dark Brotherhood armor pieces, 12 base clothing IDs, and six base weapon IDs.
All Adamantium weapons and IDs ending in `_unique` are excluded. No extra variants are inferred.
Reference: [Tribunal Dark Brotherhood Armor](https://en.uesp.net/wiki/Tribunal:Dark_Brotherhood_Armor).
Additional references: [Tribunal Base Clothing](https://en.uesp.net/wiki/Tribunal:Base_Clothing) and
[Tribunal Base Weapons](https://en.uesp.net/wiki/Tribunal:Base_Weapons).
Page item lists were verified in the browser and matched to vanilla `Tribunal.esm`. This data pack is optional.

OAAB IDs: `mod/scripts/randomisedbasicloot/oaab_items.lua`.
Frozen allowlist: `data/oaab_item_allowlist.json`. New OAAB records are not automatically included.
Reviewed directly from the installed `OAAB_Data.esm`; no other POTI mods or overrides were scanned or edited.
Source SHA-256: `551be3f5ba070b6e472b60e712006bddece35043dee972da4fb85b8bcb896d5b`.
Include ordinary unenchanted equipment designs and visual variants, including Silver Scepter.
Exclude all source-enchanted records (including Chastening and Stormruler), IDs ending in `_unique`,
and unreviewed item scripts. Imperial Battlemage Cuirass retains the reviewed `LegionUniform` exception.
Also exclude the invisible Shield and both Glass Assassin pauldrons as special-purpose equipment.
Distinct Daedric faces and faction-style helmets are treated as base designs, not artifacts solely because of their names.
OAAB Adamantium and Stalhrim base designs are included; previous material exclusions remain scoped to Tribunal/Bloodmoon.
This source-level review does not guarantee compatibility with quests or exact-ID checks introduced by other mods.
OAAB is an optional data pack, not a hard dependency. Missing IDs must be skipped when runtime support is implemented.
References: [OAAB Data repository](https://github.com/OAAB-Modding/Data),
[scepter additions](https://github.com/OAAB-Modding/Data/discussions/228), and
[Glass Assassin equipment](https://github.com/OAAB-Modding/Data/discussions/166).

## Morrowind (Base Game) - 351 Items

Source: `Morrowind.esm`.

### Armor - 122 Items

#### Helmet - 16 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Boiled Netch Leather Helm | `netch_leather_boiled_helm` | 17 |
| Bonemold Helm | `bonemold_helm` | 150 |
| Chitin Helm | `chitin helm` | 19 |
| Dreugh Helm | `dreugh_helm` | 2250 |
| Dwemer Helm | `dwemer_helm` | 450 |
| Glass Helm | `glass_helm` | 12000 |
| Imperial Chain Coif | `imperial_chain_coif_helm` | 35 |
| Imperial Silver Helm | `silver_helm` | 120 |
| Imperial Steel Helmet | `imperial helmet armor` | 70 |
| Iron Helmet | `iron_helmet` | 30 |
| Netch Leather Helm | `netch_leather_helm` | 15 |
| Nordic Fur Helm | `fur_helm` | 15 |
| Nordic Iron Helm | `nordic_iron_helm` | 50 |
| Nordic Trollbone Helm | `trollbone_helm` | 65 |
| Orcish Helm | `orcish_helm` | 1200 |
| Steel Helm | `steel_helm` | 60 |

#### Cuirass - 19 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Boiled Netch Leather Cuirass | `netch_leather_boiled_cuirass` | 37 |
| Bonemold Cuirass | `bonemold_cuirass` | 350 |
| Chitin Cuirass | `chitin cuirass` | 45 |
| Dreugh Cuirass | `dreugh_cuirass` | 5250 |
| Dwemer Cuirass | `dwemer_cuirass` | 1050 |
| Glass Cuirass | `glass_cuirass` | 28000 |
| Imperial Chain Cuirass | `imperial_chain_cuirass` | 90 |
| Imperial Silver Cuirass | `silver_cuirass` | 280 |
| Imperial Steel Cuirass | `imperial cuirass_armor` | 150 |
| Imperial Studded Leather Cuiras | `imperial_studded_cuirass` | 65 |
| Iron Cuirass | `iron_cuirass` | 70 |
| Netch Leather Cuirass | `netch_leather_cuirass` | 35 |
| Nordic Bearskin Cuirass | `fur_bearskin_cuirass` | 35 |
| Nordic Fur Cuirass | `fur_cuirass` | 35 |
| Nordic Iron Cuirass | `nordic_iron_cuirass` | 130 |
| Nordic Ringmail Cuirass | `nordic_ringmail_cuirass` | 80 |
| Nordic Trollbone Cuirass | `trollbone_cuirass` | 165 |
| Orcish Cuirass | `orcish_cuirass` | 2800 |
| Steel Cuirass | `steel_cuirass` | 150 |

#### Left Pauldron - 11 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bonemold L Pauldron | `bonemold_pauldron_l` | 120 |
| Chitin Left Pauldron | `chitin pauldron - left` | 16 |
| Dwemer Left Pauldron | `dwemer_pauldron_left` | 360 |
| Glass Left Pauldron | `glass_pauldron_left` | 9600 |
| Imperial Chain Left Pauldron | `imperial_chain_pauldron_left` | 28 |
| Imperial Steel Left Pauldron | `imperial left pauldron` | 53 |
| Iron Left Pauldron | `iron_pauldron_left` | 24 |
| Netch Leather Left Pauldron | `netch_leather_pauldron_left` | 12 |
| Nordic Fur Left Pauldron | `fur_pauldron_left` | 12 |
| Orcish Left Pauldron | `orcish_pauldron_left` | 960 |
| Steel Left Pauldron | `steel_pauldron_left` | 48 |

#### Right Pauldron - 11 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bonemold R Pauldron | `bonemold_pauldron_r` | 120 |
| Chitin Right Pauldron | `chitin pauldron - right` | 16 |
| Dwemer Right Pauldron | `dwemer_pauldron_right` | 360 |
| Glass Right Pauldron | `glass_pauldron_right` | 9600 |
| Imperial Chain Right Pauldron | `imperial_chain_pauldron_right` | 28 |
| Imperial Steel Right Pauldron | `imperial right pauldron` | 53 |
| Iron Right Pauldron | `iron_pauldron_right` | 24 |
| Netch Leather Right Pauldron | `netch_leather_pauldron_right` | 12 |
| Nordic Fur Right Pauldron | `fur_pauldron_right` | 12 |
| Orcish Right Pauldron | `orcish_pauldron_right` | 960 |
| Steel Right Pauldron | `steel_pauldron_right` | 48 |

#### Greaves - 11 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bonemold Greaves | `bonemold_greaves` | 220 |
| Chitin Greaves | `chitin greaves` | 29 |
| Dwemer Greaves | `dwemer_greaves` | 660 |
| Glass Greaves | `glass_greaves` | 17600 |
| Imperial Chain Greaves | `imperial_chain_greaves` | 50 |
| Imperial Steel Greaves | `imperial_greaves` | 98 |
| Iron Greaves | `iron_greaves` | 44 |
| Netch Leather Greaves | `netch_leather_greaves` | 22 |
| Nordic Fur Greaves | `fur_greaves` | 22 |
| Orcish Greaves | `orcish_greaves` | 1760 |
| Steel Greaves | `steel_greaves` | 88 |

#### Boots - 10 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bonemold Boots | `bonemold_boots` | 100 |
| Chitin Boots | `chitin boots` | 13 |
| Dwemer Boots | `dwemer_boots` | 300 |
| Glass Boots | `glass_boots` | 8000 |
| Imperial Steel Boots | `imperial boots` | 50 |
| Iron Boots | `iron boots` | 20 |
| Netch Leather Boots | `netch_leather_boots` | 10 |
| Nordic Fur Boots | `fur_boots` | 10 |
| Orcish Boots | `orcish_boots` | 800 |
| Steel Boots | `steel_boots` | 40 |

#### Left Gauntlet - 6 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Chitin Left Gauntlet | `chitin guantlet - left` | 9 |
| Imperial Steel Left Gauntlet | `imperial left gauntlet` | 33 |
| Iron Left Gauntlet | `iron_gauntlet_left` | 14 |
| Netch Leather Left Gauntlet | `netch_leather_gauntlet_left` | 7 |
| Nordic Fur Left Gauntlet | `fur_gauntlet_left` | 7 |
| Steel Left Gauntlet | `steel_gauntlet_left` | 28 |

#### Right Gauntlet - 6 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Chitin Right Gauntlet | `chitin guantlet - right` | 9 |
| Imperial Steel Right Gauntlet | `imperial right gauntlet` | 33 |
| Iron Right Gauntlet | `iron_gauntlet_right` | 14 |
| Netch Leather Right Gauntlet | `netch_leather_gauntlet_right` | 7 |
| Nordic Fur Right Gauntlet | `fur_gauntlet_right` | 7 |
| Steel Right Gauntlet | `steel_gauntlet_right` | 28 |

#### Shield - 18 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bonemold Shield | `bonemold_shield` | 170 |
| Bonemold Tower Shield | `bonemold_towershield` | 250 |
| Chitin Shield | `chitin_shield` | 22 |
| Chitin Tower Shield | `chitin_towershield` | 32 |
| Dreugh Shield | `dreugh_shield` | 2550 |
| Dwemer Shield | `dwemer_shield` | 510 |
| Glass Shield | `glass_shield` | 13600 |
| Glass Tower Shield | `glass_towershield` | 20000 |
| Imperial Shield | `imperial shield` | 78 |
| Iron Shield | `iron_shield` | 34 |
| Iron Tower Shield | `iron_towershield` | 50 |
| Netch Leather Shield | `netch_leather_shield` | 17 |
| Netch Leather Tower Shield | `netch_leather_towershield` | 25 |
| Nordic Leather Shield | `nordic_leather_shield` | 25 |
| Nordic Trollbone Shield | `trollbone_shield` | 78 |
| Orcish Tower Shield | `orcish_towershield` | 2000 |
| Steel Shield | `steel_shield` | 68 |
| Steel Tower Shield | `steel_towershield` | 100 |

#### Left Bracer - 7 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bonemold Left Bracer | `bonemold_bracer_left` | 50 |
| Cloth Left Bracer | `cloth bracer left` | 3 |
| Dwemer Left Bracer | `dwemer_bracer_left` | 150 |
| Iron Left Bracer | `iron_bracer_left` | 10 |
| Left Glass Bracer | `glass_bracer_left` | 4000 |
| Left Leather Bracer | `left leather bracer` | 5 |
| Nordic Fur Left Bracer | `fur_bracer_left` | 5 |

#### Right Bracer - 7 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bonemold Right Bracer | `bonemold_bracer_right` | 50 |
| Cloth Right Bracer | `cloth bracer right` | 3 |
| Dwemer Right Bracer | `dwemer_bracer_right` | 150 |
| Iron Right Bracer | `iron_bracer_right` | 10 |
| Nordic Fur Right Bracer | `fur_bracer_right` | 5 |
| Right Glass Bracer | `glass_bracer_right` | 4000 |
| Right Leather Bracer | `right leather bracer` | 5 |

### Weapon - 88 Items

#### Short Blade - 14 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Chitin Dagger | `chitin dagger` | 6 |
| Chitin Shortsword | `chitin shortsword` | 13 |
| Dwarven Shortsword | `dwarven shortsword` | 300 |
| Imperial Shortsword | `imperial shortsword` | 30 |
| Iron Dagger | `iron dagger` | 10 |
| Iron Shortsword | `iron shortsword` | 20 |
| Iron Tanto | `iron tanto` | 14 |
| Iron Wakizashi | `iron wakizashi` | 24 |
| Silver Dagger | `silver dagger` | 40 |
| Silver Shortsword | `silver shortsword` | 80 |
| Steel Dagger | `steel dagger` | 20 |
| Steel Shortsword | `steel shortsword` | 40 |
| Steel Tanto | `steel tanto` | 28 |
| Steel Wakizashi | `steel wakizashi` | 48 |

#### Long Blade One Hand - 10 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Imperial Broadsword | `imperial broadsword` | 60 |
| Iron Broadsword | `iron broadsword` | 30 |
| Iron Longsword | `iron longsword` | 40 |
| Iron Saber | `iron saber` | 24 |
| Nordic Broadsword | `nordic broadsword` | 95 |
| Silver Longsword | `silver longsword` | 160 |
| Steel Broadsword | `steel broadsword` | 60 |
| Steel Katana | `steel katana` | 100 |
| Steel Longsword | `steel longsword` | 80 |
| Steel Saber | `steel saber` | 48 |

#### Long Blade Two Hand - 6 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dwarven Claymore | `dwarven claymore` | 1200 |
| Iron Claymore | `iron claymore` | 80 |
| Nordic Claymore | `nordic claymore` | 180 |
| Silver Claymore | `silver claymore` | 320 |
| Steel Claymore | `steel claymore` | 160 |
| Steel Dai-katana | `steel dai-katana` | 240 |

#### Blunt One Hand - 8 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Chitin Club | `chitin club` | 6 |
| Dreugh Club | `dreugh club` | 200 |
| Dwarven Mace | `dwarven mace` | 360 |
| Iron Club | `iron club` | 10 |
| Iron Mace | `iron mace` | 24 |
| Spiked Club | `spiked club` | 18 |
| Steel Club | `steel club` | 20 |
| Steel Mace | `steel mace` | 48 |

#### Blunt Two Hand Close - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dwarven Warhammer | `dwarven warhammer` | 600 |
| Iron Warhammer | `iron warhammer` | 40 |
| Steel Warhammer | `steel warhammer` | 80 |

#### Blunt Two Hand Wide - 4 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dreugh Staff | `dreugh staff` | 400 |
| Silver Staff | `silver staff` | 56 |
| Steel Staff | `steel staff` | 28 |
| Wooden Staff | `wooden staff` | 8 |

#### Spear - 9 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Chitin Spear | `chitin spear` | 13 |
| Dwarven Halberd | `dwarven halberd` | 600 |
| Dwarven Spear | `dwarven spear` | 300 |
| Iron Halberd | `iron halberd` | 40 |
| Iron Spear | `iron long spear` | 20 |
| Iron Spear | `iron spear` | 20 |
| Silver Spear | `silver spear` | 80 |
| Steel Halberd | `steel halberd` | 80 |
| Steel Spear | `steel spear` | 40 |

#### Axe One Hand - 6 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Chitin War Axe | `chitin war axe` | 19 |
| Dwarven War Axe | `dwarven war axe` | 450 |
| Iron War Axe | `iron war axe` | 30 |
| Silver War Axe | `silver war axe` | 120 |
| Steel Axe | `steel axe` | 60 |
| Steel War Axe | `steel war axe` | 60 |

#### Axe Two Hand - 5 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dwarven Battle Axe | `dwarven battle axe` | 750 |
| Iron Battle Axe | `iron battle axe` | 50 |
| Nordic Battle Axe | `nordic battle axe` | 60 |
| Orcish Battle Axe | `orcish battle axe` | 2000 |
| Steel Battle Axe | `steel battle axe` | 100 |

#### Bow - 5 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bonemold Long Bow | `bonemold long bow` | 250 |
| Chitin Short Bow | `chitin short bow` | 20 |
| Long Bow | `long bow` | 50 |
| Short Bow | `short bow` | 60 |
| Steel Longbow | `steel longbow` | 100 |

#### Crossbow - 2 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dwarven Crossbow | `dwarven crossbow` | 1200 |
| Steel Crossbow | `steel crossbow` | 160 |

#### Thrown - 5 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Chitin Throwing Star | `chitin throwing star` | 3 |
| Iron Throwing Knife | `iron throwing knife` | 3 |
| Silver Dart | `silver dart` | 6 |
| Silver Throwing Star | `silver throwing star` | 16 |
| Steel Dart | `steel dart` | 6 |

#### Arrow - 5 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bonemold Arrow | `bonemold arrow` | 2 |
| Chitin Arrow | `chitin arrow` | 1 |
| Iron Arrow | `iron arrow` | 1 |
| Silver Arrow | `silver arrow` | 3 |
| Steel Arrow | `steel arrow` | 2 |

#### Bolt - 6 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bonemold Bolt | `bonemold bolt` | 2 |
| Corkbulb Bolt | `corkbulb bolt` | 5 |
| Iron Bolt | `iron bolt` | 1 |
| Orcish Bolt | `orcish bolt` | 4 |
| Silver Bolt | `silver bolt` | 8 |
| Steel Bolt | `steel bolt` | 2 |

### Clothing - 141 Items

#### Pants - 22 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Pants | `common_pants_01` | 4 |
| Common Pants | `common_pants_01_a` | 4 |
| Common Pants | `common_pants_01_e` | 4 |
| Common Pants | `common_pants_01_u` | 4 |
| Common Pants | `common_pants_01_z` | 4 |
| Common Pants | `common_pants_02` | 4 |
| Common Pants | `common_pants_03` | 4 |
| Common Pants | `common_pants_03_b` | 4 |
| Common Pants | `common_pants_03_c` | 4 |
| Common Pants | `common_pants_04` | 4 |
| Common Pants | `common_pants_04_b` | 4 |
| Common Pants | `common_pants_05` | 4 |
| Expensive Pants | `expensive_pants_01` | 15 |
| Expensive Pants | `expensive_pants_01_a` | 15 |
| Expensive Pants | `expensive_pants_01_e` | 15 |
| Expensive Pants | `expensive_pants_01_u` | 15 |
| Expensive Pants | `expensive_pants_01_z` | 15 |
| Expensive Pants | `expensive_pants_02` | 15 |
| Expensive Pants | `expensive_pants_03` | 15 |
| Exquisite Pants | `exquisite_pants_01` | 120 |
| Extravagant Pants | `extravagant_pants_01` | 60 |
| Extravagant Pants | `extravagant_pants_02` | 60 |

#### Shoes - 11 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Shoes | `common_shoes_01` | 2 |
| Common Shoes | `common_shoes_02` | 2 |
| Common Shoes | `common_shoes_03` | 2 |
| Common Shoes | `common_shoes_04` | 2 |
| Common Shoes | `common_shoes_05` | 2 |
| Expensive Shoes | `expensive_shoes_01` | 10 |
| Expensive Shoes | `expensive_shoes_02` | 10 |
| Expensive Shoes | `expensive_shoes_03` | 10 |
| Exquisite Shoes | `exquisite_shoes_01` | 80 |
| Extravagant Shoes | `extravagant_shoes_01` | 40 |
| Extravagant Shoes | `extravagant_shoes_02` | 40 |

#### Shirt - 30 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Shirt | `common_shirt_01` | 4 |
| Common Shirt | `common_shirt_01_a` | 4 |
| Common Shirt | `common_shirt_01_e` | 4 |
| Common Shirt | `common_shirt_01_u` | 4 |
| Common Shirt | `common_shirt_01_z` | 4 |
| Common Shirt | `common_shirt_02` | 4 |
| Common Shirt | `common_shirt_02_h` | 4 |
| Common Shirt | `common_shirt_02_r` | 4 |
| Common Shirt | `common_shirt_02_t` | 4 |
| Common Shirt | `common_shirt_03` | 4 |
| Common Shirt | `common_shirt_03_b` | 4 |
| Common Shirt | `common_shirt_03_c` | 4 |
| Common Shirt | `common_shirt_04` | 4 |
| Common Shirt | `common_shirt_04_a` | 4 |
| Common Shirt | `common_shirt_04_b` | 4 |
| Common Shirt | `common_shirt_04_c` | 4 |
| Common Shirt | `common_shirt_05` | 4 |
| Expensive Shirt | `expensive_shirt_01` | 15 |
| Expensive Shirt | `expensive_shirt_01_a` | 15 |
| Expensive Shirt | `expensive_shirt_01_e` | 15 |
| Expensive Shirt | `expensive_shirt_01_u` | 15 |
| Expensive Shirt | `expensive_shirt_01_z` | 15 |
| Expensive Shirt | `expensive_shirt_02` | 15 |
| Expensive Shirt | `expensive_shirt_03` | 15 |
| Exquisite Shirt | `exquisite_shirt_01` | 120 |
| Extravagant Shirt | `extravagant_shirt_01` | 60 |
| Extravagant Shirt | `extravagant_shirt_01_h` | 60 |
| Extravagant Shirt | `extravagant_shirt_01_r` | 60 |
| Extravagant Shirt | `extravagant_shirt_01_t` | 60 |
| Extravagant Shirt | `extravagant_shirt_02` | 60 |

#### Belt - 11 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Belt | `common_belt_01` | 2 |
| Common Belt | `common_belt_02` | 2 |
| Common Belt | `common_belt_03` | 2 |
| Common Belt | `common_belt_04` | 2 |
| Common Belt | `common_belt_05` | 2 |
| Expensive Belt | `expensive_belt_01` | 10 |
| Expensive Belt | `expensive_belt_02` | 10 |
| Expensive Belt | `expensive_belt_03` | 10 |
| Exquisite Belt | `exquisite_belt_01` | 80 |
| Extravagant Belt | `extravagant_belt_01` | 40 |
| Extravagant Belt | `extravagant_belt_02` | 40 |

#### Robe - 26 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Robe | `common_robe_01` | 2 |
| Common Robe | `common_robe_02` | 2 |
| Common Robe | `common_robe_02_h` | 2 |
| Common Robe | `common_robe_02_r` | 2 |
| Common Robe | `common_robe_02_t` | 2 |
| Common Robe | `common_robe_03` | 2 |
| Common Robe | `common_robe_03_a` | 2 |
| Common Robe | `common_robe_03_b` | 2 |
| Common Robe | `common_robe_04` | 2 |
| Common Robe | `common_robe_05` | 2 |
| Common Robe | `common_robe_05_a` | 2 |
| Common Robe | `common_robe_05_b` | 2 |
| Common Robe | `common_robe_05_c` | 2 |
| Expensive Robe | `expensive_robe_01` | 10 |
| Expensive Robe | `expensive_robe_02` | 10 |
| Expensive Robe | `expensive_robe_02_a` | 10 |
| Expensive Robe | `expensive_robe_03` | 10 |
| Exquisite Robe | `exquisite_robe_01` | 80 |
| Extravagant Robe | `extravagant_robe_01` | 40 |
| Extravagant Robe | `extravagant_robe_01_a` | 40 |
| Extravagant Robe | `extravagant_robe_01_b` | 40 |
| Extravagant Robe | `extravagant_robe_01_c` | 40 |
| Extravagant Robe | `extravagant_robe_01_h` | 40 |
| Extravagant Robe | `extravagant_robe_01_r` | 40 |
| Extravagant Robe | `extravagant_robe_01_t` | 40 |
| Extravagant Robe | `extravagant_robe_02` | 40 |

#### Right Glove - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Right Glove | `common_glove_right_01` | 2 |
| Expensive Right Glove | `expensive_glove_right_01` | 10 |
| Extravagant Right Glove | `extravagant_glove_right_01` | 40 |

#### Left Glove - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Left Glove | `common_glove_left_01` | 2 |
| Expensive Left Glove | `expensive_glove_left_01` | 10 |
| Extravagant Left Glove | `extravagant_glove_left_01` | 40 |

#### Skirt - 12 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Skirt | `common_skirt_01` | 4 |
| Common Skirt | `common_skirt_02` | 4 |
| Common Skirt | `common_skirt_03` | 4 |
| Common Skirt | `common_skirt_04` | 4 |
| Common Skirt | `common_skirt_04_c` | 4 |
| Common Skirt | `common_skirt_05` | 4 |
| Expensive Shirt | `expensive_skirt_03` | 15 |
| Expensive Skirt | `expensive_skirt_01` | 15 |
| Expensive Skirt | `expensive_skirt_02` | 15 |
| Exquisite Skirt | `exquisite_skirt_01` | 120 |
| Extravagant Skirt | `extravagant_skirt_01` | 60 |
| Extravagant Skirt | `extravagant_skirt_02` | 60 |

#### Ring - 12 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Ring | `common_ring_01` | 2 |
| Common Ring | `common_ring_02` | 2 |
| Common Ring | `common_ring_03` | 2 |
| Common Ring | `common_ring_04` | 2 |
| Common Ring | `common_ring_05` | 2 |
| Expensive Ring | `expensive_ring_01` | 30 |
| Expensive Ring | `expensive_ring_02` | 30 |
| Expensive Ring | `expensive_ring_03` | 30 |
| Exquisite Ring | `exquisite_ring_01` | 240 |
| Exquisite Ring | `exquisite_ring_02` | 240 |
| Extravagant Ring | `extravagant_ring_01` | 120 |
| Extravagant Ring | `extravagant_ring_02` | 120 |

#### Amulet - 11 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Amulet | `common_amulet_01` | 2 |
| Common Amulet | `common_amulet_02` | 2 |
| Common Amulet | `common_amulet_03` | 2 |
| Common Amulet | `common_amulet_04` | 2 |
| Common Amulet | `common_amulet_05` | 2 |
| Expensive Amulet | `expensive_amulet_01` | 30 |
| Expensive Amulet | `expensive_amulet_02` | 30 |
| Expensive Amulet | `expensive_amulet_03` | 30 |
| Exquisite Amulet | `exquisite_amulet_01` | 240 |
| Extravagant Ruby Amulet | `extravagant_amulet_02` | 120 |
| Extravagant Sapphire Amulet | `extravagant_amulet_01` | 120 |

## Tribunal - 26 Items

Source: `Tribunal.esm`.

### Armor - 8 Items

#### Helmet - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dark Brotherhood Helm | `darkbrotherhood helm` | 200 |

#### Cuirass - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dark Brotherhood Cuirass | `darkbrotherhood cuirass` | 1000 |

#### Left Pauldron - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dark Brotherhood Left Pauldron | `darkbrotherhood pauldron_l` | 500 |

#### Right Pauldron - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dark Brotherhood Right Pauldron | `darkbrotherhood pauldron_r` | 500 |

#### Greaves - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dark Brotherhood Greaves | `darkbrotherhood greaves` | 100 |

#### Boots - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dark Brotherhood Boots | `darkbrotherhood boots` | 500 |

#### Left Gauntlet - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dark Brotherhood Left Gauntlet | `darkbrotherhood gauntlet_l` | 200 |

#### Right Gauntlet - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dark Brotherhood Right Gauntlet | `darkbrotherhood gauntlet_r` | 200 |

### Weapon - 6 Items

#### Short Blade - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Goblin Sword | `goblin_sword` | 100 |

#### Long Blade One Hand - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Ebony Scimitar | `ebony scimitar` | 15000 |

#### Blunt One Hand - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Goblin Club | `goblin_club` | 3000 |

#### Thrown - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dwarven Dart | `centurion_projectile_dart` | 10 |
| Fine Spring Dart | `fine spring dart` | 6 |
| Spring Dart | `spring dart` | 6 |

### Clothing - 12 Items

#### Pants - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Pants | `common_pants_06` | 4 |
| Common Pants | `common_pants_07` | 4 |
| Expensive Pants | `expensive_pants_mournhold` | 15 |

#### Shoes - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Shoes | `common_shoes_06` | 2 |
| Common Shoes | `common_shoes_07` | 2 |
| Expensive Shoes | `expensive_shoes_mournhold` | 10 |

#### Shirt - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Shirt | `common_shirt_06` | 4 |
| Common Shirt | `common_shirt_07` | 4 |
| Expensive Shirt | `expensive_shirt_mournhold` | 1 |

#### Skirt - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Skirt | `common_skirt_06` | 4 |
| Common Skirt | `common_skirt_07` | 4 |
| Expensive Skirt | `expensive_skirt_mournhold` | 15 |

## Bloodmoon - 66 Items

Source: `Bloodmoon.esm`.

### Armor - 28 Items

#### Helmet - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bear Helmet | `bm bear helmet` | 40 |
| Nordic Mail Helmet | `bm_nordicmail_helmet` | 1000 |
| Wolf Helmet | `bm wolf helmet` | 40 |

#### Cuirass - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bear Cuirass | `bm bear cuirass` | 150 |
| Nordic Mail Cuirass | `bm_nordicmail_cuirass` | 5000 |
| Wolf Cuirass | `bm wolf cuirass` | 150 |

#### Left Pauldron - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bear Left Pauldron | `bm bear left pauldron` | 60 |
| Nordic Mail Left Pauldron | `bm_nordicmail_pauldronl` | 1000 |
| Wolf Left Pauldron | `bm wolf left pauldron` | 60 |

#### Right Pauldron - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bear Right Pauldron | `bm bear right pauldron` | 60 |
| Nordic Mail Right Pauldron | `bm_nordicmail_pauldronr` | 1000 |
| Wolf Right Pauldron | `bm wolf right pauldron` | 60 |

#### Greaves - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bear Greaves | `bm bear greaves` | 120 |
| Nordic Mail Greaves | `bm_nordicmail_greaves` | 2000 |
| Wolf Greaves | `bm wolf greaves` | 120 |

#### Boots - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bear Boots | `bm bear boots` | 50 |
| Nordic Mail Boots | `bm_nordicmail_boots` | 5000 |
| Wolf Boots | `bm wolf boots` | 50 |

#### Left Gauntlet - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bear Left Gauntlet | `bm bear left gauntlet` | 40 |
| Nordic Mail Left Gauntlet | `bm_nordicmail_gauntletl` | 1000 |
| Wolf Left Gauntlet | `bm wolf left gauntlet` | 40 |

#### Right Gauntlet - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bear Right Gauntlet | `bm bear right gauntlet` | 40 |
| Nordic Mail Right Gauntlet | `bm_nordicmail_gauntletr` | 1000 |
| Wolf Right Gauntlet | `bm wolf right gauntlet` | 40 |

#### Shield - 4 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bear Shield | `bm bear shield` | 100 |
| Nordic Mail Shield | `bm_nordicmail_shield` | 1000 |
| Riekling Shield | `bm_ice minion_shield1` | 50 |
| Wolf Shield | `bm wolf shield` | 100 |

### Weapon - 16 Items

#### Short Blade - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Nordic Silver Dagger | `bm nordic silver dagger` | 1000 |
| Nordic Silver Shortsword | `bm nordic silver shortsword` | 1000 |
| Riekling Lance | `bm riekling lance` | 100 |

#### Long Blade One Hand - 4 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Huntsman Longsword | `bm huntsman longsword` | 500 |
| Nordic Silver Longsword | `bm nordic silver longsword` | 1000 |
| Riekling Blade | `bm riekling sword` | 350 |
| Rusted Riekling Blade | `bm riekling sword_rusted` | 150 |

#### Long Blade Two Hand - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Nordic Silver Claymore | `bm nordic silver claymore` | 1000 |

#### Blunt One Hand - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Nordic Silver Mace | `bm nordic silver mace` | 1000 |

#### Spear - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Huntsman Spear | `bm huntsman spear` | 500 |

#### Axe One Hand - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Huntsman Axe | `bm huntsman axe` | 100 |
| Huntsman War Axe | `bm huntsman war axe` | 125 |
| Nordic Silver Axe | `bm nordic silver axe` | 1000 |

#### Axe Two Hand - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Nordic Silver Battleaxe | `bm nordic silver battleaxe` | 1000 |

#### Crossbow - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Huntsman Crossbow | `bm huntsman crossbow` | 500 |

#### Bolt - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Huntsman Bolt | `bm huntsmanbolt` | 5 |

### Clothing - 22 Items

#### Pants - 4 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Pants | `bm_nordic01_pants` | 4 |
| Common Pants | `bm_nordic02_pants` | 4 |
| Common Pants | `bm_wool01_pants` | 4 |
| Common Pants | `bm_wool02_pants` | 4 |

#### Shoes - 4 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Shoes | `bm_nordic01_shoes` | 2 |
| Common Shoes | `bm_nordic02_shoes` | 2 |
| Common Shoes | `bm_wool01_shoes` | 2 |
| Common Shoes | `bm_wool02_shoes` | 2 |

#### Shirt - 4 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Shirt | `bm_nordic01_shirt` | 4 |
| Common Shirt | `bm_nordic02_shirt` | 4 |
| Common Shirt | `bm_wool01_shirt` | 4 |
| Common Shirt | `bm_wool02_shirt` | 4 |

#### Robe - 2 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Robe | `bm_nordic01_robe` | 20 |
| Common Robe | `bm_wool01_robe` | 20 |

#### Right Glove - 4 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Right Glove | `bm_nordic01_glover` | 4 |
| Right Glove | `bm_nordic02_glover` | 4 |
| Right Glove | `bm_wool01_glover` | 4 |
| Right Glove | `bm_wool02_glover` | 4 |

#### Left Glove - 4 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Left Glove | `bm_nordic01_glovel` | 4 |
| Left Glove | `bm_nordic02_glovel` | 4 |
| Left Glove | `bm_wool01_glovel` | 4 |
| Left Glove | `bm_wool02_glovel` | 4 |

## OAAB Data - 307 Items

Source: `OAAB_Data.esm`.

### Armor - 123 Items

#### Helmet - 66 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Blue Bug Helm | `ab_a_bugbluehelm` | 30 |
| Bonemold Open Helm | `ab_a_bonemhelmopen` | 150 |
| Chitin Open Helm | `ab_a_chitinhelmopen` | 19 |
| Chitin Scout Helm | `ab_a_chitinscouthelm` | 50 |
| Cloth Neck Wrap | `ab_a_clothhelm1` | 8 |
| Cloth Neck Wrap | `ab_a_clothhelm2` | 8 |
| Cloth Neck Wrap | `ab_a_clothhelm3` | 8 |
| Common Hood | `ab_c_commonhood01` | 1 |
| Common Hood | `ab_c_commonhood02` | 1 |
| Common Hood | `ab_c_commonhood02h` | 1 |
| Common Hood | `ab_c_commonhood02hh` | 1 |
| Common Hood | `ab_c_commonhood02r` | 1 |
| Common Hood | `ab_c_commonhood02rr` | 1 |
| Common Hood | `ab_c_commonhood02t` | 1 |
| Common Hood | `ab_c_commonhood02tt` | 1 |
| Common Hood | `ab_c_commonhood03` | 1 |
| Common Hood | `ab_c_commonhood03a` | 1 |
| Common Hood | `ab_c_commonhood03b` | 1 |
| Common Hood | `ab_c_commonhood04` | 1 |
| Common Hood | `ab_c_commonhood05` | 1 |
| Common Hood | `ab_c_commonhood05a` | 1 |
| Common Hood | `ab_c_commonhood05b` | 1 |
| Common Hood | `ab_c_commonhood05c` | 1 |
| Common Hood | `ab_c_commonhoodblack` | 1 |
| Daedric Face of Revelation | `ab_a_daeazurahelm` | 13500 |
| Dreugh Helm | `ab_a_dreughhelmclose` | 2400 |
| Dunmer Iron Helmet | `ab_a_irondehelm` | 35 |
| Dust Merchant Helmet | `ab_a_dusthelm` | 75 |
| Dwemer Hat | `ab_c_dwrvhat` | 600 |
| Ebony Open Helm | `ab_a_ebonyhelmopen` | 15000 |
| Expensive Hood | `ab_c_expensivehood01` | 5 |
| Expensive Hood | `ab_c_expensivehood02` | 5 |
| Expensive Hood | `ab_c_expensivehood02a` | 5 |
| Expensive Hood | `ab_c_expensivehood03` | 5 |
| Exquisite Hood | `ab_c_exquisitehood01` | 40 |
| Extravagant Hood | `ab_c_extravaganthood01` | 20 |
| Extravagant Hood | `ab_c_extravaganthood01a` | 20 |
| Extravagant Hood | `ab_c_extravaganthood01b` | 20 |
| Extravagant Hood | `ab_c_extravaganthood01c` | 20 |
| Extravagant Hood | `ab_c_extravaganthood01h` | 20 |
| Extravagant Hood | `ab_c_extravaganthood01r` | 20 |
| Extravagant Hood | `ab_c_extravaganthood01t` | 20 |
| Extravagant Hood | `ab_c_extravaganthood02` | 20 |
| Face of Comforting Tendrils  | `ab_a_daesheoghelm` | 14500 |
| Face of the Forbidden Tickle | `ab_a_daemolaghelm` | 14000 |
| Face of the Husband of Fire | `ab_a_daedagonhelm` | 14000 |
| Glass Helm | `ab_a_glasshelmclose` | 12000 |
| Green Bug Helm | `ab_a_buggreenhelm` | 30 |
| Imperial Battlemage Hood | `ab_a_impbmhelm` | 1500 |
| Khestis Chitin Helmet | `ab_a_chitinhlahelm01` | 30 |
| Leather Hat | `ab_a_leatherhat` | 11 |
| Light Steel Helmet | `ab_a_steelhelm` | 300 |
| Mir-Moljuhn Chitin Helmet | `ab_a_chitintelhelm01` | 22 |
| Morag Tong Ar-Hadaz Mask | `ab_a_moragtonghelm01` | 50 |
| Morag Tong Dun-Saro Hood | `ab_a_moragtonghelm02` | 50 |
| Morag Tong Irovonei Helm | `ab_a_moragtonghelm04` | 50 |
| Morag Tong Mar-Roth Mask | `ab_a_moragtonghelm03` | 55 |
| Native Tongman Iron Helm | `ab_a_irondehelmtong` | 75 |
| Netchiman's Cap | `ab_a_netchimancap` | 20 |
| Orcish Open Helm | `ab_a_orchelmopen` | 1200 |
| Sal-Amur Bonemold Helm | `ab_a_bonemlighthelm` | 90 |
| Sho-Hadad Chitin Helmet | `ab_a_chitinredhelm01` | 22 |
| Steel Helm | `ab_a_steelhelmopen` | 60 |
| Telvanni Cephalopod Helm | `ab_a_cephhelmopen` | 50 |
| Wicker Hat | `ab_a_wickerhelm` | 10 |
| Wicker Hat | `ab_a_wickerhelm02` | 10 |

#### Cuirass - 7 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Blue Bug Cuirass | `ab_a_bugbluecuirass` | 60 |
| Dunmer Iron Cuirass | `ab_a_irondecuirass` | 85 |
| Dust Merchant Coat | `ab_a_dustchest` | 225 |
| Green Bug Cuirass | `ab_a_buggreencuirass` | 60 |
| Imperial Battlemage Cuirass | `ab_a_impbmcuirass` | 2500 |
| Light Steel Cuirass | `ab_a_steelcuirass` | 700 |
| Sal-Amur Bonemold Cuirass | `ab_a_bonemlightcuirass` | 240 |

#### Left Pauldron - 10 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Blue Bug Left Pauldron | `ab_a_bugbluepldleft` | 25 |
| Boiled Netch Leather Pauldron L | `ab_a_netchboilpldleft` | 15 |
| Cephalopod Left Pauldron | `ab_a_cephpauldronleft` | 30 |
| Dreugh Pauldron Left | `ab_a_dreughpldleft` | 1800 |
| Dunmer Iron Left Pauldron | `ab_a_irondepldleft` | 30 |
| Dust Merchant Pauldron L. | `ab_a_dustpldrleft` | 50 |
| Green Bug Left Pauldron | `ab_a_buggreenpldleft` | 25 |
| Imperial Battlemage Pauldron L | `ab_a_impbmpldleft` | 1200 |
| Light Steel Pauldron L. | `ab_a_steelpldrleft` | 250 |
| Sal-Amur Bonemold Pauldron L | `ab_a_bonemlightpaull` | 80 |

#### Right Pauldron - 11 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Basket | `ab_a_backbasket` | 1 |
| Blue Bug Right Pauldron | `ab_a_bugbluepldright` | 25 |
| Boiled Netch Leather Pauldron R | `ab_a_netchboilpldright` | 15 |
| Cephalopod Right Pauldron | `ab_a_cephpauldronright` | 30 |
| Dreugh Pauldron Right | `ab_a_dreughpldright` | 1800 |
| Dunmer Iron Right Pauldron | `ab_a_irondepldright` | 30 |
| Dust Merchant Pauldron R. | `ab_a_dustpldrright` | 50 |
| Green Bug Right Pauldron | `ab_a_buggreenpldright` | 25 |
| Imperial Battlemage Pauldron R | `ab_a_impbmpldright` | 1200 |
| Light Steel Pauldron R. | `ab_a_steelpldrright` | 250 |
| Sal-Amur Bonemold Pauldron R | `ab_a_bonemlightpaulr` | 80 |

#### Greaves - 7 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Blue Bug Greaves | `ab_a_bugbluegreaves` | 50 |
| Dreugh Greaves | `ab_a_dreughgreaves` | 3300 |
| Dust Merchant Greaves | `ab_a_dustgreaves` | 200 |
| Green Bug Greaves | `ab_a_buggreengreaves` | 50 |
| Imperial Battlemage Greaves | `ab_a_impbmgreaves` | 2300 |
| Light Steel Greaves | `ab_a_steelgreaves` | 400 |
| Sal-Amur Bonemold Greaves | `ab_a_bonemlightgreaves` | 160 |

#### Boots - 8 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Blue Bug Boots | `ab_a_bugblueboots` | 20 |
| Dreugh Boots | `ab_a_dreughboots` | 1500 |
| Dunmer Iron Boots | `ab_a_irondeboots` | 25 |
| Dust Merchant Boots | `ab_a_dustboots` | 180 |
| Green Bug Boots | `ab_a_buggreenboots` | 20 |
| Imperial Battlemage Boots | `ab_a_impbmboots` | 1700 |
| Light Steel Boots | `ab_a_steelboots` | 300 |
| Sal-Amur Bonemold Boots | `ab_a_bonemlightboots` | 75 |

#### Left Gauntlet - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Blue Bug Gauntlet - Left | `ab_a_bugbluegntleft` | 20 |
| Green Bug Gauntlet - Left | `ab_a_buggreengntleft` | 20 |
| Light Steel Gauntlet L. | `ab_a_steelgntlleft` | 150 |

#### Right Gauntlet - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Blue Bug Gauntlet - Right | `ab_a_bugbluegntright` | 20 |
| Green Bug Gauntlet - Right | `ab_a_buggreengntright` | 20 |
| Light Steel Gauntlet R. | `ab_a_steelgntlright` | 150 |

#### Shield - 2 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Blue Bug Shield | `ab_a_bugblueshield` | 30 |
| Green Bug Shield | `ab_a_buggreenshield` | 30 |

#### Left Bracer - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dreugh Bracer Left | `ab_a_dreughbracerl` | 750 |
| Dust Merchant Bracer L. | `ab_a_dustbracerleft` | 30 |
| Sal-Amur Bonemold Bracer L | `ab_a_bonemlightbracerl` | 25 |

#### Right Bracer - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dreugh Bracer Right | `ab_a_dreughbracerr` | 750 |
| Dust Merchant Bracer R. | `ab_a_dustbracerright` | 30 |
| Sal-Amur Bonemold Bracer R | `ab_a_bonemlightbracerr` | 25 |

### Weapon - 164 Items

#### Short Blade - 28 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Ashlander Glass Dagger | `ab_w_ashlglassdagger` | 160 |
| Ashlander Glass Shortsword | `ab_w_ashlglassshortsword` | 200 |
| Boning Knife | `ab_w_cookknifebone` | 3 |
| Bread Knife | `ab_w_cookknifebread` | 5 |
| Broken Bottle | `ab_w_bottlebroken` | 1 |
| Chitin Sickle | `ab_w_chitinsickle` | 16 |
| Cook's Knife | `ab_w_cookknifechef` | 5 |
| Dreugh Dagger | `ab_w_dreughdagger` | 300 |
| Dreugh Shortsword | `ab_w_dreughshortsword` | 500 |
| Dwarven Dagger | `ab_w_dwrvdagger` | 240 |
| Dwarven Shortsword | `ab_w_dwrvspectresword` | 300 |
| Ebony Dagger | `ab_w_ebonydagger` | 5000 |
| Ebony Tanto | `ab_w_ebonytanto` | 10000 |
| Ebony Wakizashi | `ab_w_ebonywakizashi` | 24000 |
| Farmer's Hand Scythe | `ab_w_toolhandscythe01` | 18 |
| Farmer's Sickle | `ab_w_toolhandscythe00` | 9 |
| Flint Knife | `ab_w_flintknife` | 5 |
| Glass Tanto | `ab_w_glasstanto` | 5000 |
| Glass Wakizashi | `ab_w_glasswakizashi` | 17000 |
| Imperial Tanto | `ab_w_imptanto` | 50 |
| Imperial Wakizashi | `ab_w_impwakizashi` | 68 |
| Knife | `ab_w_cookknifedinner` | 1 |
| Marking Knife | `ab_w_markingknife` | 4 |
| Silver Tanto | `ab_w_silvertanto` | 56 |
| Silver Wakizashi | `ab_w_silverwakizashi` | 96 |
| Stalhrim Shortsword | `ab_w_stalhrimshortsword` | 35000 |
| Steel Short Saber | `ab_w_steelshortsaber` | 430 |
| Wooden Stake | `ab_w_woodstake` | 2 |

#### Long Blade One Hand - 19 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Adamantium Rapier | `ab_w_adamrapier` | 7000 |
| Ashlander Glass Longsword | `ab_w_ashlglasslongsword` | 400 |
| Bonesaw | `ab_w_bonesaw` | 20 |
| Chitin Longsword | `ab_w_chitinlongsword` | 23 |
| Corkbulk Machete | `ab_w_machete` | 35 |
| Daedric Rapier | `ab_w_daedricrapier` | 50000 |
| Dreugh Longsword | `ab_w_dreughlongsword` | 1100 |
| Dwarven Longsword | `ab_w_dwrvlongsword` | 1000 |
| Ebony Katana | `ab_w_ebonykatana` | 25000 |
| Glass Katana | `ab_w_glasskatana` | 18000 |
| Glass Rapier | `ab_w_glassrapier` | 17000 |
| Glass Saber | `ab_w_glasssaber` | 14000 |
| Imperial Katana | `ab_w_impkatana` | 160 |
| Imperial Longsword | `ab_w_implongsword` | 80 |
| Iron Rapier | `ab_w_ironrapier` | 26 |
| Silver Katana | `ab_w_silverkatana` | 200 |
| Silver Rapier | `ab_w_silverrapier` | 175 |
| Steel Rapier | `ab_w_steelrapier` | 26 |
| Wooden Sword | `ab_w_wood sword` | 8 |

#### Long Blade Two Hand - 7 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dreugh Claymore | `ab_w_dreughclaymore` | 1800 |
| Ebony Claymore | `ab_w_ebonyclaymore` | 41000 |
| Ebony Dai-katana | `ab_w_ebonydaikatana` | 60000 |
| Glass Dai-Katana | `ab_w_glassdkatana` | 35000 |
| Golden Saint Claymore | `ab_w_goldstclaymore` | 2100 |
| Imperial Dai-katana | `ab_w_impdaikatana` | 550 |
| Silver Dai-katana | `ab_w_silverdaikatana` | 480 |

#### Blunt One Hand - 20 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Ashlander Glass Club | `ab_w_ashlglassclub` | 120 |
| Blacksmith's Hammer | `ab_w_toolsmithhammer` | 10 |
| Bone Scepter | `ab_w_bonescepter` | 8 |
| Brush | `ab_w_toolfireplacebrush` | 20 |
| Chitin Mace | `ab_w_chitinmace` | 15 |
| Daedric Scepter | `ab_w_daedricscepter` | 8000 |
| Dreugh Mace | `ab_w_dreughmace` | 1000 |
| Dwarven Hammer | `ab_w_dwrvspectrehammer` | 360 |
| Dwarven Scepter | `ab_w_dwrvscepter` | 300 |
| Ebony Scepter | `ab_w_ebonyscepter` | 8000 |
| Glass Mace | `ab_w_glassmace` | 8000 |
| Glass Scepter | `ab_w_glassscepter` | 2600 |
| Hammer | `ab_w_toolhammer` | 6 |
| Imperial Club | `ab_w_impclub` | 20 |
| Imperial Mace | `ab_w_impmace` | 48 |
| Nordic Mace | `ab_w_nordicmace` | 80 |
| Orcish Mace | `ab_w_orcishmace` | 4500 |
| Shovel | `ab_w_toolfireplaceshovel` | 20 |
| Silver Scepter | `ab_w_silverscepter` | 50 |
| Wooden Club | `ab_w_woodclub` | 8 |

#### Blunt Two Hand Close - 5 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Chitin Greatmace | `ab_w_chitingreatmace` | 23 |
| Dreugh Greatmace | `ab_w_dreughgreatmace` | 1000 |
| Ebony warhammer | `ab_w_ebonywarhammer` | 17000 |
| Glass Warhammer | `ab_w_glasswarhammer` | 9000 |
| Silver Warhammer | `ab_w_silverwarhammer` | 160 |

#### Blunt Two Hand Wide - 4 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Ashlander Glass Staff | `ab_w_ashlglassstaff` | 290 |
| Fishing Net | `ab_w_toolfishingnet` | 12 |
| Imperial Staff | `ab_w_impstaff` | 40 |
| Resin Staff | `ab_w_resinstaff` | 1000 |

#### Spear - 24 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Ashlander Glass Spear | `ab_w_ashlglassspear` | 340 |
| Chitin Halberd | `ab_w_chitinhalberd` | 19 |
| Chitin Longspear | `ab_w_chitinlongspear` | 21 |
| Daedric Halberd | `ab_w_daedrichalberd` | 22000 |
| Daedric Longspear | `ab_w_daelongpear` | 25000 |
| Dreugh Halberd | `ab_w_dreughhalberd` | 900 |
| Dreugh Spear | `ab_w_dreughspear` | 650 |
| Dwarven Longspear | `ab_w_dwrvlongspear` | 400 |
| Ebony Glaive | `ab_w_ebonyglaive` | 10000 |
| Ebony Halberd | `ab_w_ebonyhalberd` | 10000 |
| Egg Miner's Hook | `ab_w_eggminerhook` | 18 |
| Farmer's Scythe | `ab_w_toolscythe` | 25 |
| Flint Spear | `ab_w_flintspear` | 10 |
| Glass Spear | `ab_w_glassspear` | 12000 |
| Hoe | `ab_w_toolhoe` | 8 |
| Imperial Spear | `ab_w_impspear` | 160 |
| Nordic Long Axe | `ab_w_nordiclongaxe` | 80 |
| Nordic Silver Spear | `ab_w_nordicsilverspear` | 1000 |
| Pitchfork | `ab_w_toolpitchfork` | 9 |
| Rake | `ab_w_toolrake` | 6 |
| Shovel | `ab_w_toolshovel` | 8 |
| Silver Halberd | `ab_w_silverhalberd` | 130 |
| Sixth House Spear | `ab_w_sixthspear` | 940 |
| Stalhrim Spear | `ab_w_stalhrimspear` | 35000 |

#### Axe One Hand - 8 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Ashlander Glass War Axe | `ab_w_ashlglasswaraxe` | 340 |
| Cleaver | `ab_w_cookknifecleave` | 5 |
| Climbing Pick | `ab_w_toolclimbingpick` | 7 |
| Dreugh War Axe | `ab_w_dreughwaraxe` | 600 |
| Dwemer Crowbar | `ab_w_dwrvtoolcrowbar` | 120 |
| Imperial War Axe | `ab_w_impwaraxe` | 50 |
| Poker | `ab_w_toolfireplacepoker` | 20 |
| Wood Axe | `ab_w_toolwoodaxe` | 20 |

#### Axe Two Hand - 7 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dreugh Battle Axe | `ab_w_dreughbattleaxe` | 740 |
| Ebony Miner's Pick | `ab_w_toolebonypick` | 800 |
| Entrenching tool | `ab_w_impetool` | 10 |
| Flint Pickaxe | `ab_w_flintpickaxe` | 8 |
| Flint Wood Axe | `ab_w_flintaxe` | 5 |
| Glass Battle Axe | `ab_w_glassbattleaxe` | 13000 |
| Stalhrim Battle Axe | `ab_w_stalhrimbattleaxe` | 80000 |

#### Bow - 13 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Chitin Longbow | `ab_w_chitinlongbow` | 30 |
| Daedric Shortbow | `ab_w_daedricshortbow` | 45000 |
| Dreugh Shortbow | `ab_w_dreughshortbow` | 750 |
| Ebony Longbow | `ab_w_ebonybow` | 3000 |
| Glass Shortbow | `ab_w_glassshortbow` | 9000 |
| Huntsman Longbow | `ab_w_huntsbow` | 350 |
| Imperial Shortbow | `ab_w_impbow` | 140 |
| Iron Longbow | `ab_w_ironlongbow` | 60 |
| Nordic Silver Longbow | `ab_w_nordicsilverbow` | 2500 |
| Silver Longbow | `ab_w_silverlongbow` | 200 |
| Silver Shortbow | `ab_w_silvershortbow` | 120 |
| Stalhrim Longbow | `ab_w_stalhrimbow` | 60000 |
| Wooden Bow | `ab_w_woodbow` | 20 |

#### Crossbow - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Dwarven Arbalest | `ab_w_dwrvarbalest` | 2500 |
| Reinforced Crossbow | `ab_w_recrossbow` | 950 |
| Wooden Crossbow | `ab_w_woodcrossbow` | 70 |

#### Thrown - 10 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Chitin Dart | `ab_w_chitindart` | 1 |
| Daedric Throwing Knife | `ab_w_daedricknife` | 2500 |
| Daedric Throwing Star | `ab_w_daedricstar` | 4000 |
| Dwarven Throwing Knife | `ab_w_dwrvknife` | 15 |
| Dwarven Throwing Star | `ab_w_dwrvstar` | 10 |
| Ebony Throwing Knife | `ab_w_ebonyknife` | 35 |
| Glass Dart | `ab_w_glassdart` | 23 |
| Imperial Dart | `ab_w_impdart` | 6 |
| Silver Throwing Knife | `ab_w_silverknife` | 7 |
| Sixth House Throwing Knife | `ab_w_sixthknife` | 50 |

#### Arrow - 12 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Ashlander Bone Arrow | `ab_w_ashlbonearrow` | 2 |
| Ashlander Ebony Arrow | `ab_w_ashlebonyarrow` | 5 |
| Ashlander Glass Arrow | `ab_w_ashlglassarrow` | 4 |
| Bone Arrow | `ab_w_bonearrow` | 2 |
| Dreugh Arrow | `ab_w_dreugharrow` | 3 |
| Flint Arrow | `ab_w_flintarrow` | 1 |
| Goblin Arrow | `ab_w_goblinarrow` | 12 |
| Huntsman Arrow | `ab_w_huntsarrow` | 2 |
| Imperial Arrow | `ab_w_imparrow` | 2 |
| Orcish Arrow | `ab_w_orcisharrow` | 4 |
| Stalhrim Arrow | `ab_w_stalhrimarrow` | 17 |
| Wooden Arrow | `ab_w_woodarrow` | 1 |

#### Bolt - 4 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Bone Bolt | `ab_w_bonebolt` | 2 |
| Dwarven Bolt | `ab_w_dwrvbolt` | 3 |
| Ebony Bolt | `ab_w_ebonybolt` | 24 |
| Wooden Bolt | `ab_w_woodbolt` | 1 |

### Clothing - 20 Items

#### Shirt - 2 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Shirt | `ab_c_commonshirt02b` | 4 |
| Common Shirt | `ab_c_commonshirt05l` | 4 |

#### Belt - 3 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Belt | `ab_c_commonbelt01` | 2 |
| Common Belt | `ab_c_commonbelt02` | 2 |
| Expensive Belt | `ab_c_expensivebelt01` | 10 |

#### Robe - 1 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Robe | `ab_c_commonrobeblack` | 2 |

#### Ring - 8 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Ring | `ab_c_commonring01` | 2 |
| Common Ring | `ab_c_commonring02` | 2 |
| Expensive Ring | `ab_c_expensivering01` | 30 |
| Expensive Ring | `ab_c_expensivering02` | 30 |
| Expensive Ring | `ab_c_expensivering03` | 30 |
| Exquisite Ring | `ab_c_exquisitering01` | 240 |
| Extravagant Ring | `ab_c_extravagantring01` | 120 |
| Extravagant Ring | `ab_c_extravagantring02` | 120 |

#### Amulet - 6 Items

| Item Name | Record ID | Gold |
| --- | --- | ---: |
| Common Amulet | `ab_c_commonamulet01` | 2 |
| Common Amulet | `ab_c_commonamulet02` | 2 |
| Dwemer Amulet | `ab_c_dwemeramuletclock` | 60 |
| Expensive Amulet | `ab_c_expensiveamulet01` | 30 |
| Exquisite Amulet | `ab_c_exquisiteamulet01` | 240 |
| Extravagant Glass Amulet | `ab_c_extravagantamulet01` | 120 |

