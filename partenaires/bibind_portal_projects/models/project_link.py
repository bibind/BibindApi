from odoo import _, api, fields, models


class Project(models.Model):
    _inherit = 'project.project'

    service_id = fields.Many2one('kb.service', required=True, index=True)
    offer_code = fields.Char(related='service_id.offer', store=True, index=True)
    gitlab_project_id = fields.Integer(index=True)
    budget_id = fields.Many2one('kb.project.budget')
    kpi_velocity = fields.Float(compute='_compute_kpi_velocity')
    kpi_burndown = fields.Json()
    studio_ai_state = fields.Selection(
        [
            ('idle', 'Idle'),
            ('running', 'Running'),
            ('done', 'Done'),
            ('failed', 'Failed'),
        ],
        default='idle',
    )

    @api.constrains('service_id')
    def _check_service(self):
        for project in self:
            if not project.service_id:
                raise models.ValidationError(_('A service is required for every project.'))

    def action_open_service(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'kb.service',
            'res_id': self.service_id.id,
            'view_mode': 'form',
        }

    def action_sync_gitlab(self):
        for project in self:
            project.env['kb.projects.facade'].with_context(project_id=project.id).sync_gitlab()

    def action_open_studio(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/my/projects/{self.id}/studio',
            'target': 'self',
        }

    def _compute_kpi_velocity(self):
        for project in self:
            project.kpi_velocity = 0.0
