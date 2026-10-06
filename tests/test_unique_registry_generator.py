import pathlib
import io
import struct
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
from generate_unique_registry import physical_records, unique_name
from unique_designs import armor_class, compile_unique, conflict


def subrecord(tag, data):
    return tag + struct.pack("<I", len(data)) + data


def record(tag, ident, data_tag, data):
    body = subrecord(b"NAME", ident.encode() + b"\0") + subrecord(data_tag, data)
    return tag + struct.pack("<III", len(body), 0, 0) + body


class UniqueGeneratorTests(unittest.TestCase):
    def test_master_fields_and_enchantment_unit_conversion(self):
        data = record(b"ARMO", "armor", b"AODT", struct.pack("<IfIIII", 0, 5, 30, 100, 85, 10))
        data += record(b"CLOT", "clothing", b"CTDT", struct.pack("<IfHH", 8, 1, 120, 600))
        data += record(b"WEAP", "weapon", b"WPDT", struct.pack("<fIHHffH6BI", 20, 40, 1, 800, 1.35, 1, 20, 2, 13, 1, 18, 4, 16, 0))
        path = pathlib.Path("fixture.esm")
        with mock.patch.object(pathlib.Path, "open", return_value=io.BytesIO(data)):
            rows = physical_records(path)
        self.assertEqual(rows["armor"]["enchantCapacity"], 8.5)
        self.assertEqual(rows["clothing"]["enchantCapacity"], 60)
        self.assertEqual(rows["weapon"]["enchantCapacity"], 2)
        self.assertEqual(rows["weapon"]["slashMaxDamage"], 18)
        self.assertEqual(rows["armor"]["baseArmor"], 10)

    def test_final_weight_precedes_armor_skill_binding(self):
        item = dict(id="sample", category="armor", slot="boots")
        original = dict(weight=5, value=30, health=100, baseArmor=10, enchantCapacity=2)
        settings = {'iBootsWeight': 5, 'fLightMaxMod': 1, 'fMedMaxMod': 1.5}
        used = set()
        for ordinal in range(4):
            result = compile_unique(item, original, ordinal, settings, used)
            final = armor_class('boots', result['record']['weight'], settings)
            self.assertEqual(result['resolvedArmorClass'], final)
            for entry in result['effects']:
                if entry.get('armorClassBound'):
                    self.assertEqual(entry['skill'], final)
            self.assertIsNone(conflict(result['effects'], 'armor', 'boots'))

    def test_projectiles_have_no_equipped_effects_or_speed_scaling(self):
        item = dict(id="sample", category="weapon", slot="arrow")
        original = dict(weight=0.1, value=2, health=0, speed=1, reach=1, enchantCapacity=0,
                        chopMinDamage=0, chopMaxDamage=0, slashMinDamage=0,
                        slashMaxDamage=0, thrustMinDamage=1, thrustMaxDamage=5)
        for ordinal in range(4):
            result = compile_unique(item, original, ordinal, {}, set())
            self.assertFalse(result['effects'])
            self.assertEqual(result['record']["speed"], original["speed"])
            self.assertEqual(result['record']["chopMaxDamage"], 0)
            self.assertEqual(result['record']["health"], 0)

    def test_unique_internal_conflicts(self):
        self.assertIsNotNone(conflict([{'id': 'swiftswim'}, {'id': 'waterwalking'}], 'clothing', 'shoes'))
        self.assertIsNotNone(conflict([{'id': 'resistfire'}, {'id': 'weaknesstofire'}], 'armor', 'cuirass'))
        self.assertIsNone(conflict([{'id': 'swiftswim'}, {'id': 'waterbreathing'}], 'clothing', 'shoes'))

    def test_names_are_reproducible_and_handle_collisions(self):
        item = dict(id="sample", name="Common Ring")
        first = unique_name(item, 0, set())
        self.assertEqual(first, unique_name(item, 0, set()))
        self.assertNotEqual(first, unique_name(item, 0, {first}))


if __name__ == "__main__":
    unittest.main()
