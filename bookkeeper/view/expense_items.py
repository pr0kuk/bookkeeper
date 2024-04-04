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


class ExpenseAmountItem(ExpenseItem):
    def validate(self) -> bool:
        try:
            float(self.text())
        except ValueError:
            return False
        return True

    def restore(self) -> None:
        self.setText(str(round(self.trow.expense.amount, 2)))

    def update(self) -> None:
        self.trow.expense.amount = round(float(self.text()), 2)

    def get_err_msg(self) -> str:
        return 'Нужно ввести действительное число.'

    def should_emit_on_upd(self) -> bool:
        return True

class ExpenseCategoryItem(ExpenseItem):
    def __init__(self, row: ExpenseRow, exp_view: Any):
        self.category_view = exp_view.category_view
        self.retriever = exp_view.category_retriever
        super().__init__(row)
class ExpenseDateItem(ExpenseItem):
    fmt = "%Y-%m-%d %H:%M:%S"
