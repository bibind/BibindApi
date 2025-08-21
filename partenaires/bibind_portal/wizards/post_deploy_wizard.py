from __future__ import annotations

import logging
import uuid
from typing import Dict

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PostDeployWizard(models.TransientModel):
    """Wizard to trigger post-deploy actions."""

    _name = "kb.post.deploy.wizard"
    _description = "Post Deploy Wizard"

    environment_id = fields.Many2one("kb.environment", required=True)
    ref = fields.Char(required=True)
    correlation_id = fields.Char(default=lambda self: str(uuid.uuid4()))

    def _build_payload(self) -> Dict[str, object]:
        return {"ref": self.ref}

    def action_post_deploy(self):
        self.ensure_one()
        payload = self._build_payload()
        _logger.info(
            "post deploy",
            extra={
                "env": self.environment_id.id,
                "payload": payload,
                "correlation_id": self.correlation_id,
            },
        )
        client = self.env["bibind.api_client"].with_context(
            correlation_id=self.correlation_id
        )
        client.post_deploy(str(self.environment_id.id), payload)
        self.environment_id.message_post(
            body=f"Post deploy triggered ({self.correlation_id})"
        )
        return {"type": "ir.actions.act_window_close"}
