from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_channel_partner = fields.Boolean(string='Channel Partner')
    partner_tier = fields.Selection([
        ('registered', 'Registered'),
        ('silver', 'Silver'),
        ('gold', 'Gold')
    ], default='registered')
    commission_rate = fields.Float(string='Commission Rate', help='Percentage')
    payout_method = fields.Selection([
        ('sepa', 'SEPA'),
        ('wise', 'Wise'),
        ('manual', 'Manual'),
    ], default='sepa')
    iban = fields.Char()
    bic = fields.Char()
    vat_id = fields.Char()
