from __future__ import annotations

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    kb_product_name = fields.Char()
    kb_plan_name = fields.Char()
    kb_price_list = fields.Char(default="DEFAULT")
    kb_billing_period = fields.Selection(
        [
            ("DAY", "Day"),
            ("WEEK", "Week"),
            ("MONTH", "Month"),
            ("YEAR", "Year"),
        ]
    )
    kb_is_subscription = fields.Boolean()
