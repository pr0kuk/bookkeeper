"""
Элементы таблицы расходов
"""
from datetime import datetime
from typing import Any
from PySide6.QtWidgets import QTableWidgetItem
from bookkeeper.models.expense import Expense


class ExpenseRow:
    """
    Класс ряда таблицы
    """

    def __init__(self, expense: Expense):
        self.expense = expense


class ExpenseItem(QTableWidgetItem):
    """
    Абстрактный класс поля таблицы расходов
    """

    def __init__(self, row: ExpenseRow):
        super().__init__()
        self.trow = row
        self.restore()

    def validate(self) -> bool:
        """
        Проверка корректности значения
        """
        return True

    def restore(self) -> None:
        """
        Установка текста по значению
        """
        self.setText(self.trow.expense.comment)

    def update(self) -> None:
        """
        Установка значения по тексту
        """
        self.trow.expense.comment = self.text()

    def get_err_msg(self) -> str:
        """
        Получить сообщение об ошибке
        """
        return ''

    def should_emit_on_upd(self) -> bool:
        """
        Флаг для работы с Qt сигналами
        """
        return False


class ExpenseAmountItem(ExpenseItem):
    """
    Класс поля таблицы расходов для значения
    """

    def validate(self) -> bool:
        """
        Проверка корректности значения
        """
        try:
            float(self.text())
        except ValueError:
            return False
        return True

    def restore(self) -> None:
        """
        Установка текста по значению
        """
        self.setText(str(round(self.trow.expense.amount, 2)))

    def update(self) -> None:
        """
        Установка значения по тексту
        """
        self.trow.expense.amount = round(float(self.text()), 2)

    def get_err_msg(self) -> str:
        """
        Получить сообщение об ошибке
        """
        return 'Нужно ввести действительное число.'

    def should_emit_on_upd(self) -> bool:
        """
        Флаг для работы с Qt сигналами
        """
        return True


class ExpenseCategoryItem(ExpenseItem):
    """
    Класс поля таблицы расходов для категории
    """

    def __init__(self, row: ExpenseRow, expense_view: Any):
        self.category_view = expense_view.category_view
        self.retriever = expense_view.category_retriever
        super().__init__(row)

    def validate(self) -> bool:
        """
        Проверка корректности значения
        """
        category_name = self.text()
        return not self.category_view.category_checker(category_name)

    def restore(self) -> None:
        """
        Установка текста по значению
        """
        category = self.retriever(self.trow.expense.category)
        if category is None:
            category_item = self.category_view.get_selected_category()
            if category_item is None or category_item.category.pk == 0:
                raise ValueError('Категория не установлена')
            category = category_item.category.name
            self.trow.expense.category = category_item.category.pk
        self.setText(category)

    def update(self) -> None:
        """
        Установка значения по тексту
        """
        pk = self.category_view.category_finder(self.text())
        assert pk is not None
        self.trow.expense.category = pk

    def get_err_msg(self) -> str:
        """
        Получить сообщение об ошибке
        """
        return 'Нужно ввести существующую категорию.'


class ExpenseDateItem(ExpenseItem):
    """
    Класс поля таблицы расходов для даты
    """
    fmt = "%Y-%m-%d %H:%M:%S"

    def validate(self) -> bool:
        """
        Проверка корректности значения
        """
        date_str = self.text()
        try:
            datetime.fromisoformat(date_str)
        except ValueError:
            return False
        return True

    def restore(self) -> None:
        """
        Установка текста по значению
        """
        date = self.trow.expense.expense_date
        self.setText(date.strftime(self.fmt))

    def get_err_msg(self) -> str:
        """
        Получить сообщение об ошибке
        """
        return f'Неверный формат даты.\nИспользуйте {self.fmt}'

    def update(self) -> None:
        """
        Установка значения по тексту
        """
        self.trow.expense.expense_date = datetime.fromisoformat(self.text())

    def should_emit_on_upd(self) -> bool:
        """
        Флаг для работы с Qt сигналами
        """
        return True
