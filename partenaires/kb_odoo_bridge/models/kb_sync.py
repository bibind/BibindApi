from __future__ import annotations

import logging
from datetime import datetime, timedelta

from odoo import api, fields, models

from .kb_client import KillBillClient

_logger = logging.getLogger(__name__)


class KBSync(models.AbstractModel):
    _name = "kb.sync"
    _description = "Kill Bill Synchronization Utilities"

    @api.model
    def cron_sync_invoices(self) -> None:
        ICP = self.env["ir.config_parameter"].sudo()
        window_days = int(ICP.get_param("kb_sync_window_days", 30))
        since = (datetime.utcnow() - timedelta(days=window_days)).date().isoformat()
        partners = self.env["res.partner"].search([["kb_account_id", "!=", False]])
        client = KillBillClient(self.env)
        for partner in partners:
            invoices = client.list_account_invoices(partner.kb_account_id, since)
            for inv in invoices:
                move = self.env["account.move"].search([["kb_invoice_id", "=", inv.id]], limit=1)
                if not move:
                    move = self.env["account.move"].create(
                        {
                            "move_type": "out_invoice",
                            "partner_id": partner.id,
                            "kb_invoice_id": inv.id,
                            "invoice_date": fields.Date.today(),
                            "currency_id": self.env.company.currency_id.id,
                            "invoice_line_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "name": f"Kill Bill invoice {inv.id}",
                                        "quantity": 1.0,
                                        "price_unit": inv.amount,
                                    },
                                )
                            ],
                        }
                    )
                    move.action_post()
                payments = client.get_invoice_payments(inv.id)
                for pay in payments:
                    payment = self.env["account.payment"].search([["kb_payment_id", "=", pay.id]], limit=1)
                    if not payment:
                        payment = (
                            self.env["account.payment"].sudo().create(
                                {
                                    "payment_type": "inbound",
                                    "partner_type": "customer",
                                    "partner_id": partner.id,
                                    "amount": pay.amount,
                                    "currency_id": move.currency_id.id,
                                    "kb_payment_id": pay.id,
                                }
                            )
                        )
                        payment.action_post()
                        move.line_ids.filtered(lambda l: l.account_internal_type == "receivable").reconcile(
                            payment.line_ids
                        )
