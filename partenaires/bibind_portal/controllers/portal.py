from __future__ import annotations

import logging

from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal

_logger = logging.getLogger(__name__)


class BibindCustomerPortal(CustomerPortal):
    """Portal pages for Bibind services."""

    @http.route("/my/home", type="http", auth="user", website=True)
    def home(self, **kw):
        services = http.request.env["kb.service"].sudo().search([])
        values = self._prepare_portal_layout_values()
        values.update({"services": services})
        return http.request.render("bibind_portal.portal_home", values)

    @http.route("/my/services", type="http", auth="user", website=True)
    def services(self, **kw):
        services = http.request.env["kb.service"].sudo().search([])
        values = self._prepare_portal_layout_values()
        values.update({"services": services})
        return http.request.render("bibind_portal.portal_services", values)

    @http.route("/my/services/<int:service_id>", type="http", auth="user", website=True)
    def service_detail(self, service_id: int, **kw):
        service = http.request.env["kb.service"].sudo().browse(service_id)
        if not service.exists():
            return http.request.not_found()
        values = self._prepare_portal_layout_values()
        values.update({"service": service})
        return http.request.render("bibind_portal.portal_service_detail", values)
