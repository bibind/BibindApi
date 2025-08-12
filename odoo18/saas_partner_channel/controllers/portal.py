import json
from odoo import http
from odoo.http import request


class SaasPortal(http.Controller):
    @http.route('/saas/portal/deal', type='http', auth='portal', methods=['POST'], csrf=True)
    def portal_deal(self, **post):
        vals = {
            'name': post.get('name'),
            'partner_id': request.env.user.partner_id.id,
            'company_name': post.get('company_name'),
            'amount': float(post.get('amount') or 0.0),
        }
        request.env['saas.deal'].sudo().create(vals)
        return request.redirect('/my')

    @http.route('/saas/portal/tenant/create', type='http', auth='portal', methods=['POST'], csrf=True)
    def portal_tenant_create(self, **post):
        partner = request.env.user.partner_id
        vals = {
            'name': post.get('company_name'),
            'partner_id': partner.id,
            'admin_email': post.get('admin_email'),
            'region': post.get('region'),
            'plan': post.get('plan'),
            'status': 'provisioning',
        }
        tenant = request.env['saas.tenant'].sudo().create(vals)
        request.env['saas.provisioning.job'].sudo().create({
            'tenant_id': tenant.id,
            'stage': 'infra',
            'idempotency_key': request.env['ir.sequence'].next_by_code('saas.provisioning.job') or 'manual',
        })
        payload = {
            'company_name': post.get('company_name'),
            'admin_email': post.get('admin_email'),
            'region': post.get('region'),
            'plan': post.get('plan'),
        }
        request.env['saas.api'].sudo().create_tenant(partner, payload)
        return request.redirect(f'/saas/portal/tenant/{tenant.id}')

    @http.route('/saas/portal/tenant/<int:tenant_id>', type='http', auth='portal', website=True)
    def portal_tenant_status(self, tenant_id, **kw):
        tenant = request.env['saas.tenant'].sudo().browse(tenant_id)
        return request.render('saas_partner_channel.portal_tenant_status', {'tenant': tenant})
