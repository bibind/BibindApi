from __future__ import annotations

import hashlib
import hmac
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class KBWebhookController(http.Controller):
    @http.route("/kb/webhook", type="json", auth="public", methods=["POST"], csrf=False)
    def webhook(self, **payload):
        ICP = request.env["ir.config_parameter"].sudo()
        secret = ICP.get_param("kb_webhook_secret")
        if secret:
            signature = request.httprequest.headers.get("X-Signature", "")
            body = request.httprequest.data
            expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(signature, expected):
                _logger.warning("Invalid webhook signature")
                return {"status": "invalid"}
        _logger.info("Webhook payload: %s", payload)
        return {"status": "ok"}
