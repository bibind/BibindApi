from odoo import models


class GitLabSync(models.AbstractModel):
    _name = 'kb.sync.gitlab'
    _description = 'GitLab Synchronization Facade'

    def pull_issues(self, project):
        return []

    def push_tasks(self, project, tasks):
        return True
