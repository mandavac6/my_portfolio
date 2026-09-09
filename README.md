# Naveen Mandava — Portfolio

Personal portfolio site for **Naveen Mandava**, AI/ML Engineer. Python top to
bottom: FastAPI serves one Jinja2-rendered page, and every number, label, and
SVG path in the HTML comes from typed Python data. Warm light theme — paper
ground, caramel accents, near-black warm ink.


## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows;  source .venv/bin/activate on macOS/Linux
pip install -r requirements-dev.txt

python run.py                    # http://127.0.0.1:8000
```

`run.py` reads `HOST`, `PORT`, and `RELOAD` from the environment (see
`.env.example`). For production, drive uvicorn directly:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Layout

```
app/
  models.py            frozen dataclasses describing every kind of content
  theme.py             the caramel palette, shared by content and stylesheet
  charts.py            pure-Python SVG geometry (bars, area chart, rings, heatmap)
  config.py            settings from the environment
  main.py              FastAPI app, routes, schema.org JSON-LD
  content/
    profile.py         name, headline, hero dashboard, about, contact
    skills.py          skill matrix and the full technology stack
    projects.py        selected projects with problem / contribution / outcome
    experience.py      roles, education, certifications
    analytics.py       the "By the Numbers" section
  templates/
    base.html          document shell, meta tags, structured data
    index.html         section order
    _macros.html       section headings, progress rings, tickers
    sections/*.html    one file per section
  static/
    css/styles.css     the entire design system, no build step
    js/main.js         motion only — nav, reveals, counters, particles
scripts/export_static.py   render the site to dist/ for static hosting
tests/                     pytest suite (content, charts, rendered page)
```

### Editing content

All copy lives in `app/content/`. Nothing else needs to change:

| To change | Edit |
| --- | --- |
| Name, headline, summary, contact | `content/profile.py` |
| Skill categories, levels, tech chips | `content/skills.py` |
| Projects | `content/projects.py` |
| Jobs, education, certifications | `content/experience.py` |
| Counters, charts, latency table | `content/analytics.py` |
| Colours | `theme.py` and the `:root` block in `static/css/styles.css` |

Colours live in two places by necessity — Python hands accents to templates, CSS
paints everything else — so `tests/test_theme.py` fails if the two drift apart,
and puts a WCAG AA floor under every tone that carries text. On a light ground
that check earns its keep: a caramel that read fine on the old dark theme turns
into pale-on-white without anyone noticing.

Each accent carries a pale `start`/`end` pair for fills and a deep `ink` for
text. Keep new accents to that shape; the tests enforce both halves.

`profile.py` has `linkedin` and `github` set to `None`. Fill either in and the
link appears automatically in About and in the contact card — no template edit.

Skill levels are self-assessed and validated to `0..100`; the suite fails if one
falls outside that range.

## Tests

```bash
pytest
```

105 tests covering the chart geometry, content invariants (unique slugs, every
nav entry resolving to a section, latency rows that actually improve), the
rendered page (every section, role, and project present; no unrendered template
syntax; charts present in the server-rendered markup), and the palette (contrast
ratios, and the stylesheet agreeing with `theme.py`).

## Deploying

**Static hosting** — the page has no server-side behaviour beyond rendering, so
it exports to plain files:

```bash
python scripts/export_static.py --base-url https://your-domain.com
```

That writes `dist/` (index.html, static assets, robots.txt, sitemap.xml). Point
GitHub Pages, Netlify, Cloudflare Pages, or Vercel at it. `vercel.json` already
runs this as the build command.

`.github/workflows/deploy.yml` does this on every push to `main`: installs
dependencies, runs the test suite, exports the site with `ASSET_VERSION` set to
the commit SHA, checks the output, then publishes to GitHub Pages. A failing
test blocks the deploy. Enable it once under **Settings -> Pages -> Source ->
GitHub Actions**.

**As a service** — `Dockerfile` builds a uvicorn image:

```bash
docker build -t portfolio .
docker run -p 8000:8000 portfolio
```

Set `SITE_URL` so canonical, OpenGraph, and sitemap URLs are absolute, and bump
`ASSET_VERSION` on deploy to bust the CSS/JS cache.

## Routes

| Route | Purpose |
| --- | --- |
| `/` | the page |
| `/api/profile` | the resume as JSON |
| `/api/docs` | OpenAPI docs |
| `/healthz` | liveness probe |
| `/robots.txt` | crawler policy |

## Notes on the front end

- **No build step and no CSS framework.** `styles.css` is a hand-written design
  system driven by custom properties; per-card accents are passed from Python as
  inline `--accent-start` / `--accent-end` / `--accent-ink`.
- **Templates carry no colours.** Chart strokes, ring tracks, heatmap cells and
  the particle field all read their colours from CSS custom properties, so
  retheming means editing `theme.py` and the `:root` block, nothing else.
- **Charts render on the server.** `app/charts.py` computes bar heights, the
  area-chart path, ring dash offsets, and the heatmap, so the charts are in the
  HTML and are unit-tested. The heatmap is seeded, so a rebuild produces the
  same grid.
- **JavaScript is optional.** Scripting adds the scroll reveals, count-ups,
  cycling dashboard values, the particle field, and the project expanders. With
  JS off, `.no-js` rules put everything in its finished state.
- **Motion is opt-out.** `prefers-reduced-motion` disables animation and drops
  the particle canvas.
