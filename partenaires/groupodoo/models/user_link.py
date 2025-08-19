from odoo import fields, models


class UserLink(models.Model):
    _name = "groupodoo.user.link"
    _description = "Groupodoo User Link"

    user_id = fields.Many2one("res.users", required=True)
    bibind_user_id = fields.Char()
    external_meta = fields.Json()
    last_sync = fields.Datetime()

    _sql_constraints = [
        ("user_unique", "unique(user_id)", "User already linked"),
        ("bibind_unique", "unique(bibind_user_id)", "Bibind user already linked"),
    ]
