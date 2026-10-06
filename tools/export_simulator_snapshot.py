"""Explicit read-only source-master snapshot for the static loot simulator."""
import argparse
import json
import pathlib
import re
import struct
import urllib.request
from audit_helmets import decode, subrecords
from catalogue_bases import bases
from generate_unique_registry import physical_records

ROOT = pathlib.Path(__file__).resolve().parents[1]


def export(paths):
    url = 'https://raw.githubusercontent.com/OpenMW/openmw/openmw-0.51.0/components/esm3/loadmgef.cpp'
    source = urllib.request.urlopen(url).read().decode()
    names = re.findall(r'const StringRefId MagicEffect::\w+\("([^"]+)"\)', source)
    flags = [int(v, 16) for v in re.findall(r'0x[0-9a-f]+', re.search(r'HardcodedFlags\[NumberOfHardcodedFlags\] = \{(.*?)\};', source, re.S)[1])]
    assert len(names) == len(flags) == 143
    snapshot = dict(records={}, gmsts={}, effects={}, available={'Creature': {}, 'Armor': {}, 'Weapon': {}},
                    sources=[p.name for p in paths], effectSource=url)
    approved = {b['id']: b for b in bases(ROOT)}
    for path in paths:
        physical = physical_records(path)
        with path.open('rb') as stream:
            while header := stream.read(16):
                tag, size, _, _ = struct.unpack('<4sIII', header)
                if tag not in (b'ARMO', b'WEAP', b'CLOT', b'GMST', b'MGEF', b'CREA'):
                    stream.seek(size, 1)
                    continue
                parts = dict(subrecords(stream.read(size)))
                ident = decode(parts.get(b'NAME', b'')).lower()
                if tag in (b'ARMO', b'WEAP', b'CREA'):
                    snapshot['available'][{b'ARMO': 'Armor', b'WEAP': 'Weapon', b'CREA': 'Creature'}[tag]][ident] = True
                if ident in approved and ident in physical:
                    snapshot['records'][ident] = dict(physical[ident], id=ident, name=approved[ident]['name'],
                        mwscript=decode(parts.get(b'SCRI', b'')), enchant=decode(parts.get(b'ENAM', b'')))
                if tag == b'GMST':
                    key = decode(parts[b'NAME'])
                    if b'FLTV' in parts:
                        snapshot['gmsts'][key] = struct.unpack('<f', parts[b'FLTV'])[0]
                    elif b'INTV' in parts:
                        snapshot['gmsts'][key] = struct.unpack('<i', parts[b'INTV'])[0]
                    elif b'STRV' in parts:
                        snapshot['gmsts'][key] = decode(parts[b'STRV'])
                if tag == b'MGEF':
                    index = struct.unpack('<i', parts[b'INDX'])[0]
                    mask = flags[index]
                    snapshot['effects'][names[index].lower()] = dict(label=re.sub(r'([a-z])([A-Z])', r'\1 \2', names[index]), baseCost=struct.unpack_from('<f', parts[b'MEDT'], 4)[0],
                        onSelf=bool(mask & 64), onTouch=bool(mask & 128), onTarget=bool(mask & 256),
                        hasMagnitude=not bool(mask & 8), hasDuration=not bool(mask & 4), isAppliedOnce=bool(mask & 4096))
    # Keep only settings consumed by gameplay rules, not dialogue/UI strings.
    snapshot['gmsts'] = {k: v for k, v in snapshot['gmsts'].items() if not k.startswith('s') or k.startswith(('sMagic', 'sEffect'))}
    output = ROOT / 'data/simulator-snapshot.json'
    output.write_text(json.dumps(snapshot, ensure_ascii=True, sort_keys=True) + '\n', encoding='utf-8')
    print(f'Snapshotted {len(snapshot["records"])} approved item records to {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('masters', nargs='+', type=pathlib.Path)
    export(parser.parse_args().masters)
