"""Project documentation with AI helpers."""

import base64

from odoo import fields, models

from odoo.addons.bibind_core.services.api_client import ApiClient


class ProjectDoc(models.Model):
    _name = 'kb.project.doc'
    _description = 'Project Document'

    project_id = fields.Many2one('project.project', required=True)
    title = fields.Char(required=True)
    content_html = fields.Html()
    tags = fields.Char()
    version = fields.Char()
    attachment_ids = fields.Many2many('ir.attachment')

    # ------------------------------------------------------------------
    # AI helpers
    # ------------------------------------------------------------------
    def _call_ai(self, mode: str, prompt: str) -> str:
        """Invoke the remote AI service and return the raw result."""
        client = ApiClient.from_env(self.env)
        payload = {
            'mode': mode,
            'project_id': self.project_id.id,
            'input': prompt,
        }
        response = client.ai_task(payload)
        result = response.get('result', '')
        if result:
            data = base64.b64encode(result.encode())
            attachment = self.env['ir.attachment'].create({
                'name': f"ai-{mode}-{self.id}.txt",
                'datas': data,
                'res_model': self._name,
                'res_id': self.id,
                'type': 'binary',
                'mimetype': 'text/plain',
            })
            self.attachment_ids = [(4, attachment.id)]
            facade = self.env['kb.projects.facade']
            facade.create_task(self.project_id, {
                'title': self.title,
                'description': result,
            })
            facade.create_merge_request(self.project_id, {
                'title': self.title,
                'description': result,
            })
        return result

    def action_ai_spec_from_idea(self, idea_text):
        self.ensure_one()
        result = self._call_ai('so_conception', idea_text)
        self.content_html = f"<p>{result}</p>"

    def action_ai_plan(self):
        self.ensure_one()
        result = self._call_ai('so_planification', self.title)
        self.content_html = f"<p>{result}</p>"

    def action_ai_organisation(self):  # pragma: no cover - placeholder
        self.ensure_one()
        self._call_ai('so_organisation', self.title)

    def action_ai_quality(self):  # pragma: no cover - placeholder
        self.ensure_one()
        self._call_ai('so_qualite', self.title)

    def action_ai_realisation(self):  # pragma: no cover - placeholder
        self.ensure_one()
        self._call_ai('so_realisation', self.title)

    def action_approve(self):  # pragma: no cover - placeholder
        self.ensure_one()
        return True

    def action_reject(self):  # pragma: no cover - placeholder
        self.ensure_one()
        return True
