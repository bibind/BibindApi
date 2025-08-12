from odoo import http
from odoo.http import request
import uuid


class SaasPortal(http.Controller):
    @http.route('/saas/portal/deal', type='http', auth='user', methods=['POST'], website=True)
    def portal_deal(self, **kwargs):
        partner = request.env.user.partner_id
        values = {
            'name': kwargs.get('name'),
            'partner_id': partner.id,
            'company_name': kwargs.get('company_name'),
        }
        request.env['saas.deal'].sudo().create(values)
        return request.redirect('/my')

    @http.route('/saas/portal/tenant/create', type='http', auth='user', methods=['POST'], csrf=False)
    def portal_tenant_create(self, **kwargs):
        partner = request.env.user.partner_id
        tenant = request.env['saas.tenant'].sudo().create({
            'name': kwargs.get('company_name'),
            'partner_id': partner.id,
            'admin_email': kwargs.get('admin_email'),
            'region': kwargs.get('region'),
            'plan': kwargs.get('plan'),
            'status': 'provisioning',
        })
        idem_key = str(uuid.uuid4())
        request.env['saas.provisioning.job'].sudo().create({
            'tenant_id': tenant.id,
            'idempotency_key': idem_key,
        })
        payload = {
            'company_name': tenant.name,
            'admin_email': tenant.admin_email,
            'region': tenant.region,
            'plan': tenant.plan,
            'id_external': tenant.id_external,
        }
        request.env['saas.api'].sudo().create_tenant(partner.id, payload, idem_key)
        return request.redirect('/saas/portal/tenant/%s' % tenant.id)

    @http.route('/saas/portal/tenant/<int:tenant_id>', type='http', auth='user', website=True)
    def portal_tenant_view(self, tenant_id, **kw):
        tenant = request.env['saas.tenant'].sudo().browse(tenant_id)
        return request.render('saas_partner_channel.portal_tenant_status', {'tenant': tenant})
