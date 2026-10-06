"""Author fixed unique drafts from approved source masters, never installed overrides."""

import argparse
import collections
import hashlib
import json
import pathlib
import struct

from audit_helmets import decode, subrecords
from base_item_pool import (read_master, select_pool, select_bloodmoon_pool,
                            select_tribunal_pool, select_oaab_pool, protected_ids)
from unique_designs import compile_unique, compile_bespoke, ARMOR_SETTINGS, BESPOKE, signature

ROOT = pathlib.Path(__file__).resolve().parents[1]
PREFIX_WORDS = "Ash Amber Birch Brine Bronze Candle Cinder Cloud Copper Dawn Dusk Elm Ember Flint Fog Frost Glass Granite Hearth Heather Hollow Ivory Jade Juniper Larch Laurel Maple Marsh Mist Moon Moss Night Oak Onyx Pearl Pine Quartz Rain Reed River Rowan Rust Salt Sea Silver Snow Star Stone Storm Sun Thorn Tide Willow Wind Winter Yew".split()
TITLE_WORDS = "Accord Anchor Bargain Beacon Bond Burden Cadence Calling Covenant Credo Echo Errand Favor Gift Grace Haven Heart Heirloom Keepsake Lament Ledger Memory Mercy Oath Offering Pact Passage Pledge Promise Ransom Refuge Remnant Reprieve Resolve Secret Shelter Sign Silence Solace Song Testament Token Tribute Truce Vigil Vow Wake Warning Whisper Witness Writ".split()


def physical_records(path):
    records = {}
    with path.open("rb") as stream:
        while header := stream.read(16):
            tag, size, _, flags = struct.unpack("<4sIII", header)
            if tag not in (b"ARMO", b"WEAP", b"CLOT"):
                stream.seek(size, 1)
                continue
            parts = dict(subrecords(stream.read(size)))
            ident = decode(parts[b"NAME"]).lower()
            if flags & 0x20 or b"DELE" in parts:
                records.pop(ident, None)
                continue
            if tag == b"ARMO":
                _, weight, value, health, capacity, armor = struct.unpack("<IfIIII", parts[b"AODT"])
                record = dict(weight=weight, value=value, health=health,
                              enchantCapacity=capacity / 10, baseArmor=armor)
            elif tag == b"CLOT":
                _, weight, value, capacity = struct.unpack("<IfHH", parts[b"CTDT"])
                record = dict(weight=weight, value=value, enchantCapacity=capacity / 10)
            else:
                weight, value, _, health, speed, reach, capacity, *rest = struct.unpack("<fIHHffH6BI", parts[b"WPDT"])
                record = dict(weight=weight, value=value, health=health, speed=speed,
                              reach=reach, enchantCapacity=capacity / 10)
                for index, attack in enumerate(("chop", "slash", "thrust")):
                    record[attack + "MinDamage"] = rest[index * 2]
                    record[attack + "MaxDamage"] = rest[index * 2 + 1]
            records[ident] = record
    return records


def armor_settings(path):
    wanted = set(ARMOR_SETTINGS.values()) | {'fLightMaxMod', 'fMedMaxMod'}
    result = {}
    with path.open('rb') as stream:
        while header := stream.read(16):
            tag, size, _, _ = struct.unpack('<4sIII', header)
            if tag != b'GMST':
                stream.seek(size, 1)
                continue
            parts = dict(subrecords(stream.read(size)))
            name = decode(parts.get(b'NAME', b''))
            if name not in wanted:
                continue
            if b'INTV' in parts:
                result[name] = struct.unpack('<i', parts[b'INTV'])[0]
            elif b'FLTV' in parts:
                result[name] = struct.unpack('<f', parts[b'FLTV'])[0]
    missing = wanted - set(result)
    if missing:
        raise ValueError('Missing armor classification settings: ' + ', '.join(sorted(missing)))
    return result




def unique_name(item, ordinal, used):
    digest = hashlib.sha256((item["id"] + ":" + str(ordinal)).encode()).digest()
    count = len(PREFIX_WORDS) * len(TITLE_WORDS)
    start = int.from_bytes(digest[:4], "big") % count
    for offset in range(count):
        index = (start + offset) % count
        title = PREFIX_WORDS[index // len(TITLE_WORDS)] + " " + TITLE_WORDS[index % len(TITLE_WORDS)]
        name = title + " - " + item["name"]
        if name not in used:
            used.add(name)
            return name
    raise ValueError("Name vocabulary exhausted")


def format_effect(entry):
    names = {
        "nighteye": "Night Eye", "fortifyattribute": "Fortify", "drainattribute": "Drain",
        "fortifyskill": "Fortify", "fortifyfatigue": "Fortify Fatigue", "fortifymagicka": "Fortify Magicka",
        "blind": "Blind", "feather": "Feather", "resistfire": "Resist Fire", "resistfrost": "Resist Frost",
        "resistshock": "Resist Shock", "weaknesstofire": "Weakness to Fire", "weaknesstofrost": "Weakness to Frost",
        "shield": "Shield", "light": "Light", "slowfall": "Slowfall", "swiftswim": "Swift Swim",
        "telekinesis": "Telekinesis", "detectkey": "Detect Key", "detectenchantment": "Detect Enchantment",
        "sanctuary": "Sanctuary", "resistblightdisease": "Resist Blight Disease", "fireshield": "Fire Shield",
        "frostshield": "Frost Shield", "lightningshield": "Lightning Shield", "fortifyattack": "Fortify Attack",
        "fortifymaximummagicka": "Fortify Maximum Magicka (native units)",
        "resistpoison": "Resist Poison", "waterwalking": "Water Walking", "waterbreathing": "Water Breathing",
        "firedamage": "Fire Damage", "frostdamage": "Frost Damage", "shockdamage": "Shock Damage",
        "poison": "Poison", "damagefatigue": "Damage Fatigue", "sound": "Sound",
        "weaknesstoshock": "Weakness to Shock",
        "weaknesstopoison": "Weakness to Poison",
        "paralyze": "Paralyze", "restorehealth": "Restore Health (pts/sec)",
        "restoremagicka": "Restore Magicka (pts/sec)", "restorefatigue": "Restore Fatigue (pts/sec)",
    }
    target = entry.get("attribute", entry.get("skill", ""))
    labels = {'handtohand': 'Hand-to-hand', 'heavyarmor': 'Heavy Armor', 'mediumarmor': 'Medium Armor',
              'lightarmor': 'Light Armor'}
    label = names[entry["id"]] + (" " + labels.get(target, target.title()) if target else "") + " " + str(entry["magnitude"])
    if entry.get('duration'):
        label += ' for ' + str(entry['duration']) + ' sec'
    if entry.get('range'):
        label += ' [' + entry['range'] + ']'
    return label


def format_record(record):
    fields = []
    for key, label in (("baseArmor", "Base armor"), ("health", "Maximum condition"),
                       ("weight", "Weight"), ("value", "Gold"), ("speed", "Speed"),
                       ("reach", "Reach"), ("enchantCapacity", "Enchant capacity")):
        if key in record:
            fields.append(label + " " + str(record[key]))
    for attack in ("chop", "slash", "thrust"):
        if attack + "MinDamage" in record:
            fields.append(f"{attack.title()} {record[attack + 'MinDamage']}-{record[attack + 'MaxDamage']}")
    return "; ".join(fields)


def registry(design, items):
    templates = collections.defaultdict(list)
    for template in design["uniqueTemplates"]:
        templates[template["baseId"]].append(template)
    count = len(design['uniqueTemplates'])
    lines = ["# Unique Item Registry", "", "Generated draft authoring register, 2026-10-04. Exported to the development runtime.", "",
             f"**{len(items)} exact base item IDs; four baseline designs per item plus authored additions; {count:,} unique templates.**", "",
             "Coverage is per exact record ID, not per slot, material, or set. The target remains 3-5 per item.",
             "The old repeated slot profiles have been revised into distinct functional recipes for non-ammunition.",
             "Magnitude or name changes alone do not reserve a new recipe. These are compiled design drafts,",
             f"not {count:,} hand-authored or playtested items. Names, effect roles, and numbers are fixed in",
             "[loot-design.json](loot-design.json); no profile math or random naming occurs at drop time.", "",
             "Hierarchy: source pack -> category -> slot -> exact base item. Each row records effects,",
             "absolute stats, effect purposes, identity, drawbacks, final armor class, and template identity.",
             "Unlisted fields inherit the source; innate enchant capacity is not an added unique modifier.",
             "All template selection weights are 1. No template references a vanilla unique or quest item.", "",
             "## Review Limits", "",
             "Final weight is resolved before armor-skill effects; class-changing designs are allowed.",
             "The listed class uses the source Morrowind GMSTs. Bind marked armor skills again to loaded GMSTs",
             "after final physical overrides at runtime.",
             "Unique recipes reject internally neutralized roles (e.g. Swift Swim plus Water Walking),",
             "same-attribute fortify/drain, same-element resist/weakness, and dead added enchant capacity.",
             "The explicit conflict rules are conservative design guards, not an exhaustive engine interaction proof.",
             "Native flags, models, icons, body parts, and approved scripts must be inherited when implemented.",
             "Melee weapons include native charged strike specialties; launchers keep equipped effects only.",
             "No weapon grants Hand-to-hand. No invented conditional script mechanics are claimed.",
             "Projectile drafts stay physical-only: no unverified enchantment delivery is assumed.",
             "Projectile drafts are enabled for development; stack/replacement/field behavior needs engine validation.",
             "Extreme weapon profiles trade speed/weight for damage; zero damage channels remain zero.",
             "Ordinary unique packages target reliable mid-tier output, while extremes can win one stat with a drawback.",
             "The maximum-damage-times-speed proxy is not measured DPS; no universal dominance claim is made.",
             "Do not enable upper tiers or thousands of designs solely because schema validation passes.", "",
             "Ammunition remains a physical-only draft with limited expressive mechanics; it is not claimed",
             "to have 4 entirely new engine behaviors per base. More elaborate ammo needs delivery support.",
             "Lore/version persistence and native-tooltip limitations are recorded in",
             "[Item Metadata Design](item-metadata-design.md). Lore is not yet authored for every template.", "",
             "## Coverage", "", "| Source | Base IDs | Unique Designs |", "| --- | ---: | ---: |"]
    groups = collections.defaultdict(list)
    for item in items:
        groups[item["source"]].append(item)
    for source, rows in groups.items():
        lines.append(f"| {source} | {len(rows)} | {sum(len(templates[i['id']]) for i in rows)} |")
    for source, rows in groups.items():
        lines += ["", "## " + source]
        for category in ("armor", "weapon", "clothing"):
            subset = [item for item in rows if item["category"] == category]
            if not subset:
                continue
            lines += ["", "### " + category.title()]
            for slot in sorted({item["slot"] for item in subset}):
                lines += ["", "#### " + slot.replace("_", " ").title()]
                for item in sorted((i for i in subset if i["slot"] == slot), key=lambda i: (i["name"], i["id"])):
                    lines += ["", f"##### {item['name']} - `{item['id']}`", "",
                              "| Unique / Template ID | Identity | Fixed Physical Stats / Final Class | Effects And Their Purpose | Drawbacks |",
                              "| --- | --- | --- | --- | --- |"]
                    for template in templates[item["id"]]:
                        effects = "; ".join(format_effect(e) + ' (' + e.get('purpose', 'explicit specialty') + ')' for e in template["effects"]) or "None (physical-only)"
                        if template["effects"]:
                            if template.get('mode') == 'CastOnStrike':
                                effects += '; Cast On Strike, Touch; charge ' + str(template['charge']) + '; native autocalculated cost'
                            else:
                                effects += "; Constant Effect, Self"
                        drawbacks = "; ".join(template.get("drawbacks", [])) or "None separately specified; inspect fixed stats"
                        class_label = {'lightarmor': 'Light Armor', 'mediumarmor': 'Medium Armor',
                                       'heavyarmor': 'Heavy Armor'}.get(template.get('resolvedArmorClass'), 'Not armor')
                        physical_roles = '; '.join(field + ': ' + purpose for field, purpose in template.get('modifierPurposes', {}).items())
                        lines.append(f"| {template['name']} / `{template['id']}` | {template.get('identity', '')} | {format_record(template['record'])}; Class {class_label}; Physical roles: {physical_roles} | {effects} | {drawbacks} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vanilla", type=pathlib.Path, required=True)
    parser.add_argument("--oaab", type=pathlib.Path, required=True)
    parser.add_argument('--revise-designs', action='store_true', help='Explicit pre-v1 recipe revision; never touches game saves.')
    args = parser.parse_args()
    packs = [("Morrowind (Base Game)", args.vanilla / "Morrowind.esm", lambda data: select_pool(*data)),
             ("Tribunal", args.vanilla / "Tribunal.esm", lambda data: select_tribunal_pool(data[0])),
             ("Bloodmoon", args.vanilla / "Bloodmoon.esm", lambda data: select_bloodmoon_pool(data[0])),
             ("OAAB Data", args.oaab, lambda data: select_oaab_pool(data[0]))]
    design_path = ROOT / "data/loot-design.json"
    design = json.loads(design_path.read_text())
    settings = armor_settings(args.vanilla / 'Morrowind.esm')
    # Preserve manually authored starters and prior fixed drafts on regeneration.
    existing = collections.defaultdict(list)
    for template in design["uniqueTemplates"]:
        existing[template["baseId"]].append(template)
    used = {t["name"] for t in design["uniqueTemplates"]}
    used_signatures = set()
    # Reserve named authored recipes so systematic compilation cannot consume their identity.
    for _, _, authored in BESPOKE.values():
        used_signatures.add(signature(authored, '', ''))
    if not args.revise_designs:
        used_signatures.update(t['functionalRecipe'] for t in design['uniqueTemplates'] if t.get('functionalRecipe'))
    templates, all_items = [], []
    for source, path, selector in packs:
        physical = physical_records(path)
        for item in sorted(selector(read_master(path)), key=lambda row: row["id"]):
            item = dict(item, source=source)
            all_items.append(item)
            rows = existing[item["id"]]
            if len(rows) > design['uniqueAuthoring']['targetMaximumPerBase']:
                raise ValueError("Unexpected existing coverage: " + item["id"])
            for ordinal in range(len(rows), 4):
                digest = hashlib.sha256(item["id"].encode()).hexdigest()[:16]
                template = dict(id=f"unique_{digest}_{ordinal + 1}", baseId=item["id"],
                                name=unique_name(item, ordinal, used), weight=1,
                                record=dict(physical[item['id']]), effects=[], drawbacks=[], templateVersion=1,
                                authoringStatus="recipe_pending",
                                source=source, category=item["category"], slot=item["slot"])
                rows.append(template)
            for ordinal, template in enumerate(rows):
                if args.revise_designs or not template.get('identity'):
                    authored = BESPOKE.get(template['id'])
                    if authored:
                        used_signatures.discard(signature(authored[2], '', ''))
                    revision = compile_bespoke(template['id'], item, physical[item['id']], settings, used_signatures)
                    if not revision:
                        revision = compile_unique(item, physical[item['id']], ordinal, settings, used_signatures)
                    template.update(revision)
                    template['templateVersion'] = template.get('templateVersion', 1) + 1
                    template['revisionNote'] = 'Pre-v1: distinct functional recipe; each effect has a purpose; final-weight armor binding.'
                elif template.get('functionalRecipe'):
                    used_signatures.add(template['functionalRecipe'])
            for template in rows:
                template.setdefault("authoringStatus", "starter_draft_review_required")
                template.setdefault("templateVersion", 1)
                template.update(source=source, category=item["category"], slot=item["slot"])
            templates.extend(rows)
    ids = {i["id"] for i in all_items}
    if len(ids) != 750 or len(all_items) != 750 or ids & protected_ids():
        raise ValueError("Pool coverage/protection mismatch")
    if set(existing) - ids:
        raise ValueError("Existing templates outside approved pool")
    if (not len(ids) * design['uniqueAuthoring']['targetMinimumPerBase'] <= len(templates)
            <= len(ids) * design['uniqueAuthoring']['targetMaximumPerBase']
            or len({t["id"] for t in templates}) != len(templates)
            or len({t["name"] for t in templates}) != len(templates)):
        raise ValueError("Template count/identity mismatch")
    design["uniqueTemplates"] = templates
    design['uniqueAuthoring']['internalDeadModifiers'] = 'forbidden'
    design['uniqueAuthoring']['ammunitionException'] = 'limited_native_physical_mechanics_not_bespoke_spell_behavior'
    design['uniqueAuthoring']['differentiation'] = 'distinct_effect_roles_not_names_or_magnitudes'
    design['composition']['armorClassPolicy'] = 'resolve_final_weight_then_bind_or_validate_armor_skill'
    design['uniqueConflictPolicy'] = {
        'swimWithSurfaceTravel': 'reject', 'sameAttributeFortifyAndDrain': 'reject',
        'sameElementProtectionAndWeakness': 'reject', 'addedCapacityWithNativeEnchantment': 'reject',
        'ordinaryDeadAffixes': 'remain_allowed',
    }
    design_path.write_text(json.dumps(design, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    (ROOT / "docs/reports/unique-item-registry.md").write_text(registry(design, all_items), encoding="utf-8")
    print(f"Recorded {len(templates)} fixed templates for {len(ids)} exact base IDs.")


if __name__ == "__main__":
    main()
