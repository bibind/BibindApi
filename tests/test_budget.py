class BudgetLine:
    def __init__(self, type, amount):
        self.type = type
        self.amount = amount


class ProjectBudget:
    def __init__(self):
        self.line_ids = []
        self.spent_labor = 0
        self.spent_infra = 0
        self.spent_total = 0

    def compute(self):
        self.spent_labor = sum(l.amount for l in self.line_ids if l.type == "labor")
        self.spent_infra = sum(l.amount for l in self.line_ids if l.type == "infra")
        self.spent_total = self.spent_labor + self.spent_infra


def test_budget_compute():
    budget = ProjectBudget()
    budget.line_ids = [
        BudgetLine("labor", 100),
        BudgetLine("infra", 50),
        BudgetLine("labor", 40),
    ]
    budget.compute()
    assert budget.spent_labor == 140
    assert budget.spent_infra == 50
    assert budget.spent_total == 190
