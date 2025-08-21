"""Basic HttpCase tests for bibind_website_public.

The tests rely on Odoo's testing framework. They are skipped automatically if
Odoo is not installed in the execution environment. This allows the test suite
of this kata repository to run without pulling the heavy Odoo dependency while
still providing meaningful examples for real deployments.
"""

import pytest

odoo = pytest.importorskip("odoo")  # noqa: F841
from odoo.tests.common import HttpCase


class TestWebsiteRoutes(HttpCase):
    """Ensure that public routes are reachable."""

    def test_home_200_contains_cta(self):
        response = self.url_open("/")
        assert response.status_code == 200
        assert "Découvrir les offres" in response.text

    def test_offers_200(self):
        response = self.url_open("/offers")
        assert response.status_code == 200

    def test_docs_iframe_present(self):
        response = self.url_open("/docs")
        assert response.status_code == 200
        assert "<iframe" in response.text

    def test_jobs_get(self):
        response = self.url_open("/jobs")
        assert response.status_code == 200
