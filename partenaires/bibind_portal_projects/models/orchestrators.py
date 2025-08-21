from __future__ import annotations

import logging
import time
import uuid
from typing import Dict, Iterable

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
        self.env["ir.config_parameter"].sudo().set_param(self._lock_key(project_id), "")

    @api.model
    def _request_context(self) -> Dict[str, str]:
        """Return correlation and request identifiers for downstream calls."""

        cid = self.env.context.get("correlation_id") or str(uuid.uuid4())
        rid = self.env.context.get("request_id") or str(uuid.uuid4())
        return {"correlation_id": cid, "request_id": rid}

    @api.model
    def get_offer_strategy(self, offer_code: str):
        """Load the strategy model matching *offer_code*.

        Fallback to the default strategy if no specific one is registered.
        """

        if offer_code:
            model = f"kb.projects.strategy.{offer_code}"
            if self.env.registry.get(model):
                return self.env[model]
        return self.env["kb.projects.strategy.default"]

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

        ctx = self._request_context()

        if not self._acquire_lock(project_id):
            _logger.debug("sync already queued for project %s", project_id)
            return True

        project = self.env["project.project"].browse(project_id)
        delay = 1
        try:
            for attempt in range(max_retries):
                try:
                    self.env["kb.sync.gitlab"].with_context(**ctx).pull_issues(project)
                    payload = {"project_id": project_id, **ctx}
                    self.env["bus.bus"].sendone("gitlab.sync", payload)
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

    @api.model
    def link_service(self, project, service):
        """Link *service* to *project* using the appropriate strategy."""

        strategy = self.get_offer_strategy(project.offer_code or service.offer)
        ctx = self._request_context()
        return strategy.with_context(**ctx).link_service(project, service)

    @api.model
    def pull_issues(self, project):
        """Pull external issues for *project*."""

        strategy = self.get_offer_strategy(project.offer_code)
        ctx = self._request_context()
        return strategy.with_context(**ctx).pull_issues(project)

    @api.model
    def push_tasks(self, project, tasks: Iterable[models.Model]):
        """Push local *tasks* to the external tracker."""

        strategy = self.get_offer_strategy(project.offer_code)
        ctx = self._request_context()
        return strategy.with_context(**ctx).push_tasks(project, tasks)

    @api.model
    def plan_sprint(self, project, sprint):
        """Plan a sprint for *project*."""

        strategy = self.get_offer_strategy(project.offer_code)
        ctx = self._request_context()
        return strategy.with_context(**ctx).plan_sprint(project, sprint)

    @api.model
    def compute_kpis(self, project):
        """Compute KPIs for *project*."""

        strategy = self.get_offer_strategy(project.offer_code)
        ctx = self._request_context()
        return strategy.with_context(**ctx).compute_kpis(project)

    @api.model
    def create_environment(self, project, payload: Dict[str, object]):
        """Provision an environment for *project*."""

        strategy = self.get_offer_strategy(project.offer_code)
        ctx = self._request_context()
        return strategy.with_context(**ctx).create_environment(project, payload)
