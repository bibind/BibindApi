from odoo.tests import TransactionCase


class TestACL(TransactionCase):
    def test_portal_record_rules(self):
        group = self.env.ref('saas_partner_channel.group_saas_partner_portal')
        p1 = self.env['res.partner'].create({'name': 'P1', 'is_channel_partner': True})
        p2 = self.env['res.partner'].create({'name': 'P2', 'is_channel_partner': True})
        u1 = self.env['res.users'].with_context(no_reset_password=True).create({'name': 'U1', 'login': 'u1', 'partner_id': p1.id, 'groups_id': [(6,0,[group.id])]})
        u2 = self.env['res.users'].with_context(no_reset_password=True).create({'name': 'U2', 'login': 'u2', 'partner_id': p2.id, 'groups_id': [(6,0,[group.id])]})
        t1 = self.env['saas.tenant'].create({'name': 'T1', 'partner_id': p1.id})
        t2 = self.env['saas.tenant'].create({'name': 'T2', 'partner_id': p2.id})
        # user1 should see only t1
        Tenants = self.env['saas.tenant'].with_user(u1)
        self.assertEqual(set(Tenants.search([]).ids), {t1.id})
