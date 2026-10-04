"""Check generated SVG safety, mobile variants, references and public data."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = '{http://www.w3.org/2000/svg}'


def jpeg_size(raw):
    """Read JPEG dimensions without an image-library dependency."""
    offset = 2
    while offset < len(raw):
        assert raw[offset] == 0xff, 'Invalid JPEG marker'
        while raw[offset] == 0xff:
            offset += 1
        marker = raw[offset]
        offset += 1
        if marker in (0xd8, 0xd9, 0x01) or 0xd0 <= marker <= 0xd7:
            continue
        length = int.from_bytes(raw[offset:offset+2], 'big')
        assert length >= 2
        if marker in (0xc0, 0xc1, 0xc2):
            return (int.from_bytes(raw[offset+5:offset+7], 'big'),
                    int.from_bytes(raw[offset+3:offset+5], 'big'))
        offset += length
    raise AssertionError('JPEG has no supported frame header')


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
        assert value.startswith(('./assets/shape/', './assets/play/')), f'Unexpected image dependency: {value}'
        assert (ROOT/value).is_file(), f'Missing image: {value}'
    files = list((ROOT/'assets/shape').glob('*.svg'))
    assert len(files) == 46
    playground_files = list((ROOT/'assets/play').glob('*.svg'))
    assert len(playground_files) == 20
    files += playground_files
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
        if file.name.startswith('hero'):
            assert len(node.findall('.//'+NS+'path')) > 80
        if 'projects' in file.name:
            anchors = node.findall('.//'+NS+'a')
            assert len(anchors) == 6
            assert all(a.attrib['href'].startswith('https://github.com/Marways7/') for a in anchors)
        if '-mobile' in file.name:
            assert node.attrib['viewBox'].split()[2] == '640'
        if file.name.startswith('living-'):
            assert len(node.findall('.//'+NS+'path')) >= 144
            if '-still' in file.name:
                assert '.form{animation:none!important}' in raw
        if file.parent.name == 'play' and '-still' in file.name:
            assert '*{animation:none!important}' in raw
    for name, expected_size in [('cover.jpg', (1200, 610)), ('cover-mobile.jpg', (640, 820))]:
        cover = ROOT/'assets/play'/name
        assert cover.read_bytes().startswith(b'\xff\xd8\xff'), f'Invalid cover image: {name}'
        assert 10_000 < cover.stat().st_size < 1_000_000
        assert jpeg_size(cover.read_bytes()) == expected_size, f'Wrong cover dimensions: {name}'
    site = (ROOT/'site/index.html').read_text(encoding='utf-8')
    assert '{{' not in site, 'Unexpanded site template'
    assert len(re.findall(r'role="tabpanel"',site)) == 6
    for project in ('ECG_IdentificationX','AiliaoX','DeepReadX','cua_desktop_operator_skill','cua_desktop_operator_cli_skill','signal-sprint','college_student_self-rescue_guide_website'):
        target = f'https://github.com/Marways7/{project}'
        assert target in readme and target in site, f'Missing repository link: {project}'
    data = json.loads((ROOT/'data/public-profile.json').read_text(encoding='utf-8-sig'))
    assert data['repositories'] and data['source'] == 'https://api.github.com/users/Marways7/repos'
    for repo in data['repositories']:
        assert set(repo) == {'name', 'html_url', 'language', 'stargazers_count', 'forks_count'}
        assert repo['html_url'].startswith('https://github.com/Marways7/')
        assert isinstance(repo['stargazers_count'], int) and repo['stargazers_count'] >= 0
    for old_text in ('65.2%', 'autonomous research agent', 'count_private=true', 'komarev.com'):
        assert old_text not in readme
    print(f'Validated {len(files)} SVGs, {len(parser.paths)} README image references, two covers, six site scenes, seven repository links and public metadata schema.')


if __name__ == '__main__':
    main()
