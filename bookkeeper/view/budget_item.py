from PySide6.QtWidgets import QTableWidgetItem
from bookkeeper.models.budget import Budget


class BudgetItem(QTableWidgetItem):
    def __init__(self, budget: Budget):
        super().__init__()
        self.update(budget)

    def get(self) -> Budget:
        return self.budget


class BudgetDayItem(BudgetItem):
    def get_value(self) -> None | float:
        try:
            return float(self.text())
        except ValueError:
            return None

    def update(self, budget: Budget) -> None:
        self.budget = budget
        self.setText(str(round(self.budget.amount, 2)))


class BudgetWeekItem(BudgetItem):
    def get_value(self) -> None | float:
        try:
            return float(self.text()) / 7
        except ValueError:
            return None

    def update(self, budget: Budget) -> None:
        self.budget = budget
        self.setText(str(round(self.budget.amount * 7, 2)))


class BudgetMonthItem(BudgetItem):
    def get_value(self) -> None | float:
        try:
            return float(self.text()) / 30
        except ValueError:
            return None

    def update(self, budget: Budget) -> None:
        self.budget = budget
        self.setText(str(round(self.budget.amount * 30, 2)))
