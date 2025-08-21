# -*- coding: utf-8 -*-
"""HTTP client to op_bootstrap with resiliency features."""
from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from odoo import api, models

_logger = logging.getLogger("bibind")


class ApiClientError(Exception):
    def __init__(self, message: str, status: int | None = None, correlation_id: str | None = None):
        super().__init__(message)
        self.status = status
        self.correlation_id = correlation_id


class ApiClientAuthError(ApiClientError):
    pass


class ApiClientServerError(ApiClientError):
    pass


class ApiClientCircuitOpen(ApiClientError):
    pass


@dataclass
class _CircuitBreaker:
    fail_max: int
    reset_timeout_s: int
    failures: int = 0
    opened_at: float = 0.0

    def allow(self) -> bool:
        if self.failures < self.fail_max:
            return True
        if time.time() - self.opened_at >= self.reset_timeout_s:
            return True
        return False

    def on_success(self) -> None:
        self.failures = 0
        self.opened_at = 0.0

    def on_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.fail_max and not self.opened_at:
            self.opened_at = time.time()


class ApiClient(models.AbstractModel):
    _name = "bibind.api_client"
    _description = "Adapter to op_bootstrap"

    _token: Dict[str, Any] = {}
    _breaker: Optional[_CircuitBreaker] = None

    # ------------------------------------------------------------------
    # Configuration helpers
    # ------------------------------------------------------------------
    @api.model
    def _session(self) -> requests.Session:
        timeout = self.env["bibind.param.store"].get_int("http_timeout_s", 10)
        retry = Retry(
            total=self.env["bibind.param.store"].get_int("http_retry_total", 3),
            backoff_factor=self.env["bibind.param.store"].get_float("http_backoff_factor", 0.5),
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["GET", "POST", "PUT", "PATCH", "DELETE"]),
        )
        adapter = HTTPAdapter(max_retries=retry)
        s = requests.Session()
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        s.request = self._wrap_request(s.request, timeout)  # type: ignore
        return s

    def _wrap_request(self, func, timeout):
        def wrapper(method, url, **kwargs):
            kwargs.setdefault("timeout", timeout)
            return func(method, url, **kwargs)

        return wrapper

    # ------------------------------------------------------------------
    def resolve_secret_ref(self, ref: str) -> str:
        raise ApiClientError(f"Secret reference {ref} cannot be resolved")

    # Token management --------------------------------------------------
    def _get_token(self) -> str:
        now = time.time()
        token = self._token
        if token and token.get("expires_at", 0) > now:
            return token["access_token"]
        store = self.env["bibind.param.store"]
        url = store.get_param("kc_token_url")
        client_id = self.resolve_secret_ref(store.get_param("kc_client_id_ref"))
        client_secret = self.resolve_secret_ref(store.get_param("kc_client_secret_ref"))
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        resp = requests.post(url, data=data, timeout=10)
        if resp.status_code != 200:
            raise ApiClientAuthError("Unable to fetch token", resp.status_code)
        payload = resp.json()
        expires_in = payload.get("expires_in", 60)
        token = {
            "access_token": payload["access_token"],
            "expires_at": now + expires_in - 5,
        }
        self._token = token
        return token["access_token"]

    # Headers -----------------------------------------------------------
    def _headers(self, correlation_id: Optional[str]) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/json",
            "X-Correlation-Id": correlation_id or str(uuid.uuid4()),
        }

    # Breaker ----------------------------------------------------------
    def _get_breaker(self) -> _CircuitBreaker:
        if not self._breaker:
            store = self.env["bibind.param.store"]
            self._breaker = _CircuitBreaker(
                store.get_int("breaker_fail_max", 5),
                store.get_int("breaker_reset_s", 60),
            )
        return self._breaker

    # Request ----------------------------------------------------------
    def _request(
        self,
        method: str,
        path: str,
        json_body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        expected: int | tuple = (200, 201, 202),
    ) -> Dict[str, Any]:
        base = self.env["bibind.param.store"].get_param("op_bootstrap_base_url")
        url = f"{base.rstrip('/')}/{path.lstrip('/')}"
        correlation_id = self.env.context.get("correlation_id")
        headers = self._headers(correlation_id)
        if method in ("POST", "PUT", "PATCH", "DELETE"):
            headers.setdefault("X-Request-Id", str(uuid.uuid4()))
        breaker = self._get_breaker()
        if not breaker.allow():
            raise ApiClientCircuitOpen("circuit open", correlation_id=correlation_id)
        session = self._session()
        started = time.time()
        try:
            _logger.info(
                json.dumps(
                    {
                        "event": "http.request",
                        "method": method,
                        "url": url,
                        "params": params,
                        "correlation_id": headers["X-Correlation-Id"],
                        "request_id": headers.get("X-Request-Id"),
                    }
                )
            )
            resp: Response = session.request(
                method, url, json=json_body, params=params, headers=headers
            )
            elapsed = int((time.time() - started) * 1000)
            _logger.info(
                json.dumps(
                    {
                        "event": "http.response",
                        "status": resp.status_code,
                        "elapsed_ms": elapsed,
                        "correlation_id": headers["X-Correlation-Id"],
                    }
                )
            )
        except requests.RequestException as exc:
            breaker.on_failure()
            raise ApiClientServerError(str(exc), correlation_id=headers["X-Correlation-Id"]) from exc
        if resp.status_code == 401:
            self._token = {}
            token = self._get_token()
            headers["Authorization"] = f"Bearer {token}"
            resp = session.request(method, url, json=json_body, params=params, headers=headers)
        if resp.status_code >= 500:
            breaker.on_failure()
            raise ApiClientServerError(
                f"Server error {resp.status_code}", resp.status_code, headers["X-Correlation-Id"]
            )
        if resp.status_code in (429,):
            breaker.on_failure()
            raise ApiClientServerError("Too many requests", resp.status_code, headers["X-Correlation-Id"])
        breaker.on_success()
        if isinstance(expected, int):
            expected = (expected,)
        if resp.status_code not in expected:
            raise ApiClientError(
                f"Unexpected status {resp.status_code}", resp.status_code, headers["X-Correlation-Id"]
            )
        if resp.content:
            return resp.json()
        return {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get_context(self, instance_id: str) -> Dict[str, Any]:
        return self._request("GET", f"context/{instance_id}")

    def create_service(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "service", json_body=payload, expected=201)

    def create_environment(self, service_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", f"service/{service_id}/environment", json_body=payload, expected=201)

    def post_deploy(self, env_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", f"environment/{env_id}/deploy", json_body=payload, expected=202)

    def get_deploy_status(self, deploy_id: str) -> Dict[str, Any]:
        return self._request("GET", f"deploy/{deploy_id}")

    def post_deploy_action(self, deploy_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", f"deploy/{deploy_id}/action", json_body=payload, expected=202)

    def create_backup(self, env_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", f"environment/{env_id}/backup", json_body=payload, expected=202)

    def restore(self, env_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", f"environment/{env_id}/restore", json_body=payload, expected=202)

    def get_signed_link(self, env_id: str, link_type: str) -> Dict[str, Any]:
        return self._request("GET", f"environment/{env_id}/link/{link_type}")

    def create_issue(self, project_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", f"gitlab/{project_id}/issue", json_body=payload, expected=201)

    def create_merge_request(self, project_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", f"gitlab/{project_id}/mr", json_body=payload, expected=201)

    def trigger_pipeline(self, project_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", f"gitlab/{project_id}/pipeline", json_body=payload, expected=202)

    def ai_task(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "ai/task", json_body=payload, expected=202)

    def ai_task_status(self, task_id: str) -> Dict[str, Any]:
        return self._request("GET", f"ai/task/{task_id}")

    def ai_callback_consume(self, payload: Dict[str, Any]) -> None:
        self._request("POST", "ai/callback", json_body=payload, expected=200)
        return None
