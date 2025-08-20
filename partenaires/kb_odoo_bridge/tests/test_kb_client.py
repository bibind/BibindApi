import responses
from odoo.tests.common import TransactionCase

from ..models.kb_client import KillBillClient


class TestKBClient(TransactionCase):
    def setUp(self):
        super().setUp()
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.set_param("kb_base_url", "http://test")
        ICP.set_param("kb_api_key", "key")
        ICP.set_param("kb_api_secret", "secret")

    @responses.activate
    def test_create_account(self):
        responses.add(
            responses.POST,
            "http://test/1.0/kb/accounts",
            headers={"Location": "/1.0/kb/accounts/123"},
            json={},
            status=201,
        )
        client = KillBillClient(self.env)
        account_id = client.create_account("ext", "Name", "mail@example.com")
        self.assertEqual(account_id, "123")
