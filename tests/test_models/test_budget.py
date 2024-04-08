"""
Тесты для категорий расходов
"""

import pytest

from bookkeeper.models.budget import Budget


def test_create_object():
    b = Budget()
    assert b.amount == 0.0
    assert b.pk == 0


def test_reassign():
    """
    class should not be frozen
    """
    b = Budget()
    b.amount = 2.0
    b.pk = 1
    assert b.amount == 2.0
    assert b.pk == 1


def test_eq():
    """
    class should implement __eq__ method
    """
    b1 = Budget()
    b2 = Budget()
    assert b1 == b2