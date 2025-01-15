from odoo import models, fields, api

class BibindAPI(models.Model):
    _name = "bibind.api"
    _description = "Gestion des appels API Bibind"

    name = fields.Char(string="Nom de la configuration", required=True)
    api_url = fields.Char(string="URL de l'API", required=True, default="https://api.bibind.com")
    auth_token = fields.Char(string="Token d'authentification", required=True)
