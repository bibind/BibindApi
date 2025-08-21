from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    gitlab_issue_id = fields.Integer(index=True)
    issue_type = fields.Selection(
        [
            ('epic', 'Epic'),
            ('story', 'Story'),
            ('task', 'Task'),
            ('bug', 'Bug'),
        ],
        default='task',
    )
    story_points = fields.Float()
    sprint_id = fields.Many2one('kb.sprint')
