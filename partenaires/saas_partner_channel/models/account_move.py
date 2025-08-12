from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, api, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    saas_tenant_id = fields.Many2one('saas.tenant')

    def write(self, vals):
        payment_state_before = {m.id: m.payment_state for m in self}
        res = super().write(vals)
        for move in self:
            if payment_state_before.get(move.id) != 'paid' and move.payment_state == 'paid':
                move._create_commission_ledger()
        return res

    def _create_commission_ledger(self):
        for move in self:
            if move.move_type != 'out_invoice' or not move.saas_tenant_id:
                continue
            partner = move.saas_tenant_id.partner_id
            if not partner or not partner.is_channel_partner:
                continue
            if self.env['saas.commission.ledger'].search_count([('invoice_id', '=', move.id)]):
                continue
            rate = partner.commission_rate or 0.0
            hold_days = int(self.env['ir.config_parameter'].sudo().get_param('saas.commission_hold_days', '30'))
            hold_until = fields.Datetime.now() + relativedelta(days=hold_days)
            self.env['saas.commission.ledger'].create({
                'partner_id': partner.id,
                'tenant_id': move.saas_tenant_id.id,
                'invoice_id': move.id,
                'base_amount_ht': move.amount_untaxed_signed,
                'rate': rate,
                'amount': move.amount_untaxed_signed * rate / 100.0,
                'status': 'pending',
                'hold_until': hold_until,
                'currency_id': move.currency_id.id,
            })
