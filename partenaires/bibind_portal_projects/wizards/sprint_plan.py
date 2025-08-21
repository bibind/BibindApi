from odoo import api, fields, models


class SprintPlanWizard(models.TransientModel):
    _name = "kb.sprint.plan.wizard"
    _description = "Sprint Planning Wizard"

    project_id = fields.Many2one(
        "project.project",
        required=True,
        default=lambda self: self.env.context.get("default_project_id"),
    )
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    capacity_hours = fields.Float()
    task_ids = fields.Many2many(
        "project.task",
        string="Stories",
        domain="[('project_id','=',project_id), ('issue_type','=','story'), ('sprint_id','=', False)]",
    )

    def action_plan(self):
        self.ensure_one()
        name = self.env.context.get("default_name") or f"Sprint {self.date_start}"
        sprint = self.env["kb.sprint"].create(
            {
                "project_id": self.project_id.id,
                "name": name,
                "date_start": self.date_start,
                "date_end": self.date_end,
                "capacity_hours": self.capacity_hours,
            }
        )
        self.task_ids.write({"sprint_id": sprint.id})
        return {"type": "ir.actions.act_window_close"}
