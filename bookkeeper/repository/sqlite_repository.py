"""
Модуль описывает репозиторий, работающий с sqlite
"""

import sqlite3
from typing import Any
from datetime import datetime
from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T


def gettype(attr: Any) -> str:
    """
    Узнать типа аттрибута для БД
    """
    if isinstance(attr, int) or attr is None:
        return 'INTEGER'
    if isinstance(attr, float):
        return 'REAL'
    if isinstance(attr, datetime):
        return 'timestamp'
    if isinstance(attr, bytes):
        return 'BLOB'
    return 'TEXT'

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
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        if 'pk' in self.fields:
            self.fields.pop('pk')
        self.cls_ty = cls
        with sqlite3.connect(self.db_file) as con:
            query = (f'CREATE TABLE IF NOT EXISTS {self.table_name} 'f'(id INTEGER PRIMARY KEY, name TEXT, value INTEGER, date timestamp, real REAL)')
            con.cursor().execute(query)

    def add(self, obj: T) -> int:
        """
        Добавить объект в репозиторий, вернуть id объекта,
        также записать id в атрибут pk.
        """
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        names = ', '.join(self.fields.keys())
        qmarks = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({qmarks})',
                values
            )
            assert isinstance(cur.lastrowid, int)
            obj.pk = cur.lastrowid
        return obj.pk

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