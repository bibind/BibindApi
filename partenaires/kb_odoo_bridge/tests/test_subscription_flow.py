import responses
from odoo.tests.common import TransactionCase


class TestSubscriptionFlow(TransactionCase):
    @responses.activate
    def test_order_subscription(self):
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.set_param("kb_base_url", "http://test")
        ICP.set_param("kb_api_key", "key")
        ICP.set_param("kb_api_secret", "secret")
        partner = self.env["res.partner"].create({"name": "Demo"})
        partner.kb_account_id = "acc-1"
        product = self.env["product.template"].create(
            {
                "name": "SubProd",
                "kb_is_subscription": True,
                "kb_product_name": "Prod",
                "kb_plan_name": "Plan",
                "kb_billing_period": "MONTH",
                "list_price": 10,
            }
        )
        responses.add(
            responses.POST,
            "http://test/1.0/kb/subscriptions",
            json={"subscriptionId": "sub-1"},
            status=201,
        )
        order = self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": product.name,
                            "product_id": product.product_variant_id.id,
                            "product_uom_qty": 1,
                            "price_unit": 10,
                        },
                    )
                ],
            }
        )
        order.action_kb_subscribe()
        self.assertEqual(order.kb_subscription_id, "sub-1")
