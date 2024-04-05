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
        cat_edit_button = QPushButton("Выбрать")
        cat_edit_button.clicked.connect(self.button_clicked)
        layout.addWidget(cat_edit_button)
        self.setLayout(layout)

    def button_clicked(self):
        self.parent.table.add_exp_event()
        self.parent.table.close_category_window()
