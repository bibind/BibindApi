from odoo import api, fields, models


class ProjectBudget(models.Model):
    _name = 'kb.project.budget'
    _description = 'Project Budget'

    project_id = fields.Many2one('project.project', required=True)
    currency_id = fields.Many2one('res.currency', required=True, default=lambda self: self.env.company.currency_id)
    labor_rate_eur_hour = fields.Monetary()
    infra_monthly_cap = fields.Monetary()
    approved = fields.Boolean(default=False)
    spent_hours = fields.Float(compute='_compute_spent')
    spent_labor = fields.Monetary(compute='_compute_spent')
    spent_infra = fields.Monetary(compute='_compute_spent')
    spent_total = fields.Monetary(compute='_compute_spent')
    burn_chart = fields.Json()
    line_ids = fields.One2many('kb.budget.line', 'budget_id')

    @api.depends('line_ids.amount')
    def _compute_spent(self):
        for budget in self:
            budget.spent_hours = 0.0
            budget.spent_labor = sum(
                l.amount for l in budget.line_ids if l.type == 'labor'
            )
            budget.spent_infra = sum(
                l.amount for l in budget.line_ids if l.type == 'infra'
            )
            budget.spent_total = budget.spent_labor + budget.spent_infra


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
