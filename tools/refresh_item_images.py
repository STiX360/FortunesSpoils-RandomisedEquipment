"""Refresh exact-record UESP image links; never download or bundle game images."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode, urljoin
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


def main():
    records = json.loads((ROOT / 'data/simulator-snapshot.json').read_text(encoding='utf-8'))['records']
    images = {}
    for page in PAGES:
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
    (ROOT / 'data/item-images.json').write_text(json.dumps(images, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(f'Indexed {len(images)} exact-record image links (no images downloaded)')


if __name__ == '__main__':
    main()
