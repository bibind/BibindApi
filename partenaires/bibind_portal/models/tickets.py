from __future__ import annotations

from typing import Dict, List

from odoo import models

from odoo.addons.bibind_core.services.api_client import ApiClient


class Ticket(models.AbstractModel):
    _name = "kb.ticket"
    _description = "Proxy helpdesk tickets"

    def create_ticket(self, service: models.Model, subject: str, body: str, attachments: List[bytes] | None = None) -> Dict[str, object]:
        client = ApiClient.from_env(self.env)
        payload = {"service": service.id, "subject": subject, "body": body}
        return client.post("/tickets", json=payload)

    def list_tickets(self, service: models.Model) -> List[Dict[str, object]]:
        client = ApiClient.from_env(self.env)
        return client.get(f"/services/{service.id}/tickets")
