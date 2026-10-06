import collections
import json
import math
import pathlib
import re
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from base_item_pool import protected_ids
from generate_unique_registry import format_effect
from unique_designs import conflict


class LootDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.design = json.loads((ROOT / "data/loot-design.json").read_text())

    def test_draft_is_not_presented_as_runtime_configuration(self):
        self.assertEqual(self.design["status"], "design_draft_not_loaded_by_gameplay")

    def test_probability_weights(self):
        loot = self.design["loot"]
        self.assertTrue(0 <= loot["uniqueChance"] <= 1)
        weights = loot["affixLayoutWeights"]
        self.assertEqual(set(weights), {"prefix", "suffix", "both"})
        self.assertTrue(all(v >= 0 for v in weights.values()))
        self.assertGreater(sum(weights.values()), 0)
        self.assertEqual(list(weights.values()), [1, 1, 2])
        unique = loot["uniqueChance"]
        ordinary = (1 - unique) * loot["dropChance"]
        self.assertAlmostEqual(unique, 0.01)
        self.assertAlmostEqual((1 - unique) * (1 - loot["dropChance"]), 0.33)
        self.assertAlmostEqual(ordinary * (weights["prefix"] + weights["suffix"]) / sum(weights.values()), 0.33)
        self.assertAlmostEqual(ordinary * weights["both"] / sum(weights.values()), 0.33)
        self.assertAlmostEqual(sum(self.design["tiers"]["weights"]), 100)
        self.assertEqual(len(self.design["tiers"]["weights"]), 6)

    def test_capacity_pairs_allow_intentional_dead_affixes(self):
        self.assertEqual(self.design["composition"]["enchantCapacityWithNativeEnchantmentPolicy"],
                         "allow_intentional_dead_affix")

    def test_unique_coverage_and_identity(self):
        self.assertEqual({k: self.design["uniqueAuthoring"][k] for k in ('coverageKey', 'targetMinimumPerBase', 'targetMaximumPerBase')}, {
            "coverageKey": "exact_base_record_id",
            "targetMinimumPerBase": 3, "targetMaximumPerBase": 5,
        })
        templates = self.design["uniqueTemplates"]
        self.assertEqual(len(templates), 3001)
        self.assertEqual(len({v["id"] for v in templates}), len(templates))
        self.assertEqual(len({v["name"] for v in templates}), len(templates))
        counts = collections.Counter(v["baseId"] for v in templates)
        self.assertEqual(len(counts), 750)
        self.assertEqual(set(counts.values()), {4, 5})
        self.assertEqual(counts['steel_cuirass'], 5)
        self.assertEqual({base for base, count in counts.items() if count == 5}, {'steel_cuirass'})
        for base in ("iron_helmet", "iron longsword", "bm bear cuirass", "extravagant_amulet_02"):
            self.assertEqual(counts[base], 4)
        pool = (ROOT / "docs/reports/included-items-report.md").read_text()
        approved = set(re.findall(r"^\| [^|]+ \| `([^`]+)` \| \d+ \|$", pool, re.MULTILINE))
        self.assertEqual(set(counts), approved)
        self.assertFalse(set(counts) & protected_ids())
        for base in counts:
            self.assertIn("`" + base + "`", pool)
        register = (ROOT / "docs/reports/unique-item-registry.md").read_text()
        for template in templates:
            self.assertIn("`" + template["id"] + "`", register)
            self.assertIn(template["name"], register)
            for entry in template["effects"]:
                self.assertTrue(format_effect(entry) in register,
                                template['id'] + ': missing documented effect ' + format_effect(entry))
        self.assertEqual(collections.Counter(t["source"] for t in templates), {
            "Morrowind (Base Game)": 1405, "Tribunal": 104,
            "Bloodmoon": 264, "OAAB Data": 1228,
        })

    def test_unique_record_fields_and_effect_ids(self):
        effects = {
            "nighteye", "fortifyattribute", "blind", "resistfrost",
            "weaknesstofire", "fortifyfatigue", "resistfire",
            "fortifymagicka", "drainattribute", "weaknesstofrost", "resistshock",
            "fortifyskill", "feather",
            "shield", "light", "slowfall", "swiftswim", "telekinesis", "detectkey", "detectenchantment",
            "sanctuary", "resistblightdisease", "fireshield", "frostshield", "lightningshield",
            "fortifyattack", "fortifymaximummagicka",
            "resistpoison", "waterwalking", "waterbreathing", "weaknesstoshock", "weaknesstopoison",
            "firedamage", "frostdamage", "shockdamage", "poison", "damagefatigue", "sound",
            "paralyze", "restorehealth", "restoremagicka", "restorefatigue",
        }
        for template in self.design["uniqueTemplates"]:
            self.assertGreater(template["weight"], 0)
            record = template["record"]
            for value in record.values():
                self.assertTrue(math.isfinite(value) and value >= 0)
            self.assertGreater(record["weight"], 0)
            for attack in ("chop", "slash", "thrust"):
                if attack + "MinDamage" in record:
                    self.assertLessEqual(record[attack + "MinDamage"], record[attack + "MaxDamage"])
            for effect in template["effects"]:
                self.assertIn(effect["id"], effects)
                self.assertGreater(effect["magnitude"], 0)
                if effect["id"] in {"fortifyattribute", "drainattribute"}:
                    self.assertIn(effect["attribute"], {"strength", "speed", "endurance", "willpower", "agility", "personality", "intelligence"})
            if template["effects"]:
                self.assertIn(template["mode"], ("ConstantEffect", "CastOnStrike"))
                self.assertIsNone(conflict(template['effects'], template['category'], template['slot']))

    def test_new_unique_coverage_and_context(self):
        all_effects = {e['id'] for t in self.design['uniqueTemplates'] for e in t['effects']}
        self.assertTrue({'light', 'slowfall', 'swiftswim', 'telekinesis', 'detectkey',
                         'detectenchantment', 'sanctuary', 'resistblightdisease', 'fireshield',
                         'frostshield', 'lightningshield', 'fortifyattack', 'fortifymaximummagicka'} <= all_effects)
        skills = {e['skill'] for t in self.design['uniqueTemplates'] for e in t['effects'] if 'skill' in e}
        self.assertTrue({'heavyarmor', 'mediumarmor', 'lightarmor', 'unarmored', 'block',
                         'handtohand', 'enchant', 'alchemy'} <= skills)
        for template in self.design['uniqueTemplates']:
            for entry in template['effects']:
                if entry.get('skill') == 'handtohand':
                    self.assertEqual(template['category'], 'clothing')
                    self.assertIn(template['slot'], ('left_glove', 'right_glove'))
            if template['category'] == 'weapon' and template['slot'] in ('arrow', 'bolt', 'thrown'):
                self.assertFalse(template['effects'])
            if template['category'] == 'armor':
                self.assertGreaterEqual(len(template['effects']), 2)

    def test_distinct_non_ammunition_recipes_have_purposes(self):
        recipes = []
        for template in self.design['uniqueTemplates']:
            if template['category'] == 'weapon' and template['slot'] in ('arrow', 'bolt', 'thrown'):
                continue
            recipes.append(template['functionalRecipe'])
            self.assertTrue(template['identity'])
            for entry in template['effects']:
                self.assertTrue(entry['purpose'])
        self.assertEqual(len(recipes), len(set(recipes)))

    def test_peak_weapon_throughput_proxy_exceeds_unique_examples(self):
        peak = math.floor(18 * 1.35 + 0.5) * (1.35 * 1.2)
        for template in self.design["uniqueTemplates"]:
            if template["baseId"] == "iron longsword":
                record = template["record"]
                self.assertGreater(peak, record["slashMaxDamage"] * record["speed"])

    def test_design_markdown_table_columns(self):
        for name in ("loot-generation-design.md", "modifier-catalogue.md", "vanilla-enchantment-review.md", "unique-item-registry.md", "item-metadata-design.md", "effect-coverage-review.md", "gap-affix-implementation.md"):
            rows = (ROOT / "docs/reports" / name).read_text(encoding='utf-8').splitlines()
            width = None
            for row in rows:
                if row.startswith("|"):
                    columns = row.count("|") - 1
                    if width is None:
                        width = columns
                    self.assertEqual(columns, width, name + ": " + row)
                else:
                    width = None


if __name__ == "__main__":
    unittest.main()
