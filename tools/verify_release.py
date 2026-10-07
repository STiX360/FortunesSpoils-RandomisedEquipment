"""Inspect a release ZIP against its companion manifest; does not run tests."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def verify(archive_path, version, profile):
    archive_path = Path(archive_path)
    manifest_path = archive_path.with_suffix('.manifest.json')
    checksum_path = archive_path.with_suffix('.zip.sha256')
    checksums = {}
    for line in checksum_path.read_text(encoding='utf-8').splitlines():
        digest, name = line.split('  ', 1)
        if name in checksums:
            raise ValueError('Duplicate checksum entry')
        checksums[name] = digest
    if set(checksums) != {archive_path.name, manifest_path.name}:
        raise ValueError('Checksum file must name exactly the ZIP and companion manifest')
    for path in (archive_path, manifest_path):
        if hashlib.sha256(path.read_bytes()).hexdigest() != checksums[path.name]:
            raise ValueError('Checksum mismatch: ' + path.name)
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest['version'] != version or manifest['profile'] != profile:
        raise ValueError('Release version/profile mismatch')
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or set(names) != set(manifest['files']):
            raise ValueError('Archive entries differ from the companion manifest')
        if 'Randomised Basic Loot.omwscripts' not in names:
            raise ValueError('Missing OpenMW content manifest')
        for name in names:
            allowed = name == 'Randomised Basic Loot.omwscripts' or (
                name.startswith('scripts/') and name.endswith('.lua')) or (
                name.startswith('l10n/') and name.endswith('.yaml'))
            if not allowed or '\\' in name or '..' in name.split('/'):
                raise ValueError('Non-runtime or unsafe archive entry: ' + name)
            if hashlib.sha256(archive.read(name)).hexdigest() != manifest['files'][name]:
                raise ValueError('Packaged file differs from manifest: ' + name)
    print(f'Inspected {archive_path.name}: {len(names)} runtime files; version/profile and hashes match')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive')
    parser.add_argument('--version', required=True)
    parser.add_argument('--profile', choices=['production', 'testing'], required=True)
    args = parser.parse_args()
    verify(args.archive, args.version, args.profile)


if __name__ == '__main__':
    main()
