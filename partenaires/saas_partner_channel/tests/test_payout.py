from odoo.tests import TransactionCase
from datetime import timedelta
from odoo import fields


class TestPayout(TransactionCase):
    def test_payout_run(self):
        partner = self.env['res.partner'].create({'name': 'P', 'is_channel_partner': True})
        tenant = self.env['saas.tenant'].create({'name': 'T', 'partner_id': partner.id})
        ledger1 = self.env['saas.commission.ledger'].create({
            'partner_id': partner.id,
            'tenant_id': tenant.id,
            'amount': 10,
            'currency_id': self.env.company.currency_id.id,
            'status': 'pending',
            'hold_until': fields.Datetime.now() - timedelta(days=1),
        })
        ledger2 = self.env['saas.commission.ledger'].create({
            'partner_id': partner.id,
            'tenant_id': tenant.id,
            'amount': 20,
            'currency_id': self.env.company.currency_id.id,
            'status': 'pending',
            'hold_until': fields.Datetime.now() - timedelta(days=1),
        })
        wizard = self.env['saas.payout.run.wizard'].create({})
        run = wizard.action_generate()
        self.assertTrue(run)
        item = run.item_ids[0]
        self.assertEqual(item.amount, 30)
        self.assertEqual(item.partner_id, partner)
        self.assertTrue(all(l.status == 'payable' for l in (ledger1+ledger2)))
