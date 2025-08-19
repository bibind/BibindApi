import logging
import requests
from odoo import models, tools

_logger = logging.getLogger(__name__)


class SaasAPI(models.AbstractModel):
    _name = 'saas.api'
    _description = 'SaaS API helper'

    def _get_base_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('SAAS_API_BASE_URL')

    def _get_api_key(self):
        return self.env['ir.config_parameter'].sudo().get_param('SAAS_API_KEY')

    def _get_timeout(self):
        return int(self.env['ir.config_parameter'].sudo().get_param('SAAS_API_TIMEOUT', 30))

    def create_tenant(self, partner, payload):
        base = self._get_base_url()
        if not base:
            _logger.error('SAAS_API_BASE_URL not configured')
            return
        url = f"{base}/partners/{partner.id}/tenants"
        headers = {
            'Authorization': f"Bearer {self._get_api_key()}",
            'Content-Type': 'application/json',
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=self._get_timeout())
            response.raise_for_status()
            return response.json()
        except Exception as exc:  # pragma: no cover - network errors
            _logger.exception('Tenant creation failed: %s', exc)
            return None
