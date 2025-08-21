from odoo import http
from odoo.http import request


class ProjectPortal(http.Controller):
    @http.route('/my/projects', auth='user', website=True)
    def list_projects(self, **kw):
        projects = request.env['project.project'].sudo().search([])
        return request.render('bibind_portal_projects.projects_portal', {'projects': projects})

    @http.route('/my/projects/<int:project_id>/sync', auth='user', website=True)
    def sync_project(self, project_id, **kw):
        project = request.env['project.project'].sudo().browse(project_id)
        project.action_sync_gitlab()
        return request.redirect('/my/projects')
