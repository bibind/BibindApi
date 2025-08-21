from __future__ import annotations

import json
import logging
import time

from odoo import http
from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

_logger = logging.getLogger(__name__)


class BibindCustomerPortal(CustomerPortal):
    """Portal pages for Bibind services."""

    # ------------------------------------------------------------------
    def _json_log(self, started: float) -> None:
        """Log request metadata in JSON."""
        elapsed = int((time.time() - started) * 1000)
        data = {
            "user": request.env.user.id,
            "tenant": request.env.company.id,
            "path": request.httprequest.path,
            "correlation_id": request.env.context.get("correlation_id"),
            "elapsed_ms": elapsed,
        }
        _logger.info(json.dumps(data))

    # ------------------------------------------------------------------
    @http.route("/my/home", type="http", auth="user", website=True)
    def home(self, **kw):
        started = time.time()
        try:
            services = request.env["kb.service"].sudo().search([])
            values = self._prepare_portal_layout_values()
            values.update({"services": services})
            return request.render("bibind_portal.portal_home", values)
        finally:
            self._json_log(started)

    @http.route("/my/services", type="http", auth="user", website=True)
    def services(self, **kw):
        started = time.time()
        try:
            services = request.env["kb.service"].sudo().search([])
            values = self._prepare_portal_layout_values()
            values.update({"services": services})
            return request.render("bibind_portal.portal_services", values)
        finally:
            self._json_log(started)

    @http.route("/my/services/<int:service_id>", type="http", auth="user", website=True)
    def service_detail(self, service_id: int, **kw):
        started = time.time()
        try:
            service = request.env["kb.service"].sudo().browse(service_id)
            if not service.exists():
                return request.not_found()
            values = self._prepare_portal_layout_values()
            values.update({"service": service})
            return request.render("bibind_portal.portal_service_detail", values)
        finally:
            self._json_log(started)

    # ------------------------------------------------------------------
    def _env_action(self, env_id: int, verb: str):
        started = time.time()
        try:
            env = request.env["kb.environment"].sudo().browse(env_id)
            action = getattr(env, f"do_{verb}", None)
            if not env.exists() or not action:
                return request.make_json_response({"error": "not found"}, status=404)
            action()
            return request.make_json_response({"status": "ok"})
        except UserError as exc:
            return request.make_json_response({"error": str(exc)}, status=400)
        finally:
            self._json_log(started)

    @http.route(
        "/my/environments/<int:env_id>/start",
        type="json",
        auth="user",
        methods=["POST"],
    )
    def env_start(self, env_id: int):
        return self._env_action(env_id, "start")

    @http.route(
        "/my/environments/<int:env_id>/stop",
        type="json",
        auth="user",
        methods=["POST"],
    )
    def env_stop(self, env_id: int):
        return self._env_action(env_id, "stop")

    @http.route(
        "/my/environments/<int:env_id>/promote",
        type="json",
        auth="user",
        methods=["POST"],
    )
    def env_promote(self, env_id: int):
        return self._env_action(env_id, "promote")
