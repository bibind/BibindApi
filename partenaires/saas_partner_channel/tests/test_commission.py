from odoo.tests import TransactionCase
from odoo import fields
from datetime import timedelta


class TestCommission(TransactionCase):
    def test_commission_created_on_payment(self):
        partner = self.env['res.partner'].create({'name': 'P', 'is_channel_partner': True, 'commission_rate': 10})
        tenant = self.env['saas.tenant'].create({'name': 'T', 'partner_id': partner.id})
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.env.ref('base.res_partner_1').id,
            'invoice_date': fields.Date.today(),
            'saas_tenant_id': tenant.id,
            'invoice_line_ids': [(0,0,{'name':'A','quantity':1,'price_unit':100})],
        })
        invoice.action_post()
        invoice.write({'payment_state': 'paid'})
        ledger = self.env['saas.commission.ledger'].search([('invoice_id','=',invoice.id)])
        self.assertEqual(len(ledger),1)
        self.assertEqual(ledger.status,'pending')
        self.assertEqual(ledger.amount,10)
        self.assertAlmostEqual((ledger.hold_until - fields.Datetime.now()).days,30,delta=2)
