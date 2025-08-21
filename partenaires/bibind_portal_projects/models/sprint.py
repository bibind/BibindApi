from odoo import api, fields, models


class Sprint(models.Model):
    _name = 'kb.sprint'
    _description = 'Sprint'

    project_id = fields.Many2one('project.project', required=True, index=True)
    name = fields.Char(required=True)
    date_start = fields.Date()
    date_end = fields.Date()
    goal = fields.Char()
    state = fields.Selection(
        [
            ('planned', 'Planned'),
            ('active', 'Active'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],
        default='planned',
    )
    capacity_hours = fields.Float()
    velocity = fields.Float(compute='_compute_velocity')
    task_ids = fields.One2many('project.task', 'sprint_id')

    def _compute_velocity(self):
        for sprint in self:
            sprint.velocity = sum(sprint.task_ids.mapped('story_points'))
