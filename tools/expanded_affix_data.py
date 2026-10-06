"""Authoring definitions shared by runtime export and the static catalogue."""

MAGE = ['robe', 'amulet']
HANDS = ['left_glove', 'right_glove', 'ring']
MELEE = ['short_blade', 'long_blade_one_hand', 'long_blade_two_hand',
         'axe_one_hand', 'axe_two_hand', 'blunt_one_hand', 'blunt_two_hand_close',
         'blunt_two_hand_wide', 'spear']
ATTRIBUTES = ['strength', 'intelligence', 'willpower', 'agility', 'speed',
              'endurance', 'personality', 'luck']
SKILLS = ['block', 'armorer', 'mediumarmor', 'heavyarmor', 'bluntweapon',
          'longblade', 'axe', 'spear', 'athletics', 'enchant', 'destruction',
          'alteration', 'illusion', 'conjuration', 'mysticism', 'restoration',
          'alchemy', 'unarmored', 'security', 'sneak', 'acrobatics', 'lightarmor',
          'shortblade', 'marksman', 'mercantile', 'speechcraft', 'handtohand']
EXCLUDED = {
    'cureblightdisease': 'Never used, by user instruction.',
    'curecorprusdisease': 'Quest-sensitive cure, not ordinary loot.',
    'corprus': 'Disease acquisition / quest state.',
    'vampirism': 'Disease acquisition / quest state.',
    'extraspell': 'Internal placeholder.',
    'summoncreature04': 'Unassigned summon placeholder.',
    'summoncreature05': 'Unassigned summon placeholder.',
    'removecurse': 'Unused vanilla mechanic.',
    'sundamage': 'Special drawback; not in the approved ordinary-affix pool.',
    'stuntedmagicka': 'Special drawback; not in the approved ordinary-affix pool.',
    'resistcorprusdisease': 'Story-specific disease, not ordinary loot.',
    'weaknesstocorprusdisease': 'Story-specific disease, not ordinary loot.',
}


def tier_text(family, tier):
    entry = family['tiers'].get(str(tier))
    if not entry:
        return '-'
    effect = family['effect']
    percent = effect.startswith(('resist', 'weaknessto')) or effect in (
        'reflect', 'spellabsorption', 'chameleon', 'blind', 'sound', 'dispel')
    continuous = effect.startswith(('restore', 'damage', 'disintegrate')) or effect in (
        'absorbhealth', 'absorbmagicka', 'absorbfatigue')
    unit = '%' if percent else ' pts/sec' if continuous else ' pts'
    value = 'Enabled' if family['binary'] else str(entry['magnitude']) + unit
    if entry['duration']:
        value += f"; {entry['duration']} sec"
    mode = entry.get('mode', family['mode'])
    value += '; ' + ('CE' if mode == 'ConstantEffect' else 'on use' if mode == 'CastOnUse' else 'on strike')
    if mode != 'ConstantEffect':
        value += f'; >= {3+tier} base-cost casts'
    return f"{entry['name']} ({value})"


def families():
    result = []

    def add(effect, label, noun, slots, values, mode='ConstantEffect',
            duration=0, weight=1, binary=False, side='suffix', **extra):
        ident = effect + ':' + extra.get('attribute', extra.get('skill', ''))
        ranks = ['Whisper', 'Touch', 'Gift', 'Mantle', 'Crown', 'Dominion']
        tiers = {}
        for index, value in enumerate(values, 1):
            seconds = duration[index - 1] if isinstance(duration, list) else duration
            name = (noun + '-' + ranks[index - 1] if side == 'prefix'
                    else 'of ' + noun + "'s " + ranks[index - 1])
            delivery = mode[index - 1] if isinstance(mode, list) else mode
            tiers[str(index)] = dict(name=name, magnitude=value, duration=seconds, mode=delivery)
        result.append(dict(id=ident, effect=effect, label=label, side=side,
                           slots=slots, tiers=tiers, mode=mode[0] if isinstance(mode, list) else mode, range='Self',
                           weight=weight, binary=binary, **extra))

    small = [1, 2, 3, 4, 5, 6]
    resist = [3, 5, 7, 9, 12, 15]
    add('jump', 'Jump', 'Skyreach', ['boots', 'shoes'], [3, 6, 10, 16, 25, 35], side='prefix')
    water_modes = ['CastOnUse', 'CastOnUse', 'CastOnUse', 'ConstantEffect']
    add('waterbreathing', 'Water Breathing', 'Deepwater', ['helmet', 'amulet'], [1]*4,
        water_modes, [15, 30, 60, 0], binary=True)
    add('waterwalking', 'Water Walking', 'Stillwater', ['boots', 'shoes'], [1]*4,
        water_modes, [15, 30, 60, 0], binary=True)
    add('chameleon', 'Chameleon', 'Veiling', MAGE, [2, 4, 6, 8, 10, 12], weight=.5)
    for effect, label, noun in [('resistmagicka', 'Resist Magicka', 'Nullward'),
                                ('resistparalysis', 'Resist Paralysis', 'Freewill')]:
        add(effect, label, noun, ['shield', 'amulet'], resist)
    add('resistnormalweapons', 'Resist Normal Weapons', 'Ironward', ['cuirass', 'shield'], [2, 3, 4, 6, 8, 10], weight=.5)
    add('reflect', 'Reflect', 'Mirroring', ['amulet'], resist, weight=.25)
    add('spellabsorption', 'Spell Absorption', 'Spellfeast', ['ring', 'amulet'],
        [1, 2, 3, 4, 5], weight=.25)
    # A single suffix slot makes the three CE regeneration families mutually exclusive.
    for resource, noun in [('health', 'Lifewell'), ('fatigue', 'Secondwind'),
                           ('magicka', 'Aetherwell')]:
        add('restore' + resource, 'Restore ' + resource.title(), noun, ['amulet'],
            [1, 2, 3], weight=.1, side='suffix')

    # Timed utility grows real duration; instant effects grow charge capacity.
    utility = [
        ('invisibility', 'Invisibility', 'Vanishing', MAGE, [1]*6, [5, 10, 15, 20, 30, 45], True, 'Self'),
        ('open', 'Open', 'Unsealing', HANDS, [10, 20, 30, 45, 65, 85], 0, False, 'Touch'),
        ('lock', 'Lock', 'Sealing', HANDS, [5, 10, 20, 30, 40, 50], 0, False, 'Touch'),
        ('dispel', 'Dispel', 'Unweaving', ['ring', 'amulet'], [5, 10, 15, 20, 30, 40], 0, False, 'Self'),
    ]
    add('levitate', 'Levitate', 'Cloudstep', ['shoes', 'robe', 'amulet'], [15, 15, 15, 15, 25, 50],
        ['CastOnUse']*3 + ['ConstantEffect']*3, [15, 30, 60, 0, 0, 0], .5)
    for effect, label, noun, slots, values, duration, binary, target in utility:
        add(effect, label, noun, slots, values, 'CastOnUse', duration, .5, binary)
        result[-1]['range'] = target
    for effect, label, noun, slots in [
        ('curecommondisease', 'Cure Common Disease', 'Cleanblood', ['amulet']),
        ('curepoison', 'Cure Poison', 'Purging', ['amulet']),
        ('cureparalyzation', 'Cure Paralysis', 'Unbinding', ['amulet']),
        ('mark', 'Mark', 'Waymark', ['amulet']),
        ('recall', 'Recall', 'Homecoming', ['amulet']),
        ('almsiviintervention', 'Almsivi Intervention', 'Templeward', ['amulet']),
        ('divineintervention', 'Divine Intervention', 'Divineward', ['amulet']),
    ]:
        add(effect, label, noun, slots, [1]*6, 'CastOnUse', weight=.25, binary=True)
    for parameter, targets in [('attribute', ATTRIBUTES), ('skill', SKILLS)]:
        for target in targets:
            add('restore' + parameter, 'Restore ' + target.title(), 'Renewed ' + target.title(),
                ['ring'], small, 'CastOnUse', 5, 1/len(targets), **{parameter: target})

    for effect, label, noun in [
        ('charm', 'Charm', 'Allure'), ('commandhumanoid', 'Command Humanoid', 'Authority'),
        ('commandcreature', 'Command Creature', 'Beastmaster'),
        ('calmhumanoid', 'Calm Humanoid', 'Truce'), ('calmcreature', 'Calm Creature', 'Stillbeast'),
        ('frenzyhumanoid', 'Frenzy Humanoid', 'Discord'), ('frenzycreature', 'Frenzy Creature', 'Wildrage'),
        ('rallyhumanoid', 'Rally Humanoid', 'Courage'), ('rallycreature', 'Rally Creature', 'Wildheart'),
        ('demoralizehumanoid', 'Demoralize Humanoid', 'Dread'),
        ('demoralizecreature', 'Demoralize Creature', 'Beastfear'), ('turnundead', 'Turn Undead', 'Graveward'),
    ]:
        if effect.startswith('command'):
            values, durations = [5, 15, 25], [10, 20, 30]
        elif effect.startswith(('calm', 'frenzy', 'rally', 'demoralize', 'turnundead')):
            values, durations = [25, 50, 100], [10, 20, 30]
        else:
            values, durations = [3, 5, 8, 12, 18, 25], [5, 8, 10, 12, 15, 20]
        add(effect, label, noun, MAGE, values, 'CastOnUse', durations, .25)
        result[-1]['range'] = 'Touch'

    summons = [
        ('AncestralGhost', 'Ancestral Ghost', 'sMagicAncestralGhostID'),
        ('Bonelord', 'Bonelord', 'sMagicBonelordID'),
        ('Bonewalker', 'Bonewalker', 'sMagicLeastBonewalkerID'),
        ('CenturionSphere', 'Centurion Sphere', 'sMagicCenturionSphereID'),
        ('Clannfear', 'Clannfear', 'sMagicClannfearID'), ('Daedroth', 'Daedroth', 'sMagicDaedrothID'),
        ('Dremora', 'Dremora', 'sMagicDremoraID'), ('Fabricant', 'Fabricant', 'sMagicFabricantID'),
        ('FlameAtronach', 'Flame Atronach', 'sMagicFlameAtronachID'),
        ('FrostAtronach', 'Frost Atronach', 'sMagicFrostAtronachID'),
        ('GoldenSaint', 'Golden Saint', 'sMagicGoldenSaintID'),
        ('GreaterBonewalker', 'Greater Bonewalker', 'sMagicGreaterBonewalkerID'),
        ('Hunger', 'Hunger', 'sMagicHungerID'), ('Scamp', 'Scamp', 'sMagicScampID'),
        ('SkeletalMinion', 'Skeletal Minion', 'sMagicSkeletalMinionID'),
        ('StormAtronach', 'Storm Atronach', 'sMagicStormAtronachID'),
        ('WingedTwilight', 'Winged Twilight', 'sMagicWingedTwilightID'),
        ('Wolf', 'Wolf', 'sMagicCreature01ID'), ('Bear', 'Bear', 'sMagicCreature02ID'),
        ('Bonewolf', 'Bonewolf', 'sMagicCreature03ID'),
    ]
    for ident, label, gmst in summons:
        extra = dict(requiredCreatureGMST=gmst)
        if ident == 'Fabricant':
            extra['expansion'] = 'tribunal'
        elif ident in ('Wolf', 'Bear', 'Bonewolf'):
            extra['expansion'] = 'bloodmoon'
        add('summon' + ident.lower(), 'Summon ' + label, label + ' Gate', MAGE,
            [1]*6, 'CastOnUse', [5, 10, 15, 20, 30, 45], 1/len(summons), True, side='prefix', **extra)
    bound = [('dagger', 'Dagger', 'Weapon'), ('longsword', 'Longsword', 'Weapon'),
             ('mace', 'Mace', 'Weapon'), ('battleaxe', 'Battle Axe', 'Weapon'),
             ('spear', 'Spear', 'Weapon'), ('longbow', 'Longbow', 'Weapon'),
             ('cuirass', 'Cuirass', 'Armor'), ('helm', 'Helm', 'Armor'),
             ('boots', 'Boots', 'Armor'), ('shield', 'Shield', 'Armor'),
             ('gloves', 'Gloves', 'Armor')]
    for ident, label, record_type in bound:
        gmsts = (['sMagicBoundLeftGauntletID', 'sMagicBoundRightGauntletID']
                 if ident == 'gloves' else ['sMagicBound' + label.replace(' ', '') + 'ID'])
        add('bound' + ident, 'Bound ' + label, 'Spectral ' + label, MAGE, [1]*6,
            'CastOnUse', [5, 10, 15, 20, 30, 45], 1/len(bound), True,
            side='prefix', requiredItemGMSTs=gmsts, requiredType=record_type)

    for effect, label, noun, values, duration, binary in [
        ('absorbhealth', 'Absorb Health', 'Bloodfeast', [1, 2, 3, 4, 6, 8], 1, False),
        ('absorbfatigue', 'Absorb Fatigue', 'Vigorfeast', [2, 3, 4, 6, 8, 10], 1, False),
        ('absorbmagicka', 'Absorb Magicka', 'Magefeast', small, 1, False),
        ('damagehealth', 'Damage Health', 'Wounding', [1, 2, 3, 4, 6, 8], 1, False),
        ('damagemagicka', 'Damage Magicka', 'Magebane', small, 1, False),
        ('drainhealth', 'Drain Health', 'Lifeleech', [2, 3, 4, 6, 8, 10], 3, False),
        ('drainmagicka', 'Drain Magicka', 'Spellleech', [2, 3, 4, 6, 8, 10], 3, False),
        ('drainfatigue', 'Drain Fatigue', 'Vigorleech', [2, 3, 4, 6, 8, 10], 3, False),
        ('burden', 'Burden', 'Leadweight', [3, 5, 8, 12, 16, 20], 3, False),
        ('blind', 'Blind', 'Dimming', [2, 4, 6, 8, 10, 12], 3, False),
        ('sound', 'Sound', 'Dissonance', [2, 4, 6, 8, 10, 12], 3, False),
        ('silence', 'Silence', 'Hushing', [1]*6, [1, 2, 3, 4, 5, 6], True),
        ('paralyze', 'Paralysis', 'Stillness', [1]*6, [2, 3, 5, 7, 10, 15], True),
        ('disintegratearmor', 'Disintegrate Armor', 'Rust', [5, 10, 15, 25, 40, 60], 1, False),
        ('disintegrateweapon', 'Disintegrate Weapon', 'Brittleness', [5, 10, 15, 25, 40, 60], 1, False),
        ('soultrap', 'Soultrap', 'Soulbinding', [1]*6, [2, 3, 5, 8, 12, 20], True),
    ]:
        add(effect, label, noun, MELEE, values, 'CastOnStrike', duration, .25 if effect == 'paralyze' else .5, binary,
            side='prefix' if effect in ('burden', 'blind', 'sound') else 'suffix')
        result[-1]['range'] = 'Touch'
    for target, label in [('fire', 'Fire'), ('frost', 'Frost'), ('shock', 'Shock'),
                           ('magicka', 'Magicka'), ('poison', 'Poison'),
                           ('normalweapons', 'Normal Weapons'), ('commondisease', 'Common Disease'),
                           ('blightdisease', 'Blight Disease')]:
        add('weaknessto' + target, 'Weakness to ' + label, label + ' Breach', MELEE,
            resist, 'CastOnStrike', 3, .5)
        result[-1]['range'] = 'Touch'
    for action in ['absorb', 'damage', 'drain']:
        for parameter, targets in [('attribute', ATTRIBUTES), ('skill', SKILLS)]:
            for target in targets:
                add(action + parameter, action.title() + ' ' + target.title(),
                    action.title() + ' ' + target.title(), MELEE, small,
                    'CastOnStrike', 1 if action == 'damage' else 3,
                    .5/len(targets), **{parameter: target})
                result[-1]['range'] = 'Touch'
    return result
