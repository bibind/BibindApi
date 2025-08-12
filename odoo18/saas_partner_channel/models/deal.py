from odoo import api, fields, models


class SaasDeal(models.Model):
    _name = 'saas.deal'
    _description = 'SaaS Deal Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    company_name = fields.Char()
    stage = fields.Selection([
        ('registered', 'Registered'),
        ('qualified', 'Qualified'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ], default='registered')
    amount = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    registered_at = fields.Datetime(default=fields.Datetime.now)
    won_at = fields.Datetime()
    notes = fields.Text()

    @api.model
    def create(self, vals):
        if not vals.get('registered_at'):
            vals['registered_at'] = fields.Datetime.now()
        return super().create(vals)
