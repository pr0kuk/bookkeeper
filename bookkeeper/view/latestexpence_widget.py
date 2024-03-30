"""
Widget of latest expences
"""
RowCount = 10

from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget, QTableWidget)

def set_data(table: QTableWidget, data: list[list[str]]) -> None:
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            table.setItem(i, j, QtWidgets.QTableWidgetItem(x.capitalize()))


class ExpenceWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        header = QtWidgets.QLabel("Последние расходы")
        table = QtWidgets.QTableWidget(RowCount, 4)
        table.setHorizontalHeaderLabels(["Дата ", "Сумма ", "Категория ", "Комментарий"])
        header = table.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch if i == 3 else QtWidgets.QHeaderView.ResizeToContents)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        set_data(table, [])
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(header)
        layout.addWidget(table)
        self.setLayout(layout)