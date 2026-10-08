"""
Generate the site's leaf artwork.

Everything visual on this site is drawn here rather than photographed, so it can
be regenerated, recoloured or reshaped without a designer. Replace any of it with
real photographs whenever they exist — see scripts/README.md.

Leaves are built parametrically: a midrib of length L, with half-width along it
following w(s) = A * s^a * (1-s)^b. That beta-like profile gives a rounded base
and a pointed tip, and changing a and b alone produces convincingly different
species — broad and blunt, or narrow and willowy.

Output is deterministic: an unchanged run produces byte-identical files, so a
diff in git means the artwork actually changed.

Run:  python3 scripts/artwork.py [--png]
Out:  assets/img/banner-{light,dark}.svg   page banner
      assets/img/logo.svg                  about-page mark
      assets/img/leaf_icon.svg             favicon
      assets/img/offerings/*.svg           one tile per offering
"""

import pathlib
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"
# Fixed salt + no timestamp => regenerating unchanged artwork is a no-op in git.
matplotlib.rcParams["svg.hashsalt"] = "irynas-green-space"
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img"

# Mid-tone greens chosen to sit legibly on both the light and the dark surface,
# so tiles and the logo need only one version each.
GREENS = ["#2f7d4f", "#4a9d6e", "#6fbf8e", "#8fcfa5", "#3c6b4a"]

SURFACE = {"light": "#fbfdfa", "dark": "#141a16"}
BANNER_GREENS = {
    "light": ["#2f7d4f", "#4a9d6e", "#6fbf8e", "#a8d5b5", "#cbe6d4"],
    "dark": ["#6fbf8e", "#4a9d6e", "#3f8f63", "#2a5f45", "#1f4433"],
}


def leaf(centre, angle, length, width=0.34, a=0.85, b=1.6, n=140):
    """Outline of one leaf, as an (N, 2) array of points.

    centre is the base of the midrib; angle is the direction it points.
    """
    s = np.linspace(0.0, 1.0, n)
    half_w = width * length * (s**a) * ((1.0 - s) ** b)
    half_w /= max(half_w.max(), 1e-9)
    half_w *= width * length

    u = np.array([np.cos(angle), np.sin(angle)])
    v = np.array([-np.sin(angle), np.cos(angle)])
    spine = np.outer(s * length, u) + np.asarray(centre)
    side_a = spine + np.outer(half_w, v)
    side_b = spine - np.outer(half_w, v)
    return np.vstack([side_a, side_b[::-1]]), spine


def draw_leaf(ax, centre, angle, length, colour, alpha, z, veins=True, lw=0.9, **kw):
    outline, spine = leaf(centre, angle, length, **kw)
    ax.add_patch(
        Polygon(outline, closed=True, facecolor=colour, edgecolor="none",
                alpha=alpha, zorder=z, clip_on=False)
    )
    ax.add_patch(
        Polygon(outline, closed=True, fill=False, edgecolor=colour,
                linewidth=lw, alpha=min(alpha * 2.1, 0.85), zorder=z + 0.1, clip_on=False)
    )
    if veins:
        ax.plot(spine[:, 0], spine[:, 1], color=colour, lw=lw * 0.7,
                alpha=min(alpha * 1.8, 0.7), zorder=z + 0.2, clip_on=False,
                solid_capstyle="round")


def new_axes(w, h, facecolor=None):
    fig = plt.figure(figsize=(w, h), facecolor=facecolor or "none")
    ax = fig.add_axes([0, 0, 1, 1], facecolor=facecolor or "none")
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def save(fig, path, facecolor):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="svg", facecolor=facecolor, transparent=(facecolor is None),
                metadata={"Date": None})
    print("wrote", path.relative_to(OUT.parent.parent))
    if "--png" in sys.argv:
        fig.savefig(path.with_suffix(".png"), dpi=110, facecolor=facecolor or "white")
    plt.close(fig)


# -- banner ------------------------------------------------------------------

def banner(mode):
    W, H = 16.0, 4.4
    rng = np.random.default_rng(5)
    fig, ax = new_axes(W, H, SURFACE[mode])
    palette = BANNER_GREENS[mode]

    # A loose canopy: larger, paler leaves behind; smaller, stronger ones in front.
    for i in range(52):
        depth = i / 51.0
        length = rng.uniform(1.1, 2.3) * (1.25 - 0.4 * depth)
        centre = (rng.uniform(-1.5, W + 1.5), rng.uniform(-1.4, H + 1.0))
        angle = rng.uniform(0.15, np.pi - 0.15) + rng.choice([0, np.pi])
        colour = palette[min(int(depth * len(palette)), len(palette) - 1)]
        draw_leaf(ax, centre, angle, length, colour,
                  alpha=0.13 + 0.20 * depth, z=i,
                  a=rng.uniform(0.75, 1.0), b=rng.uniform(1.4, 2.0),
                  width=rng.uniform(0.28, 0.38), lw=0.7)
    save(fig, OUT / f"banner-{mode}.svg", SURFACE[mode])


# -- logo and favicon --------------------------------------------------------

def logo():
    fig, ax = new_axes(3.2, 3.2)
    # Three leaves from a shared base - a simple sprig.
    for angle, length, colour, z in [
        (np.deg2rad(90), 2.5, "#2f7d4f", 3),
        (np.deg2rad(142), 1.8, "#4a9d6e", 2),
        (np.deg2rad(38), 1.8, "#6fbf8e", 1),
    ]:
        draw_leaf(ax, (1.6, 0.35), angle, length, colour, alpha=0.42, z=z, lw=1.4)
    ax.plot([1.6, 1.6], [0.0, 0.5], color="#2f7d4f", lw=1.6, zorder=0,
            solid_capstyle="round", clip_on=False)
    save(fig, OUT / "logo.svg", None)


def favicon():
    fig, ax = new_axes(1.0, 1.0)
    draw_leaf(ax, (0.5, 0.08), np.deg2rad(90), 0.86, "#2f7d4f",
              alpha=0.55, z=1, lw=2.2, width=0.46)
    save(fig, OUT / "leaf_icon.svg", None)


# -- offering tiles ----------------------------------------------------------
# Each tile stays botanical rather than becoming an icon, but the arrangement
# differs so the four read as distinct at a glance.

def tile_refill(ax, W, H):
    # Nested arcs - a vessel being filled, drawn as concentric leaf outlines.
    for i, scale in enumerate([1.0, 0.72, 0.46]):
        draw_leaf(ax, (W / 2, H * 0.12), np.deg2rad(90), H * 0.78 * scale,
                  GREENS[i], alpha=0.30, z=i, lw=1.4, width=0.42)


def tile_laundry(ax, W, H):
    # Three leaves lying along flowing lines - water, movement.
    rng = np.random.default_rng(2)
    for i in range(3):
        y = H * (0.26 + 0.24 * i)
        xs = np.linspace(W * 0.06, W * 0.94, 160)
        ys = y + 0.16 * np.sin(xs * 1.5 + i)
        ax.plot(xs, ys, color=GREENS[i], lw=1.5, alpha=0.5, zorder=i,
                clip_on=False, solid_capstyle="round")
        draw_leaf(ax, (W * (0.3 + 0.2 * i), y), np.deg2rad(rng.uniform(5, 35)),
                  H * 0.3, GREENS[i], alpha=0.3, z=i + 0.5, lw=1.2)


def tile_sound(ax, W, H):
    # Concentric rings radiating from a single leaf.
    for i, r in enumerate([0.82, 0.62, 0.42]):
        theta = np.linspace(np.pi * 0.08, np.pi * 0.92, 160)
        ax.plot(W / 2 + r * W * 0.5 * np.cos(theta), H * 0.16 + r * H * 0.8 * np.sin(theta),
                color=GREENS[i], lw=1.5, alpha=0.45, zorder=i, clip_on=False,
                solid_capstyle="round")
    draw_leaf(ax, (W / 2, H * 0.12), np.deg2rad(90), H * 0.4, GREENS[0],
              alpha=0.38, z=5, lw=1.4)


def tile_space(ax, W, H):
    # Leaves curving inward - an enclosure, something held.
    for i, angle in enumerate([150, 110, 70, 30]):
        draw_leaf(ax, (W / 2, H * 0.1), np.deg2rad(angle), H * 0.74,
                  GREENS[i % len(GREENS)], alpha=0.26, z=i, lw=1.2, width=0.3)


def tiles():
    for name, fn in [("refill", tile_refill), ("laundry", tile_laundry),
                     ("sound", tile_sound), ("space", tile_space)]:
        W = H = 3.0
        fig, ax = new_axes(W, H)
        fn(ax, W, H)
        save(fig, OUT / "offerings" / f"{name}.svg", None)


for mode in ("light", "dark"):
    banner(mode)
logo()
favicon()
tiles()
