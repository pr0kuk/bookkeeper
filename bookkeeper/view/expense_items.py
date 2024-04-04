from datetime import datetime
from typing import Any
from PySide6.QtWidgets import QTableWidgetItem
from bookkeeper.models.expense import Expense

class ExpenseRow:
    def __init__(self, expense: Expense):
        self.expense = expense

class ExpenseItem(QTableWidgetItem):
    def __init__(self, row: ExpenseRow):
        super().__init__()
        self.trow = row
        self.restore()

    def validate(self) -> bool:
        return True

    def restore(self) -> None:
        self.setText(self.trow.expense.comment)

    def update(self) -> None:
        self.trow.expense.comment = self.text()

    def get_err_msg(self) -> str:
        return ''

    def should_emit_on_upd(self) -> bool:
        return False
