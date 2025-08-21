from __future__ import annotations

import logging
import time
from typing import Iterable, List

from odoo import models

from odoo.addons.bibind_core.services.api_client import ApiClient

_logger = logging.getLogger(__name__)


class GitLabSync(models.AbstractModel):
    """Facade around the external API to synchronize GitLab objects."""

    _name = "kb.sync.gitlab"
    _description = "GitLab Synchronization Facade"

    def _ensure_label(self, name: str) -> int:
        tag = self.env["ir.tags"].search([("name", "=", name)], limit=1)
        if not tag:
            tag = self.env["ir.tags"].create({"name": name})
        return tag.id

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def pull_issues(self, project):
        """Fetch labels, epics, issues and merge requests from GitLab.

        Data is retrieved via :class:`ApiClient`.  Issues and epics are mirrored
        to ``project.task`` records while labels are created as ``ir.tags``.  The
        operation is idempotent: existing tasks are updated in place.
        """

        client = ApiClient.from_env(self.env)
        proj_id = project.gitlab_project_id

        labels = client.get(f"/gitlab/projects/{proj_id}/labels") or []
        epics = client.get(f"/gitlab/projects/{proj_id}/epics") or []
        issues = client.get(f"/gitlab/projects/{proj_id}/issues") or []
        merge_requests = client.get(
            f"/gitlab/projects/{proj_id}/merge_requests"
        ) or []

        for label in labels:
            try:
                self._ensure_label(label.get("name"))
            except Exception:  # pragma: no cover - defensive
                _logger.exception("label sync failed: %s", label)

        def _sync_issue(data, issue_type="task"):
            task = self.env["project.task"].search(
                [("gitlab_issue_id", "=", data["id"])], limit=1
            )
            tag_ids: List[int] = []
            for label_name in data.get("labels", []):
                tag_ids.append(self._ensure_label(label_name))
            vals = {
                "name": data.get("title"),
                "gitlab_issue_id": data["id"],
                "issue_type": issue_type,
                "tag_ids": [(6, 0, tag_ids)],
            }
            if task:
                task.write(vals)
            else:
                vals["project_id"] = project.id
                task = self.env["project.task"].create(vals)
            return task

        tasks = []
        for epic in epics:
            tasks.append(_sync_issue(epic, "epic"))
        for issue in issues:
            tasks.append(_sync_issue(issue, issue.get("type", "task")))

        # Merge requests are fetched for completeness, but not mirrored yet.
        if merge_requests:
            _logger.info(
                "Fetched %d merge requests for project %s", len(merge_requests), proj_id
            )
        return tasks

    def push_tasks(self, project, tasks: Iterable[models.Model]):
        """Push local tasks back to GitLab."""

        client = ApiClient.from_env(self.env)
        proj_id = project.gitlab_project_id

        for task in tasks:
            payload = {
                "title": task.name,
                "description": task.description or "",
            }
            try:
                if task.gitlab_issue_id:
                    client.put(
                        f"/gitlab/projects/{proj_id}/issues/{task.gitlab_issue_id}",
                        payload,
                    )
                else:
                    resp = client.post(
                        f"/gitlab/projects/{proj_id}/issues", payload
                    )
                    task.gitlab_issue_id = resp.get("id")
            except Exception:  # pragma: no cover - defensive
                _logger.exception("Failed to push task %s", task.id)
                time.sleep(1)
        return True
