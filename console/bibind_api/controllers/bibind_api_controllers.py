from odoo import http
from odoo.http import request

class BibindConsole(http.Controller):
    @http.route('/console', type='http', auth='user', website=True)
    def console_page(self, **kwargs):
        services = request.env['bibind.api'].search([('user_id', '=', request.env.user.id)])
        return request.render('bibind_api.console_template', {'services': services})
