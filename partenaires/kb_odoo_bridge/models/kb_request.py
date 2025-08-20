from __future__ import annotations

import uuid

from odoo import api, fields, models


class KBRequest(models.Model):
    _name = "kb.request"
    _description = "Kill Bill Request"
    _rec_name = "request_id"

    res_model = fields.Char(required=True)
    res_id = fields.Integer(required=True)
    operation = fields.Char(required=True)
    request_id = fields.Char(default=lambda self: str(uuid.uuid4()), required=True)
    state = fields.Selection(
        [
            ("pending", "Pending"),
            ("done", "Done"),
            ("error", "Error"),
        ],
        default="pending",
    )
    message = fields.Char()

    _sql_constraints = [
        (
            "unique_request",
            "unique(res_model, res_id, operation)",
            "Request already exists",
        )
    ]

    @api.model
    def log_request(self, model: str, res_id: int, operation: str) -> "KBRequest":
        return self.create({"res_model": model, "res_id": res_id, "operation": operation})
