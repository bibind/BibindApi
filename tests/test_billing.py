class ProjectMilestone:
    def __init__(self, amount):
        self.amount = amount
        self.state = "draft"

    def action_confirm(self):
        self.state = "confirmed"

    def action_invoice(self):
        self.state = "invoiced"

    def action_mark_paid(self):
        self.state = "paid"


def test_milestone_flow():
    ms = ProjectMilestone(1000)
    ms.action_confirm()
    assert ms.state == "confirmed"
    ms.action_invoice()
    assert ms.state == "invoiced"
    ms.action_mark_paid()
    assert ms.state == "paid"
