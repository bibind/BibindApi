from datetime import timedelta
from odoo import models, fields, api


class SaasTenant(models.Model):
    _name = 'saas.tenant'
    _description = 'SaaS Tenant'

    name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    plan = fields.Selection([('start', 'Start'), ('pro', 'Pro'), ('scale', 'Scale')], default='start')
    addons = fields.Char()
    region = fields.Selection([('eu-west-3', 'EU West 3'), ('us-east-1', 'US East 1')], default='eu-west-3')
    admin_email = fields.Char()
    status = fields.Selection([
        ('provisioning', 'Provisioning'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
        ('suspended', 'Suspended'),
    ], default='provisioning')
    stage = fields.Selection([
        ('infra', 'Infra'),
        ('app', 'App'),
        ('ia', 'IA'),
        ('ready', 'Ready'),
    ], default='infra')
    progress = fields.Integer(default=0)
    trial_end_at = fields.Datetime()
    access_url = fields.Char()
    id_external = fields.Char(index=True)
    subscription_id = fields.Many2one('sale.subscription')


    @api.model
    def cron_trial_expiring(self):
        soon = fields.Datetime.now() + timedelta(days=3)
        tenants = self.search([('trial_end_at', '<=', soon), ('status', '=', 'ready')])
        return True
