from odoo import api, fields, models


class StudioAI(models.Model):
    _name = 'kb.studio.ai'
    _description = 'AI Tasks for Project'

    project_id = fields.Many2one('project.project', required=True)
    name = fields.Char(required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('running', 'Running'), ('done', 'Done'), ('failed', 'Failed')],
        default='draft',
    )
    result = fields.Text()

    def run_task(self):
        for task in self:
            task.state = 'done'
            task.result = 'ok'
