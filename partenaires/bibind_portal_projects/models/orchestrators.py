"""Facade for project related remote operations.

This model acts as a thin layer on top of :class:`ApiClient` to hide the
details of the HTTP API from the rest of the code base.  Only the minimal
methods required by the tests are implemented.
"""

from odoo import api, models

from odoo.addons.bibind_core.services.api_client import ApiClient

from __future__ import annotations

import logging
import time

from odoo import api, models

_logger = logging.getLogger(__name__)



class ProjectsFacade(models.Model):
    _name = "kb.projects.facade"
    _description = "Projects Facade"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @api.model
    def _lock_key(self, project_id: int) -> str:
        return f"gitlab.sync.lock.{project_id}"

    @api.model
    def _acquire_lock(self, project_id: int) -> bool:
        params = self.env["ir.config_parameter"].sudo()
        key = self._lock_key(project_id)
        if params.get_param(key):
            return False
        params.set_param(key, "1")
        return True

    @api.model
    def _release_lock(self, project_id: int) -> None:
        self.env["ir.config_parameter"].sudo().set_param(
            self._lock_key(project_id), ""
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    @api.model
    def sync_gitlab(self, max_retries: int = 3):
        """Synchronize a project's backlog with GitLab.

        The synchronization is queued via the Odoo bus and retries are
        performed with exponential backoff.  A simple locking mechanism ensures
        the job is idempotent when triggered concurrently.
        """

        project_id = self.env.context.get("project_id")
        if not project_id:
            return False

        if not self._acquire_lock(project_id):
            _logger.debug("sync already queued for project %s", project_id)
            return True

        project = self.env["project.project"].browse(project_id)
        delay = 1
        try:
            for attempt in range(max_retries):
                try:
                    self.env["kb.sync.gitlab"].pull_issues(project)
                    self.env["bus.bus"].sendone(
                        "gitlab.sync", {"project_id": project_id}
                    )
                    break
                except Exception as exc:  # pragma: no cover - defensive
                    if attempt + 1 == max_retries:
                        _logger.exception("gitlab sync failed: %s", exc)
                        raise
                    time.sleep(delay)
                    delay *= 2
        finally:
            self._release_lock(project_id)

        return True

    # ------------------------------------------------------------------
    # GitLab helpers
    # ------------------------------------------------------------------
    @api.model
    def create_task(self, project, payload):
        """Create an issue in the remote project."""
        client = ApiClient.from_env(self.env)
        return client.create_issue(project.id, payload)

    @api.model
    def create_merge_request(self, project, payload):
        """Create a merge request in the remote project."""
        client = ApiClient.from_env(self.env)
        return client.create_merge_request(project.id, payload)
