"""Website-only base metadata from committed authoring inputs."""
import json
import re
from collections import defaultdict
from export_runtime_design import SLOTS, WEAPON_SKILLS


def scope_rule(effect, scope):
    if '`' in scope:
        return dict(baseIds=re.findall(r'`([^`]+)`', scope))
    if effect.startswith('Fortify ') and effect[8:] in WEAPON_SKILLS:
        return dict(category='weapon', slots=WEAPON_SKILLS[effect[8:]])
    if 'Melee weapons' in scope or scope == 'Short blades, spears':
        return dict(category='weapon', slots=['short_blade', 'spear'] if scope == 'Short blades, spears' else
                    [s for values in WEAPON_SKILLS.values() for s in values if s not in ('bow', 'crossbow')])
    if scope == 'Wearables':
        return dict(wearable=True)
    if scope == 'Clothing':
        return dict(category='clothing')
    return dict(wearable=True, allArmor='Armor' in scope,
                slots=sorted({s for token, slots in SLOTS.items() if token.lower() in scope.lower() for s in slots}))


def gap_rule(ident):
    jewelry = ['ring', 'amulet']
    gloves = ['left_glove', 'right_glove']
    body = ['shirt', 'pants', 'skirt', 'robe']
    mage = ['helmet', 'robe', *jewelry]
    slots = {
        'light': ['helmet', 'shield', *jewelry], 'slowfall': ['skirt', 'robe', 'amulet'],
        'swiftswim': ['boots', 'shoes', 'greaves', 'pants', *jewelry],
        'telekinesis': [*gloves, *jewelry], 'detectkey': ['helmet', *gloves, *jewelry],
        'detectenchantment': ['helmet', *jewelry], 'sanctuary': [*body, *jewelry],
        'blight': ['ring', 'amulet', 'belt'], 'fireshield': ['cuirass', 'shield', 'amulet'],
        'frostshield': ['cuirass', 'shield', 'amulet'], 'lightningshield': ['cuirass', 'shield', 'amulet'],
        'maxmagicka': mage, 'enchant': mage, 'alchemy': ['robe', 'amulet'],
        'unarmored': [*body, *gloves, 'shoes', *jewelry], 'block': ['shield'],
        'handtohand': [*gloves, 'left_gauntlet', 'right_gauntlet', 'left_bracer', 'right_bracer'],
    }
    if ident in ('heavyarmor', 'mediumarmor', 'lightarmor'):
        return dict(category='armor', armorSkill=True)
    if ident == 'attack':
        return dict(category='weapon', nonProjectile=True)
    rule = dict(slots=slots[ident])
    if ident in ('slowfall', 'telekinesis', 'sanctuary', 'unarmored', 'alchemy', 'blight'):
        rule['category'] = 'clothing'
    elif ident == 'block':
        rule['category'] = 'armor'
    else:
        rule['wearable'] = True
    return rule


def bases(root):
    registry = json.loads((root / 'data/loot-design.json').read_text(encoding='utf-8'))
    uniques = defaultdict(list)
    for entry in registry['uniqueTemplates']:
        if entry['slot'] not in ('arrow', 'bolt', 'thrown'):
            uniques[entry['baseId']].append({key: entry.get(key) for key in
                ('name', 'id', 'record', 'effects', 'mode', 'identity', 'drawbacks')})
    source = category = slot = None
    result = []
    for line in (root / 'docs/reports/included-items-report.md').read_text(encoding='utf-8').splitlines():
        if match := re.match(r'^## (.+) - \d+ Items', line):
            source = match[1]
        elif match := re.match(r'^### (Armor|Weapons?|Clothing) -', line):
            category = {'Armor': 'armor', 'Weapon': 'weapon', 'Weapons': 'weapon', 'Clothing': 'clothing'}[match[1]]
        elif match := re.match(r'^#### (.+) - \d+ Items', line):
            slot = match[1].lower().replace(' ', '_')
        elif source and line.startswith('|'):
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            if len(cells) == 3 and re.fullmatch(r'`[^`]+`', cells[1]) and cells[2].isdigit():
                ident = cells[1].strip('`')
                result.append(dict(id=ident, name=cells[0], source=source, category=category,
                                   slot=slot, value=int(cells[2]), uniques=uniques[ident]))
    return result
