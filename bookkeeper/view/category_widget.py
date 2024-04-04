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

    def set_category_list(self, categories: list[Category]) -> None:
        table = self.categories_widget
        uniq_pk: dict[int, CategoryItem] = {}
        set_once: bool = False
        for x in categories:
            pk = x.pk
            parent = x.parent
            parent_category: Any = table
            if parent is not None:
                parent_category = uniq_pk.get(int(parent))
            category_item = CategoryItem(parent_category, x)
            uniq_pk.update({pk: category_item})
            if not set_once:
                table.setCurrentItem(category_item)
                set_once = True

    def contextMenuEvent(self, event: Any) -> None:
        self.menu.exec_(event.globalPos())

    def delete_category(self, category_item: CategoryItem, *_: int) -> None:
        root = self.categories_widget.invisibleRootItem()
        (category_item.parent() or root).removeChild(category_item)

    def rename_category(self, category_item: CategoryItem, column: int) -> None:
        category_item.setText(column, category_item.category.name)

    def set_err_category(self, category_item: CategoryItem, column: int) -> None:
        category_item.setText(column, f'"{category_item.text(column)}"_err ''не будет установлена')

    def edit_category_event(self, category_item: CategoryItem, column: int) -> None:
        entered_text = category_item.text(column)

        if category_item.category.pk == 0:
            action: Any = self.category_adder
            revert: Any = self.set_err_category
        else:
            action = self.category_modifier
            revert = self.rename_category

        if not self.category_checker(entered_text):
            self.sign.disconnect()
            revert(category_item, column)
            self.sign.connect(self.edit_category_event)
            QMessageBox.critical(self, 'Ошибка', f'Категория {entered_text} уже существует')
        else:
            category_item.update(entered_text)
            action(category_item.category)
            self.category_changed.emit()

    def add_category_event(self) -> None:
        category_items = self.categories_widget.selectedItems()
        if len(category_items) == 0:
            parent_item: Any = self.categories_widget
            parent_pk = None
        else:
            assert len(category_items) == 1
            parent_item = category_items.pop()
            parent_pk = parent_item.category.pk

        if parent_pk == 0:
            QMessageBox.critical(self, 'Ошибка', 'Создание подкатегории с ошибкой.')
            return

        self.sign.disconnect()
        new_category = CategoryItem(parent_item, Category(parent=parent_pk))
        self.sign.connect(self.edit_category_event)
        self.categories_widget.setCurrentItem(new_category)
        self.categories_widget.edit(self.categories_widget.currentIndex())
        

    def delete_category_event(self) -> None:
        category_item = self.categories_widget.currentItem()
        if category_item is None:
            return
        assert isinstance(category_item, CategoryItem)
        if category_item.category.pk == 0:
            self.delete_category(category_item)
            return

        self.delete_category(category_item)
        self.category_deleter(category_item.category)
        self.category_changed.emit()

    def get_selected_category(self) -> QTreeWidgetItem:
        return self.categories_widget.currentItem()

    def register_category_adder(self, handler: Callable[[Category], None]) -> None:
        self.category_adder = handler

    def register_category_modifier(self, handler: Callable[[Category], None]) -> None:
        self.category_modifier = handler

    def register_category_checker(self, handler: Callable[[str], bool]) -> None:
        self.category_checker = handler

    def register_category_deleter(self, handler: Callable[[Category], None]) -> None:
        self.category_deleter = handler

    def register_category_finder(self, handler: Callable[[str], None | int]) -> None:
        self.category_finder = handler