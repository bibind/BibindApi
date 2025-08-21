from odoo.tests.common import TransactionCase


class TestPortalSecurity(TransactionCase):
    def setUp(self):
        super().setUp()
        Tenant = self.env['pce.tenant']
        self.tenant1 = Tenant.create({'name': 'Tenant A'})
        self.tenant2 = Tenant.create({'name': 'Tenant B'})
        User = self.env['res.users'].with_context(no_reset_password=True)
        self.user1 = User.create({'name': 'U1', 'login': 'u1', 'tenant_id': self.tenant1.id})
        self.user2 = User.create({'name': 'U2', 'login': 'u2', 'tenant_id': self.tenant2.id})
        Service = self.env['kb.service']
        self.s1 = Service.create({'name': 'S1', 'tenant_id': self.tenant1.id})
        self.s2 = Service.create({'name': 'S2', 'tenant_id': self.tenant2.id})

    def test_visibility(self):
        self.env.invalidate_all()
        services_u1 = self.env['kb.service'].with_user(self.user1).search([])
        services_u2 = self.env['kb.service'].with_user(self.user2).search([])
        self.assertEqual(services_u1, self.s1)
        self.assertEqual(services_u2, self.s2)
