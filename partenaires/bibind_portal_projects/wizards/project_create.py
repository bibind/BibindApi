from odoo import fields, models


class ProjectCreateWizard(models.TransientModel):
    """Wizard helping to select or create a service before creating a project."""

    _name = "kb.project.create.wizard"
    _description = "Project Create Wizard"

    name = fields.Char(required=True)
    service_id = fields.Many2one("kb.service")

    def action_next(self):
        """Create the project or redirect to service creation wizard."""
        self.ensure_one()
        if not self.service_id:
            action = self.env.ref("bibind_portal.action_create_service_wizard").read()[0]
            action.setdefault("context", {})["default_name"] = self.name
            return action
        project = self.env["project.project"].create(
            {"name": self.name, "service_id": self.service_id.id}
        )
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "res_id": project.id,
            "view_mode": "form",
            "target": "current",
        }
