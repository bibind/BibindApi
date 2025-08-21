import base64

from odoo import fields, models

# The lightweight ``ApiClient`` is imported from the top-level module so
# tests can monkeypatch it easily.
from bibind_core import ApiClient


class StudioAI(models.Model):
    _name = 'kb.studio.ai'
    _description = 'AI Tasks for Project'

    project_id = fields.Many2one('project.project', required=True)
    name = fields.Char(required=True)
    mode = fields.Selection(
        [
            ('so_conception', 'Conception'),
            ('so_organisation', 'Organisation'),
            ('so_planification', 'Planification'),
            ('so_qualite', 'Qualité'),
            ('so_realisation', 'Réalisation'),
        ],
        required=True,
    )
    state = fields.Selection(
        [('draft', 'Draft'), ('running', 'Running'), ('done', 'Done'), ('failed', 'Failed')],
        default='draft',
    )
    result = fields.Text()

    def run_task(self):
        """Execute the AI task by delegating to the API client."""
        client = ApiClient.from_env(self.env)
        for task in self:
            task.state = 'running'
            payload = {
                'mode': task.mode,
                'project_id': task.project_id.id,
                'input': task.name,
            }
            try:
                # Interact with the generic ``/ai/tasks`` endpoint.
                response = client.post("/ai/tasks", payload)
                task.result = response.get('result', '')
                task.state = 'done'
                # store result as attachment
                if task.result:
                    data = base64.b64encode(task.result.encode())
                    attachment = self.env['ir.attachment'].create({
                        'name': f"ai-{task.mode}-{task.id}.txt",
                        'datas': data,
                        'res_model': task._name,
                        'res_id': task.id,
                        'type': 'binary',
                        'mimetype': 'text/plain',
                    })
                    # create tasks and merge requests based on result
                    facade = self.env['kb.projects.facade']
                    facade.create_task(task.project_id, {
                        'title': task.name,
                        'description': task.result,
                    })
                    facade.create_merge_request(task.project_id, {
                        'title': task.name,
                        'description': task.result,
                    })
            except Exception:  # pragma: no cover - defensive
                task.state = 'failed'
