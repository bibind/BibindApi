import hmac
import hashlib
import json
import logging
from typing import Any, Dict

from odoo import http
from odoo.http import request

from odoo.addons.bibind_core.models.api_client import mask_secrets

_logger = logging.getLogger("bibind")


class SaasWebhook(http.Controller):
    @http.route('/webhooks/tenant', type='json', auth='public', methods=['POST'], csrf=False)
    def tenant_webhook(self):
        secret = request.env['ir.config_parameter'].sudo().get_param('SAAS_WEBHOOK_SECRET', '')
        signature = request.httprequest.headers.get('X-Signature')
        body = request.httprequest.data
        expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature or ''):
            _logger.warning(json.dumps({"event": "invalid_signature"}))
            return http.Response('invalid signature', status=401)
        payload = json.loads(body.decode())
        correlation_id = payload.get('correlation_id') or request.httprequest.headers.get('X-Correlation-Id')
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
        if event == 'tenant.ready':
            self._handle_tenant_ready(payload)
        elif event == 'tenant.stage_changed':
            self._handle_stage_changed(payload)
        return {'status': 'ok'}

    def _handle_tenant_ready(self, payload: Dict[str, Any]):
        _logger.info(
            json.dumps(
                {
                    "action": "tenant_ready",
                    "payload": mask_secrets(payload),
                    "correlation_id": request.env.context.get('correlation_id'),
                }
            )
        )
        tenant = request.env['saas.tenant'].sudo().search([('id_external', '=', payload.get('tenant_id'))])
        if tenant and tenant.status != 'ready':
            tenant.write({
                'status': 'ready',
                'stage': 'ready',
                'progress': 100,
                'access_url': payload.get('access_url'),
            })
            self._enqueue_deployment('sync', payload)

    def _handle_stage_changed(self, payload: Dict[str, Any]):
        _logger.info(
            json.dumps(
                {
                    "action": "stage_changed",
                    "payload": mask_secrets(payload),
                    "correlation_id": request.env.context.get('correlation_id'),
                }
            )
        )
        tenant = request.env['saas.tenant'].sudo().search([('id_external', '=', payload.get('tenant_id'))])
        if tenant:
            stage = payload.get('stage')
            progress = payload.get('progress', 0)
            stages = ['infra', 'app', 'ia', 'ready']
            if stages.index(stage) >= stages.index(tenant.stage):
                tenant.write({'stage': stage, 'progress': progress})
                self._enqueue_deployment('sync', payload)

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
        correlation_id = payload.get('correlation_id') or request.httprequest.headers.get('X-Correlation-Id')
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
            self._enqueue_deployment('ai', payload)
        elif event == 'payment.succeeded':
            self._handle_payment(payload)
            self._enqueue_deployment('payment', payload)
        return {'status': 'ok'}

    def _handle_payment(self, payload: Dict[str, Any]):
        invoice_id = payload.get('invoice_id')
        if invoice_id:
            invoice = request.env['account.move'].sudo().search([('id', '=', invoice_id)])
            if invoice:
                invoice.write({'payment_state': 'paid'})
        _logger.info(
            json.dumps(
                {
                    "action": "payment_update",
                    "payload": mask_secrets(payload),
                    "correlation_id": request.env.context.get('correlation_id'),
                }
            )
        )

    def _enqueue_deployment(self, action: str, payload: Dict[str, Any]):
        if 'kb.deployment' not in request.env or 'environment_id' not in payload:
            return
        env_model = request.env['kb.environment'].sudo()
        env_rec = env_model.search([('id', '=', payload['environment_id'])])
        if not env_rec:
            return
        request.env['kb.deployment'].sudo().create({
            'environment_id': env_rec.id,
            'action': action,
            'payload': payload,
            'correlation_id': request.env.context.get('correlation_id'),
        })
