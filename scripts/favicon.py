"""
Build the browser-tab icon in the formats browsers actually use.

Safari ignores SVG favicons declared with rel="shortcut icon". With no
/favicon.ico at the origin root it falls back to whatever it has cached for the
domain — and because this site shares hdclark94.github.io with another one, that
meant showing the other site's icon. So PNGs are required, not optional.

At 16px a favicon has to be a silhouette: the three-leaf mark used elsewhere
turns to mush, so this is one leaf, solid, with a cut midrib. Same beta-shaped
profile as the rest of the artwork, so it is recognisably the same plant.

Run:  python3 scripts/favicon.py
Out:  assets/img/favicon-{16,32,180,512}.png
"""

import pathlib

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"
LEAF = "#235c39"
MASTER = 1024
SIZES = [512, 180, 32, 16]


def leaf_points(a=0.85, b=1.6, n=400):
    """Half-width w(s) = s^a (1-s)^b along the midrib: round base, pointed tip."""
    s = np.linspace(0.0, 1.0, n)
    w = (s**a) * ((1.0 - s) ** b)
    w /= w.max()
    right = np.column_stack([w, s])
    left = np.column_stack([-w[::-1], s[::-1]])
    return np.vstack([right, left])


def main():
    fig = plt.figure(figsize=(1, 1), dpi=MASTER)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-0.62, 0.62)
    ax.set_ylim(-0.08, 1.08)
    ax.axis("off")

    pts = leaf_points()
    pts[:, 0] *= 0.52  # width relative to length
    ax.add_patch(Polygon(pts, closed=True, facecolor=LEAF, edgecolor="none"))
    # Midrib cut out of the silhouette rather than drawn on top, so it still
    # reads once the icon is scaled down.
    ax.plot([0, 0], [0.04, 0.80], color="#ffffff", lw=MASTER * 0.055 / 12,
            solid_capstyle="round", alpha=0.95)

    tmp = OUT / "favicon-512.png"
    fig.savefig(tmp, transparent=True, dpi=MASTER)
    plt.close(fig)

    master = Image.open(tmp).convert("RGBA")
    for size in SIZES:
        out = OUT / f"favicon-{size}.png"
        master.resize((size, size), Image.LANCZOS).save(out, "PNG", optimize=True)
        print(f"  {out.relative_to(ROOT)}  {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
