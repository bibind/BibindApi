from odoo import api, fields, models


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

    @api.model
    def create_from_issue(self, issue):
        """Create a task from a GitLab issue dict."""
        vals = {
            'name': issue.get('title'),
            'description': issue.get('description'),
            'gitlab_issue_id': issue.get('id'),
            'issue_type': issue.get('type') or 'task',
            'story_points': issue.get('story_points', 0.0),
        }
        if issue.get('sprint_id'):
            vals['sprint_id'] = issue['sprint_id']
        return self.create(vals)

    def update_from_issue(self, issue):
        """Update the task from a GitLab issue dict."""
        vals = {
            k: v
            for k, v in {
                'name': issue.get('title'),
                'description': issue.get('description'),
                'issue_type': issue.get('type'),
                'story_points': issue.get('story_points'),
            }.items()
            if v is not None
        }
        if issue.get('sprint_id'):
            vals['sprint_id'] = issue['sprint_id']
        if vals:
            self.write(vals)
        return True

    def to_issue_payload(self):
        """Return a dict payload representing the task for GitLab."""
        self.ensure_one()
        return {
            'id': self.gitlab_issue_id,
            'title': self.name,
            'description': self.description,
            'type': self.issue_type,
            'story_points': self.story_points,
            'sprint_id': self.sprint_id.id,
        }
