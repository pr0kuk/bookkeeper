"""
Category Window
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class EditCategoryWindow(QWidget):
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Изменение категорий")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Категории"))
        layout.addWidget(self.parent.category_view)
        ch_button = QPushButton("Выбрать")
        ch_button.clicked.connect(self.ch_button_clicked)
        ad_button = QPushButton("Новая категория")
        ad_button.clicked.connect(self.ad_button_clicked)
        layout.addWidget(ch_button)
        layout.addWidget(ad_button)
        self.setLayout(layout)

    def ch_button_clicked(self):
        self.parent.table.add_expense_event()
        self.parent.table.close_category_window()

    def ad_button_clicked(self):
        self.parent.category_view.add_supercategory()