"""
Концепты виджетов
"""
from __future__ import annotations
from typing import Protocol, Callable
from datetime import datetime
from PySide6 import QtCore, QtWidgets
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.view.category.category_window import EditCategoryWindow
from bookkeeper.view.expenses.expense_table import Table
from bookkeeper.view.category.category_item import CategoryItem


class ExpensePresenter:
    """
    Концепт презентера расходов
    """
    get_expenses_from_till: Callable[[datetime, datetime], list[float]]

    def retrieve_category(self, pk: int) -> str | None:
        """
        Получить название категории по id
        """

    def add_expense(self, expense: Expense) -> None:
        """
        Добавить расход
        """

    def delete_expense(self, expense: Expense) -> None:
        """
        Удалить расход
        """

    def modify_expense(self, expense: Expense) -> None:
        """
        Изменить запись расхода
        """


class ExpenseWidget(Protocol):
    """
    Концепт виджета расходов
    """
    category_view: CategoryWidget
    table: Table
    expense_changed: QtCore.Signal
    category_retriever: Callable[[int], None | str]
    expense_adder: Callable[[Expense], None]
    expense_deleter: Callable[[Expense], None]
    expense_modifier: Callable[[Expense], None]
    edit_category_window: EditCategoryWindow

    def set_expense_list(self, data: list[Expense]) -> None:
        """
        Инициализация списка расходов
        """

    def update_categories(self) -> None:
        """
        Обновить категории
        """

    def emit_expense_changed(self) -> None:
        """
        Создать сигнал изменения расходов
        """

    def register_category_retriever(self, handler: Callable[[int], None | str]) -> None:
        """
        Установить обработчик получения расходов
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


class CategoryWidget(Protocol):
    """
    Концепт виджета категорий
    """

    def set_category_list(self, categories: list[Category]) -> None:
        """
        Инициализировать дерево категорий
        """

    def delete_category(self, category_item: CategoryItem, *_: int) -> None:
        """
        Удалить категорию
        """

    def rename_category(self, category_item: CategoryItem, column: int) -> None:
        """
        Переименовать категорию
        """

    def set_err_category(self, category_item: CategoryItem, column: int) -> None:
        """
        Установка категорию с уже существующим именем
        """

    def edit_category_event(self, category_item: CategoryItem, column: int) -> None:
        """
        Обработчик изменения названия категории
        """

    def add_category_event(self) -> None:
        """
        Обработчик добавления категории
        """

    def add_supercategory(self) -> None:
        """
        Добавить категорию без родителя
        """

    def delete_category_event(self) -> None:
        """
        Обработчик удаления категории
        """

    def get_selected_category(self) -> QtWidgets.QTreeWidgetItem:
        """
        Получить текущий элемент дерева
        """

    def register_category_adder(self, handler: Callable[[Category], None]) -> None:
        """
        Установить обработчик добавления категории
        """

    def register_category_modifier(self, handler: Callable[[Category], None]) -> None:
        """
        Установить обработчик изменения категории
        """

    def register_category_checker(self, handler: Callable[[str], bool]) -> None:
        """
        Установить обработчик проверки категории
        """

    def register_category_deleter(self, handler: Callable[[Category], None]) -> None:
        """
        Установить обработчик удаления категории
        """

    def register_category_finder(self, handler: Callable[[str], None | int]) -> None:
        """
        Установить обработчик поиска категории
        """


class BudgetWidget(Protocol):
    """
    Концепт виджета бюджета
    """
    expense_presenter: ExpensePresenter

    def register_budget_modifier(self, handler: Callable[[Budget], None]) -> None:
        """
        Установить обработчик изменения бюджета
        """

    def register_budget_getter(self, handler: Callable[[], Budget]) -> None:
        """
        Установить обработчик получения бюджета
        """

    def register_expense_getter(self, handler: Callable[[], list[float]]) -> None:
        """
        Установить обработчик получения расходов
        """
