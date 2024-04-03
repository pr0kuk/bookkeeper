from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem
from typing import Any
from PySide6.QtWidgets import QTreeWidgetItem
from bookkeeper.models.category import Category

class CategoryItem(QTreeWidgetItem):
    def __init__(self, parent: Any, category: Category):
        super().__init__(parent, [category.name])
        self.setFlags(self.flags() | Qt.ItemIsEditable)
        self.category = category

    def update(self, name: str) -> None:
        self.category.name = name

    def __str__(self) -> str:
        return self.category.name