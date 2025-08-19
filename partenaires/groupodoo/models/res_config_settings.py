from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    groupodoo_api_base_url = fields.Char(config_parameter="groupodoo_api_base_url")
    groupodoo_webhook_secret = fields.Char(config_parameter="groupodoo_webhook_secret")
