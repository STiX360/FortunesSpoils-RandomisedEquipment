"""Shared ordinary-weapon delivery policy for Lua export and catalogue rows."""
import math

CONTROL_EFFECTS = {'paralyze', 'silence', 'blind', 'sound', 'burden',
                   'drainattribute', 'drainskill', 'absorbattribute', 'absorbskill'}
BINARY_EFFECTS = {'paralyze', 'silence', 'soultrap'}
DAMAGE_EFFECTS = {'firedamage', 'frostdamage', 'shockdamage', 'poison',
                  'damagehealth', 'damagemagicka', 'damagefatigue'}
DAMAGE_SPEED_MIN = .75
DAMAGE_SPEED_MAX = 1.5
PROFILES = [
    dict(label='Short blades', slots=['short_blade'], controlDuration=1),
    dict(label='One-handed weapons', slots=['long_blade_one_hand', 'axe_one_hand', 'blunt_one_hand'], controlDuration=.75),
    dict(label='Two-handed blades and axes', slots=['long_blade_two_hand', 'axe_two_hand'], controlDuration=.55),
    dict(label='Warhammers and spears', slots=['blunt_two_hand_close', 'spear'], controlDuration=.45),
    dict(label='Staves', slots=['blunt_two_hand_wide'], controlDuration=1.25,
         magnitude=1.5, mode='CastOnUse', range='Target', area=3),
]
MELEE_SLOTS = [slot for profile in PROFILES for slot in profile['slots']]


def policy():
    return dict(controlEffects={effect: True for effect in sorted(CONTROL_EFFECTS)},
                damageEffects={effect: True for effect in sorted(DAMAGE_EFFECTS)},
                damageSpeedMin=DAMAGE_SPEED_MIN, damageSpeedMax=DAMAGE_SPEED_MAX,
                profiles={slot: profile for profile in PROFILES for slot in profile['slots']})


def resolve_effects(effects, profile, base_speed=1):
    control = any(effect['id'] in CONTROL_EFFECTS for effect in effects)
    result = []
    for effect in effects:
        value = dict(effect)
        if control:
            value['duration'] = max(1, math.floor(value.get('duration', 1) * profile['controlDuration'] + .5))
        if 'magnitude' in profile:
            if value['id'] not in BINARY_EFFECTS:
                value['magnitude'] = max(1, math.floor(value['magnitude'] * profile['magnitude'] + .5))
            value.update(range=profile['range'], area=profile['area'])
        elif value['id'] in DAMAGE_EFFECTS:
            speed = base_speed if math.isfinite(base_speed) and base_speed > 0 else 1
            multiplier = min(DAMAGE_SPEED_MAX, max(DAMAGE_SPEED_MIN, 1 / speed))
            value['magnitude'] = max(1, math.floor(value['magnitude'] * multiplier + .5))
        result.append(value)
    return result


def variants(effects, slots):
    if any(effect['id'] in CONTROL_EFFECTS for effect in effects):
        profiles = PROFILES
    else:
        profiles = [dict(label='Melee weapons (excluding staves)',
                         slots=[slot for slot in MELEE_SLOTS if slot != 'blunt_two_hand_wide'],
                         controlDuration=1), PROFILES[-1]]
    for profile in profiles:
        eligible = [slot for slot in profile['slots'] if slot in slots]
        if eligible:
            yield dict(profile, slots=eligible)
