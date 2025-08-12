from collections import defaultdict
from datetime import date
from odoo import api, fields, models


class PayoutRunWizard(models.TransientModel):
    _name = 'saas.payout.run.wizard'
    _description = 'Generate payout run'

    date = fields.Date(default=fields.Date.today)

    def action_generate(self):
        Ledger = self.env['saas.commission.ledger']
        ledgers = Ledger.search([
            ('status', '=', 'pending'),
            ('hold_until', '<=', fields.Datetime.now()),
        ])
        if not ledgers:
            return False
        ledgers.write({'status': 'payable'})
        grouped = defaultdict(float)
        for ledger in ledgers:
            grouped[ledger.partner_id] += ledger.amount
        run = self.env['saas.payout.run'].create({
            'name': f'Payout {self.date.strftime("%Y-%m")}',
            'period_start': date(self.date.year, self.date.month, 1),
            'period_end': self.date,
            'state': 'draft',
        })
        for partner, amount in grouped.items():
            self.env['saas.payout.item'].create({
                'run_id': run.id,
                'partner_id': partner.id,
                'amount': amount,
                'currency_id': partner.currency_id.id if partner.currency_id else self.env.company.currency_id.id,
            })
        return {'type': 'ir.actions.act_window_close'}
