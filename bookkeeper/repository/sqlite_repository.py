"""
Модуль описывает репозиторий, работающий с sqlite
"""

import sqlite3
from typing import Any
from datetime import datetime
from bookkeeper.repository.abstract_repository import AbstractRepository, T
from itertools import count

class Custom():
        pk: int = 0
        name: str = "TEST"
        value: int = 24
        date: datetime = datetime.now()
        real: float = 2.5

        def __str__(self) -> str:
            return f'pk={self.pk} name={self.name} value={self.value}'

        def __eq__(self, other) -> bool:
            return self.pk == other.pk and self.name == other.name and self.value == other.value


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

def forcetostring(value: str | int) -> str | int:
    """Sets decoration to string value.
    """
    if isinstance(value, str):
        return f'\'{value}\''
    return value

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

    def __init__(self, db_file: str) -> None:
        """
        Конструктор репозитория
        """
        self._container: dict[Custom, T] = {}
        self._counter = count(1)
        self.db_file = db_file
        self.table_name = 'custom_class'
        self.fields = {'name' :'', 'value' : 0,'date':None, 'real' : 0.0}
        with sqlite3.connect(self.db_file) as con:
            query = (f'CREATE TABLE IF NOT EXISTS {self.table_name} 'f'(id INTEGER PRIMARY KEY, name TEXT, value INTEGER, date timestamp, real REAL)')
            con.cursor().execute(query)

    def fill_object(self, result: Any) -> T:
        """
        Создать объект по данным из БД
        """
        obj = Custom()
        obj.pk = result[0]
        for x, res in zip(self.fields, result[1:]):
            setattr(obj, x, res)
        return obj

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
        self._container[obj.pk] = obj
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
        query = f'SELECT * FROM {self.table_name}'
        condition = ''
        if where is not None:
            condition = ' WHERE'
            for key, val in where.items():
                condition += f' {key} = {forcetostring(val)} AND'
            query += condition.rsplit(' ', 1)[0]
        with sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
            results = con.cursor().execute(query).fetchall()
            objs = [self.fill_object(result) for result in results]
        return objs

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        pass

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        pass