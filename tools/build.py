"""Explicit export, static-site, and packaging tasks. Never runs tests."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def run_tool(name):
    subprocess.run([sys.executable, str(ROOT / 'tools' / name)], cwd=ROOT, check=True)


def commit_id():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return 'uncommitted'


def package(profile, version, drop_chance):
    profiles = json.loads((ROOT / 'release/profiles.json').read_text(encoding='utf-8'))
    overrides = dict(profiles[profile])
    if drop_chance is not None:
        overrides['dropChance'] = drop_chance
    if overrides['dropChance'] is None:
        raise ValueError('Production drop rate is undecided. Supply --drop-chance (0 to 1).')
    if not 0 <= overrides['dropChance'] <= 1:
        raise ValueError('Drop chance must be between 0 and 1.')
    stage = ROOT / 'build' / ('mod-' + profile)
    if stage.resolve().parent != (ROOT / 'build').resolve():
        raise ValueError('Staging directory must remain inside this repository build directory.')
    if stage.exists():
        # Fixed build-only path, never the working mod or another installation.
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    sources = sorted((ROOT / 'mod/scripts').rglob('*.lua'))
    sources += sorted((ROOT / 'mod/l10n').rglob('*.yaml'))
    sources += sorted((ROOT / 'mod').glob('*.omwscripts'))
    if not sources or not list((ROOT / 'mod').glob('*.omwscripts')):
        raise ValueError('Missing runtime source or .omwscripts manifest.')
    for source in sources:
        if source.is_symlink():
            raise ValueError('Symlinks are not packaged: ' + str(source))
        target = stage / source.relative_to(ROOT / 'mod')
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    config = stage / 'scripts/randomisedbasicloot/config.lua'
    text = config.read_text(encoding='utf-8')
    for key, value in overrides.items():
        literal = str(value).lower() if isinstance(value, bool) else str(value)
        text, count = re.subn(r'(?m)^(\s*' + re.escape(key) + r'\s*=\s*)[^,\n]+',
                             lambda match: match[1] + literal, text)
        if count != 1:
            raise ValueError('Expected exactly one config default: ' + key)
    config.write_text(text, encoding='utf-8', newline='\n')
    files = {str(p.relative_to(stage)).replace('\\', '/'):
             hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(stage.rglob('*')) if p.is_file()}
    manifest = dict(version=version, profile=profile, commit=commit_id(),
                    defaults=overrides, validated=False, files=files)
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    archive = dist / f'fortunes-spoils-{version}-{profile}.zip'
    manifest_path = archive.with_suffix('.manifest.json')
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    shutil.copyfile(ROOT / 'release/INSTALL.md', dist / 'INSTALL.md')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as output:
        for path in sorted(stage.rglob('*')):
            if path.is_file():
                entry = zipfile.ZipInfo(path.relative_to(stage).as_posix(), (1980, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                output.writestr(entry, path.read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    manifest_digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    archive.with_suffix('.zip.sha256').write_text(
        f'{digest}  {archive.name}\n{manifest_digest}  {manifest_path.name}\n', encoding='utf-8')
    print(archive)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('task', choices=['export', 'site', 'package'])
    parser.add_argument('--profile', choices=['testing', 'production'], default='testing')
    parser.add_argument('--drop-chance', type=float)
    parser.add_argument('--version')
    args = parser.parse_args()
    meta = json.loads((ROOT / 'release/metadata.json').read_text(encoding='utf-8'))
    version = args.version or meta['version']
    if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+(?:-[A-Za-z0-9.-]+)?', version):
        parser.error('Version must be major.minor.patch with an optional prerelease suffix.')
    if args.task == 'export':
        run_tool('export_runtime_design.py')
    elif args.task == 'site':
        run_tool('build_modifier_preview.py')
        run_tool('build_loot_simulator.py')
        out = ROOT / 'build/site'
        page = out / 'index.html'
        stamp = html.escape(f"Modifier Catalogue / {version} / {meta['status']}")
        page.write_text(page.read_text(encoding='utf-8').replace(
            'Modifier Catalogue / Development Build', stamp), encoding='utf-8')
        simulator = out / 'simulator.html'
        simulator.write_text(simulator.read_text(encoding='utf-8').replace(
            'Loot Simulator / Development Build', html.escape(f"Loot Simulator / {version} / {meta['status']}")), encoding='utf-8')
        (out / '.nojekyll').touch()
        (out / 'build-info.json').write_text(json.dumps(dict(version=version, commit=commit_id(),
                                                            status=meta['status']), indent=2) + '\n',
                                              encoding='utf-8')
    else:
        package(args.profile, version, args.drop_chance)


if __name__ == '__main__':
    main()
