from odoo import models, fields, api

class UpdateCompany(models.TransientModel):
    _name = "bibind.company.update"
    _description = "Mise à jour de la société principale avec des données Bibind"

    def update_company_info(self):
        company = self.env.company
        company.write({
            'name': 'Bibind',
            'phone': '+33 112345678',
            'email': 'contact@bibind.com',
        })
