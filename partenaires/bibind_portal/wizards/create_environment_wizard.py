from __future__ import annotations

import logging
import uuid
from typing import Dict

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CreateEnvironmentWizard(models.TransientModel):
    """Wizard to create a new environment for a service."""

    _name = "kb.create.environment.wizard"
    _description = "Create Environment Wizard"

    service_id = fields.Many2one("kb.service", required=True)
    env = fields.Selection(
        [
            ("dev", "Dev"),
            ("stage", "Stage"),
            ("prod", "Prod"),
            ("custom", "Custom"),
        ],
        required=True,
    )
    region = fields.Char()
    cluster = fields.Char()
    namespace = fields.Char()
    correlation_id = fields.Char(default=lambda self: str(uuid.uuid4()))

    @api.constrains("service_id", "env")
    def _check_unique_env(self):
        for wiz in self:
            existing = self.env["kb.environment"].search(
                [
                    ("service_id", "=", wiz.service_id.id),
                    ("env", "=", wiz.env),
                ],
                limit=1,
            )
            if existing:
                raise UserError("Environment already exists for this service")

    def _build_payload(self) -> Dict[str, object]:
        return {
            "env": self.env,
            "region": self.region,
            "cluster": self.cluster,
            "namespace": self.namespace,
        }

    def action_create(self):
        self.ensure_one()
        payload = self._build_payload()
        _logger.info(
            "create environment",
            extra={
                "payload": payload,
                "service": self.service_id.id,
                "correlation_id": self.correlation_id,
            },
        )
        client = self.env["bibind.api_client"].with_context(
            correlation_id=self.correlation_id
        )
        client.create_environment(str(self.service_id.id), payload)
        env = self.env["kb.environment"].create(
            {
                "service_id": self.service_id.id,
                "env": self.env,
                "region": self.region,
                "cluster": self.cluster,
                "namespace": self.namespace,
            }
        )
        env.message_post(body=f"Environment created ({self.correlation_id})")
        return {"type": "ir.actions.act_window_close"}
