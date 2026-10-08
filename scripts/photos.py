"""
Build responsive WebP variants for photographs in assets/img/.

Why this exists: the theme's `figure.liquid` emits a <picture> with a WebP
srcset whenever `imagemagick.enabled` is true, and relies on the
jekyll-imagemagick plugin to produce those files at build time. On the GitHub
Actions runner that plugin silently produces nothing, so the srcset points at
files that 404 — and a <picture> does *not* fall back to its <img> when the
source it selected fails to load. The result is a broken image with a green
build.

So the variants are generated here and committed instead. The widths are read
from _config.yml, so the two stay in step.

SVG artwork is untouched — it needs no variants.

Run:  python3 scripts/photos.py
Out:  assets/img/<name>-<width>.webp for each photo
"""

import pathlib
import re
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
QUALITY = 80
SOURCE_SUFFIXES = {".jpg", ".jpeg", ".png", ".tiff"}


def configured_widths():
    """Read imagemagick.widths from _config.yml without a YAML dependency."""
    text = (ROOT / "_config.yml").read_text()
    block = re.search(r"imagemagick:.*?widths:\n((?:\s*-\s*\d+\n)+)", text, re.S)
    if not block:
        sys.exit("Could not find imagemagick.widths in _config.yml")
    return [int(n) for n in re.findall(r"-\s*(\d+)", block.group(1))]


def main():
    widths = configured_widths()
    print("widths from _config.yml:", widths)

    photos = [
        p
        for p in sorted(IMG.rglob("*"))
        if p.suffix.lower() in SOURCE_SUFFIXES and "-" not in p.stem
    ]
    if not photos:
        print("no source photographs found")
        return

    for photo in photos:
        with Image.open(photo) as im:
            im = im.convert("RGB")
            for w in widths:
                if w > im.width:
                    # Never upscale: a variant wider than the source is just a
                    # bigger file with no more detail in it.
                    continue
                h = round(im.height * w / im.width)
                out = photo.with_name(f"{photo.stem}-{w}.webp")
                im.resize((w, h), Image.LANCZOS).save(
                    out, "WEBP", quality=QUALITY, method=6
                )
                print(f"  {out.relative_to(ROOT)}  {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
