"""Build a portable preview with all local images, styles, scripts and fonts embedded."""
from pathlib import Path
import base64
import mimetypes
import re

root = Path(__file__).resolve().parent

def data_url(path):
    mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    return 'data:' + mime + ';base64,' + base64.b64encode(path.read_bytes()).decode('ascii')

html = (root / 'index.html').read_text(encoding='utf-8')
fonts = (root / 'assets/fonts.css').read_text(encoding='utf-8')
for match in set(re.findall(r'url\(([^)]+)\)', fonts)):
    name = match.strip('"\'')
    fonts = fonts.replace(match, data_url(root / 'assets' / name))
css = (root / 'styles.css').read_text(encoding='utf-8')
js = (root / 'app.js').read_text(encoding='utf-8')
html = html.replace('<link rel="stylesheet" href="assets/fonts.css">', '<style>' + fonts + '</style>')
html = html.replace('<link rel="stylesheet" href="styles.css">', '<style>' + css + '</style>')
html = html.replace('<script defer src="app.js"></script>', '')
html = html.replace('</body>', '<script>' + js + '</script></body>')
for path in (root / 'assets').glob('*'):
    if path.is_file() and path.suffix in ('.jpg', '.png', '.svg', '.webp'):
        html = html.replace('assets/' + path.name, data_url(path))
assert 'src="assets/' not in html
assert '<script defer src=' not in html
assert 'url(fonts/' not in html
(root / 'OPEN-WEBSITE.html').write_text(html, encoding='utf-8')
print('Portable preview:', len(html.encode('utf-8')), 'bytes')
