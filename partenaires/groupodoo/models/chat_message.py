from odoo import api, fields, models, tools


class ChatMessage(models.Model):
    _name = "groupodoo.chat.message"
    _description = "Groupodoo Chat Message"
    _order = "ts desc"

    session_id = fields.Many2one(
        "groupodoo.chat.session", required=True, index=True, ondelete="cascade"
    )
    direction = fields.Selection(
        [("outbound", "Outbound"), ("inbound", "Inbound")], required=True
    )
    role = fields.Selection(
        [("user", "User"), ("assistant", "Assistant"), ("system", "System")],
        default="user",
    )
    content = fields.Text()
    payload_json = fields.Json()
    error = fields.Char()
    ts = fields.Datetime(default=fields.Datetime.now, index=True)

    @api.model
    def create(self, vals):
        if vals.get("content"):
            vals["content"] = tools.html_sanitize(vals["content"])
        return super().create(vals)

    def write(self, vals):
        if vals.get("content"):
            vals["content"] = tools.html_sanitize(vals["content"])
        return super().write(vals)
