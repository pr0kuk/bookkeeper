"""
Модуль описывает репозиторий, работающий с sqlite
"""

import sqlite3
from typing import Any
from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    Абстрактный репозиторий.
    Абстрактные методы:
    add
    get
    get_all
    update
    delete
    """

    def __init__(self, db_file: str, cls: type) -> None:
        """
        Конструктор репозитория
        """
        pass

    def add(self, obj: T) -> int:
        """
        Добавить объект в репозиторий, вернуть id объекта,
        также записать id в атрибут pk.
        """
        pass

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        pass

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        pass

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        pass

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        pass