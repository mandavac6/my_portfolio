"""Runtime settings, read from the environment with sensible defaults."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
PROJECT_ROOT = BASE_DIR.parent


def _flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    reload: bool = _flag("RELOAD", default=False)
    # Cache-busting suffix for static assets; bump on deploy or set from a build id.
    asset_version: str = os.getenv("ASSET_VERSION", "1")
    # Absolute base URL, used for canonical/OpenGraph tags when deployed.
    site_url: str = os.getenv("SITE_URL", "")


settings = Settings()
