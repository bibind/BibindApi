from __future__ import annotations

import json
from lxml import etree
from odoo import fields, models

from ..models.kb_client import KillBillClient


class KBCatalogPushWizard(models.TransientModel):
    _name = "kb.catalog.push.wizard"
    _description = "Publish Catalog to Kill Bill"

    format = fields.Selection([
        ("json", "JSON"),
        ("xml", "XML"),
    ], default="json", required=True)

    def action_push(self) -> None:
        client = KillBillClient(self.env)
        products = self.env["product.template"].search([["kb_is_subscription", "=", True]])
        if self.format == "json":
            payload = self._export_json(products)
            client.upload_catalog(json.dumps(payload), "application/json")
        else:
            xml = self._export_xml(products)
            client.upload_catalog(xml, "application/xml")

    def _export_json(self, products):
        items = []
        for p in products:
            items.append({
                "name": p.kb_product_name or p.name,
                "plans": [{
                    "name": p.kb_plan_name or p.kb_product_name or p.name,
                    "billingPeriod": p.kb_billing_period or "MONTH",
                    "priceList": p.kb_price_list or "DEFAULT",
                }],
            })
        return {"products": items}

    def _export_xml(self, products) -> str:
        root = etree.Element("catalog")
        for p in products:
            prod_el = etree.SubElement(root, "product")
            etree.SubElement(prod_el, "name").text = p.kb_product_name or p.name
            plans_el = etree.SubElement(prod_el, "plans")
            plan_el = etree.SubElement(plans_el, "plan")
            etree.SubElement(plan_el, "name").text = p.kb_plan_name or p.name
            etree.SubElement(plan_el, "billingPeriod").text = p.kb_billing_period or "MONTH"
            etree.SubElement(plan_el, "priceList").text = p.kb_price_list or "DEFAULT"
        return etree.tostring(root, xml_declaration=True, encoding="UTF-8").decode()
