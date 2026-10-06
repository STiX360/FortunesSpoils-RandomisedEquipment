"""Read TES3 plugins in OpenMW load order and audit common helmet candidates."""

import argparse
import collections
import json
import pathlib
import re
import struct


def decode(data):
    return data.split(b"\0", 1)[0].decode("cp1252", errors="replace")


def subrecords(data):
    offset = 0
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError("Truncated subrecord header")
        tag, size = struct.unpack_from("<4sI", data, offset)
        offset += 8
        if offset + size > len(data):
            raise ValueError("Truncated subrecord payload")
        yield tag, data[offset:offset + size]
        offset += size


def load_config(path):
    directories, plugins = [], []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        key, _, value = line.partition("=")
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = re.sub(r'&([&"])', r'\1', value[1:-1])
        if key.strip() == "data":
            directories.append(pathlib.Path(value))
        elif key.strip() == "content" and pathlib.Path(value).suffix.lower() in (
            ".esm", ".esp", ".omwaddon", ".omwgame"
        ):
            plugins.append(value)
    return directories, plugins


def scan(config):
    directories, plugins = load_config(config)
    effective = {tag: {} for tag in (b"ARMO", b"NPC_", b"LEVI", b"SCPT", b"INFO")}
    armor_history = collections.defaultdict(list)
    missing = []
    for plugin in plugins:
        path = next((root / plugin for root in reversed(directories)
                     if (root / plugin).is_file()), None)
        if path is None:
            missing.append(plugin)
            continue
        with path.open("rb") as stream:
            while header := stream.read(16):
                if len(header) != 16:
                    raise ValueError(f"Truncated record header: {path}")
                tag, size, _, flags = struct.unpack("<4sIII", header)
                if tag not in effective:
                    stream.seek(size, 1)
                    continue
                parts = list(subrecords(stream.read(size)))
                fields = dict(parts)
                if tag == b"SCPT":
                    ident = decode(fields.get(b"SCHD", b"")[:32]).lower()
                else:
                    ident = decode(fields.get(b"INAM" if tag == b"INFO" else b"NAME", b"")).lower()
                if not ident:
                    continue
                if tag == b"ARMO":
                    armor_history[ident].append(plugin)
                if flags & 0x20 or b"DELE" in fields:
                    effective[tag].pop(ident, None)
                else:
                    effective[tag][ident] = (plugin, parts)

    helmets = {}
    for ident, (plugin, parts) in effective[b"ARMO"].items():
        fields = dict(parts)
        data = fields.get(b"AODT", b"")
        if len(data) != 24:
            continue
        armor_type, weight, value, health, capacity, armor = struct.unpack("<IfIIII", data)
        if armor_type != 0:
            continue
        helmets[ident] = {
            "id": ident, "name": decode(fields.get(b"FNAM", b"")),
            "value": value, "script": decode(fields.get(b"SCRI", b"")),
            "enchantment": decode(fields.get(b"ENAM", b"")),
            "winning_plugin": plugin, "override_history": armor_history[ident],
            "npc_ids": [], "ordinary_npc_ids": [], "essential_npc_ids": [],
            "scripted_npc_ids": [], "leveled_lists": [], "references": [],
            "lua_references": [],
        }

    for npc_id, (plugin, parts) in effective[b"NPC_"].items():
        fields = dict(parts)
        flags = struct.unpack("<I", fields.get(b"FLAG", b"\0" * 4))[0]
        essential = bool(flags & 2)
        scripted = bool(decode(fields.get(b"SCRI", b"")))
        inventory_ids = {decode(data[4:36]).lower() for tag, data in parts
                         if tag == b"NPCO" and len(data) == 36
                         and struct.unpack_from("<i", data)[0] != 0}
        for ident in inventory_ids & helmets.keys():
            helmet = helmets[ident]
            helmet["npc_ids"].append(npc_id)
            if essential:
                helmet["essential_npc_ids"].append(npc_id)
            if scripted:
                helmet["scripted_npc_ids"].append(npc_id)
            if not essential and not scripted:
                helmet["ordinary_npc_ids"].append(npc_id)

    for list_id, (plugin, parts) in effective[b"LEVI"].items():
        item_id = None
        for tag, data in parts:
            if tag == b"INAM":
                item_id = decode(data).lower()
            elif tag == b"INTV" and item_id in helmets:
                helmets[item_id]["leveled_lists"].append({
                    "id": list_id, "level": struct.unpack("<H", data)[0], "plugin": plugin,
                })
                item_id = None

    # Scan explicit item IDs, not display names, to avoid incidental text matches.
    pattern = re.compile(r"(?<![a-z0-9_])(" + "|".join(
        re.escape(ident) for ident in sorted(helmets, key=len, reverse=True)
    ) + r")(?![a-z0-9_])", re.IGNORECASE)
    for tag in (b"SCPT", b"INFO"):
        for record_id, (plugin, parts) in effective[tag].items():
            field_tags = (b"SCTX",) if tag == b"SCPT" else (b"BNAM", b"SCVR")
            for field, data in parts:
                if field not in field_tags:
                    continue
                for line in decode(data).splitlines():
                    for ident in {match.group(0).lower() for match in pattern.finditer(line)}:
                        helmets[ident]["references"].append({
                            "kind": tag.decode(), "plugin": plugin, "record": record_id,
                            "field": field.decode(), "text": line.strip(),
                        })

    # Loose Lua in configured data roots: winning paths, including helper files.
    # This is deliberately broader than scripts proven reachable at runtime.
    lua_files = {}
    for root in directories:
        scripts = root / "scripts"
        if scripts.is_dir():
            for path in scripts.rglob("*"):
                if path.is_file() and path.suffix.lower() == ".lua":
                    lua_files[path.relative_to(root).as_posix().lower()] = path
    for path in lua_files.values():
        for number, line in enumerate(path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), 1):
            for ident in {match.group(0).lower() for match in pattern.finditer(line)}:
                helmets[ident]["lua_references"].append({
                    "path": str(path), "line": number, "text": line.strip(),
                })

    for helmet in helmets.values():
        helmet["npc_count"] = len(helmet["npc_ids"])
        helmet["ordinary_npc_count"] = len(helmet["ordinary_npc_ids"])
        helmet["leveled_list_count"] = len({entry["id"] for entry in helmet["leveled_lists"]})
        reasons = []
        if helmet["script"]:
            reasons.append("scripted item")
        if helmet["enchantment"]:
            reasons.append("already enchanted")
        if not 0 < helmet["value"] <= 150:
            reasons.append("outside 1-150 gold cap")
        if helmet["ordinary_npc_count"] < 5 and helmet["leveled_list_count"] == 0:
            reasons.append("insufficient common-use evidence")
        if helmet["references"]:
            reasons.append("explicit script/dialogue references need review")
        helmet["exclusion_reasons"] = reasons
        helmet["candidate"] = not reasons

    return {
        "config": str(config), "plugins_scanned": len(plugins) - len(missing),
        "missing_plugins": missing, "npc_records": len(effective[b"NPC_"]),
        "loose_lua_files_scanned": len(lua_files),
        "scripts_without_source": [ident for ident, (_, parts) in effective[b"SCPT"].items()
                                   if not dict(parts).get(b"SCTX")],
        "helmets": sorted(helmets.values(), key=lambda h: (-h["ordinary_npc_count"], h["id"])),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=pathlib.Path)
    parser.add_argument("output", type=pathlib.Path)
    args = parser.parse_args()
    result = scan(args.config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Scanned {result['plugins_scanned']} plugins, {result['npc_records']} NPC records; "
          f"missing {len(result['missing_plugins'])} plugins")
    for helmet in result["helmets"]:
        if helmet["candidate"] or (not helmet["script"] and not helmet["enchantment"]
                                   and 0 < helmet["value"] <= 150):
            print(f"{helmet['id']} | {helmet['name']} | value={helmet['value']} | "
                  f"NPCs={helmet['npc_count']} ordinary={helmet['ordinary_npc_count']} | "
                  f"lists={helmet['leveled_list_count']} | refs={len(helmet['references'])} | "
                  f"candidate={helmet['candidate']}")
