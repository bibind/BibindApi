from odoo import _, api, fields, models
from odoo.exceptions import RedirectWarning


class Project(models.Model):
    _inherit = 'project.project'

    service_id = fields.Many2one('kb.service', required=True, index=True)
    offer_code = fields.Char(related='service_id.offer', store=True, index=True)
    gitlab_project_id = fields.Integer(index=True)
    budget_id = fields.Many2one('kb.project.budget')
    sprint_ids = fields.One2many('kb.sprint', 'project_id')
    kpi_velocity = fields.Float(compute='compute_kpis')
    kpi_burndown = fields.Json(compute='compute_kpis')
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
                action = project.env.ref(
                    "bibind_portal_projects.action_project_create_wizard"
                )
                raise RedirectWarning(
                    _('A service is required for every project.'),
                    action.id,
                    _('Select or create a service'),
                )

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

    @api.depends('task_ids.story_points', 'task_ids.stage_id', 'task_ids.sprint_id')
    def compute_kpis(self):
        for project in self:
            # Gather sprints ordered by start date
            sprints = self.env['kb.sprint'].search([
                ('project_id', '=', project.id)
            ], order='date_start')
            total_points = sum(project.task_ids.mapped('story_points'))
            done_points = 0.0
            labels = []
            values = []
            velocities = []
            for sprint in sprints:
                completed = sum(
                    sprint.task_ids.filtered(lambda t: t.stage_id and t.stage_id.fold).mapped('story_points')
                )
                done_points += completed
                remaining = max(total_points - done_points, 0.0)
                labels.append(sprint.name)
                values.append(remaining)
                velocities.append(completed)
            project.kpi_velocity = sum(velocities) / len(velocities) if velocities else 0.0
            project.kpi_burndown = {
                'labels': labels,
                'values': values,
            }
