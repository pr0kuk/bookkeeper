from datetime import datetime, timedelta
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from .concepts import CategoryConcept, ExpenseConcept, BudgetConcept
from bookkeeper.repository.sqlite_repository import SQLiteRepository

def get_rep(type : Category | Budget | Expense):
    return SQLiteRepository[type]("data/sqlite.db", type)


class BudgetPresenter:
    def __init__(self,  view : BudgetConcept):
        self.view = view
        self.expense_presenter = self.view.expense_presenter
        self.repo = get_rep(Budget)
        self.view.register_budget_modifier(self.modify_budget)
        self.view.register_budget_getter(self.get_budget)
        self.view.register_expense_getter(self.get_expense)

    def get_expense(self) -> list[float]:
        return [sum(self.expense_presenter.get_expenses_from_till(datetime.now(), datetime.now() - timedelta(days=d))) for d in [1, 7, 30]]

    def modify_budget(self, budget: Budget) -> None:
        self.repo.update(budget)

    def get_budget(self) -> Budget:
        budgets = self.repo.get_all()
        if len(budgets) == 0:
            budget = Budget()
            self.repo.add(budget)
            budgets.append(budget)
        return budgets.pop()