"""Contrast guardrails for the light theme.

A light theme fails quietly: a caramel that looked fine on the dark ground turns
into pale-on-white and nobody notices until someone tries to read it. These
tests put a floor under that, and check the stylesheet has not drifted away from
``app.theme``.
"""

from __future__ import annotations

import re

import pytest

from app import theme
from app.config import STATIC_DIR

AA_NORMAL = 4.5  # WCAG AA, text below 18pt
AA_LARGE = 3.0  # WCAG AA, large or bold display text


def _channel(value: int) -> float:
    c = value / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast(a: str, b: str) -> float:
    lo, hi = sorted((luminance(a), luminance(b)))
    return (hi + 0.05) / (lo + 0.05)


class TestContrastHelper:
    def test_black_on_white_is_the_maximum(self):
        assert contrast("#000000", "#ffffff") == pytest.approx(21.0, abs=0.01)

    def test_identical_colours_have_no_contrast(self):
        assert contrast("#7a4f2a", "#7a4f2a") == pytest.approx(1.0)


class TestReadability:
    @pytest.mark.parametrize("ink", theme.INK)
    def test_ink_ramp_is_readable_on_paper(self, ink: str):
        assert contrast(ink, theme.CANVAS) >= AA_NORMAL

    @pytest.mark.parametrize("name,accent", [
        ("HONEY", theme.HONEY),
        ("CARAMEL_MID", theme.CARAMEL_MID),
        ("GOLD", theme.GOLD),
        ("AMBER", theme.AMBER),
        ("BRONZE", theme.BRONZE),
        ("UMBER", theme.UMBER),
    ])
    def test_accent_ink_carries_text_on_both_grounds(self, name: str, accent):
        # Accent ink labels sit on cards (white) and on the page (paper).
        assert contrast(accent.ink, theme.SURFACE) >= AA_NORMAL, name
        assert contrast(accent.ink, theme.CANVAS) >= AA_NORMAL, name

    @pytest.mark.parametrize("name,accent", [
        ("HONEY", theme.HONEY),
        ("CARAMEL_MID", theme.CARAMEL_MID),
        ("GOLD", theme.GOLD),
        ("AMBER", theme.AMBER),
        ("BRONZE", theme.BRONZE),
        ("UMBER", theme.UMBER),
    ])
    def test_domain_badge_reverses_out_in_white(self, name: str, accent):
        # .domain-badge paints white text on a solid accent-ink background.
        assert contrast("#ffffff", accent.ink) >= AA_NORMAL, name

    @pytest.mark.parametrize("name,accent", [
        ("HONEY", theme.HONEY),
        ("CARAMEL_MID", theme.CARAMEL_MID),
        ("GOLD", theme.GOLD),
        ("AMBER", theme.AMBER),
        ("BRONZE", theme.BRONZE),
        ("UMBER", theme.UMBER),
    ])
    def test_accent_fills_stay_pale_enough_to_wash(self, name: str, accent):
        # Fills are layered translucently over white; anything this dark would
        # read as grey-brown rather than warm.
        assert luminance(accent.start) > 0.4, f"{name} start is too dark for a wash"
        assert luminance(accent.end) > luminance(accent.start), f"{name} gradient inverted"

    @pytest.mark.parametrize("index", sorted(theme.TEXT))
    def test_text_ramp(self, index: int):
        colour = theme.TEXT[index]
        if index <= theme.TEXT_AA_MAX_INDEX:
            assert contrast(colour, theme.CANVAS) >= AA_NORMAL
        else:
            # Decorative tones still have to be visible at all.
            assert contrast(colour, theme.CANVAS) >= 1.6

    def test_primary_button_label_is_readable(self):
        # .btn-primary is white on a c700 -> c600 gradient; check the light end.
        assert contrast("#ffffff", theme.CARAMEL[600]) >= AA_LARGE

    def test_page_is_light(self):
        assert luminance(theme.CANVAS) > 0.85
        assert luminance(theme.SURFACE) > luminance(theme.CANVAS)


class TestStylesheetMatchesTheme:
    """The stylesheet restates these tokens; make sure it restates them correctly."""

    @staticmethod
    def _root_vars() -> dict[str, str]:
        css = (STATIC_DIR / "css" / "styles.css").read_text(encoding="utf-8")
        block = css.split(":root {", 1)[1].split("}", 1)[0]
        return dict(re.findall(r"--([\w-]+):\s*([^;]+);", block))

    def test_canvas_and_surface_agree(self):
        root = self._root_vars()
        assert root["canvas"].strip() == theme.CANVAS
        assert root["surface"].strip() == theme.SURFACE
        assert root["sunken"].strip() == theme.SUNKEN

    @pytest.mark.parametrize("step", [50, 100, 200, 300, 400, 500, 600, 700, 800, 900])
    def test_caramel_ramp_agrees(self, step: int):
        assert self._root_vars()[f"c{step}"].strip() == theme.CARAMEL[step]

    @pytest.mark.parametrize("index", sorted(theme.TEXT))
    def test_text_ramp_agrees(self, index: int):
        assert self._root_vars()[f"t{index}"].strip() == theme.TEXT[index]
