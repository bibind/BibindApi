from __future__ import annotations

import json
from typing import Any, Dict

from lxml import etree
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from ..models.kb_client import KillBillClient


class KBCatalogPullWizard(models.TransientModel):
    _name = "kb.catalog.pull.wizard"
    _description = "Import Kill Bill Catalog"

    def action_pull(self) -> None:
        client = KillBillClient(self.env)
        catalog = client.get_catalog_json_or_xml()
        if catalog.content_type.startswith("application/json"):
            data = json.loads(catalog.content)
            self._import_json(data)
        else:
            xml_root = etree.fromstring(catalog.content.encode())
            self._import_xml(xml_root)

    # ------------------------------------------------------------------
    def _import_json(self, data: Dict[str, Any]) -> None:
        products = data.get("products", [])
        for prod in products:
            tmpl = self.env["product.template"].search([["kb_product_name", "=", prod.get("name")]], limit=1)
            vals = {
                "name": prod.get("name"),
                "kb_product_name": prod.get("name"),
                "kb_plan_name": prod.get("plans", [{}])[0].get("name"),
                "kb_billing_period": prod.get("plans", [{}])[0].get("billingPeriod"),
                "kb_price_list": prod.get("plans", [{}])[0].get("priceList", "DEFAULT"),
                "kb_is_subscription": True,
            }
            if tmpl:
                tmpl.write(vals)
            else:
                self.env["product.template"].create(vals)

    def _import_xml(self, root: etree._Element) -> None:
        ns = root.nsmap.get(None, "")
        for prod in root.findall(f"{{{ns}}}product"):
            name = prod.findtext(f"{{{ns}}}name")
            plan = prod.find(f"{{{ns}}}plans/{{{ns}}}plan")
            period = plan.findtext(f"{{{ns}}}billingPeriod") if plan is not None else None
            plan_name = plan.findtext(f"{{{ns}}}name") if plan is not None else None
            tmpl = self.env["product.template"].search([["kb_product_name", "=", name]], limit=1)
            vals = {
                "name": name,
                "kb_product_name": name,
                "kb_plan_name": plan_name,
                "kb_billing_period": period,
                "kb_price_list": "DEFAULT",
                "kb_is_subscription": True,
            }
            if tmpl:
                tmpl.write(vals)
            else:
                self.env["product.template"].create(vals)
