import hmac
import hashlib
import json
from unittest import mock

from odoo.tests.common import HttpCase


class WebhookCase(HttpCase):
    def _headers(self, sig=None):
        headers = {"Content-Type": "application/json"}
        if sig:
            headers["X-Signature"] = sig
        return headers

    def test_hmac_validation(self):
        payload = {
            "correlation_id": "c1",
            "event": "e",
            "subject": "s",
            "instance_id": "i",
            "at": "now",
        }
        secret = "s3"
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.set_param("webhook_hmac_secret_ref", "ref")
        sig = hmac.new(secret.encode(), json.dumps(payload).encode(), hashlib.sha256).hexdigest()
        with mock.patch(
            "odoo.addons.bibind_core.models.api_client.ApiClient.resolve_secret_ref",
            return_value=secret,
        ):
            resp = self.url_open(
                "/bibind/webhook/audit",
                data=json.dumps(payload),
                method="POST",
                headers=self._headers(sig),
            )
        assert resp.json()["status"] == "ok"

    def test_correlation_id_propagation(self):
        payload = {
            "correlation_id": "cid",
            "event": "e",
            "subject": "s",
            "instance_id": "i",
            "at": "now",
        }

        captured = {}

        def fake_get_param(self, key, default=None):
            captured["cid"] = self.env.context.get("correlation_id")
            return None

        with mock.patch(
            "odoo.addons.bibind_core.models.settings.ParamStore.get_param",
            new=fake_get_param,
        ):
            self.url_open(
                "/bibind/webhook/audit",
                data=json.dumps(payload),
                method="POST",
                headers=self._headers(),
            )
        assert captured["cid"] == "cid"

    def test_bad_payload_returns_400(self):
        resp = self.url_open(
            "/bibind/webhook/audit",
            data=json.dumps({"correlation_id": "x"}),
            method="POST",
            headers=self._headers(),
        )
        assert resp.status_code == 400
