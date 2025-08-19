import hmac
import json
import uuid
from odoo import http
from odoo.http import request
from ..utils import compute_hmac


class GroupodooController(http.Controller):
    """Minimal controller handling chat messages."""

    @http.route("/groupodoo/csrf", type="json", auth="user")
    def csrf(self):
        """Return CSRF token for widgets."""
        return {"token": request.csrf_token()}

    @http.route(
        "/groupodoo/api/chat/send",
        type="json",
        auth="user",
        methods=["POST"],
        csrf=True,
    )
    def send(self, session_uuid=None, message=None, **kw):
        env = request.env
        session = env["groupodoo.chat.session"].sudo().search(
            [("uuid", "=", session_uuid)], limit=1
        )
        if not session:
            return http.Response(status=404)
        user = request.env.user
        if user.has_group("base.group_portal") and session.user_id.id != user.id:
            return http.Response(status=403)
        env["groupodoo.chat.message"].sudo().create(
            {
                "session_id": session.id,
                "direction": "outbound",
                "role": "user",
                "content": message or "",
            }
        )
        return {"ok": True, "idempotency_key": str(uuid.uuid4())}

    @http.route(
        "/groupodoo/api/chat/webhook",
        type="json",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def webhook(self, **kw):
        raw = request.httprequest.data or b""
        sig = request.httprequest.headers.get("X-Bibind-Signature", "")
        secret = (
            request.env["ir.config_parameter"].sudo().get_param("groupodoo_webhook_secret", "")
        )
        expected = compute_hmac(secret, raw)
        if not hmac.compare_digest(sig, expected):
            return http.Response(status=403)
        data = json.loads(raw.decode("utf-8") or "{}")
        session_uuid = data.get("session_uuid")
        session = request.env["groupodoo.chat.session"].sudo().search(
            [("uuid", "=", session_uuid)], limit=1
        )
        if session:
            request.env["groupodoo.chat.message"].sudo().create(
                {
                    "session_id": session.id,
                    "direction": "inbound",
                    "role": data.get("role", "assistant"),
                    "content": data.get("content", ""),
                    "payload_json": data,
                }
            )
        return {"status": "ok"}
