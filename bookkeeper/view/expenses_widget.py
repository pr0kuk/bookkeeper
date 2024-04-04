from typing import Callable
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QMessageBox
from bookkeeper.view.category_widget import CategoryWidget
from bookkeeper.view.presenters import ExpensePresenter
from bookkeeper.models.expense import Expense
from .expense_table import Table
from .category_window import EditCategoryWindow
class ExpenseWidget(QWidget):
    expense_changed = QtCore.Signal()
    category_retriever: Callable[[int], None | str]
    expense_adder: Callable[[Expense], None]
    expense_deleter: Callable[[Expense], None]
    expense_modifier: Callable[[Expense], None]

    def __init__(self, category_view: CategoryWidget) -> None:
        super().__init__()
        self.category_view = category_view
        layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Последние расходы")
        layout.addWidget(message)
        self.table = Table(self)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.presenter = ExpensePresenter(self)
        self.edit_category_window = EditCategoryWindow(self)


