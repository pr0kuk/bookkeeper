from typing import Any, Callable
from .budget_item import BudgetDayItem, BudgetMonthItem, BudgetWeekItem, BudgetItem
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QMessageBox
from bookkeeper.view.presenters import BudgetPresenter
from bookkeeper.models.budget import Budget

class BudgetWidget(QWidget):
    budget_getter: Callable[[], Budget]
    budget_modifier: Callable[[Budget], None]
    exp_getter: Callable[[], list[float]]

    def __init__(self, expense_presenter: Any) -> None:
        super().__init__()
        self.expenses_table = QtWidgets.QTableWidget(3, 2)
        self.expenses_table.setHorizontalHeaderLabels(["Сумма ", "Бюджет "])
        self.expenses_table.setVerticalHeaderLabels(["День ", "Неделя ", "Месяц "])
        for i in range(2):
            self.expenses_table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch if i == 1 else QtWidgets.QHeaderView.ResizeToContents)
        budget = Budget()
        for i,l in zip(range(3), [BudgetDayItem, BudgetWeekItem, BudgetMonthItem]):
            self.expenses_table.setItem(i, 1, l(budget))
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Бюджет"))
        layout.addWidget(self.expenses_table)
        self.setLayout(layout)
        self.expense_presenter = expense_presenter
        for i in range(3):
            lost_item = QtWidgets.QTableWidgetItem()
            lost_item.setFlags(lost_item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.expenses_table.setItem(i, 0, lost_item)
        self.sign = self.expenses_table.itemChanged
        self.sign.connect(self.edit_budget_event)
        self.presenter = BudgetPresenter(self)
        expenses = self.expense_getter()
        budget = self.budget_getter()
        self.update_expenses(expenses)
        self.update_budget(budget)