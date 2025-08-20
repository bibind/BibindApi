import json
import responses
from odoo.tests.common import TransactionCase


class TestCatalog(TransactionCase):
    @responses.activate
    def test_pull_catalog_json(self):
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.set_param("kb_base_url", "http://test")
        ICP.set_param("kb_api_key", "key")
        ICP.set_param("kb_api_secret", "secret")
        responses.add(
            responses.GET,
            "http://test/1.0/kb/catalog",
            json={
                "products": [
                    {
                        "name": "Prod",
                        "plans": [
                            {"name": "Plan", "billingPeriod": "MONTH", "priceList": "DEFAULT"}
                        ],
                    }
                ]
            },
            status=200,
        )
        wiz = self.env["kb.catalog.pull.wizard"].create({})
        wiz.action_pull()
        tmpl = self.env["product.template"].search([["kb_product_name", "=", "Prod"]])
        self.assertTrue(tmpl)

    @responses.activate
    def test_push_catalog(self):
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.set_param("kb_base_url", "http://test")
        ICP.set_param("kb_api_key", "key")
        ICP.set_param("kb_api_secret", "secret")
        self.env["product.template"].create(
            {
                "name": "Prod",
                "kb_is_subscription": True,
                "kb_product_name": "Prod",
                "kb_plan_name": "Plan",
                "kb_billing_period": "MONTH",
            }
        )
        responses.add(
            responses.POST,
            "http://test/1.0/kb/catalog/xml",
            status=200,
        )
        wiz = self.env["kb.catalog.push.wizard"].create({"format": "json"})
        wiz.action_push()
        self.assertEqual(len(responses.calls), 1)
