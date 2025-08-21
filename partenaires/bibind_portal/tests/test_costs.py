from unittest import mock
from decimal import Decimal

from odoo.tests.common import TransactionCase


class CostEstimateCase(TransactionCase):
    """Ensure costs are updated via ApiClient."""

    def setUp(self):
        super().setUp()
        Tenant = self.env['pce.tenant']
        self.tenant = Tenant.create({'name': 'Tenant'})
        Service = self.env['kb.service']
        self.service = Service.create({'name': 'S1', 'tenant_id': self.tenant.id})
        Env = self.env['kb.environment']
        self.env1 = Env.create({'service_id': self.service.id, 'env': 'dev', 'tenant_id': self.tenant.id})

    def test_refresh_all_for_service(self):
        with mock.patch('odoo.addons.bibind_core.services.api_client.ApiClient.from_env') as mock_cli:
            fake_client = mock.Mock()
            fake_client.get.return_value = {'amount': 12.5}
            mock_cli.return_value = fake_client
            estimator = self.env['kb.cost.estimate']
            amounts = estimator.refresh_all_for_service(self.service)
            assert amounts[self.env1.id] == Decimal('12.5')
            self.env1.refresh()
            assert self.env1.cost_estimate == Decimal('12.5')
            fake_client.get.assert_called_once_with(f'/environments/{self.env1.id}/costs:estimate')
