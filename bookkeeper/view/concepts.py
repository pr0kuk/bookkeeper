from typing import Protocol, Callable
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
class ExpenseConcept(Protocol):
    def register_exp_adder(self, handler: Callable[[Expense], None]) -> None:
        pass
    def register_exp_deleter(self, handler: Callable[[Expense], None]) -> None:
        pass
    def register_exp_modifier(self, handler: Callable[[Expense], None]) -> None:
        pass
    def register_category_retriever(self, handler: Callable[[int], str | None]) -> None:
        pass
    def set_exp_list(self, data: list[Expense]) -> None:
        pass
class CategoryConcept(Protocol):
    def set_category_list(self, categories: list[Category]) -> None:
        pass
    def register_category_modifier(self, handler: Callable[[Category], None]) -> None:
        pass
    def register_category_adder(self, handler: Callable[[Category], None]) -> None:
        pass
    def register_category_checker(self, handler: Callable[[str], bool]) -> None:
        pass
    def register_category_finder(self, handler: Callable[[str], None | int]) -> None:
        pass
    def register_category_deleter(self, handler: Callable[[Category], None]) -> None:
        pass
class BudgetConcept(Protocol):
    exp_presenter: ExpenseConcept
    def register_bgt_modifier(self, handler: Callable[[Budget], None]) -> None:
        pass
    def register_bgt_getter(self, handler: Callable[[], Budget]) -> None:
        pass
    def register_exp_getter(self, handler: Callable[[], list[float]]) -> None:
        pass