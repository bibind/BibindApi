from decimal import Decimal

from odoo import api, fields, models


class ProjectBudget(models.Model):
    _name = "kb.project.budget"
    _description = "Project Budget"

    project_id = fields.Many2one("project.project", required=True)
    currency_id = fields.Many2one(
        "res.currency", required=True, default=lambda self: self.env.company.currency_id
    )
    labor_rate_eur_hour = fields.Monetary()
    infra_monthly_cap = fields.Monetary()
    approved = fields.Boolean(default=False)
    spent_hours = fields.Float(compute="_compute_spent")
    spent_labor = fields.Monetary(compute="_compute_spent")
    spent_infra = fields.Monetary(compute="_compute_spent")
    spent_total = fields.Monetary(compute="_compute_spent")
    burn_rate = fields.Float(compute="_compute_spent")
    velocity = fields.Float(compute="_compute_spent")
    burn_chart = fields.Json()
    velocity_chart = fields.Json()
    line_ids = fields.One2many("kb.budget.line", "budget_id")

    @api.depends("project_id")
    def _compute_spent(self):
        """Aggregate costs and KPIs for the budget."""
        timesheet_model = None
        if (
            self.env["ir.module.module"]
            .sudo()
            .search_count([("name", "=", "hr_timesheet"), ("state", "=", "installed")])
        ):
            timesheet_model = self.env.get("account.analytic.line")
        env_model = self.env["kb.environment"]
        for budget in self:
            # Hours and labor -------------------------------------------------
            hours = 0.0
            if timesheet_model and budget.project_id:
                domain = [("project_id", "=", budget.project_id.id)]
                hours = sum(timesheet_model.search(domain).mapped("unit_amount"))
            budget.spent_hours = hours
            budget.spent_labor = hours * budget.labor_rate_eur_hour

            # Infrastructure costs -------------------------------------------
            infra_cost = Decimal("0.0")
            service = budget.project_id.service_id
            if service:
                envs = env_model.search([("service_id", "=", service.id)])
                for env in envs:
                    try:
                        infra_cost += Decimal(str(env.cost_estimate or 0.0))
                    except Exception:
                        continue
            budget.spent_infra = float(infra_cost)

            # Total -----------------------------------------------------------
            budget.spent_total = budget.spent_labor + budget.spent_infra

            # KPIs ------------------------------------------------------------
            sprints = self.env["kb.sprint"].search(
                [("project_id", "=", budget.project_id.id)], order="date_start"
            )
            total_points = sum(budget.project_id.task_ids.mapped("story_points"))
            done_points = 0.0
            burn_labels: list[str] = []
            burn_values: list[float] = []
            velocities: list[float] = []
            for sprint in sprints:
                completed = sum(
                    sprint.task_ids.filtered(
                        lambda t: t.stage_id and t.stage_id.fold
                    ).mapped("story_points")
                )
                done_points += completed
                remaining = max(total_points - done_points, 0.0)
                burn_labels.append(sprint.name)
                burn_values.append(remaining)
                velocities.append(completed)
            budget.velocity = sum(velocities) / len(velocities) if velocities else 0.0
            budget.burn_rate = budget.spent_total / len(sprints) if sprints else 0.0
            budget.burn_chart = {"labels": burn_labels, "values": burn_values}
            budget.velocity_chart = {"labels": burn_labels, "values": velocities}


class BudgetLine(models.Model):
    _name = "kb.budget.line"
    _description = "Budget Line"

    budget_id = fields.Many2one("kb.project.budget", required=True)
    name = fields.Char(required=True)
    type = fields.Selection(
        [
            ("labor", "Labor"),
            ("infra", "Infrastructure"),
            ("license", "License"),
            ("misc", "Misc"),
        ],
        required=True,
    )
    amount = fields.Monetary()
    date = fields.Date(default=fields.Date.today)
    notes = fields.Text()
