"""The chart maths runs on the server, so it can be checked directly."""

from __future__ import annotations

import math

import pytest

from app.charts import build_area_chart, build_bar_chart, build_heatmap, build_ring


class TestBarChart:
    def test_tallest_bar_is_full_height(self):
        chart = build_bar_chart((("a", 10.0, "ms"), ("b", 5.0, "ms")))
        assert chart.max_value == 10.0
        assert chart.bars[0].height_pct == 100.0
        assert chart.bars[1].height_pct == 50.0

    def test_display_appends_unit(self):
        chart = build_bar_chart((("a", 180.0, "ms"),))
        assert chart.bars[0].display == "180ms"

    def test_empty_input_rejected(self):
        with pytest.raises(ValueError):
            build_bar_chart(())


class TestAreaChart:
    def test_path_spans_the_plot_area(self):
        chart = build_area_chart((0.1, 0.5, 0.9), width=300, height=100)
        assert chart.line_path.startswith("M30.0,")
        assert len(chart.dots) == 3
        # First x is the left padding, last is width - right padding.
        assert chart.dots[0].x == 30.0
        assert chart.dots[-1].x == 290.0

    def test_lowest_value_sits_on_the_baseline(self):
        chart = build_area_chart((0.2, 0.8), height=100, padding=(30, 10, 10, 20))
        baseline = 100 - 20  # height - bottom padding
        assert chart.dots[0].y == pytest.approx(baseline)
        assert chart.dots[1].y == pytest.approx(10.0)  # top padding

    def test_flat_series_does_not_divide_by_zero(self):
        chart = build_area_chart((0.5, 0.5, 0.5))
        assert all(d.y == chart.dots[0].y for d in chart.dots)

    def test_area_path_closes_back_to_the_baseline(self):
        chart = build_area_chart((0.1, 0.9))
        assert chart.area_path.endswith("Z")

    def test_last_label_is_formatted(self):
        chart = build_area_chart((0.61, 0.924))
        assert chart.last_label == "92.4%"

    def test_single_point_rejected(self):
        with pytest.raises(ValueError):
            build_area_chart((0.5,))


class TestRing:
    def test_offset_matches_percentage(self):
        ring = build_ring("Python", "Languages", 75, "#fff", size=72, stroke=6)
        assert ring.radius == pytest.approx((72 - 6) / 2)
        assert ring.circumference == pytest.approx(2 * math.pi * ring.radius, abs=0.01)
        assert ring.offset == pytest.approx(ring.circumference * 0.25, abs=0.01)

    def test_full_ring_has_no_offset(self):
        assert build_ring("x", "y", 100, "#fff").offset == 0.0


class TestHeatmap:
    def test_shape(self):
        heat = build_heatmap(("Mon", "Tue"), cols=10)
        assert len(heat.cells) == 20
        assert len(heat.row_cells(0)) == 10

    def test_is_deterministic(self):
        a = build_heatmap(("Mon",), cols=8, seed=7)
        b = build_heatmap(("Mon",), cols=8, seed=7)
        assert [c.intensity for c in a.cells] == [c.intensity for c in b.cells]

    def test_opacity_stays_visible_and_bounded(self):
        heat = build_heatmap(("Mon", "Tue", "Wed"), cols=24)
        assert all(0.05 <= c.opacity <= 0.9 for c in heat.cells)
