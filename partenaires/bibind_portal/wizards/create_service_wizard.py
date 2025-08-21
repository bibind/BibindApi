from __future__ import annotations

import logging
import uuid
from typing import Dict

from odoo import fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CreateServiceWizard(models.TransientModel):
    """Wizard to create a new service through the orchestrator."""

    _name = "kb.create.service.wizard"
    _description = "Create Service Wizard"

    name = fields.Char(required=True)
    offer = fields.Selection(
        [
            ("ecom", "E-com"),
            ("iot", "IoT"),
            ("lms", "LMS"),
        ],
        required=True,
    )
    plan = fields.Char()
    sla = fields.Selection(
        [
            ("standard", "Standard"),
            ("premium", "Premium"),
            ("enterprise", "Enterprise"),
        ]
    )
    correlation_id = fields.Char(default=lambda self: str(uuid.uuid4()))

    def _build_payload(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "offer": self.offer,
            "plan": self.plan,
            "sla": self.sla,
        }

    def action_create(self):
        self.ensure_one()
        if self.env["kb.service"].search([("name", "=", self.name)], limit=1):
            raise UserError("Service already exists")
        payload = self._build_payload()
        _logger.info(
            "create service",
            extra={"payload": payload, "correlation_id": self.correlation_id},
        )
        client = self.env["bibind.api_client"].with_context(
            correlation_id=self.correlation_id
        )
        client.create_service(payload)
        service = self.env["kb.service"].create(payload)
        service.message_post(body=f"Service created ({self.correlation_id})")
        return {"type": "ir.actions.act_window_close"}
