from .expense_items import ExpenseAmountItem, ExpenseCategoryItem, ExpenseItem, ExpenseRow, ExpenseDateItem
from typing import Any
from PySide6.QtWidgets import QTableWidget, QMenu, QMessageBox, QHeaderView
from bookkeeper.models.expense import Expense

class Table(QTableWidget):
    def __init__(self, parent: Any):
        super().__init__()
        self.parent = parent
        self.setColumnCount(4)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(["Дата ", "Сумма ", "Категория ", "Комментарий"])
        for i in range(4):
            self.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch if i == 3 else QHeaderView.ResizeToContents)
        self.menu = QMenu(self)
        self.menu.addAction('Добавить').triggered.connect(self.open_category_window)
        self.menu.addAction('Удалить').triggered.connect(self.delete_exp_event)
        self.sign = self.itemChanged
        self.sign.connect(self.update_exp_event)

    def open_category_window(self):
        self.parent.edit_category_window.show()

    def close_category_window(self):
        self.parent.edit_category_window.close()
    
