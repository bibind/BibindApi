import responses
from odoo.tests.common import TransactionCase


class TestPartnerFlow(TransactionCase):
    @responses.activate
    def test_create_account_button(self):
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.set_param("kb_base_url", "http://test")
        ICP.set_param("kb_api_key", "key")
        ICP.set_param("kb_api_secret", "secret")
        responses.add(
            responses.POST,
            "http://test/1.0/kb/accounts",
            headers={"Location": "/1.0/kb/accounts/abc"},
            json={},
            status=201,
        )
        partner = self.env["res.partner"].create({"name": "Demo", "email": "d@e.mo"})
        partner.action_create_kb_account()
        self.assertEqual(partner.kb_account_id, "abc")
