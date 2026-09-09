"""Typed content model for the portfolio.

Everything the page renders is one of these dataclasses. They are frozen so a
section cannot be mutated halfway through a request, and they carry only
presentation-neutral data -- colours live in :class:`Accent`, which templates
turn into CSS custom properties.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Accent:
    """A card accent, rendered into CSS custom properties.

    ``start``/``end`` are the gradient stops used for fills — bars, badges,
    timeline dots, the wash behind a card. ``ink`` is the darker companion used
    wherever the accent has to carry *text*, so small labels stay legible on the
    light background instead of inheriting a pale fill colour.
    """

    start: str
    end: str
    ink: str

    @property
    def css(self) -> str:
        return f"--accent-start:{self.start};--accent-end:{self.end};--accent-ink:{self.ink}"

    @property
    def gradient(self) -> str:
        return f"linear-gradient(135deg, {self.start}, {self.end})"


@dataclass(frozen=True)
class Link:
    label: str
    href: str
    value: str = ""
    icon: str = ""

    @property
    def external(self) -> bool:
        return self.href.startswith("http")


@dataclass(frozen=True)
class Stat:
    """A headline number: ``value`` is already formatted for display."""

    value: str
    label: str
    sub: str = ""


@dataclass(frozen=True)
class Counter:
    """A number that animates up from zero when it scrolls into view."""

    target: float
    label: str
    sub: str = ""
    suffix: str = ""
    prefix: str = ""
    decimals: int = 0


@dataclass(frozen=True)
class Skill:
    name: str
    level: int  # 0-100, self assessed

    def __post_init__(self) -> None:
        if not 0 <= self.level <= 100:
            raise ValueError(f"{self.name}: level must be 0-100, got {self.level}")


@dataclass(frozen=True)
class SkillCategory:
    title: str
    icon: str
    accent: Accent
    skills: tuple[Skill, ...]


@dataclass(frozen=True)
class Metric:
    """A small before/after style result attached to a project."""

    value: str
    label: str
    sub: str = ""


@dataclass(frozen=True)
class Project:
    slug: str
    title: str
    domain: str
    summary: str
    accent: Accent
    tags: tuple[str, ...]
    metrics: tuple[Metric, ...]
    problem: str
    contribution: str
    outcome: str


@dataclass(frozen=True)
class Role:
    title: str
    company: str
    location: str
    period: str
    domain: str
    accent: Accent
    highlights: tuple[str, ...]
    tags: tuple[str, ...]


@dataclass(frozen=True)
class Education:
    degree: str
    school: str
    location: str
    period: str


@dataclass(frozen=True)
class Certification:
    name: str
    issuer: str


@dataclass(frozen=True)
class Ticker:
    """A dashboard value that cycles through a few plausible readings."""

    label: str
    values: tuple[str, ...]
    icon: str = ""
    interval_ms: int = 2400


@dataclass(frozen=True)
class PipelineStage:
    label: str
    icon: str
    sub: str = ""
    progress: int = 100


@dataclass(frozen=True)
class TaglineSegment:
    """One piece of the hero headline."""

    text: str
    gradient: bool = False
    break_after: bool = False


@dataclass(frozen=True)
class Profile:
    name: str
    initials: str
    title: str
    tagline: tuple[TaglineSegment, ...]
    summary: str
    availability: str
    location: str
    email: str
    phone: str
    linkedin: Optional[str] = None
    github: Optional[str] = None
    resume_path: Optional[str] = None

    @property
    def mailto(self) -> str:
        return f"mailto:{self.email}"

    @property
    def tel(self) -> str:
        return "tel:" + self.phone.replace("-", "").replace(" ", "")


@dataclass(frozen=True)
class LatencyRow:
    """Before/after latency, stored in seconds so the bar widths stay honest."""

    label: str
    before_s: float
    after_s: float

    @property
    def ratio_pct(self) -> float:
        if self.before_s <= 0:
            return 0.0
        return max((self.after_s / self.before_s) * 100.0, 1.0)

    @staticmethod
    def _humanise(seconds: float) -> str:
        if seconds < 1:
            return f"{seconds * 1000:.0f}ms"
        if seconds < 90:
            return f"{seconds:.0f}s" if seconds >= 10 else f"{seconds:g}s"
        if seconds < 3600:
            return f"{seconds / 60:.0f}m"
        if seconds < 86400:
            return f"{seconds / 3600:.0f}h"
        return f"{seconds / 86400:.0f}d"

    @property
    def before_label(self) -> str:
        return self._humanise(self.before_s)

    @property
    def after_label(self) -> str:
        return self._humanise(self.after_s)


@dataclass(frozen=True)
class Section:
    """Nav entry / section heading pair."""

    slug: str
    nav_label: str
    eyebrow: str
    title: str
    title_accent: str
    blurb: str = ""
    in_nav: bool = True


@dataclass(frozen=True)
class SiteContent:
    """Everything the index template needs, assembled once at import time."""

    profile: Profile
    sections: tuple[Section, ...]
    hero_stats: tuple[Stat, ...]
    hero_tickers: tuple[Ticker, ...]
    hero_headline_metric: Ticker
    hero_sparkline: tuple[float, ...]
    hero_stages: tuple[PipelineStage, ...]
    hero_badges: tuple[Stat, ...]
    skill_categories: tuple[SkillCategory, ...]
    tech_stack: tuple[str, ...]
    projects: tuple[Project, ...]
    roles: tuple[Role, ...]
    education: tuple[Education, ...]
    certifications: tuple[Certification, ...]
    about_paragraphs: tuple[str, ...]
    about_lead: str
    quick_facts: tuple[Link, ...]
    counters: tuple[Counter, ...]
    role_preferences: tuple[str, ...]
    socials: tuple[Link, ...]
    year: int = 2026
    nav_sections: tuple[Section, ...] = field(default_factory=tuple)

    def section(self, slug: str) -> Section:
        for s in self.sections:
            if s.slug == slug:
                return s
        raise KeyError(f"unknown section: {slug}")
