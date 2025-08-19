from odoo import fields, models


class SaasProvisioningJob(models.Model):
    _name = 'saas.provisioning.job'
    _description = 'Provisioning Job'

    tenant_id = fields.Many2one('saas.tenant', required=True)
    stage = fields.Selection([
        ('infra', 'Infra'),
        ('app', 'App'),
        ('ia', 'IA'),
        ('ready', 'Ready'),
    ], default='infra')
    progress = fields.Integer(default=0)
    error = fields.Text()
    idempotency_key = fields.Char(required=True, copy=False)
    started_at = fields.Datetime()
    finished_at = fields.Datetime()
