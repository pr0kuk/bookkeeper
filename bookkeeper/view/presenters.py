"""
Presenters File
"""
from typing import TypeVar, Any
from datetime import datetime, timedelta
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from .concepts import BudgetWidget, CategoryWidget

T = TypeVar('T', bound=Budget | Category | Expense)


def get_rep(model_type: type[T]) -> SQLiteRepository[T]:
    """
    Получить sqlite репозиторий для объекта типа type

    Parameters
    ----------
    type - тип объекта, для которого получить репозиторий

    Returns
    -------
    Объект класса SQLiteRepository
    """
    return SQLiteRepository[T]("data/sqlite.db", model_type)


class BudgetPresenter:
    """
    Presenter для виджета бюджета
    """

    def __init__(self, view: BudgetWidget):
        self.view = view
        self.expense_presenter = self.view.expense_presenter
        self.repo = get_rep(Budget)
        self.view.register_budget_modifier(self.modify_budget)
        self.view.register_budget_getter(self.get_budget)
        self.view.register_expense_getter(self.get_expense)

    def get_expense(self) -> list[float]:
        """
        Получить суммы расходов за 1, 7, 30 дней
        """
        return [sum(self.expense_presenter.get_expenses_from_till(
            datetime.now(), datetime.now() - timedelta(days=d))) for d in [1, 7, 30]]

    def modify_budget(self, budget: Budget) -> None:
        """
        Изменить бюджет
        """
        self.repo.update(budget)

    def get_budget(self) -> Budget:
        """
        Получить объект бюджета
        """
        budgets = self.repo.get_all()
        if len(budgets) == 0:
            budget = Budget()
            self.repo.add(budget)
            budgets.append(budget)
        return budgets.pop()


class CategoryPresenter:
    """
    Presenter для виджета категория
    """

    def __init__(self, view: CategoryWidget):
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
        """
        Изменить категорию
        """
        self.category_repo.update(category)

    def check_name(self, name: str) -> bool:
        """
        Проверить по имени существует ли категория
        """
        if name in [category.name for category in self.categories]:
            return False
        return True

    def find_category_by_name(self, name: str) -> int | None:
        """
        Найти id по имени категории
        """
        for category in self.categories:
            if category.name == name:
                return int(category.pk)
        return None

    def add_category(self, category: Category) -> None:
        """
        Добавить категорию
        """
        self.category_repo.add(category)
        self.categories.append(category)

    def delete_category(self, top_lvl_category: Category) -> None:
        """
        Удалить категорию
        """
        queue = [top_lvl_category]
        to_delete = []
        while len(queue) != 0:
            proc = queue.pop()
            to_delete.append(proc)
            queue.extend([x for x in self.categories if x.parent == proc.pk])
        for x in to_delete:
            self.categories.remove(x)
            self.category_repo.delete(x.pk)


class ExpensePresenter:
    """
    Presenter для виджета расходов
    """

    def __init__(self, view: Any):
        self.view = view
        self.repo = get_rep(Expense)
        self.category_repo = get_rep(Category)
        self.expenses = self.repo.get_all()
        self.view.register_expense_adder(self.add_expense)
        self.view.register_expense_deleter(self.delete_expense)
        self.view.register_expense_modifier(self.modify_expense)
        self.view.register_category_retriever(self.retrieve_category)
        self.view.set_expense_list(self.expenses)

    def retrieve_category(self, pk: int) -> str | None:
        """
        Получить название категории по id
        """
        category = self.category_repo.get(pk)
        if category is None:
            return None
        return str(category.name)

    def add_expense(self, expense: Expense) -> None:
        """
        Добавить расход
        """
        self.repo.add(expense)
        self.expenses.append(expense)

    def delete_expense(self, expense: Expense) -> None:
        """
        Удалить расход
        """
        self.expenses.remove(expense)
        self.repo.delete(expense.pk)

    def modify_expense(self, expense: Expense) -> None:
        """
        Изменить запись расхода
        """
        self.repo.update(expense)

    def get_expenses_from_till(self, start: datetime, end: datetime) -> list[float]:
        """
        Получить список всех расходов в определённый период
        """
        assert start > end
        return [x.amount for x in self.expenses if x.expense_date <
                start and x.expense_date > end]
