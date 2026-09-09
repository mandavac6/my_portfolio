"""Resume content, assembled into a single :class:`~app.models.SiteContent`.

Each module in this package owns one slice of the page. ``SITE`` is built once
at import time and treated as immutable for the life of the process.
"""

from __future__ import annotations

from app.content import analytics, experience, profile, projects, skills
from app.models import SiteContent

SITE = SiteContent(
    profile=profile.PROFILE,
    sections=profile.SECTIONS,
    hero_stats=profile.HERO_STATS,
    hero_tickers=profile.HERO_TICKERS,
    hero_headline_metric=profile.HERO_HEADLINE_METRIC,
    hero_sparkline=profile.HERO_SPARKLINE,
    hero_stages=profile.HERO_STAGES,
    hero_badges=profile.HERO_BADGES,
    skill_categories=skills.CATEGORIES,
    tech_stack=skills.TECH_STACK,
    projects=projects.PROJECTS,
    roles=experience.ROLES,
    education=experience.EDUCATION,
    certifications=experience.CERTIFICATIONS,
    about_lead=profile.ABOUT_LEAD,
    about_paragraphs=profile.ABOUT_PARAGRAPHS,
    quick_facts=profile.QUICK_FACTS,
    counters=analytics.COUNTERS,
    role_preferences=profile.ROLE_PREFERENCES,
    socials=profile.SOCIALS,
    year=profile.YEAR,
    nav_sections=tuple(s for s in profile.SECTIONS if s.in_nav),
)

__all__ = ["SITE", "analytics", "experience", "profile", "projects", "skills"]
