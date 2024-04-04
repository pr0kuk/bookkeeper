"""
Latest expences Widget
"""
RowCount = 10
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QVBoxLayout, QAbstractItemView



class ExpenceWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
