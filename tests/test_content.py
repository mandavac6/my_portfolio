"""Guardrails on the resume content itself.

These catch the mistakes that are easy to make when editing content by hand:
a nav link with no section, a skill level outside 0-100, a role with no
highlights, contact details drifting out of sync.
"""

from __future__ import annotations

import pytest

from app.content import SITE, analytics
from app.models import LatencyRow, Skill


class TestProfile:
    def test_identity(self):
        assert SITE.profile.name == "Naveen Mandava"
        assert SITE.profile.initials == "NM"
        assert SITE.profile.email == "naveen.mandava1999@gmail.com"

    def test_mailto_and_tel_are_well_formed(self):
        assert SITE.profile.mailto == "mailto:naveen.mandava1999@gmail.com"
        assert SITE.profile.tel == "tel:9379867149"

    def test_headline_has_a_gradient_segment(self):
        assert any(seg.gradient for seg in SITE.profile.tagline)


class TestSections:
    def test_every_nav_entry_resolves_to_a_section(self):
        for section in SITE.nav_sections:
            assert SITE.section(section.slug) is section

    def test_slugs_are_unique(self):
        slugs = [s.slug for s in SITE.sections]
        assert len(slugs) == len(set(slugs))

    def test_unknown_slug_raises(self):
        with pytest.raises(KeyError):
            SITE.section("nope")


class TestSkills:
    def test_levels_are_percentages(self):
        with pytest.raises(ValueError):
            Skill("Bad", 140)

    def test_every_category_has_skills(self):
        assert SITE.skill_categories
        for cat in SITE.skill_categories:
            assert cat.skills, f"{cat.title} has no skills"
            assert cat.accent.start.startswith("#")

    def test_tech_stack_has_no_duplicates(self):
        assert len(SITE.tech_stack) == len(set(SITE.tech_stack))


class TestProjects:
    def test_slugs_unique_and_complete(self):
        slugs = [p.slug for p in SITE.projects]
        assert len(slugs) == len(set(slugs))
        for project in SITE.projects:
            assert project.metrics, f"{project.slug} has no metrics"
            assert project.problem and project.contribution and project.outcome


class TestExperience:
    def test_roles_are_newest_first(self):
        assert SITE.roles[0].company == "Kaiser Permanente"
        assert SITE.roles[-1].company == "Reliance"

    def test_every_role_has_highlights_and_tags(self):
        for role in SITE.roles:
            assert role.highlights, f"{role.company} has no highlights"
            assert role.tags, f"{role.company} has no tags"

    def test_education_and_certifications_present(self):
        assert len(SITE.education) == 2
        assert {c.name for c in SITE.certifications} == {
            "Azure AI Fundamentals",
            "Certified Kubernetes Administrator",
        }


class TestLatencyRow:
    def test_ratio_is_the_after_share_of_before(self):
        row = LatencyRow(label="x", before_s=100.0, after_s=25.0)
        assert row.ratio_pct == pytest.approx(25.0)

    def test_ratio_never_collapses_to_invisible(self):
        row = LatencyRow(label="x", before_s=86400.0, after_s=1.0)
        assert row.ratio_pct == 1.0

    @pytest.mark.parametrize(
        "seconds,expected",
        [(0.25, "250ms"), (3.0, "3s"), (45.0, "45s"), (120.0, "2m"), (7200.0, "2h"), (172800.0, "2d")],
    )
    def test_humanised_labels(self, seconds, expected):
        assert LatencyRow(label="x", before_s=seconds, after_s=seconds).before_label == expected

    def test_all_rows_improve(self):
        for row in analytics.LATENCY_ROWS:
            assert row.after_s < row.before_s, row.label


class TestAnalytics:
    def test_counters_have_labels(self):
        assert SITE.counters
        for counter in SITE.counters:
            assert counter.label

    def test_latency_budget_roughly_matches_the_p95_counter(self):
        total_ms = sum(bar.value for bar in analytics.LATENCY_BUDGET.bars)
        p95 = next(c for c in SITE.counters if c.label == "p95 Latency")
        assert total_ms <= p95.target * 1000
