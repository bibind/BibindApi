"""Website controllers for Bibind public site.

This file implements a minimal subset of the specification. The goal is to
provide lightweight routes that can be tested without running a full Odoo
stack.  Real deployments should expand on these handlers with full features
such as caching, error handling and templating as described in the
specification.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from odoo import http, _

# Optional imports from bibind_core.  The try/except allows the module to be
# imported in environments where bibind_core is not available (e.g. tests in
# this kata repository).
try:  # pragma: no cover - library availability depends on environment
    from odoo.addons.bibind_core.lib.api_client import ApiClient
    from odoo.addons.bibind_core.lib.param_store import ParamStore
except Exception:  # pragma: no cover - executed when bibind_core is missing
    ApiClient = object  # type: ignore

    class ParamStore:  # type: ignore
        """Fallback ParamStore used when bibind_core is unavailable."""

        @staticmethod
        def get_param(key: str, default: Optional[str] = None) -> Optional[str]:
            return default


_logger = logging.getLogger("bibind")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@dataclass
class CacheItem:
    """A tiny in-memory cache record."""

    timestamp: float
    data: Any


class _TTLCache:
    """Simple in-memory cache with a TTL per key."""

    def __init__(self, ttl: int = 600) -> None:
        self.ttl = ttl
        self._store: Dict[str, CacheItem] = {}

    def get(self, key: str) -> Optional[Any]:
        item = self._store.get(key)
        if item and (time.time() - item.timestamp) < self.ttl:
            return item.data
        return None

    def set(self, key: str, value: Any) -> None:
        self._store[key] = CacheItem(timestamp=time.time(), data=value)


_cache = _TTLCache()


def _load_jobs_data() -> list[Dict[str, Any]]:
    """Load job definitions from the static JSON file."""

    cached = _cache.get("jobs")
    if cached is not None:
        return cached
    path = Path(__file__).resolve().parent.parent / "data" / "jobs.json"
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        data = []
    _cache.set("jobs", data)
    return data


# ---------------------------------------------------------------------------
# Controller
# ---------------------------------------------------------------------------

class WebsitePublicController(http.Controller):
    """Public routes for the Bibind website."""

    @http.route("/", type="http", auth="public", website=True)
    def home(self, **kwargs: Any):
        """Render the home page.

        The real implementation would load teaser offers via ``ApiClient`` and
        pass them to the template.  Here we only render a minimal template.
        """

        return http.request.render("bibind_website_public.index", {})

    # ------------------------------------------------------------------
    # Offers catalogue
    # ------------------------------------------------------------------
    @http.route("/offers", type="http", auth="public", website=True)
    def offers(self, **kwargs: Any):
        """List available offers."""
        return http.request.render("bibind_website_public.offers", {})

    @http.route("/offers/<string:slug>", type="http", auth="public", website=True)
    def offer_detail(self, slug: str, **kwargs: Any):
        """Display the detail of a single offer."""
        # In a full implementation ``slug`` would be used to fetch data.
        context = {"slug": slug}
        return http.request.render("bibind_website_public.offer_detail", context)

    # ------------------------------------------------------------------
    # API documentation
    # ------------------------------------------------------------------
    @http.route("/docs", type="http", auth="public", website=True)
    def docs(self, **kwargs: Any):
        """Render the API documentation page."""
        base_url = ParamStore.get_param("op_bootstrap_base_url", "")
        iframe_url = f"{base_url}/openapi.yaml" if base_url else ""
        return http.request.render("bibind_website_public.docs", {"iframe_url": iframe_url})

    # ------------------------------------------------------------------
    # Jobs
    # ------------------------------------------------------------------
    @http.route("/jobs", type="http", auth="public", website=True)
    def jobs(self, q: Optional[str] = None, **kwargs: Any):
        """Render the list of open jobs, optionally filtered by ``q``."""
        jobs = _load_jobs_data()
        if q:
            q_lower = q.lower()
            jobs = [job for job in jobs if q_lower in job.get("title", "").lower()]
        return http.request.render("bibind_website_public.jobs", {"jobs": jobs, "query": q})

    @http.route("/jobs/apply", type="http", auth="public", methods=["POST"], website=True, csrf=True)
    def jobs_apply(self, **post: Any):
        """Handle job application submission.

        This simplified handler validates the honeypot field and required
        parameters, then pretends to send an email using the ``mail.template``
        defined in ``data/mail_templates.xml``.  No data is persisted.
        """

        if post.get("website_hp"):
            return http.Response(status=400)
        required = ["full_name", "email", "role", "message"]
        if any(not post.get(k) for k in required):
            return http.Response(status=400)
        # In real deployment, ``mail.mail`` would be created here.
        return http.local_redirect("/jobs?ok=1")
