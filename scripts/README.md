# Artwork generation

Every image on this site is drawn by [`artwork.py`](artwork.py) rather than
photographed. The generated SVGs are committed, so the site builds without
running anything here — you only need this when changing how the artwork looks,
or replacing it.

`scripts/` is excluded from the published site in `_config.yml`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
make art
```

## What it produces

| File                      | Used for                              |
| ------------------------- | ------------------------------------- |
| `banner-{light,dark}.svg` | Strip across the top of the home page |
| `logo.svg`                | The mark beside the home-page text    |
| `leaf_icon.svg`           | Favicon (the browser-tab icon)        |
| `offerings/{name}.svg`    | One tile per offering card            |

## How the leaves are drawn

A leaf is a midrib of length `L` with half-width along it following

```
w(s) = A · s^a · (1-s)^b        for s from 0 (base) to 1 (tip)
```

That profile gives a tapered base and a pointed tip, and the two exponents alone
change the species convincingly:

- **higher `a`** → narrower base
- **higher `b`** → sharper tip
- **lower both** → broad and blunt, more like a petal

Current defaults are `a=0.85, b=1.6`, which reads as a generic broadleaf. The
first version used `a=0.55, b=1.0` and everyone saw avocados, so if the shapes
start looking like fruit, raise `b`.

## Changing the colours

`GREENS` near the top is used for the logo and tiles — mid-tones picked to sit
legibly on **both** the light and dark backgrounds, so those files need only one
version each. `BANNER_GREENS` and `SURFACE` are per-theme, because the banner
covers the full width and needs its own background.

If you move away from greens, check the tile colours still read on both
backgrounds, or split the tiles into light and dark versions as the banner does.

## Output is deterministic

Regenerating unchanged artwork produces byte-identical files, so a diff in git
means the artwork actually changed. Three things make that true, and all three
are easy to break:

- `svg.hashsalt` is pinned, so element ids come from a fixed salt rather than a
  random uuid
- `metadata={"Date": None}` on save, so no timestamp is embedded
- patches use `clip_on=False` — the axes already fills the figure so the clip is
  redundant, and matplotlib derives clip-path ids unstably

If a small edit produces a hundred-line diff, one of those has been lost.

## Replacing artwork with photographs

The artwork is a placeholder for a real shop that doesn't have photos yet.
When it does:

**Banner** — put the photo in `assets/img/`, point `banner:` in
`_pages/about.md` at it and delete the `banner_dark:` line. The layout handles a
single image. It is sized with `object-fit: cover`, so any wide-ish photo crops
sensibly.

**Offering tiles** — drop images into `assets/img/offerings/` and change the
`image:` line in the matching file in `_offerings/`. Square works best; they
render at 84 px.

**Logo** — replace `image:` under `profile:` in `_pages/about.md`.

Photos in `assets/img/` are automatically converted to responsive WebP at build
time, provided ImageMagick is installed. SVGs are left alone.
