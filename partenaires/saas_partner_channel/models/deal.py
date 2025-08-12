from odoo import models, fields


class SaasDeal(models.Model):
    _name = 'saas.deal'
    _description = 'SaaS Deal'
    _inherit = ['mail.thread']

    name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    company_name = fields.Char()
    stage = fields.Selection([
        ('registered', 'Registered'),
        ('qualified', 'Qualified'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ], default='registered', tracking=True)
    amount = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    registered_at = fields.Datetime()
    won_at = fields.Datetime()
    notes = fields.Text()
