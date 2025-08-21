from __future__ import annotations

import logging
from typing import Dict

from odoo import api, fields, models
from odoo.exceptions import UserError

from odoo.addons.bibind_core.models.mixins import AuditMixin, PceMixin
from odoo.addons.bibind_core.services.api_client import ApiClient

_logger = logging.getLogger(__name__)


class Service(models.Model, AuditMixin, PceMixin):
    """Service offered to a customer.

    This model stores the high level information of a service.  It inherits
    :class:`AuditMixin` and :class:`PceMixin` provided by ``bibind_core`` to
    handle tenant isolation and auditing.
    """

    _name = "kb.service"
    _description = "Customer service"
    _inherit = ["mail.thread"]

    name = fields.Char(required=True, tracking=True)
    offer = fields.Selection([
        ("ecom", "E‑com"),
        ("iot", "IoT"),
        ("lms", "LMS"),
    ], tracking=True)
    plan = fields.Char()
    sla = fields.Selection([
        ("standard", "Standard"),
        ("premium", "Premium"),
        ("enterprise", "Enterprise"),
    ])
    customer_id = fields.Many2one("res.partner", index=True)
    labels = fields.Many2many("ir.tags")
    environments = fields.One2many("kb.environment", "service_id")
    total_cost_estimate = fields.Monetary(string="Total cost", compute="compute_total_cost")
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)

    def action_open(self):
        """Open the form view of the service."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
        }

    @api.depends("environments.cost_estimate")
    def compute_total_cost(self):
        for service in self:
            service.total_cost_estimate = sum(service.environments.mapped("cost_estimate"))

    def get_links(self) -> Dict[str, str]:
        """Return contextual links for the service.

        The API client knows how to build URLs for the service based on the
        tenant context.
        """
        self.ensure_one()
        client = ApiClient.from_env(self.env)
        try:
            return client.get_context(self, fields=["admin", "api", "gitlab"])
        except Exception as exc:  # pragma: no cover - defensive
            _logger.exception("api context failed: %s", exc)
            return {}

    def message_post(self, **kwargs):  # type: ignore[override]
        """Log messages in JSON format for consistency."""
        kwargs.setdefault("body", kwargs.get("body", ""))
        return super().message_post(**kwargs)
