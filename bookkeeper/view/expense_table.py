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
    
    def add_expense(self, expense: Expense) -> None:
        row = ExpenseRow(expense)
        category_item = ExpenseCategoryItem(row, self.parent)
        rcount = self.rowCount()
        self.setRowCount(rcount+1)
        self.sign.disconnect()
        self.setItem(rcount, 0, ExpenseDateItem(row))
        self.setItem(rcount, 1, ExpenseAmountItem(row))
        self.setItem(rcount, 2, category_item)
        self.setItem(rcount, 3, ExpenseItem(row))
        self.sign.connect(self.update_exp_event)

    def delete_exp_event(self) -> None:
        row = self.currentRow()
        if row == -1:
            return
        titem = self.item(row, 0)
        self.removeRow(row)
        assert isinstance(titem, ExpenseItem)
        exp_to_del = titem.trow.expense
        self.parent.exp_deleter(exp_to_del)
        self.parent.emit_exp_changed()

    def add_exp_event(self) -> None:
        expense = Expense()
        try:
            self.add_expense(expense)
        except ValueError as valerr:
            QMessageBox.critical(self, 'Ошибка', f'{valerr}')
            return
        self.parent.exp_adder(expense)
        self.parent.emit_exp_changed()
