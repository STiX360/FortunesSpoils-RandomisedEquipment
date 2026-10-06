import importlib.util
import pathlib
import struct
import tempfile
import unittest


spec = importlib.util.spec_from_file_location(
    "audit", pathlib.Path(__file__).resolve().parents[1] / "tools/audit_helmets.py"
)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def record(tag, *fields):
    payload = b"".join(key + struct.pack("<I", len(value)) + value for key, value in fields)
    return struct.pack("<4sIII", tag, len(payload), 0, 0) + payload


def name(value):
    return value.encode() + b"\0"


def helmet(ident, *extra):
    return record(b"ARMO", (b"NAME", name(ident)), (b"FNAM", name(ident)),
                  (b"AODT", struct.pack("<IfIIII", 0, 2, 25, 100, 5, 3)), *extra)


def npc(ident, item, flags=0, *extra):
    return record(b"NPC_", (b"NAME", name(ident)), (b"FLAG", struct.pack("<I", flags)),
                  (b"NPCO", struct.pack("<i32s", 1, item.encode())), *extra)


class AuditTests(unittest.TestCase):
    def test_winners_inventory_and_references(self):
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).resolve().parent) as tmp:
            root = pathlib.Path(tmp)
            data = root / "Data & More"
            data.mkdir()
            (data / "base.esm").write_bytes(
                helmet("common_helm") + helmet("uniform_helm") + helmet("deleted_helm")
                + npc("ordinary", "common_helm") + npc("essential", "common_helm", 2)
                + npc("scripted", "common_helm", 0, (b"SCRI", name("quest")))
                + npc("overridden", "common_helm")
                + record(b"LEVI", (b"NAME", name("generic_loot")),
                         (b"INAM", name("common_helm")), (b"INTV", struct.pack("<H", 3)),
                         (b"INAM", name("common_helm")), (b"INTV", struct.pack("<H", 4)))
                + record(b"SCPT", (b"SCHD", b"quest".ljust(52, b"\0")),
                         (b"SCTX", b'Player->GetItemCount "common_helm"\n'))
                + record(b"INFO", (b"INAM", name("dialogue1")),
                         (b"BNAM", b'Player->RemoveItem "common_helm" 1'))
            )
            (data / "patch.esp").write_bytes(
                helmet("uniform_helm", (b"SCRI", name("legionuniform")))
                + record(b"ARMO", (b"NAME", name("deleted_helm")), (b"DELE", b"\0" * 4))
                + npc("overridden", "uniform_helm")
            )
            scripts = data / "scripts"
            scripts.mkdir()
            (scripts / "check.lua").write_text('local id = "common_helm"\n')
            config = root / "openmw.cfg"
            quoted_path = str(data).replace("&", "&&")
            config.write_text(f'data="{quoted_path}"\ncontent=base.esm\ncontent=patch.esp\n')
            result = audit.scan(config)
            helmets = {h["id"]: h for h in result["helmets"]}
            self.assertEqual(result["missing_plugins"], [])
            self.assertNotIn("deleted_helm", helmets)
            common = helmets["common_helm"]
            self.assertEqual(common["npc_count"], 3)
            self.assertEqual(common["ordinary_npc_count"], 1)
            self.assertEqual(common["leveled_list_count"], 1)
            self.assertEqual(len(common["references"]), 2)
            self.assertEqual(len(common["lua_references"]), 1)
            self.assertFalse(common["candidate"])
            self.assertEqual(helmets["uniform_helm"]["script"], "legionuniform")
            self.assertEqual(helmets["uniform_helm"]["npc_ids"], ["overridden"])

    def test_truncated_subrecords_fail(self):
        with self.assertRaises(ValueError):
            list(audit.subrecords(b"NAME" + struct.pack("<I", 100) + b"x"))


if __name__ == "__main__":
    unittest.main()
