"""Reproducible WebP compression/resizing of the preserved licensed photo; no creative alteration."""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
PHOTO = ROOT.parents[1] / 'docs/design/landing/assets/batumi-panorama.png'
EXPECTED = '330e636d2ab7a56ff1d647616536e9a65eb883449d8de57a584eb64c7a0456ec'


def main():
    if hashlib.sha256(PHOTO.read_bytes()).hexdigest() != EXPECTED:
        raise SystemExit('Preserved original photo identity differs; no images written')
    with Image.open(PHOTO) as source:
        source = source.convert('RGB'); receipt = []
        for width in [480, 960, 1335]:
            size = (width, round(source.height * width / source.width))
            image = source.resize(size, Image.Resampling.LANCZOS)
            path = ROOT / 'assets' / f'batumi-{width}.webp'
            image.save(path, 'WEBP', quality=84, method=6)
            receipt.append({'file': path.name, 'size': list(size), 'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    (ROOT / 'assets/PHOTO_PROVENANCE.json').write_text(json.dumps({'source_path': PHOTO.relative_to(ROOT.parents[1]).as_posix(), 'source_sha256': EXPECTED, 'creator': 'Alexabsent', 'title': 'Batumi.png', 'photo_date': 'December 2023', 'source_url': 'https://commons.wikimedia.org/wiki/File:Batumi.png', 'license': 'CC0 1.0', 'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/', 'modification': 'Aspect-preserving resizing/WebP compression; CSS object-fit display crop only', 'variants': receipt}, indent=2) + '\n', encoding='utf8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
