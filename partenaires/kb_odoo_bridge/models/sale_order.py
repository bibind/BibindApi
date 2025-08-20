from __future__ import annotations

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from .kb_client import KillBillClient

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    kb_subscription_id = fields.Char(readonly=True)

    def action_kb_subscribe(self) -> None:
        self.ensure_one()
        if not self.partner_id.kb_account_id:
            raise UserError(_("Partner has no Kill Bill account."))
        client = KillBillClient(self.env)
        sub_ids = []
        for line in self.order_line:
            tmpl = line.product_id.product_tmpl_id
            if not tmpl.kb_is_subscription:
                continue
            sub_id = client.create_subscription(
                self.partner_id.kb_account_id,
                tmpl.kb_product_name or tmpl.name,
                tmpl.kb_billing_period or "MONTH",
                tmpl.kb_price_list or "DEFAULT",
                plan_name=tmpl.kb_plan_name,
            )
            sub_ids.append(sub_id)
        if sub_ids:
            self.sudo().write({"kb_subscription_id": ",".join(sub_ids)})
        else:
            raise UserError(_("No subscription products on order."))
