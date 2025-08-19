from datetime import timedelta
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    tenant_id = fields.Many2one('saas.tenant')

    @api.model
    def _commission_retention_days(self):
        return int(self.env['ir.config_parameter'].sudo().get_param('saas_retention_days', 30))

    def write(self, vals):
        res = super().write(vals)
        if 'payment_state' in vals and vals['payment_state'] == 'paid':
            self._create_commissions()
        return res

    def _create_commissions(self):
        retention_days = self._commission_retention_days()
        for move in self:
            if move.tenant_id and move.payment_state == 'paid' and move.state == 'posted':
                partner = move.tenant_id.partner_id
                rate = partner.commission_rate
                base = move.amount_untaxed_signed
                amount = base * rate / 100.0
                hold = fields.Datetime.now() + timedelta(days=retention_days)
                self.env['saas.commission.ledger'].create({
                    'partner_id': partner.id,
                    'tenant_id': move.tenant_id.id,
                    'invoice_id': move.id,
                    'base_amount_ht': base,
                    'rate': rate,
                    'amount': amount,
                    'status': 'pending',
                    'hold_until': hold,
                })
