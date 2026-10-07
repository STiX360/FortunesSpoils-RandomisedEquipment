"""Refresh exact-record UESP/OAAB image links; never bundle game images."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, urlencode, urljoin
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PAGES = [f'{game}:Base_{kind}' for game in ('Morrowind', 'Tribunal', 'Bloodmoon')
         for kind in ('Armor', 'Weapons', 'Clothing')]
PAGES.append('Tribunal:Dark_Brotherhood_Armor')


class Rows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell = None
        self.link = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'tr':
            self.row = []
        elif tag in ('td', 'th') and self.row is not None:
            self.cell = {'text': '', 'images': []}
        elif tag == 'br' and self.cell is not None:
            self.cell['text'] += '\n'
        elif tag == 'a':
            self.link = attrs.get('href')
        elif tag == 'img' and self.cell is not None and self.link and '/wiki/File:' in self.link:
            self.cell['images'].append({'url': urljoin('https://en.uesp.net', attrs['src']),
                                        'filePage': urljoin('https://en.uesp.net', self.link)})

    def handle_data(self, data):
        if self.cell is not None:
            self.cell['text'] += data

    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            self.row.append(self.cell)
            self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        elif tag == 'a':
            self.link = None


def read_json(url):
    request = Request(url, headers={'User-Agent': 'FortunesSpoilsImageIndex/1.0'})
    with urlopen(request, timeout=60) as response:
        return json.load(response)


def add_oaab_images(images, records):
    library = 'https://www.oaab.dev/library/'
    rows = read_json('https://www.oaab.dev/assets/data/library/OAAB_Data_filtered.json')
    tree = read_json('https://api.github.com/repos/OAAB-Modding/OAAB-Modding.github.io/git/trees/main?recursive=1')
    if tree.get('truncated'):
        raise ValueError('OAAB file index is truncated; cannot verify thumbnail paths')
    paths = {entry['path'] for entry in tree['tree'] if entry['type'] == 'blob'}
    count = 0
    for row in rows:
        ident = str(row.get('id', '')).lower()
        if ident not in records or ident in images:
            continue
        mesh = str(row.get('mesh', '')).replace('\\', '/').lower().removeprefix('meshes/')
        if not mesh.endswith('.nif'):
            continue
        path = 'assets/images/library/thumbnails/meshes/' + mesh[:-4] + '.webp'
        if path not in paths:
            continue
        url = 'https://www.oaab.dev/' + quote(path, safe='/')
        images[ident] = dict(url=url, filePage=library, sourcePage=library,
                             sourceLabel='OAAB Library', rendering='smooth', recordId=row['id'])
        count += 1
    print(f'OAAB Library: {count} new exact-record matches with verified thumbnail paths')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--oaab-only', action='store_true', help='Keep existing UESP links and fill OAAB gaps')
    args = parser.parse_args()
    records = json.loads((ROOT / 'data/simulator-snapshot.json').read_text(encoding='utf-8'))['records']
    images = json.loads((ROOT / 'data/item-images.json').read_text(encoding='utf-8')) if args.oaab_only else {}
    for page in ([] if args.oaab_only else PAGES):
        url = 'https://en.uesp.net/w/api.php?' + urlencode(dict(action='parse', page=page, prop='text', format='json'))
        request = Request(url, headers={'User-Agent': 'FortunesSpoilsImageIndex/1.0'})
        with urlopen(request, timeout=45) as response:
            data = json.load(response)
        parser = Rows()
        parser.feed(data['parse']['text']['*'])
        count = 0
        for row in parser.rows:
            image = next((image for cell in row for image in cell['images']), None)
            if not image:
                continue
            for cell in row:
                for line in cell['text'].splitlines():
                    ident = line.strip().lower()
                    if ident in records:
                        images[ident] = {**image, 'sourcePage': 'https://en.uesp.net/wiki/' + page.replace(' ', '_')}
                        count += 1
        print(f'{page}: {count} matching records')
    add_oaab_images(images, records)
    (ROOT / 'data/item-images.json').write_text(json.dumps(images, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(f'Indexed {len(images)} exact-record image links (no images downloaded)')


if __name__ == '__main__':
    main()
