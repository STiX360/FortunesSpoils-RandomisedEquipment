"""Compile distinct, purposeful unique recipes, rather than four repeated slot rolls."""

import hashlib
import itertools
import json
import math

ARMOR_SETTINGS = {
    'helmet': 'iHelmWeight', 'cuirass': 'iCuirassWeight', 'left_pauldron': 'iPauldronWeight',
    'right_pauldron': 'iPauldronWeight', 'greaves': 'iGreavesWeight', 'boots': 'iBootsWeight',
    'left_gauntlet': 'iGauntletWeight', 'right_gauntlet': 'iGauntletWeight', 'shield': 'iShieldWeight',
    'left_bracer': 'iGauntletWeight', 'right_bracer': 'iGauntletWeight',
}
ARMOR_SKILLS = {'lightarmor', 'mediumarmor', 'heavyarmor'}
PROJECTILES = {'arrow', 'bolt', 'thrown'}


def armor_class(slot, weight, settings):
    if weight <= 0:
        return None
    baseline = math.floor(settings[ARMOR_SETTINGS[slot]])
    if weight <= baseline * settings['fLightMaxMod'] + 0.0005:
        return 'lightarmor'
    if weight <= baseline * settings['fMedMaxMod'] + 0.0005:
        return 'mediumarmor'
    return 'heavyarmor'


def atom(ident, low, high, purpose, **parameters):
    return dict(id=ident, low=low, high=high, purpose=purpose, **parameters)


def skill(name, purpose):
    return atom('fortifyskill', 3, 7, purpose, skill=name)


def attribute(name, purpose):
    return atom('fortifyattribute', 2, 6, purpose, attribute=name)


def atoms_for(item, final_class):
    slot, category = item['slot'], item['category']
    jewelry = slot in ('ring', 'amulet')
    head = slot == 'helmet'
    feet = slot in ('boots', 'shoes')
    hands = slot in ('left_glove', 'right_glove', 'left_gauntlet', 'right_gauntlet', 'left_bracer', 'right_bracer')
    body = slot in ('robe', 'shirt', 'pants', 'skirt')
    atoms = [
        attribute('strength', 'carrying supplies and physical striking power'),
        attribute('endurance', 'fatigue-related endurance during extended excursions'),
        attribute('agility', 'combat steadiness and handling'),
        attribute('willpower', 'spell resistance and casting steadiness'),
        atom('fortifyfatigue', 8, 22, 'a larger fatigue reserve, not regeneration'),
        atom('feather', 8, 18, 'less effective encumbrance while equipped'),
        atom('resistfire', 8, 18, 'protection from fire hazards'),
        atom('resistfrost', 8, 18, 'protection from frost hazards'),
        atom('resistshock', 8, 18, 'protection from shock hazards'),
        atom('resistpoison', 10, 25, 'protection from poisonous enemies'),
        atom('resistblightdisease', 15, 35, 'protection during ashland expeditions'),
    ]
    if category == 'armor':
        atoms.append(atom('shield', 2, 5, 'magical defense independent of base armor'))
        if final_class:
            atoms.append(atom('fortifyskill', 3, 6, 'training for this final-weight armor class',
                              skill=final_class, armorClassBound=True))
    if feet or slot in ('pants', 'greaves', 'skirt') or jewelry:
        atoms += [attribute('speed', 'faster overland movement'), skill('athletics', 'sustained travel efficiency'),
                  atom('swiftswim', 15, 35, 'underwater travel speed'),
                  atom('waterwalking', 1, 1, 'crossing the surface of water'),
                  atom('waterbreathing', 1, 1, 'remaining underwater without drowning')]
    if feet or body:
        atoms += [atom('slowfall', 2, 6, 'controlled descents'), skill('acrobatics', 'jumping and fall proficiency')]
    if head or jewelry:
        atoms += [atom('light', 10, 25, 'illumination for exploration'), atom('nighteye', 10, 25, 'darkness visibility'),
                  atom('detectkey', 20, 60, 'finding hidden keys'),
                  atom('detectenchantment', 20, 60, 'finding enchanted objects')]
    if head or slot == 'robe' or jewelry:
        atoms += [attribute('intelligence', 'a mage or crafter attribute reserve'),
                  atom('fortifymagicka', 8, 18, 'extra flat spellcasting resource'),
                  atom('fortifymaximummagicka', 1, 3, 'Intelligence-scaled Magicka capacity'),
                  skill('enchant', 'native enchantment use and crafting efficiency'),
                  skill('alchemy', 'potion crafting proficiency')]
    if category == 'clothing' and (body or jewelry):
        atoms += [attribute('personality', 'social encounters'), skill('speechcraft', 'persuasion'),
                  skill('mercantile', 'trade negotiations'), atom('sanctuary', 3, 7, 'evasion in an unarmored build')]
    if category == 'clothing' and (body or jewelry or slot in ('shoes', 'left_glove', 'right_glove')):
        atoms.append(skill('unarmored', 'defense without native armor'))
    if hands or jewelry:
        atoms += [skill('security', 'lock work'), atom('telekinesis', 2, 6, 'remote interaction reach')]
    if slot == 'shield':
        atoms.append(skill('block', 'shield blocking proficiency'))
    if category == 'clothing' and slot in ('left_glove', 'right_glove'):
        atoms += [skill('handtohand', 'unarmed striking proficiency'), skill('sneak', 'quiet infiltration'),
                  skill('alchemy', 'handling alchemical ingredients')]
    if slot in ('cuirass', 'shield', 'amulet'):
        atoms += [atom('fireshield', 2, 5, 'a fire-themed magical ward'),
                  atom('frostshield', 2, 5, 'a frost-themed magical ward'),
                  atom('lightningshield', 2, 5, 'a shock-themed magical ward')]
    return atoms


def conflict(effects, category, slot):
    ids = {e['id'] for e in effects}
    skills = {e.get('skill') for e in effects}
    if 'swiftswim' in ids and ids & {'waterwalking', 'levitate'}:
        return 'swimming bonuses cannot serve their role during forced surface travel or levitation'
    if 'waterbreathing' in ids and ids & {'waterwalking', 'levitate'}:
        return 'underwater breathing is neutralized by a forced above-water travel mode'
    if 'light' in ids and (ids & {'nighteye', 'invisibility', 'chameleon'} or 'sneak' in skills):
        return 'light must not undermine stealth or duplicate the same visibility role'
    if 'handtohand' in skills and (category != 'clothing' or slot not in ('left_glove', 'right_glove')):
        return 'Hand-to-hand requires clothing gloves'
    if 'handtohand' in skills and 'block' in skills:
        return 'shield-dependent blocking is not part of an unarmed package'
    if category == 'armor' and 'unarmored' in skills:
        return 'Unarmored must not be assigned to native armor'
    if 'fortifymagicka' in ids and 'fortifymaximummagicka' in ids:
        return 'use one resource identity rather than two versions of extra Magicka'
    drained = {e.get('attribute') for e in effects if e['id'] == 'drainattribute'}
    if 'strength' in drained and 'feather' in ids:
        return 'encumbrance relief should not be offset by draining carrying capacity'
    if 'intelligence' in drained and ids & {'fortifymagicka', 'fortifymaximummagicka'}:
        return 'the Magicka specialty should not drain its scaling attribute'
    keys = [(e['id'], e.get('attribute'), e.get('skill')) for e in effects]
    if len(keys) != len(set(keys)):
        return 'duplicate spell-effect roles'
    for element, shield in (('fire', 'fireshield'), ('frost', 'frostshield'), ('shock', 'lightningshield'), ('poison', None)):
        if 'weaknessto' + element in ids and ('resist' + element in ids or shield in ids):
            return 'same-element protection and weakness offset one another'
    for entry in effects:
        if entry['id'] == 'drainattribute' and any(e['id'] == 'fortifyattribute' and e.get('attribute') == entry.get('attribute') for e in effects):
            return 'same-attribute bonus and penalty offset one another'
    return None


def costs_for(seed):
    costs = [dict(id='drainattribute', attribute=name, magnitude=2 + seed % 3,
                  purpose='reduced ' + name + ' while equipped')
             for name in ('intelligence', 'personality', 'strength', 'speed', 'willpower', 'endurance', 'agility')]
    costs += [dict(id='weaknessto' + element, magnitude=12 + seed % 14,
                   purpose='a real vulnerability to ' + element)
              for element in ('fire', 'frost', 'shock', 'poison')]
    start = seed % len(costs)
    return costs[start:] + costs[:start]


def signature(effects, category, slot):
    # Magnitude and name changes alone do not make a new functional recipe.
    return json.dumps(sorted((e['id'], e.get('attribute', ''), e.get('skill', '')) for e in effects), separators=(',', ':'))


def hash_number(text):
    return int(hashlib.sha256(text.encode()).hexdigest()[:16], 16)


def physical_roles(original, record, purposes):
    changed = {}
    for field, purpose in purposes.items():
        if field == 'damage':
            if any(record[key] != original[key] for key in record if key.endswith('Damage')):
                changed[field] = purpose
        elif record.get(field) != original.get(field):
            changed[field] = purpose
    return changed


def purposeful(ident, magnitude, purpose, **parameters):
    return dict(id=ident, magnitude=magnitude, purpose=purpose, **parameters)


BESPOKE = {
    'steel_cuirass_winters_sarcophagus': (
        'An immobile fortress of ice: retaliate with frost and regenerate, then unequip to act.',
        {},
        [purposeful('paralyze', 1, 'immobile ice prison while equipped; removed by unequipping', range='Self'),
         purposeful('frostshield', 100, 'extreme frost retaliation against attackers', range='Self'),
         purposeful('restorehealth', 5, 'recover health while enduring attacks in the ice prison', range='Self'),
         purposeful('restoremagicka', 3, 'replenish spellcasting reserves for use after leaving the prison', range='Self'),
         purposeful('restorefatigue', 10, 'restore stamina for combat after leaving the prison', range='Self')]),
    'iron_helmet_watchman': (
        'Night watch: see in darkness and find keys, at the expense of social presence.',
        dict(baseArmor=11, health=120, weight=3.5, value=150),
        [purposeful('nighteye', 20, 'keep watch in darkness'), purposeful('detectkey', 45, 'locate keys during patrols'),
         purposeful('fortifyattribute', 4, 'remain steady against hostile magic', attribute='willpower'),
         purposeful('drainattribute', 4, 'the social cost of a withdrawn watchman', attribute='personality')]),
    'iron_helmet_anvil': (
        'Heavy-armor conversion: an iron helmet reforged into a slow, durable heavy harness.',
        dict(baseArmor=18, health=400, weight=12, value=180),
        [purposeful('fortifyskill', 5, 'support the armor class created by the final weight', skill='heavyarmor', armorClassBound=True),
         purposeful('fortifyattribute', 5, 'fatigue endurance under a heavy harness', attribute='endurance'),
         purposeful('drainattribute', 10, 'pay for the harness with slower travel', attribute='speed')]),
    'iron_helmet_blindpilgrim': (
        'Blind traversal: extreme travel speed and safer descent, with genuinely impaired sight.',
        dict(baseArmor=6, health=60, weight=2, value=200),
        [purposeful('fortifyattribute', 20, 'rapid pilgrimage', attribute='speed'),
         purposeful('slowfall', 3, 'survive awkward descents'), purposeful('blind', 60, 'a real sight handicap; no counteracting vision spell')]),
    'iron_longsword_oath': (
        'A long-combat reserve for a battlemage who gives up diplomacy.',
        dict(slashMinDamage=2, slashMaxDamage=22, speed=1.35, health=1000, weight=18, value=190),
        [purposeful('fortifyfatigue', 25, 'sustain extended combat'),
         purposeful('fortifyattribute', 4, 'spell steadiness while wielding the blade', attribute='willpower'),
         purposeful('drainattribute', 5, 'a cost during dialogue while the weapon is equipped', attribute='personality')]),
    'iron_longsword_bitter': (
        'A precise, fast dueling edge that is expensive to keep repaired.',
        dict(slashMinDamage=2, slashMaxDamage=24, speed=1.55, health=90, weight=14, value=210),
        [purposeful('fortifyattack', 7, 'land deliberate dueling strikes'),
         purposeful('drainattribute', 5, 'reduce endurance in exchange for precision', attribute='endurance')]),
    'iron_longsword_doorbreaker': (
        'A heavy single-hit blade rather than a fast damage-per-second weapon.',
        dict(slashMinDamage=8, slashMaxDamage=28, speed=0.75, health=1200, weight=45, value=230),
        [purposeful('fortifyattribute', 6, 'power individual strikes', attribute='strength'),
         purposeful('fortifyskill', 5, 'handle this long blade', skill='longblade'),
         purposeful('drainattribute', 8, 'the separate overland-mobility cost', attribute='speed')]),
    'bear_cuirass_winterhide': (
        'Icewater expedition armor: frost protection and underwater breathing, not surface travel.',
        dict(baseArmor=18, health=450, weight=20, value=550),
        [purposeful('resistfrost', 20, 'survive cold hazards'), purposeful('waterbreathing', 1, 'remain beneath icy water'),
         purposeful('drainattribute', 4, 'reduced carrying and striking power', attribute='strength')]),
    'bear_cuirass_coldpromise': (
        'A frost specialist with a severe, different-element vulnerability.',
        dict(baseArmor=12, health=350, weight=16, value=600),
        [purposeful('resistfrost', 25, 'specialize against frost'), purposeful('weaknesstofire', 25, 'a genuine fire vulnerability'),
         purposeful('fortifyattribute', 5, 'fatigue endurance in prolonged cold expeditions', attribute='endurance')]),
    'bear_cuirass_sleeper': (
        'A huge fatigue reservoir in slow, low-protection but hard-wearing armor.',
        dict(baseArmor=6, health=1200, weight=40, value=550),
        [purposeful('fortifyfatigue', 60, 'a capacity reservoir, not regeneration'),
         purposeful('fortifyattribute', 7, 'fatigue endurance', attribute='endurance'),
         purposeful('drainattribute', 12, 'a large travel-speed cost', attribute='speed')]),
    'ruby_amulet_hearth': (
        'A conspicuous fire-warded lantern charm that leaves its wearer exposed to frost.',
        dict(weight=1, value=500),
        [purposeful('resistfire', 18, 'fire protection'), purposeful('light', 20, 'illumination rather than stealth'),
         purposeful('fortifyattribute', 5, 'spell steadiness', attribute='willpower'),
         purposeful('weaknesstofrost', 25, 'frost vulnerability; no frost ward to cancel it')]),
    'ruby_amulet_cinder': (
        'An alchemist working beside fire who must avoid lightning.',
        dict(weight=1, value=550),
        [purposeful('fortifyskill', 8, 'alchemy proficiency', skill='alchemy'),
         purposeful('fortifyattribute', 5, 'support potion crafting', attribute='intelligence'),
         purposeful('resistfire', 8, 'fire protection'), purposeful('weaknesstoshock', 15, 'a real shock vulnerability')]),
    'ruby_amulet_ashheart': (
        'An extreme fire-and-Magicka charm with frost exposure and poor endurance.',
        dict(weight=2, value=650),
        [purposeful('resistfire', 35, 'an extreme single-element specialty'),
         purposeful('fortifymaximummagicka', 3, 'Intelligence-scaled spellcasting reserve'),
         purposeful('weaknesstofrost', 35, 'a severe opposite-element cost'),
         purposeful('drainattribute', 6, 'reduced fatigue endurance, not drained Magicka scaling', attribute='endurance')]),
}


def compile_bespoke(template_id, item, original, settings, used_signatures):
    if template_id not in BESPOKE:
        return None
    identity, changes, authored = BESPOKE[template_id]
    record = dict(original, **changes)
    final_class = armor_class(item['slot'], record['weight'], settings) if item['category'] == 'armor' else None
    effects = [dict(e) for e in authored]
    for e in effects:
        if e.get('armorClassBound'):
            e['skill'] = final_class
    reason = conflict(effects, item['category'], item['slot'])
    if reason:
        raise ValueError(template_id + ': ' + reason)
    recipe = signature(effects, item['category'], item['slot'])
    if recipe in used_signatures:
        raise ValueError('Duplicate authored recipe: ' + template_id)
    used_signatures.add(recipe)
    costs = [e['purpose'] for e in effects if e['id'] in ('drainattribute', 'blind', 'paralyze') or e['id'].startswith('weakness')]
    return dict(record=record, effects=effects, mode='ConstantEffect', identity=identity, concept=identity,
                modifierPurposes=physical_roles(original, record, {field: identity for field in changes if field != 'value'}),
                drawbacks=costs, resolvedArmorClass=final_class, armorSkillPolicy='bind_after_final_weight',
                functionalRecipe=recipe, authoringStatus='individually_authored_draft_review_required')


def compile_unique(item, original, ordinal, settings, used_signatures):
    seed = hash_number(item['id'] + ':' + str(ordinal))
    category, slot = item['category'], item['slot']
    record = dict(original)
    weight_scale = (0.45 + seed % 36 / 100, 1.1 + seed % 36 / 100,
                    0.8 + seed % 21 / 100, 1.3 + seed % 46 / 100)[ordinal]
    record['weight'] = round(max(0.01, original['weight'] * weight_scale), 4)
    record['value'] = max(40, math.floor(original['value'] * 1.75 + 0.5) + 40)
    physical_purposes = {'weight': 'lighter travel equipment' if weight_scale < 1 else 'extra encumbrance paid for the specialty'}
    if category == 'armor':
        record['baseArmor'] = math.floor(original['baseArmor'] * (0.9, 1.2, 1.05, 0.75)[ordinal] + 0.5)
        record['health'] = math.floor(original['health'] * (0.8, 0.65, 1.35, 1.8)[ordinal] + 0.5)
        physical_purposes.update(baseArmor='the resolved protection tradeoff', health='the resolved durability tradeoff')
    elif category == 'weapon':
        # Projectile speed/reach/condition overrides do not invent unsupported mechanics.
        factors = (1.08, 1.35, 0.9, 1.15)
        for attack in ('chop', 'slash', 'thrust'):
            for bound in ('Min', 'Max'):
                key = attack + bound + 'Damage'
                record[key] = min(255, math.floor(original[key] * factors[ordinal] + 0.5))
        if slot not in PROJECTILES:
            record['speed'] = round(original['speed'] * (1.12, 0.8, 1.05, 0.95)[ordinal], 4)
            record['health'] = min(65535, math.floor(original['health'] * (0.7, 1.1, 1.5, 0.85)[ordinal] + 0.5))
            physical_purposes.update(speed='attack cadence traded against strike damage', health='repair burden or endurance')
        physical_purposes['damage'] = 'strike output traded against handling or carried weight'
    final_class = armor_class(slot, record['weight'], settings) if category == 'armor' else None
    if category == 'weapon' and slot in PROJECTILES:
        concepts = ('Trail Reserve', 'Siege Burden', 'Practice Quiver', 'Last Volley')
        return dict(record=record, effects=[], mode=None, concept=concepts[ordinal],
                    identity=f"{concepts[ordinal]}: physical ammunition specialization; limited native mechanics",
                    modifierPurposes=physical_roles(original, record, physical_purposes), drawbacks=['Damage/weight tradeoff; no invented projectile spells'],
                    authoringStatus='physical_ammunition_draft_limited_mechanics')
    if category == 'weapon' and slot not in ('bow', 'crossbow') and ordinal == 3:
        payloads = [atom('firedamage', 3, 8, 'fire damage delivered to the struck target'),
                    atom('frostdamage', 3, 8, 'frost damage delivered to the struck target'),
                    atom('shockdamage', 3, 8, 'shock damage delivered to the struck target'),
                    atom('poison', 2, 5, 'poison pressure on the struck target'),
                    atom('damagefatigue', 5, 12, 'wear down the enemy fatigue reserve'),
                    atom('blind', 8, 15, 'disrupt the enemy vision'),
                    atom('sound', 5, 12, 'disrupt enemy spellcasting')]
        for name in ('strength', 'agility', 'speed', 'willpower', 'endurance'):
            payloads.append(atom('drainattribute', 2, 5, 'temporarily reduce enemy ' + name, attribute=name))
        combinations = list(itertools.combinations(payloads, 4))
        for offset in range(len(combinations)):
            ingredients = combinations[(seed + offset) % len(combinations)]
            if not any(e['id'] in ('firedamage', 'frostdamage', 'shockdamage', 'poison', 'damagefatigue') for e in ingredients):
                continue
            effects = []
            for entry in ingredients:
                data = {k: v for k, v in entry.items() if k not in ('low', 'high')}
                data.update(magnitude=entry['low'] + seed % (entry['high'] - entry['low'] + 1),
                            duration=1 if entry['id'] in ('firedamage', 'frostdamage', 'shockdamage', 'poison', 'damagefatigue') else 3,
                            range='Touch', area=0)
                effects.append(data)
            recipe = 'CastOnStrike:' + signature(effects, category, slot)
            if recipe in used_signatures:
                continue
            used_signatures.add(recipe)
            roles = [e['purpose'] for e in effects]
            return dict(record=record, effects=effects, mode='CastOnStrike',
                        charge=120 + seed % 81, isAutocalc=True,
                        concept='Target disruption', identity='Charged strike package: ' + '; '.join(roles),
                        modifierPurposes=physical_roles(original, record, physical_purposes),
                        drawbacks=['Consumes enchantment charge; slower handling and repair burden'],
                        functionalRecipe=recipe, authoringStatus='distinct_recipe_draft_review_required')
        raise ValueError('No distinct charged recipe for ' + item['id'])
    if category == 'weapon':
        weapon_skill = {
            'short_blade': 'shortblade', 'long_blade_one_hand': 'longblade', 'long_blade_two_hand': 'longblade',
            'blunt_one_hand': 'bluntweapon', 'blunt_two_hand_close': 'bluntweapon', 'blunt_two_hand_wide': 'bluntweapon',
            'axe_one_hand': 'axe', 'axe_two_hand': 'axe', 'spear': 'spear', 'bow': 'marksman', 'crossbow': 'marksman',
        }[slot]
        choices = [skill(weapon_skill, 'proficiency with this exact weapon subtype'),
                   atom('fortifyattack', 2, 5, 'accuracy rather than raw damage'),
                   attribute('strength', 'physical striking power'), attribute('agility', 'combat handling'),
                   attribute('endurance', 'fatigue-related stamina'), attribute('willpower', 'casting and resistance support'),
                   atom('fortifyfatigue', 10, 20, 'fatigue reserve for extended combat'),
                   atom('feather', 8, 16, 'less effective equipment burden'),
                   atom('nighteye', 10, 25, 'fighting in darkness'),
                   atom('resistfire', 8, 16, 'fighting fire-using enemies'), atom('resistfrost', 8, 16, 'fighting frost-using enemies'),
                   atom('resistshock', 8, 16, 'fighting shock-using enemies'), atom('resistpoison', 10, 20, 'fighting poisonous enemies')]
    else:
        choices = atoms_for(item, final_class)
    combinations = list(itertools.combinations(choices, 3))
    start = seed % len(combinations)
    for offset in range(len(combinations)):
        ingredients = combinations[(start + offset) % len(combinations)]
        for cost in costs_for(seed):
            effects = []
            for index, ingredient in enumerate(ingredients):
                data = {k: v for k, v in ingredient.items() if k not in ('low', 'high')}
                data['magnitude'] = ingredient['low'] + ((seed >> (index * 5)) % (ingredient['high'] - ingredient['low'] + 1))
                effects.append(data)
            effects.append(dict(cost))
            recipe = signature(effects, category, slot)
            if conflict(effects, category, slot) or recipe in used_signatures:
                continue
            used_signatures.add(recipe)
            roles = [e['purpose'] for e in effects[:-1]]
            concept = ' / '.join(roles)
            return dict(record=record, effects=effects, mode='ConstantEffect', concept=concept,
                        identity='A specialist for ' + '; '.join(roles) + ', paid for with ' + cost['purpose'] + '.',
                        modifierPurposes=physical_roles(original, record, physical_purposes),
                        drawbacks=[cost['purpose'] + ' (' + str(cost['magnitude']) + ')'],
                        resolvedArmorClass=final_class, armorSkillPolicy='bind_after_final_weight',
                        functionalRecipe=recipe, authoringStatus='distinct_recipe_draft_review_required')
    raise ValueError('No distinct coherent recipe available for ' + item['id'])
