import hmac
import hashlib
import json
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied


class SaasWebhook(http.Controller):
    @http.route('/webhooks/tenant', type='json', auth='public', methods=['POST'], csrf=False)
    def tenant_webhook(self):
        body = request.httprequest.data
        secret = request.env['ir.config_parameter'].sudo().get_param('SAAS_WEBHOOK_SECRET', '')
        signature = request.httprequest.headers.get('X-Signature')
        expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature or '', expected):
            raise AccessDenied()
        data = json.loads(body.decode('utf-8'))
        event = data.get('event')
        tenant = request.env['saas.tenant'].sudo().search([('id_external', '=', data.get('id_external'))], limit=1)
        if not tenant:
            return True
        if event == 'tenant.ready':
            tenant.write({'status': 'ready', 'stage': 'ready', 'progress': 100, 'access_url': data.get('access_url')})
        elif event == 'tenant.stage_changed':
            tenant.write({'stage': data.get('stage'), 'progress': data.get('progress')})
        elif event == 'tenant.failed':
            tenant.write({'status': 'failed'})
        return True
