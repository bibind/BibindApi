from __future__ import annotations

from decimal import Decimal
from typing import Dict

from odoo import api, models

from odoo.addons.bibind_core.services.api_client import ApiClient


class CostEstimate(models.AbstractModel):
    """Helpers to estimate costs via the external API."""

    _name = "kb.cost.estimate"
    _description = "Cost estimation helpers"

    def estimate_for_env(self, env: models.Model) -> Decimal:
        client = ApiClient.from_env(self.env)
        resp = client.get(f"/environments/{env.id}/costs:estimate")
        amount = resp.get("amount", 0.0)
        return Decimal(str(amount))

    def refresh_all_for_service(self, service: models.Model) -> Dict[int, Decimal]:
        amounts: Dict[int, Decimal] = {}
        for env in service.environments:
            value = self.estimate_for_env(env)
            env.cost_estimate = value
            amounts[env.id] = value
        service.compute_total_cost()
        return amounts
