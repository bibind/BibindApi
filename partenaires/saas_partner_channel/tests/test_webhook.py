from odoo.tests import TransactionCase
from odoo import http
import hmac
import hashlib
import json
from types import SimpleNamespace


class TestWebhook(TransactionCase):
    def test_tenant_ready_webhook(self):
        tenant = self.env['saas.tenant'].create({
            'name': 'Test',
            'partner_id': self.env.ref('base.res_partner_1').id,
            'status': 'provisioning',
            'id_external': 'ext1',
        })
        secret = 'testsecret'
        self.env['ir.config_parameter'].sudo().set_param('SAAS_WEBHOOK_SECRET', secret)
        payload = {'event': 'tenant.ready', 'id_external': 'ext1', 'access_url': 'http://a'}
        body = json.dumps(payload).encode()
        sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

        class DummyRequest:
            def __init__(self, env):
                self.env = env
                self.httprequest = SimpleNamespace(data=body, headers={'X-Signature': sig})

        old_request = http.request
        http.request = DummyRequest(self.env)
        try:
            from ..controllers.webhook import SaasWebhook
            SaasWebhook().tenant_webhook()
        finally:
            http.request = old_request

        self.assertEqual(tenant.refresh().status, 'ready')
        self.assertEqual(tenant.access_url, 'http://a')
        # idempotent second call
        http.request = DummyRequest(self.env)
        try:
            SaasWebhook().tenant_webhook()
        finally:
            http.request = old_request
        self.assertEqual(tenant.refresh().status, 'ready')
