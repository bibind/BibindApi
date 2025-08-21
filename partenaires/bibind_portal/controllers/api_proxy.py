from __future__ import annotations

import logging

from odoo import http
from odoo.http import request

from odoo.addons.bibind_core.services.api_client import ApiClient

_logger = logging.getLogger(__name__)


class ApiProxyController(http.Controller):
    @http.route(
        "/my/api/monitoring/signurl/<int:env_id>",
        type="json",
        auth="user",
        methods=["GET"],
    )
    def monitoring_link(self, env_id: int):
        env = request.env["kb.environment"].sudo().browse(env_id)
        client = ApiClient.from_env(request.env)
        link = client.get(f"/environments/{env.id}/monitoring:link")
        return {"url": link.get("url")}

    @http.route(
        "/my/api/logs/signurl/<int:env_id>",
        type="json",
        auth="user",
        methods=["GET"],
    )
    def logs_link(self, env_id: int):
        env = request.env["kb.environment"].sudo().browse(env_id)
        client = ApiClient.from_env(request.env)
        link = client.get(f"/environments/{env.id}/logs:link")
        return {"url": link.get("url")}
