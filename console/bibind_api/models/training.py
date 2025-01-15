from odoo import models, fields

class Training(models.Model):
    _name = "bibind.training"
    _description = "Gestion des formations Bibind"

    name = fields.Char(string="Nom de la formation", required=True)
    description = fields.Text(string="Description")
    duration = fields.Float(string="Durée (heures)", required=True)
