import json
import logging
import uuid

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


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

        correlation_id = (
            request.httprequest.headers.get("X-Correlation-Id")
            or str(uuid.uuid4())
        )
        _logger.info(
            json.dumps(
                {
                    "event": "gitlab.webhook",
                    "project_id": project_id,
                    "payload": payload,
                    "correlation_id": correlation_id,
                }
            )
        )
        request.env["kb.projects.facade"].sudo().with_context(
            project_id=project_id, correlation_id=correlation_id
        ).with_delay().sync_gitlab()
        response = {"status": "queued", "correlation_id": correlation_id}
        _logger.info(json.dumps({"response": response}))
        return response
