"""
Модуль описывает репозиторий, работающий с sqlite
"""

import sqlite3
import os
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


def convert_datetime(val: Any) -> datetime:
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.fromisoformat(val.decode())


def adapt_datetime(val: datetime) -> str:
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return val.isoformat()


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

    def __init__(self, db_file: str, ty: type) -> None:
        """
        Конструктор репозитория
        """
        self.db_file = db_file
        self.table_name = ty.__name__.lower()
        self.fields = get_annotations(ty, eval_str=True)
        self.fields.pop('pk')
        self.cls_ty = ty
        self.table_name = ty.__name__.lower()
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        sqlite3.register_converter('timestamp', convert_datetime)
        sqlite3.register_adapter(datetime, adapt_datetime)
        with sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES) as con:
            values = [(f'{x}', gettype(getattr(ty, x))) for x in self.fields]
            qstring = ', '.join([f'{x} {typ}' for x, typ in values])
            query = (f'CREATE TABLE IF NOT EXISTS {self.table_name} '
                     f'(id INTEGER PRIMARY KEY, {qstring})')
            con.cursor().execute(query)

    def fill_object(self, result: Any) -> T:
        """
        Создать объект по данным из БД
        """
        obj: T = self.cls_ty()
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
        with sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES) as con:
            cur = con.cursor()
            cur.execute(
                f'INSERT INTO {
                    self.table_name} ({names}) VALUES ({qmarks})',
                values)
            assert isinstance(cur.lastrowid, int)
            obj.pk = cur.lastrowid
        return obj.pk

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        with sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES) as con:
            result = con.cursor().execute(
                f'SELECT * FROM {self.table_name} WHERE id = {pk}').fetchone()
            if result is None:
                return None
            obj: T = self.fill_object(result)
        return obj

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
                condition += f' {key} = {val} AND'
            query += condition.rsplit(' ', 1)[0]
        with sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES) as con:
            results = con.cursor().execute(query).fetchall()
            objs = [self.fill_object(result) for result in results]
        return objs

    def update(self, obj: Any) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        values = tuple(getattr(obj, x) for x in self.fields)
        upd_stm = ', '.join([f'{col} = ?' for col in self.fields])
        with sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES) as con:
            if not self.is_pk_in_db(con.cursor(), obj.pk):
                raise ValueError(f'No object with id={obj.pk} in DB.')
            con.cursor().execute(
                f'UPDATE {
                    self.table_name} SET {upd_stm} WHERE id = {
                    obj.pk}', values)

    def is_pk_in_db(self, cur: Any, pk: int) -> bool:
        """
        Узнать есть ли запись в БД
        """
        res = cur.execute(f'SELECT * FROM {self.table_name} WHERE id = {pk}').fetchone()
        return res is not None

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        with sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES) as con:
            if not self.is_pk_in_db(con.cursor(), pk):
                raise KeyError(f'No object with id={pk} in DB.')
            con.cursor().execute(f'DELETE FROM {self.table_name} WHERE id = {pk}')
