"""Facade for project related remote operations.

This model acts as a thin layer on top of :class:`ApiClient` to hide the
details of the HTTP API from the rest of the code base.  Only the minimal
methods required by the tests are implemented.
"""

from odoo import api, models

from odoo.addons.bibind_core.services.api_client import ApiClient


class ProjectsFacade(models.Model):
    _name = 'kb.projects.facade'
    _description = 'Projects Facade'

    @api.model
    def sync_gitlab(self):
        project = self.env['project.project'].browse(self.env.context.get('project_id'))
        self.env['kb.sync.gitlab'].pull_issues(project)
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
