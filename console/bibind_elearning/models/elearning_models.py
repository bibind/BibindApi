from odoo import models, fields

class ElearningCourse(models.Model):
    _inherit = 'product.product'

    is_training = fields.Boolean(string="Est une formation", default=False)

class ElearningSlideChannel(models.Model):
    _inherit = 'slide.channel'

    additional_info = fields.Text(string="Informations supplémentaires")
