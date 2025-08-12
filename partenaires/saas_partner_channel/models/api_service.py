import logging
import requests
from odoo import models, api

_logger = logging.getLogger(__name__)


class SaasApi(models.AbstractModel):
    _name = 'saas.api'
    _description = 'SaaS API Service'

    @api.model
    def create_tenant(self, partner_id, payload, idempotency_key):
        """Call external SaaS API. Placeholder implementation."""
        base_url = self.env['ir.config_parameter'].sudo().get_param('SAAS_API_BASE_URL')
        api_key = self.env['ir.config_parameter'].sudo().get_param('SAAS_API_KEY')
        if not base_url:
            _logger.info('No API base URL configured, skipping call')
            return
        url = f"{base_url}/partners/{partner_id}/tenants"
        headers = {'Authorization': f'Bearer {api_key}', 'Idempotency-Key': idempotency_key}
        try:
            requests.post(url, json=payload, headers=headers, timeout=5)
        except Exception as e:
            _logger.exception('API call failed: %s', e)
