"""
Модуль описывает репозиторий, работающий с sqlite
"""

import sqlite3
import os
from typing import Any
from datetime import datetime
from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T


def convert_datetime(val: Any) -> datetime:
    """
    Сконвертировать дату формата ISO в объект типа datetime
    """
    return datetime.fromisoformat(val.decode())


def adapt_datetime(val: datetime) -> str:
    """
    Сконвертировать объект типа datetime в строку формата ISO
    """
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
        if 'pk' in self.fields:
            self.fields.pop('pk')
        self.cls_ty = ty
        self.table_name = ty.__name__.lower()
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        sqlite3.register_converter('timestamp', convert_datetime)
        sqlite3.register_adapter(datetime, adapt_datetime)
        with sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES) as con:
            vals = [(f'{x}', gettype(getattr(ty, x))) for x in self.fields]
            qstring = ', '.join([f'{x} {typ}' for x, typ in vals])
            query = (f'CREATE TABLE IF NOT EXISTS {self.table_name} '
                     f'(id INTEGER PRIMARY KEY, {qstring})')
            con.cursor().execute(query)

    def fill_object(self, res: Any) -> T:
        """
        Создать объект по данным из БД
        """
        obj: T = self.cls_ty()
        obj.pk = res[0]
        for x, r in zip(self.fields, res[1:]):
            setattr(obj, x, r)
        return obj

    def add(self, obj: T) -> int:
        """
        Добавить объект в репозиторий, вернуть id объекта,
        также записать id в атрибут pk.
        """
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'попытка добавить в БД {obj} с ненулевым pk')
        names = ', '.join(self.fields.keys())
        qmarks = ', '.join("?" * len(self.fields))
        vals = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES) as con:
            cur = con.cursor()
            cur.execute(
                f'INSERT INTO {
                    self.table_name} ({names}) VALUES ({qmarks})',
                vals)
            assert isinstance(cur.lastrowid, int)
            obj.pk = cur.lastrowid
        return obj.pk

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        with sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES) as con:
            res = con.cursor().execute(
                f'SELECT * FROM {self.table_name} WHERE id = {pk}').fetchone()
            if res is None:
                return None
            obj: T = self.fill_object(res)
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
            res = con.cursor().execute(query).fetchall()
            objs = [self.fill_object(r) for r in res]
        return objs

    def update(self, obj: Any) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        vals = tuple(getattr(obj, x) for x in self.fields)
        state = ', '.join([f'{col} = ?' for col in self.fields])
        with sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES) as con:
            if not self.find_obj(con.cursor(), obj.pk):
                raise ValueError(f'Couldnt find id={obj.pk} in DB.')
            con.cursor().execute(
                f'UPDATE {
                    self.table_name} SET {state} WHERE id = {
                    obj.pk}', vals)

    def find_obj(self, cur: Any, pk: int) -> bool:
        """
        Узнать есть ли запись в БД
        """
        res = cur.execute(f'SELECT * FROM {self.table_name} WHERE id = {pk}').fetchone()
        return res is not None

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        with sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES) as con:
            if not self.find_obj(con.cursor(), pk):
                raise KeyError(f'Couldnt find id={pk} in DB.')
            con.cursor().execute(f'DELETE FROM {self.table_name} WHERE id = {pk}')


def gettype(attr: Any) -> str:
    """
    Узнать тип аттрибута для БД
    """
    if isinstance(attr, int) or attr is None:
        return 'INTEGER'
    if isinstance(attr, float):
        return 'REAL'
    if isinstance(attr, datetime):
        return 'timestamp'
    return 'TEXT'
