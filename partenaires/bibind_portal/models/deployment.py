from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, Optional

from odoo import api, fields, models

from odoo.addons.bibind_core.models.mixins import AuditMixin

_logger = logging.getLogger(__name__)


class Deployment(models.Model, AuditMixin):
    """Deployment history for environments."""

    _name = "kb.deployment"
    _description = "Deployment"
    _inherit = ["mail.thread"]

    environment_id = fields.Many2one("kb.environment", required=True, index=True)
    action = fields.Selection([
        ("plan", "Plan"),
        ("apply", "Apply"),
        ("promote", "Promote"),
        ("rollback", "Rollback"),
        ("scale", "Scale"),
        ("stop", "Stop"),
        ("start", "Start"),
        ("backup", "Backup"),
        ("restore", "Restore"),
    ], required=True)
    status = fields.Selection([
        ("queued", "Queued"),
        ("running", "Running"),
        ("succeeded", "Succeeded"),
        ("failed", "Failed"),
    ], default="queued", tracking=True)
    correlation_id = fields.Char(index=True)
    payload = fields.Json()
    outputs = fields.Json()
    started_at = fields.Datetime()
    finished_at = fields.Datetime()

    def mark_running(self):
        self.write({"status": "running", "started_at": fields.Datetime.now()})

    def mark_succeeded(self, outputs: Optional[Dict[str, object]] = None):
        vals = {"status": "succeeded", "finished_at": fields.Datetime.now()}
        if outputs:
            vals["outputs"] = outputs
        self.write(vals)

    def mark_failed(self, outputs: Optional[Dict[str, object]] = None):
        vals = {"status": "failed", "finished_at": fields.Datetime.now()}
        if outputs:
            vals["outputs"] = outputs
        self.write(vals)

    def as_timeline_item(self) -> Dict[str, object]:
        self.ensure_one()
        return {
            "action": self.action,
            "status": self.status,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "outputs": self.outputs,
        }
