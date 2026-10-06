"""Build a Markdown review inventory from four explicitly selected masters."""

import argparse
import json
import pathlib
import struct

from audit_helmets import decode, load_config, subrecords


SOURCES = (
    ("Morrowind", "Morrowind.esm"),
    ("Tribunal", "Tribunal.esm"),
    ("Bloodmoon", "Bloodmoon.esm"),
    ("Tamriel Data", "Tamriel_Data.esm"),
)


def read_helmets(path):
    records = {}
    with path.open("rb") as stream:
        while header := stream.read(16):
            if len(header) != 16:
                raise ValueError(f"Truncated record header: {path}")
            tag, size, _, flags = struct.unpack("<4sIII", header)
            if tag != b"ARMO":
                stream.seek(size, 1)
                continue
            fields = dict(subrecords(stream.read(size)))
            ident = decode(fields.get(b"NAME", b"")).lower()
            if flags & 0x20 or b"DELE" in fields:
                records.pop(ident, None)
                continue
            data = fields.get(b"AODT", b"")
            if len(data) != 24 or struct.unpack_from("<I", data)[0] != 0:
                continue
            records[ident] = {
                "id": ident, "name": decode(fields.get(b"FNAM", b"")),
                "value": struct.unpack_from("<I", data, 8)[0],
                "script": decode(fields.get(b"SCRI", b"")),
                "enchantment": decode(fields.get(b"ENAM", b"")),
            }
    return records


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def normal_helmet_ids(path):
    with path.open("rb") as stream:
        while header := stream.read(16):
            if len(header) != 16:
                raise ValueError(f"Truncated record header: {path}")
            tag, size, _, flags = struct.unpack("<4sIII", header)
            if tag != b"LEVI":
                stream.seek(size, 1)
                continue
            parts = list(subrecords(stream.read(size)))
            if decode(dict(parts).get(b"NAME", b"")).lower() == "l_n_armor_helmet":
                return {decode(data).lower() for tag, data in parts if tag == b"INAM"}
    raise ValueError(f"Missing vanilla l_n_armor_helmet list: {path}")


def reviewed_lua_reference(reference):
    path = reference["path"].replace("\\", "/").lower()
    text = reference["text"].strip()
    if path.endswith("/scripts/sunsdusk/player_modules/p_clean.lua") and text.startswith("--"):
        return True
    if path.endswith("/scripts/craftingframework/parsers/converttsvtolua.lua") and "\t" in text:
        return True
    if "/scripts/fresh-loot/item-lists/" in path:
        return text.startswith('"') and text.endswith('",')
    if path.endswith("/scripts/tr_spells/leveled_lists.lua"):
        return text.startswith('["') and "={" in text
    if path.endswith("/scripts/deadly-blight-openmw-lua/shared.lua"):
        return text.startswith('["meshes/') and "--" in text
    return False


def passed_checks(source, current, trusted_normal=False):
    if current is None:
        return False
    if trusted_normal:
        # Trust the vanilla normal-item list, not arbitrary load-order additions.
        # The gameplay value cap is separate from membership of the review pool.
        return all(not r["enchantment"] and r["script"].lower() in ("", "legionuniform")
                   for r in (source, current))
    for record in (source, current):
        if (record["script"].lower() not in ("", "legionuniform")
                or record["enchantment"] or not 0 < record["value"] <= 150):
            return False
    unresolved = [ref for ref in current["references"]
                  if not (ref.get("record", "").lower() == "isvampirehiddenhelmet"
                          and ref.get("plugin", "").lower() == "melodies and moonlight.esp")]
    if unresolved:
        return False
    if current["ordinary_npc_count"] < 5 and current["leveled_list_count"] == 0:
        return False
    return all(reviewed_lua_reference(ref) for ref in current.get("lua_references", []))


def build(config, audit):
    directories, _ = load_config(config)
    current = {record["id"]: record for record in audit["helmets"]}
    groups, seen, trusted_ids = [], set(), set()
    for label, plugin in SOURCES:
        path = next((root / plugin for root in reversed(directories)
                     if (root / plugin).is_file()), None)
        if path is None:
            raise FileNotFoundError(f"Configured data folders do not contain {plugin}")
        if plugin == "Morrowind.esm":
            trusted_ids = normal_helmet_ids(path)
        records = [record for ident, record in read_helmets(path).items() if ident not in seen]
        seen.update(record["id"] for record in records)
        records = [record for record in records if passed_checks(
            record, current.get(record["id"]), record["id"] in trusted_ids)]
        groups.append((label, plugin, path, records))

    lines = [
        "# Trusted and Eligible Helmet Review Pool", "", "Prepared 2026-10-04. Temporary review document; not enabled in the mod.", "",
        "## Trusted Vanilla Baseline", "",
        "Per the user's policy, all vanilla entries in `l_n_armor_helmet` are trusted base items.",
        "Reference: [UESP: Leveled Normal Helmets](https://en.uesp.net/wiki/Morrowind:Leveled_Lists#l_n_armor_helmet).",
        "UESP returned HTTP 403, so membership was read directly from the installed vanilla `Morrowind.esm`.",
        "No entries added to this list by POTI's merged/override plugins are automatically trusted.",
        "For these vanilla entries, common-use counts and external ID references are informational, not exclusion gates.",
        "Unknown attached scripts and pre-existing enchantments still block selection; LegionUniform is the reviewed exception.",
        "The full trusted pool includes items above 150 gold. The running mod's 150-gold cap is unchanged;",
        "those rows are marked as currently outside the drop cap. Membership does not certify every mod interaction.", "",
        "## Base-Item Reference", "",
        "User-designated reference: [UESP: Morrowind Base Armor](https://en.uesp.net/wiki/Morrowind:Base_Armor).",
        "Use this to cross-check which vanilla items are ordinary base armor rather than special variants.",
        "This is separate from source-plugin membership and from replacement safety in the installed game.",
        "The page returned HTTP 403 during retrieval, so no rows have yet been verified against its contents.",
        "Inclusion below means passing the available local audit checks, not UESP confirmation or universal quest safety.", "",
        "## Scope", "",
        "Only Morrowind, Tribunal, Bloodmoon, and Tamriel Data source plugins were read for this inventory.",
        "Other mods' newly introduced items (including OAAB) are not included. POTI files were not edited.",
        "Items are grouped by the first of these four plugins that defines their helmet record ID,",
        "not by the plugin that currently overrides them. Names and gold below use the loaded POTI records.", "",
        "For expansion and Tamriel Data items, the existing audit checks still apply:", "",
        "- Helmet-slot armor in the source plugin and in the prior loaded-record audit.",
        "- No enchantment in either the source or loaded record.",
        "- No attached MWScript other than `LegionUniform`, which must be preserved and tested on generated variants.",
        "- Value between 1 and 150 gold in both records.",
        "- At least five direct NPC definitions without essential/script flags, OR at least one direct leveled-item list.",
        "- No unresolved explicit ID references in winning MWScript source or dialogue conditions/results.",
        "  The user has accepted possible incompatibility with Melodies and Moonlight's `isvampirehiddenhelmet`",
        "  checks, so those specific references alone no longer exclude an item. Other references still do.",
        "- No unresolved loose-Lua hits. Reviewed exceptions are Fresh Loot catalogs, TR Spells leveled-list",
        "  data, and Deadly Blight model-keyed entries where the item ID appears in a comment.", "",
        "  Also excluded from dependency flags: comments in Sun's Dusk's `p_clean.lua` and sample TSV",
        "  rows in Crafting Framework's standalone `convertTsvToLua.lua` conversion utility.", "",
        "Outside the trusted vanilla baseline, failed checks and other pending-reference reviews are excluded.",
        "Clothing-slot headwear is excluded. Separate IDs remain separate rows even when names match.", "",
        "NPC/list counts and POTI-specific notes reuse the prior `helmet-audit.json`; no new all-mod scan was run.",
        "NPCs = distinct winning NPC definitions carrying the item directly (including unused/test records).",
        "Lists = distinct winning leveled-item lists containing it directly, including merchant/equipment lists.",
        "Neither count includes indirect nested-list use or establishes quest safety.", "",
        "Missing hits are not proof of safety. Computed IDs, archive scripts, non-Lua data, indirect quest",
        "dependencies, and per-instance protections are outside these checks. Runtime protections remain necessary.",
        "Re-audit after load-order changes. The report does not install an allowlist or replace any items.",
        "These are policy-eligible candidates, not an in-game compatibility certification. `LegionUniform`",
        "preservation and the optional vampire integration are not yet implemented or validated in this mod.", "",
        "## Summary", "", "| Group | Passed |",
        "| --- | ---: |",
    ]
    for label, _, _, records in groups:
        lines.append(f"| {label} | {len(records)} |")
    lines.extend(["", "## Source Files", ""])
    for _, plugin, path, _ in groups:
        lines.append(f"- `{plugin}`: `{path}`")

    for label, _, _, records in groups:
        lines.extend(["", f"## {label}", ""])
        rows = sorted(records, key=lambda r: (current[r["id"]]["name"].casefold(), r["id"]))
        if not rows:
            lines.extend(["No items passed all checks in this group.", ""])
            continue
        lines.extend(["| Record ID | Loaded Name | Gold | POTI NPCs | POTI Lists | Example Item Lists | Compatibility Conditions |",
                      "| --- | --- | ---: | ---: | ---: | --- | --- |"])
        for record in rows:
            loaded = current[record["id"]]
            examples = sorted({entry["id"] for entry in loaded["leveled_lists"]})[:3]
            conditions = []
            if record["id"] in trusted_ids:
                conditions.append("Trusted vanilla normal-item entry")
                if loaded["value"] > 150:
                    conditions.append("Outside current 150-gold gameplay cap")
            if loaded["script"].lower() == "legionuniform":
                conditions.append("Preserve LegionUniform; equip/unequip test pending")
            if any(ref["record"].lower() == "isvampirehiddenhelmet"
                   and ref["plugin"].lower() == "melodies and moonlight.esp"
                   for ref in loaded["references"]):
                conditions.append("Accepted vampire-hiding compatibility risk")
            values = [f'`{record["id"]}`', loaded["name"], loaded["value"],
                      loaded["npc_count"], loaded["leveled_list_count"],
                      ", ".join(f"`{ident}`" for ident in examples) or "Direct NPC use",
                      "; ".join(conditions) or "No additional conditions identified"]
            lines.append("| " + " | ".join(cell(v) for v in values) + " |")
        lines.append("")
    return "\n".join(lines) + "\n", groups


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=pathlib.Path)
    parser.add_argument("audit", type=pathlib.Path)
    parser.add_argument("output", type=pathlib.Path)
    args = parser.parse_args()
    markdown, groups = build(args.config, json.loads(args.audit.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8")
    for label, _, _, records in groups:
        print(f"{label}: {len(records)} helmets")
    print(f"Written {args.output}")
