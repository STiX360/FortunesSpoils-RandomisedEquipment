"""Export static source equipment pools; never scan installed mod overrides."""

import argparse
import json
import pathlib
import re
import struct

from audit_helmets import decode, subrecords


SLOTS = {
    "armor": ("helmet", "cuirass", "left_pauldron", "right_pauldron", "greaves",
              "boots", "left_gauntlet", "right_gauntlet", "shield", "left_bracer", "right_bracer"),
    "weapon": ("short_blade", "long_blade_one_hand", "long_blade_two_hand", "blunt_one_hand",
               "blunt_two_hand_close", "blunt_two_hand_wide", "spear", "axe_one_hand",
               "axe_two_hand", "bow", "crossbow", "thrown", "arrow", "bolt"),
    "clothing": ("pants", "shoes", "shirt", "belt", "robe", "right_glove", "left_glove",
                 "skirt", "ring", "amulet"),
}
CLOTHING_ID = re.compile(
    r"^(common|expensive|extravagant|exquisite)_"
    r"(pants|shoes|shirt|belt|robe|glove_right|glove_left|skirt|ring|amulet)_\d{2}(?:_[a-z])?$"
)
STANDARD_GLASS_ARMOR_IDS = (
    'glass_helm', 'glass_cuirass', 'glass_greaves', 'glass_boots',
    'glass_pauldron_left', 'glass_pauldron_right',
    'glass_bracer_left', 'glass_bracer_right', 'glass_shield', 'glass_towershield',
)
BLOODMOON_ARMOR_IDS = (
    "bm_nordicmail_boots", "bm_nordicmail_cuirass", "bm_nordicmail_greaves",
    "bm_nordicmail_helmet", "bm_nordicmail_gauntletl", "bm_nordicmail_gauntletr",
    "bm_nordicmail_pauldronl", "bm_nordicmail_pauldronr", "bm_nordicmail_shield",
    "bm wolf boots", "bm wolf cuirass", "bm wolf greaves", "bm wolf helmet",
    "bm wolf left gauntlet", "bm wolf right gauntlet",
    "bm wolf left pauldron", "bm wolf right pauldron", "bm wolf shield",
    "bm bear boots", "bm bear cuirass", "bm bear greaves", "bm bear helmet",
    "bm bear left gauntlet", "bm bear right gauntlet",
    "bm bear left pauldron", "bm bear right pauldron", "bm bear shield",
    "bm_ice minion_shield1",
)
BLOODMOON_WEAPON_IDS = (
    "bm huntsman axe", "bm huntsman war axe", "bm huntsmanbolt", "bm huntsman crossbow",
    "bm huntsman longsword", "bm huntsman spear", "bm nordic silver axe",
    "bm nordic silver battleaxe", "bm nordic silver mace", "bm nordic silver longsword",
    "bm nordic silver claymore", "bm nordic silver dagger", "bm nordic silver shortsword",
    "bm riekling sword", "bm riekling sword_rusted", "bm riekling lance",
)
BLOODMOON_CLOTHING_IDS = (
    "bm_nordic01_glovel", "bm_nordic01_glover", "bm_nordic02_glovel", "bm_nordic02_glover",
    "bm_wool01_glovel", "bm_wool01_glover", "bm_wool02_glovel", "bm_wool02_glover",
    "bm_nordic01_pants", "bm_nordic02_pants", "bm_wool01_pants", "bm_wool02_pants",
    "bm_nordic01_robe", "bm_wool01_robe",
    "bm_nordic01_shirt", "bm_nordic02_shirt", "bm_wool01_shirt", "bm_wool02_shirt",
    "bm_nordic01_shoes", "bm_nordic02_shoes", "bm_wool01_shoes", "bm_wool02_shoes",
)
TRIBUNAL_ARMOR_IDS = (
    "darkbrotherhood helm", "darkbrotherhood cuirass", "darkbrotherhood greaves",
    "darkbrotherhood boots", "darkbrotherhood pauldron_l", "darkbrotherhood pauldron_r",
    "darkbrotherhood gauntlet_l", "darkbrotherhood gauntlet_r",
)
TRIBUNAL_WEAPON_IDS = (
    "centurion_projectile_dart", "spring dart", "fine spring dart",
    "ebony scimitar", "goblin_sword", "goblin_club",
)
TRIBUNAL_CLOTHING_IDS = (
    "common_pants_06", "common_pants_07", "expensive_pants_mournhold",
    "common_shirt_06", "common_shirt_07", "expensive_shirt_mournhold",
    "common_shoes_06", "common_shoes_07", "expensive_shoes_mournhold",
    "common_skirt_06", "common_skirt_07", "expensive_skirt_mournhold",
)


def protected_ids():
    manifest = json.loads((pathlib.Path(__file__).resolve().parents[1] / "data/protected_item_ids.json").read_text(encoding="utf-8"))
    return {ident for source in manifest["sources"] for ident in source["ids"]}


def read_master(path):
    items, lists = {}, {}
    tags = {b"ARMO": ("armor", b"AODT"), b"WEAP": ("weapon", b"WPDT"),
            b"CLOT": ("clothing", b"CTDT")}
    with path.open("rb") as stream:
        while header := stream.read(16):
            if len(header) != 16:
                raise ValueError("Truncated TES3 record header")
            tag, size, _, flags = struct.unpack("<4sIII", header)
            if tag not in tags and tag != b"LEVI":
                stream.seek(size, 1)
                continue
            parts = list(subrecords(stream.read(size)))
            fields = dict(parts)
            ident = decode(fields.get(b"NAME", b"")).lower()
            if flags & 0x20 or b"DELE" in fields:
                (lists if tag == b"LEVI" else items).pop(ident, None)
                continue
            if tag == b"LEVI":
                lists[ident] = [decode(value).lower() for key, value in parts if key == b"INAM"]
                continue
            category, data_tag = tags[tag]
            data = fields[data_tag]
            if category == "weapon":
                kind = struct.unpack_from("<H", data, 8)[0]
                value = struct.unpack_from("<I", data, 4)[0]
            else:
                kind = struct.unpack_from("<I", data)[0]
                value = struct.unpack_from("<H" if category == "clothing" else "<I", data, 8)[0]
            items[ident] = {
                "id": ident, "category": category, "slot": SLOTS[category][kind],
                "name": decode(fields.get(b"FNAM", b"")), "value": value,
                "script": decode(fields.get(b"SCRI", b"")),
                "enchantment": decode(fields.get(b"ENAM", b"")),
            }
    return items, lists


def expand_list(ident, lists, items, visiting=None):
    visiting = set() if visiting is None else visiting
    if ident in visiting:
        raise ValueError(f"Cyclic leveled list: {ident}")
    if ident in items:
        return {ident}
    if ident not in lists:
        raise ValueError(f"Unresolved normal-list entry: {ident}")
    result = set()
    for entry in lists[ident]:
        result.update(expand_list(entry, lists, items, visiting | {ident}))
    return result


def select_pool(items, lists):
    excluded = protected_ids()
    evidence = {}
    roots = sorted(ident for ident in lists
                   if ident.startswith(("l_n_armor", "l_n_wpn_", "l_n_rings", "l_n_amulet")))
    for root in roots:
        for ident in expand_list(root, lists, items):
            evidence.setdefault(ident, set()).add(root)
    # Vanilla normal lists do not cover every clothing slot.
    for ident, item in items.items():
        if item["category"] == "clothing" and CLOTHING_ID.fullmatch(ident):
            evidence.setdefault(ident, set()).add("Standard numbered clothing series")
    for ident in STANDARD_GLASS_ARMOR_IDS:
        if ident not in items:
            continue
        item = items[ident]
        if item['category'] != 'armor' or item['script'] or item['enchantment']:
            raise ValueError('Unexpected standard Glass armor source record: ' + ident)
        evidence.setdefault(ident, set()).add('User-approved standard Glass armor base')
    selected = []
    for ident in evidence:
        item = items[ident]
        if ident.endswith("_unique") or ident in excluded:
            continue
        if item["enchantment"] or item["script"].lower() not in ("", "legionuniform"):
            continue
        selected.append(dict(item, evidence=sorted(evidence[ident])))
    return sorted(selected, key=lambda r: (r["category"], SLOTS[r["category"]].index(r["slot"]), r["id"]))


def select_approved_expansion(items, categories):
    excluded = protected_ids()
    selected = []
    for category, ids in categories.items():
        for ident in ids:
            if ident.endswith("_unique") or ident in excluded:
                continue
            item = items.get(ident)
            if not item or item["category"] != category or item["script"] or item["enchantment"]:
                raise ValueError(f"Missing or unexpectedly protected approved expansion item: {ident}")
            selected.append(dict(item, evidence=["User-approved expansion item list"]))
    return sorted(selected, key=lambda row: (row["category"], SLOTS[row["category"]].index(row["slot"]), row["id"]))


def select_bloodmoon_pool(items):
    return select_approved_expansion(items, {
        "armor": BLOODMOON_ARMOR_IDS, "weapon": BLOODMOON_WEAPON_IDS, "clothing": BLOODMOON_CLOTHING_IDS,
    })


def select_tribunal_pool(items):
    return select_approved_expansion(items, {
        "armor": TRIBUNAL_ARMOR_IDS, "weapon": TRIBUNAL_WEAPON_IDS, "clothing": TRIBUNAL_CLOTHING_IDS,
    })


def select_oaab_pool(items):
    excluded = protected_ids()
    manifest = json.loads((pathlib.Path(__file__).resolve().parents[1] / "data/oaab_item_allowlist.json").read_text(encoding="utf-8"))
    selected = []
    for category, ids in manifest["items"].items():
        for ident in ids:
            if ident in excluded:
                continue
            item = items.get(ident)
            if (not item or item["category"] != category or item["enchantment"]
                    or item["script"].lower() not in ("", "legionuniform")
                    or ident.endswith("_unique")):
                raise ValueError(f"Missing or unexpectedly protected approved OAAB item: {ident}")
            selected.append(dict(item, evidence=["Reviewed static OAAB allowlist"]))
    if len({row["id"] for row in selected}) != len(selected):
        raise ValueError("Duplicate OAAB allowlist ID")
    return sorted(selected, key=lambda row: (row["category"], SLOTS[row["category"]].index(row["slot"]), row["id"]))


def lua_pool(rows, source="Morrowind.esm"):
    label = "base-game" if source == "Morrowind.esm" else f"optional {source.removesuffix('.esm')}"
    lines = [f"-- Static {label} pool. Generated from source {source} for review.",
             "-- Loaded by the development runtime. Missing IDs are skipped.",
             "-- See docs/reports/included-items-report.md for included items and scope.", "return {"]
    for category, slots in SLOTS.items():
        lines.append(f"    {category} = {{")
        for slot in slots:
            lines.append(f"        {slot} = {{")
            for row in rows:
                if row["category"] == category and row["slot"] == slot:
                    lines.append(f"            {json.dumps(row['id'])},")
            lines.append("        },")
        lines.append("    },")
    return "\n".join(lines + ["}", ""])


def markdown_pool(rows):
    lines = ["# Static Base-Game Item Pool", "", "Prepared 2026-10-04. Static pool loaded by the development build.", "",
             "## Policy", "",
             "- Base game only: read directly from vanilla `Morrowind.esm`; no expansion or POTI additions.",
             "- Armor and weapons: trust entries recursively reached from vanilla `l_n_armor*` and `l_n_wpn_*` lists.",
             "- Also include the ten explicitly approved standard Glass armor IDs (including both shields and both bracers).",
             "- Jewelry: vanilla `l_n_rings` / `l_n_amulet`, plus the standard numbered clothing series.",
             "- Other clothing: explicit standard numbered Common, Expensive, Extravagant, and Exquisite IDs,",
             "  including letter-suffixed visual variants. Named quest/custom clothing variants are not selected by this rule.",
             "- Skip source-enchanted items and source scripts other than the reviewed `LegionUniform` exception.",
             "- Exclude every record ID ending in `_unique`, across all source packs.",
             "- Exclude exact quest, unique, and artifact IDs reviewed in `data/protected_item_ids.json`.",
             "- No maximum-value filter when defining this static pool. The current prototype's value cap remains unchanged.",
             "- Keep every distinct ID, including left/right items. No runtime selection by names, prefixes, or loot tables.", "",
             "The shipped Lua table contains literal IDs only. The extraction tool is a development utility, not an in-game dependency.",
             "External ID references are not blanket exclusion gates for these trusted base items. Compatibility with every",
             "installed mod is not guaranteed; runtime handling must skip missing, newly enchanted, or unreviewed scripted records.", "",
             "## Coverage", "", "| Category | IDs |", "| --- | ---: |"]
    for category in SLOTS:
        lines.append(f"| {category.title()} | {sum(r['category'] == category for r in rows)} |")
    lines.extend([f"| **Total** | **{len(rows)}** |", "", "## Generation Status", "",
                  "Randomised Basic Loot supports armor, weapons, and clothing with per-item corpse replacement.",
                  "Runtime safety checks still skip all scripted and already-enchanted bases, even when their IDs are listed.",
                  "Projectiles use physical-only modifiers; equipment and balance behavior still need in-game validation.",
                  "Rings share one base-item list; left/right ring equipment positions are not separate record types.", "",
                  "Baseline reference: [UESP Leveled Lists](https://en.uesp.net/wiki/Morrowind:Leveled_Lists).",
                  "Record slot mappings checked against OpenMW's",
                  "[armor](https://raw.githubusercontent.com/OpenMW/openmw/master/components/esm3/loadarmo.hpp),",
                  "[clothing](https://raw.githubusercontent.com/OpenMW/openmw/master/components/esm3/loadclot.hpp), and",
                  "[weapon](https://raw.githubusercontent.com/OpenMW/openmw/master/components/esm3/loadweap.hpp) definitions.", ""])
    for category, slots in SLOTS.items():
        lines.extend([f"## {category.title()}", ""])
        for slot in slots:
            group = [row for row in rows if row["category"] == category and row["slot"] == slot]
            lines.extend([f"### {slot.replace('_', ' ').title()} ({len(group)})", ""])
            if not group:
                lines.extend(["No ordinary items selected for this subtype.", ""])
                continue
            lines.extend(["| ID | Vanilla Name | Gold | Baseline Evidence |", "| --- | --- | ---: | --- |"])
            for row in group:
                name = row["name"].replace("|", "\\|")
                lines.append(f"| `{row['id']}` | {name} | {row['value']} | {', '.join(row['evidence'])} |")
            lines.append("")
    return "\n".join(lines) + "\n"


def included_items_report(rows, bloodmoon_rows=None, tribunal_rows=None, oaab_rows=None):
    bloodmoon_rows = bloodmoon_rows or []
    tribunal_rows = tribunal_rows or []
    oaab_rows = oaab_rows or []
    packs = [("Morrowind (Base Game)", "Morrowind.esm", rows)]
    if tribunal_rows:
        packs.append(("Tribunal", "Tribunal.esm", tribunal_rows))
    if bloodmoon_rows:
        packs.append(("Bloodmoon", "Bloodmoon.esm", bloodmoon_rows))
    if oaab_rows:
        packs.append(("OAAB Data", "OAAB_Data.esm", oaab_rows))
    lines = [
        "# Included Items Report", "", "Prepared 2026-10-04.", "",
        "This reports the current static item pool, not the equipment categories supported by the running prototype.",
        "Hierarchy: mod/expansion -> category -> sub-category. Each included ID appears once.",
        "Names and values are original source-master values, not POTI overrides.", "",
        "Record IDs ending in `_unique` are excluded from every source pack.", "",
        "Exact quest, unique, and artifact IDs are additionally excluded using `data/protected_item_ids.json`.",
        "Wiki references and the current intersection audit: [Vanilla Enchantment Review](vanilla-enchantment-review.md).", "",
        "## Mod / Expansion Summary", "",
        "| Mod / Expansion | Armor | Weapons | Clothing | Total | Status |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for label, _, records in packs:
        counts = [sum(row["category"] == category for row in records) for category in SLOTS]
        lines.append(f"| {label} | {counts[0]} | {counts[1]} | {counts[2]} | {len(records)} | Included |")
    if not bloodmoon_rows:
        lines.append("| Bloodmoon | 0 | 0 | 0 | 0 | Not included |")
    if not tribunal_rows:
        lines.append("| Tribunal | 0 | 0 | 0 | 0 | Not included |")
    lines.extend([
        "| Tamriel Data / Other Mods | 0 | 0 | 0 | 0 | Not included |", "",
        f"**Total included IDs: {sum(len(records) for _, _, records in packs)}.**", "",
        "Base-game IDs: `mod/scripts/randomisedbasicloot/base_items.lua`.",
        "Selection policy and generation limitations: [Base-Game Item Pool](base-game-item-pool.md).", "",
    ])
    if bloodmoon_rows:
        lines.extend([
            "Bloodmoon IDs: `mod/scripts/randomisedbasicloot/bloodmoon_items.lua`.",
            "Bloodmoon selection is exactly the user-approved Nordic Mail, Wolf, and Bear armor sets",
            "plus the Riekling Shield (28 armor IDs), the linked base clothing (22 IDs), and base weapons",
            "excluding Stalhrim (16 IDs). Named enchanted variants and other unlisted items are not included.",
            "This is an optional data pack, not a hard dependency.",
            "IDs and values were checked against the installed vanilla `Bloodmoon.esm`, without editing POTI.",
            "No value cap is applied to pool membership; Nordic Mail entries exceed the prototype's unchanged gameplay cap.", "",
            "References: [Bloodmoon Base Clothing](https://en.uesp.net/wiki/Bloodmoon:Base_Clothing) and",
            "[Bloodmoon Base Weapons](https://en.uesp.net/wiki/Bloodmoon:Base_Weapons).",
            "Page item lists were verified in the browser and matched to expansion records.", "",
        ])
    if tribunal_rows:
        lines.extend([
            "Tribunal IDs: `mod/scripts/randomisedbasicloot/tribunal_items.lua`.",
            "Tribunal includes eight Dark Brotherhood armor pieces, 12 base clothing IDs, and six base weapon IDs.",
            "All Adamantium weapons and IDs ending in `_unique` are excluded. No extra variants are inferred.",
            "Reference: [Tribunal Dark Brotherhood Armor](https://en.uesp.net/wiki/Tribunal:Dark_Brotherhood_Armor).",
            "Additional references: [Tribunal Base Clothing](https://en.uesp.net/wiki/Tribunal:Base_Clothing) and",
            "[Tribunal Base Weapons](https://en.uesp.net/wiki/Tribunal:Base_Weapons).",
            "Page item lists were verified in the browser and matched to vanilla `Tribunal.esm`. This data pack is optional.", "",
        ])
    if oaab_rows:
        manifest = json.loads((pathlib.Path(__file__).resolve().parents[1] / "data/oaab_item_allowlist.json").read_text(encoding="utf-8"))
        lines.extend([
            "OAAB IDs: `mod/scripts/randomisedbasicloot/oaab_items.lua`.",
            "Frozen allowlist: `data/oaab_item_allowlist.json`. New OAAB records are not automatically included.",
            "Reviewed directly from the installed `OAAB_Data.esm`; no other POTI mods or overrides were scanned or edited.",
            f"Source SHA-256: `{manifest['source_sha256']}`.",
            "Include ordinary unenchanted equipment designs and visual variants, including Silver Scepter.",
            "Exclude all source-enchanted records (including Chastening and Stormruler), IDs ending in `_unique`,",
            "and unreviewed item scripts. Imperial Battlemage Cuirass retains the reviewed `LegionUniform` exception.",
            "Also exclude the invisible Shield and both Glass Assassin pauldrons as special-purpose equipment.",
            "Distinct Daedric faces and faction-style helmets are treated as base designs, not artifacts solely because of their names.",
            "OAAB Adamantium and Stalhrim base designs are included; previous material exclusions remain scoped to Tribunal/Bloodmoon.",
            "This source-level review does not guarantee compatibility with quests or exact-ID checks introduced by other mods.",
            "OAAB is an optional data pack, not a hard dependency. Missing IDs must be skipped when runtime support is implemented.",
            "References: [OAAB Data repository](https://github.com/OAAB-Modding/Data),",
            "[scepter additions](https://github.com/OAAB-Modding/Data/discussions/228), and",
            "[Glass Assassin equipment](https://github.com/OAAB-Modding/Data/discussions/166).", "",
        ])
    for label, source, records in packs:
        lines.extend([f"## {label} - {len(records)} Items", "", f"Source: `{source}`.", ""])
        for category, slots in SLOTS.items():
            count = sum(row["category"] == category for row in records)
            lines.extend([f"### {category.title()} - {count} Items", ""])
            if not count:
                lines.extend(["No included items in this category.", ""])
                continue
            for slot in slots:
                group = sorted((row for row in records if row["category"] == category and row["slot"] == slot),
                               key=lambda row: (row["name"].casefold(), row["id"]))
                if not group:
                    continue
                lines.extend([f"#### {slot.replace('_', ' ').title()} - {len(group)} Items", "",
                              "| Item Name | Record ID | Gold |", "| --- | --- | ---: |"])
                for row in group:
                    name = row["name"].replace("|", "\\|")
                    lines.append(f"| {name} | `{row['id']}` | {row['value']} |")
                lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("master", type=pathlib.Path)
    parser.add_argument("lua_output", type=pathlib.Path)
    parser.add_argument("markdown_output", type=pathlib.Path)
    parser.add_argument("--report", type=pathlib.Path)
    parser.add_argument("--bloodmoon", type=pathlib.Path)
    parser.add_argument("--bloodmoon-lua-output", type=pathlib.Path)
    parser.add_argument("--tribunal", type=pathlib.Path)
    parser.add_argument("--tribunal-lua-output", type=pathlib.Path)
    parser.add_argument("--oaab", type=pathlib.Path)
    parser.add_argument("--oaab-lua-output", type=pathlib.Path)
    args = parser.parse_args()
    if bool(args.bloodmoon) != bool(args.bloodmoon_lua_output):
        parser.error("--bloodmoon and --bloodmoon-lua-output must be supplied together")
    if bool(args.tribunal) != bool(args.tribunal_lua_output):
        parser.error("--tribunal and --tribunal-lua-output must be supplied together")
    if bool(args.oaab) != bool(args.oaab_lua_output):
        parser.error("--oaab and --oaab-lua-output must be supplied together")
    rows = select_pool(*read_master(args.master))
    bloodmoon_rows = select_bloodmoon_pool(read_master(args.bloodmoon)[0]) if args.bloodmoon else []
    tribunal_rows = select_tribunal_pool(read_master(args.tribunal)[0]) if args.tribunal else []
    oaab_rows = select_oaab_pool(read_master(args.oaab)[0]) if args.oaab else []
    args.lua_output.write_text(lua_pool(rows), encoding="utf-8")
    args.markdown_output.write_text(markdown_pool(rows), encoding="utf-8")
    if args.bloodmoon_lua_output:
        args.bloodmoon_lua_output.write_text(lua_pool(bloodmoon_rows, "Bloodmoon.esm"), encoding="utf-8")
    if args.tribunal_lua_output:
        args.tribunal_lua_output.write_text(lua_pool(tribunal_rows, "Tribunal.esm"), encoding="utf-8")
    if args.oaab_lua_output:
        args.oaab_lua_output.write_text(lua_pool(oaab_rows, "OAAB_Data.esm"), encoding="utf-8")
    if args.report:
        args.report.write_text(included_items_report(rows, bloodmoon_rows, tribunal_rows, oaab_rows), encoding="utf-8")
    for category in SLOTS:
        print(f"{category}: {sum(r['category'] == category for r in rows)}")
    print(f"Total: {len(rows)}")
    if bloodmoon_rows:
        print(f"Bloodmoon: {len(bloodmoon_rows)}")
    if tribunal_rows:
        print(f"Tribunal: {len(tribunal_rows)}")
    if oaab_rows:
        print(f"OAAB: {len(oaab_rows)}")
    print(f"Combined total: {len(rows) + len(bloodmoon_rows) + len(tribunal_rows) + len(oaab_rows)}")
