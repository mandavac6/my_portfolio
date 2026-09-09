"""Colour tokens shared by the Python content modules and the stylesheet.

The site is a **light** theme: warm paper ground, caramel accents, near-black
warm ink. The stylesheet declares the same values as CSS custom properties;
these exist so content modules can hand a template an :class:`Accent` without
hard-coding hex strings all over the place.

Note which end of the caramel ramp does what here. On a light ground the pale
tints (100-300) are *fills* — washes behind cards, bar gradients, badges — and
the deep tones (600-900) are *ink*: anything that has to be read as text. Every
:class:`Accent` therefore carries both.
"""

from __future__ import annotations

from app.models import Accent

# Surfaces
CANVAS = "#faf7f2"  # warm paper, the page ground
SURFACE = "#ffffff"  # cards and panels
SUNKEN = "#f3ede4"  # inset wells inside a card

# Caramel ramp, light to deep
CARAMEL = {
    50: "#fdf8ef",
    100: "#faedcd",
    200: "#f5dba8",
    300: "#ecc882",
    400: "#d4a373",
    500: "#c4935a",
    600: "#a06535",
    700: "#7a4f2a",
    800: "#5a3a1e",
    900: "#3d2714",
}

# Ink tones that clear 4.5:1 on the paper ground, deepest first.
INK = ("#4a2f16", "#5a3a1e", "#6b4423", "#7a4f2a", "#875730", "#8f5c2c", "#96602f")

# Warm neutral text ramp, darkest first. Mirrors --t0..--t6 in the stylesheet;
# tests/test_theme.py fails if the two drift apart.
TEXT = {
    0: "#1a1411",  # headings
    1: "#2a221d",
    2: "#3d332c",  # card titles, strong body
    3: "#55483d",  # body copy
    4: "#7a6a5c",  # muted labels
    5: "#9c8b7b",  # decorative only, below AA
    6: "#bcab99",  # decorative only, below AA
}

# Ramp entries above this index are decorative and exempt from the AA check.
TEXT_AA_MAX_INDEX = 4

# Named accents used across sections.
#
# The fills stay in the pale 200-400 band: a card wash is a translucent layer
# over white, and anything darker than this turns grey-brown rather than warm.
# All the contrast lives in ``ink``, which steps down the ramp so the six cards
# still read as distinct.
HONEY = Accent(start="#f5dba8", end="#faedcd", ink="#96602f")
CARAMEL_MID = Accent(start="#ecc882", end="#f7e3bb", ink="#8f5c2c")
GOLD = Accent(start="#f0d295", end="#faedcd", ink="#8a5628")
AMBER = Accent(start="#e8bf85", end="#f7e6c8", ink="#7a4f2a")
BRONZE = Accent(start="#ddb078", end="#f3ddb8", ink="#6b4423")
UMBER = Accent(start="#d4a373", end="#eed3ab", ink="#5a3a1e")

ACCENT_CYCLE = (CARAMEL_MID, GOLD, AMBER, BRONZE, UMBER, HONEY)
