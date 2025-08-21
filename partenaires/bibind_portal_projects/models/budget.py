from decimal import Decimal

from odoo import api, fields, models


class ProjectBudget(models.Model):
    _name = 'kb.project.budget'
    _description = 'Project Budget'

    project_id = fields.Many2one('project.project', required=True)
    currency_id = fields.Many2one('res.currency', required=True, default=lambda self: self.env.company.currency_id)
    labor_rate_eur_hour = fields.Monetary()
    infra_monthly_cap = fields.Monetary()
    approved = fields.Boolean(default=False)
    spent_hours = fields.Float(compute="_compute_spent")
    spent_labor = fields.Monetary(compute="_compute_spent")
    spent_infra = fields.Monetary(compute="_compute_spent")
    spent_total = fields.Monetary(compute="_compute_spent")
    burn_chart = fields.Json()
    line_ids = fields.One2many('kb.budget.line', 'budget_id')

    @api.depends("project_id")
    def _compute_spent(self):
        timesheet_model = self.env.get("account.analytic.line")
        cost_service = self.env["kb.cost.estimate"]
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
                for env in service.environments:
                    try:
                        infra_cost += cost_service.estimate_for_env(env)
                    except Exception:
                        continue
            budget.spent_infra = float(infra_cost)

            # Total -----------------------------------------------------------
            budget.spent_total = budget.spent_labor + budget.spent_infra
            budget.burn_chart = budget.project_id.kpi_burndown


class BudgetLine(models.Model):
    _name = 'kb.budget.line'
    _description = 'Budget Line'

    budget_id = fields.Many2one('kb.project.budget', required=True)
    name = fields.Char(required=True)
    type = fields.Selection(
        [
            ('labor', 'Labor'),
            ('infra', 'Infrastructure'),
            ('license', 'License'),
            ('misc', 'Misc'),
        ],
        required=True,
    )
    amount = fields.Monetary()
    date = fields.Date(default=fields.Date.today)
    notes = fields.Text()
