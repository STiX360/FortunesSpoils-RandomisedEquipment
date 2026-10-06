import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'tools'))
from weapon_affix_rules import DAMAGE_EFFECTS, PROFILES, resolve_effects
from expanded_affix_data import families


class WeaponAffixRulesTests(unittest.TestCase):
    def test_direct_damage_speed_curve(self):
        for ident in DAMAGE_EFFECTS:
            effects = [dict(id=ident, magnitude=15, duration=1)]
            for speed, expected in ((1.5, 11), (1, 15), (.75, 20), (.01, 23), (100, 11)):
                with self.subTest(effect=ident, speed=speed):
                    result = resolve_effects(effects, PROFILES[0], speed)
                    self.assertEqual(result[0]['magnitude'], expected)
                    self.assertEqual(result[0]['duration'], 1)
                    self.assertEqual(effects[0]['magnitude'], 15)

    def test_invalid_speed_falls_back(self):
        effect = [dict(id='firedamage', magnitude=15, duration=1)]
        for speed in (0, -1, float('nan'), float('inf')):
            self.assertEqual(resolve_effects(effect, PROFILES[0], speed)[0]['magnitude'], 15)

    def test_staff_scaling_is_separate(self):
        result = resolve_effects([dict(id='firedamage', magnitude=15, duration=1)], PROFILES[-1], .75)[0]
        self.assertEqual((result['magnitude'], result['range'], result['area']), (23, 'Target', 3))

    def test_non_damage_effects_not_scaled_by_speed(self):
        for ident in ('absorbhealth', 'drainhealth', 'disintegratearmor', 'weaknesstofire'):
            effect = dict(id=ident, magnitude=10, duration=1)
            self.assertEqual(resolve_effects([effect], PROFILES[0], 1.5)[0]['magnitude'], 10)

    def test_expanded_resistance_slots(self):
        selected = [f for f in families() if f['effect'] in ('resistmagicka', 'resistparalysis')]
        self.assertEqual(len(selected), 2)
        for family in selected:
            self.assertEqual(set(family['slots']), {'ring', 'amulet', 'belt'})
            self.assertEqual(family['side'], 'suffix')

    def test_belts_have_no_cures_or_restores(self):
        for family in families():
            if family['effect'].startswith(('cure', 'restore')):
                self.assertNotIn('belt', family['slots'])


if __name__ == '__main__':
    unittest.main()
