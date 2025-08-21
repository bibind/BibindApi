import json
from odoo.tests.common import HttpCase


class WebhookCase(HttpCase):
    def test_audit_webhook(self):
        payload = {
            'correlation_id': 'c1', 'event': 'e', 'subject': 's', 'instance_id': 'i', 'at': 'now'
        }
        self.url_open('/bibind/webhook/audit', data=json.dumps(payload), method='POST')
