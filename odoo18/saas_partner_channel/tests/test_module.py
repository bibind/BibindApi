from datetime import timedelta
import hmac
import hashlib
import json
from odoo.tests import TransactionCase, tagged
from odoo import fields


@tagged('post_install', '-at_install')
class TestSaasPartnerChannel(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Partner',
            'is_channel_partner': True,
            'commission_rate': 10,
        })
        self.tenant = self.env['saas.tenant'].create({
            'name': 'Tenant',
            'partner_id': self.partner.id,
            'id_external': 'EXT1',
        })

    def test_webhook_ready(self):
        payload = {
            'event': 'tenant.ready',
            'tenant_id': 'EXT1',
            'access_url': 'https://ready.example.com',
        }
        secret = 'shhh'
        self.env['ir.config_parameter'].sudo().set_param('SAAS_WEBHOOK_SECRET', secret)
        body = json.dumps(payload).encode()
        sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        self.url_open('/webhooks/tenant', data=body, headers={'X-Signature': sig})
        self.assertEqual(self.tenant.refresh().status, 'ready')
        self.assertEqual(self.tenant.access_url, 'https://ready.example.com')

    def test_commission_on_invoice_paid(self):
        move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.env.ref('base.res_partner_1').id,
            'invoice_date': fields.Date.today(),
            'tenant_id': self.tenant.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'Test',
                'quantity': 1,
                'price_unit': 100,
                'account_id': self.env['account.account'].search([('internal_type', '=', 'receivable')], limit=1).id,
            })]
        })
        move.action_post()
        move.write({'payment_state': 'paid'})
        ledger = self.env['saas.commission.ledger'].search([('invoice_id', '=', move.id)])
        self.assertTrue(ledger)
        self.assertEqual(ledger.amount, 10)
        retention = self.env['ir.config_parameter'].sudo().get_param('saas_retention_days', 30)
        self.assertAlmostEqual((ledger.hold_until - fields.Datetime.now()).days, int(retention), delta=1)

    def test_payout_run_wizard(self):
        past = fields.Datetime.now() - timedelta(days=40)
        ledgers = self.env['saas.commission.ledger'].create([
            {
                'partner_id': self.partner.id,
                'tenant_id': self.tenant.id,
                'base_amount_ht': 100,
                'rate': 10,
                'amount': 10,
                'status': 'pending',
                'hold_until': past,
            },
            {
                'partner_id': self.partner.id,
                'tenant_id': self.tenant.id,
                'base_amount_ht': 200,
                'rate': 10,
                'amount': 20,
                'status': 'pending',
                'hold_until': past,
            },
        ])
        wizard = self.env['saas.payout.run.wizard'].create({})
        wizard.action_generate()
        run = self.env['saas.payout.run'].search([], limit=1, order='id desc')
        self.assertTrue(run)
        self.assertEqual(len(run.item_ids), 1)
        self.assertEqual(run.item_ids.amount, 30)

    def test_portal_acl(self):
        partner2 = self.env['res.partner'].create({'name': 'Other', 'is_channel_partner': True})
        tenant2 = self.env['saas.tenant'].create({'name': 'Other Tenant', 'partner_id': partner2.id})
        user = self.env['res.users'].with_context(no_reset_password=True).create({
            'name': 'PortalUser',
            'login': 'portal@example.com',
            'email': 'portal@example.com',
            'partner_id': self.partner.id,
            'groups_id': [(6, 0, [self.env.ref('saas_partner_channel.saas_group_partner_portal').id])],
        })
        tenants = self.env['saas.tenant'].sudo(user).search([])
        self.assertIn(self.tenant, tenants)
        self.assertNotIn(tenant2, tenants)
