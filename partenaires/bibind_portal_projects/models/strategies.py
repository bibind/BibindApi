from odoo import api, models


class DefaultProjectStrategy(models.AbstractModel):
    """Default no-op strategy for project operations."""

    _name = "kb.projects.strategy.default"
    _description = "Default project strategy"

    @api.model
    def link_service(self, project, service):
        """Fallback implementation that simply returns True."""
        return True

    @api.model
    def pull_issues(self, project):
        """Return an empty list of issues."""
        return []

    @api.model
    def push_tasks(self, project, tasks):
        """Return True indicating tasks were 'pushed'."""
        return True

    @api.model
    def plan_sprint(self, project, sprint):
        """Return True indicating sprint planning succeeded."""
        return True

    @api.model
    def compute_kpis(self, project):
        """Return an empty dictionary of KPIs."""
        return {}

    @api.model
    def create_environment(self, project, payload):
        """Return the input payload to mimic environment creation."""
        return payload
