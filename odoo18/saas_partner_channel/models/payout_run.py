from odoo import fields, models


class SaasPayoutRun(models.Model):
    _name = 'saas.payout.run'
    _description = 'Payout Run'

    name = fields.Char(required=True)
    period_start = fields.Date()
    period_end = fields.Date()
    executed_at = fields.Datetime()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], default='draft')
    fx_table_json = fields.Text()
    item_ids = fields.One2many('saas.payout.item', 'run_id')


class SaasPayoutItem(models.Model):
    _name = 'saas.payout.item'
    _description = 'Payout Item'

    run_id = fields.Many2one('saas.payout.run')
    partner_id = fields.Many2one('res.partner', required=True)
    amount = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    fx_rate_used = fields.Float()
    net_after_withholding = fields.Monetary(currency_field='currency_id')
    bank_ref = fields.Char()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('exported', 'Exported'),
        ('paid', 'Paid'),
    ], default='draft')
