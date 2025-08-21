from odoo import _, api, fields, models


class ProjectDoc(models.Model):
    _name = 'kb.project.doc'
    _description = 'Project Document'

    project_id = fields.Many2one('project.project', required=True)
    title = fields.Char(required=True)
    content_html = fields.Html()
    tags = fields.Char()
    version = fields.Char()
    attachment_ids = fields.Many2many('ir.attachment')

    def action_ai_spec_from_idea(self, idea_text):
        self.ensure_one()
        # Placeholder for AI call
        self.content_html = f"<p>{idea_text}</p>"

    def action_ai_plan(self):
        self.ensure_one()
        return True
