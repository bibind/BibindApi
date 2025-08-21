from odoo import http
from odoo.http import request


class GitLabWebhook(http.Controller):
    """Handle incoming GitLab webhooks."""

    @http.route(
        "/gitlab/<int:project_id>/webhook",
        type="json",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def gitlab_webhook(self, project_id: int, **payload):
        """Trigger a synchronization for the given *project_id*."""

        request.env["kb.projects.facade"].sudo().with_context(
            project_id=project_id
        ).sync_gitlab()
        return {"status": "ok"}
