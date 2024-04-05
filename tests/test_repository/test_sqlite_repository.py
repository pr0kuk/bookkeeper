from bookkeeper.repository.sqlite_repository import SQLiteRepository
from os import remove
import pytest
from datetime import datetime


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


@pytest.fixture
def custom_class():
    return Custom


@pytest.fixture
def repo():
    try:
        remove("data/sqlite.db")
    except BaseException:
        pass
    return SQLiteRepository("data/sqlite.db", Custom)


def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(1)


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects


def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.name = str(i)
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'name': '0'}) == [objects[0]]
