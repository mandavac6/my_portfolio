"""Pure-Python geometry for the SVG charts on the page.

The original site computed these paths in the browser. Doing it here means the
markup arrives complete: the charts are visible without JavaScript, and the
maths is unit-testable.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Bar:
    label: str
    value: float
    unit: str = ""
    height_pct: float = 0.0

    @property
    def display(self) -> str:
        text = f"{self.value:g}"
        return f"{text}{self.unit}"


@dataclass(frozen=True)
class BarChart:
    bars: tuple[Bar, ...]
    max_value: float


def build_bar_chart(items: Sequence[tuple[str, float, str]]) -> BarChart:
    """``items`` is a sequence of ``(label, value, unit)`` triples."""
    if not items:
        raise ValueError("bar chart needs at least one bar")
    max_value = max(value for _, value, _ in items)
    bars = tuple(
        Bar(label=label, value=value, unit=unit, height_pct=round(value / max_value * 100, 2))
        for label, value, unit in items
    )
    return BarChart(bars=bars, max_value=max_value)


@dataclass(frozen=True)
class Dot:
    x: float
    y: float
    value: float


@dataclass(frozen=True)
class GridLine:
    y: float


@dataclass(frozen=True)
class AxisLabel:
    text: str
    y: float


@dataclass(frozen=True)
class AreaChart:
    width: float
    height: float
    line_path: str
    area_path: str
    dots: tuple[Dot, ...]
    grid_lines: tuple[GridLine, ...]
    y_labels: tuple[AxisLabel, ...]
    last: Dot
    last_label: str


def build_area_chart(
    values: Sequence[float],
    y_labels: Sequence[str] = (),
    width: float = 300.0,
    height: float = 100.0,
    padding: tuple[float, float, float, float] = (30.0, 10.0, 10.0, 20.0),
    value_format: str = "{:.1%}",
) -> AreaChart:
    """Build the line + filled-area path for a small trend chart.

    ``padding`` is ``(left, right, top, bottom)`` in viewBox units.
    """
    if len(values) < 2:
        raise ValueError("area chart needs at least two points")

    left, right, top, bottom = padding
    inner_w = width - left - right
    inner_h = height - top - bottom

    lo, hi = min(values), max(values)
    span = (hi - lo) or 1.0

    xs = [left + (i / (len(values) - 1)) * inner_w for i in range(len(values))]
    ys = [top + inner_h - ((v - lo) / span) * inner_h for v in values]

    line_path = " ".join(
        f"{'M' if i == 0 else 'L'}{x:.1f},{ys[i]:.1f}" for i, x in enumerate(xs)
    )
    baseline = top + inner_h
    area_path = f"{line_path} L{xs[-1]:.1f},{baseline:.1f} L{left:.1f},{baseline:.1f} Z"

    grid = tuple(GridLine(y=round(top + inner_h * (1 - t), 2)) for t in (0.25, 0.5, 0.75, 1.0))

    labels: tuple[AxisLabel, ...] = ()
    if y_labels:
        step = inner_h / max(len(y_labels) - 1, 1)
        labels = tuple(
            AxisLabel(text=text, y=round(top + inner_h - i * step + 3, 2))
            for i, text in enumerate(y_labels)
        )

    dots = tuple(Dot(x=round(x, 2), y=round(ys[i], 2), value=values[i]) for i, x in enumerate(xs))

    return AreaChart(
        width=width,
        height=height,
        line_path=line_path,
        area_path=area_path,
        dots=dots,
        grid_lines=grid,
        y_labels=labels,
        last=dots[-1],
        last_label=value_format.format(values[-1]),
    )


@dataclass(frozen=True)
class Ring:
    label: str
    sublabel: str
    pct: int
    color: str
    size: float
    stroke: float
    radius: float
    circumference: float
    offset: float

    @property
    def center(self) -> float:
        return self.size / 2


def build_ring(
    label: str,
    sublabel: str,
    pct: int,
    color: str,
    size: float = 72.0,
    stroke: float = 6.0,
) -> Ring:
    radius = (size - stroke) / 2
    circumference = 2 * math.pi * radius
    return Ring(
        label=label,
        sublabel=sublabel,
        pct=pct,
        color=color,
        size=size,
        stroke=stroke,
        radius=round(radius, 3),
        circumference=round(circumference, 3),
        offset=round(circumference * (1 - pct / 100), 3),
    )


@dataclass(frozen=True)
class HeatCell:
    row: int
    col: int
    intensity: float
    delay_ms: int

    @property
    def opacity(self) -> float:
        return round(0.05 + self.intensity * 0.85, 3)


@dataclass(frozen=True)
class Heatmap:
    rows: tuple[str, ...]
    cols: int
    cells: tuple[HeatCell, ...]

    def row_cells(self, row: int) -> tuple[HeatCell, ...]:
        return tuple(c for c in self.cells if c.row == row)


def build_heatmap(row_labels: Sequence[str], cols: int = 24, seed: int = 20260909) -> Heatmap:
    """Deterministic activity grid.

    Seeded so the server and any static export agree -- the original picked
    fresh random numbers on every render, which flickered on rehydration.
    """
    rng = random.Random(seed)
    cells = []
    for r in range(len(row_labels)):
        for c in range(cols):
            # Weekday working hours are busier than the tails of the day.
            time_of_day = math.sin(math.pi * (c + 0.5) / cols) ** 1.5
            noise = rng.random()
            intensity = min(1.0, 0.15 + 0.65 * time_of_day * noise + 0.25 * noise**3)
            cells.append(
                HeatCell(
                    row=r,
                    col=c,
                    intensity=round(intensity, 3),
                    delay_ms=int((r * cols + c) * 3),
                )
            )
    return Heatmap(rows=tuple(row_labels), cols=cols, cells=tuple(cells))
