"""Render the site to plain files in ``dist/``.

The page has no server-side behaviour beyond rendering, so it can be deployed
as static hosting (GitHub Pages, Netlify, Cloudflare Pages, Vercel) instead of
running uvicorn. Usage::

    python scripts/export_static.py            # -> dist/
    python scripts/export_static.py --out out  # -> out/
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import STATIC_DIR, settings  # noqa: E402
from app.content import SITE  # noqa: E402
from app.main import build_json_ld, page_context, templates  # noqa: E402


def render_index() -> str:
    context = page_context(request=None)
    context.pop("request", None)
    context["json_ld"] = build_json_ld()
    html = templates.get_template("index.html").render(**context)
    # Relative asset paths so the export also works from a subdirectory, or
    # opened straight off disk.
    return html.replace('href="/static/', 'href="static/').replace('src="/static/', 'src="static/')


def sitemap(base_url: str) -> str:
    base = base_url.rstrip("/") or ""
    urls = [f"{base}/"] + [f"{base}/#{s.slug}" for s in SITE.nav_sections]
    entries = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n</urlset>\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="dist", help="output directory (default: dist)")
    parser.add_argument(
        "--base-url",
        default=settings.site_url,
        help="absolute site URL, used for sitemap.xml and robots.txt",
    )
    args = parser.parse_args()

    out = (ROOT / args.out).resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    (out / "index.html").write_text(render_index(), encoding="utf-8")
    shutil.copytree(STATIC_DIR, out / "static")

    (out / "profile.json").write_text(
        json.dumps(
            {
                "name": SITE.profile.name,
                "title": SITE.profile.title,
                "email": SITE.profile.email,
                "location": SITE.profile.location,
                "summary": SITE.profile.summary,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    robots = ["User-agent: *", "Allow: /"]
    if args.base_url:
        robots.append(f"Sitemap: {args.base_url.rstrip('/')}/sitemap.xml")
        (out / "sitemap.xml").write_text(sitemap(args.base_url), encoding="utf-8")
    (out / "robots.txt").write_text("\n".join(robots) + "\n", encoding="utf-8")

    files = sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())
    total = sum((out / f).stat().st_size for f in files)
    print(f"exported {len(files)} files ({total / 1024:.0f} KB) to {out}")
    for f in files:
        print(f"  {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
