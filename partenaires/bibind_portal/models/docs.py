from __future__ import annotations

from odoo import fields, models

from odoo.addons.bibind_core.models.mixins import AuditMixin


class Doc(models.Model, AuditMixin):
    _name = "kb.doc"
    _description = "Service documentation"

    service_id = fields.Many2one("kb.service")
    title = fields.Char(required=True)
    content = fields.Html(sanitize=True)
    tags = fields.Many2many("ir.tags")
    version = fields.Char()
