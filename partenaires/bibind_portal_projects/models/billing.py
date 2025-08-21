from odoo import _, api, fields, models


class ProjectMilestone(models.Model):
    _name = 'kb.project.milestone'
    _description = 'Project Milestone'

    project_id = fields.Many2one('project.project', required=True)
    name = fields.Char(required=True)
    description = fields.Text()
    amount = fields.Monetary()
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('invoiced', 'Invoiced'), ('paid', 'Paid')],
        default='draft',
    )
    due_date = fields.Date()
    sale_order_id = fields.Many2one('sale.order')
    account_move_id = fields.Many2one('account.move')
    killbill_subscription_id = fields.Char()

    def action_confirm(self):
        for milestone in self:
            milestone.state = 'confirmed'

    def action_invoice(self):
        for milestone in self:
            milestone.state = 'invoiced'

    def action_mark_paid(self):
        for milestone in self:
            milestone.state = 'paid'
