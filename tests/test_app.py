"""End-to-end checks on the rendered page and the JSON API."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.content import SITE
from app.main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="module")
def page(client: TestClient) -> str:
    response = client.get("/")
    assert response.status_code == 200
    return response.text


class TestPage:
    def test_title_and_description(self, page: str):
        assert "<title>Naveen Mandava — AI/ML Engineer</title>" in page
        assert SITE.profile.summary in page

    def test_every_section_is_rendered(self, page: str):
        for section in SITE.sections:
            assert f'id="{section.slug}"' in page, section.slug

    def test_every_role_appears(self, page: str):
        for role in SITE.roles:
            assert role.company in page
            assert role.period in page

    def test_every_project_appears(self, page: str):
        for project in SITE.projects:
            assert project.title in page
            assert f'id="detail-{project.slug}"' in page

    def test_contact_details_present(self, page: str):
        assert SITE.profile.mailto in page
        assert SITE.profile.phone in page

    def test_no_unrendered_template_syntax(self, page: str):
        assert "{{" not in page and "{%" not in page

    def test_emoji_entities_are_not_double_escaped(self, page: str):
        assert "&amp;#" not in page

    def test_charts_rendered_server_side(self, page: str):
        # SVG path data and bar heights must be in the markup, not computed in JS.
        assert 'class="area-line"' in page
        assert "--dash-offset:" in page
        assert "--h:" in page

    def test_structured_data_included(self, page: str):
        assert '"@type": "Person"' in page
        assert "Kaiser Permanente" in page


class TestRoutes:
    def test_health(self, client: TestClient):
        assert client.get("/healthz").text == "ok"

    def test_robots(self, client: TestClient):
        assert "User-agent: *" in client.get("/robots.txt").text

    def test_static_assets_served(self, client: TestClient):
        assert client.get("/static/css/styles.css").status_code == 200
        assert client.get("/static/js/main.js").status_code == 200

    def test_profile_api_shape(self, client: TestClient):
        data = client.get("/api/profile").json()
        assert data["profile"]["name"] == "Naveen Mandava"
        assert len(data["experience"]) == len(SITE.roles)
        assert len(data["projects"]) == len(SITE.projects)
        assert data["experience"][0]["company"] == "Kaiser Permanente"
