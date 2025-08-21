from __future__ import annotations

from typing import List, Dict

from odoo import models

from odoo.addons.bibind_core.services.api_client import ApiClient


class Billing(models.AbstractModel):
    _name = "kb.billing"
    _description = "Billing helpers"

    def get_invoices(self, service: models.Model) -> List[Dict[str, object]]:
        client = ApiClient.from_env(self.env)
        return client.get(f"/services/{service.id}/invoices")
