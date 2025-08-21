# -*- coding: utf-8 -*-
"""Security helpers for multi-tenant isolation."""
from __future__ import annotations

from typing import List

from odoo import _, api, models
from odoo.exceptions import AccessError


class SecurityHelpers(models.AbstractModel):
    _name = "bibind.security.helpers"
    _description = "Security helpers"

    @api.model
    def domain_for_tenant(self, model: str) -> List:
        """Return domain restricting records to user tenant."""
        user = self.env.user
        tid = getattr(user, "tenant_id", False)
        if not tid:
            return [("id", "=", False)]
        return ["|", ("tenant_id", "=", tid), ("tenant_id", "=", False)]

    @api.model
    def check_tenant(self, records):
        user = self.env.user
        tid = getattr(user, "tenant_id", False)
        for rec in records:
            if rec.tenant_id and rec.tenant_id != tid:
                raise AccessError(_("Access denied for tenant"))

    @api.model
    def propagate_tenant(self, vals):
        tid = getattr(self.env.user, "tenant_id", False)
        if tid and "tenant_id" not in vals:
            vals["tenant_id"] = tid
        return vals
