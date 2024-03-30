"""
Budget Widget
"""
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QVBoxLayout, QAbstractItemView

def set_data(table: QTableWidget, spent: list[float], day_budget: float) -> None:
    budget = [day_budget, day_budget * 7, day_budget * 30]
    for i, [lost, limit] in enumerate(zip(spent, budget)):
        table.setItem(i, 0, QTableWidgetItem(str(lost)))
        table.setItem(i, 1, QTableWidgetItem(str(limit)))

class BudgetWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        table = QTableWidget(3, 2)
        table.setHorizontalHeaderLabels(["Сумма ", "Бюджет "])
        table.setVerticalHeaderLabels(["День ", "Неделя ", "Месяц "])
        for i in range(2):
            table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch if i == 1 else QHeaderView.ResizeToContents)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        set_data(table, [0, 0, 0], 1)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Бюджет"))
        layout.addWidget(table)
        self.setLayout(layout)