from unittest import mock

from odoo.tests.common import HttpCase


class ServiceFlowsCase(HttpCase):
    """Cover portal routes and security for services."""

    def setUp(self):
        super().setUp()
        Tenant = self.env['pce.tenant']
        self.tenant1 = Tenant.create({'name': 'Tenant A'})
        self.tenant2 = Tenant.create({'name': 'Tenant B'})
        User = self.env['res.users'].with_context(no_reset_password=True)
        portal_group = self.env.ref('base.group_portal')
        self.user1 = User.create({'name': 'U1', 'login': 'u1', 'password': 'pwd1', 'tenant_id': self.tenant1.id})
        self.user1.groups_id = [(6, 0, [portal_group.id])]
        self.user2 = User.create({'name': 'U2', 'login': 'u2', 'password': 'pwd2', 'tenant_id': self.tenant2.id})
        self.user2.groups_id = [(6, 0, [portal_group.id])]
        Service = self.env['kb.service']
        self.s1 = Service.create({'name': 'S1', 'tenant_id': self.tenant1.id})
        self.s2 = Service.create({'name': 'S2', 'tenant_id': self.tenant2.id})
        Env = self.env['kb.environment']
        self.env1 = Env.create({'service_id': self.s1.id, 'env': 'dev', 'tenant_id': self.tenant1.id})
        self.env2 = Env.create({'service_id': self.s2.id, 'env': 'dev', 'tenant_id': self.tenant2.id})

    def test_routes_and_security(self):
        """Ensure portal routes enforce authentication and security."""
        resp = self.url_open('/my/services', allow_redirects=False)
        assert resp.status_code == 302
        self.authenticate('u1', 'pwd1')
        resp = self.url_open('/my/services')
        assert resp.status_code == 200
        resp = self.url_open(f'/my/services/{self.s2.id}')
        assert resp.status_code == 404

    def test_api_proxy(self):
        """Monitoring and log signurl endpoints use ApiClient."""
        self.authenticate('u1', 'pwd1')
        with mock.patch('odoo.addons.bibind_core.services.api_client.ApiClient.from_env') as mock_cli:
            fake_client = mock.Mock()
            fake_client.get.return_value = {'url': 'http://m'}
            mock_cli.return_value = fake_client
            resp = self.url_open(
                f'/my/api/monitoring/signurl/{self.env1.id}',
                method='GET',
                headers={'Content-Type': 'application/json'},
            )
            assert resp.json()['url'] == 'http://m'
            fake_client.get.assert_called_once_with(f'/environments/{self.env1.id}/monitoring:link')
