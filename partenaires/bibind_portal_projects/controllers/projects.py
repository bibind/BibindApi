from odoo import http
from odoo.http import request


class ProjectPortal(http.Controller):
    @http.route("/my/projects", auth="user", website=True)
    def list_projects(self, **kw):
        projects = request.env["project.project"].sudo().search([])
        return request.render(
            "bibind_portal_projects.projects_portal", {"projects": projects}
        )


    @http.route('/my/projects/new', auth='user', website=True)
    def create_project(self, **kw):
        action = (
            request.env.ref("bibind_portal_projects.action_project_create_wizard")
            .sudo()
            .read()[0]
        )
        return request.redirect(f"/web#action={action['id']}")

    @http.route('/my/projects/<int:project_id>/sync', auth='user', website=True)
    def sync_project(self, project_id, **kw):
        project = request.env["project.project"].sudo().browse(project_id)
        project.action_sync_gitlab()
        return request.redirect("/my/projects")

    @http.route(
        "/my/projects/<int:project_id>/milestones/<int:milestone_id>/invoice",
        auth="user",
        website=True,
    )
    def invoice_milestone(self, project_id, milestone_id, **kw):
        milestone = request.env["kb.project.milestone"].sudo().browse(milestone_id)
        milestone.action_invoice()
        return request.redirect(f"/my/projects/{project_id}")
