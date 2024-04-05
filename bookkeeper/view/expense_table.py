"""
Таблица Расходов
"""
from typing import Any
from PySide6.QtWidgets import QTableWidget, QMenu, QMessageBox, QHeaderView
from bookkeeper.models.expense import Expense
from .expense_items import (ExpenseAmountItem, ExpenseCategoryItem, ExpenseItem,
                            ExpenseDateItem)


class Table(QTableWidget):
    """
    Класс таблицы расходов
    """

    def __init__(self, widget_parent: Any):
        super().__init__()
        self.widget_parent = widget_parent
        self.setColumnCount(4)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(["Дата ", "Сумма ", "Категория ", "Комментарий"])
        for i in range(4):
            self.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.Stretch if i == 3 else
                QHeaderView.ResizeMode.ResizeToContents)
        self.menu = QMenu(self)
        self.menu.addAction('Добавить').triggered.connect(self.open_category_window)
        self.menu.addAction('Удалить').triggered.connect(self.delete_expense_event)
        self.sign = self.itemChanged
        self.sign.connect(self.update_expense_event)

    def open_category_window(self) -> None:
        """
        Открыть окно категорий
        """
        self.widget_parent.edit_category_window.show()

    def close_category_window(self) -> None:
        """
        Закрыть окно категория
        """
        self.widget_parent.edit_category_window.close()

    def update_expense_event(self, expense_item: ExpenseItem) -> None:
        """
        Обновить расход
        """
        if not expense_item.validate():
            self.sign.disconnect()
            QMessageBox.critical(self, 'Ошибка', expense_item.get_err_msg())
            expense_item.restore()
            self.sign.connect(self.update_expense_event)
            return

        expense_item.update()
        if isinstance(expense_item, ExpenseAmountItem):
            self.sign.disconnect()
            expense_item.restore()
            self.sign.connect(self.update_expense_event)

        if expense_item.should_emit_on_upd():
            self.widget_parent.emit_expense_changed()

        self.widget_parent.expense_modifier(expense_item.expense)

    def add_expense(self, expense: Expense) -> None:
        """
        Добавить расход
        """

        category_item = ExpenseCategoryItem(expense, self.widget_parent)
        rcount = self.rowCount()
        self.setRowCount(rcount + 1)
        self.sign.disconnect()
        self.setItem(rcount, 0, ExpenseDateItem(expense))
        self.setItem(rcount, 1, ExpenseAmountItem(expense))
        self.setItem(rcount, 2, category_item)
        self.setItem(rcount, 3, ExpenseItem(expense))
        self.sign.connect(self.update_expense_event)

    def delete_expense_event(self) -> None:
        """
        Обработка нажатия на кнопку удалить
        """
        row = self.currentRow()
        if row == -1:
            return
        titem = self.item(row, 0)
        self.removeRow(row)
        assert isinstance(titem, ExpenseItem)
        expense_to_del = titem.expense
        self.widget_parent.expense_deleter(expense_to_del)
        self.widget_parent.emit_expense_changed()

    def add_expense_event(self) -> None:
        """
        Обработка нажатия на кнопку добавить
        """
        expense = Expense()
        try:
            self.add_expense(expense)
        except ValueError as valerr:
            QMessageBox.critical(self, 'Ошибка', f'{valerr}')
            return
        self.widget_parent.expense_adder(expense)
        self.widget_parent.emit_expense_changed()

    def contextMenuEvent(self, event: Any) -> None:
        """
        Обработка контекстного меню
        """
        self.menu.exec_(event.globalPos())

    def update_categories(self) -> None:
        """
        Обновить все категории
        """
        try:
            for row in range(self.rowCount()):
                titem = self.item(row, 2)
                assert isinstance(titem, ExpenseItem)
                titem.restore()
        except ValueError as vallerr:
            QMessageBox.critical(self, 'Ошибка', f'{vallerr}')
