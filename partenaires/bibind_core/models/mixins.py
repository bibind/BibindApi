# -*- coding: utf-8 -*-
"""Reusable mixins for Bibind modules."""
from __future__ import annotations

import json
import logging
import re
import uuid
from typing import Any, Dict, List

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger("bibind")


class AuditMixin(models.AbstractModel):
    """Mixin that propagates correlation identifiers on create/write."""

    _name = "bibind.audit.mixin"
    _description = "Audit helper mixin"

    correlation_id = fields.Char(index=True, help="Correlation identifier for cross-system tracing")

    @api.model_create_multi
    def create(self, vals_list: List[Dict[str, Any]]):  # type: ignore[override]
        cid = self.env.context.get("correlation_id")
        for vals in vals_list:
            vals.setdefault("correlation_id", cid or str(uuid.uuid4()))
        records = super().create(vals_list)
        return records

    def write(self, vals: Dict[str, Any]):  # type: ignore[override]
        with self.env.cr.savepoint():
            cid = self.env.context.get("correlation_id")
            if "correlation_id" not in vals:
                vals["correlation_id"] = cid or str(uuid.uuid4())
            return super().write(vals)

    def get_correlation_id(self) -> str:
        self.ensure_one()
        return self.correlation_id or str(uuid.uuid4())


class PceMixin(models.AbstractModel):
    """Mixin that carries tenant and customer references for PCE objects."""

    _name = "bibind.pce.mixin"
    _description = "PCE helper mixin"

    tenant_id = fields.Char(index=True)
    customer_id = fields.Many2one("res.partner", index=True)
    pce_instance_id = fields.Char(index=True)

    _tenant_re = re.compile(r"^[A-Za-z0-9_-]+$")

    @api.constrains("tenant_id", "pce_instance_id")
    def _check_identifier_format(self):
        for rec in self:
            for field in ("tenant_id", "pce_instance_id"):
                value = rec[field]
                if value and not self._tenant_re.match(value):
                    raise ValidationError(_("Invalid format for %s") % field)

    @api.model_create_multi
    def create(self, vals_list: List[Dict[str, Any]]):  # type: ignore[override]
        helper = self.env["bibind.security.helpers"]
        for vals in vals_list:
            helper.propagate_tenant(vals)
        return super().create(vals_list)

    def ensure_tenant(self) -> None:
        for rec in self:
            if not rec.tenant_id:
                raise ValueError("Missing tenant on record %s" % rec.id)

    def pce_domain(self) -> List[Any]:
        """Return domain that allows access to record if tenant matches or is empty."""
        tid = self.env.user.tenant_id if hasattr(self.env.user, "tenant_id") else False
        if tid:
            return ['|', ('tenant_id', '=', tid), ('tenant_id', '=', False)]
        return []

    def with_tenant(self, tenant_id: str):
        return self.search([("tenant_id", "=", tenant_id)])


class JsonLogMixin(models.AbstractModel):
    """Mixin offering structured JSON logging bound to records."""

    _name = "bibind.jsonlog.mixin"
    _description = "JSON logger mixin"

    def _log(self, level: str, msg: str, **kwargs: Any) -> None:
        data = {
            "model": self._name,
            "ids": self.ids,
            "tenant_id": getattr(self, "tenant_id", None),
            "correlation_id": getattr(self, "correlation_id", None),
            "user_id": self.env.uid,
            "message": msg,
        }
        data.update(kwargs)
        line = json.dumps(data, ensure_ascii=False)
        getattr(_logger, level.lower())(line)

    def log_info(self, msg: str, **kwargs: Any) -> None:
        self._log("info", msg, **kwargs)

    def log_debug(self, msg: str, **kwargs: Any) -> None:
        self._log("debug", msg, **kwargs)

    def log_warning(self, msg: str, **kwargs: Any) -> None:
        self._log("warning", msg, **kwargs)

    def log_error(self, msg: str, **kwargs: Any) -> None:
        self._log("error", msg, **kwargs)

    def log_exception(self, msg: str, **kwargs: Any) -> None:
        self._log("exception", msg, **kwargs)
