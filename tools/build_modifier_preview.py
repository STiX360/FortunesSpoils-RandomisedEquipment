"""Export a standalone catalogue preview; does not run the mod or tests."""
import json
import pathlib
import re
from expanded_affix_data import families as expanded_families, tier_text
from weapon_affix_rules import MELEE_SLOTS, resolve_effects, variants, BINARY_EFFECTS
from catalogue_bases import bases, scope_rule, gap_rule

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNTIME = ROOT / 'mod/scripts/randomisedbasicloot'


def table_rows(path):
    section = ''
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('#'):
            section = line.lstrip('# ').strip()
        if line.startswith('|'):
            yield section, [c.strip() for c in line.strip('|').split('|')]


def plain(text):
    return text.replace('**', '').replace('`', '')


MODE_LABELS = {'ConstantEffect': 'Constant Effect', 'CastOnUse': 'When Used',
               'CastOnStrike': 'When Strikes'}


def delivery_variants(family, modes):
    labels = [MODE_LABELS[mode] for mode in modes]
    present = [labels[index] for index, cell in enumerate(family['tiers']) if cell != '-']
    yield dict(family, mode=' / '.join(dict.fromkeys(present)), tierModes=labels)


def weapon_variants(family):
    entries = family.get('weaponTiers')
    if not entries:
        yield family
        return
    sample = next(effects for _, effects in entries if effects)
    for profile in variants(sample, family.get('slots', MELEE_SLOTS)):
        cells = []
        for name, effects in entries:
            if not effects:
                cells.append('-')
                continue
            values = []
            for index, effect in enumerate(resolve_effects(effects, profile)):
                ident = effect['id']
                percent = ident.startswith(('resist', 'weakness')) or ident in ('blind', 'sound')
                rate = ident.startswith(('damage', 'disintegrate')) or ident in ('absorbhealth', 'absorbmagicka', 'absorbfatigue', 'poison', 'firedamage', 'frostdamage', 'shockdamage')
                value = 'Enabled' if ident in BINARY_EFFECTS else str(effect['magnitude']) + ('%' if percent else ' pts/sec' if rate else ' pts')
                value += f"; {effect.get('duration', 1)} sec"
                if len(effects) > 1:
                    value = ('benefit ' if index == 0 else 'cost ') + value
                values.append(value)
            target = '; on target; 3 ft area' if profile.get('range') == 'Target' else '; on touch; 0 ft area'
            cells.append(name + ' (' + '; '.join(values) + target + ')')
        mode = MODE_LABELS[profile.get('mode', 'CastOnStrike')]
        result = {key: value for key, value in family.items() if key != 'weaponTiers'}
        result.update(slots=profile['slots'], scope=profile['label'], tiers=cells,
                      mode=mode, tierModes=[mode]*6,
                      notes='Baseline note: ' + family['notes'] + ' Values above are resolved for ' + profile['label'] +
                      ('; staff delivery is on use, on target with a fixed 3-foot area' if profile.get('range') == 'Target' else '; delivery remains on strike, on touch') +
                      '. Unique templates are unchanged. Staff candidates require native on-target support.')
        yield result


def bargain_families():
    source = (RUNTIME / 'bargain_affixes.lua').read_text(encoding='utf-8')
    pattern = (r"\{ id = '([^']+)', names = \{([^}]+)\}, side = '([^']+)'(.*?),"
               r"\s*boon = \{([^}]+)\}, cost = \{([^}]+)\},"
               r"\s*benefits = \{([^}]+)\}, penalties = \{([^}]+)\} \}")
    labels = {'resistfrost': 'Resist Frost', 'resistshock': 'Resist Shock',
              'weaknesstofire': 'Weakness to Fire', 'weaknesstofrost': 'Weakness to Frost',
              'fortifyskill': 'Fortify', 'drainattribute': 'Drain',
              'fortifyattribute': 'Fortify', 'blind': 'Blind'}

    def effect(spec):
        fields = dict(re.findall(r"(\w+) = '([^']+)'", spec))
        label = labels[fields['id']]
        parameter = fields.get('skill') or fields.get('attribute')
        return label + (' ' + parameter.title() if parameter else '')

    def unit(spec):
        ident = dict(re.findall(r"(\w+) = '([^']+)'", spec))['id']
        return '%' if ident.startswith(('resist', 'weakness')) or ident == 'blind' else ' pts'

    matches = re.findall(pattern, source, re.S)
    declared = re.findall(r"\{ id = '([^']+)', names =", source)
    if len(matches) != len(declared) or not matches:
        raise ValueError('Bargain authoring format changed; update the catalogue exporter.')
    for ident, names, side, flags, boon, cost, benefits, penalties in matches:
        names = re.findall(r"'([^']+)'", names)
        benefits = [int(value.strip()) for value in benefits.split(',')]
        penalties = [int(value.strip()) for value in penalties.split(',')]
        if len(benefits) != 6 or len(penalties) != 6 or len(names) != 6 or len(set(names)) != 6:
            raise ValueError(f'{ident}: expected six distinct names and six benefit/penalty tiers')
        strike = 'strike = true' in flags
        yield dict(family=names[0], effect=f'{effect(boon)} / {effect(cost)}', side=side,
                   kind='Hybrid', runtimeId='bargain:' + ident,
                   rule=dict(category='weapon', slots=MELEE_SLOTS) if strike else
                        dict(category='clothing', slots=['amulet']) if ident == 'silver_tongue' else dict(wearable=True),
                   effectSpecs=[dict(re.findall(r"(\w+) = '([^']+)'", spec)) for spec in (boon, cost)],
                   scope='Amulets' if ident == 'silver_tongue' else 'Melee weapons' if strike else 'Armor and clothing, including jewelry',
                   notes=('Both effects affect the struck target for 3 seconds: a debuff helps the attacker, '
                          'while a buff strengthens the target.' if strike else
                          'Both effects apply to the wearer while equipped; attribute drains reverse on unequip.')
                         + ' Resist Magicka can reduce the debuff magnitude; listed values are before resistance.'
                         + (' The target buff is not reduced by Resist Magicka.' if strike else
                            ' Resistance is a gearing opportunity, not assumed when balancing the drawback.')
                         + ' One affix slot; requires bargainAffixes. Family weight x0.35 before biases.',
                   tiers=[f'{name} (benefit {benefit}{unit(boon)}; cost {penalty}{unit(cost)})'
                          for name, benefit, penalty in zip(names, benefits, penalties)],
                   weaponTiers=[(name, [dict(dict(re.findall(r"(\w+) = '([^']+)'", spec)), magnitude=value, duration=3, range='Touch')
                                       for spec, value in ((boon, benefit), (cost, penalty))])
                                for name, benefit, penalty in zip(names, benefits, penalties)] if strike else None,
                   mode='When Strikes' if strike else 'Constant Effect',
                   source='bargain_affixes.lua', special=False)


def build():
    families = []
    for section, cells in table_rows(ROOT / 'docs/reports/modifier-catalogue.md'):
        if len(cells) < 9 or not any('**' in c for c in cells[2:8]):
            continue
        families.append(dict(family=cells[0], effect=cells[1], side='prefix' if 'Prefix' in section else 'suffix',
                             kind='Magical', scope=plain(cells[8]), notes=plain(cells[9]) if len(cells) > 9 else '',
                             tiers=[plain(c) for c in cells[2:8]], mode='When Strikes' if 'Offensive' in section else 'Constant Effect',
                             source='modifier-catalogue.md', special='Special' in section,
                             runtimeId=cells[1], rule=scope_rule(cells[1], cells[8])))
        if 'Offensive' in section:
            entries = []
            for cell in cells[2:8]:
                match = re.search(r'\*\*([^*]+)\*\*\s*\((\d+)\s+pts?\s+for\s+(\d+)\s+sec', cell)
                entries.append((match[1], [dict(id=cells[1].lower().replace(' ', ''), magnitude=int(match[2]),
                                               duration=int(match[3]), range='Touch')]))
            families[-1]['weaponTiers'] = entries
            if cells[8] == 'Short blades, spears':
                families[-1]['slots'] = ['short_blade', 'spear']

    # Extract only literal authoring arrays, never evaluate gameplay Lua.
    loot = (RUNTIME / 'loot.lua').read_text(encoding='utf-8')
    physical_scopes = {
        'edge': 'Non-projectile weapons',
        'construction': 'Armor, including shields',
        'durability': 'Armor and non-projectile weapons',
        'lightwork': 'All equipment except projectiles', 'appraisal': 'All equipment except projectiles; appraisal setting required',
        'handling': 'Melee weapons, bows and crossbows', 'measure': 'Melee weapons',
        'receptivity': 'Armor, clothing and non-projectile weapons; positive base enchant capacity required',
    }
    fields = {'damage': 'Weapon damage', 'baseArmor': 'Base armor', 'health': 'Maximum condition',
              'weight': 'Item weight', 'value': 'Gold value', 'speed': 'Weapon speed',
              'reach': 'Weapon reach', 'enchantCapacity': 'Enchant capacity'}
    pattern = r"\{ id = '([^']+)', side = '([^']+)', field = '([^']+)'.*?values = \{([^}]+)\}, names = \{([^}]+)\}"
    for ident, side, field, values, names in re.findall(pattern, loot):
        values = [float(v.strip()) for v in values.split(',')]
        names = re.findall(r"'([^']+)'", names)
        families.append(dict(family=ident.replace('_', ' ').title(), effect=fields[field], side=side,
                             kind='Crafted', runtimeId=ident, field=field, scope=physical_scopes[ident],
                             notes='All six tiers are available on any eligible base.'
                             + (' Intentionally dead when combined with a native enchantment.' if ident == 'receptivity' else ''),
                             tiers=[f'{name} ({value * 100:+g}%)' for name, value in zip(names, values)],
                             mode='Record stat', source='loot.lua', special=False))

    projectile_source = (RUNTIME / 'projectile_loot.lua').read_text(encoding='utf-8')
    grades = re.findall(r"\{ name = '([^']+)', bonus = (\d+), weight = (\d+) \}", projectile_source)
    families.append(dict(family='Projectile Quality', effect='Projectile damage', side='prefix',
                         kind='Crafted', scope='Arrows, bolts and thrown weapons',
                         slots=['arrow', 'bolt', 'thrown'],
                         notes='One roll per original stack; fixed grades, not ordinary affix tiers. '
                               + ' / '.join(f'{name}: {weight}%' for name, _, weight in grades)
                               + '. No suffixes, uniques, enchantments, weight or value modifiers. '
                               + 'Bonuses apply to positive damage channels only, capped at 255. '
                               + 'Base value and weight are retained; records are reused per base and grade.',
                         tiers=[f'{name} (+{bonus} damage)' for name, bonus, _ in grades] + ['-']*3,
                         mode='Record stat', source='projectile_loot.lua', special=False))

    gap_rows = [c for _, c in table_rows(ROOT / 'docs/reports/gap-affix-implementation.md')
                if len(c) == 4 and re.match(r'^\d+ /', c[1])]
    gaps = (RUNTIME / 'gap_affixes.lua').read_text(encoding='utf-8')
    gap_pattern = r"\{ id = '([^']+)', effect = '([^']+)'(.*?), magnitudes = \{([^}]+)\},\s*names = \{([^}]+)\}"
    for row, match in zip(gap_rows, re.findall(gap_pattern, gaps, re.S)):
        ident, effect, flags, magnitudes, names = match
        names = re.findall(r"'([^']+)'", names)
        values = [v.strip() for v in magnitudes.split(',')]
        unit = ' native units' if ident == 'maxmagicka' else ' ft' if effect in ('detectkey', 'detectenchantment', 'telekinesis') else ' pts'
        block = re.search(r"\{ id = '" + re.escape(ident) + r"'(.*?)(?=\n    \{ id =|\n\})", gaps, re.S)[1]
        mode_array = re.search(r'modes = \{([^}]+)\}', block)
        duration_array = re.search(r'durations = \{([^}]+)\}', block)
        modes = re.findall(r"'([^']+)'", mode_array[1]) if mode_array else ['ConstantEffect'] * 6
        durations = [int(v.strip()) for v in duration_array[1].split(',')] if duration_array else [0] * 6
        cells = [f'{name} ({value}{unit}' + (f'; {duration} sec; on use' if duration else '; CE') + ')'
                 for name, value, duration in zip(names, values, durations)]
        families.extend(delivery_variants(dict(family=names[0], effect=row[0], side='suffix', kind='Magical', scope=row[2],
                             notes=row[3] + ('; requires advancedGapAffixes' if 'advanced = true' in flags else '')
                             + ('; class is resolved after all weight modifiers' if ident in ('heavyarmor', 'mediumarmor', 'lightarmor') else ''),
                             tiers=cells, source='gap_affixes.lua', special=False,
                             runtimeId=effect + ':' + ident, rule=gap_rule(ident)), modes))
    families.extend(bargain_families())
    for f in expanded_families():
        tiers = [tier_text(f, tier) for tier in range(1, 7)]
        notes = f"Requires expandedAffixes. Family weight x{f['weight']:.4g} before biases."
        if f.get('expansion'):
            notes += ' Requires loaded ' + f['expansion'].title() + ' and its enabled source switch.'
        if f.get('requiredCreatureGMST') or f.get('requiredItemGMSTs'):
            notes += ' Requires valid engine-mapped summon/bound records.'
        if f['mode'] == 'ConstantEffect' and f['effect'].startswith('restore'):
            notes += ' Points per second while equipped; stacks across equipment.'
        if f['binary']:
            notes += ' Binary effect: potency is not a magnitude roll.'
        modes = [f['tiers'].get(str(tier), {}).get('mode', f['mode']) for tier in range(1, 7)]
        families.extend(delivery_variants(dict(family=f['label'], effect=f['label'], side=f['side'],
                             kind='Magical', slots=f['slots'], scope=', '.join(s.replace('_', ' ') for s in f['slots']),
                             tiers=tiers, notes=notes, source='expanded_affix_data.py', special=False,
                             runtimeId=f['id'], rule=dict(slots=f['slots']),
                             effectSpecs=[dict(id=f['effect'], skill=f.get('skill'), attribute=f.get('attribute'))]), modes))
        if f['mode'] == 'CastOnStrike':
            families[-1]['weaponTiers'] = [
                (entry['name'], [dict(id=f['effect'], magnitude=entry['magnitude'], duration=entry['duration'], range=f['range'])])
                if (entry := f['tiers'].get(str(tier))) else ('', []) for tier in range(1, 7)]
    families = [variant for family in families for variant in weapon_variants(family)]
    template = (ROOT / 'site/modifier_preview.html').read_text(encoding='utf-8')
    payload = json.dumps(families, ensure_ascii=True).replace('<', '\\u003c')
    output = ROOT / 'build/site/index.html'
    output.parent.mkdir(parents=True, exist_ok=True)
    base_payload = json.dumps(bases(ROOT), ensure_ascii=True).replace('<', '\\u003c')
    output.write_text(template.replace('/*CATALOGUE_DATA*/[]', payload)
                      .replace('/*BASE_DATA*/[]', base_payload)
                      .replace('/*BASE_BROWSER*/', (ROOT / 'site/base_browser.js').read_text(encoding='utf-8')), encoding='utf-8')
    print(f'Exported {len(families)} modifier families to {output}')


if __name__ == '__main__':
    build()
