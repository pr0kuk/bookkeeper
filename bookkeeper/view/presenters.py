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

class CategoryPresenter:
    def __init__(self,  view: CategoryConcept):
        self.view = view
        self.category_repo = get_rep(Category)
        self.categories = self.category_repo.get_all()
        self.view.set_category_list(self.categories)
        self.view.register_category_modifier(self.modify_category)
        self.view.register_category_adder(self.add_category)
        self.view.register_category_checker(self.check_name)
        self.view.register_category_deleter(self.delete_category)
        self.view.register_category_finder(self.find_category_by_name)

    def modify_category(self, category: Category) -> None:
        self.category_repo.update(category)

    def check_name(self, name: str) -> bool:
        if name in [category.name for category in self.categories]:
            return False
        return True

    def find_category_by_name(self, name: str) -> int | None:
        for category in self.categories:
            if category.name == name:
                return int(category.pk)
        return None

    def add_category(self, category: Category) -> None:
        self.category_repo.add(category)
        self.categories.append(category)

    def delete_category(self, top_lvl_category: Category) -> None:
        queue = [top_lvl_category]
        to_delete = []
        while len(queue) != 0:
            proc = queue.pop()
            to_delete.append(proc)
            queue.extend([x for x in self.categories if x.parent == proc.pk])
        for x in to_delete:
            self.categories.remove(x)
            self.category_repo.delete(x.pk)

