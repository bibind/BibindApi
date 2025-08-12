from odoo import fields, models


class SaasCommissionLedger(models.Model):
    _name = 'saas.commission.ledger'
    _description = 'Commission Ledger'

    partner_id = fields.Many2one('res.partner', required=True)
    tenant_id = fields.Many2one('saas.tenant')
    invoice_id = fields.Many2one('account.move')
    base_amount_ht = fields.Monetary(currency_field='currency_id')
    rate = fields.Float()
    amount = fields.Monetary(currency_field='currency_id')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('payable', 'Payable'),
        ('paid', 'Paid'),
        ('clawed_back', 'Clawed Back')
    ], default='pending')
    hold_until = fields.Datetime()
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    note = fields.Text()
