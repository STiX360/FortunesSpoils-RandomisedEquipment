import pathlib
import json
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
from base_item_pool import (
    BLOODMOON_ARMOR_IDS, BLOODMOON_CLOTHING_IDS, BLOODMOON_WEAPON_IDS, TRIBUNAL_ARMOR_IDS,
    TRIBUNAL_CLOTHING_IDS, TRIBUNAL_WEAPON_IDS,
    expand_list, included_items_report, select_bloodmoon_pool, select_pool, select_tribunal_pool,
    select_oaab_pool,
    protected_ids, select_approved_expansion,
)


def item(ident, category, slot, script="", enchantment="", value=30):
    return {"id": ident, "category": category, "slot": slot, "name": ident,
            "script": script, "enchantment": enchantment, "value": value}


class PoolTests(unittest.TestCase):
    def test_nested_normal_lists_and_clothing_without_runtime_cap(self):
        items = {
            "iron_helmet": item("iron_helmet", "armor", "helmet", value=1000),
            "iron_sword": item("iron_sword", "weapon", "long_blade_one_hand"),
            "common_shirt_01": item("common_shirt_01", "clothing", "shirt"),
            "common_glove_l_balmolagmer": item("common_glove_l_balmolagmer", "clothing", "left_glove"),
            "quest_ring": item("quest_ring", "clothing", "ring"),
        }
        lists = {"l_n_armor": ["nested"], "nested": ["iron_helmet", "iron_helmet"],
                 "l_n_wpn_melee": ["iron_sword"]}
        rows = select_pool(items, lists)
        self.assertEqual({r["id"] for r in rows}, {"iron_helmet", "iron_sword", "common_shirt_01"})
        self.assertEqual(len(rows), 3)

    def test_source_protections(self):
        items = {
            "normal": item("normal", "armor", "helmet"),
            "uniform": item("uniform", "armor", "cuirass", script="LegionUniform"),
            "quest": item("quest", "armor", "helmet", script="quest"),
            "enchanted": item("enchanted", "armor", "helmet", enchantment="magic"),
        }
        rows = select_pool(items, {"l_n_armor": list(items)})
        self.assertEqual({r["id"] for r in rows}, {"normal", "uniform"})

    def test_bad_nested_lists_fail_closed(self):
        with self.assertRaises(ValueError):
            expand_list("a", {"a": ["b"], "b": ["a"]}, {})
        with self.assertRaises(ValueError):
            expand_list("missing", {}, {})

    def test_report_groups_source_category_then_subcategory(self):
        report = included_items_report([item("iron_helmet", "armor", "helmet")])
        source = report.index("## Morrowind (Base Game) - 1 Items")
        category = report.index("### Armor - 1 Items", source)
        subtype = report.index("#### Helmet - 1 Items", category)
        row = report.index("| iron_helmet | `iron_helmet` | 30 |", subtype)
        self.assertLess(source, category)
        self.assertLess(category, subtype)
        self.assertLess(subtype, row)
        self.assertEqual(report.count("`iron_helmet`"), 1)
        self.assertIn("| Tribunal | 0 | 0 | 0 | 0 | Not included", report)

    def test_bloodmoon_is_exact_approved_list(self):
        items = {ident: item(ident, "armor", "helmet") for ident in BLOODMOON_ARMOR_IDS}
        items.update({ident: item(ident, "weapon", "axe_one_hand") for ident in BLOODMOON_WEAPON_IDS})
        items.update({ident: item(ident, "clothing", "shirt") for ident in BLOODMOON_CLOTHING_IDS})
        items["bm bear helmet eddard"] = item("bm bear helmet eddard", "armor", "helmet", enchantment="magic")
        items["bm ice dagger"] = item("bm ice dagger", "weapon", "short_blade")
        rows = select_bloodmoon_pool(items)
        self.assertEqual(len(rows), 66)
        expected = set(BLOODMOON_ARMOR_IDS + BLOODMOON_WEAPON_IDS + BLOODMOON_CLOTHING_IDS)
        self.assertEqual({row["id"] for row in rows}, expected)
        report = included_items_report([], rows)
        self.assertIn("| Bloodmoon | 28 | 16 | 22 | 66 | Included |", report)
        self.assertIn("## Bloodmoon - 66 Items", report)
        items[BLOODMOON_ARMOR_IDS[0]]["enchantment"] = "unexpected"
        with self.assertRaises(ValueError):
            select_bloodmoon_pool(items)

    def test_tribunal_is_exact_approved_pool_without_adamantium(self):
        items = {ident: item(ident, "armor", "helmet") for ident in TRIBUNAL_ARMOR_IDS}
        items.update({ident: item(ident, "weapon", "thrown") for ident in TRIBUNAL_WEAPON_IDS})
        items.update({ident: item(ident, "clothing", "shirt") for ident in TRIBUNAL_CLOTHING_IDS})
        items["royal_guard_helm"] = item("royal_guard_helm", "armor", "helmet")
        items["adamantium_axe"] = item("adamantium_axe", "weapon", "axe_one_hand")
        rows = select_tribunal_pool(items)
        expected = set(TRIBUNAL_ARMOR_IDS + TRIBUNAL_WEAPON_IDS + TRIBUNAL_CLOTHING_IDS)
        self.assertEqual({row["id"] for row in rows}, expected)
        self.assertEqual(len(rows), 26)
        self.assertIn("| Tribunal | 8 | 6 | 12 | 26 | Included |", included_items_report([], [], rows))

    def test_unique_suffix_is_excluded_from_base_and_expansion(self):
        items = {
            "iron_helmet": item("iron_helmet", "armor", "helmet"),
            "iron_helmet_unique": item("iron_helmet_unique", "armor", "helmet"),
        }
        rows = select_pool(items, {"l_n_armor": list(items)})
        self.assertEqual([row["id"] for row in rows], ["iron_helmet"])
        from base_item_pool import select_approved_expansion
        rows = select_approved_expansion(items, {"armor": tuple(items)})
        self.assertEqual([row["id"] for row in rows], ["iron_helmet"])

    def test_oaab_is_frozen_allowlist_not_all_plain_records(self):
        manifest = json.loads((pathlib.Path(__file__).resolve().parents[1] / "tools" /
                               "oaab_item_allowlist.json").read_text())
        items = {ident: item(ident, category, {"armor": "helmet", "weapon": "blunt_one_hand",
                                             "clothing": "ring"}[category])
                 for category, ids in manifest["items"].items() for ident in ids}
        items["ab_a_impbmcuirass"]["script"] = "LegionUniform"
        for ident in ("ab_a_invisshield", "ab_a_glassassassinpauldronleft", "new_plain_record",
                      "future_unique", "ab_w_silverscepterchastening", "ab_w_silversceptershock"):
            items[ident] = item(ident, "weapon", "blunt_one_hand")
        rows = select_oaab_pool(items)
        ids = {row["id"] for row in rows}
        self.assertEqual(len(rows), 307)
        self.assertIn("ab_w_silverscepter", ids)
        self.assertEqual(ids, {ident for entries in manifest["items"].values() for ident in entries})
        report = included_items_report([], oaab_rows=rows)
        self.assertIn("| OAAB Data | 123 | 164 | 20 | 307 | Included |", report)
        self.assertEqual(report.count("`ab_w_silverscepter`"), 1)
        self.assertFalse(any(ident.endswith("_unique") for ident in ids))
        for field in ("script", "enchantment"):
            items["ab_w_silverscepter"][field] = "unexpected"
            with self.assertRaises(ValueError):
                select_oaab_pool(items)
            items["ab_w_silverscepter"][field] = ""
        del items["ab_w_silverscepter"]
        with self.assertRaises(ValueError):
            select_oaab_pool(items)

    def test_protected_ids_are_excluded_even_without_scripts_or_magic(self):
        ids = ("bonemold_founders_helm", "daedric_pauldron_right", "keening")
        self.assertTrue(set(ids).issubset(protected_ids()))
        items = {ident: item(ident, "armor", "helmet") for ident in ids}
        items["iron_helmet"] = item("iron_helmet", "armor", "helmet")
        for rows in (select_pool(items, {"l_n_armor": list(items)}),
                     select_approved_expansion(items, {"armor": tuple(items)})):
            self.assertEqual([row["id"] for row in rows], ["iron_helmet"])

    def test_protected_manifest_has_explicit_lowercase_ids(self):
        ids = protected_ids()
        self.assertEqual(len(ids), 306)
        self.assertTrue(all(ident == ident.lower() and ident.strip() == ident for ident in ids))
        self.assertNotIn("iron_helmet", ids)
        self.assertNotIn("extravagant_amulet_02", ids)
        self.assertIn("common_glove_l_balmolagmer", ids)
        self.assertIn("common_glove_r_balmolagmer", ids)
        self.assertIn("gauntlet _horny_fist_l", ids)


if __name__ == "__main__":
    unittest.main()
