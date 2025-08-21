from __future__ import annotations

import logging
from typing import Dict

from odoo import api, fields, models
from odoo.exceptions import UserError

from odoo.addons.bibind_core.models.mixins import AuditMixin, PceMixin
from odoo.addons.bibind_core.services.orchestrator import ServiceOrchestrator

_logger = logging.getLogger(__name__)


class Environment(models.Model, AuditMixin, PceMixin):
    """Service environment such as dev/stage/prod."""

    _name = "kb.environment"
    _description = "Service environment"
    _inherit = ["mail.thread"]

    service_id = fields.Many2one("kb.service", index=True, required=True)
    env = fields.Selection([
        ("dev", "Dev"),
        ("stage", "Stage"),
        ("prod", "Prod"),
        ("custom", "Custom"),
    ], required=True, index=True)
    region = fields.Char(index=True)
    cluster = fields.Char(index=True)
    namespace = fields.Char(index=True)
    status = fields.Selection([
        ("provisioning", "Provisioning"),
        ("running", "Running"),
        ("degraded", "Degraded"),
        ("stopped", "Stopped"),
        ("failed", "Failed"),
    ], index=True, default="provisioning")
    cost_estimate = fields.Monetary()
    backup_policy = fields.Selection([
        ("daily-7", "Daily 7"),
        ("hourly-48", "Hourly 48"),
        ("continuous", "Continuous"),
    ])
    monitoring_profile = fields.Selection([
        ("basic", "Basic"),
        ("plus", "Plus"),
        ("enterprise", "Enterprise"),
    ])
    hpa = fields.Boolean()
    replicas = fields.Integer(default=1)
    db_tier = fields.Selection([("s", "Small"), ("m", "Medium"), ("l", "Large")])
    cache_tier = fields.Selection([("s", "Small"), ("m", "Medium"), ("l", "Large")])
    gitlab_project_id = fields.Integer(index=True)
    deployments_count = fields.Integer(compute="_compute_deployments_count")
    docs_count = fields.Integer(compute="_compute_docs_count")
    tickets_count = fields.Integer(compute="_compute_tickets_count")
    currency_id = fields.Many2one("res.currency", related="service_id.currency_id", store=True)

    def _compute_deployments_count(self):
        for env in self:
            env.deployments_count = self.env["kb.deployment"].search_count([("environment_id", "=", env.id)])

    def _compute_docs_count(self):
        for env in self:
            env.docs_count = self.env["kb.doc"].search_count([("service_id", "=", env.service_id.id)])

    def _compute_tickets_count(self):
        for env in self:
            env.tickets_count = self.env["kb.ticket"].search_count([("service_id", "=", env.service_id.id)])

    # Command pattern wrappers -------------------------------------------------

    def _validate_command(self, verb: str) -> None:
        """Ensure the user and environment can execute a command."""
        self.check_access_rights("write")
        self.check_access_rule("write")
        allowed = {
            "start": ["stopped"],
            "stop": ["running", "degraded"],
            "scale": ["running", "degraded"],
            "backup": ["running", "degraded"],
            "restore": ["running", "degraded", "stopped"],
            "promote": ["running"],
            "rollback": ["running", "degraded"],
            "extension_add": ["running", "stopped"],
            "migrate": ["running", "stopped"],
        }
        if verb in allowed and self.status not in allowed[verb]:
            raise UserError("Environment state does not allow this action")
        if not self.env.context.get("deployment_window_open", True):
            raise UserError("Deployment window is closed")

    def _run_command(self, verb: str, payload: Dict[str, object] | None = None) -> Dict[str, object]:
        self.ensure_one()
        self._validate_command(verb)
        payload = payload or {}
        orchestrator: ServiceOrchestrator = self.env["bibind.service_orchestrator"]
        correlation_id = payload.get("correlation_id") or self.env.context.get("correlation_id")
        headers = {"X-Correlation-Id": correlation_id} if correlation_id else {}
        _logger.info("env command %s", verb, extra={"env": self.id, "payload": payload})
        return orchestrator.run(self.id, verb, payload=payload, headers=headers)

    def do_start(self):
        self._run_command("start")

    def do_stop(self):
        self._run_command("stop")

    def do_scale(self, replicas: int):
        self._run_command("scale", {"replicas": replicas})

    def do_backup(self):
        self._run_command("backup")

    def do_restore(self):
        self._run_command("restore")

    def do_promote(self):
        self._run_command("promote")

    def do_rollback(self):
        self._run_command("rollback")

    def do_extension_add(self, extension: str):
        self._run_command("extension_add", {"extension": extension})

    def do_migrate(self, target: str):
        self._run_command("migrate", {"target": target})
