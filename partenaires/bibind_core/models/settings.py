# -*- coding: utf-8 -*-
"""Configuration panel and parameter store for Bibind."""
from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ParamStore(models.AbstractModel):
    _name = "bibind.param.store"
    _description = "Parameters accessor"

    @api.model
    @lru_cache(maxsize=128)
    def get_param(self, key: str, default: Any = None) -> Any:
        ICP = self.env["ir.config_parameter"].sudo()
        return ICP.get_param(key, default)

    @api.model
    def get_int(self, key: str, default: int = 0) -> int:
        v = self.get_param(key)
        try:
            return int(v)
        except (TypeError, ValueError):
            return default

    @api.model
    def get_float(self, key: str, default: float = 0.0) -> float:
        v = self.get_param(key)
        try:
            return float(v)
        except (TypeError, ValueError):
            return default

    @api.model
    def get_bool(self, key: str, default: bool = False) -> bool:
        v = self.get_param(key)
        if isinstance(v, str):
            return v.lower() in ("1", "true", "yes")
        return bool(v) if v is not None else default

    @api.model
    def get_log_level(self) -> int:
        lv = (self.get_param("log_level") or "INFO").upper()
        return getattr(logging, lv, logging.INFO)

    @api.model
    def clear_cache(self) -> None:
        self.get_param.cache_clear()  # type: ignore


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    op_bootstrap_base_url = fields.Char(string="Bootstrap URL")
    kc_token_url = fields.Char(string="Keycloak Token URL")
    kc_client_id_ref = fields.Char(string="Client ID ref")
    kc_client_secret_ref = fields.Char(string="Client secret ref")
    http_timeout_s = fields.Integer(string="HTTP timeout (s)")
    http_retry_total = fields.Integer(string="HTTP retries")
    http_backoff_factor = fields.Float(string="Backoff factor")
    breaker_fail_max = fields.Integer(string="Breaker fail max")
    breaker_reset_s = fields.Integer(string="Breaker reset (s)")
    log_level = fields.Selection([
        ("DEBUG", "DEBUG"),
        ("INFO", "INFO"),
        ("WARNING", "WARNING"),
        ("ERROR", "ERROR"),
    ], string="Log level")

    def set_values(self):  # type: ignore[override]
        res = super().set_values()
        ICP = self.env["ir.config_parameter"].sudo()
        for field in [
            "op_bootstrap_base_url",
            "kc_token_url",
            "kc_client_id_ref",
            "kc_client_secret_ref",
            "http_timeout_s",
            "http_retry_total",
            "http_backoff_factor",
            "breaker_fail_max",
            "breaker_reset_s",
            "log_level",
        ]:
            value = getattr(self, field)
            if value or value == 0:
                ICP.set_param(field, value)
        self.env["bibind.param.store"].clear_cache()
        return res

    @api.model
    def get_values(self):  # type: ignore[override]
        res = super().get_values()
        store = self.env["bibind.param.store"]
        for field in [
            "op_bootstrap_base_url",
            "kc_token_url",
            "kc_client_id_ref",
            "kc_client_secret_ref",
            "http_timeout_s",
            "http_retry_total",
            "http_backoff_factor",
            "breaker_fail_max",
            "breaker_reset_s",
            "log_level",
        ]:
            res[field] = store.get_param(field)
        return res

    def action_test_connection(self):
        client = self.env["bibind.api_client"]
        try:
            client.get_context("ping")
        except ApiClientError as exc:  # type: ignore[name-defined]
            raise UserError(_("Connection failed: %s") % exc) from exc
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {"message": _("Connection successful"), "type": "success"},
        }
