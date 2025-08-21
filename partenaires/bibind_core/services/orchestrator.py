# -*- coding: utf-8 -*-
"""Client for the external service orchestrator."""
from __future__ import annotations

import json
import logging
import uuid
from typing import Any, Dict, Optional

import requests
from odoo import models

_logger = logging.getLogger("bibind")


class OrchestratorError(Exception):
    """Base error raised by :class:`ServiceOrchestrator`."""

    def __init__(self, message: str, status: int | None = None, correlation_id: str | None = None):
        super().__init__(message)
        self.status = status
        self.correlation_id = correlation_id


class OrchestratorAuthError(OrchestratorError):
    """Authentication error."""


class OrchestratorServerError(OrchestratorError):
    """5xx server side error."""


class ServiceOrchestrator(models.AbstractModel):
    _name = "bibind.service_orchestrator"
    _description = "HTTP client to orchestrate environments"

    # ------------------------------------------------------------------
    def _base_url(self) -> str:
        return self.env["bibind.param.store"].get_param("orchestrator_base_url")

    def _headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = headers or {}
        correlation_id = headers.get("X-Correlation-Id") or str(uuid.uuid4())
        request_id = headers.get("X-Request-Id") or str(uuid.uuid4())
        return {
            "Content-Type": "application/json",
            "X-Correlation-Id": correlation_id,
            "X-Request-Id": request_id,
        }

    # ------------------------------------------------------------------
    def run(
        self,
        env_id: int,
        verb: str,
        payload: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Invoke a command on the orchestrator."""

        payload = payload or {}
        headers = self._headers(headers)
        base = self._base_url()
        url = f"{base.rstrip('/')}/environment/{env_id}/{verb}"
        _logger.info(
            json.dumps(
                {
                    "event": "orchestrator.request",
                    "url": url,
                    "verb": verb,
                    "env": env_id,
                    "correlation_id": headers["X-Correlation-Id"],
                    "request_id": headers["X-Request-Id"],
                }
            )
        )
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
        except requests.RequestException as exc:  # pragma: no cover - network issue
            raise OrchestratorServerError(
                str(exc), correlation_id=headers["X-Correlation-Id"]
            ) from exc
        _logger.info(
            json.dumps(
                {
                    "event": "orchestrator.response",
                    "status": resp.status_code,
                    "correlation_id": headers["X-Correlation-Id"],
                    "request_id": headers["X-Request-Id"],
                }
            )
        )
        if resp.status_code == 401:
            raise OrchestratorAuthError("Unauthorized", resp.status_code, headers["X-Correlation-Id"])
        if resp.status_code >= 500:
            raise OrchestratorServerError(
                f"Server error {resp.status_code}", resp.status_code, headers["X-Correlation-Id"]
            )
        if resp.status_code >= 400:
            raise OrchestratorError(
                f"Error {resp.status_code}", resp.status_code, headers["X-Correlation-Id"]
            )
        if resp.content:
            return resp.json()
        return {}
