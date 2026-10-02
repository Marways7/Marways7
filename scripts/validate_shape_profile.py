"""Check generated SVG safety, mobile variants, references and public data."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = '{http://www.w3.org/2000/svg}'


class LocalImages(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if tag in ('img', 'source') and name in ('src', 'srcset'):
                self.paths.append(value)


def main():
    readme = (ROOT/'README.md').read_text(encoding='utf-8-sig')
    parser = LocalImages()
    parser.feed(readme)
    for value in parser.paths:
        assert value.startswith('./assets/shape/'), f'Unexpected image dependency: {value}'
        assert (ROOT/value).is_file(), f'Missing image: {value}'
    files = list((ROOT/'assets/shape').glob('*.svg'))
    assert len(files) == 30
    for file in files:
        raw = file.read_text(encoding='utf-8')
        node = ET.fromstring(raw)
        assert node.tag == NS+'svg'
        assert node.find(NS+'title') is not None
        assert node.find('.//'+NS+'script') is None
        assert node.find('.//'+NS+'foreignObject') is None
        assert node.find('.//'+NS+'image') is None
        assert 'prefers-reduced-motion:reduce' in raw
        assert not re.search(r'\b(?:NaN|Infinity)\b', raw)
        assert file.stat().st_size < 600_000, f'Unexpected asset size: {file.name}'
        if 'hero' in file.name and 'cinema' not in file.name:
            assert len(node.findall('.//'+NS+'path')) > 80
        if 'projects' in file.name:
            anchors = node.findall('.//'+NS+'a')
            assert len(anchors) == 6
            assert all(a.attrib['href'].startswith('https://github.com/Marways7/') for a in anchors)
        if '-mobile' in file.name:
            assert node.attrib['viewBox'].split()[2] == '640'
    data = json.loads((ROOT/'data/public-profile.json').read_text(encoding='utf-8-sig'))
    assert data['repositories'] and data['source'] == 'https://api.github.com/users/Marways7/repos'
    for repo in data['repositories']:
        assert set(repo) == {'name', 'html_url', 'language', 'stargazers_count', 'forks_count'}
        assert repo['html_url'].startswith('https://github.com/Marways7/')
        assert isinstance(repo['stargazers_count'], int) and repo['stargazers_count'] >= 0
    for old_text in ('65.2%', 'autonomous research agent', 'count_private=true', 'komarev.com'):
        assert old_text not in readme
    print(f'Validated {len(files)} SVGs, {len(parser.paths)} README image references, six project links per atlas and public metadata schema.')


if __name__ == '__main__':
    main()
