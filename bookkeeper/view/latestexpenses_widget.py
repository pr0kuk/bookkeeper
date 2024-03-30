"""
Latest expences Widget
"""
RowCount = 10
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QVBoxLayout, QAbstractItemView

def set_data(table: QTableWidget, data: list[list[str]]) -> None:
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            table.setItem(i, j, QTableWidgetItem(x.capitalize()))


class ExpenceWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        table = QTableWidget(RowCount, 4)
        table.setHorizontalHeaderLabels(["Дата ", "Сумма ", "Категория ", "Комментарий"])
        for i in range(4):
            table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch if i == 3 else QHeaderView.ResizeToContents)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        set_data(table, [])
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Последние расходы"))
        layout.addWidget(table)
        self.setLayout(layout)