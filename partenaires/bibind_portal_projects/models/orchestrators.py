from odoo import api, models


class ProjectsFacade(models.Model):
    _name = 'kb.projects.facade'
    _description = 'Projects Facade'

    @api.model
    def sync_gitlab(self):
        project = self.env['project.project'].browse(self.env.context.get('project_id'))
        self.env['kb.sync.gitlab'].pull_issues(project)
        return True
