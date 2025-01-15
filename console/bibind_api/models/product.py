from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_bibind_service = fields.Boolean(string="Service Bibind", default=False)
