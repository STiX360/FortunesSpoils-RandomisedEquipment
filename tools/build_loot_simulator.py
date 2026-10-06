"""Bundle the actual Lua loot rules into an offline static simulator."""
import json
import pathlib
import re
import shutil
from catalogue_bases import bases

ROOT = pathlib.Path(__file__).resolve().parents[1]


def lua(value):
    if value is None:
        return 'nil'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str):
        return re.sub(r'\\u00([0-9a-f]{2})', lambda m: '\\%03d' % int(m[1], 16),
                      json.dumps(value, ensure_ascii=False))
    if isinstance(value, list):
        return '{' + ','.join(lua(v) for v in value) + '}'
    return '{' + ','.join('[' + lua(k) + ']=' + lua(v) for k, v in value.items()) + '}'


def build():
    snapshot = json.loads((ROOT / 'data/simulator-snapshot.json').read_text(encoding='utf-8'))
    base_data = [b for b in bases(ROOT) if b['id'] in snapshot['records']]
    templates = json.loads((ROOT / 'data/loot-design.json').read_text(encoding='utf-8'))['uniqueTemplates']
    for b in base_data:
        b['record'] = snapshot['records'][b['id']]
        b['uniques'] = [u for u in templates if u['baseId'] == b['id']]
    modules = ['config', 'item_rules', 'gap_affixes', 'magic_catalogue', 'expanded_catalogue',
               'effect_availability', 'bargain_affixes', 'regional_flavor', 'weapon_affix_policy',
               'weapon_affixes', 'projectile_loot', 'tier_progression', 'loot']
    bootstrap = ['simSnapshot=' + lua(snapshot), 'simBases=' + lua({b['id']: b for b in base_data})]
    for name in modules:
        source = (ROOT / 'mod/scripts/randomisedbasicloot' / (name + '.lua')).read_text(encoding='utf-8')
        bootstrap.append("package.preload['scripts.randomisedbasicloot." + name + "']=function()\n" + source + '\nend')
    bootstrap.append((ROOT / 'site/loot_simulator.lua').read_text(encoding='utf-8'))
    images = json.loads((ROOT / 'data/item-images.json').read_text(encoding='utf-8'))
    for b in base_data:
        b['image'] = images.get(b['id'])
    out = ROOT / 'build/site'
    out.mkdir(parents=True, exist_ok=True)
    template = (ROOT / 'site/loot_simulator.html').read_text(encoding='utf-8')
    payload = json.dumps(base_data, ensure_ascii=True).replace('<', '\\u003c')
    code = json.dumps('\n'.join(bootstrap), ensure_ascii=True).replace('<', '\\u003c')
    template = template.replace('/*SIM_BASES*/[]', payload).replace('/*SIM_LUA*/""', code)
    template = template.replace('/*SIM_JS*/', (ROOT / 'site/loot_simulator.js').read_text(encoding='utf-8'))
    regional = (ROOT / 'mod/scripts/randomisedbasicloot/regional_flavor.lua').read_text(encoding='utf-8')
    interiors = re.findall(r"'([^']+)'", re.search(r'local dwemer = \{(.*?)\}', regional, re.S)[1])
    regions = re.findall(r"\['((?:\\.|[^'])*)'\] =", re.search(r'local regions = \{(.*?)\n\}', regional, re.S)[1])
    locations = [dict(label='Neutral / unmapped', region='', interior='')]
    locations += [dict(label=r.replace("\\'", "'").title() + ' / exterior', region=r.replace("\\'", "'"), interior='') for r in regions]
    locations += [dict(label=r + ' / interior', region='', interior=r) for r in interiors]
    template = template.replace('/*SIM_LOCATIONS*/[]', json.dumps(locations))
    template = template.replace('/*SIM_EFFECT_LABELS*/{}', json.dumps({k: v['label'] for k, v in snapshot['effects'].items()}))
    (out / 'simulator.html').write_text(template, encoding='utf-8')
    shutil.copytree(ROOT / 'site/vendor', out / 'vendor', dirs_exist_ok=True)
    print(f'Bundled Lua loot simulator with {len(base_data)} source bases')


if __name__ == '__main__':
    build()
