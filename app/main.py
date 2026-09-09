"""FastAPI application: one rendered page, plus a small read-only JSON API.

The page is fully server rendered — every number, path, and label in the HTML
comes from :mod:`app.content`. The JavaScript in ``static/js/main.js`` only adds
motion on top of markup that already stands on its own.
"""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import __version__
from app.config import STATIC_DIR, TEMPLATES_DIR, settings
from app.content import SITE, analytics

app = FastAPI(
    title=f"{SITE.profile.name} — Portfolio",
    description=SITE.profile.summary,
    version=__version__,
    docs_url="/api/docs",
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
templates.env.globals.update(
    site=SITE,
    analytics=analytics,
    asset_version=settings.asset_version,
    site_url=settings.site_url,
)


def build_json_ld() -> str:
    """schema.org Person markup, so the page describes itself to crawlers."""
    person: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": SITE.profile.name,
        "jobTitle": SITE.profile.title,
        "email": SITE.profile.email,
        "telephone": SITE.profile.phone,
        "description": SITE.profile.summary,
        "address": {"@type": "PostalAddress", "addressLocality": SITE.profile.location},
        "worksFor": {"@type": "Organization", "name": SITE.roles[0].company},
        "alumniOf": [
            {"@type": "EducationalOrganization", "name": e.school} for e in SITE.education
        ],
        "knowsAbout": list(SITE.tech_stack),
        "hasCredential": [c.name for c in SITE.certifications],
    }
    if SITE.profile.linkedin or SITE.profile.github:
        person["sameAs"] = [u for u in (SITE.profile.linkedin, SITE.profile.github) if u]
    if settings.site_url:
        person["url"] = settings.site_url
    return json.dumps(person, indent=2)


JSON_LD = build_json_ld()


def page_context(request: Request | None = None) -> dict[str, Any]:
    """Everything ``index.html`` renders from."""
    return {
        "request": request,
        "site": SITE,
        "profile": SITE.profile,
        "analytics": analytics,
        "asset_version": settings.asset_version,
        "site_url": settings.site_url,
        "json_ld": JSON_LD,
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    context = page_context(request)
    context.pop("request", None)
    return templates.TemplateResponse(request, "index.html", context)


@app.get("/healthz", response_class=PlainTextResponse)
async def healthz() -> str:
    return "ok"


def _serialise(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return {k: _serialise(v) for k, v in asdict(value).items()}
    if isinstance(value, (list, tuple)):
        return [_serialise(v) for v in value]
    if isinstance(value, dict):
        return {k: _serialise(v) for k, v in value.items()}
    return value


@app.get("/api/profile")
async def api_profile() -> JSONResponse:
    """The resume content as JSON — handy for a recruiter tool or an agent."""
    return JSONResponse(
        {
            "profile": _serialise(SITE.profile),
            "skills": _serialise(SITE.skill_categories),
            "projects": _serialise(SITE.projects),
            "experience": _serialise(SITE.roles),
            "education": _serialise(SITE.education),
            "certifications": _serialise(SITE.certifications),
        }
    )


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots() -> str:
    lines = ["User-agent: *", "Allow: /"]
    if settings.site_url:
        lines.append(f"Sitemap: {settings.site_url.rstrip('/')}/sitemap.xml")
    return "\n".join(lines) + "\n"
