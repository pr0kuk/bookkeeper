"""
Frame Window
"""
from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget)
from .latestexpenses_widget import ExpenceWidget
from .budget_widget import BudgetWidget
from .edit_widget import EditWidget

class Frame(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Bookkeeper")
        layout = QtWidgets.QVBoxLayout()
        for w in [ExpenceWidget(), BudgetWidget(), EditWidget()]:
            layout.addWidget(w)
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)