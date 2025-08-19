from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_channel_partner = fields.Boolean(string='Channel Partner', default=False)
    partner_tier = fields.Selection([
        ('registered', 'Registered'),
        ('silver', 'Silver'),
        ('gold', 'Gold')
    ], string='Tier', default='registered')
    commission_rate = fields.Float(string='Commission Rate (%)', default=0.0)
    payout_method = fields.Selection([
        ('sepa', 'SEPA'),
        ('wise', 'Wise'),
        ('manual', 'Manual'),
    ], string='Payout Method', default='sepa')
    iban = fields.Char(string='IBAN')
    bic = fields.Char(string='BIC')
    vat_id = fields.Char(string='VAT ID')
