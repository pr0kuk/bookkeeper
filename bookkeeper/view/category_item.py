"""
Элементы дерева категорий
"""
from typing import Any
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem
from bookkeeper.models.category import Category


class CategoryItem(QTreeWidgetItem):
    """
    Класс элемента дерева категорий
    """

    def __init__(self, parent: Any, category: Category):
        super().__init__(parent, [category.name])
        self.setFlags(self.flags() | Qt.ItemIsEditable)
        self.category = category

    def update(self, name: str) -> None:
        """
        Установить имя категории
        """
        self.category.name = name

    def __str__(self) -> str:
        """
        Получить имя категории
        """
        return self.category.name
