from typing import Any, Callable
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QTreeWidgetItem, QMenu, QMessageBox
from bookkeeper.view.presenters import CategoryPresenter
from bookkeeper.models.category import Category
from .category_item import CategoryItem

class CategoryWidget(QWidget):
    category_changed = QtCore.Signal()
    category_adder: Callable[[Category], None]
    category_modifier: Callable[[Category], None]
    category_checker: Callable[[str], bool]
    category_deleter: Callable[[Category], None]
    category_finder: Callable[[str], None | int]

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Изменение категорий")
        layout = QtWidgets.QVBoxLayout()
        self.categories_widget = QtWidgets.QTreeWidget()
        self.categories_widget.setColumnCount(1)
        self.categories_widget.setHeaderLabel('Категории')
        layout.addWidget(self.categories_widget)
        self.setLayout(layout)
        self.presenter = CategoryPresenter(self)
        self.menu = QMenu(self)
        self.menu.addAction('Добавить').triggered.connect(self.add_category_event)
        self.menu.addAction('Удалить').triggered.connect(self.delete_category_event)
        self.sign = self.categories_widget.itemChanged
        self.sign.connect(self.edit_category_event)

    def open_window(self):
        self.edit_ctg = EditCtgWindow(self.cat_list)
        self.edit_ctg.show()