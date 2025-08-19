import uuid
from odoo import api, fields, models


class ChatSession(models.Model):
    _name = "groupodoo.chat.session"
    _description = "Groupodoo Chat Session"
    _order = "last_activity desc"

    name = fields.Char(required=True)
    uuid = fields.Char(
        string="UUID",
        required=True,
        copy=False,
        index=True,
        default=lambda self: str(uuid.uuid4()),
    )
    user_id = fields.Many2one("res.users", required=True, index=True)
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company, index=True
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("closed", "Closed"),
            ("error", "Error"),
        ],
        default="draft",
        index=True,
    )
    bibind_conversation_id = fields.Char()
    n8n_workflow_id = fields.Char()
    last_activity = fields.Datetime()
    idempotency_key = fields.Char(index=True)
    privacy = fields.Selection(
        [("portal", "Portal"), ("internal", "Internal")], default="portal"
    )

    _sql_constraints = [
        ("uuid_unique", "unique(uuid)", "UUID must be unique."),
        (
            "idempotency_key_unique",
            "unique(idempotency_key)",
            "Idempotency key must be unique.",
        ),
    ]
