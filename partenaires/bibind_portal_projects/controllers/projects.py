from odoo import http
from odoo.http import request


class ProjectPortal(http.Controller):
    """Website portal for project-related pages."""

    # ------------------------------------------------------------------
    # Project listing and creation
    # ------------------------------------------------------------------
    @http.route("/my/projects", auth="user", website=True)
    def list_projects(self, **kw):
        """Display all projects for the current user."""
        projects = request.env["project.project"].sudo().search([])
        return request.render(
            "bibind_portal_projects.projects_portal", {"projects": projects}
        )

    @http.route("/my/projects/new", auth="user", website=True)
    def create_project(self, **kw):
        """Open the project creation wizard."""
        action = (
            request.env.ref("bibind_portal_projects.action_project_create_wizard")
            .sudo()
            .read()[0]
        )
        return request.redirect(f"/web#action={action['id']}")

    # ------------------------------------------------------------------
    # Project details
    # ------------------------------------------------------------------
    @http.route("/my/projects/<int:project_id>", auth="user", website=True)
    def project_detail(self, project_id: int, **kw):
        """Display details of a single project."""
        project = request.env["project.project"].sudo().browse(project_id)
        if not project.exists():
            return request.not_found()
        return request.render(
            "bibind_portal_projects.project_portal_detail", {"project": project}
        )

    # ------------------------------------------------------------------
    # Asynchronous actions
    # ------------------------------------------------------------------
    @http.route("/my/projects/<int:project_id>/sync", auth="user", website=True)
    def sync_project(self, project_id: int, **kw):
        """Trigger an asynchronous synchronization with GitLab."""
        request.env["kb.projects.facade"].sudo().with_context(
            project_id=project_id
        ).sync_gitlab()
        return request.redirect(f"/my/projects/{project_id}")

    @http.route("/my/projects/<int:project_id>/sprints/new", auth="user", website=True)
    def sprint_new(self, project_id: int, **kw):
        """Open the sprint planning wizard for the project."""
        try:
            action = (
                request.env.ref("bibind_portal_projects.action_sprint_plan_wizard")
                .sudo()
                .read()[0]
            )
        except Exception:  # pragma: no cover - defensive
            return request.redirect(
                f"/web#id={project_id}&model=project.project&view_type=form"
            )
        action["context"] = {"default_project_id": project_id}
        return request.redirect(f"/web#action={action['id']}")

    @http.route(
        "/my/projects/<int:project_id>/studio/ai",
        type="json",
        auth="user",
        methods=["POST"],
    )
    def studio_ai(self, project_id: int, **kw):
        """Launch a simple AI task for the project via the facade."""
        request.env["kb.projects.facade"].sudo().with_context(
            project_id=project_id
        ).run_studio_ai()
        return {"status": "ok"}
