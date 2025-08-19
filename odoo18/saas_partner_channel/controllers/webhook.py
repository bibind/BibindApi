import hmac
import hashlib
import json
from odoo import http
from odoo.http import request


class SaasWebhook(http.Controller):
    @http.route('/webhooks/tenant', type='json', auth='public', methods=['POST'], csrf=False)
    def tenant_webhook(self):
        secret = request.env['ir.config_parameter'].sudo().get_param('SAAS_WEBHOOK_SECRET', '')
        signature = request.httprequest.headers.get('X-Signature')
        body = request.httprequest.data
        expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature or ''):
            return http.Response('invalid signature', status=401)
        payload = json.loads(body.decode())
        event = payload.get('event')
        if event == 'tenant.ready':
            self._handle_tenant_ready(payload)
        elif event == 'tenant.stage_changed':
            self._handle_stage_changed(payload)
        return {'status': 'ok'}

    def _handle_tenant_ready(self, payload):
        tenant = request.env['saas.tenant'].sudo().search([('id_external', '=', payload.get('tenant_id'))])
        if tenant and tenant.status != 'ready':
            tenant.write({
                'status': 'ready',
                'stage': 'ready',
                'progress': 100,
                'access_url': payload.get('access_url'),
            })

    def _handle_stage_changed(self, payload):
        tenant = request.env['saas.tenant'].sudo().search([('id_external', '=', payload.get('tenant_id'))])
        if tenant:
            stage = payload.get('stage')
            progress = payload.get('progress', 0)
            stages = ['infra', 'app', 'ia', 'ready']
            if stages.index(stage) >= stages.index(tenant.stage):
                tenant.write({'stage': stage, 'progress': progress})
