from __future__ import annotations

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from .kb_client import KillBillClient

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    kb_account_id = fields.Char(readonly=True)
    kb_external_key = fields.Char(default=lambda self: self._get_default_external_key())

    def _get_default_external_key(self) -> str:
        self.ensure_one()
        return self.ref or str(self.id)

    def action_create_kb_account(self) -> None:
        for partner in self:
            if partner.kb_account_id:
                raise UserError(_("Kill Bill account already linked."))
            # Advisory lock to avoid duplicates
            self.env.cr.execute("SELECT pg_advisory_lock(%s)", (partner.id,))
            try:
                client = KillBillClient(self.env)
                account_id = client.create_account(
                    partner.kb_external_key or str(partner.id),
                    partner.name or "",
                    partner.email or "",
                )
                partner.sudo().write({"kb_account_id": account_id})
            finally:
                self.env.cr.execute("SELECT pg_advisory_unlock(%s)", (partner.id,))

