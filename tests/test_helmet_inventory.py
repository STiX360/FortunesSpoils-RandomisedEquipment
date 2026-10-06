import copy
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
from helmet_inventory import passed_checks


class FilterTests(unittest.TestCase):
    def setUp(self):
        self.source = {"script": "", "enchantment": "", "value": 40}
        self.current = dict(self.source, references=[], lua_references=[],
                            ordinary_npc_count=2, leveled_list_count=1)

    def test_plain_common_record_passes(self):
        self.assertTrue(passed_checks(self.source, self.current))

    def test_rejects_each_protection_flag_and_missing_record(self):
        self.assertFalse(passed_checks(self.source, None))
        for key, value in (("script", "quest_script"), ("enchantment", "ench"), ("value", 151)):
            for which in ("source", "current"):
                with self.subTest(key=key, which=which):
                    source, current = copy.deepcopy(self.source), copy.deepcopy(self.current)
                    (source if which == "source" else current)[key] = value
                    self.assertFalse(passed_checks(source, current))

    def test_uncommon_and_script_references_fail(self):
        self.current["leveled_list_count"] = 0
        self.assertFalse(passed_checks(self.source, self.current))
        self.current["ordinary_npc_count"] = 5
        self.assertTrue(passed_checks(self.source, self.current))
        self.current["references"] = [{"text": "GetItemCount"}]
        self.assertFalse(passed_checks(self.source, self.current))

    def test_reviewed_catalog_hit_passes_but_unknown_dependency_fails(self):
        self.current["lua_references"] = [{
            "path": "C:/mods/Fresh Loot/scripts/fresh-loot/item-lists/ids.lua",
            "text": '"bm bear helmet",',
        }]
        self.assertTrue(passed_checks(self.source, self.current))
        self.current["lua_references"].append({
            "path": "C:/mods/Quest/scripts/quest.lua", "text": 'check("bm bear helmet")',
        })
        self.assertFalse(passed_checks(self.source, self.current))

    def test_uniform_exception_and_specific_accepted_vampire_reference(self):
        self.current["script"] = "LegionUniform"
        self.current["references"] = [{
            "record": "IsVampireHiddenHelmet", "plugin": "Melodies and Moonlight.esp",
        }]
        self.assertTrue(passed_checks(self.source, self.current))
        self.current["references"].append({"record": "quest_check", "plugin": "Quest.esp"})
        self.assertFalse(passed_checks(self.source, self.current))

    def test_reviewed_comment_and_conversion_sample_pass(self):
        self.current["lua_references"] = [
            {"path": "C:/mods/SD/scripts/SunsDusk/player_modules/p_clean.lua",
             "text": "-- iron_helmet, steel_helm"},
            {"path": "C:/mods/CF/scripts/CraftingFramework/parsers/convertTsvToLua.lua",
             "text": "iron_helmet\tIron Helmet\t5\t30"},
        ]
        self.assertTrue(passed_checks(self.source, self.current))
        self.current["lua_references"][0]["text"] = 'check("iron_helmet")'
        self.assertFalse(passed_checks(self.source, self.current))

    def test_trusted_normal_policy_ignores_refs_and_review_value_cap(self):
        self.source["value"] = self.current["value"] = 2250
        self.current["references"] = [{"record": "quest", "plugin": "Quest.esp"}]
        self.assertFalse(passed_checks(self.source, self.current))
        self.assertTrue(passed_checks(self.source, self.current, trusted_normal=True))
        self.current["script"] = "unknown_script"
        self.assertFalse(passed_checks(self.source, self.current, trusted_normal=True))


if __name__ == "__main__":
    unittest.main()
