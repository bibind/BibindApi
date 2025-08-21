# -*- coding: utf-8 -*-
"""Webhook endpoints for op_bootstrap callbacks."""
from __future__ import annotations

import hmac
import json
import logging
import hashlib
import time

from odoo import http
from odoo.http import request

_logger = logging.getLogger("bibind")


def _check_signature(payload: bytes, signature: str, secret: str) -> bool:
    mac = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, signature)


class BibindWebhookController(http.Controller):
    @http.route(
        "/bibind/webhook/audit",
        type="json",
        auth="public",
        csrf=False,
        methods=["POST"],
    )
    def audit_event(self):
        payload = request.httprequest.get_data() or b"{}"
        data = json.loads(payload)
        required = {"correlation_id", "event", "subject", "instance_id", "at"}
        if not required.issubset(data):
            return http.Response(status=400)
        secret_ref = request.env["bibind.param.store"].get_param(
            "webhook_hmac_secret_ref"
        )
        if secret_ref:
            secret = request.env["bibind.api_client"].resolve_secret_ref(secret_ref)
            sig = request.httprequest.headers.get("X-Signature")
            if not sig or not _check_signature(payload, sig, secret):
                return http.Response(status=403)
        _logger.info(json.dumps({"event": "auditEvent", "payload": data}))
        return {"status": "ok"}

    @http.route(
        "/bibind/webhook/ai_callback",
        type="json",
        auth="public",
        csrf=False,
        methods=["POST"],
    )
    def ai_callback(self):
        start = time.monotonic()
        payload = request.httprequest.get_data() or b"{}"
        data = json.loads(payload)
        required = {"task_id", "status", "correlation_id"}
        if not required.issubset(data):
            return http.Response(status=400)
        secret_ref = request.env["bibind.param.store"].get_param(
            "webhook_hmac_secret_ref"
        )
        if secret_ref:
            secret = request.env["bibind.api_client"].resolve_secret_ref(secret_ref)
            sig = request.httprequest.headers.get("X-Signature")
            if not sig or not _check_signature(payload, sig, secret):
                return http.Response(status=403)
        request.env["bus.bus"].sendone("ai.task.status", data)
        duration = time.monotonic() - start
        _logger.info(
            json.dumps(
                {"event": "ai.task.status", "payload": data, "duration": duration}
            )
        )
        return {"status": "ok"}
