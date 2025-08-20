from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

_logger = logging.getLogger(__name__)


@dataclass
class InvoiceDTO:
    id: str
    amount: float
    currency: str
    status: str


@dataclass
class PaymentDTO:
    id: str
    amount: float
    status: str


@dataclass
class CatalogDTO:
    content: str
    content_type: str


class CircuitBreaker:
    """Very small circuit breaker implementation."""

    def __init__(self, max_failures: int = 5, reset_timeout: int = 60) -> None:
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.open_until = 0.0

    def call(self, func, *args, **kwargs):
        now = time.time()
        if self.failures >= self.max_failures and now < self.open_until:
            raise RuntimeError("Circuit breaker open")
        try:
            return func(*args, **kwargs)
        except Exception:
            self.failures += 1
            if self.failures >= self.max_failures:
                self.open_until = now + self.reset_timeout
            raise
        else:
            self.failures = 0


class KillBillClient:
    """HTTP client for Kill Bill API."""

    def __init__(self, env) -> None:
        self.env = env
        ICP = env["ir.config_parameter"].sudo()
        self.base_url = (ICP.get_param("kb_base_url") or "").rstrip("/")
        self.api_key = ICP.get_param("kb_api_key") or ""
        self.api_secret = ICP.get_param("kb_api_secret") or ""
        self.basic_login = ICP.get_param("kb_basic_auth_login") or ""
        self.basic_password = ICP.get_param("kb_basic_auth_password") or ""

        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.circuit_breaker = CircuitBreaker()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _headers(self) -> Dict[str, str]:
        return {
            "X-Killbill-ApiKey": self.api_key,
            "X-Killbill-ApiSecret": self.api_secret,
            "X-Killbill-CreatedBy": "odoo",
            "Accept": "application/json",
        }

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        headers = self._headers()
        headers.update(kwargs.pop("headers", {}))
        request_id = str(uuid.uuid4())
        headers["X-Request-Id"] = request_id
        kwargs["headers"] = headers
        kwargs.setdefault("timeout", (5, 20))
        auth = (self.basic_login, self.basic_password) if self.basic_login else None
        _logger.info("KB request %s %s", method, url, extra={"request_id": request_id})
        response = self.circuit_breaker.call(self.session.request, method, url, auth=auth, **kwargs)
        if response.status_code in (406, 415) and headers["Accept"] == "application/json":
            headers["Accept"] = "application/xml"
            response = self.circuit_breaker.call(self.session.request, method, url, auth=auth, **kwargs)
        if response.status_code >= 400:
            raise RuntimeError(f"Kill Bill error {response.status_code}: {response.text}")
        return response

    # ------------------------------------------------------------------
    # API methods
    # ------------------------------------------------------------------
    def create_account(self, external_key: str, name: str, email: str) -> str:
        payload = {"name": name, "externalKey": external_key, "email": email}
        resp = self._request("POST", "/1.0/kb/accounts", json=payload)
        location = resp.headers.get("Location", "")
        return location.rsplit("/", 1)[-1]

    def create_subscription(
        self,
        account_id: str,
        product_name: str,
        billing_period: str,
        price_list: str,
        plan_name: Optional[str] = None,
    ) -> str:
        payload = {
            "accountId": account_id,
            "productName": product_name,
            "billingPeriod": billing_period,
            "priceList": price_list,
            "productCategory": "BASE",
        }
        if plan_name:
            payload["planName"] = plan_name
        resp = self._request("POST", "/1.0/kb/subscriptions", json=payload)
        data = resp.json()
        return data.get("subscriptionId") or data.get("subscription_id") or ""

    def list_account_invoices(self, account_id: str, since_date: Optional[str] = None) -> List[InvoiceDTO]:
        params: Dict[str, Any] = {"withItems": "true"}
        if since_date:
            params["startDate"] = since_date
        resp = self._request("GET", f"/1.0/kb/accounts/{account_id}/invoices", params=params)
        data = resp.json()
        invoices: List[InvoiceDTO] = []
        for inv in data:
            invoices.append(
                InvoiceDTO(
                    id=str(inv.get("invoiceId" or inv.get("invoice_id"))),
                    amount=float(inv.get("amount") or inv.get("balance") or 0.0),
                    currency=inv.get("currency", "USD"),
                    status=inv.get("status", "UNKNOWN"),
                )
            )
        return invoices

    def get_invoice_payments(self, invoice_id: str) -> List[PaymentDTO]:
        resp = self._request("GET", f"/1.0/kb/invoices/{invoice_id}/payments")
        data = resp.json()
        payments: List[PaymentDTO] = []
        for pay in data:
            payments.append(
                PaymentDTO(
                    id=str(pay.get("paymentId" or pay.get("payment_id"))),
                    amount=float(pay.get("amount") or 0.0),
                    status=pay.get("status", "UNKNOWN"),
                )
            )
        return payments

    def get_catalog_json_or_xml(self) -> CatalogDTO:
        resp = self._request("GET", "/1.0/kb/catalog")
        content_type = resp.headers.get("Content-Type", "application/json")
        return CatalogDTO(content=resp.text, content_type=content_type)

    def upload_catalog(self, content: str, content_type: str = "application/xml") -> None:
        headers = {"Content-Type": content_type}
        self._request("POST", "/1.0/kb/catalog/xml", data=content, headers=headers)

