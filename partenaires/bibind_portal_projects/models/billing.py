from odoo import _, api, fields, models


class ProjectMilestone(models.Model):
    _name = "kb.project.milestone"
    _description = "Project Milestone"

    project_id = fields.Many2one("project.project", required=True)
    name = fields.Char(required=True)
    description = fields.Text()
    amount = fields.Monetary()
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("invoiced", "Invoiced"),
            ("paid", "Paid"),
        ],
        default="draft",
    )
    due_date = fields.Date()
    sale_order_id = fields.Many2one("sale.order")
    account_move_id = fields.Many2one("account.move")
    killbill_subscription_id = fields.Char()

    @api.model
    def _module_installed(self, name: str) -> bool:
        """Check if a module is installed in the current environment."""
        Module = self.env["ir.module.module"].sudo()
        return bool(
            Module.search_count([("name", "=", name), ("state", "=", "installed")])
        )

    def action_confirm(self):
        kb_billing = self.env["kb.billing"]
        sale_installed = self._module_installed("sale")
        for milestone in self:
            if sale_installed and milestone.sale_order_id:
                milestone.sale_order_id.action_confirm()
            else:
                kb_billing.action_confirm(milestone)
            milestone.state = "confirmed"

    def action_invoice(self):
        kb_billing = self.env["kb.billing"]
        account_installed = self._module_installed("account")
        for milestone in self:
            if account_installed and milestone.sale_order_id:
                invoice = milestone.sale_order_id._create_invoices()
                if invoice:
                    invoice.action_post()
                    milestone.account_move_id = invoice[0]
            else:
                kb_billing.action_invoice(milestone)
            milestone.state = "invoiced"

    def action_mark_paid(self):
        kb_billing = self.env["kb.billing"]
        payment_installed = self._module_installed("payment")
        for milestone in self:
            if payment_installed and milestone.account_move_id:
                milestone.account_move_id.action_post()
                milestone.account_move_id.write({"payment_state": "paid"})
            else:
                kb_billing.action_mark_paid(milestone)
            milestone.state = "paid"
