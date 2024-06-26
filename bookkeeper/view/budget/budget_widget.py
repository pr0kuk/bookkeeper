"""
Виджет бюджета
"""
from typing import Any, Callable
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QMessageBox
from bookkeeper.presenters.presenters import BudgetPresenter
from bookkeeper.models.budget import Budget
from bookkeeper.view.budget.budget_item import BudgetItem


class BudgetWidget(QWidget):
    """
    Виджет бюджета
    """
    budget_getter: Callable[[], Budget]
    budget_modifier: Callable[[Budget], None]
    expense_getter: Callable[[], list[float]]

    def __init__(self, expense_presenter: Any) -> None:
        super().__init__()
        self.expenses_table = QtWidgets.QTableWidget(3, 2)
        self.expenses_table.setHorizontalHeaderLabels(["Сумма ", "Бюджет "])
        self.expenses_table.setVerticalHeaderLabels(["День ", "Неделя ", "Месяц "])
        for i in range(2):
            self.expenses_table.horizontalHeader().setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeMode.Stretch if i == 1 else
                QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        budget = Budget()
        for i, l in zip(range(3), [1, 7, 30]):
            self.expenses_table.setItem(i, 1, BudgetItem(budget, l))
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Бюджет"))
        layout.addWidget(self.expenses_table)
        self.setLayout(layout)
        self.expense_presenter = expense_presenter
        for i in range(3):
            lost_item = QtWidgets.QTableWidgetItem()
            lost_item.setFlags(lost_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.expenses_table.setItem(i, 0, lost_item)
        self.sign = self.expenses_table.itemChanged
        self.sign.connect(self.edit_budget_event)
        self.presenter = BudgetPresenter(self)
        expenses = self.expense_getter()
        budget = self.budget_getter()
        self.update_expenses(expenses)
        self.update_budget(budget)

    def edit_budget_event(self, budget_item: BudgetItem) -> None:
        """
        Обработка изменения текстового значения бюджета
        """
        value = budget_item.get_value()
        if value is None:
            QMessageBox.critical(self, 'Ошибка', 'Используйте только числа.')
        else:
            budget_item.get().amount = value
            self.budget_modifier(budget_item.get())
        self.update_budget(budget_item.get())

    def update_expenses(self, exps: list[float]) -> None:
        """
        Обновить расходы
        """
        self.sign.disconnect()
        for i, expense in enumerate(exps):
            self.expenses_table.item(i, 0).setText(str(round(expense, 2)))
        self.sign.connect(self.edit_budget_event)

    def update_budget(self, budget: Budget) -> None:
        """
        Обновить бюджет
        """
        self.sign.disconnect()
        for i in range(3):
            it = self.expenses_table.item(i, 1)
            assert isinstance(it, BudgetItem)
            it.update(budget)
        self.sign.connect(self.edit_budget_event)

    def retrieve_expense(self) -> None:
        """
        Обёртка обновления расходов
        """
        self.update_expenses(self.expense_getter())

    def register_budget_getter(self, handler: Callable[[], Budget]) -> None:
        """
        Установить обработчик получения бюджета
        """
        self.budget_getter = handler

    def register_budget_modifier(self, handler: Callable[[Budget], None]) -> None:
        """
        Установить обработчик изменения бюджета
        """
        self.budget_modifier = handler

    def register_expense_getter(self, handler: Callable[[], list[float]]) -> None:
        """
        Установить обработчик получения расходов
        """
        self.expense_getter = handler
