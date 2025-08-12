from odoo import models, fields


class PayoutRunWizard(models.TransientModel):
    _name = 'saas.payout.run.wizard'
    _description = 'Generate Payout Run'

    period_start = fields.Date(required=True, default=lambda self: fields.Date.today().replace(day=1))
    period_end = fields.Date(required=True, default=fields.Date.today)

    def action_generate(self):
        ledgers = self.env['saas.commission.ledger'].search([
            ('status', '=', 'pending'),
            ('hold_until', '<', fields.Datetime.now())
        ])
        if not ledgers:
            return False
        run = self.env['saas.payout.run'].create({
            'period_start': self.period_start,
            'period_end': self.period_end,
        })
        groups = {}
        for l in ledgers:
            groups.setdefault(l.partner_id, []).append(l)
        for partner, lines in groups.items():
            amount = sum(lines.mapped('amount'))
            item = self.env['saas.payout.item'].create({
                'run_id': run.id,
                'partner_id': partner.id,
                'amount': amount,
                'currency_id': partner.company_id.currency_id.id if partner.company_id else self.env.company.currency_id.id,
            })
            lines.write({'status': 'payable', 'payout_item_id': item.id})
        return run
