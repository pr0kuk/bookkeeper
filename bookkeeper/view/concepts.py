"""
Концепты виджетов
"""
from typing import Protocol, Callable
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense


class ExpenseConcept(Protocol):
    """
    Концепт виджета расходов
    """
    def register_expense_adder(self, handler: Callable[[Expense], None]) -> None:
        """
        Установить обработчик добавления расходов
        """

    def register_expense_deleter(self, handler: Callable[[Expense], None]) -> None:
        """
        Установить обработчик удаления расходов
        """

    def register_expense_modifier(self, handler: Callable[[Expense], None]) -> None:
        """
        Установить обработчик изменения расходов
        """

    def register_category_retriever(self, handler: Callable[[int], str | None]) -> None:
        """
        Установить обработчик получения расходов
        """

    def set_expense_list(self, data: list[Expense]) -> None:
        """
        Установить обработчик инициализации расходов
        """


class CategoryConcept(Protocol):
    """
    Концепт виджета категорий
    """
    def set_category_list(self, categories: list[Category]) -> None:
        """
        Установить обработчик инициализации категорий
        """

    def register_category_modifier(self, handler: Callable[[Category], None]) -> None:
        """
        Установить обработчик изменения категории
        """

    def register_category_adder(self, handler: Callable[[Category], None]) -> None:
        """
        Установить обработчик добавления категории
        """

    def register_category_checker(self, handler: Callable[[str], bool]) -> None:
        """
        Установить обработчик проверки категории
        """

    def register_category_finder(self, handler: Callable[[str], None | int]) -> None:
        """
        Установить обработчик поиска категории
        """

    def register_category_deleter(self, handler: Callable[[Category], None]) -> None:
        """
        Установить обработчик удаления категории
        """


class BudgetConcept(Protocol):
    """
    Концепт виджета бюджета
    """
    expense_presenter: ExpenseConcept

    def register_bgt_modifier(self, handler: Callable[[Budget], None]) -> None:
        """
        Установить обработчик изменения бюджета
        """


    def register_bgt_getter(self, handler: Callable[[], Budget]) -> None:
        """
        Установить обработчик получения бюджета
        """


    def register_expense_getter(self, handler: Callable[[], list[float]]) -> None:
        """
        Установить обработчик получения расходов
        """
