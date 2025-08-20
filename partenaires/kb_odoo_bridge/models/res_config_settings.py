from __future__ import annotations

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    kb_base_url = fields.Char(config_parameter="kb_base_url")
    kb_api_key = fields.Char(config_parameter="kb_api_key")
    kb_api_secret = fields.Char(config_parameter="kb_api_secret")
    kb_basic_auth_login = fields.Char(config_parameter="kb_basic_auth_login")
    kb_basic_auth_password = fields.Char(config_parameter="kb_basic_auth_password")
    kb_webhook_secret = fields.Char(config_parameter="kb_webhook_secret")
    kb_sync_window_days = fields.Integer(config_parameter="kb_sync_window_days", default=30)
