import hmac
import hashlib
import json
import logging
import uuid

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied

from odoo.addons.bibind_core.models.api_client import mask_secrets

_logger = logging.getLogger("bibind")


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

    @http.route('/webhooks/op_bootstrap', type='json', auth='public', methods=['POST'], csrf=False)
    def op_bootstrap_webhook(self):
        secret = request.env['ir.config_parameter'].sudo().get_param('SAAS_WEBHOOK_SECRET', '')
        signature = request.httprequest.headers.get('X-Signature')
        body = request.httprequest.data
        expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature or ''):
            _logger.warning(json.dumps({"event": "invalid_signature"}))
            return http.Response('invalid signature', status=401)
        payload = json.loads(body.decode())
        correlation_id = (
            payload.get('correlation_id')
            or request.httprequest.headers.get('X-Correlation-Id')
            or str(uuid.uuid4())
        )
        request.env = request.env(context=dict(request.env.context, correlation_id=correlation_id))
        event = payload.get('event')
        _logger.info(
            json.dumps(
                {
                    "event": event,
                    "payload": mask_secrets(payload),
                    "correlation_id": correlation_id,
                }
            )
        )
        if event == 'ai.task.status':
            request.env['bus.bus'].sendone('ai.task.status', payload)
        elif event == 'payment.succeeded':
            invoice_id = payload.get('invoice_id')
            if invoice_id:
                invoice = request.env['account.move'].sudo().search([('id', '=', invoice_id)])
                if invoice:
                    invoice.write({'payment_state': 'paid'})
            _logger.info(
                json.dumps(
                    {
                        "action": "payment_update",
                        "invoice_id": payload.get('invoice_id'),
                        "correlation_id": correlation_id,
                    }
                )
            )
        response = {'status': 'ok', 'correlation_id': correlation_id}
        _logger.info(json.dumps({"response": response}))
        return response
