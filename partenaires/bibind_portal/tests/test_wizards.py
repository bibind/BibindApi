from unittest import mock

from odoo.tests.common import TransactionCase
from odoo.addons.bibind_core.services.api_client import ApiClient


class WizardFlowsCase(TransactionCase):
    """Validate environment command flows creating deployments."""

    def setUp(self):
        super().setUp()
        Tenant = self.env['pce.tenant']
        self.tenant = Tenant.create({'name': 'Tenant'})
        Service = self.env['kb.service']
        self.service = Service.create({'name': 'S1', 'tenant_id': self.tenant.id})
        Env = self.env['kb.environment']
        self.env1 = Env.create({'service_id': self.service.id, 'env': 'dev', 'tenant_id': self.tenant.id})

    def test_start_creates_deployment(self):
        def fake_run(self, env_id, verb, payload=None, headers=None):
            client = ApiClient.from_env(self.env)
            client.post('/deployments', json={'environment': env_id, 'action': verb})
            self.env['kb.deployment'].create({'environment_id': env_id, 'action': verb})
            return {}

        with mock.patch('odoo.addons.bibind_portal.models.environment.ServiceOrchestrator.run', new=fake_run):
            with mock.patch('odoo.addons.bibind_core.services.api_client.ApiClient.from_env') as mock_cli:
                fake_client = mock.Mock()
                mock_cli.return_value = fake_client
                fake_client.post.return_value = {'id': 1}
                self.env1.do_start()
                fake_client.post.assert_called_once_with('/deployments', json={'environment': self.env1.id, 'action': 'start'})

        dep = self.env['kb.deployment'].search([('environment_id', '=', self.env1.id), ('action', '=', 'start')])
        assert dep
