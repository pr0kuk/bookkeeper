"""
Поля таблицы бюджета
"""
from PySide6.QtWidgets import QTableWidgetItem
from bookkeeper.models.budget import Budget


class BudgetItem(QTableWidgetItem):
    """
    Абстрактный класс поля бюджета
    """
    def __init__(self, budget: Budget, days: int):
        super().__init__()
        self.factor = days
        self.update(budget)

    def get(self) -> Budget:
        """
        Получить объект бюджета
        """
        return self.budget

    def get_value(self) -> None | float:
        """
        Получить значение по тексту
        """
        try:
            return float(self.text())/self.factor
        except ValueError:
            return None

    def update(self, budget: Budget) -> None:
        """
        Установить текст по значению
        """
        self.budget = budget
        self.setText(str(round(self.budget.amount*self.factor, 2)))