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

    def set_expense_list(self, data: list[Expense]) -> None:
        list_to_delete: list[Expense] = []
        for x in data:
            try:
                self.table.add_expense(x)
            except ValueError as vallerr:
                QMessageBox.critical(self, 'Ошибка',f'{vallerr}.\nЗапись 'f'{x.expense_date.strftime("%Y-%m-%d %H:%M:%S")}'' будет удалена.')
                list_to_delete.append(x)
        for x in list_to_delete:
            self.expense_deleter(x)

