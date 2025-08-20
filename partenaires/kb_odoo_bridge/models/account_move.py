from __future__ import annotations

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    kb_invoice_id = fields.Char(readonly=True)
