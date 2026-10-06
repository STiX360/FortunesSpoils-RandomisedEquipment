import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from catalogue_bases import bases
from build_loot_simulator import lua


class SimulatorTests(unittest.TestCase):
    def test_weapon_headers_are_classified(self):
        items = {b['id']: b for b in bases(ROOT)}
        self.assertEqual(items['iron arrow']['category'], 'weapon')
        self.assertEqual(items['iron dagger']['category'], 'weapon')
        self.assertEqual(items['iron_helmet']['category'], 'armor')
        self.assertEqual(items['common_shirt_01']['category'], 'clothing')

    def test_lua_literal_escaping(self):
        self.assertEqual(lua('a"b\n'), '"a\\"b\\n"')
        self.assertEqual(lua('\0'), '"\\000"')
        self.assertEqual(lua(False), 'false')
        self.assertEqual(lua([1, 2]), '{1,2}')
